import setuptools

setuptools.setup(
    name="deep_toggl",
    version="0.1",
    author="gianscarpe",
    author_email="me@scarpellini.dev",
    description="Package for managing deep work",
    url="https://github.com/gianscarpe/sampleproject",
    entry_points = {
        'console_scripts': ['deep_toggl = deep_toggl:main']
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
