from odoo import models, fields, api

class Board(models.Model):
    _name = 'school.customize.board'
    _rec_name = 'board_name'
    board_name = fields.Char(string='Board')
