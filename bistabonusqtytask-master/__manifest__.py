
{
    'name' : "Bista Bonus",
    'version' : '1.0',
    'category' : 'Bista Bonus qty task',
    'summary': 'IGMS',
    'sequence': -105,
    'description': """
    The module contains all the common features of Bonus qty.
    """,
    'author':'Suprodip Sarkar',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends' : ['sale', 'stock'],
    'data': [
        'views/menu.xml',
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        # 'views/game_view.xml',
        # 'views/membership_view.xml',
        # 'views/event_view.xml',
    ],
    'demo': [
        # 'demo/account_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

