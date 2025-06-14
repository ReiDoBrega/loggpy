from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="loggpy",
    version="0.1.0",
    author="ReiDoBrega",
    author_email="pedro94782079@gmail.com",
    description="A powerful Python logging library with custom levels and colored output support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ReiDoBrega/loggpy",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "coloredlogs>=15.0.0",
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
    ],
    keywords=[
        "logging", "logger", "colored-logs", "custom-logging", "terminal", 
        "debug", "development-tools", "logging-library"
    ],
    project_urls={
        "Homepage": "https://github.com/ReiDoBrega/loggpy",
        "Repository": "https://github.com/ReiDoBrega/loggpy",
        "Bug Tracker": "https://github.com/ReiDoBrega/loggpy/issues",
    },
)