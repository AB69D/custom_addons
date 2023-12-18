from odoo import fields, models, api, _ 
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # bonus_qty = fields.Char(string="Bonus Quantity")

    def action_confirm(self):

        # for item in self.order_line:
            # if item.product_uom_qty + item.bonus_qty > item.product_template_id. :
            # search_redmi_ids = self.env['stock.quant'].search([('product_tmpl_id', '=', item.product_template_id.product_tmpl_id)])
            
            
            # search_redmi_ids = self.env['stock.quant'].search([('product_id', '=', item.product_template_id.name)])
            # cnt = 0
            # for rec in search_redmi_ids:
            #     print("cnt: ", cnt, "id: ", rec.id)
            #     cnt += 1
            # if item.product_uom_qty + item.bonus_qty > cnt:
            #     raise UserError("cnt")
            # print("................Error not found................", cnt)



            # search_count = self.env['stock.quant'].search_count([('product_id', '=', item.product_template_id.name)])
            # print("....................Search Count...", search_count)

        # print("Error", cnt)


        for item in self.order_line:
            if item.product_uom_qty + item.bonus_qty > item.product_template_id.qty_available:
                raise UserError("Quantity not available")
            print(".............................qty_available", item.product_template_id.name)
            print(".............................qty_available", item.product_template_id.qty_available)
            print(".........................item.qty_available", item.product_template_id.qty_available)
            
            
        return super(SaleOrder, self).action_confirm()
