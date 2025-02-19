# import time
# from odoo import models, fields,api,_,os
# from odoo.exceptions import ValidationError, UserError
# import ast
# import random
# import requests
# import base64
# import time
# import time
# import logging
# _logger = logging.getLogger(__name__)


# class o2bProcessLock(models.Model):
#     _name = 'o2b.process.lock'
#     _description = 'O2b Process modular lock data'

#     record_id = fields.Char(string='Record ID')
#     model = fields.Char(string='Model')
#     active = fields.Boolean(string = 'Active',default =True)
#     user_id = fields.Char(string='user ID')
#     lock_date = fields.Datetime(string='Record Lock Date', default=fields.Datetime.now)
#     release_date= fields.Datetime(string='Release Date', default=fields.Datetime.now)


# class o2bProcessEmail(models.Model):
#     _name = 'o2b.process.email'
#     _description = 'O2b Process email'

#     record_id = fields.Char()
#     model = fields.Char()
#     current_id = fields.Char(string="Current ID")
#     next_id = fields.Char(string = 'Next Id')
#     recipient = fields.Char(string='Email to')
#     mail_subject = fields.Char(string='Mail Subject')
#     mail_body = fields.Char(string=' Body')
#     create_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)
#     mail_send_date = fields.Datetime(string='Send Date', default=fields.Datetime.now)
#     attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
#     mail_count = fields.Char(string = 'Mail limit')
#     is_active = fields.Boolean(string = 'Status', default =True)
#     is_sent = fields.Boolean(string = 'Mail sent'  , default = False)
#     mail_trigger = fields.Char(string = 'Mail trigger')
#     active = fields.Boolean(string = 'Active',default =True)


# class o2bProcessManagerTable(models.Model):
#     _name = 'o2b.process.manager'
#     _description = 'O2b Process Modular'

#     record_id = fields.Char(string='Record ID')
#     model = fields.Char(string='Model')
#     model_stage = fields.Char(string='Model Stage')
#     prev_id = fields.Char(string='Previous ID')
#     pre_name = fields.Char(string='Previous Name')
#     pre_type = fields.Char(string='Previous Type')
#     current_id = fields.Char(string='Current ID')
#     current_name = fields.Char(string='Current Name')
#     current_type = fields.Char(string='Current Type')
#     next_id = fields.Char(string='Next ID')
#     next_name = fields.Char(string='Next Name')
#     next_type = fields.Char(string='Next Type')
#     record_lock = fields.Boolean(string='Record Lock', default=False)
#     active = fields.Boolean(string = 'Active',default =True)

   

# class o2bProcessModularEmail(models.Model):
#     _name = 'o2b.process.modular.email'
#     _description = 'O2b Process Modular email'

#     process_id = fields.Char()
#     process_name = fields.Char()
#     model_name = fields.Char()
#     process_email_line = fields.Many2one('o2b.process.modular', string='O2b Proces Email', ondelete='cascade',invisible=1)
#     prev_step = fields.Char(string="Previous step")
#     next_step = fields.Char(string = 'Next step')
#     next_step_id = fields.Char(string = 'Next Id')
#     current_step = fields.Char(string='current step')
#     current_node_id = fields.Char(string='Current Id')
#     recipient = fields.Char(string='Email to')
#     mail_subject = fields.Char(string='Mail Subject')
#     mail_body = fields.Char(string=' Body')
#     template_id = fields.Char(string='Template Id')
#     mail_trigger = fields.Char(string='Mail trigger')
#     mail_limit = fields.Char(string='Mail limit')


# class o2bProcessModularFieldMethod(models.Model):
#     _name = 'o2b.process.modular.field.method'
#     _description = 'O2b Process Modular Field method'

#     process_id = fields.Char()
#     process_name = fields.Char()
#     model_name = fields.Char()
#     field_name = fields.Char()
#     field_label = fields.Char()
#     field_id = fields.Char()
#     field_type = fields.Char()
#     field_method = fields.Char()
#     is_required = fields.Boolean(string = 'Required', default=False)
#     activity_name = fields.Char()
#     activity_type = fields.Char()
#     form_id = fields.Char(string = 'Form Id')
#     process_field_line = fields.Many2one('o2b.process.modular', string ='Process Fields', ondelete='cascade',invisible=1)
#     default_value = fields.Char(string = 'Default Value')

# class o2bProcessModularView(models.Model):
#     _name = 'o2b.process.modular.view'
#     _description = 'O2b Process Modular view '

#     process_id = fields.Char()
#     process_name = fields.Char()
#     model_name = fields.Char()
#     activity_name = fields.Char()
#     view_id = fields.Char(string ='View Id')
#     view_name = fields.Char(string ='Name')
#     view_type = fields.Char(string = 'Type')
#     view_data = fields.Char(string ='Data')
#     activity_type = fields.Char(string = 'Type')
#     node_id = fields.Char(string = 'Node Id')
#     process_views = fields.Many2one('o2b.process.modular', string='O2b Process group', ondelete='cascade',invisible=1)

# class o2bProcessModularAction(models.Model):
#     _name = 'o2b.process.modular.action'
#     _description = 'O2b Process Modular Actions'

#     process_id = fields.Char()
#     process_name = fields.Char()
#     model_name = fields.Char()
#     activity_name = fields.Char()
#     action_id = fields.Char(string ='Action Id')
#     action_name = fields.Char(string ='Name')
#     domain = fields.Char(string ='Domain')
#     activity_type = fields.Char(string = 'Type')
#     context = fields.Char(string = 'Context')
#     node_id = fields.Char(string = 'Node Id')
#     process_actions = fields.Many2one('o2b.process.modular', string='O2b Process group', ondelete='cascade',invisible=1)



# class o2bProcessModularMenuGroup(models.Model):
#     _name = 'o2b.process.modular.group'
#     _description = 'O2b Process Modular group '

#     process_id = fields.Char()
#     process_name = fields.Char()
#     model_name = fields.Char()
#     activity_name = fields.Char()
#     group = fields.Char(string ='Group')
#     process_groups = fields.Many2one('o2b.process.modular', string='O2b Process group', ondelete='cascade',invisible=1)
#     activity_type = fields.Char()
#     node_id = fields.Char(string = 'Node Id')
#     action_id = fields.Char(string = 'Action Id')
#     menu_id = fields.Char(string ='Menu Id')
#     parent_id = fields.Char(string ='Parrent Id')
#     # status = fields.Boolean(string = 'Active Status' , default=False)
#     # prev_menu_name = fields.Char(string = 'Prev Name')
#     # curr_menu_name = fields.Char(string = 'Curr Name')
#     # prev_menu_id = fields.Char(string = 'Pre Menu id')
#     # count = fields.Integer(string = 'Count', default=0)

# class o2bProcessModularMenu(models.Model):
#     _name = 'o2b.process.modular.menu'
#     _description = 'O2b Process Modular Menu '

#     process_id = fields.Char()
#     process_name = fields.Char()
#     model_name = fields.Char()
#     menu_name = fields.Char()
#     menu_id = fields.Char(string ='Menu Id')
#     parent_id = fields.Char(string ='Parrent Id')
#     node_id = fields.Char(string = 'Node Id')
#     action_id = fields.Char(string = 'Action Id')
#     activity_type = fields.Char()
#     menu_type = fields.Char(string = 'Menu')
#     status = fields.Boolean(string = 'Active Status' , default=True)
#     pre_menu_id = fields.Char(string = 'Prev id')
#     pre_parent_menu_id = fields.Char(string = 'Pre Parrent id')
#     count = fields.Integer(string = 'Count', default=0)
#     process_menus = fields.Many2one('o2b.process.modular', string='O2b Process menu', ondelete='cascade',invisible=1)


# class o2bProcessModularRemarkHistory(models.Model):
#     _name = 'o2b.process.modular.remark.history'
#     _description = 'O2b Process Modular Remark History'

#     serial_id = fields.Char(string ="Serial No")
#     remark = fields.Char(string = 'Remarks')
#     decision = fields.Char(string='Decision')
#     current_stage = fields.Char(string='Current Stage')
    
  
# class o2bProcessModularStatusBar(models.Model):
#     _name = 'o2b.process.modular.statusbar'
#     _description = 'O2b Process Modular Stage Statusbar'

#     process_id = fields.Char()
#     process_name = fields.Char()
#     model_name = fields.Char()
#     process_stage_line = fields.Many2one('o2b.process.modular', string='Process Status Bar', ondelete='cascade',invisible=1)
#     # process_stage_name = fields.Char(string = 'Stage Name')
#     process_node_id= fields.Char(string = 'Process Node Id')
#     stage_name = fields.Char(string = 'Stage Name')
#     stage_value = fields.Char(string = 'Stage Value')
#     node_type = fields.Char(string = 'Stage Type')
  
# class o2bProcessModularStageDecesion(models.Model):
#     _name = 'o2b.process.modular.stage.decision'
#     _description = 'O2b Process Modular stages decision'
#     process_id = fields.Char()
#     process_name = fields.Char()
#     process_decision_line = fields.Many2one('o2b.process.modular', string='O2b Proces decision', ondelete='cascade',invisible=1)
#     o2b_sequence = fields.Char()
#     o2b_operand = fields.Char()
#     o2b_operator = fields.Char()
#     o2b_value= fields.Char()
#     previous_stage = fields.Char()
#     next_stage = fields.Char()
#     next_stage_id = fields.Char()
#     domain = fields.Char(string='Domain')
#     decision_name = fields.Char(string='Decision State')
#     exception_state = fields.Char(string='Exception State')
#     odoo_domain = fields.Char(string=' Parse Domain')


# # modal class for process store process stages
# class o2bProcessModularStage(models.Model):
#     _name = 'o2b.process.modular.stage'
#     _description = 'O2b Process Modular stages'
#     process_id = fields.Char()
#     activity_name = fields.Char()
#     model_name = fields.Char()
#     previous_stage = fields.Char()
#     previous_stage_id = fields.Char()
#     current_stage = fields.Char()
#     current_stage_id = fields.Char()
#     next_stage = fields.Char()
#     next_stage_id = fields.Char()
#     process_name = fields.Char()
#     python_code = fields.Text(string='Python Code', default=False)
#     process_stages = fields.Many2one('o2b.process.modular', string='O2b Process', ondelete='cascade',invisible=1)
#     activity_type = fields.Char()


# class o2bProcessModular(models.Model):
#     _name = 'o2b.process.modular'
#     _description = 'O2b Process Modular'
#     _rec_name = 'process_name'

#     #request field
#     current_user = fields.Many2one('res.users', string='Current User', default=lambda self: self.env.user.id)
#     process_id = fields.Char()
#     model_detail = fields.Char()
#     model_name = fields.Char()
#     fields_data = fields.Char()
#     menu_data = fields.Char()
#     action_data = fields.Char()
#     access_right_data = fields.Char()
#     user_name = fields.Char()
#     user_request = fields.Char()
#     button_data = fields.Char()
#     registry_status = fields.Boolean('Registry Status', default=True)
#     #internal user field
#     activity_name = fields.Char()
#     previous_stage = fields.Char()
#     current_stage = fields.Char()
#     next_stage = fields.Char()
#     process_name = fields.Char()
#     process_stages_ids = fields.One2many('o2b.process.modular.stage', 'process_stages', string='Process Stage ID')
#     process_stages_decision_ids = fields.One2many('o2b.process.modular.stage.decision', 'process_decision_line', string='Process Decision ID')
#     process_stages_field_ids = fields.One2many('o2b.process.modular.field.method', 'process_field_line', string='Field ID',)
#     process_state_ids = fields.One2many('o2b.process.modular.statusbar', 'process_stage_line', string='Field ID')
#     process_group_ids = fields.One2many('o2b.process.modular.group', 'process_groups', string='Group Ids')
#     process_menu_ids = fields.One2many('o2b.process.modular.menu', 'process_menus', string='Group Ids')
#     process_view_ids = fields.One2many('o2b.process.modular.view', 'process_views', string='View Ids')
#     process_action_ids = fields.One2many('o2b.process.modular.action', 'process_actions', string='Action Ids')
#     process_email_ids = fields.One2many('o2b.process.modular.email', 'process_email_line', string='Email Ids')
#     basic_start_template = fields.Text(string='XML Content', default=''' ''')

    

#     @api.model
#     def lock_record(self, model, record_id,user_id,node_id):
#         _logger.info("** lock_record : model is:%s  and record id: %s", model,record_id)
#         _logger.info("** lock_record userid %s ", user_id)
#         if model:
#             model = model.strip()
#         if record_id:
#             print(" ** record lck type of reocrd id: ", type(record_id))
#             record_id = str(record_id)

#         lock_data_search = self.env['o2b.process.lock'].sudo().search(['&',('model','=',model.strip()),('record_id','=',record_id)],limit =1)
#         response = None
#         if lock_data_search and lock_data_search.user_id == str(user_id):
#             print(" ** current record lock is in your queue. after filling records please release this record via cliking done button",lock_data_search )
#             response = ['USER_QUEUE']
#             return response
#         elif lock_data_search and lock_data_search.user_id != str(user_id) and lock_data_search.user_id != False:
#             print(" show alert to this record is pending on other user id ::", lock_data_search.user_id)
#             user = self.env['res.users'].sudo().browse(int(lock_data_search.user_id))

#             response = ['OTHER_QUEUE',user.name]
#             return response
#         else:
#             process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',model.strip()),('current_stage_id','=',node_id)])
#             data = {
#                     'record_id'     : record_id ,
#                     'model'         : model,
#                     'user_id'       : str(user_id),
#                     # 'lock_date'     : ,
#                     # 'release_date'  : ,
#                     }
#             if process.next_stage_id:
#                 _logger.info(" ** writing new lock record")
#                 new_lock_record  = self.env['o2b.process.lock'].sudo().create(data)
#                 response = ['FINAL']
#                 return response
#         return response

#     @api.model
#     def lock_release(self, model, record_id,user_id):
#         _logger.info("** lock_release : model is:%s  and record id: %s", model,record_id)

#         if model:
#             model = model.strip()

#         if record_id:
#             record_id = str(record_id)

#         if user_id:
#             user_id = str(user_id)

#         release_record = self.env['o2b.process.lock'].sudo().search(['&',('model','=',model.strip()),('record_id','=',record_id),('user_id','=',user_id)],limit =1)
#         _logger.info(" ** releasing records %s ", str(release_record))
#         if release_record:
#             release_record.sudo().write({'active':False})
       

#     @api.model
#     def update_app_list(self,process_name):
#         count = 0
#         _logger.info("process name: %s", process_name)
#         module_name = 'o2b_' + process_name.replace(' ','_').lower()
#         result = self.env['base.module.update'].with_user(2).sudo().update_module()
#         print("calling update_module base method: ", result)

#         # calling method to upgrade button: 
#         current_module = self.env['ir.module.module'].sudo().search([('name','=',module_name)],limit=1)
#         current_module.with_user(2).sudo().button_immediate_install()
#         # current_module.with_user(1).sudo().button_immediate_upgrade()
#         result = self.env['base.module.update'].with_user(2).sudo().update_module()
#         print("current module module_name : ", module_name)
#         print("current module object : ", current_module)
        
#         model = 'o2b.' + process_name.replace(' ','_').lower()
#         current_model = self.env['ir.model'].sudo().search([('model','=',model)],limit=1)
#         if not current_model:
#             result = self.env['base.module.update'].with_user(2).sudo().update_module()
#             _logger.info("calling update_module base method: %s", result)
#             # calling method to upgrade button: 
#             current_module = self.env['ir.module.module'].sudo().search([('name','=',module_name)],limit=1)
#             current_module.with_user(2).sudo().button_immediate_install()
#             # current_module.with_user(1).sudo().button_immediate_upgrade()
#             result = self.env['base.module.update'].with_user(2).sudo().update_module()
           

#         # time.sleep(2)
#         # return json.dumps({'folder_code': '123', 'message': 'folder created successfully'}) ;


#     @api.model
#     def update_module_state(self):
#         _logger.info("We are in update stage moudle %s",self)
#         print("we are in update")
#         # print("we are in update",odoo.cli.server.prepare_environment())
#         # Get the database cursor
#         cr = self.env.cr
#         # Define the SQL query
#         sql_query = """
#         UPDATE ir_module_module
#         SET state='installed'
#         WHERE name LIKE 'o2b_%'
#         AND state='to upgrade';
#         """
#         # Execute the SQL query
#         cr.execute(sql_query)
#         # Optionally, commit the transaction
#         self.env.cr.commit()

#     @api.model
#     def action_test(self,model,record,records,decision_records,all_decision,current_decision):
#         _logger.info("decision records : %s",decision_records)
#         _logger.info("all_decision records : %s",len(all_decision))
#         print("***************action test *************** : ",current_decision)
#         print("model : ",model)
#         print("record : ",record)
#         print("records : ",records)
#         print("decision_records ",decision_records)
#         print("all_decision ",all_decision)
#         print("current_decision ",current_decision)

#         if not decision_records:
#             _logger.info("no record found to apply decision rule.")
#         else:
#             for rec in decision_records:
#                 record_current_stage = rec.x_o2b_stage
#                 _logger.info("record found and current stage is :%s  ", record_current_stage)
#                 self.sudo().schedular_decision_maker(rec,model,model._name,all_decision,current_decision)

#     def schedular_decision_maker(self,record,model,model_name,all_decision,current_decision):
#         _logger.info("********************schedular_decision_maker: ********************** %s  and current record decision %s", record,  current_decision)
#         _logger.info("Model name : %s ", model)
#         # print("model name ", model_name)
#         # print("type of modle name:", type(model_name))
#         process = self.env['o2b.process.modular'].sudo().search([('model_name','=',model_name.strip())])
#         print(" all desision ids ==============: ", process.process_stages_decision_ids)
#         print(" all desision stage  ==============: ", process.process_state_ids)
#         for reccc in process.process_stages_decision_ids:
#             _logger.info("reccc ::::::::: %s", reccc.decision_name)
#         # decision_line = process.process_stages_decision_ids if process.process_stages_decision_ids else None
#         decision_line = process.process_stages_decision_ids.filtered(lambda r: r.decision_name == current_decision)
#         print("fileter record decision lines: ", decision_line)
#         # decision_line = process.process_stages_decision_ids.filtered(lambda s: s.decision_name == current_decision) if process.process_stages_decision_ids else None
#         if decision_line and decision_line[0].decision_name == current_decision:
#             sequence = 0
#             _logger.info("yes decision line availabe%s ", decision_line)
#             for rec in decision_line:
#                 _logger.info("store data from decisin table  pre stage: %s", rec.previous_stage )
#                 _logger.info("decisin table  next stage: %s", rec.next_stage )
#                 # print("decisin table  domain: ", rec.domain )
#                 print("decisin table  parse domain: ", rec.odoo_domain )
#                 # print("decisin table  parse type odoo_domain : ", type(rec.odoo_domain))
#                 # print("decisin table  parse type domain : ", type(rec.domain))
#                 result = self.sudo().adnvace_rule_engine(rec,rec.domain,rec.odoo_domain,record,sequence,process.process_state_ids,model_name)
#                 sequence = sequence + 1
#                 _logger.info('result of decision rule engine:%s',result)
#                 if result[0] == True:
#                     _logger.info("first time stage changed...")
#                     return;
#             _logger.info("if not rule apply then stage change automatically to decesion exception stage: %s", record)
#             process_id = ''
#             process_name =''
#             decision_list = []
#             if all_decision:
#                 for data in all_decision:
#                     decision_list.append(data.current_stage)
#                     process_name = data.process_name
#                     process_id= data.process_id
#             print("data list : ::::", decision_list)

#             if record.x_o2b_stage in  decision_list:
#                 _logger.info("****** exception states ")
#                 process_decision = self.env['o2b.process.modular.stage.decision'].sudo().search([('process_name','=',process_name),('decision_name','=', record.x_o2b_stage)], limit=1)
#                 print("which decision excetion is executed with next step: name ", process_decision.exception_state)
#                 # print("which decision excetion is executed with next step: value", process_decision.exception_state.replace(' ','_').lower())
#                 print("current record: ", record)
#                 print("current record sh iv : ", process_decision.exception_state)
#                 print("current record sh iv : ", type(process_decision.exception_state))
#                 if process_decision.exception_state and process_decision.exception_state != 'null':
#                     print("**goiing in exception state: ")
#                     record.with_user(2).sudo().write({
#                     'x_o2b_stage': process_decision.exception_state.replace(' ','_').lower(),
#                     'x_done': True,
#                     })
#                 else:
#                     _logger.info("** exception state without exception stage defined.")
#                     # record.with_user(2).sudo().write({
#                     #     'x_o2b_stage': process_decision.previous_stage.replace(' ','_').lower(),
#                     #     'x_done': True,
#                     #     })
        
#     @api.model
#     def decision_action(self, model, record_id, fields,node_id,user_id):
#         _logger.info("done method called %s", model)
#         if model:
#             model = model.strip()
#         self.env[model].sudo().pre(self)
#         if record_id:
#             record_id = int(record_id)
#             current_record_model = self.env[model].sudo().browse(record_id)
#             current_stage = current_record_model.x_o2b_stage
#             _logger.info("*** decision action : %s  for model %s : ",current_stage,model)
#             # comment below line if end stage done button hide:
#             process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',model.strip()),('current_stage_id','=',node_id)])
#             if process.next_stage_id:
#                 current_record_model.sudo().write({
#                     'x_done': False,
#                     })

#             statusbar = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',model),('process_node_id','=',node_id)],limit=1)
#             base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
#             domain = ''
#             if statusbar:
#                 domain = '[("x_o2b_stage","=","'+ statusbar.stage_value + '"),("x_done","=",True)]'
#             print("domain: ", domain)
#             action_id = self.env['ir.actions.act_window'].sudo().search(
#             [('res_model', '=', model.strip()), ('domain', '=', domain)],
#             order='id desc',
#             limit=1
#             )
#             print("action_id :" , action_id)
#             redirect_url = ''
#             if action_id:
#                 redirect_url = '{}/web#action={}&model={}&view_type=list'.format(base_url, action_id.id, model)
#                 _logger.info(" decision node Record URL: %s", redirect_url)
#             msg = ""
#             response = ['normal', redirect_url,msg]
#             self.env[model].sudo().post(self)
#             self.process_manager_crud(model, record_id,node_id)
#             self.lock_release(model, record_id,user_id)
#             return response



#     @api.model
#     def decision_action_cron(self, model, record_id, fields,node_id):
#         _logger.info("done method called %s", model)
#         if model:
#             model = model.strip()
#         self.env[model].sudo().pre(self)
#         # end calling pre inbuit method here 
#         if record_id:
#             _logger.info("**********record id: %s ", record_id)
#             record_id = int(record_id)
#             current_record_model = self.env[model].sudo().browse(record_id)
#             current_stage = current_record_model.x_o2b_stage
#             _logger.info("*** decision action : %s  for model %s : ",current_stage,model)
#             model_field = self.env['ir.model.fields'].sudo().search(['&',('model','=',model.strip()),('ttype','=','selection'),('name','=','x_o2b_stage')])
#             selection_field = self.env['ir.model.fields.selection'].sudo().search(['&',('field_id','=',model_field.id),('value','=',current_stage.strip())])
#             #fetching next node is decision or not:
#             cur_step = ''
#             pre_step = ''
#             next_step = ''
#             step_type = ''
#             process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',model.strip()),('current_stage','=',selection_field.name)])
#             # call remark_history method
#             self.sudo().remark_history(model,record_id,fields,process)
#             if process:
#                 cur_step = process.current_stage
#                 pre_step = process.previous_stage
#                 next_step = process.next_stage
#                 step_type = process.activity_type

#             _logger.info("###### steping forwared without rule engine : %s", next_step)
#             nex_stage = self.env['o2b.process.modular.statusbar'].sudo().search([('process_name', '=',process.process_name),('stage_name','=',next_step)],limit=1)
#             cur_stage = self.env['o2b.process.modular.statusbar'].sudo().search([('process_name', '=',process.process_name),('stage_name','=',cur_step)],limit=1)
#             _logger.info("*** next step name or: %s or value is %s ; ", nex_stage.stage_value, nex_stage.stage_name)
#             _logger.info("*** curent step name or: %s or value is %s ; ", cur_stage.stage_value, cur_stage.stage_name)
#             if next_step:
#                 next_stage = next_step.replace(' ','_').lower()
#                 cur_step = cur_step.replace(' ','_').lower()
#                 not_specail_char = ('{' in next_step) or ('[' in next_step) or (':' in next_step)
#             if next_step and not not_specail_char and nex_stage.stage_value:
#                 print("next step::::::::::::::::", next_stage)
#                 current_record_model.sudo().write({
#                     # 'x_o2b_stage': nex_stage.stage_value,
#                     'x_done': False,
#                     })
              
#             base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
#             # search aaction id
#             domain = ''
#             if next_step:
#                 domain = '[("x_o2b_stage","=","'+ cur_stage.stage_value + '"),("x_done","=",True)]'
#             print("domain: ", domain)
#             action_id = self.env['ir.actions.act_window'].sudo().search(
#             [('res_model', '=', model.strip()), ('domain', '=', domain)],
#             order='id desc',
#             limit=1
#             )
#             print("action_id :" , action_id)
#             redirect_url = ''
#             if action_id:
#             # http://localhost:8086/web#action=1106&model=x_o2b_admission_process&view_type=list&cids=1&menu_id=880
#                 redirect_url = '{}/web#action={}&model={}&view_type=list'.format(base_url, action_id.id, model)
#                 _logger.info(" decision node Record URL: %s", redirect_url)
#                 if cur_step == 'decision' and not_specail_char:
#                     msg = "[(Rule Engine automatically executing in backgroup for decision stage..]"
#                     response = ['decision', redirect_url,msg]
#                     # url = self.update_stage(model, record_id)
#                     return response;

#             msg = "[(Next Stage : " + next_step  + ")]"
#             response = ['normal', redirect_url,msg]
#             self.env[model].sudo().post(self)
#             return response

#     # write method which confirm reuired field is emply or not:
#     @api.model
#     def required_field_check(self, model, record_id, fields,node_id):
#         response = []
#         _logger.info("required_field_check model %s", model)
#         _logger.info("required_field_check node id %s", node_id)
#         if model:
#             model = model.strip()
#         if record_id and node_id:
#             _logger.info("**********record id: %s ", record_id)
#             record_id = int(record_id)
#             current_record_model = self.env[model].sudo().browse(record_id)
#             current_stage = current_record_model.x_o2b_stage
#             _logger.info("*** decision action : %s  for model %s : ",current_stage,model)
#             model_field = self.env['ir.model.fields'].sudo().search(['&',('model','=',model.strip()),('ttype','=','selection'),('name','=','x_o2b_stage')])
#             selection_field = self.env['ir.model.fields.selection'].sudo().search(['&',('field_id','=',model_field.id),('value','=',current_stage.strip())])
#             required_form_fields = self.env['o2b.process.modular.field.method'].sudo().search([('model_name', '=',model),('form_id','=',node_id),('is_required','=',True)])
#             _logger.info("** all required fields on current form %s ", str(required_form_fields))
#             for rec_field in required_form_fields:
#                 print("** proceess table field id :",rec_field.field_id)
#                 print("** proceess table field name :",rec_field.field_name)
#                 print("** proceess table field label: ",rec_field.field_label)
#                 print("** proceess table field is required :",rec_field.is_required)
#                 print("** proceess table form :",rec_field.form_id)
#                 field_exist = self.env['ir.model.fields'].sudo().search(['&',('name','=',rec_field.field_name),('model','=',rec_field.model_name)])
#                 _logger.info("***** in database field exist corresponind model %s ", field_exist)
#                 domain = []
#                 domain.append(('&'))
#                 domain.append(('id', '=', record_id))
#                 domain.append((rec_field.field_name, '=', None))                
#                 model_field_blank = self.env[model].sudo().search(domain)
#                 print(" ** after making domain: ", domain)
#                 print("** after checking required field valeu **************************", model_field_blank)
#                 if field_exist and not model_field_blank:
#                     _logger.info("***yes we have pass :")
#                     response = ['Pass', rec_field.field_name,rec_field.field_label]
#                     # self.process_manager_crud(model, record_id, fields,node_id)
#                 else:
#                     _logger.info("**** yes model field black give alert on screent to required field")
#                     response = ['Failed', rec_field.field_name,rec_field.field_label]
#             return response

#     # create process manager record : responisble to update and create record in process manager table
#     def process_manager_crud(self, model, record_id,node_id):
#         _logger.info("** process manager insert rec id: %s ",record_id)
#         _logger.info(" **p_manager model name : %s ", model)
#         process_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',model.strip()),('current_stage_id','=',node_id)])

#         if process_stage:
#             print(" process_stage",process_stage)
#             p_manager_record = self.env['o2b.process.manager'].sudo().search(['&',('model','=',model.strip()),('record_id','=',record_id)])
#             current_model = self.env[model].sudo().search([('id','=',record_id)])
#             if p_manager_record:
#                 _logger.info(" ** process record model%s: and current step %s  ", p_manager_record.model,p_manager_record.current_id)
#                 # update
#                 p_manager_record.sudo().write({
#                     'record_id'     : record_id ,
#                     'model'         : model ,
#                     'current_id'    : process_stage.current_stage_id ,
#                     # 'current_name'  : process_stage.current_stage ,
#                     # 'current_type'  : process_stage.activity_type ,
#                     # 'next_id'       : process_stage.next_stage_id ,
#                     # 'next_name'     : process_stage.next_stage ,
#                     })
#             else:
#                 # create
#                 p_manager_record.sudo().create({
#                     'record_id'     : record_id ,
#                     'model'         : model ,
#                     # 'model_stage'   : current_model.x_o2b_stage ,
#                     # 'prev_id'       : process_stage.previous_stage_id ,
#                     # 'pre_name'      : process_stage.previous_stage ,
#                     # 'pre_type'      : 'defined lateral' ,
#                     'current_id'    : process_stage.current_stage_id ,
#                     # 'current_name'  : process_stage.current_stage ,
#                     # 'current_type'  : process_stage.activity_type ,
#                     # 'next_id'       : process_stage.next_stage_id ,
#                     # 'next_name'     : process_stage.next_stage ,

#                     })


#     # write code for advance rule engine start here
#     def adnvace_rule_engine(self,rec,domain,odoo_domain, model,sequence,process,model_name):
#         _logger.info("**rule engine and process decision table%s", rec)
#         _logger.info(" **rule engine model name : %s ", model_name)
#         _logger.info(" **rule engile process statusbar table: %s ", process)
#         print("odoooooooooooooooooooo_domain: ", odoo_domain ,'type of descision rule: ', type(odoo_domain))
#         dummy_domain = odoo_domain.replace(", '&',",",")
#         print("dummy domain: ",dummy_domain, "count of or ", dummy_domain.count('|'))
#         or_count =  dummy_domain.count('|')
#         dummy_domain = dummy_domain.replace(", '|',"," ,")
#         or_data = '['
#         if or_count:
#             for  i in range(or_count):
#                 or_data = or_data + "'|',"
#         dummy_domain = dummy_domain.replace('[', or_data)
#         dummy_domain =  ast.literal_eval(dummy_domain)
#         dummy_domain.append(('id', '=', model.id))
#         print("final dummy_domain :", dummy_domain, "type of dummy domain : ", type(dummy_domain))

#         actual_list = ast.literal_eval(odoo_domain)
#         actual_list.append(('id', '=', model.id))
#         print("type of decesion rule : : " ,type(actual_list))
#         print("value of actual list  : : " ,actual_list)
#         model_obj = model
#         # print("model object is :", model_obj)
#         print("model object is********* :", model,model_obj)
#         dynamic_sequence = sequence
#         record = None
#         try:
#             record = model_obj.search(actual_list)
#             if not record:
#                 record = model_obj.search(dummy_domain)
#                 _logger.info("decision  record found via dummy domian  : %s", record)
#             _logger.info("decesion record found real domian   : %s", record)
#         except Exception as e:
#             _logger.info("except in odoo domain : while searching record: %s", str(e))
#         update_stage_name = rec.next_stage
#         update_stage_value = rec.next_stage.replace(' ','_').lower()
#         _logger.info("***** process statusbar table rec object: %s ",rec )
#         _logger.info("***** process statusbar table next step name: %s ",update_stage_name )
#         _logger.info("***** process statusbar table next step value  %s ",update_stage_value )
        
#         # before fetch via node id: 
#         # updated_state_value = process.search([('stage_name','=',update_stage_name)],limit=1)
#         print(" xxxxxxxxxxxxxxxxx.modelname; ",model_name)
#         updated_state_value = process.search([('process_node_id','=',rec.next_stage_id),('model_name','=',model_name)],limit=1)
#         _logger.info("*** finding current stage in statusbar table %s %s:",process,updated_state_value)
#         _logger.info("**** actucal value in statusbar table %s and %s",updated_state_value.stage_name,updated_state_value.stage_value)
#         current_remark_field = self.env['ir.model.fields'].sudo().search(['&',('name','=','x_remark'),('model','=',model_name)])
#         _logger.info(" ** model have remark field or not: %s ", str(current_remark_field))
#         if record and updated_state_value :
#             for data in record:
#                 _logger.info("updated records: %s and stage is: %s  stage is : ", data,update_stage_value)
#                 if current_remark_field:
#                     data.sudo().write({
#                     'x_o2b_stage': updated_state_value.stage_value,
#                     'x_remark'   : '',
#                     'x_decision' : '',
#                     'x_done': True,
#                     })

#                 else:
#                     data.sudo().write({
#                     'x_o2b_stage': updated_state_value.stage_value,
#                     'x_done': True,
#                     })
#                 # creating new record in process manager table if next step is email after decesion making
#                 if updated_state_value.node_type == 'email':
#                     print("fdddddddddddddddddd object upe", updated_state_value)
#                     print("fdddddddddddddddddd tupe", updated_state_value.node_type)
#                     print("fdddddddddddddddddd nod id", updated_state_value.process_node_id)
#                     print("fdddddddddddddddddd recod ", updated_state_value.node_type)
#                     print("fdddddddddddddddddd model nan", updated_state_value.model_name)
#                     vals= {
#                         'record_id'     : data.id,
#                         'model_stage'   : data.x_o2b_stage ,
#                         'current_id'    : updated_state_value.process_node_id,
#                         'model'         : updated_state_value.model_name ,
#                         'current_name'  : updated_state_value.stage_name ,
#                         # 'next_id'       : p_stage.next_stage_id ,
#                         # 'next_name'     : p_stage.next_stage ,
#                     }
#                     # rec.write(vals)
#                     print(" *******************next tupe is emaiL ")
#                     p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',data.id),('model','=',updated_state_value.model_name)])
#                     print(" ** email curent valuse : process manager record id is: ", p_record.current_id , p_record.model)
#                     print(" ** email before write value: domain attache:record for next value : ", data.id, "model : ",updated_state_value.model_name)
#                     print(" *** email next id after decision: ", updated_state_value.process_node_id)
#                     if not p_record:
#                         self.env['o2b.process.manager'].sudo().create(vals)
#                     else:
#                         p_record.sudo().write(vals)
#                     print(" ** email before write : process manager record id is: ", p_record.current_id , p_record.model)
#                     # self.process_manager_crud(updated_state_value.model_name, p_record.id,updated_state_value.process_node_id)
#                     record_mail = self.env['o2b.process.modular.email'].search([('model_name','=',p_record.model),('current_node_id','=', updated_state_value.process_node_id)],limit=1)
#                     # create record in mail template:
#                     new_mail_record = self.env['o2b.process.email'].sudo().create({
#                                 'record_id'     : p_record.record_id,
#                                 'model'         : p_record.model,
#                                 'current_id'    : p_record.current_id,
#                                 'next_id'       : record_mail.next_step_id,
#                                 'recipient'     : record_mail.recipient ,
#                                 'mail_subject'  : record_mail.mail_subject ,
#                                 'mail_body'     : record_mail.mail_body ,
#                                 # 'create_date'   : record_mail.next_stage_id ,
#                                 # 'mail_send_date': record_mail.next_stage_id ,
#                                 # 'attachment_ids': record_mail.next_stage_id ,
#                                 'mail_count'    : record_mail.mail_limit ,
#                                 'is_active'     : True ,
#                                 'is_sent'       : False ,
#                                 'mail_trigger'  : record_mail.mail_trigger ,
#                                 })
#                     # call fetch attachment and update email table record
#                     self._fetch_attachment(record_mail,new_mail_record)
                    
#                 if updated_state_value.node_type != 'email':
#                     _logger.info(" **we ain in not in email for next record is deleteing")
#                     p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',data.id),('model','=',updated_state_value.model_name)])
#                     print(" ** not email before deleting: domain attache:record id: ", data.id, "model : ",updated_state_value.model_name)
#                     print(" ** not email before deleting: process manager record id is: ", p_record)
#                     # p_record.sudo().unlink()
#                     p_record.write({'active' : False})
#                     # p_record.save()

#             return [True , sequence]
#         else:
#             print("model  decisin exception of current data:", model)
#             model.with_user(2).sudo().write({
#             # 'x_o2b_stage': 'decision_exception',
#             'x_done': True,
#             })
#             return [False , None]
#     # advance rule engine end here


#     def rule_engine(self,current_record_store_value,operator, condition_value, technical_name, model,sequence):
#         print("\n***************** rule engine method**********\necord_store_value",current_record_store_value)
#         print("sequence :  %s and operator is %s and condtion value is %s and technical_name is %s , mode is %s ",sequence,operator,condition_value,technical_name,model)
#         # Read all fields for the record
#         record_data = model.read()[0]  # read() returns a list, take the first (and usually the only) element
#         # Print each field and its value
#         result = False
#         for field_name, field_value in record_data.items():
#             # print(f"Field: {field_name}, Value: {field_value}")
#             if field_name == technical_name and field_value == condition_value:
#                 # print("yes we found the field name and rquest to docntin math H ")
#                 result = True;
#                 # return True;
#             else:
#                 print("condition is not matched:")
#                 # retult =  False
#                 # return False;
#         return [result,sequence]

#         # dynamic code execution
#         # code = f'''
#         # if {current_record_store_value} {operator} {condition_value}:
#         #     print(f"{current_record_store_value} is {operator} {condition_value}")
#         # else:
#         #     print(f"{current_record_store_value} is not {operator} {condition_value}")
#         # '''
#         # # Execute the dynamically generated code
#         # # exec(code)

#         return True;

# # method to chnange stage without conditonal statement:
#     @api.model
#     def update_stage_not_found(self,model, record_id):
#         obj = self.env[model].sudo().browse(record_id)
#         # test code start 
#         base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
#         print("base url: ", base_url)
#         # search aaction id
#         domain = '[("x_o2b_stage","=","'+ obj.x_o2b_stage+ '")]'
#         print("domain: ", domain)
#         action_id = self.env['ir.actions.act_window'].sudo().search([('res_model','=',model),('domain','=',domain)])
#         print("action_id :" , action_id)

#         # http://localhost:8086/web#action=1106&model=x_o2b_admission_process&view_type=list&cids=1&menu_id=880
#         redirect_url = '{}/web#action={}&model={}&view_type=list'.format(base_url, action_id.id, model)
#         print("Record URL:", redirect_url)
#         # test code end here 
#         try:
#             current_stage = obj.x_o2b_stage
#             print("current stage: ", current_stage)
#             obj.write({
#                     'x_o2b_stage': 'decision'
#                     })

#         except Exception as e:
#             # raise exceptions.ValidationError("Done button is only applicable for Oflow Process Module.")
#             # raise UserError(_("Done button is only applicable for Oflow Process Module."))
#             # raise UserError("Done button is only applicable for Oflow Process Module.")
#             # return "not_found"
#             print("excetpion is : ", e)
#         return redirect_url;
#         # find next stage

# #  end here 


#     @api.model
#     def update_stage(self,model, record_id):
#         obj = self.env[model].sudo().browse(record_id)
#         # test code start 
#         base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
#         print("base url: ", base_url)
#         # search aaction id
#         domain = '[("x_o2b_stage","=","'+ obj.x_o2b_stage+ '")]'
#         print("domain: ", domain)
#         action_id = self.env['ir.actions.act_window'].sudo().search([('res_model','=',model),('domain','=',domain)])
#         print("action_id :" , action_id)

#         # http://localhost:8086/web#action=1106&model=x_o2b_admission_process&view_type=list&cids=1&menu_id=880
#         redirect_url = '{}/web#action={}&model={}&view_type=list'.format(base_url, action_id.id, model)
#         print("Record URL:", redirect_url)
#         # test code end here 
#         try:
#             current_stage = obj.x_o2b_stage
#             print("current stage: ", current_stage)
#         except Exception as e:
#             # raise exceptions.ValidationError("Done button is only applicable for Oflow Process Module.")
#             # raise UserError(_("Done button is only applicable for Oflow Process Module."))
#             # raise UserError("Done button is only applicable for Oflow Process Module.")
#             return "base_module"

#         # find next stage
#         model_id = self.env['ir.model'].sudo().search([('model','=',model)])
#         field_id = self.env['ir.model.fields'].sudo().search(['&',('model_id','=',model_id.id),('name','=','x_o2b_stage')])
#         all_states = self.env['ir.model.fields.selection'].sudo().search([('field_id','=',field_id.id)])
#         stage =[]
#         for rec in all_states:
#             new_dict = {}
#             new_dict['sequence'] = rec.sequence
#             new_dict['value'] = rec.value
#             new_dict['name'] = rec.name
#             stage.append(new_dict)
#         print("all stage in list: ", stage)
#         result_dict = self.get_dict_by_value(stage,current_stage,None)
#         if result_dict:
#             serial_no = result_dict.get('sequence')
#             print("servrial no: ", serial_no)
#             next_update_record = self.get_dict_by_value(stage,None,serial_no+1)
#             print("next_update_record :", next_update_record)
#             process_modular = self.env['o2b.process.modular'].sudo().search([('model_name','=',model.strip())])
#             _logger.info("*** finding current stage for desision rule %s :",process_modular.process_stage_line)

#             if next_update_record:
#                 obj.write({
#                     'x_o2b_stage': next_update_record.get('value')
#                     })
#                 # write code for upating o2b.process.modular.stage talbe start her
#                 # o2b_process = self.env['o2b.process.modular'].sudo().search([('model_name','=',model.strip())])
#                 # if o2b_process:
#                 #     for rec in o2b_process:
#                 #         rec.sudo().write({
#                 #             'current_stage' : next_update_record.get('name'),
#                 #             'is_active': True if rec.activity_name == next_update_record.get('name') else False
#                 #             })
            
#                 # write code for upating o2b.process.modular.stage talbe end here
#         else:
#             print("Dictionary with value '{}' not found.".format(current_stage))

#         if not current_stage:
#             print("fetch database ", stage[0].get('value').strip())
#             obj.write({
#                 'x_o2b_stage': stage[0].get('value').strip()
#                 })

#         # test code for creating file in o2b_process_module
#         print("we in file updating and creating block ")
#         module_path = os.path.dirname(__file__)
#         print("Module path :", module_path)
#         python_file = os.path.join(module_path, 'override_models.py')
#         if os.path.exists(python_file):
#            print(f' {python_file} exists.')
#         else:
#             content = '''\
# from odoo import models, fields,api,_,os
# from odoo.exceptions import ValidationError, UserError

# class o2bProcessModularOverride(models.Model):
#     _inherit = 'o2b.process.modular'

#     # Please defind your method and bind it done button
#     @api.model
#     def action_1(self):
#         print("O2b Technologies : action_1")
#             '''
#             with open(python_file, 'w') as f:
#                 f.write(content)  # You can write initial content here if needed
#             print(f"File '{python_file}' created successfully.")

#         # Navigate one directory level back
#         parent_dir = os.path.dirname(module_path)
#         print("parrent directory: ", parent_dir)
#         js_file_path = parent_dir + '/static/src/views/form/override_form_controller.js'
#         print("js_file_path path: ", js_file_path)
#         if os.path.exists(js_file_path):
#            print(f' {js_file_path} exists.')
#         else:
#             content = '''\
# /** @odoo-module **/
# import { patch } from "@web/core/utils/patch";
# import { FormController } from "@web/views/form/form_controller";
# import { Component, onWillStart, useEffect, useRef, onRendered, useState, toRaw } from "@odoo/owl";
# import { useBus, useService } from "@web/core/utils/hooks";
# import { useModel } from "@web/views/model";
# import { SIZES } from "@web/core/ui/ui_service";
# import rpc from 'web.rpc';
# import { useViewButtons } from "@web/views/view_button/view_button_hook";
# import { useSetupView } from "@web/views/view_hook";
# import { useDebugCategory } from "@web/core/debug/debug_context";
# import { usePager } from "@web/search/pager_hook";
# import { isX2Many } from "@web/views/utils";
# import { registry } from "@web/core/registry";
# const viewRegistry = registry.category("views");

# odoo.__DEBUG__ && console.log("Console log inside the patch function", FormController.prototype, "form_controller");

# patch(FormController.prototype, 'web.FormView', {
#     setup() {
#         this._super.apply(this, arguments);
#         this.orm = useService("orm");
#         this.done = this.done.bind(this); // Ensure 'done' is bound to the class instance
#     },
#     async done() {
#         console.log("done****", this);
#         // Assuming you have access to 'record' from the context or instance
#         const record = this.model.root;
#         const model = this.model.root.resModel;
#         let canProceed = true;
#         let record_id = this.props.resId
#         console.log("model**** :", model);
#         console.log("this.props :" , this.props)
#         console.log("we have current recodr Id ", record_id)
#         if(record_id === undefined || !record_id)
#         {   
#             console.log("if not found record : ", record_id)
#             window.location.reload();
#         }
#         if(true)
#         {
#         try {
#             const call_method = await this.orm.call('o2b.process.modular', "update_stage", [model,record_id]);
#             console.log("call_method print", call_method)
#             if(call_method)
#             {   this.model.load({ resId: record_id });
#                 // window.location.reload();
#                 return this.model.load({ resId: record_id });
#             }
#             console.log("Stage updated", record_id);
#         } catch (error) {
#             console.log("Failed to update state:", error);
#         }
#         }
#     }
# });
#         '''
            
#             with open(js_file_path, 'w') as f:
#                 f.write(content)  # You can write initial content here if needed
#             print(f"File '{js_file_path}' created successfully.")
#         # end file creating: 
#         response = ['normal', redirect_url]
#         return response;
#         # return redirect_url;

#     # Function to get dictionary based on 'value' key
#     def get_dict_by_value(self,list_of_dicts, value,sequence):
#         if value:
#             for item in list_of_dicts:
#                 if item['value'] == value:
#                     return item
#         if sequence == 0 or  sequence:
#             for item in list_of_dicts:
#                 if item['sequence'] == sequence:
#                     return item
#         return None  # Return None if not found

#     # Remark history save function call:
#     def remark_history(self,model,record_id,fields,process):
#         _logger.info("*** remark_history: %s", model)
#         _logger.info("*** record id :  %s", record_id)
#         _logger.info("*** process activity_type:  %s", process.activity_type)
#         _logger.info("*** process activity name:  %s", process.next_stage)
#         if model:
#             model = model.strip()
#         if record_id:
#             record_id = int(record_id)
#         model_exist = self.env['ir.model'].sudo().search([('model','=',model)])
#         current_model = self.env[model].sudo().search([('id','=',record_id)])
#         _logger.info("*** current record: in remark history: %s ", current_model)
#         current_record_field = self.env['ir.model.fields'].sudo().search(['&',('name','=','x_remark'),('model','=',model)])
#         _logger.info("***** current record : x_o2b_decision check %s ", current_record_field)
#         if current_model and current_record_field:
#             _logger.info("***intert into remark table:%s ,%s:", current_model.x_remark,current_model.x_decision)
#             field = model.split('.')[-1]
#             _logger.info("**** filed in remak histroy:%s  " , field)
#             relation_field = 'x_o2b_' + field +'_in_remark_history'
#             _logger.info(" *** history remark table: %s ", relation_field)
#             if current_model.x_remark or current_model.x_decision:
#                 self.env['o2b.process.modular.remark.history'].sudo().create({
#                     relation_field  : record_id,
#                     'decision'      : current_model.x_decision,
#                     'remark'        : current_model.x_remark,
#                     'current_stage' : current_model.x_o2b_stage
#                     })
#                 print(" ********* current stage change " , current_model.x_o2b_stage)
#                 if process.next_stage not in ['decision','email']:
#                     _logger.info(" ** next step is : %s ", process.next_stage)
#                     current_model.sudo().write({
#                         'x_remark'   : '',
#                         'x_decision' : '',
#                         })
#                     self.env['o2b.process.modular.remark.history'].sudo().create({
#                     relation_field  : record_id,
#                     'decision'      : current_model.x_decision,
#                     'remark'        : 'Automatically moved from email' if process.activity_type =='email' else 'automatically moved from decision stage',
#                     'current_stage' : current_model.x_o2b_stage
#                     })
      
#     # Univarsal Schedular
#     def _universal_schedular(self,model_obj, model_name):
#         # _logger.info(" ****process manager schedular is running*****")
#         try:
#             p_record = self.env['o2b.process.manager'].sudo().search([('model','=',model_name)])
#             _logger.info("*** process manager have record count: %s : ",len(p_record))
#             for rec in p_record:
#                 _logger.info(" ** record : %s and model: %s  and node id : %s ",rec.record_id,rec.model,rec.current_id)
#                 record_id = int(rec.record_id)
#                 cur_record_model = self.env[rec.model].sudo().browse(record_id)
#                 current_stage = cur_record_model.x_o2b_stage
#                 _logger.info("*** Univeral model current stage : %s  for model %s : ",current_stage,rec.model)
#                 curr_id = ''
#                 cur_step = ''
#                 curr_type = ''
#                 next_id = ''
#                 next_step = ''
#                 next_type  = ''
#                 # process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model),('current_stage','=',current_stage)])
#                 process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model),('current_stage_id','=',rec.current_id)])
#                 _logger.info(" ** current process record exist or not: %s ", str(process))
#                 if process:
#                     curr_id = process.current_stage_id
#                     cur_step = process.current_stage
#                     curr_type = process.activity_type
#                     next_id = process.next_stage_id
#                     next_step = process.next_stage
#                     _logger.info(" ** universal schedular next id is %s : ", next_id)
#                     if next_id:
#                         next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',next_id)],limit=1)
#                         print(" *** next object value : ", next_obj.node_type)
#                         if next_obj.node_type not in ['decision','email']:
#                             _logger.info(" ** in normal stage move and type is :: %s ",next_obj.node_type,)
#                             _logger.info(" ** in normal stage value is %s :",next_obj.stage_value,)
#                             cur_record_model.sudo().write({
#                                 'x_o2b_stage': next_obj.stage_value,
#                                 'x_done': True,
#                                 })
#                             self.remark_history(rec.model,rec.record_id,None,process)
#                             rec.write({'active' : False})
#                             # rec.save()
#                             # rec.sudo().unlink()

#                         if next_obj.node_type in ['decision']:
#                             _logger.info(" ** in decision next step is desision: %s ", next_obj.node_type)
#                             _logger.info(" ** in decision stage value is %s :",next_obj.stage_value,)
#                             p_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model.strip()),('current_stage_id','=',next_id)])
#                             print(" %%%%%%%%%% for decision current id: :", p_stage.current_stage_id)
#                             print(" %%%%%%%%%% for decision  current stage name:", p_stage.current_stage)
#                             print(" %%%%%%%%%% for decision : activityname ", p_stage.activity_name)
#                             print(" %%%%%%%%%% for decision : next id", p_stage.next_stage_id)
#                             print(" %%%%%%%%%% for decision : activity_type", p_stage.activity_type)
#                             p_curr = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',next_id)],limit=1)
#                             vals= {
#                                 'model_stage'   : cur_record_model.x_o2b_stage ,
#                                 'current_id'    : p_stage.current_stage_id,
#                                 'current_name'  : p_stage.current_stage ,
#                                 'next_id'       : p_stage.next_stage_id ,
#                                 'next_name'     : p_stage.next_stage ,
#                                 }
#                             rec.sudo().write(vals)
#                             self.remark_history(rec.model,rec.record_id,None,process)
#                             decisions_nodes = self.env['o2b.process.modular.stage'].search([('model_name', '=', rec.model.strip()), ('activity_type', '=', 'decision')])
#                             for recc in decisions_nodes:
#                                 desision_records = self.env[rec.model].sudo().browse(record_id)
#                                 current_stage = cur_record_model.x_o2b_stage
#                                 model = desision_records
#                                 record = desision_records
#                                 records = desision_records
#                                 self.env['o2b.process.modular'].action_test(model, record, records, desision_records, decisions_nodes,recc.current_stage)
#                             self.remark_history(rec.model,rec.record_id,None,process)
#                             # rec.sudo().unlink()

#                         if next_obj.node_type in['email']:
#                             _logger.info(" ** we are in email step reocrd for current record id %s : ", rec.record_id)
#                             print(" rec.current_id : ",rec.current_id )
#                             email_current_id_obj = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model.strip()),('current_stage_id','=',rec.current_id)],limit=1)
#                             print(" ** email current id: ", email_current_id_obj.current_stage_id, email_current_id_obj.next_stage_id)
#                             record_mail = self.env['o2b.process.modular.email'].search([('model_name','=',rec.model.strip()),('current_node_id','=', email_current_id_obj.next_stage_id)],limit=1)
#                             _logger.info("** all mail triiger list * %s ", str(record_mail))
#                             current_step = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_mail.current_node_id)],limit=1)
#                             # _logger.info("** mail step record for model: %s : ", rec.model_name)
#                             _logger.info("** record curr stage name : %s : ", current_step.stage_name)
#                             _logger.info("** record curr stage value: %s : ", current_step.stage_value)
#                             # records = self.env[rec.model_name].sudo().search([('x_o2b_stage','=',current_step.stage_value)])
#                             next_step = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_mail.next_step_id)],limit=1)
#                             _logger.info("** record  next stage name : %s : ", next_step.stage_name)
#                             _logger.info("** record next stage value: %s : ", next_step.stage_value)
#                             # p_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model.strip()),('current_stage_id','=',rec.next_id)])
#                             #check after email next not is not decision
#                             self.remark_history(rec.model,rec.record_id,None,process)
#                             email_next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_mail.next_step_id)],limit=1)
#                             if email_next_obj.node_type not in ['decision']:
#                                 print(" ** after email this is simple step to forward simply type : ", email_next_obj.node_type)
#                                 cur_record_model.sudo().write({
#                                     'x_o2b_stage': next_step.stage_value,
#                                     'x_done': True,
#                                     })
#                                 self.remark_history(rec.model,rec.record_id,None,process)
#                                 # handle mail content here and sending mail
#                                 new_mail_record = self.env['o2b.process.email'].sudo().create({
#                                     'record_id'     : rec.record_id,
#                                     'model'         : rec.model,
#                                     'current_id'    : rec.current_id,
#                                     'next_id'       : record_mail.next_step_id,
#                                     'recipient'     : record_mail.recipient ,
#                                     # 'recipient'     : record_mail.recipient ,
#                                     'mail_subject'  : record_mail.mail_subject ,
#                                     'mail_body'     : record_mail.mail_body ,
#                                     # 'create_date'   : record_mail.next_stage_id ,
#                                     # 'mail_send_date': record_mail.next_stage_id ,
#                                     # 'attachment_ids': record_mail.next_stage_id ,
#                                     'mail_count'    : record_mail.mail_limit ,
#                                     'is_active'     : True ,
#                                     'is_sent'       : False ,
#                                     'mail_trigger'  : record_mail.mail_trigger ,
#                                     })
#                                 # call fetch attachment and update email table record
#                                 self._fetch_attachment(record_mail,new_mail_record)

#                                 # handle stage if next step is also email or decision
#                             # email_next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_mail.next_step_id)],limit=1)
#                             if email_next_obj.node_type in['decision']:
#                                 print(" ** after email next step is decion type is:: ", email_next_obj.node_type)
#                                 print(" **** we are in emain next decision: next:",email_next_obj.process_node_id)
#                                 # create new record in email table
#                                 new_mail_record = self.env['o2b.process.email'].sudo().create({
#                                 'record_id'     : rec.record_id,
#                                 'model'         : rec.model,
#                                 'current_id'    : rec.current_id,
#                                 'next_id'       : record_mail.next_step_id,
#                                 'recipient'     : record_mail.recipient ,
#                                 'mail_subject'  : record_mail.mail_subject ,
#                                 'mail_body'     : record_mail.mail_body ,
#                                 # 'create_date'   : record_mail.next_stage_id ,
#                                 # 'mail_send_date': record_mail.next_stage_id ,
#                                 # 'attachment_ids': record_mail.next_stage_id ,
#                                 'mail_count'    : record_mail.mail_limit ,
#                                 'is_active'     : True ,
#                                 'is_sent'       : False ,
#                                 'mail_trigger'  : record_mail.mail_trigger ,
#                                 })
#                                 # call fetch attachment and update email table record
#                                 self._fetch_attachment(record_mail,new_mail_record)
#                                 # call decsion making schedular
#                                 decisions_nodes = self.env['o2b.process.modular.stage'].search([('model_name', '=', rec.model.strip()), ('activity_type', '=', 'decision')])
#                                 for recc in decisions_nodes:
#                                     desision_records = self.env[rec.model].sudo().browse(record_id)
#                                     current_stage = cur_record_model.x_o2b_stage
#                                     model = desision_records
#                                     record = desision_records
#                                     records = desision_records
#                                     self.env['o2b.process.modular'].action_test(model, record, records, desision_records, decisions_nodes,recc.current_stage)
#                                 self.remark_history(rec.model,rec.record_id,None,process)
#                             else:
#                                 rec.write({'active' : False})
#                                 # rec.save()
#                                 # rec.sudo().unlink()
#                     else:
#                         _logger.info(" ** if next id false means end of stage %s ", next_id)
#                         cur_record_model.write({
#                             'x_done': True
#                             })
#                         # rec.sudo().unlink()
#                         rec.write({'active' : False})
#                         # rec.save()
#                         # rec.sudo().unlink()
#                 # call mail sending queue method:
#             self._mail_sender()
#         except Exception as e:
#             _logger.info(" ** process manager table %s ",str(e))
#             pass                  

#     # o2b mail sender service method
#     def _mail_sender(self):
#         try:
#             _logger.info("** we are in mail sender service:")
#             email_records = self.env['o2b.process.email'].sudo().search([('is_sent','=',False)])
#             for email_queue in email_records:
#                 _logger.info("mail queue current data: %s", email_queue)
#                 # trying to fetch dynamic value for getting recepient: 
#                 # just tesing puprose for picking one record
#                 recipient  = ""
#                 msg_body = ""
#                 msg_subject = ""
#                 if email_queue:
#                     # to = email_queue.recipient
#                     record_model = self.env[email_queue.model].sudo().browse(int(email_queue.record_id))
#                     if record_model:
#                         recipient = record_model.x_o2b_email
#                         _logger.info("")
#                     msg_body = email_queue.mail_body
#                     msg_subject = email_queue.mail_subject
#                     _logger.info(" trying to email send : %s: for record id: %s ", recipient,str(email_queue))
                    
#                     # mail_values = {
#                     #     'subject'   : msg_subject,
#                     #     'email_to'  : recipient,
#                     #     'body_html' : msg_body,
#                     #     # 'attachment_ids': [(6, 0, email_queue.attachment_ids.id)],
#                     # }
#                     # mail = self.env['mail.mail'].with_user(2).sudo().create(mail_values)
#                     # mail_sent = mail.sudo().send(auto_commit=True)

#                     # trying to create new template oject to send mail
#                     _logger.info(" we are in email through email template")
#                     email_template = {
#                     'name'          : 'oflow_email_template',
#                     'model_id'      : 97,
#                     'subject'       : msg_subject,
#                     'description'   : msg_subject,
#                     'body_html'     : msg_body,
#                     'email_from'    : 'info@oflowai.com',
#                     'use_default_to': False,
#                     'email_to'      : recipient,
#                     # 'partner_to'    : '',
#                     # 'email_cc'      : '',
#                     # 'reply_to'      : '',
#                     # 'scheduled_date': '',
#                     }
#                     odoo_mail_template = self.env['mail.template'].search([('name','=','oflow_email_template')])
#                     if odoo_mail_template:
#                         _logger.info(" ** update existing mail template: ")
#                         odoo_mail_template.with_user(2).sudo().write(email_template)
#                     else:
#                         _logger.info(" ** creating new mail template")
#                         odoo_mail_template = self.env['mail.template'].with_user(2).sudo().create(email_template)
                    
#                     # checking muliple ids
#                     attachment_tuples = [(4, attachment.id) for attachment in email_queue.attachment_ids]
#                     odoo_mail_template.attachment_ids = attachment_tuples
#                     mail_id = odoo_mail_template.sudo().send_mail(self.id, force_send=True)
#                     odoo_mail_template.attachment_ids = [(5, 0, 0)]
#                     # time.sleep(3)
#                     email_queue.sudo().write({
#                         'is_sent':True,
#                         'active' :False
#                         })

#         except Exception as e:
#             _logger.info(" some erron in seding emial%s",str(e))

#     # o2b mail sender service method
#     def _fetch_attachment(self,record_mail,new_mail_record):
#         try:
#             _logger.info("** we are in fetching attachment from middleware service")
#             # call node fetch api to get attachents and update process email table
#             #for local
#             url = 'http://192.168.1.26:3636/email/fetch/attachment' 
#             # for internal
#             # url = 'http://122.160.26.224:3636/email/fetch/attachment' 
#             # for live
#             # url = 'http://192.168.1.26:3636/email/fetch/attachment'  
#             headers = {
#             'Content-Type': 'application/json',
#             }
#             data = {
#             'key': 'o2b_technologies',
#             'id'    : record_mail.template_id
#             }

#             response = requests.post(url, json=data, headers=headers)
#             print(" type of reposne: ", type(response))
#             response_data = response.json()

#             # Extract attachment_file data
#             attachment_files = response_data.get('message', [{}])[0].get('attachment_file', [])
#             print(" *** length: ", len(attachment_files))
#             attachment_id = []
#             for file in attachment_files:
#                 file_data = bytes(file['data'])
#                 # encoded_data = base64.b64encode(file_data).decode('utf-8')
#                 new_file = self.env['ir.attachment'].sudo().create({
#                 'name': random.randint(1, 100),
#                 'type': 'binary',
#                 'datas': base64.encodebytes(file_data),
#                 'res_model': 'o2b.process.mail',
#                 'res_id': new_mail_record.id,
#                 'mimetype': 'application/pdf'
#                 })
#                 print(" *** new file: ", new_file)
#                 attachment_id.append(new_file.id)
#                 new_mail_record.sudo().write({
#                 'attachment_ids': attachment_id,
#                 })
#                 print(" attachmetn id update or nO : ", new_mail_record.attachment_ids)
#         except Exception as error:
#             _logger.info("=====Exception while fetching and updating email table template %s", error)
#             pass