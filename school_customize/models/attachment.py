from odoo import models, fields, api

class Board(models.Model):
    _name = 'school.customize.attachment'
    _rec_name = 'attachment_name'

    attachment_name = fields.Char(string='Attachment Name')
