# -*- coding: utf-8 -*-
{
    'name': "Bodhi integration",
    'author': "Simbioz, Yury Stasovsky",
    'license': 'LGPL-3',
    'website' : "https://coraltree.co",
    'category': 'Custom integration',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'purchase', 'mrp', 'sce'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
       # 'wizard/wiz_view.xml',
        'view.xml',
        'views/bodhi.xml',
        'views/sce_inventory.xml',
        'views/sale_order.xml',
        'views/purchase_order.xml'
    ],
    'installable': True,
}
