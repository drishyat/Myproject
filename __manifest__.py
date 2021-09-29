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
                'sale',
                ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'wizard/validate_tolerance.xml',
        'wizard/report_generate.xml',
        'wizard/xlxs_report_generate.xml',
        'views/action_manager.xml',
        'views/accomodation.xml',
        'views/order_food.xml',
        'views/tolerance.xml',
        'views/tree_color.xml',
        'reports/report.xml',
        'reports/gerate_report_template.xml',

    ],
    'demo': [
        # 'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,


}
