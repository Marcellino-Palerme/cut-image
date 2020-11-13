#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages

setup(
    name='cuti',
    version='1.3',
    author='Marcellino Palerme',
    author_email='marcellino.palerme@inra.fr',
    description='cut several images.',
    license='CeCILL 2.1',
    url='https://sourcesup.renater.fr/projects/cut-image',
    scripts=["cuti/run.py"],
    classifiers=['Programming Language::Python'],
    packages=find_packages(exclude=["*.test", "*.test.*", "test.*", "test",
                                    "run.py"]),
    include_package_data=True,
    install_requires=['scikit_image'],
    entry_points={
        'console_scripts': [
            'cuti = run:run'
        ]}
)
