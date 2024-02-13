# -*- coding: utf-8 -*-
{
    'name': "Alhamd School Project",

    'summary': """DSM School customization for Alhamd school""",

    'description': """
    """,

    'author': "Dynamic Solution Maker",
    'website': "http://dsmpk.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'school', 'hr_attendance' , 'school_fees' , 'account'],

    # always loaded,
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/student.xml',
        'views/parent.xml',
        'views/teacher.xml',
        'views/school_fees_view.xml',
        'views/admission_registrater.xml',
        'views/student_payslip.xml',
        'views/notice.xml',
        'data/cron.xml',
        'wizards/payment_fee_wizard.xml',
        'reports/report_view.xml',
        'views/data.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
