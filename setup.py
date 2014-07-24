#!/usr/bin/env python

import os
from setuptools import setup, find_packages

import mkadmin

setup(
    name='django-mkadmin',
    version=mkadmin.__version__,
    description=(
        'Modifies the stock Django-Administration interface'
        ' to fit my ideas a little bit better.'),
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    author='Matthias Kestenholz',
    author_email='mk@feinheit.ch',
    url='http://github.com/matthiask/django-mkadmin/',
    license='BSD License',
    platforms=['OS Independent'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.7',
        'feedparser',
    ],
)
