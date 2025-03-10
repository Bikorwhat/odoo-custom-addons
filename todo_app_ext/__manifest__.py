# -*- coding: utf-8 -*-
{
    'name': "Todo App Extension",
    'summary': "Enhances the Todo App with additional features",
    'description': """
        This module extends the Todo App by adding follow-ups, 
        tracking, and additional functionalities.
    """,
    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Productivity',
    'version': '0.1',

    # Dependencies (ensure 'todo_app' exists)
    'depends': ['base', 'mail', 'todo_app'],

    # Always loaded data files
    'data': [
        'security/ir.model.access.csv',  # Ensure this file exists
        'views/view.xml',  # Ensure the correct path
    ],

    # Uncomment if you actually have demo data
    # 'demo': [
    #     'demo/demo.xml',
    # ],

    'installable': True,
    'application': True,
    'auto_install': False,  
}
