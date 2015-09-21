#########################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY OpenERP SA (<http://www.odoo.com>)
#    Copyright (C) 2014-TODAY Probuse Consulting Service Pvt. Ltd. (<http://probuse.com>).
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
#
#########################################################################################
from openerp.osv import osv, fields
from openerp.tools.translate import _


class sale_order_line_widget(osv.osv):
    _name = 'sale.order.line.widget'
    
    _columns = {
        'employee_id' : fields.many2one('hr.employee', 'Employee'),
        'project_id' : fields.many2one('project.project', 'Project'),
        'value2' : fields.float('Value'),
        'sale_id': fields.many2one('sale.order', 'Order')
    }
    
class sale_product_widget(osv.osv):
    _name = 'sale.product.widget'
    
    _columns = {
        'sale_order_id': fields.many2one('sale.order', 'Order'),
        'product_id' : fields.many2one('product.product', 'product'),
        'attribute_id': fields.many2one('product.attribute', 'Attribute'),
        'product_attr_id': fields.many2one('product.attribute.value', 'Product Attribute Value'),
        'product_attr1_id': fields.many2one('product.attribute.value', 'Product Attribute Value2'),
        'value2' : fields.float('Value'),
    }
    
class sale_order(osv.osv):
    _inherit = 'sale.order'
    
    _columns = {
        'sale_widget_ids': fields.one2many('sale.order.line.widget', 'sale_id', 'Sale Order Widget'),
        'sale_product_widget_ids': fields.one2many('sale.product.widget', 'sale_order_id', 'Sale Order Widget'),
        'template_id' : fields.many2one('product.template', 'Product'),
        'attribute_id': fields.many2one('product.attribute', 'Attribute'),
        'attribute_id1': fields.many2one('product.attribute', 'Attribute1'),
    }
    
    def onchange_product_template(self, cr, uid, ids, template_id, context=None):
        res = {}
        template_data = self.pool.get('product.template').browse(cr, uid, template_id, context=context)
        attribute_ids_list = []
        
        #if not template_data.attribute_line_ids:
        #    raise osv.except_osv(_('Warning!'), _('Please configure attributes of Product.'))
        for attr in template_data.attribute_line_ids:
            attribute_ids_list.append(attr.id)
        res.update({'domain':{ 'attribute_id':[('id', 'in', attribute_ids_list)],'attribute_id1':[('id' ,'in', attribute_ids_list)]}})
        return res
    
    
    def product_widget(self, cr, uid, ids, context=None):
        sale_data = self.browse(cr, uid, ids, context=context)[0]
        
        #if not sale_data.template_id or not sale_data.attribute_id or not sale_data.attribute_id1:
        #    raise osv.except_osv(_('Warning!'), _('Please configure template and attributes.'))
        
        product = sale_data.template_id.id
        attribute_1 = sale_data.attribute_id.id
        attribute_2 = sale_data.attribute_id1.id
        
        template_data = self.pool.get('product.template').browse(cr, uid, product, context=context)
        
        value_list = []

        if template_data.attribute_line_ids:
            for attr in template_data.attribute_line_ids:
                if attr.id == attribute_1 or attr.id == attribute_2:
                    for value in attr.value_ids:
                        value_list.append(value.id)
                    
        attribute_1_list = self.pool.get('product.attribute.value').search(cr, uid, [('attribute_id','=', attribute_1), ('id', 'in', value_list)])
        attribute_2_list = self.pool.get('product.attribute.value').search(cr, uid, [('attribute_id','=', attribute_2), ('id', 'in', value_list)])

        attribute_widget_list = []
        
        for attr_1 in attribute_1_list:
            for attr_2 in attribute_2_list:
                attribute_widget_list.append((0, 0, {'product_attr1_id': attr_2,'product_attr_id':attr_1, 'value2': 0.0}))
        self.write(cr, uid, ids, {'sale_product_widget_ids': attribute_widget_list})
        return
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        res= super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context=context)
        project_ids = self.pool.get('project.project').search(cr, uid, [('partner_id', '=', part)], context=context)
        employee_ids = self.pool.get('hr.employee').search(cr, uid, [], context=context)
        res['value'].update({'sale_widget_ids' : []})
        for project in project_ids:
            for emp in employee_ids:
                res['value']['sale_widget_ids'].append({'employee_id': emp,'project_id':project, 'value2': 0.0})
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: