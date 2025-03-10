{
    'name': 'helpdesk to todo Bridge',
    'version': '1.0',
    'category': 'Sales',
    'author': 'Your Name',
    'depends': ['helpdesk_systems','todo_app','crm'],  
    'data': [
        'security/ir.model.access.csv',
        'views/crm_wizard_view.xml',
        'views/todo_wizard_view.xml',
        'views/view.xml',
    ],
    'installable': True,
    'application': False,
}
