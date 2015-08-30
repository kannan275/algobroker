# Copyright (C) 2015 Bitquant Research Laboratories (Asia) Limited
# Released under the Simplified BSD License

from setuptools import (
    setup,
    find_packages,
    )

setup(
    name="algobroker",
    version = "0.0.1",
    author="Joseph C Wang",
    author_email='joequant@gmail.com',
    url="https://github.com/joequant/algobroker",
    description="Algorithmic trading broker",
    long_description="""Algobroker is an interface to trading and events""",
    license="BSD",
    packages=find_packages(),
    package_data = {'algobroker': ['algobroker/keys/*.example']},
    setup_requires = ['pyzmq',
                'msgpack-python',
                'plivo'],
    use_2to3 = True
)
                                