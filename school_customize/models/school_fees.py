
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentFeesRegister(models.Model):
    _inherit = "student.fees.register"

    @api.onchange("fees_structure")
    def on_change_fees_structure(self):
        self.standard_id = self.fees_structure.class_id.id;




class StudentFeesStructure(models.Model):
    _inherit = "student.fees.structure"

    class_id = fields.Many2one("standard.standard")


