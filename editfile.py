import requests
import json
import openai
import os
from dotenv import load_dotenv
import base64
from github import Github
import random
import string
import time
import re

load_dotenv()

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

random_string = int(time.time()) 

# Set your personal access tokens and repository details
openai_access_token = os.getenv("OPENAI_ACCESS_TOKEN")
github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
repo_owner = os.getenv("REPO_OWNER")
repo_name = os.getenv("REPO_NAME")

issue_number = 41  # Set the issue number you want to read

# Initialize the OpenAI client
openai.api_key = openai_access_token

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
    issue_branch = "main"



    print(extract_url(issue_body))
    

else:
    print("Error fetching issue data:", response.status_code)

file_url = convert_url_to_raw(extract_url(issue_body))
file_name = extract_filename(file_url, issue_branch)

print(file_url)
print(file_name)

# Send a GET request to the GitHub API
response_file = requests.get(file_url)


# Check if the request was successful
if response_file.status_code == 200:
    file_data = f"{response_file.text}"
    print(file_data)


 # Set the options for the OpenAI client
    prompt = f"Ignoring any URLs here, apply these instructions: {issue_body}\n\nTo this code: {response_file.text}\n\nReturn only code in your response."
    model = "gpt-3.5-turbo"
    tokens = 100  # The number of tokens to generate
    temperature = 0.8  # The higher the value, the more random the output

    print("Prompt:", prompt)

    # Send the issue body as a request to ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        #model="gpt-4",
        messages=[
            {"role": "user", "content": f"{prompt}"}
        ]
    )

    # Write the ChatGPT response to the console
    chatgpt_response = response.choices[0].message.content
    print("ChatGPT response:", chatgpt_response)


    #chatgpt_response = file_data

    # Create a new branch
    branch_name = f"chatgpt-{model}-response-{issue_number}-{random_string}"
    base_branch = repo.get_branch("main")
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_branch.commit.sha)

#Get the file's content and SHA
    file_path = file_name
    file_contents = repo.get_contents(file_path, ref="main")
    file_data = file_contents.decoded_content.decode("utf-8")
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
    pr_title = f"ChatGPT `{model}` response for issue #{issue_number}"
    pr_body = f"Adding a file containing the ChatGPT `{model}` response for issue #{issue_number}:\n\n{chatgpt_response}"
    base = "main"
    head = branch_name
    pr = repo.create_pull(title=pr_title, body=pr_body, head=head, base=base)
    print(f"Successfully created pull request {pr.number}: {pr.title}")

# # Get the file's content and SHA
#     file_path = "helloworld.py"
#     file_contents = repo.get_contents(file_path, ref="main")
#     file_data = file_contents.decoded_content.decode("utf-8")
#     file_sha = file_contents.sha

#     # Update the file with the ChatGPT response
#     new_file_data = f"{chatgpt_response}"
#     repo.update_file(
#         path=file_path,
#         message=f"Update {file_path} with ChatGPT response for issue {issue_number}",
#         #content=new_file_data.encode("utf-8"),
#         content=new_file_data,
#         sha=file_sha,
#         branch="main",
#     )
#     print(f"Successfully updated {file_path} with the ChatGPT response")

else:
    print("Error fetching issue data:", response.status_code)

#     # Create a new branch
#     branch_name = f"chatgpt-response-{issue_number}-{random_string}"
#     base_branch = repo.get_branch("main")
#     repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_branch.commit.sha)

#     # Create a new file with the ChatGPT response
#     #file_name = f"chatgpt-response-{issue_number}-{random_string}.py"
#     file_name = "helloworld.py"
#     repo.create_file(
#         path=file_name,
#         message=f"Add ChatGPT response for issue #{issue_number}",
#         content=chatgpt_response,
#         branch=branch_name,
#     )


# else:
#     print("Error fetching file data:", response_file.status_code)

