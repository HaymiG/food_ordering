from odoo import models, fields

# models/food_category.py
class FoodCategory(models.Model):
    _name = 'food_ordering.food_category'
    _description = 'Food Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text()
    food_item_ids = fields.One2many('food_ordering.food_item', 'category_id', string="Items")
    # image_128 = fields.Image(string="Category Image") 
    # image_1920 = fields.Image(string="Category Image")


