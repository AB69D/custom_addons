
{
    'name' : 'Hospital Management',
    'version' : '1.0',
    'category' : 'Hospital Management System',
    'summary': 'HMS',
    'sequence': -100,
    'description': """
    The module contains all the common features of Hospital Management System.
    """,
    'author':'Suprodip Sarkar SS',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends' : ['mail','hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/access_groups.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/employee_view.xml',
        'views/appointment_view.xml',
        'views/menu.xml',
        'views/purchase_reports.xml',
    ],
    'demo': [
        # 'demo/account_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
