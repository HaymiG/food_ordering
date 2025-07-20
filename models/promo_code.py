from odoo import models, fields
from datetime import date

class PromoCode(models.Model):
    _name = 'food_ordering.promo_code'
    _description = 'Promo Code'

    code = fields.Char(string='Code', required=True)
    discount_percent = fields.Float(string='Discount %')
    valid_from = fields.Date(string='Valid From', default=fields.Date.today)
    valid_to = fields.Date(string='Valid To')
