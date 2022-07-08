from odoo import models, fields, api

class Category(models.Model):
    _name = 'school.customize.category'
    _rec_name = 'category_name'

    category_name = fields.Char(string='Category')
