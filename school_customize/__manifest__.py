# -*- coding: utf-8 -*-
{
    'name': "Alhamd School Project",

    'summary': """DSM School customization for Alhum Schhol""",

    'description': """
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'school', 'school_fees'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/student.xml',
        'views/parent.xml',
        'views/teacher.xml',
        'views/school_fees_view.xml',
        'views/admission_registrater.xml',
        'data/cron.xml',
        'wizards/payment_fee_wizard.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
