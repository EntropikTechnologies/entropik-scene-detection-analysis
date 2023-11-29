from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="entropik_scene_detection_analysis",
    version="1.0.2",
    author="Entropik Tech",
    author_email="entropiktech@entropiktech.com",
    description="Entropik Scene Detection Analysis",
    long_description=long_description,
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=required,
    dependency_links=["https://download.pytorch.org/whl/cu117"],
    include_package_data=True,
    zip_safe=True,
)
