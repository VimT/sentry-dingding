#!/usr/bin/env python
"""
sentry-dingding
==============

An extension for Sentry which integrates with DingDing. It will forwards
notifications to an dingding room.
"""
from setuptools import setup, find_packages

install_requires = [
    'sentry>=6.0.0',
]

setup(
    name='sentry-dingding',
    version='8.22',
    author='VimT',
    author_email='vimt@foxmail.com',
    url='https://github.com/VimT/sentry-dingding',
    description='A Sentry extension which integrates with DingDing.',
    long_description=__doc__,
    packages=find_packages(exclude=['tests']),
    zip_safe=False,
    install_requires=install_requires,
    include_package_data=True,
    entry_points={
        'sentry.apps': [
            'sentry_dingding = sentry_dingding ',
        ],
        'sentry.plugins': [
            'dingding = sentry_dingding.models:DingDingMessage',
         ],
    },
    classifiers=[
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development'
    ],
)
