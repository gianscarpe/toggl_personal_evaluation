import re

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    version = re.search(
        r'^__version__\s*=\s*"(.*)"',
        open("deep_toggl/__init__.py").read(),
        re.MULTILINE,
    ).group(1)
setuptools.setup(
    name="deep_toggl",
    version=version,
    author="gianscarpe",
    author_email="me@scarpellini.dev",
    long_description_content_type="text/markdown",
    description="Simple tool for toggl summary",
    long_description=long_description,
    url="https://github.com/gianscarpe/sampleproject",
    entry_points={"console_scripts": ["deep_toggl = deep_toggl:main"]},
    install_requires=["pendulum", "togglCli", "calmap"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
