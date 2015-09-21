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

{
    'name' : 'Web widget x2many 2d matix sample',
    'version': '1.0',
    'author': 'Probuse Consulting Service Pvt. Ltd.',
    'category' : 'Website',
    'website': 'https://www.probuse.com',
    'description': ''' 
    It will shows the product attributes in matrix form on sale order based on configured values.
    Configuration is available on sale order.
  ''',
    'depends':['sale', 'web_widget_x2many_2d_matrix', 'project', 'hr'],
    'data' : [
              'sale_view.xml'
              ],
    'installable':True,
    'auto_install':False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
