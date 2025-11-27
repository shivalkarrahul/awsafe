from setuptools import setup, find_packages

setup(
    name="awsafe",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "boto3"
    ],
    entry_points={
        "console_scripts": [
            "awsafe=awsafe.cli:cli"
        ]
    }
)
