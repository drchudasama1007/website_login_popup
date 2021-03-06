# -*- coding: utf-8 -*-
"""
    This file is used for create and inherit the core controllers
"""
import datetime
import json
from datetime import timedelta, date
from odoo.http import request
from odoo.tools.safe_eval import safe_eval
from werkzeug.exceptions import NotFound

from odoo import http
import odoo
import logging
from odoo.tools.translate import _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.sale.controllers.variant import VariantController
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSale
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
from psycopg2 import Error


_logger = logging.getLogger(__name__)

class AuthLoginSignup(http.Controller):

    @http.route('/web/login_custom', type='json', auth="none", methods=['GET', 'POST'],)
    def web_login_custom(self, login, password, redirect=None, **kw):
        values = {}
        values['login_success'] = False
        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(request.session.db, login, password)
                if uid:
                    current_user = request.env['res.users'].sudo().search([('id', '=', uid)])
                    if current_user.has_group('base.group_user'):
                        values['user_type'] = 'internal'
                    else:
                        values['user_type'] = 'portal'
                    values['login_success'] = True

            except odoo.exceptions.AccessDenied as e:
                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True
        return values

    @http.route('/web/signup_custom', type='json', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = kw
        result = {}

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                values = {key: qcontext.get(key) for key in
                          ('login', 'name', 'password')}
                if not values:
                    result.update({'is_success': False, 'error': 'The form was not properly filled in.'})
                    return result
                if values.get('password') != qcontext.get('confirm_password'):
                    result.update({'is_success': False, 'error': 'Passwords do not match; please retype them.'})
                    return result

                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    result.update(
                        {'is_success': False, 'error': 'Another user is already registered using this email address..'})
                    return result

                supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
                lang = request.context.get('lang', '').split('_')[0]
                if lang in supported_lang_codes:
                    values['lang'] = lang

                db, login, password = request.env['res.users'].sudo().signup(values, token=None)
                request.env.cr.commit()  # as authenticate will use its own cursor we need to commit the current transaction
                uid = request.session.authenticate(db, login, password)
                if not uid:
                    result.update({'is_success': False, 'error': 'Authentication Failed.'
                                   })
                    return result
                request.env.cr.commit()
                result.update({'is_success': True})
                return result

            except Error as e:
                result.update({'is_success': False, 'error': 'Could not create a new account.'})
                return result