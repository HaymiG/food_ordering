from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_menu_item = fields.Boolean(string="Is Food Item")
    food_category_id = fields.Many2one('food_ordering.food_category', string='Food Category')

    @api.model
    def create(self, vals):
        product = super().create(vals)
        product._create_variant_ids()  # important for POS
        if vals.get('is_menu_item'):
            self.env['food_ordering.food_item'].create({
                'product_id': product.product_variant_id.id,
                'category_id': vals.get('food_category_id'),
                'name': product.name,
                'price': product.list_price,
            })
        return product

    def write(self, vals):
        res = super().write(vals)
        for product in self:
            food_item = self.env['food_ordering.food_item'].search([('product_id', '=', product.product_variant_id.id)], limit=1)
            if 'is_menu_item' in vals:
                if vals['is_menu_item'] and not food_item:
                    self.env['food_ordering.food_item'].create({
                        'product_id': product.product_variant_id.id,
                        'category_id': product.food_category_id.id if product.food_category_id else False,
                        'name': product.name,
                        'price': product.list_price,
                    })
                elif not vals['is_menu_item'] and food_item:
                    food_item.unlink()
            elif food_item:
                food_item.name = product.name
                food_item.price = product.list_price
                food_item.category_id = product.food_category_id.id
        return res

    def unlink(self):
        food_items = self.env['food_ordering.food_item'].search([('product_id', 'in', self.mapped('product_variant_id').ids)])
        food_items.unlink()
        return super().unlink()
