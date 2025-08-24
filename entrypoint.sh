#!/bin/sh
set -e

# run updater
python3 moduler_updater.py

# run odoo
exec odoo-bin "$@"
