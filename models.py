# -*- coding: utf-8 -*-
from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class bodhi_dpt(models.Model):
    _name = 'bodhi.dpt'
    
    
    
    @api.multi
    @api.depends('client_id','service','prod_request')
    def name_get(self):
        res = []
        for inst in self:
            #res = super(bodhi_dpt, obj=inst).name_get()
            nm = " ".join(filter(None, [inst.service, inst.prod_request, 'by', inst.client_id.name]))
            _logger.info('nm is: %s' % (unicode(nm)))
            res.append((inst.id, nm))
        return res
            
    
    @api.multi
    @api.depends('client_id', 'service', 'qty_in_grams')
    def _compute_display_name(self):
        for inst in self:
            nlist = [inst.service, inst.prod_request, 'BY', inst.client_id.name]
            inst.display_name = " ".join(filter(None, nlist))
            
    @api.onchange('sale_order_id', 'purchase_order_id')
    def _set_client_id(self):
        if self.sale_order_id:
            self.client_id = self.sale_order_id.partner_id
        if self.purchase_order_id:
            self.client_id = self.purchase_order_id.partner_id
        
            
    display_name = fields.Char(string="DPT", compute='_compute_display_name')
            
    state = fields.Selection([
                              ('draft', 'Draft'),
                              ('pur_man_1', 'Purchase Manager 1'),
                              ('wh_arrive', 'WH Material Arrive'),
                              ('lab_1', 'Lab 1'),
                              ('lab_2', 'Lab 2'),
                              ('lab_for_xr_backend', 'Lab XR Backend'),
                              ('pur_man_2', '...TBC...'),
                              ('pur_man_3', 'Purchase Manager 2'),
                              ('done', 'Done'),
                              ], string='State', default='draft')
    #purchase manager 
    #4.
    service = fields.Selection([('split', 'Split'), ('purchase', 'Purchase'), ('process', 'Process')], 'Service')
    #2. Expected Delivery Date and Time
    exp_delivery_datetime = fields.Datetime(string="Expected Delivery Date and Time", groups='bodhi.pur_man')
    #5. Product request
    prod_request = fields.Selection(selection=[('shatter','Shatter'),('crumble','Crumble')], string="Product request")
#    prod_request = fields.Selection(selection=[('shatter','Shatter'),('crumble','Crumble')], string="Product request", groups='bodhi.pur_man')
    #5a Send fill google form
    if_google_form_fill_sent = fields.Boolean(string="Send and Fill Out Google Form", groups='bodhi.pur_man')
    if_processing_aggr = fields.Boolean(string="Signed Processing Agreement", groups='bodhi.pur_man')
    #26.
    manif_datetime = fields.Datetime(string="Manifest Date and Time", groups='bodhi.pur_man')
    manif_veh = fields.Char(string="Manifest Vehicle", groups='bodhi.pur_man')
    #27.
    total_owed_cc = fields.Float(string="Total Owed to Conscious Cannabis", groups='bodhi.pur_man')
    total_owed_bv = fields.Float(string="Total Owed to Bodhi Ventures", groups='bodhi.pur_man')    
    
    # t b c in warehouse when material arrives
    #6.
    delivery_date = fields.Date(string="Delivery Date", groups='bodhi.wh')
    #7.
    qty_in_grams = fields.Float(string="Quantity delivered in grams", groups='bodhi.wh')
    #8.
    tot_transfer_amount = fields.Float(string="Total transfer amount", groups='bodhi.wh')
    #8.2
    tot_paid_for_purchase_material = fields.Float(string="Total paid for purchased material", groups='bodhi.wh')
    #9.
    est_num_runs = fields.Float(string="Estimated number of runs", groups='bodhi.wh')
    if_pur_invoice_and_file_with_beth_received = fields.Boolean(string="Receive Purchase Invoice and File With Beth", groups='bodhi.wh')
    if_signed_all_manif_inv_and_transf_money = fields.Boolean(string="Sign All Manifest/Invoices and Transfer Money", groups='bodhi.wh')
    
    
    # t b c in lab 
    #10.
    cust_yield = fields.Float(string="Customer Yield", groups='bodhi.lab')
    #11.
    cons_cannabis_yield = fields.Float(string="Conscious Cannabis Yield", groups='bodhi.lab')
    #.12
    num_of_tests = fields.Integer(string="Number of Tests", groups='bodhi.lab')
    #.13
    num_of_bh_tests = fields.Integer(string="Number of Tests", groups='bodhi.lab')
    
    #.13
    xr_yield = fields.Float(string="XR Yield", groups='bodhi.lab')
    #.14
    xr_num_of_tests = fields.Float(string="XR Number of Tests", groups='bodhi.lab')
    
    # t b c  IN LAB FOR XR BACKEND
    #15.
    bh_material_packaged = fields.Float(string="Bodhi High Material Packaged", groups='bodhi.lab')
    #16.
    ht_material_packaged = fields.Float(string="Honey Tree Material Packaged", groups='bodhi.lab')
    #17.
    gl_material_packaged = fields.Float(string="Globs Material Packaged", groups='bodhi.lab')
    #18.
    dist_run = fields.Float(string="Distilate Ran", groups='bodhi.lab')
    #19.
    tot_yield_percent = fields.Float(string="Total Yield Percent", groups='bodhi.lab')
    tot_tests_backend = fields.Float(string="Total Tests on Back End", groups='bodhi.lab')
    
    # t b c
    #20.
    testing_ratio = fields.Float(string="Testing Ratio", groups='bodhi.pur_man')
    #21.
    cost_encurred_for_testing = fields.Float(string="Cost  Encurred For Testing", groups='bodhi.pur_man')
    #22.
    total_investment = fields.Float(string="Total Investment", groups='bodhi.pur_man')
    #23.
    total_grams_yield = fields.Float(string="Total Grams Yield", groups='bodhi.pur_man')
    #25.
    val_per_gram = fields.Float(string="Value Per Gram", groups='bodhi.pur_man')
    
   # #########################################
    name = fields.Char(string='Name')
    client_id = fields.Many2one('res.partner', 'Client')
    sale_order_id = fields.Many2one('sale.order', 'Initial Sale Order', groups='bodhi.pur_man')
    purchase_order_id = fields.Many2one('purchase.order', 'Initial Purchase Order', groups='bodhi.pur_man')
    run_ids = fields.One2many(comodel_name='bodhi.run', inverse_name='dpt_id', 
                             string='Bodhi Runs')
    mo_ids = fields.One2many(comodel_name='mrp.production', inverse_name='bodhi_dpt_id', 
                             string='Manufacturing Orders')
    
class bodhi_run(models.Model):
    _name = 'bodhi.run'    
    
    #@api.multi
    #@api.depends('run_number')
    #def name_get(self):
        #res = []
        #for inst in self:
            #res.append((inst.id, inst.run_number))
            #_logger.info("runned on %s" % (unicode(inst)))
            #res.append((inst.id, unicode(inst.run_number)))
        #return res
            
    @api.multi
    @api.depends('run_number')
    def name_get(self):
        res = []
        for inst in self:
           # if not inst.name:
                res.append((inst.id, inst.run_number))
                _logger.info("runned on %s" % (unicode(inst)))
        return res    
    
    @api.multi
    @api.depends('run_number')
    def _get_display_name(self):
        for inst in self:
            inst.display_name = unicode(inst.run_number)
    
    state = fields.Selection([('draft', 'Draft'),
                              ('wh_sec_A', 'WH Sec. A'),
                              ('extr_1', 'First Extraction Sec. B'),
                              ('pp_1', 'Post Processing Sec. D'),
                              ('pp_2', 'Post Processing Sec. E'),
                              ('done', 'Done'),
                              ], string = 'State', default='draft')    
    
    name = fields.Char(string="Name")
    display_name = fields.Char(compute='_get_display_name')
    dpt_id = fields.Many2one(comodel_name="bodhi.dpt", string="DPT order")
    client_id = fields.Many2one(comodel_name='res.partner', related='dpt_id.client_id', string=None)
    runs_together_added = fields.Many2many(comodel_name="bodhi.run", relation="bodhi_run_together", column1="runs_together_added", column2="runs_together_main", string="Runs added")
    runs_together_main = fields.Many2many(comodel_name="bodhi.run", relation="bodhi_run_together", column1="runs_together_main", column2="runs_together_added", string="added to Run")

    #TO BE COMPLETED IN WAREHOUSE
        #Section A
    c_date = fields.Date(string="Date", groups='bodhi.wh')
    #service (already)
    strain = fields.Char(string="Strain")    

    original_flower_lot_ids = fields.Char(string="Original Flower Lots", groups='bodhi.wh')
#    original_flower_lot_ids = fields.Many2many(comodel_name='sce.inventory', string="Original Flower Lots", groups='bodhi.wh')
    g_per_run = fields.Float(string="#g Per Run", groups='bodhi.wh')
    #TO BE COMPLETED IN EXTRACTION FOR FIRST RUN
        #Section B
    run_number = fields.Char(string='Run #')
#    run_number = fields.Char(string='Run #', groups='bodhi.extr')
    run_date = fields.Date(string='Run Date', groups='bodhi.extr')
    machine_num = fields.Char(string='Machine #', groups='bodhi.extr')
    pre_purge_weight = fields.Float(string='Pre Purge Weight', groups='bodhi.extr')

    #TO BE COMPLETED IN POST PROCESSING Section D
    runs_put_together = fields.Char(string="Runs Put Together", groups='bodhi.pp')
    hydro_carbon_num = fields.Char(string="Hydro Carbon # barcode", groups='bodhi.pp')
    total_weight = fields.Float(string="Total Weight", groups='bodhi.pp')
    consistancy = fields.Char(string="Consistancy", groups='bodhi.pp')
    test_date = fields.Date(string="Test Date", groups='bodhi.pp')
    customer_weight = fields.Float(string="Customer Weight", groups='bodhi.pp')
    bodhi_weight = fields.Float(string="Bodhi Weight", groups='bodhi.pp')
    new_bodhi_lot_num = fields.Char(string="New Bodhi Lot #", groups='bodhi.pp')

    #TO BE COMPLETED IN POST PROCESSING Section E
    tot_thc = fields.Float(string="Total THC", groups='bodhi.pp')
    tot_cbd = fields.Float(string="Total CBD", groups='bodhi.pp')
    tot_canna = fields.Float(string="Total Canna.", groups='bodhi.pp')
    terpenes = fields.Float(string="Terpenes", groups='bodhi.pp')
    pass_fail = fields.Selection(string="Pass/Fail", selection=[('pass','Pass'),('fail','Fail')], groups='bodhi.pp')
    grade = fields.Selection(string="Grade", selection=[('bh','Bodhi High'),('ht','Honey Tree'), ('gl','Glob')], groups='bodhi.pp')
    type_of_package = fields.Selection(string="Type of Package", selection=[('box','Box'),('pl','Palette')], groups='bodhi.pp')    



class SaleOrder(models.Model):
    _inherit = "sale.order"        
    
    @api.multi
    def bodhi_start(self):
        self.ensure_one()
        if not self.bodhi_dpt_id:
            self.bodhi_dpt_id = self.env['bodhi.dpt'].create({
                'sale_order_id':self.id,
                'client_id':self.partner_id.id,
            })
        return  {
            'name':"Created Bodhi Process",
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'bodhi.dpt',
            'res_id': self.bodhi_dpt_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'self',
            'domain': '[]',
        }            
             
                    
    bodhi_dpt_id = fields.Many2one(comodel_name="bodhi.dpt", string="Bodhi Process")        

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"        

    @api.multi
    def bodhi_start(self):
        self.ensure_one()
        if not self.bodhi_dpt_id:
            self.bodhi_dpt_id = self.env['bodhi.dpt'].create({
                    'purchase_order_id':self.id,
                    'client_id':self.partner_id.id,
                })
        return  {
            'name':"Created Bodhi Process",
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'bodhi.dpt',
            'res_id': self.bodhi_dpt_id.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'self',
            'domain': '[]',
            #'context': context
        }            

    bodhi_dpt_id = fields.Many2one(comodel_name="bodhi.dpt", string="Bodhi Process")            
    
class mrpProduction(models.Model):
    _inherit = "mrp.production"        

    bodhi_dpt_id = fields.Many2one(comodel_name="bodhi.dpt", string="Bodhi Process")          
    
class Inventory(models.Model):
    _inherit = "sce.inventory"      
    
    is_sorted = fields.Boolean(string="Is Sorted")
    slab_label_ids = fields.One2many(comodel_name='bodhi.slab_label', inverse_name='inventory_id', 
                                    string='Slab Label')
    grade = fields.Selection(selection=[('bh','BodhiHigh'),('ht','HoneyTree'),('gl','Glob')], string='Grade')
    stars = fields.Selection(selection=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], string='Stars')

    
class SlabLabel(models.Model):
    _name = 'bodhi.slab_label'
    
    inventory_id = fields.Many2one(comodel_name='sce.inventory', string='Sce Inventory')
    strain = fields.Many2one(comodel_name='sce.strain', related='inventory_id.strain_id', string='Strain')
    run_id = fields.Many2one(comodel_name='bodhi.run', string='Run')
    run_number = fields.Char(related='run_id.run_number', string='Run #')
    prepurge_weight = fields.Float(string='PrePurge Weight')
    actual_weight = fields.Float(string='PrePurge Weight')
    #grade = fields.Selection(string='Grade', related='inventory_id.grade') 
    client = fields.Many2one(comodel_name='res.partner', related='run_id.client_id')
    split = fields.Boolean(string='If Split')
    weight_after_split = fields.Float(string='After Split Weight')
    number_of_containers = fields.Integer(string='ContNum', help='How many containers included in lot')
    container_number = fields.Integer(string='Container #')
    
    
    
    
    