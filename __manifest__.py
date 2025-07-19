{
    'name': 'Food Ordering System',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Backend models for food ordering system',
    'depends': ['product', 'website_sale', 'website_sale_stock', 'point_of_sale'],
    'data': [
         'data/sequence_data.xml',
        'security/ir.model.access.csv',
        # 'views/product_template_inherit.xml',
        'views/website_pages.xml',
        'views/homepage.xml',
        'views/header.xml',
        'views/footer.xml',
        'views/website_templates.xml',
        'views/restaurant_views.xml',
        'views/food_category_views.xml',
        'views/food_item_views.xml',
        'views/customization_option_views.xml',
        # 'views/promo_code_views.xml',
        'views/order_views.xml',
        #  'views/payment_views.xml',
        # 'views/website_menu_template.xml',
        
        'views/food_menu.xml',
    ],
    'controllers': [
    'controllers/controllers.py',
    ],
    'assets': {
        'web.assets_frontend': [
    
            'food_ordering/static/src/css/header.css',
            'food_ordering/static/src/css/footer.css',
            'food_ordering/static/src/css/homepage.css',
            'food_ordering/static/src/css/offer_styles.css',
            'food_ordering/static/src/js/offer_scripts.js',
             'food_ordering/static/src/img',
            
        ]
    },
    'images': ['icon.png', 'static/description/icon.png'],

    'installable': True,
    'application': True,
}
