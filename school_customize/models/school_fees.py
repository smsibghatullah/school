
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentFeesRegister(models.Model):
    _inherit = "student.fees.register"

    @api.onchange("fees_structure")
    def on_change_fees_structure(self):
        self.standard_id = self.fees_structure.class_id.id;

    # def _get_default_journal(self):
    #     return self.env['account.journal'].search(
    #         [('id', '=', self.env.context.get('active_id'))]).id

    due_date = fields.Date("Due Date", required=True, help="Due Date",
                       default=fields.Date.context_today)
    validity_date = fields.Date("Validity Date", required=True, help="Validity Date",
                       default=fields.Date.context_today)
    journal_id = fields.Many2one(
        "account.journal", "Journal",
        help="Select Journal", required=False,
        default=lambda self: self._get_default_journal()
    )

    def _get_default_journal(self):
        journal =  self.env['account.journal'].search([('name' , '=' , "Student Custom Invoice")])[0].id
        return journal


    def fees_register_confirm(self):
        """Method to confirm payslip"""
        stud_obj = self.env["student.student"]
        slip_obj = self.env["student.payslip"]
        school_std_obj = self.env["school.standard"]
        for rec in self:
            if not rec.journal_id:
                raise ValidationError(_("Kindly, Select Account Journal!"))
            if not rec.fees_structure:
                raise ValidationError(_("Kindly, Select Fees Structure!"))
            school_std_rec = school_std_obj.search(
                [("standard_id", "=", rec.standard_id.id)])
            for stu in stud_obj.search(
                    [("standard_id", "in", school_std_rec.ids),
                     ("state", "=", "done")]):
                # Check if payslip exist of student
                if slip_obj.search(
                        [("student_id", "=", stu.id), ("date", "=", rec.date)]):
                    raise ValidationError(_(
                        """There is already a Payslip exist for student: %s for same date.!
                        """) % stu.name)
                else:
                    rec.number = self.env["ir.sequence"].next_by_code(
                        "student.fees.register") or _("New")
                    res = {"student_id": stu.id,
                           "register_id": rec.id,
                           "name": rec.name,
                           "date": rec.date,
                           "due_date": rec.due_date,
                           "validity_date": rec.validity_date,
                           "company_id": rec.company_id.id,
                           "currency_id": rec.company_id.currency_id.id or False,
                           "journal_id": rec.journal_id.id,
                           "fees_structure_id": rec.fees_structure.id or False}
                    slip_rec = slip_obj.create(res)
                    slip_rec.onchange_student()
            # Calculate the amount
            amount = sum([data.total for data in rec.line_ids])
            rec.write({"total_amount": amount, "state": "confirm"})




class StudentFeesStructure(models.Model):
    _inherit = "student.fees.structure"

    class_id = fields.Many2one("standard.standard")


