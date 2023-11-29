from setuptools import setup, find_packages


with open('requirements.txt') as f:
     required = f.read().splitlines()


setup(
    name='entropik_scene_detection_analysis',
    version='1.0.0',
    author='Entropik Tech',
    author_email='entropiktech@entropiktech.com',
    description='Entropik Scene Detection Analysis',
    url='',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires='>=3.9',
    install_requires=required,
    include_package_data=True,
    zip_safe=False
)