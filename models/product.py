
from odoo import models, fields, api

class Product(models.Model):
    _name = 'mysales.product'
    _description = "its my product module"
    name = fields.Char("Name")
    desc = fields.Char("Description")
    price = fields.Float("price", digits=(6, 2))
    in_stock = fields.Integer("in stock", required=True)
    cust_id = fields.Many2one('mysales.customer', string='Customer')
    product_pic = fields.Binary("product_pic", attachment=True)

