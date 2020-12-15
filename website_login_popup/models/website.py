# -*- coding: utf-8 -*-

import json

import werkzeug.urls
import werkzeug.utils
from odoo.http import request


import odoo
from odoo import fields, models, http
from odoo.addons.auth_oauth.controllers.main import OAuthLogin
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist


class Website(models.Model):
    _inherit = "website"

    def getDatabase(self):
        """
                To display database in login popup
                :return: List of databases
                """
        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        return values['databases']