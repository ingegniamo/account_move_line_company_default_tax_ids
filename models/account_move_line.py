import logging

from odoo import api, models

_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('fiscal_position_id')
    def _onchange_fpos_id_show_update_fpos(self):
        super()._onchange_fpos_id_show_update_fpos()
        for line in self.invoice_line_ids:
            line.tax_ids = line._get_computed_taxes()

    def action_update_fpos_values(self):
        super().action_update_fpos_values()
        for line in self.invoice_line_ids:
            line.tax_ids = line._get_computed_taxes()


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_computed_taxes(self):
        tax_ids = super()._get_computed_taxes()
        if not tax_ids and self.display_type =='product':
            if self.move_id.is_sale_document(include_receipts=True):
                tax_ids = self.move_id.company_id.account_sale_tax_id
            elif self.move_id.is_purchase_document(include_receipts=True):
                
                tax_ids = self.move_id.company_id.account_purchase_tax_id

        if tax_ids and self.move_id.fiscal_position_id:
            tax_ids = self.move_id.fiscal_position_id.map_tax(tax_ids)
        return tax_ids