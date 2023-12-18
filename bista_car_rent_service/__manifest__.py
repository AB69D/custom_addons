{
    'name': 'Car Rent ',
    'version': '16.0.1.0.0',
    'description': 'This module is for automate the car rent service',
    'author': 'AB9D',
    'category':'Service',
    'website': 'oabdoo.com',
    'depends': ['base','stock',],
    'sequence': -20000000,
    'summary':'its provite a service for car rent',
    'data': [
        'data/user_form_sequence.xml',
        'data/rent_history_sequence.xml',
        
        'views/user_form_view.xml',
        'views/car_product_view.xml',
        'views/color_tag_view.xml',
        'views/rent_package_view.xml',
        'views/car_brand_view.xml',
        'views/rent_history_view.xml',
        'views/payment_history_view.xml',
        'views/customer_invoice.xml',
        
        
        
        'wizard/payment_confirmation_wizard_view.xml',
        'wizard/down_payment.xml',
        
        
        'report/user_form_report.xml',
        
        'views/menu.xml',
        'security/access_group.xml',
        'security/ir.model.access.csv',
        
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
