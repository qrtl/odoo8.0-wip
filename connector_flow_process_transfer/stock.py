# -*- coding: utf-8 -*-
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


from openerp.osv import fields, osv, expression
from openerp import models, api
from openerp.addons.connector_flow.task.abstract_task \
    import AbstractChunkReadTask


class stock_move(osv.osv):
    _inherit = 'stock.move'

    def get_move_data(self, cr, uid, picking, context=None):
        res = []
        picking_id = self.pool.get('stock.picking').search(cr, uid, [('name','=',picking)], context=context)[0]
        move_ids = self.search(cr, uid, [('picking_id','=',picking_id)], context=context)
        if move_ids:
            res = move_ids
        return res


class ReceiptImport(AbstractChunkReadTask):
    def read_chunk(self, config=None, chunk_data=None, async=True):
        picking = chunk_data.get('Name')
        StockMove = self.session.env['stock.move']
        move_ids = StockMove.get_move_data(picking)
        StockMove.browse(move_ids).action_done()


class ReceiptImportTask(models.Model):
    _inherit = 'impexp.task'

    @api.model
    def _get_available_tasks(self):
        return super(ReceiptImportTask, self)._get_available_tasks() \
            + [('receipt_import', 'Receipt Import')]

    def receipt_import_class(self):
        return ReceiptImport
