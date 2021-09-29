# -*- coding: utf-8 -*-
{
    'name': "Hotel New",
    'summary': """Hotel """,
    'description': """Hotel""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',
    'depends': ['base',
                'mail',
                'stock',
                'contacts',

                ],
    'data': [
        'security/ir.model.access.csv',
        'views/hotel_management.xml',
        'views/order_food.xml',
        'views/tolerance.xml',
        'data/data.xml',



    ],
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,


}
