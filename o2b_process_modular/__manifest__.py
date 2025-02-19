# -*- coding: utf-8 -*-
##########################################################################
# Author      : O2b Technologies Pvt. Ltd.(<www.o2btechnologies.com>)
# Copyright(c): 2016-Present O2b Technologies Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
##########################################################################
{
    'name'      : "Oflow",
    'summary'   : """
        O2B Process Modular is Module that faciliate user to create module in odoo plateform.
        This is low code Plateform for odoo automation.""",
    'description': """
        Long description of module's purpose
    """,
    'author'    : "O2b Technologies",
    'website'   : "https://www.o2btechnologies.com/",
    'category'  : 'Uncategorized',
    'license'   : 'OPL-1',
    'version'   : '0.1',
    'depends'   : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/data.xml'
    ],
    'post_init_hook': 'post_init_hook',
 
     'assets'   : {
        'web.assets_backend': [
            '/o2b_process_modular/static/src/views/form/form_controller.js',
            '/o2b_process_modular/static/src/views/form/list_controller.js',
            '/o2b_process_modular/static/src/views/form/form_controller.xml',
            '/o2b_process_modular/static/src/views/form/list_controller.xml',
        ]
    },
}
