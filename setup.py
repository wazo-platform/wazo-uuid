#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from setuptools import setup
from setuptools import find_packages

setup(
    name='wazo_uuid',
    version='1.0',
    description='Python code related to Wazo UUID',
    author='Wazo Authors',
    author_email='dev@wazo.community',
    url='http://wazo.community',
    license='GPLv3',
    packages=find_packages(),
    scripts=[
        'bin/xivo-configure-uuid'
    ],
)
