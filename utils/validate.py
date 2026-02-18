import os

def validate_directory(directory: str) -> tuple:
    """
    Function to validate if the provided directory path is valid
    and exists in the filesystem.

    Returns:
        tuple: (bool, str) - (True if valid, False if invalid and error message)
    """
    if os.path.isdir(directory):
        return True, os.path.abspath(directory)
    else:
        return False, f"Directory {directory} is not valid."
