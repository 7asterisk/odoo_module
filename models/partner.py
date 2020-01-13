from odoo import fields, models

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    company = fields.Boolean("Company", default=False)

    customer_ids = fields.Many2many('mysales.customer', string="customer", readonly=True)
