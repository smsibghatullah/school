from odoo import models, fields, api


class StudentCustomize(models.Model):
    _inherit = 'student.student'

    joining_date = fields.Date(string='Joining Date')
    category_id = fields.Many2one('school.customize.category', string='Category')
    section_id = fields.Many2one('school.customize.section', string='Section')
    board_id = fields.Many2one('school.customize.board', string='Board')
    attachment_id = fields.Many2many('school.customize.attachment', string='Attachments')
    emergency_address = fields.Char(string='Emergency Address')