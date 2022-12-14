# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class PaymentFeeWizard(models.TransientModel):
    """Defining TransientModel to move standard."""

    _name = 'payment.fee.wizard'
    _description = "Student payment Fee"

    student_payslip_id = fields.Many2one('student.payslip', 'Pay Slip', required=True)
    amount_due = fields.Float()
    amount_paid = fields.Float()
    memo = fields.Char()
    date = fields.Date()
    description = fields.Char()
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 compute='_compute_from_lines')
    journal_id = fields.Many2one('account.journal',
        domain="[('type', 'in', ('bank', 'cash'))]")

    remaning_amount = fields.Float( "Remaning Amount")

    @api.onchange("amount_paid")
    def on_change_student(self):
        self.remaning_amount = self.amount_due - self.amount_paid

    # def _remaning_amount(self):
    #     self.remaning_amount = self.amount_due - self.amount_paid
    def _compute_from_lines(self):
        self.company_id = self.env.company

    def pay_api(self, data=None):
        print(data)
        student_payslip_id = self.env['student.payslip'].search([('id', '=', int(data['student_payslip_id']))])
        res = self.create({'student_payslip_id': student_payslip_id.id, 'date': data['date'], 'memo': data['memo'],
                           'amount_paid': data['amount_paid'], 'amount_due': data['amount_due'],
                           'journal_id': data['journal_id']})
        res.pay()
        return 'paid'

    def pay(self):
        """Generate invoice of student fee"""
        sequence_obj = self.env["ir.sequence"]
        for item in self:
            rec = item.student_payslip_id
            # if rec.number == "/":
            rec.number = sequence_obj.next_by_code("student.payslip"
                    ) or _("New")
            rec.state = "pending"
            partner = rec.student_id and rec.student_id.partner_id
            vals = {"partner_id": partner.id,
                    "invoice_date": self.date,
                    "journal_id": rec.journal_id.id,
                    "name": rec.number,
                    "student_payslip_id": rec.id,
                    "move_type": "out_invoice"}
            invoice_line = []
            product_id = self.env['product.product'].search([('default_code','=','fee')])
            # for line in rec.line_ids:
                #     replaced / deprecated fields of v13:
                #     default_debit_account_id,
                #     default_credit_account_id from account.journal
            acc_id = rec.journal_id.default_account_id.id
            # if line.account_id.id:
            #     acc_id = line.account_id.id
            invoice_line_vals = {
                "name": self.memo,
                "product_id": product_id.id,
                "account_id": acc_id,
                "quantity": 1.000,
                "price_unit": self.amount_paid}
            invoice_line.append((0, 0, invoice_line_vals))
            vals.update({"invoice_line_ids": invoice_line})
            # creates invoice
            invoice = self.env["account.move"].create(vals)
            invoice.action_post()
            # Register payment if journal is attached on SO
            if rec.journal_id:
                payment_method_manual_in = self.env.ref(
                    "account.account_payment_method_manual_in"
                )
                register_payments = (
                    self.env["account.payment.register"]
                    .with_context(active_model='account.move', active_ids=[invoice.id],
                                  journal_id=rec.journal_id.id).create(
                        {
                         "journal_id": self.journal_id.id,
                         "payment_date": self.date,
                         "amount": self.amount_paid

                         })
                )
                payment = self.env["account.payment"].browse(
                    register_payments.action_create_payments()
                )

                rec.paid_amount = self.amount_paid
                rec.due_amount = self.amount_due - self.amount_paid
                if rec.due_amount == 0:
                    rec.state = 'paid'
            return rec
