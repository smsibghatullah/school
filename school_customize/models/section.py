from odoo import models, fields, api


class Section(models.Model):
    _name = 'school.customize.section'
    _rec_name = 'category_name'

    category_name = fields.Char(string='Category')
