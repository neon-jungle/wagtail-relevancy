#!/usr/bin/env python
"""
Install wagtail-relevancy using setuptools
"""

from wagtailrelevancy import __version__

with open('README.rst', 'r') as f:
    readme = f.read()

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='wagtail-relevancy',
    version=__version__,
    description="A plugin for assisting editors with keeping their content up to date.",
    long_description=readme,
    author='Liam Brenner',
    author_email='liam@takeflight.com.au',
    url='https://github.com/takeflight/wagtail-relevancy',

    install_requires=[
        'wagtail>=1.0',
    ],
    zip_safe=False,
    license='BSD License',

    packages=find_packages(),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
