
{
    'name' : "Indoor Games Management System",
    'version' : '1.0',
    'category' : 'Indoor Games Management System',
    'summary': 'IGMS',
    'sequence': -105,
    'description': """
    The module contains all the common features of Indoor Games Management System.
    """,
    'author':'Suprodip Sarkar',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends' : ['sale'],
    'data': [
        'views/menu.xml',
        'security/ir.model.access.csv',
        'views/member_view.xml',
        # 'views/female_patient_view.xml',
        'views/game_view.xml',
        'views/membership_view.xml',
        'views/event_view.xml',
        'views/transaction_view.xml',
        'views/report_view.xml',
        'views/tournament_view.xml',
        # 'views/tevent_view.xml',
        'report/indoor_reports.xml',
        'report/indoor_reports__.xml',
        'report/purchase_reports.xml'
    ],
    'demo': [
        # 'demo/account_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

# 1. xml end tag typing mistake
# 2. action with same name in diff xml
# 3. no upgrade - no upgrade command in run server command
# 4. no action with id 512 found --> sol--> reload 3 times


