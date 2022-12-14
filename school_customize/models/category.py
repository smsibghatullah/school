from odoo import models, fields, api
from datetime import date
class Category(models.Model):
    _name = 'school.customize.category'
    _rec_name = 'category_name'

    category_name = fields.Char(string='Category')

    @api.model
    def _cron_mark_daily_attendance(self):
        classes_records = self.env['school.standard'].sudo().search([])
        print('sdsdddddddddddddddddddd')
        for classes_record in classes_records:
            print(classes_record)
            if (classes_record.user_id.id):
                rec = self.env['daily.attendance'].create({
                    'user_id': classes_record.user_id.id,
                    'standard_id': classes_record.id,
                    'date': date.today(),
                })
                print(rec)
                new_records = self.env['daily.attendance.line'].search([('standard_id','=',rec.id)])
                for item in new_records:
                    item.is_absent = True
                    item.is_present = False