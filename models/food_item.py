from odoo import models, fields

class FoodItem(models.Model):
    _name = 'food_ordering.food_item'
    _description = 'Food Item'

    product_id = fields.Many2one('product.product', string='POS Product')
    category_id = fields.Many2one('food_ordering.food_category', string="Category", required=True)
    restaurant_id = fields.Many2one('food_ordering.restaurant', string='Restaurant')
    description = fields.Text(string='Description')
    image_1920 = fields.Image(string="Image")
    price = fields.Float(related='product_id.list_price', string='Price', store=True)
    name = fields.Char(related='product_id.name', string='Food Name', store=True)
    is_offer = fields.Boolean(string="Is Offer", default=False)


