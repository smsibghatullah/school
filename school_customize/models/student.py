from datetime import datetime

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

    fees_heads_structure_line = fields.Many2many("student.fees.structure.line",
                                "student_fees_structures", "fees_id", "slip_id",
                                "Fees Structure", help="Fee structure line")


    def onchange_standard_id(self , res):
        records = res.env['student.fees.structure'].search([('class_id' , '=' ,
                        res.standard_id.standard_id.id)]).line_ids
        for record in records:
            res.fees_heads_structure_line = [(0, 0, {
                'product_id' : record.product_id.id ,
                'name':record.name,
                'code': record.code,
                'type':record.type,
                'account_id': record.account_id.id,
                'amount' : record.amount
            }) ]
        return  res

    @api.model
    def create(self, vals):
        res = super(StudentCustomize, self).create(vals)
        edit_res = self.onchange_standard_id(res)
        return res

    def write(self, vals):
        res = super(StudentCustomize, self).write(vals)
        print(self.standard_id.name)

        channel_id = self.env['mail.channel'].search([('name','=',self.standard_id.name)])
        if not channel_id:
            channel_id = self.env['mail.channel'].create({'name': self.standard_id.name})

        for item in self.parent_id:
            if item.commercial_partner_id.id not in channel_id.channel_partner_ids.ids:
                channel_id.channel_last_seen_partner_ids = [(0, 0,  { 'partner_id': item.commercial_partner_id.id })]

        return res

class StudentPayslipLine(models.Model):
    """Student PaySlip Line"""

    _inherit = "student.payslip.line"

    date = fields.Date("Date", readonly=True, help="Current Date of payslip",
                       default=fields.Date.context_today, )

    discount_amount = fields.Float("Discounted Amount",  readonly=True , digits=(16, 2), help="Discount Amount")

class StudentPayslip(models.Model):
    _inherit = "student.payslip"

    # payslip_structure_line = fields.One2many("student.fees.structure.line", "fees_id",
    #                            "Heads Line", help="PayslipsLine")
    payslip_structure_line = fields.Many2many("student.fees.structure.line",
                                                 "student_payslip_structures", "fees_id", "slip_id",
                                                 "PaySlip Structure", help="PayslipsLine")

    discount = fields.Float("Discount", readonly=True, digits=(16, 2), help="Discount")

    final_amount = fields.Float("Final Amount", readonly=True, digits=(16, 2), help="final Amount")


    due_date = fields.Date("Due Date", required=True, help="Due Date",
                       default=fields.Date.context_today)
    validity_date = fields.Date("Validity Date", required=True, help="Validity Date",
                       default=fields.Date.context_today)


    # fees_heads_structure_line = fields.Many2many("student.fees.structure.line",
    #                             "student_fees_structures", "fees_id", "slip_id",
    #                             "Fees Structure", help="Fee structure line")

    def payslip_cancel(self):
        self.state = "cancel"

    def payslip_payment(self):
        rec = self.env['payment.fee.wizard'].create({'student_payslip_id': self.id,
                                                     'amount_due': self.due_amount,
                                                     'description': self.name ,
                                                     'date': datetime.now().strftime('%Y-%m-%d') ,
                                                     'journal_id' : self.env['account.journal'].search([('name' , '=' , 'Cash')]).id ,




                                                     })
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

    # def payslip_confirm(self):
    #     """Method to confirm payslip"""
    #
    #     records = self.env['student.student'].search([('id', '=', self.student_id.id)]).fees_heads_structure_line
    #
    #     for record in records:
    #         self.payslip_structure_line = [(0, 0, {
    #             'product_id': record.product_id.id,
    #             'name': record.name,
    #             'code': record.code,
    #             'type': record.type,
    #             'account_id': record.account_id.id,
    #             'discount' : record.discount ,
    #             'amount':   record.amount - ((record.discount / 100 ) * record.amount)
    #         })]

    def payslip_confirm(self):
        """Method to confirm payslip"""
        print("payslip working =======================================>")
        records = self.env['student.student'].search([('id', '=', self.student_id.id)]).fees_heads_structure_line
        print(self.student_id.id,"==========;;;;;;;;;;;;;;======")
        for record in records:
            print(record.product_id.id,"lllllllllllllllllllllllllllllllll")
            self.payslip_structure_line = [(0, 0, {
                    'product_id': record.product_id.id,
                    'name': record.name,
                    'code': record.code,
                    'type': record.type,
                    'account_id': record.account_id.id,
                    'discount' : record.discount ,
                    'amount':   record.amount - record.discount
                    })]

            self.line_ids = [(0,0, {
                'slip_id': self.id,
                "product_id": record.product_id.id,
                "name": record.name,
                "code": record.code,
                "date": self.date,
                "type": record.type,
                "account_id": record.account_id.id,
                "amount": record.amount,
                "discount_amount" : record.discount,
                "currency_id": record.currency_id.id or False,
                "currency_symbol": record.currency_symbol or False
            })]

        for rec in self:
            if not rec.journal_id:
                raise ValidationError(_("Kindly, Select Account Journal!"))
            if not rec.fees_structure_id:
                raise ValidationError(_("Kindly, Select Fees Structure!"))


            old_payslips = self.env['student.payslip'].search([('state','in',['draft','confirm']),
                                                               ('student_id','=',rec.student_id.id)])
            old_payslip_partial_paid = self.env['student.payslip'].search([('state','in',['pending']),
                                                               ('student_id','=',rec.student_id.id)])
            lines = []
            # for old_payslip in old_payslips:
            #     for line in old_payslip.line_ids:
            #         line_vals = {"slip_id": rec.id,
            #                      "product_id": line.product_id.id,
            #                      "name": line.name,
            #                      "code": line.code,
            #                      "date": line.date,
            #                      "type": line.type,
            #                      "account_id": line.account_id.id,
            #                      "amount": line.amount,
            #                      "currency_id": line.currency_id.id or False,
            #                      "currency_symbol": line.currency_symbol or False}
            #         lines.append((0, 0, line_vals))
            #     old_payslip.state = 'cancel'
            # rec.write({"line_ids": lines})

            lines = []
            print('endddddddddddddddddddddddddddd')
            product_partial_payment = self.env['product.product'].search([('default_code','=','PartialPayment')])
            for old_payslip in old_payslip_partial_paid:
                # for line in old_payslip.line_ids:
                print(product_partial_payment.id,"kkkkkkkkkkkkkkkkkkkkkkk")
                line_vals = {"slip_id": rec.id,
                                 "product_id": product_partial_payment.id,
                                 "name": old_payslip.number,
                                 "code": "PAR",
                                 "date": old_payslip.date,
                                 "type": "month",
                                 "account_id": 39,
                                 "discount_amount" : 0,
                                 "amount": old_payslip.due_amount,
                                 # "currency_id": line.currency_id.id or False,
                                 # "currency_symbol": line.currency_symbol or False
                                 }
                lines.append((0, 0, line_vals))
                old_payslip.state = 'cancel'
            rec.write({"line_ids": lines})


            lines = []
            # for data in rec.fees_structure_id.line_ids or []:
            #     line_vals = {"slip_id": rec.id,
            #                 "product_id": data.product_id.id,
            #                 "name": data.name,
            #                 "code": data.code,
            #                 "date": rec.date,
            #                 "type": data.type,
            #                 "account_id": data.account_id.id,
            #                 "amount": data.amount,
            #                 "currency_id": data.currency_id.id or False,
            #                 "currency_symbol": data.currency_symbol or False}
            #     lines.append((0, 0, line_vals))
            # rec.write({"line_ids": lines})




            amount= 0.0
            discount = 0.0
            # amount = sum(data.amount for data in rec.line_ids)
            for data in rec.line_ids:
                amount += data.amount
                discount += data.discount_amount

            rec.register_id.write({"total_amount": rec.total})
            rec.write({"total": amount,
                       "discount": discount ,
                       "final_amount" : amount - discount ,
                    "state": "confirm",
                    "due_amount": amount - discount ,
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



class StuedntsFeeHead(models.Model):

    _inherit = "student.fees.structure.line"

    discount = fields.Float('Discount')





