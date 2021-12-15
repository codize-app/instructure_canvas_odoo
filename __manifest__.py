# -*- coding: utf-8 -*-
{
    'name': "Instructure Canvas Odoo Connector",

    'summary': """
        Connector Odoo-Instructure Canvas""",

    'description': """
        Connector Odoo-Instructure Canvas
    """,

    'author': "Codize",
    'website': "https://www.codize.ar",

    'category': 'Sales',
    'version': '0.1',

    'depends': ['base', 'sale', 'product'],

    'data': [
        'views/res_company.xml',
        'views/res_partner.xml',
        'views/product_template.xml',
    ]
}
