from setuptools import find_packages, setup

setup(
    name="sensor",
    version="0.0.1",
    author="ritwik",
    author_email="ritwik94348gupta@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
)

def get_requirements():
    