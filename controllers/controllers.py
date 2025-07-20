from odoo import http
from odoo.http import request

class FoodOrderingWebsite(http.Controller):

    @http.route('/', type='http', auth="public", website=True)
    def homepage(self, **kwargs):
        categories = request.env['food_ordering.food_category'].sudo().search([])
        return request.render("food_ordering.food_ordering_homepage", {
            'categories': categories
        })

    @http.route('/about', type='http', auth='public', website=True)
    def about_page(self, **kwargs):
        return request.render('food_ordering.about_page_template')

    @http.route('/offers', type='http', auth='public', website=True)
    def offers_page(self, **kwargs):
        return request.render('food_ordering.offers_page_template')

    @http.route('/menu', type='http', auth="public", website=True)
    def menu(self, category_id=None, search=None, price_min=None, price_max=None, **kwargs):
        Category = request.env['food_ordering.food_category'].sudo()
        FoodItem = request.env['food_ordering.food_item'].sudo()

        categories = Category.search([])
        # food_items = request.env['food_ordering.food_item'].sudo().search([...])


        domain = []
        if category_id:
            domain.append(('category_id', '=', int(category_id)))
        if search:
            domain = ['|', ('name', 'ilike', search), ('description', 'ilike', search)] + domain
        if price_min:
            domain.append(('price', '>=', float(price_min)))
        if price_max:
            domain.append(('price', '<=', float(price_max)))

        food_items = FoodItem.search(domain)

        return request.render("food_ordering.menu_page", {
            "categories": categories,
            "food_items": food_items,
            "selected_category": int(category_id) if category_id else None,
            "search_term": search,
            "price_min": price_min,
            "price_max": price_max,
        })

    @http.route(['/cart/add/<int:food_item_id>'], type='http', auth="public", website=True, methods=['POST'])
    def add_to_cart(self, food_item_id, **kwargs):
        cart = request.session.get('cart', {})
        quantity = int(kwargs.get('quantity', 1))

        if str(food_item_id) in cart:
            cart[str(food_item_id)] += quantity
        else:
            cart[str(food_item_id)] = quantity

        request.session['cart'] = cart
        request.session['cart_success_msg'] = "Item added to cart successfully!"
        request.session.modified = True
        return request.redirect('/cart')

    @http.route(['/cart'], type='http', auth="public", website=True)
    def view_cart(self, **kwargs):
        cart = request.session.get('cart', {})
        food_item_ids = [int(i) for i in cart.keys()]
        
        # Fetch only existing food items from DB
        food_items = request.env['food_ordering.food_item'].sudo().search([('id', 'in', food_item_ids)])
        
        # Clean cart: keep only existing item IDs
        valid_ids = set(str(item.id) for item in food_items)
        cleaned_cart = {k: v for k, v in cart.items() if k in valid_ids}
        
        # Update session cart if cleaned differs from original
        if cleaned_cart != cart:
            request.session['cart'] = cleaned_cart
            request.session.modified = True
            cart = cleaned_cart
        
        # Calculate total only for valid items
        total = sum(item.price * cart.get(str(item.id), 0) for item in food_items)
        
        success_msg = request.session.pop('cart_success_msg', '')
        
        return request.render('food_ordering.cart_page', {
            'cart': cart,
            'food_items': food_items,
            'total': total,
            'success_msg': success_msg,
        })

    @http.route(['/cart/remove/<int:food_item_id>'], type='http', auth="public", website=True)
    def remove_from_cart(self, food_item_id, **kwargs):
        cart = request.session.get('cart', {})
        cart.pop(str(food_item_id), None)
        request.session['cart'] = cart
        request.session['cart_success_msg'] = "Item removed from cart."
        request.session.modified = True
        return request.redirect('/cart')

    @http.route('/checkout', auth='user', website=True)
    def checkout(self, **kwargs):
        cart = request.session.get('cart', {})
        if not cart:
            return request.redirect('/cart')

        food_items = request.env['food_ordering.food_item'].sudo().browse([int(i) for i in cart.keys()])
        total = sum(item.price * cart.get(str(item.id), 0) for item in food_items)

        return request.render('food_ordering.checkout_page', {
            'cart': cart,
            'food_items': food_items,
            'total': total,
        })

    @http.route('/checkout/confirm', type='http', auth='user', website=True, methods=['POST'])
    def confirm_order(self, **post):
        cart = request.session.get('cart', {})
        if not cart:
            return request.redirect('/cart')

        delivery_address = post.get('delivery_address', '').strip()
        payment_method = post.get('payment_method', 'cash')

        order = request.env['food_ordering.order'].sudo().create({
            'customer_id': request.env.user.partner_id.id,
            'delivery_address': delivery_address,
            'payment_method': payment_method,
        })

        for food_id_str, qty in cart.items():
            food_id = int(food_id_str)
            quantity = int(qty)
            food_item = request.env['food_ordering.food_item'].sudo().browse(food_id)
            if food_item.exists():
                request.env['food_ordering.order_line'].sudo().create({
                    'order_id': order.id,
                    'food_item_id': food_item.id,
                    'quantity': quantity,
                })

        request.session['cart'] = {}
        request.session.modified = True

        return request.render('food_ordering.order_confirmation')
