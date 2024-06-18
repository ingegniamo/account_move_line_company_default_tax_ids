import logging


from odoo import api, fields, models, Command, _


_logger = logging.getLogger(__name__)


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
