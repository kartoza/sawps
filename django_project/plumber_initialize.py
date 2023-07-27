"""
This script initializes
"""

#########################################################
# Setting up the  context
#########################################################

#########################################################
# Imports
#########################################################
from django.db import connection
from django.db.utils import OperationalError
import time
import os
import shutil
import django

django.setup()

#########################################################
# 1. Waiting for PostgreSQL
#########################################################

print('-----------------------------------------------------')
print('1. Waiting for PostgreSQL')
for _ in range(60):
    try:
        connection.ensure_connection()
        break
    except OperationalError:
        time.sleep(1)
else:
    connection.ensure_connection()
connection.close()

print('-----------------------------------------------------')
print('2. Generate plumber.R file')
# TODO: generate plumber.R from db
src_plumber = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'frontend',
    'utils',
    'plumber_template.R'
)
dest_plumber = os.path.join(
    '/',
    'home',
    'web',
    'plumber_data',
    'plumber.R'
)
shutil.copyfile(src_plumber, dest_plumber)

print('-----------------------------------------------------')
print('3. Spawn initial plumber process')
from frontend.tasks.run_statistical_model import (  # noqa
    spawn_initial_r_plumber
)
plumber_process = spawn_initial_r_plumber()
if plumber_process:
    print(f'plumber process pid {plumber_process.pid}')
else:
    raise RuntimeError('Cannot execute plumber process!')
