from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="modelcards",
    version='0.0.3',
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    description="📝 Utility to create, edit, and publish model cards on the Hugging Face Hub.",
    license="MIT",
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
)
