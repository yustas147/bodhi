# -*- coding: utf-8 -*-
{
    'name': "Bodhi integration",
    'author': "Simbioz, Yury Stasovsky",
    'license': 'LGPL-3',
    'website' : "https://coraltree.co",
    'category': 'Custom integration',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['sce'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
       # 'wizard/wiz_view.xml',
        'view.xml',
        'views/bodhi.xml',
    ],
    'installable': True
}
