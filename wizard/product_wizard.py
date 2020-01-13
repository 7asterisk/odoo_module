from odoo import fields, models, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, RedirectWarning, ValidationError


class ProductWizard(models.TransientModel):
    _name = "wizard.product"

    state = fields.Selection([
        ('confirm', 'Confirm'),
        ('done', 'Done')
    ], default='confirm'
    )

    def get_context(self):
        return self._context.get('active_id')

    product_ids = fields.Many2one('mysales.product', string="product", default=lambda self: self.get_context())
    in_stock = fields.Integer('in stock')

    @api.one
    def confirm_progressbar(self):
        self.write({
            'state': 'confirm',
        })

    @api.one
    def done_progressbar(self):
        self.write({
            'state': 'done',
        })
        for obj in self:
            for ele in obj.product_ids:
                ele.in_stock = obj.in_stock


