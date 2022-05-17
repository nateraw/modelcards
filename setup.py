from setuptools import find_packages, setup


def get_version() -> str:
    rel_path = "modelcards/__init__.py"
    with open(rel_path, "r") as fp:
        for line in fp.read().splitlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="modelcards",
    version=get_version(),
    author="Nathan Raw",
    author_email="naterawdata@gmail.com",
    description=(
        "📝 Utility to create, edit, and publish model cards on the Hugging Face Hub."
    ),
    license="MIT",
    install_requires=requirements,
    packages=find_packages(),
    include_package_data=True,
)
