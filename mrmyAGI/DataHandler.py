# Do Not Change Above Line#
import sqlite3
import os
import zipfile
from typing import Optional, List

from logger import Logger


class DataHandler:
    """
    A class that provides various data handling operations.
    """

    version: Optional[float] = 0.1
    name = "DataHandler"
    log = Logger()
    script_path: Optional[str] = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        pass

    def load_file(self, file_path: str) -> bytes:
        """
        Load the contents of a file.

        Args:
            file_path: The path to the file.

        Returns:
            The contents of the file as bytes.
        """
        with open(file_path, "rb") as file:
            return file.read()

    def save_file(self, data: bytes, file_path: str) -> None:
        """
        Save data to a file.

        Args:
            data: The data to be saved.
            file_path: The path to save the file.
        """
        with open(file_path, "wb") as file:
            file.write(data)

    def get_files_recursive(self, folder_path: str) -> List[str]:
        """
        Get a list of files in a folder and its subfolders recursively.

        Args:
            folder_path: The path to the folder.

        Returns:
            A list of file paths.
        """
        file_list = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_list.append(file_path)
        return file_list

    def zip_files(self, file_list: List[str], zip_path: str) -> None:
        """
        Zip a list of files.

        Args:
            file_list: The list of file paths to be zipped.
            zip_path: The path to save the zip file.
        """
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            for file in file_list:
                zip_file.write(file, os.path.basename(file))

    def unzip_files(self, zip_path: str, extract_path: str) -> None:
        """
        Unzip a zip file.

        Args:
            zip_path: The path to the zip file.
            extract_path: The path to extract the files.
        """
        with zipfile.ZipFile(zip_path, "r") as zip_file:
            zip_file.extractall(extract_path)

    def initialize_sqlite_db(self, db_name: str) -> None:
        """
        Initialize a SQLite database.

        Args:
            db_name: The name of the database.
        """
        db_path = os.path.join(self.script_path, f"{db_name}.db")
        connection = sqlite3.connect(db_path)
        connection.close()

    def tokenize_file(self, file_path: str) -> List[str]:
        """
        Tokenize the contents of a file.

        Args:
            file_path: The path to the file.

        Returns:
            A list of tokens.
        """
        with open(file_path, "r") as file:
            content = file.read()
        tokens = content.split()
        return tokens

    def store_data_in_vectorstore(self, data: List[str]) -> None:
        """
        Store data in a vectorstore.

        Args:
            data: The data to be stored.
        """
        # TODO: Implement storing data in a vectorstore
        pass


if __name__ == "__main__":
    data_handler = DataHandler()
