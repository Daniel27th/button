from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='button',
    version='0.0.3.post3',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    python_requires='>=3.*',

    author='Minhwan Kim',
    author_email='minhwan.kim@member.fsf.org',
    description='Tiny automation tool written in Python',
    keywords='automation build tool',
    url='https://github.com/azurelysium/button',
    project_urls={
        'Documentation': 'https://github.com/azurelysium/button',
        'Source Code': 'https://github.com/azurelysium/button',
    },
    classifiers=[
        'License :: OSI Approved :: MIT License'
    ],

    install_requires=[
        "colorama==0.4.4",
        "tabulate==0.8.9",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',

    entry_points={
        'console_scripts': [
            'btn = button.cli:main',
        ],
    },
)
