from odoo import fields, models, api, _ 


class SaleOrder(models.Model):
    _inherit = "sale.order.line"

    bonus_qty = fields.Integer(string="Bonus Quantity", compute="_get_bonus")


    def _get_bonus(self):
        for item in self:
            # item.bonus_qty = ((item.product_uom_qty) // int(item.product_template_id.buy_qty)) * int(item.product_template_id.bonus_qty)
            if int(item.product_template_id.buy_qty) != 0:
                item.bonus_qty = ((item.product_uom_qty) // int(item.product_template_id.buy_qty)) * int(item.product_template_id.bonus_qty)

            print("..............................item.bonus_qty", item.bonus_qty)
            print("..............................item.product_uom_qty", item.product_uom_qty)
            print("..............................item.product_template_id.buy_qty", item.product_template_id.buy_qty)
            print("..............................item.product_template_id.buy_qty", item.product_template_id.bonus_qty)




    # @api.onchange('product_uom_qty')
    # def onchange_product_template_id(self,):
    #     for item in self:
    #         item.bonus_qty = item.product_uom_qty % item.product_template_id.bonus_qty
    #         print("..............................onchange print", item.bonus_qty)
    #     print("..............................onchange print", self.product_template_id.min_qty)

# action_confirm() --> _action_confirm() --> _create_analytic_account() --> _prepare_analytic_account_data()

