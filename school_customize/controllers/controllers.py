# -*- coding: utf-8 -*-
# from odoo import http


# class SchoolCustomize(http.Controller):
#     @http.route('/school_customize/school_customize', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_customize/school_customize/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_customize.listing', {
#             'root': '/school_customize/school_customize',
#             'objects': http.request.env['school_customize.school_customize'].search([]),
#         })

#     @http.route('/school_customize/school_customize/objects/<model("school_customize.school_customize"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_customize.object', {
#             'object': obj
#         })
