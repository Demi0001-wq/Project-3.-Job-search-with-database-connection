import os
from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """
    Reads the configuration file and returns a dictionary of parameters.
    """
    # Create a parser
    parser = ConfigParser()
    # Read config file
    if os.path.exists(filename):
        parser.read(filename)
    else:
        # Check if the file is in the parent directory
        parent_dir_file = os.path.join(os.path.dirname(__file__), "..", filename)
        if os.path.exists(parent_dir_file):
            parser.read(parent_dir_file)
        else:
            raise FileNotFoundError(f"Config file {filename} not found.")

    # Get section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} is not found in the {filename} file.")

    return db
