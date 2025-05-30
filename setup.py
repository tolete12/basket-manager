#! /usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

long_description = open('README.rst', 'rb').read().decode('utf-8')

install_requires = ["requests<=2.21.0", "beautifulsoup4<=4.7.1", "PyQt5==5.14.0"]

setuptools.setup(
    name="AmericanSportsManager",
    version="0.0.1",
    url="https://github.com/pablorasines/AmericanSportsManager",
    download_url="https://github.com/pablorasines/AmericanSportsManager.git",
    author="pablorasines",
    author_email="pablo.rasines.diez@gmail.com",
    description="American Sports Manager",
    packages=["bin", "db", "gui", "models", "resources", "utilities", "variables"],
    install_requires=install_requires,
    license='MIT License',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
)