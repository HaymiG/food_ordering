from odoo import models

class Customer(models.Model):
    _inherit = 'res.partner'

    # Extend partner if needed, else you can skip this file for now.
    # e.g. add delivery address fields if needed
