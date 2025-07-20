from odoo import models, fields, api

class Order(models.Model):
    _name = 'food_ordering.order'
    _description = 'Order'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                       default=lambda self: self.env['ir.sequence'].next_by_code('food_ordering.order'))
    customer_id = fields.Many2one('res.partner', string='Customer')
    order_line_ids = fields.One2many('food_ordering.order_line', 'order_id', string='Order Lines')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('delivering', 'Delivering'),
        ('done', 'Done')
    ], default='draft', string="Status")

    # Buttons visibility
    can_confirm = fields.Boolean(compute="_compute_button_visibility")
    can_prepare = fields.Boolean(compute="_compute_button_visibility")
    can_deliver = fields.Boolean(compute="_compute_button_visibility")
    can_done = fields.Boolean(compute="_compute_button_visibility")

    delivery_address = fields.Char(string="Delivery Address")
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('telebirr', 'TeleBirr'),
        ('cbe', 'CBE Birr'),
        ('other', 'Other')
    ], string="Payment Method", default='cash')

    total_price = fields.Float(string='Total Price', compute='_compute_total_price')

    @api.depends('status')
    def _compute_button_visibility(self):
        for order in self:
            order.can_confirm = order.status == 'draft'
            order.can_prepare = order.status == 'confirmed'
            order.can_deliver = order.status == 'preparing'
            order.can_done = order.status == 'delivering'

    @api.depends('order_line_ids.price_subtotal')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(line.price_subtotal for line in order.order_line_ids)

    def action_confirm(self):
        self.status = 'confirmed'

    def action_prepare(self):
        self.status = 'preparing'

    def action_deliver(self):
        self.status = 'delivering'

    def action_done(self):
        self.status = 'done'


class OrderLine(models.Model):
    _name = 'food_ordering.order_line'
    _description = 'Order Line'

    order_id = fields.Many2one('food_ordering.order', string='Order')
    food_item_id = fields.Many2one('food_ordering.food_item', string='Food Item')
    quantity = fields.Integer(string='Quantity', default=1)
    price_unit = fields.Float(string='Unit Price', related='food_item_id.price')
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit

            line.price_subtotal = line.quantity * line.price_unit


