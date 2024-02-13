from odoo import models, fields, api



class SchoolSchool(models.Model):
    ''' Defining School Information'''

    _inherit = 'school.school'
    _description = 'School Information'
    _rec_name = "name"


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

    @api.model
    def create(self, vals):
        res = super(ParentCustomize, self).create(vals)
        channel_id = self.env['mail.channel'].create({'name': vals['name']+'_Parent',
                                         'channel_type':'chat',
                                         'public': 'private'})
        channel_id.channel_last_seen_partner_ids = [(0, 0, {'partner_id': res.commercial_partner_id.id})]
        return res