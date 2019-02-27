# Copyright 2017-2019 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
import re
import subprocess
import uuid

logger = logging.getLogger(__name__)
XIVO_UUID_FILENAME = '/etc/profile.d/xivo_uuid.sh'
XIVO_UUID_RE = re.compile(r'(export )?XIVO_UUID=([0-9a-f-]{36})$')


def get_wazo_uuid():
    for uuid_unchecked in _find_uuid():
        if not uuid_unchecked:
            continue

        try:
            uuid_checked = str(uuid.UUID(uuid_unchecked))
        except ValueError:
            logger.debug('ignoring invalid Wazo UUID "%s"', uuid_unchecked)
            continue

        return uuid_checked

    raise Exception('XIVO_UUID not found')


def _find_uuid():
    yield _find_uuid_environ()
    yield _find_uuid_systemctl()
    yield _find_uuid_file()


def _find_uuid_environ():
    return os.environ.get('XIVO_UUID')


def _find_uuid_systemctl():
    try:
        output = subprocess.check_output(['systemctl', 'show-environment'])
    except (subprocess.CalledProcessError, OSError):
        return None

    return _extract_uuid_env_variable(output.decode('utf-8'))


def _find_uuid_file():
    try:
        with open(XIVO_UUID_FILENAME, 'r') as f:
            environment_string = f.read()
    except IOError:
        return None

    return _extract_uuid_env_variable(environment_string)


def _extract_uuid_env_variable(environment_string):
    for line in environment_string.split('\n'):
        match = XIVO_UUID_RE.match(line)
        if match:
            return match.group(2)
    return None
