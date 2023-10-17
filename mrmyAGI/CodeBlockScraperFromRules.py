from typing import List, Optional
import os
import requests
from bs4 import BeautifulSoup


class CodeBlockScraper:
    def __init__(self, source: str, block_trigger: str, folder_path: Optional[str] = None):
        self.source = source
        self.block_trigger = block_trigger
        self.folder_path = folder_path
        self.log_file_path = ""

        # Create folder for saving code blocks if it doesn't exist
        if self.folder_path is not None and not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        # Set log file name based on input source
        if self.source.startswith("http"):
            self.log_file_path = os.path.join(self.folder_path, "log_web.txt")
        elif self.source.startswith("file"):
            self.log_file_path = os.path.join(self.folder_path, "log_file.txt")

        # Call scrape_code_blocks method
        self.scrape_code_blocks()

    def fetch_html_content(self) -> Optional[str]:
        """
        Fetches HTML content from a web page.
        """
        if self.source.startswith("http"):
            try:
                response = requests.get(self.source)
                return response.text
            except requests.exceptions.RequestException as e:
                self.save_log_to_file(f"Error fetching web content: {str(e)}")
                return None
        else:
            self.save_log_to_file("Error fetching web content: Invalid URL")
            return None

    def fetch_file_content(self) -> Optional[str]:
        """
        Fetches content from a local file.
        """
        if self.source.startswith("file"):
            file_path = self.source.replace("file://", "")
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    return file.read()
            else:
                self.save_log_to_file("Error fetching file content: File does not exist")
                return None
        else:
            self.save_log_to_file("Error fetching file content: Invalid file path")
            return None

    def read_file_as_single_block(self, file_path: str) -> Optional[str]:
        """
        Reads the content of a file as a single block.
        """
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                return file.read()
        else:
            self.save_log_to_file("Error reading file as single block: File does not exist")
            return None

    def extract_code_blocks_from_file(self) -> List[str]:
        """
        Extracts code blocks from a local file.
        """
        if self.block_trigger == "":
            self.save_log_to_file("Error extracting code blocks from file: Block trigger not provided")
            return []

        content = self.fetch_file_content()
        if content is not None:
            blocks = content.split(self.block_trigger)
            return [block.strip() for block in blocks if block.strip()]
        else:
            return []

    def extract_code_blocks_from_html(self) -> List[str]:
        """
        Extracts code blocks from HTML content.
        """
        if self.block_trigger == "":
            self.save_log_to_file("Error extracting code blocks from HTML: Block trigger not provided")
            return []

        content = self.fetch_html_content()
        if content is not None:
            soup = BeautifulSoup(content, "html.parser")
            code_blocks = soup.find_all("code")
            return [block.get_text().strip() for block in code_blocks]
        else:
            return []

    def extract_code_blocks(self) -> List[str]:
        """
        Extracts code blocks from the source.
        """
        if self.source.startswith("http"):
            code_blocks = self.extract_code_blocks_from_html()
        elif self.source.startswith("file"):
            code_blocks = self.extract_code_blocks_from_file()
        else:
            self.save_log_to_file("Error extracting code blocks: Invalid source")
            return []

        if not code_blocks:
            self.save_log_to_file("No code blocks found")

        return code_blocks

    def save_code_blocks_to_folder(self, code_blocks: List[str]):
        """
        Saves code blocks to a folder.
        """
        if self.folder_path is not None:
            for i, block in enumerate(code_blocks):
                file_path = os.path.join(self.folder_path, f"code_block_{i}.txt")
                with open(file_path, "w") as file:
                    file.write(block)

    def save_log_to_file(self, message: str):
        """
        Saves log messages to a file.
        """
        with open(self.log_file_path, "a") as file:
            file.write(f"{message}\n")

    def scrape_code_blocks(self):
        """
        Handles the entire process of scraping code blocks.
        """
        code_blocks = self.extract_code_blocks()
        self.save_code_blocks_to_folder(code_blocks)


if __name__ == "__main__":
    source = "http://example.com"  # Replace with your source URL or file path
    block_trigger = "#CODE_BLOCK#"