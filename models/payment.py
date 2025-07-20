from odoo import models, fields

class Payment(models.Model):
    _name = 'food_ordering.payment'
    _description = 'Payment'

    order_id = fields.Many2one('food_ordering.order', string='Order')
    amount = fields.Float(string='Amount')
    method = fields.Selection([
        ('cash', 'Cash on Delivery'),
        ('online', 'Online Payment')
    ], string='Payment Method')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('failed', 'Failed')
    ], string='Status', default='pending')
