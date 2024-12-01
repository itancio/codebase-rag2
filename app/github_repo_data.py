import os
import re
import json
import requests
from git import Repo, GitCommandError
from langchain.schema import Document


class GithubRepoData:
    def __init__(self, url: str):
        """
        Initializes the GithubRepoData object with repository details.

        Args:
            url (str): The GitHub repository URL.
        """
        # Match the URL to extract the owner and repo name
        pattern = r"(?:https?://|git@)github\.com[:/](.+?)/(.+?)(?:/|\.git|$)"
        match = re.match(pattern, url)
        if not match:
            raise ValueError(f"Invalid GitHub URL: {url}")
        owner, repo = match.groups()

        # Fetch repository details from GitHub API
        api_url = f'https://api.github.com/repos/{owner}/{repo}'
        response = requests.get(api_url)
        if response.status_code == 200:
            github = response.json()
            visibility = github.get('visibility', 'unknown')

            if visibility == 'public':
                self.id = github.get('id')
                self.owner = github.get('owner').get('login')
                self.fullname = github.get('full_name')
                self.repo_name = github.get('name')
                self.main_branch = github.get('default_branch')
                self.description = github.get('description')
                self.events_url = github.get('events_url')
                self.dir_path = os.path.join(os.getcwd(), self.repo_name)
            else:
                raise ValueError(f'Repository {self.owner}/{self.repo_name} is not public.')
        elif response.status_code == 404:
            raise ValueError(f"Repository {owner}/{repo} not found.")
        elif response.status_code == 403:
            raise ValueError("GitHub API rate limit exceeded. Please try again later.")
        else:
            raise ValueError(f"Failed to fetch repository details. HTTP Status: {response.status_code}")

    def to_dict(self):
        return {
            "id": self.id,
            "owner": self.owner,
            "fullname": self.fullname,
            "repo_name": self.repo_name,
            "description": self.description,
            "events_url": self.events_url,
            "dir_path": self.dir_path,
            "url": f"https://github.com/{self.owner}/{self.repo_name}"
        }

    def exists(self) -> bool:
        """Checks if the repository is already cloned."""
        return os.path.exists(self.dir_path)

    def clone(self) -> bool:
        """Clones the repository into the specified local directory."""
        if self.exists():
            print(f"Repository {self.repo_name} already cloned at {self.dir_path}.")
            return True

        try:
            os.makedirs(self.dir_path, exist_ok=True)
            clone_url = f"https://github.com/{self.fullname}.git"
            print(f"Cloning {self.repo_name} into {self.dir_path}")
            Repo.clone_from(clone_url, self.dir_path)
            print(f"Repository {self.repo_name} cloned successfully.")
            return True
        except GitCommandError as e:
            raise ValueError(f"Failed to clone {self.repo_name}: {e}")
