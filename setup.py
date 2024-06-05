from setuptools import setup, find_packages
import os

def parse_requirements(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

requirements = parse_requirements("requirements.txt")

setup(
    name="foundation_pose",  # Use lowercase name
    version="0.1",
    author="Bowen Wen",
    description="Foundation Pose: A unified foundation model for 6D object pose estimation and tracking",
    long_description=open("readme.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/NVlabs/FoundationPose",
    packages=find_packages(include=['foundation_pose', 'foundation_pose.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    dependency_links=["--extra-index-url https://download.pytorch.org/whl/cu118"],
    install_requires=requirements,
    include_package_data=True,
)
