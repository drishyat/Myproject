# -*- coding: utf-8 -*-
{
    'name': "Hotel demo",
    'summary': """Hotel  Demo""",
    'description': """Hotel""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',
    'depends': ['base',
                'mail',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/hotel_management.xml',
        'data/data.xml',



    ],
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,


}
