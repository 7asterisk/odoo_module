# -*- coding: utf-8 -*-
from odoo import http

# class Mysales(http.Controller):
#     @http.route('/mysales/mysales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mysales/mysales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mysales.listing', {
#             'root': '/mysales/mysales',
#             'objects': http.request.env['mysales.mysales'].search([]),
#         })

#     @http.route('/mysales/mysales/objects/<model("mysales.mysales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mysales.object', {
#             'object': obj
#         })