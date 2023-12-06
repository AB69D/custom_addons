{
    'name': 'Bista Test Module',
    'version': '16.0.1.0.0',
    'description': 'This module is just for testing my module',
    'author': 'AB9D',
    'category':'Test Module',
    'website': 'oabdoo.com',
    'depends': ['base','mail'],
    'sequence': -10000000,
    'summary':'this module build for test',
    'data': [
        'views/base_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
