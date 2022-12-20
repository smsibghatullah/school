from odoo import models, fields, api

class SchoolStandard(models.Model):
    '''Defining a standard related to school.'''

    _inherit = 'school.standard'

    @api.model
    def create(self, vals):
        res = super(SchoolStandard, self).create(vals)
        self.env['mail.channel'].create({'name':vals['name']})
        return res