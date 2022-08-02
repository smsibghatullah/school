from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class StudentCustomize(models.Model):
    _inherit = 'student.student'

    joining_date = fields.Date(string='Joining Date')
    category_id = fields.Many2one('school.customize.category', string='Category')
    section_id = fields.Many2one('school.customize.section', string='Section')
    board_id = fields.Many2one('school.customize.board', string='Board')
    attachment_id = fields.Many2many('school.customize.attachment', string='Attachments')
    emergency_address = fields.Char(string='Emergency Address')


class StudentPayslipLine(models.Model):
    """Student PaySlip Line"""

    _inherit = "student.payslip.line"

    date = fields.Date("Date", readonly=True, help="Current Date of payslip",
                       default=fields.Date.context_today, )

class StudentPayslip(models.Model):
    _inherit = "student.payslip"

    def payslip_cancel(self):
        self.state = "cancel"

    def payslip_payment(self):
        rec = self.env['payment.fee.wizard'].create({'student_payslip_id': self.id,
                                               'amount_due': self.due_amount,
                                               'description': self.name})
        view = self.env.ref('school_customize.view_payment_fee_wizard_form')
        return {
            'name': "Payment Fee ",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'payment.fee.wizard',
            'view_id': view.id,
            'target': 'new',
            'res_id': rec.id,
        }

    def payslip_confirm(self):
        """Method to confirm payslip"""
        for rec in self:
            if not rec.journal_id:
                raise ValidationError(_("Kindly, Select Account Journal!"))
            if not rec.fees_structure_id:
                raise ValidationError(_("Kindly, Select Fees Structure!"))

            #old un-piad record
            old_payslips = self.env['student.payslip'].search([('state','in',['draft','confirm']),
                                                               ('student_id','=',rec.student_id.id)])
            old_payslip_partial_paid = self.env['student.payslip'].search([('state','in',['pending']),
                                                               ('student_id','=',rec.student_id.id)])
            lines = []
            for old_payslip in old_payslips:
                for line in old_payslip.line_ids:
                    line_vals = {"slip_id": rec.id,
                                 "product_id": line.product_id.id,
                                 "name": line.name,
                                 "code": line.code,
                                 "date": line.date,
                                 "type": line.type,
                                 "account_id": line.account_id.id,
                                 "amount": line.amount,
                                 "currency_id": line.currency_id.id or False,
                                 "currency_symbol": line.currency_symbol or False}
                    lines.append((0, 0, line_vals))
                old_payslip.state = 'cancel'
            rec.write({"line_ids": lines})

            lines = []
            product_partial_payment = self.env['product.product'].search([('default_code','=','PartialPayment')])
            for old_payslip in old_payslip_partial_paid:
                # for line in old_payslip.line_ids:
                line_vals = {"slip_id": rec.id,
                                 "product_id": product_partial_payment.id,
                                 "name": old_payslip.number,
                                 "code": "PAR",
                                 "date": old_payslip.date,
                                 "type": "month",
                                 "account_id": 39,
                                 "amount": old_payslip.due_amount,
                                 # "currency_id": line.currency_id.id or False,
                                 # "currency_symbol": line.currency_symbol or False
                                 }
                lines.append((0, 0, line_vals))
                old_payslip.state = 'cancel'
            rec.write({"line_ids": lines})


            lines = []
            for data in rec.fees_structure_id.line_ids or []:
                line_vals = {"slip_id": rec.id,
                            "product_id": data.product_id.id,
                            "name": data.name,
                            "code": data.code,
                            "date": rec.date,
                            "type": data.type,
                            "account_id": data.account_id.id,
                            "amount": data.amount,
                            "currency_id": data.currency_id.id or False,
                            "currency_symbol": data.currency_symbol or False}
                lines.append((0, 0, line_vals))
            rec.write({"line_ids": lines})


            # Compute amount
            amount = 0
            amount = sum(data.amount for data in rec.line_ids)
            rec.register_id.write({"total_amount": rec.total})
            rec.write({"total": amount,
                    "state": "confirm",
                    "due_amount": amount,
                    "currency_id": rec.company_id.currency_id.id or False})
            template = self.env['mail.template'].sudo().search([
                ('name', 'ilike', 'Fees Reminder')], limit=1)
            if template:
                for user in rec.student_id.parent_id:
                    subject = _("Fees Reminder")
                    if user.email:
                        body = _("""
                        <div>
                            <p>Dear """ + str(user.display_name) + """,
                            <br/><br/>
                            We are getting in touch as school fees due on """+str(rec.date)+""" remain unpaid for """+str(rec.student_id.display_name)+""".
                            <br/><br/>
                            We kindly ask that you arrange to pay the """+str(rec.due_amount)+""" balance as soon as possible.
                            <br/><br/>
                            Thank You.
                        </div>""")
                        template.send_mail(rec.id, email_values={
                            'email_from': self.env.user.email or '',
                            'email_to': user.email,
                            'subject': subject,
                            'body_html': body,
                            }, force_send=True)
