#!/usr/bin/env python3

import os
import odoo
from odoo.tools.parse_version import parse_version
from odoo import api, SUPERUSER_ID
from odoo.modules.registry import Registry


def main():
    update_list=[]

    odoo_path = odoo.addons.__path__
    odoo.addons.__path__ = [odoo.tools.config['addons_path']]
    module_version=odoo.modules.module.get_modules_with_version()

    odoo.tools.config['db_user']=os.environ.get('USER', 'odoo')
    odoo.tools.config['db_password']=os.environ.get('PASSWORD', 'odoo')
    odoo.tools.config['db_port']=os.environ.get('PORT', 5432)
    odoo.tools.config['db_host']=os.environ.get('HOST', 'db')

    db_name = os.environ.get('DB_NAME')
    if not db_name:
        odoo.addons.__path__ = odoo_path
        return

    registry = odoo.registry(db_name)
    db = registry._db

    with odoo.api.Environment.manage(), db.cursor() as cr:

        env = api.Environment(cr, SUPERUSER_ID, {})
        Module = env['ir.module.module']

        known_mods = Module.with_context(lang=None).search([])
        known_mods_names = {mod.name: mod for mod in known_mods}

        for module_name in module_version:
            mod = known_mods_names.get(module_name)
            if mod and parse_version(module_version[module_name]) > parse_version(mod.latest_version):
                update_list.append(module_name)

    odoo.addons.__path__ = odoo_path

    if update_list:
        odoo.tools.config['update'] = ','.join(update_list)
        odoo.tools.config['db_name'] = db_name
        rc = odoo.service.server.start(preload=[odoo.tools.config['db_name']], stop=True)
        sys.exit(rc)

if __name__ == '__main__':
    main()
