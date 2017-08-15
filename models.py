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
            
    display_name = fields.Char(string="DPT", compute='_compute_display_name')
            
        
    #purchase manager 
    #4.
    service = fields.Selection([('split', 'Split'), ('purchase', 'Purchase'), ('process', 'Process')], 'Service')
    #2. Expected Delivery Date and Time
    exp_delivery_datetime = fields.Datetime(string="Expected Delivery Date and Time")
    #5. Product request
    prod_request = fields.Selection(selection=[('shatter','Shatter'),('crumble','Crumble')], string="Product request")
    #5a Send fill google form
    if_google_form_fill_sent = fields.Boolean(string="Send and Fill Out Google Form")
    if_processing_aggr = fields.Boolean(string="Signed Processing Agreement")
    #26.
    manif_datetime = fields.Datetime(string="Manifest Date and Time")
    manif_veh = fields.Char(string="Manifest Vehicle")
    #27.
    total_owed_cc = fields.Float(string="Total Owed to Conscious Cannabis")
    total_owed_bv = fields.Float(string="Total Owed to Bodhi Ventures")    
    
    # t b c in warehouse when material arrives
    #6.
    delivery_date = fields.Date(string="Delivery Date")
    #7.
    qty_in_grams = fields.Float(string="Quantity delivered in grams")
    #8.
    tot_transfer_amount = fields.Float(string="Total transfer amount")
    #8.2
    tot_paid_for_purchase_material = fields.Float(string="Total paid for purchased material")
    #9.
    est_num_runs = fields.Float(string="Estimated number of runs")
    if_pur_invoice_and_file_with_beth_received = fields.Boolean(string="Receive Purchase Invoice and File With Beth")
    if_signed_all_manif_inv_and_transf_money = fields.Boolean(string="Sign All Manifest/Invoices and Transfer Money")
    
    
    # t b c in lab 
    #10.
    cust_yield = fields.Float(string="Customer Yield")
    #11.
    cons_cannabis_yield = fields.Float(string="Conscious Cannabis Yield")
    #.12
    num_of_tests = fields.Integer(string="Number of Tests")
    #.13
    num_of_bh_tests = fields.Integer(string="Number of Tests")
    
    #.13
    xr_yield = fields.Float(string="XR Yield")
    #.14
    xr_num_of_tests = fields.Float(string="XR Number of Tests")
    
    # t b c  IN LAB FOR XR BACKEND
    #15.
    bh_material_packaged = fields.Float(string="Bodhi High Material Packaged")
    #16.
    ht_material_packaged = fields.Float(string="Honey Tree Material Packaged")
    #17.
    gl_material_packaged = fields.Float(string="Globs Material Packaged")
    #18.
    dist_run = fields.Float(string="Distilate Ran")
    #19.
    tot_yield_percent = fields.Float(string="Total Yield Percent")
    tot_tests_backend = fields.Float(string="Total Tests on Back End")
    
    # t b c
    #20.
    testing_ratio = fields.Float(string="Testing Ratio")
    #21.
    cost_encurred_for_testing = fields.Float(string="Cost  Encurred For Testing")
    #22.
    total_investment = fields.Float(string="Total Investment")
    #23.
    total_grams_yield = fields.Float(string="Total Grams Yield")
    #25.
    val_per_gram = fields.Float(string="Value Per Gram")
    
   # #########################################
    name = fields.Char(string='Name')
    client_id = fields.Many2one('res.partner', 'Client')
    sale_order_id = fields.Many2one('sale.order', 'Initial Sale Order')
    run_ids = fields.One2many(comodel_name='bodhi.run', inverse_name='dpt_id', 
                             string='Bodhi Runs')
    
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
            
    name = fields.Char(string="Name")
    display_name = fields.Char(compute='_get_display_name')
    dpt_id = fields.Many2one(comodel_name="bodhi.dpt", string="DPT order")
    client_id = fields.Many2one(comodel_name='res.partner', related='dpt_id.client_id', string=None)
    runs_together_added = fields.Many2many(comodel_name="bodhi.run", relation="bodhi_run_together", column1="runs_together_added", column2="runs_together_main", string="Runs added")
    runs_together_main = fields.Many2many(comodel_name="bodhi.run", relation="bodhi_run_together", column1="runs_together_main", column2="runs_together_added", string="added to Run")

    #TO BE COMPLETED IN WAREHOUSE
        #Section A
    c_date = fields.Date(string="Date")
    #service (already)
    strain = fields.Char(string="Strain")    

    original_flower_lot_ids = fields.Many2many(comodel_name='sce.inventory', string="Original Flower Lots")
#    original_flower_lot_id = fields.Many2one(comodel_name='sce.inventory', string="Original Flower Lot")
    g_per_run = fields.Float(string="#g Per Run")
    #TO BE COMPLETED IN EXTRACTION FOR FIRST RUN
        #Section B
    run_number = fields.Char(string='Run #')
    run_date = fields.Date(string='Run Date')
    machine_num = fields.Char(string='Machine #')
    pre_purge_weight = fields.Float(string='Pre Purge Weight')

    #TO BE COMPLETED IN POST PROCESSING Section D
    runs_put_together = fields.Char(string="Runs Put Together")
    hydro_carbon_num = fields.Char(string="Hydro Carbon # barcode")
    total_weight = fields.Float(string="Total Weight")
    consistancy = fields.Char(string="Consistancy")
    test_date = fields.Date(string="Test Date")
    customer_weight = fields.Float(string="Customer Weight")
    bodhi_weight = fields.Float(string="Bodhi Weight")
    new_bodhi_lot_num = fields.Char(string="New Bodhi Lot #")

    #TO BE COMPLETED IN POST PROCESSING Section E
    tot_thc = fields.Float(string="Total THC")
    tot_cbd = fields.Float(string="Total CBD")
    tot_canna = fields.Float(string="Total Canna.")
    terpenes = fields.Float(string="Terpenes")
    pass_fail = fields.Selection(string="Pass/Fail", selection=[('pass','Pass'),('fail','Fail')])
    grade = fields.Selection(string="Grade", selection=[('bh','Bodhi High'),('ht','Honey Tree'), ('gl','Glob')])
    type_of_package = fields.Selection(string="Type of Package", selection=[('box','Box'),('pl','Palette')])    


