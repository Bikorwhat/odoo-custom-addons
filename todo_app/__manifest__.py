# -*- coding: utf-8 -*-
{
    'name': "todo_app",

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
    'depends': ['base',
                'mail',"portal","web",'helpdesk_systems'
                ],

    # always loaded
    'data': [
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        
        'report/ir_actions_report_templates.xml',
        'report/ir_actions_report.xml',
        
        
        'data/todo_data.xml',
        'data/corn_jobs.xml',
        'data/mail_template.xml',
        
        'wizard/todo_remark_view.xml',
        
        'views/todo.xml',
        'views/todo_category.xml',
        'views/todo_task.xml',
        'views/todo_tag_view.xml',
        'views/todo_stage_view.xml',
        'views/todo_task_template.xml',
        'views/todo_menu_views.xml',
        'views/portal_todo.xml',
        
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,  
    'auto_install': False, 
}

