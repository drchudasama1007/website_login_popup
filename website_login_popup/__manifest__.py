# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2018 Odoo Helper
# See LICENSE file for full copyright and licensing details.
#
##############################################################################
{
    'name': 'Website Login Popup',
    'category': 'Website',
    'summary': 'Website Login/Signup Popup',

    'version': '0.1',
    'description': """
Website Login/Signup Popup
==================
        This module allows user can Login/Signup By Popup From Any Page of Website. This module has Login/Signup Functnality By Ajax with all validation.
        """,

    'author': 'Odoo Helper',
    'license': 'AGPL-3',

    'depends': [
        'base','website','auth_signup'
        ],
    'data': [
        'views/assets.xml',
        'views/template.xml',
    ],
    'images': ['images/OdooHelper.jpg'],
    'price': 18.24,
    'currency': 'USD',

    'installable': True,
    'application': False
}
