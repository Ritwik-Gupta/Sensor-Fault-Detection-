from setuptools import find_packages, setup
from typing import List

REQUIREMENTS_FILE_PATH = "./requirements.txt"
HYPHEN_E_DOT = "-e ."

def get_requirements() -> List[str]:
    with open(REQUIREMENTS_FILE_PATH) as requirements_file:
        lines = requirements_file.readlines()

    lines = [x.replace("\n","") for x in lines]
    
    if(HYPHEN_E_DOT in lines):
        lines.remove(HYPHEN_E_DOT)

    return lines

setup(
    name="sensor",
    version="0.0.1",
    author="ritwik",
    author_email="ritwik94348gupta@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)

