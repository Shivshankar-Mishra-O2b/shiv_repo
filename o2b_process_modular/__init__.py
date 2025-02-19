from . import controllers
from . import models
from odoo import api, SUPERUSER_ID


# post init hook call
def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    menu_model = env['ir.ui.menu']
    # Search for a record based on some criteria for app menu
    record = menu_model.search([('name', '=', 'Apps'),('active','=',True),('id','=',5)], limit=1)
    if record:
        record.write({
            'active': False,
        })
    # for Discuss app menu hide
    record = menu_model.search([('name', '=', 'Discuss'),('active','=',True),('id','=',74)], limit=1)
    if record:
        record.write({
            'active': False,
        })
    # for security addtion
    database_setup_key = env['ir.config_parameter'].search([('key','=', 'oflow_security_key')],limit=1)
    if not database_setup_key:
        database_setup_key.create({
            'key'   : 'oflow_security_key',
            'value' : 'o2b_technologies',
            })
