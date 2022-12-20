from odoo import models, fields, api


class StudentReminder(models.Model):
    """Defining student reminder."""
    _inherit = 'student.reminder'

    @api.model
    def check_user(self):
        '''Method to get default value of logged in Student'''
        return self.env['student.student'].search([
                                        ('user_id', '=', self._uid)]).id

    class_id = fields.Many2one('school.standard', 'Class')
    stu_id = fields.Many2one('student.student', 'Student Name', required=False,
                            default=check_user, help='Relative student')


    @api.model
    def create(self, vals):
        """Inherited create method to assign value to users for delegation"""
        class_id = vals['class_id']
        students = self.env['student.student'].search([('standard_id','=',class_id)])
        print(students)
        for item in students:
            vals['stu_id'] = item.id
            res = super(StudentReminder, self).create(vals)
        return res