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

load_dotenv()

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

random_string = int(time.time()) 

# Set your personal access tokens and repository details
openai_access_token = os.getenv("OPENAI_ACCESS_TOKEN")
github_access_token = os.getenv("GITHUB_ACCESS_TOKEN")
repo_owner = os.getenv("REPO_OWNER")
repo_name = os.getenv("REPO_NAME")

issue_number = 38  # Set the issue number you want to read

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
    file_extension, prompt_body = get_filetype_prompt(issue_body)

    # Initialize the OpenAI client
    openai.api_key = openai_access_token

    # Set the options for the OpenAI client
    prompt = f"{prompt_body}"
    model = "gpt-3.5-turbo"
    tokens = 100  # The number of tokens to generate
    temperature = 0.8  # The higher the value, the more random the output

    # Send the issue body as a request to ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{prompt}"}
        ]
    )

    # Write the ChatGPT response to the console
    chatgpt_response = response.choices[0].message.content
    print("ChatGPT response:", chatgpt_response)

    # Create a new branch
    branch_name = f"chatgpt-response-{issue_number}-{random_string}"
    base_branch = repo.get_branch("main")
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=base_branch.commit.sha)

    # Create a new file with the ChatGPT response
    file_name = f"chatgpt-response-{issue_number}-{random_string}{file_extension}"
    repo.create_file(
        path=file_name,
        message=f"Add ChatGPT `{model}` response for issue #{issue_number}",
        content=chatgpt_response.encode("utf-8"),
        branch=branch_name,
    )

    # Create a pull request
    pr_title = f"ChatGPT response for issue #{issue_number}"
    pr_body = f"Adding a file containing the ChatGPT `{model}` response for issue #{issue_number}:\n\n{chatgpt_response}"
    base = "main"
    head = branch_name
    pr = repo.create_pull(title=pr_title, body=pr_body, head=head, base=base)
    print(f"Successfully created pull request {pr.number}: {pr.title}")

else:
    print("Error fetching issue data:", response.status_code)