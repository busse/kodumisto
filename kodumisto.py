import os
import re
import time

from dotenv import load_dotenv

import requests

from github import Github
import openai

import json
import base64
import random
import string



load_dotenv()
random_string = int(time.time())
issue_number = 41  # Set the issue number you want to read -- TODO(busse): Command line arg

# Set personal access tokens and repository details
openai_access_token = os.getenv("OPENAI_ACCESS_TOKEN")
github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
repo_owner = os.getenv("REPO_OWNER") # TODO(busse): Command line arg
repo_name = os.getenv("REPO_NAME") # TODO(busse): Command line arg

def get_filetype_prompt(string):
    # Find the index of the first newline character
    newline_index = string.find('\n')
    if newline_index == -1:
        # If there is no newline character, return the whole string as the first line
        return string, ''
    else:
        # Split the string at the newline character
        file_extension = string[:newline_index]
        prompt_body = string[newline_index+1:]
        return file_extension, prompt_body

def determine_file_action(issue_body):
    # Issues where the intent is to create a new file should start with the desired extension, ex:
    #  .py
    #  .csv
    #  .md
    # 
    # Note that the actual scripting or output formatting should still be specified in the Issue;
    #   The first line is not passed to the Prompt
    if issue_body.startswith("."):
        return "create"
    elif issue_body.startswith("http"):
        return "edit"
    else:
        return "create-no-extension"

# For edits: The following three functions help parse the Issue body to get the file to edit
def extract_url(text):
    regex = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+(/[^\s]*)?'
    match = re.search(regex, text)
    if match:
        return match.group()
    return None

def convert_url_to_raw(text):
    strip_blob = text.replace("blob/", "")
    change_domain = strip_blob.replace("github.com", "raw.githubusercontent.com")
    return change_domain

def extract_filename(url, branch):
    parts = url.split("/")
    try:
        branch_index = parts.index(branch)
    except ValueError:
        return None

    path_parts = parts[branch_index + 1:]
    path = "/".join(path_parts)

    return path


def main():


    # Initialize the GitHub client
    gh = Github(github_access_token)
    repo = gh.get_repo(f"{repo_owner}/{repo_name}")

    # Construct the GitHub API URL
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}"

    # Set the request headers with the GitHub access token
    headers = {
        "Authorization": f"token {github_access_token}"
    }

    # Send a GET request to the GitHub API
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        issue_data = response.json()
        issue_body = issue_data["body"]

        file_action = determine_file_action(issue_body)

        # We only need a file extension if adding a new file
        if file_action == "create":
            file_extension, prompt_body = get_filetype_prompt(issue_body)

            #Set the prompt for an add
            prompt = f"{prompt_body}"

        # If it's an edit, we need to get the file path/name
        elif file_action == "edit":
            issue_branch = "main" # TODO(busse): Possible future logic to get files from branches other than main
            file_url = convert_url_to_raw(extract_url(issue_body))
            file_name = extract_filename(file_url, issue_branch)

            # Send a GET request to the GitHub API
            response_file = requests.get(file_url)

            # Check if the request was successful
            if response_file.status_code == 200:
                #file_data = f"{response_file.text}"
            
                #Set the prompt for an edit
                prompt = f"Ignoring any URLs here, apply these instructions: {issue_body}\n\nTo this code: {response_file.text}\n\nReturn only code in your response."
            else:
                print("Error fetching file:", response.status_code)
        
        else:
            print("Error fetching issue data:", response.status_code)


        # Initialize the OpenAI client
        openai.api_key = openai_access_token

        # Set the options for the OpenAI client

        model = "gpt-4" # TODO(busse): Command line arg

        # Send the issue body as a request to ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-4", # TODO(busse): Command line arg
            messages=[
                {"role": "user", "content": f"{prompt}"}
            ]
        )

        # Write the ChatGPT response to the console
        chatgpt_response = response.choices[0].message.content
        print("ChatGPT response:", chatgpt_response)

        # Create a new branch
        branch_name = f"chatgpt-{model}-response-{issue_number}-{random_string}"
        base_branch = repo.get_branch("main")
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_branch.commit.sha)

        # If the Issue asks for a new file, create it
        if file_action == "create":
            # Create a new file with the ChatGPT response
            file_name = f"chatgpt-{model}-response-{issue_number}-{random_string}{file_extension}"
            repo.create_file(
                path=file_name,
                message=f"Add ChatGPT `{model}` response for issue #{issue_number}",
                content=chatgpt_response.encode("utf-8"),
                branch=branch_name,
            )

        elif file_action == "edit":
            #Get the file's content and SHA
            file_path = file_name
            file_contents = repo.get_contents(file_path, ref="main")
            #file_data = file_contents.decoded_content.decode("utf-8")
            file_sha = file_contents.sha

            # Update the file with the ChatGPT response
            new_file_data = f"{chatgpt_response}"
            repo.update_file(
                path=file_path,
                message=f"Update `{file_path}` with ChatGPT `{model}` response for issue {issue_number}",
                content=new_file_data.encode("utf-8"),
                #content=new_file_data,
                sha=file_sha,
                branch=branch_name,
            )

        # Create a pull request
        pr_title = f"ChatGPT {model} response for issue #{issue_number}"
        pr_body = f"Pull request containing the ChatGPT `{model}` response for issue #{issue_number}:\n\n{chatgpt_response}"
        base = "main"
        head = branch_name
        pr = repo.create_pull(title=pr_title, body=pr_body, head=head, base=base)
        print(f"Successfully created pull request {pr.number}: {pr.title}")

    else:
        print("Error fetching issue data:", response.status_code)

if __name__ == "__main__":
    main()
