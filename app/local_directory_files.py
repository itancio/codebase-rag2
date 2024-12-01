import os
from langchain.schema import Document
from app.constants import IGNORED_DIRS
from app.language_support import LanguageSupport

class LocalDirectoryFiles:
    def __init__(self, dir_path: str, repo_fullname: str, main_branch: str):
        """
        Initializes the LocalDirectoryFiles object.

        Args:
            dir_path (str): Path to the local directory.
            repo_fullname (str): Full name of the repository (e.g., owner/repo).
            main_branch (str): Main branch of the repository.
        """
        self.dir_path = dir_path
        self.repo_fullname = repo_fullname
        self.main_branch = main_branch

    def read_file(self, filepath: str) -> str:
        """Reads the contents of a file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Failed to read file {filepath}: {e}")

    def get_files(self) -> list[Document]:
        """
        Recursively retrieves all files in the directory and creates `Document` objects.

        Returns:
            list[Document]: List of Document objects.
        """
        documents = []
        for root, _, files in os.walk(self.dir_path):
            if any(ignored_dir in root for ignored_dir in IGNORED_DIRS):
                continue

            for file in files:
                file_path = os.path.join(root, file)
                extension = os.path.splitext(file_path)[1]
    
                if LanguageSupport.is_supported_language(extension) :
                    content = self.read_file(file_path)
                    relative_path = os.path.relpath(file_path, self.dir_path)
                    if content:
                        document = Document(
                            page_content=content,
                            metadata={
                                "filename": file,
                                "path": file_path,
                                "url": f"https://github.com/{self.repo_fullname}/blob/{self.main_branch}/{relative_path}"
                            }
                        )
                        documents.append(document)
        return documents
