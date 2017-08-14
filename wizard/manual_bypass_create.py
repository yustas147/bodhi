# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _


class ManualBypassCreate(models.TransientModel):
    _name = 'mrp_wo_ed.manual.bypass.create'

    product_id = fields.Many2one('product.product', 'Produced Bypass Product')
    quantity = fields.Float(string='Quantity')
    mo_id = fields.Many2one(comodel_name='mrp.production', string='MO')
    

    @api.multi
    def apply(self):
        for wiz in self:
            location = self.env.ref('stock.stock_location_locations_virtual')
            dest_location = wiz.mo_id.location_dest_id
            st_move = self.env['stock.move'].create({'location_id':location.id,
                                           'location_dest_id': dest_location.id,
                                           'product_id': wiz.product_id.id,
                                           'product_uom': wiz.product_id.uom_id.id,
                                           'product_uom_qty': wiz.quantity,
                                           'name': wiz.mo_id.name,
                                           'origin': wiz.mo_id.name,
                                           'production_id': wiz.mo_id.id})
            st_move.action_done()
        #product = self.env['product.product'].get_inventory_product(self.inventory_type_id, self.strain_id)
        #return {
            #'name': _('Product Variants'),
            #'type': 'ir.actions.act_window',
            #'res_model': 'product.product',
            #'view_type': 'form',
            #'view_mode': 'form',
            #'res_id': product.id,
            #'target': 'current',
            #'view_id': self.env.ref('product.product_variant_easy_edit_view').id,
        #}