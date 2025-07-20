from odoo import models, fields

class Restaurant(models.Model):
    _name = 'food_ordering.restaurant'
    _description = 'Restaurant'

    name = fields.Char(string='Name', required=True)
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
