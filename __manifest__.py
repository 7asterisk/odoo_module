{
    'name': "mysales",

    'summary': """
       my sales
       """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['purchase', 'base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_wizard.xml',
        'views/views.xml',
        'views/product_views.xml',
        'views/order_views.xml',
        'views/templates.xml',
        'sequence/ir_order_sequence.xml',
        'sequence/ir_customer_sequence.xml',
        'reports/order_report_template.xml',
        'views/email_tamplate.xml',
        'views/partner_view.xml',
        'scheduler/customer_festival_scheduler.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
