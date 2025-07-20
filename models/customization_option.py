from odoo import models, fields

class CustomizationOption(models.Model):
    _name = 'food_ordering.customization_option'
    _description = 'Customization Option'

    name = fields.Char(string='Name', required=True)
    price_extra = fields.Float(string='Additional Price')
    option_type = fields.Selection([
        ('checkbox', 'Checkbox'),
        ('select', 'Select')
    ], string='Type', required=True)
