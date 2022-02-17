# This file is needed for editable installs (`pip install -e .`).
# Can be removed once the following is resolved
# https://github.com/pypa/packaging-problems/issues/256
from setuptools import setup
from pathlib import Path

lines = Path("sphinx_multilingual").joinpath("__init__.py")
for line in lines.read_text(encoding='utf-8').split("\n"):
    if line.startswith("__version__ ="):
        version = line.split(" = ")[-1].strip('"')
        break

setup(
    name="sphinx-multilingual",
    version=version,
    python_requires=">=3.6",
    author="BE",
    author_email="bernard.etiennot@macq.eu",
    url="https://docs.macq.eu",
    project_urls={
        "Documentation": "https://docs.macq.eu",
    },
    # this should be a whitespace separated string of keywords, not a list
    keywords="multilingual documentation",
    description="An extension to manage multilingual documentation generation with Sphinx",
    long_description=Path("./README.md").read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=['sphinx_multilingual'],
    install_requires=[
        "sphinx>=3,<5",
    ],
    extras_require={
        "sphinx": [
            "sphinx~=4.4",  # Force Sphinx to be the latest version
        ],
    },
)