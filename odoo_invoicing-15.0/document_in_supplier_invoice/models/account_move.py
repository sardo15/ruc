from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_l10n_latam_documents_new_domain(self):
        self.ensure_one()
        return [('active', '=', True), ('account_journal_id', '=', self.journal_id.id), ('country_id', '=', self.company_id.country_id.id)]

    @api.depends('journal_id', 'partner_id', 'company_id', 'move_type')
    def _compute_l10n_latam_available_document_types(self):
        if self.env.company.country_id == self.env.ref('base.pe'):
            self._compute_l10n_latam_available_document_types_peru()
        else:
            super(AccountMove, self)._compute_l10n_latam_available_document_types()

    def _compute_l10n_latam_available_document_types_peru(self):
        self.l10n_latam_available_document_type_ids = False
        purchase_ids = self.filtered(lambda x: x.journal_id and x.partner_id and x.move_type in ['in_invoice', 'in_refund'])

        for rec in purchase_ids:
            rec.l10n_latam_available_document_type_ids = self.env['l10n_latam.document.type'].search(rec._get_l10n_latam_documents_new_domain())

        for rec in self.filtered(lambda x: x.journal_id and x.l10n_latam_use_documents and x.partner_id):
            if rec not in purchase_ids:
                rec.l10n_latam_available_document_type_ids = self.env['l10n_latam.document.type'].search(rec._get_l10n_latam_documents_domain())
