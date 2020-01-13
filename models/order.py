# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from datetime import datetime, timedelta


class mysales(models.Model):
    _name = 'mysales.order'
    _description = "its orders"
    _rec_name = 'order_id'

    order_id = fields.Char(string='Order no', required=True, copy=False,
                           duplicate=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    cust_id = fields.Many2one('mysales.customer', string='Customer', required=True)
    profile_pic = fields.Binary(string="profile pic", related="cust_id.profile_pic")
    pno= fields.Char(string="phone no", related="cust_id.pno")
    order_line_ids = fields.One2many('mysales.orderline', 'sales_order_id', string='product')
    total = fields.Float("total", compute='_compute_total')
    order_time = fields.Datetime(string="order time", default=datetime.now(), required=True, readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
    ], default='draft', copy=False)

    start_date = fields.Datetime("start_time", default=datetime.now())
    end_date = fields.Datetime("start_time", default=datetime.now())

    @api.model
    def create(self, vals):
        if vals.get('order_id', _('New')) == _('New'):
            vals['order_id'] = self.env['ir.sequence'].next_by_code('mysales.order.sequence') or _('New')
        res = super(mysales, self).create(vals)
        return res

    @api.depends('order_line_ids.sub_total')
    def _compute_total(self):
        for order in self:
            order.total = 0.0
            for i in order.order_line_ids:
                order.total = order.total + i.sub_total
                print('total: ', order.total)

    @api.multi
    def draft_progressbar(self):
        if self.state == 'done':
            for order in self:
                for line in order.order_line_ids:
                    line.product_id.in_stock = line.product_id.in_stock + line.quantity

        self.write({
            'state': 'draft',
        })

    @api.one
    def confirm_progressbar(self):
        self.write({
            'state': 'confirm',
        })

    @api.multi
    def done_progressbar(self):
        self.write({
            'state': 'done',
        })
        for order in self:
            for line in order.order_line_ids:
                line.product_id.in_stock = line.product_id.in_stock - line.quantity

    # @api.one
    # def done_order(self):
    #     for order in self:
    #         for i in order.order_line_ids:
    #             # order.total = order.total + i.sub_total


class order_lines(models.Model):
    _name = 'mysales.orderline'
    _description = "order line"
    product_id = fields.Many2one('mysales.product', string='product_id', required=True)
    sales_order_id = fields.Many2one('mysales.order', string='order name')
    quantity = fields.Integer('quantity', default=1)
    price = fields.Float("price", related='product_id.price')
    in_stock = fields.Integer('in stock', related='product_id.in_stock')
    sub_total = fields.Float("sub total", compute='_compute_subtotal')
    tax = fields.Float("tax", default=0)
    state = fields.Selection('state', related='sales_order_id.state')

    @api.multi
    @api.depends('quantity', 'price', 'tax')
    def _compute_subtotal(self):
        for i in self:
            price = i.price + (i.price / 100) * i.tax
            i.sub_total = i.quantity * price
