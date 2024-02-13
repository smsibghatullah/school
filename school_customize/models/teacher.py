from odoo import models, fields, api




class teacherCustomize(models.Model):

    _inherit = 'school.teacher'

    nic = fields.Char(string='NIC')