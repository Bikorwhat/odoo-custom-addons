# -*- coding: utf-8 -*-
{
    'name': "sales ext",

    'summary': "Short (1 phrase/line) summary of the sales's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/wizard.xml',
        'views/sales_ext_view.xml',
    ],
    # only loaded in demonstration mode
    'application': True,  # ✅ Important! Ensures it appears in Apps menu
    'installable': True,
    'auto_install': False,
}

