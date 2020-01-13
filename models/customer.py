# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from datetime import datetime
from odoo import models, fields, api, _
from datetime import date
import re


class Customer(models.Model):
    _name = 'mysales.customer'
    _description = "Customer"

    name = fields.Char("Name", required=True)
    customer_id = fields.Char("customer id", required=True, copy=False, duplicate=False, readonly=True,
                              index=True, default=lambda self: _('New'))
    address = fields.Char("Address")
    pno = fields.Char("Phone No.")
    profile_pic = fields.Binary("photo", label=False, attachment=True)
    dob = fields.Date(string="Date of birth", required=True, default="1972-11-11")
    email = fields.Char(string="email", required=True)
    adhar = fields.Char(string="adhar no", required=True)
    panno = fields.Char(string='pan no', required=True)
    festival_date = fields.Date(string='festival date')
    festival_name = fields.Char(string="festival name")

    @api.multi
    def send_festival_email(self):
        customer_obj = self.env['mysales.customer']
        template = self.env.ref('mysales.festival_wish_email', False)
        today = datetime.now()
        nice_today = '%-' + today.strftime('%m') + '-' + today.strftime('%d')
        cust_id = customer_obj.search([('festival_date', 'like', nice_today)])
        if cust_id:
            try:
                for val in cust_id:
                    template.send_mail(val.id)
            except Exception as e:
                print("Exception", e)
        return True

    @api.model
    def create(self, vals):
        if vals.get('customer_id', _('New')) == _('New'):
            vals['customer_id'] = self.env['ir.sequence'].next_by_code('mysales.customer.sequence') or _('New')
        res = super(Customer, self).create(vals)
        return res

    @api.multi
    def send_mail(self):
        template = self.env.ref('mysales.customer_email', False)
        template.send_mail(self.id)
        return True

    @api.multi
    @api.constrains('dob', 'email', 'panno', 'pno', 'adhar')
    def dob_validation(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        print("today date: ", age)
        if age < 18:
            self.dob = date(1992, 5, 17)
            print(self.dob)
            raise UserError("You age must be above 18")
        email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

        if not re.search(email_regex, self.email):
            raise UserError("email format is invalid")
        pan_regex = "^([a-zA-Z]){5}([0-9]){4}([a-zA-Z]){1}?$"
        if not re.search(pan_regex, self.panno):
            raise UserError("pan no is not valid")
        pno_regex = "[0-9]{10}"
        if not re.search(pno_regex, self.pno):
            raise UserError("phone number is not valid")
        adhar_regex = "[0-9]{12}"
        if not re.search(adhar_regex, self.adhar):
            raise UserError("adhar number is not valid")
