from odoo import models, fields, api




class ParentCustomize(models.Model):

    _inherit = 'school.parent'

    nic = fields.Char(string='NIC')
    qualification = fields.Char(string='Qualification')
    marital_status = fields.Char(string='Marital Status')
    occupation = fields.Char(string='Occupation')
    income = fields.Integer(string='Income')
    office_phone = fields.Char(string='Office Phone')
    office_address = fields.Char(string='Office Address')
    alive = fields.Boolean(string='alive')

