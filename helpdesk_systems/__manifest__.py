# -*- coding: utf-8 -*-
{
    'name': "helpdesk_systems",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

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
    'depends': ['base','portal','mail'],

    # always loaded
    'data': [
          'security/ir.model.access.csv',
        'security/model.security.xml',
        'data/stage_data.xml',
        'wizard/stage_wizard.xml',
        'views/report.xml',
        'views/views.xml',
        'views/category.xml',
        'views/helpdesk_team_views.xml',
         'views/portal_list.xml',
        'views/type.xml',
        'views/tag.xml',
        'views/menu.xml',
        'views/portal_templates.xml',
        'reports/ir_actions_report_template.xml',
        'reports/ir_actions_report.xml',
          'reports/team_progress.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,  # ✅ Important! Ensures it appears in Apps menu
    'installable': True,
    'auto_install': False,
}

