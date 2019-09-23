#!/usr/bin/env python3
"""Team Manager

flask-smorest example
"""

from setuptools import setup, find_packages

# Get the long description from the README file
with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='team-manager',
    version='0.0',
    description='Team Manager',
    long_description=long_description,
    # url='',
    # author='',
    # author_email='@nobatek.com',
    # license='',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        # 'License :: ,
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords=[
    ],
    packages=find_packages(),
    install_requires=[
        'flask>=1.0.0',
        'python-dotenv>=0.9.0',
        'flask-smorest>=0.18.0,<0.19',
        'marshmallow>=3.0.0',
        'sqlalchemy>=1.2.5',
        'sqlalchemy-utils>=0.32.21',
        'flask-sqlalchemy>=2.3.2',
        'marshmallow_sqlalchemy>=0.18,<0.19',
    ],
)
