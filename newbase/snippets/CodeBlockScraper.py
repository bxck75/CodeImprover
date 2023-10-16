import requests
import os
from bs4 import BeautifulSoup
from Code_Refactorer import Code_Refactorer
from credits import HUGGINGFACE_TOKEN


class CodeBlockScraper:
    def __init__(self, input_source, scraper_on=True):
        self.url = None
        self.input_source = input_source
        self.scraper_on = scraper_on
        self.input_filepath = None
        self.code_blocks = {}
        self.block_trigger = "###################"
        self.folder_name = "PythonHuggingFaceScripts"
        self.log = ""
        self.log_file = "scrape_urlss.txt"

        if "http" not in input_source:
            self.scraper_on = False
            self.input_filepath = input_source
            self.fetch_file_content()
        else:
            self.scraper_on = True
            self.url = input_source

    def fetch_web_content(self):
        if self.scraper_on:
            # Send a GET request to fetch the web content
            response = requests.get(self.url)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                self.soup = BeautifulSoup(response.text, "html.parser")
            else:
                self.log += "Failed to retrieve web content. Please check the URL."
                exit()

    def fetch_file_content(self):
        # Check if the request was successful
        if os.path.exists(self.input_filepath):
            self.blocks_from_file()
        else:
            self.log += "Failed to retrieve web content. Please check the File."
            exit()

    def read_file_as_single_script(self, file_path):
        # Read the entire file as a single script without block triggers
        with open(file_path, "r") as f:
            content = f.read()  # Read the entire file as a single string
            f.close()

        self.single = False  # Set self.single to False to indicate multiple scripts
        self.code_blocks = {"Single Script": content}  # Use a single name for the script

    def blocks_from_file(self, file_path):
        # Read code blocks from a file
        with open(file_path, "r") as f:
            content = f.readlines()
            f.close()

        blocks = []
        current_block = ""
        name = None
        skip_next_trigger = False

        for line in content:
            if skip_next_trigger:
                skip_next_trigger = False
                continue

            if line.strip() == self.block_trigger:
                if name is not None:
                    self.code_blocks[name] = current_block  # same output format as extract_code_blocks
                    name = None
                    current_block = ""
                else:
                    skip_next_trigger = True
            else:
                if name is None:
                    name = line.strip()
                current_block += line

    def extract_code_blocks(self):
        if self.scraper_on:
            # Find all h3 tags with class "relative group" and their associated pre tags
            h3_tags = self.soup.find_all("h3", {"class": "relative group"})
            for h3_tag in h3_tags:
                # Extract the name from the last span within the h3 tag
                name = h3_tag.find_all("span")[-1].text.strip()
                # Find the next pre tag within a div