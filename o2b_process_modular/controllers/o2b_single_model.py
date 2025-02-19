# import time
# from odoo import models, fields,api,_,os
# from odoo.exceptions import ValidationError, UserError
# import ast
# import random
# import requests
# import base64
# import logging
# import re
# import dns.resolver
# from datetime import datetime, date,timedelta
# import json
# # from email_validator import validate_email, EmailNotValidError



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


# class o2bProcessModularStageEmailVerified(models.Model):
#     _name = 'o2b.process.modular.emailverified'
#     _description = 'O2b Process Modular Email Verified'
#     process_id = fields.Char()
#     process_name = fields.Char()
#     email_verified_line = fields.Many2one('o2b.process.modular', string='O2b Proces Email Verified', ondelete='cascade',invisible=1)
#     current_stage = fields.Char()
#     current_id = fields.Char()
#     email_verify_list = fields.Char(string = 'Email list')
   

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
#     set_unset_value = fields.Char(string = 'Set Value')

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
#     current_stage = fields.Char(string='Current Stage')
#     remark_uid = fields.Many2one('res.users', string="User", default=lambda self: self.env.user.id)
    
  
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
#     process_menu_name_list = fields.Char()
#     process_menu_node_list = fields.Char()
#     process_stages_ids = fields.One2many('o2b.process.modular.stage', 'process_stages', string='Process Stage ID')
#     process_stages_decision_ids = fields.One2many('o2b.process.modular.stage.decision', 'process_decision_line', string='Process Decision ID')
#     process_stages_field_ids = fields.One2many('o2b.process.modular.field.method', 'process_field_line', string='Stage Field ID',)
#     process_state_ids = fields.One2many('o2b.process.modular.statusbar', 'process_stage_line', string='Field ID')
#     process_group_ids = fields.One2many('o2b.process.modular.group', 'process_groups', string='Group Ids')
#     process_menu_ids = fields.One2many('o2b.process.modular.menu', 'process_menus', string='menu Ids')
#     process_view_ids = fields.One2many('o2b.process.modular.view', 'process_views', string='View Ids')
#     process_action_ids = fields.One2many('o2b.process.modular.action', 'process_actions', string='Action Ids')
#     process_email_ids = fields.One2many('o2b.process.modular.email', 'process_email_line', string='Email Ids')
#     process_email_verified_ids = fields.One2many('o2b.process.modular.emailverified', 'email_verified_line', string='Email verified Ids')
#     basic_start_template = fields.Text(string='XML Content', default=''' ''')
#     auto_process_api_status = fields.Boolean('Json API next step status', default=False)
#     auto_process_webform_status = fields.Boolean('Web form next step status', default=False)

    

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
#         # calling method to upgrade button: 
#         current_module = self.env['ir.module.module'].sudo().search([('name','=',module_name)],limit=1)
#         current_module.with_user(1).sudo().button_immediate_install()
#         current_module.with_user(1).sudo().button_immediate_upgrade()
#         result = self.env['base.module.update'].with_user(2).sudo().update_module()
        
#         model = 'o2b.' + process_name.replace(' ','_').lower()
#         current_model = self.env['ir.model'].sudo().search([('model','=',model)],limit=1)
#         if not current_model:
#             result = self.env['base.module.update'].with_user(2).sudo().update_module()
#             _logger.info("calling update_module base method: %s", result)
#             # calling method to upgrade button: 
#             current_module = self.env['ir.module.module'].sudo().search([('name','=',module_name)],limit=1)
#             current_module.with_user(1).sudo().button_immediate_install()
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
    


#     # **************uitility method start here*******************
    
#     # write code for ugraded_rule_engine start here
#     def upgraded_rule_engine(self,process_mng_ob,statusbar_obj,rule_rec_obj):
#         _logger.info(" **upgraded_rule_engineprocess_mng_ob %s", process_mng_ob)
#         _logger.info(" **statusbar obj : %s ", statusbar_obj)
#         _logger.info(" **decision rule obje: %s ", rule_rec_obj)
#         node_domain = rule_rec_obj.get('domain')
#         dummy_domain = rule_rec_obj.get('node_domain')
#         odoo_domain = self.domain_parse(rule_rec_obj.get('domain'))
#         record_next_name = rule_rec_obj.get('next_name')
#         record_next_id = rule_rec_obj.get('next_id')
#         record_exception_name = rule_rec_obj.get('exception_name')
#         record_exception_id = rule_rec_obj.get('exception_id')
#         _logger.info(" ***node domian: %s ", str(node_domain))
#         _logger.info(" ***node parse domian: %s ", str(dummy_domain))
#         _logger.info(" ***odoo_domain: %s ", str(odoo_domain))

#         print(" ****  ooo node domain type ", type(node_domain))
#         print(" ****  ooo parse domain type ", type(dummy_domain))
#         print(" ****  ooo odoo_domain domain type ", type(odoo_domain))
        
#         dummy_domain = dummy_domain.replace(", & ,",",")
#         print(" &&&&&&&& dummin doman after remoe and ",dummy_domain )
#         or_count =  dummy_domain.count('|')
#         dummy_domain = dummy_domain.replace(", '|',"," ,")
#         or_data = '['
#         if or_count:
#             for  i in range(or_count):
#                 or_data = or_data + "'|',"
#         dummy_domain = dummy_domain.replace('[', or_data)
#         # replace 'false' to False and 'true' to True
#         dummy_domain = dummy_domain.replace('"true"','True')
#         dummy_domain = dummy_domain.replace('"false"','False')

#         dummy_domain =  ast.literal_eval(dummy_domain)
#         dummy_domain.append(('id', '=', int(process_mng_ob.record_id)))
#         _logger.info("after parse nodedomain converted final dummy domain : %s and type of %s", dummy_domain, type(dummy_domain))

#         print(" current record from process manger ", process_mng_ob.record_id)
#         actual_list = odoo_domain
#         actual_list.append(('id', '=', int(process_mng_ob.record_id)))
#         print(" uuuuuuuuuuuuuuuuuuuuuuuuuu", process_mng_ob , process_mng_ob.record_id, process_mng_ob.current_id)
#         model_obj = self.env[process_mng_ob.model].sudo().browse(int(process_mng_ob.record_id))
#         print("model object is :", model_obj)
#         # print("model object is x_decision :", model_obj.x_decision)
#         record = None
#         print(" chekcing actual_list:*************8 ", actual_list)
#         print(" chekcing dummy_domain:*************8 ", dummy_domain)
#         try:
#             record = model_obj.search(dummy_domain)
#             _logger.info(" *** dmmy domain which is applied %s  and type %s  ",dummy_domain, type(dummy_domain))
#             if not record:
#                 record1 = model_obj.search(actual_list)
#                 _logger.info(" *** actual domain which is applied %s  and type %s  ",actual_list, type(actual_list))
#                 _logger.info("decision  record found via actual_list  : %s", record1)

#             _logger.info("decesion record found dummy_domain   : %s", record)
#         except Exception as e:
#             _logger.info(" ** after applying data is not found moving previous states")
  
#         if record:
#             print(" *** yes decision rule applyed and fetch record value ", record)
#             print(" *** sant model name : ", process_mng_ob.model, " strip ", process_mng_ob.model.strip())
#             print(" *** sant record_next_id : ", record_next_id, " strip ", record_next_id.strip())
#             updated_state_value = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',process_mng_ob.model.strip()),('process_node_id','=',record_next_id)],limit=1)
#             _logger.info("*** finding current stage in statusbar table %s:",updated_state_value)
#             _logger.info("**** actucal value in statusbar table %s and %s",updated_state_value.stage_name,updated_state_value.stage_value)
#             current_remark_field = self.env['ir.model.fields'].sudo().search(['&',('name','=','x_decision'),('model','=',process_mng_ob.model.strip())])
#             _logger.info(" ** model have remark field or not: %s ", str(current_remark_field))
#             _logger.info("updated records withs antosh: %s and stage is: %s  stage is : ", record,updated_state_value)
#             if updated_state_value:
#                 if current_remark_field:
#                     record.sudo().write({
#                     'x_o2b_stage': updated_state_value.stage_value,
#                     'x_remark'   : '',
#                     'x_decision' : '',
#                     'x_done': True,
#                     })
#                 else:
#                     record.sudo().write({
#                     'x_o2b_stage': updated_state_value.stage_value,
#                     'x_done': True,
#                     })


#             #creating record in process manager table if agian next step is decision
#             if updated_state_value.node_type == 'decision':
#                 print("again next is decision object", updated_state_value)
#                 print("fdddddddddddddddddd tupe", updated_state_value.node_type)
#                 print("fdddddddddddddddddd nod id", updated_state_value.process_node_id)
#                 print("fdddddddddddddddddd recod ", updated_state_value.node_type)
#                 print("fdddddddddddddddddd model nan", updated_state_value.model_name)
#                 next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',process_mng_ob.model.strip()),('process_node_id','=',updated_state_value.process_node_id)],limit=1)
#                 self.handle_decision_records(process_mng_ob,next_obj)
               
#             # creating new record in process manager table if next step is email after decesion making
#             if updated_state_value.node_type == 'email':
#                 print("fdddddddddddddddddd object upe", updated_state_value)
#                 print("fdddddddddddddddddd tupe", updated_state_value.node_type)
#                 print("fdddddddddddddddddd nod id", updated_state_value.process_node_id)
#                 print("fdddddddddddddddddd recod ", updated_state_value.node_type)
#                 print("fdddddddddddddddddd model nan", updated_state_value.model_name)
#                 vals= {
#                     'record_id'     : record.id,
#                     'model_stage'   : record.x_o2b_stage ,
#                     'current_id'    : updated_state_value.process_node_id,
#                     'model'         : updated_state_value.model_name ,
#                     'current_name'  : updated_state_value.stage_name ,
#                     }
#                 # rec.write(vals)
#                 print(" *******************next tupe is emaiL with aryan ")
#                 p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',record.id),('model','=',updated_state_value.model_name)])
#                 print(" ** email curent valuse : process manager record id is: ", p_record.current_id , p_record.model)
#                 print(" ** email before write value: domain attache:record for next value : ", record.id, "model : ",updated_state_value.model_name)
#                 print(" *** email next id after decision: ", updated_state_value.process_node_id)
#                 if not p_record:
                    
#                     self.env['o2b.process.manager'].create(vals)
#                 else:
#                     new_p_rect = self.env['o2b.process.manager'].create(vals)
#                     p_record.write({ 
#                         'current_id'    : updated_state_value.process_node_id,
#                         'active'        : False
#                         })
#                 print(" ** email before write : process manager record id is: ", p_record.current_id , p_record.model)

#                 # self.process_manager_crud(updated_state_value.model_name, p_record.id,updated_state_value.process_node_id)
#                 record_mail = self.env['o2b.process.modular.email'].search([('model_name','=',p_record.model),('current_node_id','=', updated_state_value.process_node_id)],limit=1)
#                 # create record in mail template:
#                 new_mail_record = self.env['o2b.process.email'].sudo().create({
#                             'record_id'     : p_record.record_id,
#                             'model'         : p_record.model,
#                             'current_id'    : p_record.current_id,
#                             'next_id'       : record_mail.next_step_id,
#                             'recipient'     : record_mail.recipient ,
#                             'mail_subject'  : record_mail.mail_subject ,
#                             'mail_body'     : record_mail.mail_body ,
#                             # 'create_date'   : record_mail.next_stage_id ,
#                             # 'mail_send_date': record_mail.next_stage_id ,
#                             # 'attachment_ids': record_mail.next_stage_id ,
#                             'mail_count'    : record_mail.mail_limit ,
#                             'is_active'     : True ,
#                             'is_sent'       : False ,
#                             'mail_trigger'  : record_mail.mail_trigger ,
#                             })
#                 # call fetch attachment and update email table record
#                 self._fetch_attachment(record_mail,new_mail_record)
#             if updated_state_value.node_type not in ['decision','email']:
#                 _logger.info(" **we ain in not in email for next record is deleteing %s and model%s",record.id,updated_state_value.model_name)
#                 p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',record.id),('model','=',updated_state_value.model_name)])
#                 print(" ** not email before deleting: domain attache:record id: ", record.id, "model : ",updated_state_value.model_name)
#                 print(" ** not email before deleting: process manager record id is: ", p_record)
#                 # p_record.sudo().unlink()
#                 p_record.write({'active' : False})
#                 # p_record.save()
#             return 1
#         else:
#             _logger.info(" \n ******rule engine failed for record *****\n%s: and stage value is %s  ",model_obj,model_obj.x_o2b_stage )
#             print(":", model_obj)
#             model_obj.with_user(2).sudo().write({
#             # 'x_o2b_stage': 'decision_exception',
#             'x_done': True,
#             })
#             return 0
#     # advance rule engine end here
    
#     # domain parse method for odoo
#     def domain_parse(self,domain):
#         data_list = []
#         for record in domain:
#             if len(record) == 1:
#                 data_list.append((record))
#             if len(record)>1:
#                 data_list.append(tuple(record))
#         return data_list;
#     # end here

#     # fetch all decision rule from server and processed it
#     @api.model
#     def handle_decision_records(self,rec,next_obj):
#         _logger.info("handle decison_recordds process manger table data : %s",rec)
#         _logger.info("rec model : %s",rec.model)
#         print("rec current id: ",rec.record_id)
#         _logger.info("next object record: %s", str(next_obj))
#         _logger.info("next_obj.process_node_id %s",next_obj.process_node_id)
#         _logger.info("next_obj.stage_name %s",next_obj.stage_value)
#         _logger.info("next_obj.node_type %s",next_obj.node_type)
#         # ******calling middleware api to fetch deciion rules******
#         # try:
#         _logger.info("** we are in fetching node decision from middleware service")
#         url = 'http://192.168.1.26:3636/decision/fetch' 
#         url = 'http://122.160.26.224:3636/decision/fetch' 
#         headers = {
#         'Content-Type': 'application/json',
#         }
#         data = {
#         'key': 'o2b_technologies',
#         'process_id'    : next_obj.process_id,
#         'curr_id'       : next_obj.process_node_id,
#         'curr_name'     : next_obj.stage_name
#         }
#         _logger.info(" ** complete request body: %s ", data)
#         response = requests.post(url, json=data, headers=headers)
#         records = response.json().get('message',)
#         _logger.info("** fetch decision rule reponse %s", str(records))
#         if records != 'NOT_FOUND':
#             decision_status = []
#             for record in records:
#                 # print("single diceiosn records next name", record)
#                 _logger.info("\n decision  next name :%s ", record.get('next_name'))
#                 _logger.info("\n decision  next id: %s ", record.get('next_id'))
#                 _logger.info("\n decision  exception name :%s ", record.get('exception_name'))
#                 _logger.info("\n decision  next exception id: %s ", record.get('exception_id'))
#                 _logger.info("\ndecision  domain: %s ", record.get('domain'))
#                 _logger.info("\ndecision  domain parse: %s ", self.domain_parse(record.get('domain')))
#                 _logger.info("********end process records**************")
#                 # call upgraded decision rule method here
#                 record_acutal_condition = record.get('domain')
#                 record_parse_condition = self.domain_parse(record.get('domain'))
#                 record_next_name = record.get('next_name')
#                 record_next_id = record.get('domain')
#                 record_exception_name = record.get('exception_name')
#                 record_exception_id = record.get('exception_id')
#                 rule_engine_status = self.upgraded_rule_engine(rec,next_obj,record)
#                 decision_status.append(rule_engine_status)

#             _logger.info("** dicision_status %s", decision_status)
#             atleast_one_execution = 1 in decision_status
#             _logger.info(" ** check atleast_one_execution value : %s ",atleast_one_execution)
#             if  not atleast_one_execution:
#                 _logger.info(" all rule failded we are checking if there is any exception state in condition.")
#                 if record_exception_id:
#                     current_stage = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_exception_id)],limit=1)
#                     model_obj = self.env[rec.model].sudo().browse(int(rec.record_id))
#                     model_obj.with_user(2).sudo().write({
#                         'x_o2b_stage'   : current_stage.stage_value,
#                         'x_done'        : True,
#                     })
#             # except Exception as e:
#             #     _logger.info(" *** while connecting with api . there is some errro." + str(e))
       
        
#     # this method is calling on clicking done button via
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
#                 code = process.model_name.replace('.','_').lower()
#                 current_record_model.sudo().write({
#                     'x_done'            : False,
#                     'x_reference_no'    : self.env['ir.sequence'].next_by_code(code),
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

#     # Remark history save function call:
#     def remark_history(self,model,record_id,fields,process):
#         _logger.info("*** remark_history : %s", process)
#         _logger.info("*** remark_history: %s", model)
#         _logger.info("*** record id :  %s", record_id)
#         _logger.info("*** process activity_type:  %s", process.activity_type)
#         _logger.info("*** process activity name next name:  %s", process.next_stage)
#         if model:
#             model = model.strip()
#         if record_id:
#             record_id = int(record_id)
#         model_exist = self.env['ir.model'].sudo().search([('model','=',model)])
#         current_model = self.env[model].sudo().search([('id','=',record_id)])
#         _logger.info("*** current record: in remark history: %s ", current_model)
#         # current_record_field = self.env['ir.model.fields'].sudo().search(['&',('name','=','x_remark'),('model','=',model)])
#         current_record_field = self.env['ir.model.fields'].sudo().search(['&',('name','=','x_decision'),('model','=',model)])
#         _logger.info("***** current record : x_o2b_decision check %s ", current_record_field)
#         if current_model and current_record_field:
#             # _logger.info("***intert into remark table:%s ,%s:", current_model.x_remark,current_model.x_decision)
#             field = model.split('.')[-1]
#             _logger.info("**** filed in remak histroy:%s  " , field)
#             relation_field = 'x_o2b_' + field +'_in_remark_history'
#             _logger.info(" *** history remark table: %s ", relation_field)
#             if current_model.x_remark or current_model.x_decision:
#                 print(" YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY  remakr history  create_date", current_model.create_uid.id)
#                 print(" YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY  remakr history  write", current_model.write_uid.id)
#                 print(" YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY  remakr history current_model.logged_in_user.id",current_model.logged_in_user.id)
#                 current_step = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',current_model._name),('process_node_id','=',process.current_stage_id)],limit=1)

#                 remark_obj = self.env['o2b.process.modular.remark.history'].create({
#                     relation_field  : record_id,
#                     'decision'      : current_model.x_decision,
#                     'remark'        : current_model.x_remark,
#                     'current_stage' : current_step.stage_name,
#                     })
#                 print(" rmarkt table create uid befor",remark_obj.create_uid)
#                 print(" rmarkt table write uid before ",remark_obj.write_uid)
#                 current_uid = current_model.remark_user.id
#                 # if current_model.write_uid:
#                 #     if current_model.write_uid.id != 1:
#                 #         current_uid = current_model.write_uid.id
#                 #     else:
#                 #         current_uid = current_model.logged_in_user.id if current_model.create_uid.id == 1 else current_model.create_uid.id
#                 remark_obj.write({
#                      'remark_uid'   : current_uid if current_uid else 2,
#                     })
#                 print(" rmarkt table create uid after udpaet",remark_obj.create_uid)
#                 print(" rmarkt table write uid after",remark_obj.write_uid)
#                 print(" ********* current stage change " , current_model.x_o2b_stage)
#                 msg = None
#                 next_step_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',current_model._name),('process_node_id','=',process.next_stage_id)],limit=1)

#                 if next_step_obj.node_type not in ['decision']:
#                     _logger.info(" ** setting decsion blank next step is : %s ", next_step_obj.node_type)
#                     current_model.sudo().write({
#                         'x_remark'   : '',
#                         'x_decision' : '',
#                         })

#                     # if next_step_obj.node_type not in ['discard','reject','exception','end']:
#                     #     if next_step_obj.node_type =='email':
#                     #         msg = 'Process manager moved this record from email step'

#                     #     if next_step_obj.node_type =='email_verify':
#                     #         msg = 'Process manager moved this record from Email Verify step'

#                     #     if next_step_obj.node_type =='decision':
#                     #         msg = 'Process manager moved this record from Decision step'

#                     #     self.env['o2b.process.modular.remark.history'].sudo().create({
#                     #     relation_field  : record_id,
#                     #     'decision'      : current_model.x_decision,
#                     #     'remark'        : msg,
#                     #     'current_stage' : next_step_obj.stage_name
#                     #     })
      
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
#                 print(" ***************process next step : ", process.next_stage_id)
#                 if process:
#                     curr_id = process.current_stage_id
#                     cur_step = process.current_stage
#                     curr_type = process.activity_type
#                     next_id = process.next_stage_id
#                     next_step = process.next_stage
#                     _logger.info(" ** universal schedular next id is %s : ", next_id)
#                     if next_id:
#                         self.remark_history(rec.model,rec.record_id,None,process)
#                         next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',next_id)],limit=1)
#                         print(" *** next object value : ", next_obj.node_type)
#                         if next_obj.node_type not in ['decision','email','email_verify']:
#                             _logger.info(" ** in normal stage move and type is :: %s ",next_obj.node_type,)
#                             _logger.info(" ** in normal stage value is %s :",next_obj.stage_value,)
#                             cur_record_model.sudo().write({
#                                 'x_o2b_stage': next_obj.stage_value,
#                                 'x_done': True,
#                                 })
#                             # self.remark_history(rec.model,rec.record_id,None,process)
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
#                             # self.remark_history(rec.model,rec.record_id,None,process)
#                             self.handle_decision_records(rec,next_obj)
#                             #working santosh
#                             # decisions_nodes = self.env['o2b.process.modular.stage'].search([('model_name', '=', rec.model.strip()), ('activity_type', '=', 'decision')])
#                             # for recc in decisions_nodes:
#                             #     desision_records = self.env[rec.model].sudo().browse(record_id)
#                             #     current_stage = cur_record_model.x_o2b_stage
#                             #     model = desision_records
#                             #     record = desision_records
#                             #     records = desision_records
#                             #     self.env['o2b.process.modular'].action_test(model, record, records, desision_records, decisions_nodes,recc.current_stage)
#                             # self.remark_history(rec.model,rec.record_id,None,process)
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
                            
#                             # self.remark_history(rec.model,rec.record_id,None,process)
                            
#                             email_next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_mail.next_step_id)],limit=1)
#                             if email_next_obj.node_type not in ['decision']:
#                                 print(" ** after email this is simple step to forward simply type : ", email_next_obj.node_type)
#                                 cur_record_model.sudo().write({
#                                     'x_o2b_stage': next_step.stage_value,
#                                     'x_done': True,
#                                     })
#                                 # self.remark_history(rec.model,rec.record_id,None,process)
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
#                                 # call new decsion handling method
#                                 self.handle_decision_records(rec,email_next_obj)
#                                 # # call decsion making schedular
#                                 # decisions_nodes = self.env['o2b.process.modular.stage'].search([('model_name', '=', rec.model.strip()), ('activity_type', '=', 'decision')])
#                                 # for recc in decisions_nodes:
#                                 #     desision_records = self.env[rec.model].sudo().browse(record_id)
#                                 #     current_stage = cur_record_model.x_o2b_stage
#                                 #     model = desision_records
#                                 #     record = desision_records
#                                 #     records = desision_records
#                                 #     self.env['o2b.process.modular'].action_test(model, record, records, desision_records, decisions_nodes,recc.current_stage)
                                
#                                 # self.remark_history(rec.model,rec.record_id,None,process)
#                             else:
#                                 rec.write({'active' : False})
#                                 # rec.save()
#                                 # rec.sudo().unlink()

#                         if next_obj.node_type in['email_verify']:
#                             _logger.info(" ** we are in email_verified next id %s : ", rec.record_id)
#                             self.handle_email_verify(process,next_obj,rec.record_id)
#                             print(" next_objddddddddddd.", rec.current_id)
                           
#                             email_current_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model),('current_stage_id','=',next_obj.process_node_id)])
#                             email_verified_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',email_current_stage.next_stage_id)],limit=1)
#                             print(" &&&&&&&&&&&&&&&we are in email verified objeo; ", email_verified_obj)
#                             print(" &&&&&&&&&&&&&&&we are in email verified objeo; ", email_verified_obj.node_type)
#                             if email_verified_obj.node_type not in ['decision','email','email_verify']:
#                                 print(" ** after email this is simple step to forward simply type : ", email_verified_obj.node_type)
#                                 cur_record_model.sudo().write({
#                                     'x_o2b_stage': email_verified_obj.stage_value,
#                                     'x_done': True,
#                                     })
#                                 # self.remark_history(rec.model,rec.record_id,None,process)
#                             if email_verified_obj.node_type in['decision']:
#                                 print(" ** email verified next stage is decision ", email_verified_obj.node_type)
#                                 # create new record in email table
#                                 self.handle_decision_records(rec,email_verified_obj)
#                                 # self.remark_history(rec.model,rec.record_id,None,process)
#                             else:
#                                 rec.write({'active' : False})
                              
#                             if email_verified_obj.node_type in['email']:
#                                 print(" ******we are in type mail emailverified ====>email rec.current_id : ",rec.current_id )
#                                 email_current_id_obj = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model.strip()),('current_stage_id','=',rec.current_id)],limit=1)
#                                 print(" nextnext id :" ,email_current_id_obj.next_stage_id)
#                                 print(" current id :" ,email_current_id_obj.current_stage_id)
#                                 # create new record if email after email verify:
#                                 vals= {
#                                 'record_id'     : rec.record_id,
#                                 'model'   :     rec.model ,
#                                 'current_id'    : email_current_id_obj.next_stage_id,
#                                 }
#                                 p_manager_record = self.env['o2b.process.manager'].sudo().create(vals)
#                                 print(" new procdess redod xxxxxx", p_manager_record)
#                                 print(' previous ', rec.current_id, rec.id)
#                                 rec.write({'active':False})
#                             else:
#                                 rec.write({'active' : False})
                               
#                         _logger.info(" ** if next id false means end of stage %s ", next_id)
#                         cur_record_model.write({
#                             'x_done': True
#                             })
#         except Exception as e:
#             _logger.info(" ** process manager table %s ",str(e))
#             cur_record_model.write({
#                         'x_done': True
#                         })
#             pass                  

# # o2b mail sender service method
#     def _mail_sender(self):
#         try:
#             _logger.info("** we are in mail sender service:")
#             email_records = self.env['o2b.process.email'].sudo().search([('is_sent','=',False)])
#             for email_queue in email_records:
#                 mail_create_time = email_queue.create_date
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
#                         _logger.info("**** acutal email extact from node value() %s", email_queue.recipient)
#                         if email_queue.recipient:
#                             match = re.match(r'^[a-zA-Z0-9_]+', email_queue.recipient)
#                             if match:
#                                 result = match.group(0)
#                                 # _logger.info(" yes actual email is extract %s ",result)
#                                 if hasattr(record_model, result):
#                                     recipient = getattr(record_model, result)
#                                     # _logger.info("**email will send to :%s", recipient)
#                             else:
#                                 # _logger.info(" No actual email is extract %s ",result)
#                                 if hasattr(record_model, 'x_o2b_email'):
#                                     recipient = getattr(record_model, 'x_o2b_email')
#                         _logger.info("** acutual email address where email send : %s ",recipient)
#                     msg_body = email_queue.mail_body
#                     msg_subject = email_queue.mail_subject
#                     _logger.info(" trying to recepient : %s: for record id: %s ", recipient,str(email_queue))
                    
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
#                     model_record = self.env['ir.model'].sudo().search([('model','=',email_queue.model)],limit=1)
#                     _logger.info(" ** email model applied id found or not %s and model name %s  ", str(model_record),email_queue.model)
#                     # print(" recod model record_model.x_o2b_name ", record_model.x_o2b_name)
#                     # pattern = r'{{\s*object\.(\w+)\s*}}'
#                     pattern = r'{{\s*object\.(\w+(?:\.\w+)*)\s*}}'
#                     # Find all matches and create a list of tuples (object, field_name)
#                     matches = re.findall(pattern, msg_body)
#                     # Create a list of tuples (object, field_name)
#                     object_field_pairs = [('object', match) for match in matches]
#                     # replace {{object.
#                     msg_body =  msg_body.replace("{{object.","")
#                     print("after remving {{object.", msg_body)
#                     msg_body = msg_body.replace("}}"," ")
#                     print('after remving }}', msg_body)
#                     print(" ***** object_field_pairs ", object_field_pairs)
#                     for data in object_field_pairs:
#                         dynamic_obj,technical_field = data
#                         print(" **********dynamic_obj ", dynamic_obj)
#                         print(" **********technical_field ", technical_field)
#                         target_string = technical_field
#                         if hasattr(record_model, technical_field):
#                             field_value = getattr(record_model, technical_field)
#                             msg_body = msg_body.replace(technical_field,str(field_value))
#                             print(" ** compelte dynamic emai template: ", msg_body)
#                         elif '.' in technical_field:
#                             base_field, sub_field = technical_field.split('.', 1)
#                             _logger.info(" in relation fields base field : %s and subfiled :%s", str(base_field),str(sub_field))
#                             if hasattr(record_model, base_field):
#                                 parent_obj = getattr(record_model, base_field)
#                                 parent_obj = parent_obj[:1]
                                
#                                 _logger.info(" ** parent_obj %s", str(parent_obj))
#                                 _logger.info(" ** parent_obj %s", str(parent_obj._name))
                                
#                                 # further logic if we handle particular model name . 
#                                 # if parent_obj._name == 'res.partner':
#                                 #     sub_field = 'name'
#                                 # if parent_obj._name == 'res.users':
#                                 #     sub_field = 'login'
#                                 # further logic if we handle particular model name . 

#                                 if hasattr(parent_obj, sub_field):
#                                     child_obj = getattr(parent_obj, sub_field)
#                                     _logger.info(" ** child object : %s", child_obj)
#                                     msg_body = msg_body.replace(technical_field,str(child_obj))
#                                     _logger.info(' ** final msg_body in relational %s', msg_body)
#                     print(" all pais of oject ::::::::",object_field_pairs )
#                     context = {
#                         'object'    : record_model,  
#                         # 'x_o2b_name': record_model.x_o2b_name if record_model else '',
#                     }
#                     odoo_mail_template = self.env['mail.template'].search([('name', '=', 'oflow_email_template')], limit=1)
#                     if odoo_mail_template:
#                         _logger.info(" ** updating existing mail template ")
#                         # rendered_body_html = odoo_mail_template.body_html.render(context)
#                         rendered_body_html = odoo_mail_template.body_html

#                         # Prepare the email template dictionary to update it
#                         email_template = {
#                             'name'          : 'oflow_email_template',
#                             'model_id'      : model_record.id if model_record else 97,  
#                             'subject'       : msg_subject,
#                             'description'   : msg_subject,  
#                             'body_html'     : msg_body,  
#                             'email_from'    : 'info@oflowai.com',
#                             'use_default_to': False,
#                             'email_to'      : recipient,
#                         }
#                         odoo_mail_template.sudo().write(email_template)
#                     else:
#                         _logger.info(" ** creating new mail template ")
#                         # rendered_body_html = odoo_mail_template.body_html.render(context)
#                         rendered_body_html = odoo_mail_template.body_html

#                         # Create the email template
#                         email_template = {
#                             'name'          : 'oflow_email_template',
#                             'model_id'      : model_record.id if model_record else 97,
#                             'subject'       : msg_subject,
#                             'description'   : msg_subject,
#                             'body_html'     : msg_body,
#                             'email_from'    : 'info@oflowai.com',
#                             'use_default_to': False,
#                             'email_to'      : recipient,
#                         }
#                         odoo_mail_template = self.env['mail.template'].sudo().create(email_template)
#                     # Handle attachments
#                     attachment_tuples = [(4, attachment.id) for attachment in email_queue.attachment_ids]
#                     odoo_mail_template.attachment_ids = attachment_tuples
#                     time_count = 0
#                     data_format = 'minutes'
#                     # scheduled when email should trigger
#                     if not email_queue.mail_trigger.isdigit():
#                         time_count = scheduled_data['timeCount']
#                         if time_count:
#                             time_count = int(time_count)
#                         data_format = scheduled_data['timeFormat']
#                     else:
#                         time_count = int(email_queue.mail_trigger)

#                     if time_count > 0 :
#                         time_units = {
#                             'second'    : 1,
#                             'minutes'   : 60,
#                             'hours'     : 3600,
#                             'days'      : 86400,
#                             'weeks'     : 604800,
#                             'months'    : 2628000  
#                             }
#                         time_in_seconds = time_count * time_units[data_format]
#                         print("time in seconds ", time_in_seconds)
#                         current_time = datetime.now()
#                         mail_scheduled_time = mail_create_time
#                         try:
#                             future_time = mail_scheduled_time + timedelta(seconds=time_in_seconds)
#                             _logger.info("Current time %s:" ,str(current_time))
#                             _logger.info("future  time %s:" ,str(future_time))
                           
#                             # Compare current time with future time (if the current time has passed the future time)
#                             if current_time >= future_time:
#                                 _logger.info("Time condition met. email is sending")
#                                 mail_id = odoo_mail_template.sudo().with_context(context).send_mail(record_model.id, force_send=True)
#                                 email_queue.sudo().write({
#                                     'is_sent':True,
#                                     'active' :False
#                                     })
#                             else:
#                                 _logger.info("Time condition not met yet.")
#                         except ValueError as e:
#                             _logger.info("error while schedular the email %s", str(e))
#                     else:
#                         _logger.info(" email is schedulad immediate. count value is %s",str(time_count))
#                         mail_id = odoo_mail_template.sudo().with_context(context).send_mail(record_model.id, force_send=True)
#                         email_queue.sudo().write({
#                         'is_sent':True,
#                         'active' :False
#                         })
#                     # shedular email end here
#                     # Clean up attachments (clear the attachment relation)
#                     odoo_mail_template.attachment_ids = [(5, 0, 0)]          
#         except Exception as e:
#             _logger.info(" some erron in sending email :%s",str(e))

#     # o2b mail sender service method
#     def _fetch_attachment(self,record_mail,new_mail_record):
#         try:
#             _logger.info("** we are in fetching attachment from middleware service")
#             # call node fetch api to get attachents and update process email table
#             #for local
#             url = 'http://192.168.1.26:3636/email/fetch/attachment' 
#             # for internal
#             url = 'http://122.160.26.224:3636/email/fetch/attachment' 
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
#             _logger.info("=====Exception while fetching and updating email table template %s", str(error))
#             pass



# # ****************email verifiy that email is exist or ot***************************
#     @api.model
#     def handle_email_verify(self, cur_obj, next_obj, record_id):
#         _logger.info("Just validating email verify step cur_obj: %s", str(cur_obj))
#         _logger.info("Just validating email verify step main_obj: %s and record_id: %s", str(next_obj), str(record_id))
        
#         process_id = cur_obj.process_id
#         model = cur_obj.model_name
#         current_id = next_obj.process_node_id
#         print("********* Email verification process id:", process_id)
#         print("********* Email verification model:", model)
#         print("********* Email verification current stage id:", current_id)

#         # Search for the email verification object
#         email_verified_obj = self.env['o2b.process.modular.emailverified'].sudo().search([
#             ('process_id', '=', process_id),
#             ('current_id', '=', current_id)
#         ],limit=1)
        
#         email_list = None
#         if email_verified_obj:
#             try:
#                 # Safely parse the email list stored in the record
#                 email_list = ast.literal_eval(email_verified_obj.email_verify_list)
#             except (ValueError, SyntaxError) as e:
#                 _logger.error("Failed to parse email_verify_list. Error: %s", e)

#         if email_list:
#             # Fetch the target record model
#             record_model = self.env[model].sudo().browse(int(record_id))
#             print("Current record in model:", record_model)
#             for email in email_list:
#                 # Check if the field exists in the model
#                 if hasattr(record_model, email):
#                     field_value = getattr(record_model, email)
#                     print(f"Actual value for email {email}: {field_value}")
                    
#                     if field_value:
#                         # Proceed with email verification (e.g., call verify_email_exist function)
#                         print(f"Email check status for {email}: {field_value}")
#                         email_result = self.verify_email_exist(field_value)
#                         update_dict = {}
#                         print(" email result ", email_result)
#                         if email_result and email_result == True:
#                             update_dict[email+'_status'] = email_result
#                             record_model.write(update_dict)



#                     else:
#                         _logger.warning("Field value for %s is empty or None.", email)
#                 else:
#                     _logger.warning("Field %s does not exist in the model %s.", email, model)

# # ****************email verifiy that email is exist or ot***************************
#     # @api.model
#     # def verify_email_exist(self,email):

#     #     email_verified_status = False
#     #     format_verifty_status = False
#     #     dns_check_status  = False
#     #     _logger.info("*** in verify_email_exist : %s",email)
        
#     #     regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#     #     format_verifty_status = re.match(regex, email) is not None
#     #     domain = email.split('@')[1]
#     #     try:
#     #         mx_records = dns.resolver.resolve(domain, 'MX')
#     #         dns_check_status =  True if mx_records else False
#     #     except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
#     #         dns_check_status =  False

#     #     if dns_check_status and format_verifty_status:
#     #         email_verified_status = True
#     #         return email_verified_status
#     #     else:
#     #         return False
    
    
#     @api.model
#     def verify_email_exist(self,email):

#         email_verified_status = False
#         format_verifty_status = False
#         dns_check_status  = False
#         _logger.info("*** in verify_email_exist : %s",email)
        
#         regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
#         format_verifty_status = re.match(regex, email) is not None
#         # dns_check_status = validate_email(email,verify=True)
#         try:
#             dns_check_status = validate_email(email, check_deliverability=False)
#             print(" *** dns_check_status",dns_check_status)
#             email = dns_check_status.normalized

#         except EmailNotValidError as e:
#             print("email respose check staus ", str(e))

#         if dns_check_status and format_verifty_status:
#             email_verified_status = True
#             return email_verified_status
#         else:
#             return False



#     # schedualr for release after specefied time. here specefied time is 5 minutes **** start here
#     @api.model
#     def _global_lock_release_schedular(self):
#         SPECIFIED_TIME = 1
#         current_time = datetime.now()
#         lock_records= self.env['o2b.process.lock'].sudo().search([])
#         for record in lock_records:
#             _logger.info(" lock record id : %s  is processing to relase the record .", str(record))
#             if record.lock_date <=  current_time - timedelta(minutes=SPECIFIED_TIME):
#                 record.write({
#                     'active' : False
#                     })
#         # sening pending emails
#         # self.sudo()._mail_sender()
#         try:
#             self.sudo()._mail_sender()
#         except Exception as e:
#             _logger.info(" calling self.sudo()._mail_sender() %s ",str(e))

#     # schedualr for release after specefied time. here specefied time is 5 minutes **** end here

#     # schedualr for sending email which are pending in process email table**** start here
#     # @api.model
#     # def _global_lock_release_schedular(self):
#     #     self._mail_sender()
#     # # schedualr for sending email which are pending in process email table**** end here


#     # create process manager record :for accepting request from json api  or web form api
#     def process_manager_insert(self,process_id,record_id,request_type):
#         _logger.info("** process manager insert for webform and json api: %s ",record_id)
#         print(" process id : ", process_id)
#         print(" process record_id : ", record_id)
#         print(" process request type : ", request_type)

#         process_stage = None
#         if request_type == 'json_api':
#             process_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('process_id','=',process_id.strip()),('activity_type','=','start')],limit=1)
#         if request_type == 'webform':
#             process_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('process_id','=',process_id.strip()),('activity_type','=','webform')],limit=1)

#         print(" insert in process mangaer dta ", process_stage)
#         if process_stage:
#             print(" process_stage",process_stage)
#             p_manager_record = self.env['o2b.process.manager'].sudo().search(['&',('model','=',process_stage.model_name.strip()),('record_id','=',record_id)])
#             if p_manager_record:
#                 _logger.info(" ** process record model%s: and current step %s  ", p_manager_record.model,p_manager_record.current_id)
#                 # update
#                 p_manager_record.sudo().write({
#                     'record_id'     : record_id ,
#                     'model'         : process_stage.model_name.strip() ,
#                     'current_id'    : process_stage.current_stage_id ,
#                     })
#             else:
#                 # create
#                 p_manager_record.sudo().create({
#                     'record_id'     : record_id ,
#                     'model'         : process_stage.model_name.strip() ,
#                     'current_id'    : process_stage.current_stage_id ,
#                     })
















# # ****************code for old decsion state handling start here***************************8
#     # @api.model
#     # def action_test(self,model,record,records,decision_records,all_decision,current_decision):
#     #     _logger.info("decision records : %s",decision_records)
#     #     _logger.info("all_decision records : %s",len(all_decision))
#     #     print("***************action test *************** : ",current_decision)
#     #     print("model : ",model)
#     #     print("record : ",record)
#     #     print("records : ",records)
#     #     print("decision_records ",decision_records)
#     #     print("all_decision ",all_decision)
#     #     print("current_decision ",current_decision)

#     #     if not decision_records:
#     #         _logger.info("no record found to apply decision rule.")
#     #     else:
#     #         for rec in decision_records:
#     #             record_current_stage = rec.x_o2b_stage
#     #             _logger.info("record found and current stage is :%s  ", record_current_stage)
#     #             self.sudo().schedular_decision_maker(rec,model,model._name,all_decision,current_decision)

#     # def schedular_decision_maker(self,record,model,model_name,all_decision,current_decision):
#     #     _logger.info("********************schedular_decision_maker: ********************** %s  and current record decision %s", record,  current_decision)
#     #     _logger.info("Model name : %s ", model)
#     #     # print("model name ", model_name)
#     #     # print("type of modle name:", type(model_name))
#     #     process = self.env['o2b.process.modular'].sudo().search([('model_name','=',model_name.strip())])
#     #     print(" all desision ids ==============: ", process.process_stages_decision_ids)
#     #     print(" all desision stage  ==============: ", process.process_state_ids)
#     #     for reccc in process.process_stages_decision_ids:
#     #         _logger.info("reccc ::::::::: %s", reccc.decision_name)
#     #     # decision_line = process.process_stages_decision_ids if process.process_stages_decision_ids else None
#     #     decision_line = process.process_stages_decision_ids.filtered(lambda r: r.decision_name == current_decision)
#     #     print("fileter record decision lines: ", decision_line)
#     #     # decision_line = process.process_stages_decision_ids.filtered(lambda s: s.decision_name == current_decision) if process.process_stages_decision_ids else None
#     #     if decision_line and decision_line[0].decision_name == current_decision:
#     #         sequence = 0
#     #         _logger.info("yes decision line availabe%s ", decision_line)
#     #         for rec in decision_line:
#     #             _logger.info("store data from decisin table  pre stage: %s", rec.previous_stage )
#     #             _logger.info("decisin table  next stage: %s", rec.next_stage )
#     #             # print("decisin table  domain: ", rec.domain )
#     #             print("decisin table  parse domain: ", rec.odoo_domain )
#     #             # print("decisin table  parse type odoo_domain : ", type(rec.odoo_domain))
#     #             # print("decisin table  parse type domain : ", type(rec.domain))
#     #             result = self.sudo().adnvace_rule_engine(rec,rec.domain,rec.odoo_domain,record,sequence,process.process_state_ids,model_name)
#     #             sequence = sequence + 1
#     #             _logger.info('result of decision rule engine:%s',result)
#     #             if result[0] == True:
#     #                 _logger.info("first time stage changed...")
#     #                 return;
#     #         _logger.info("if not rule apply then stage change automatically to decesion exception stage: %s", record)
#     #         process_id = ''
#     #         process_name =''
#     #         decision_list = []
#     #         if all_decision:
#     #             for data in all_decision:
#     #                 decision_list.append(data.current_stage)
#     #                 process_name = data.process_name
#     #                 process_id= data.process_id
#     #         print("data list : ::::", decision_list)

#     #         if record.x_o2b_stage in  decision_list:
#     #             _logger.info("****** exception states ")
#     #             process_decision = self.env['o2b.process.modular.stage.decision'].sudo().search([('process_name','=',process_name),('decision_name','=', record.x_o2b_stage)], limit=1)
#     #             print("which decision excetion is executed with next step: name ", process_decision.exception_state)
#     #             # print("which decision excetion is executed with next step: value", process_decision.exception_state.replace(' ','_').lower())
#     #             print("current record: ", record)
#     #             print("current record sh iv : ", process_decision.exception_state)
#     #             print("current record sh iv : ", type(process_decision.exception_state))
#     #             if process_decision.exception_state and process_decision.exception_state != 'null':
#     #                 print("**goiing in exception state: ")
#     #                 record.with_user(2).sudo().write({
#     #                 'x_o2b_stage': process_decision.exception_state.replace(' ','_').lower(),
#     #                 'x_done': True,
#     #                 })
#     #             else:
#     #                 _logger.info("** exception state without exception stage defined.")
#     #                 # record.with_user(2).sudo().write({
#     #                 #     'x_o2b_stage': process_decision.previous_stage.replace(' ','_').lower(),
#     #                 #     'x_done': True,
#     #                 #     })

#     # # write code for advance rule engine start here
#     # def adnvace_rule_engine(self,rec,domain,odoo_domain, model,sequence,process,model_name):
#     #     _logger.info("**rule engine and process decision table%s", rec)
#     #     _logger.info(" **rule engine model name : %s ", model_name)
#     #     _logger.info(" **rule engile process statusbar table: %s ", process)
#     #     print("odoooooooooooooooooooo_domain: ", odoo_domain ,'type of descision rule: ', type(odoo_domain))
#     #     dummy_domain = odoo_domain.replace(", '&',",",")
#     #     print("dummy domain: ",dummy_domain, "count of or ", dummy_domain.count('|'))
#     #     or_count =  dummy_domain.count('|')
#     #     dummy_domain = dummy_domain.replace(", '|',"," ,")
#     #     or_data = '['
#     #     if or_count:
#     #         for  i in range(or_count):
#     #             or_data = or_data + "'|',"
#     #     dummy_domain = dummy_domain.replace('[', or_data)
#     #     dummy_domain =  ast.literal_eval(dummy_domain)
#     #     dummy_domain.append(('id', '=', model.id))
#     #     print("final dummy_domain :", dummy_domain, "type of dummy domain : ", type(dummy_domain))

#     #     actual_list = ast.literal_eval(odoo_domain)
#     #     actual_list.append(('id', '=', model.id))
#     #     print("type of decesion rule : : " ,type(actual_list))
#     #     print("value of actual list  : : " ,actual_list)
#     #     model_obj = model
#     #     # print("model object is :", model_obj)
#     #     print("model object is********* :", model,model_obj)
#     #     dynamic_sequence = sequence
#     #     record = None
#     #     try:
#     #         record = model_obj.search(actual_list)
#     #         if not record:
#     #             record = model_obj.search(dummy_domain)
#     #             _logger.info("decision  record found via dummy domian  : %s", record)
#     #         _logger.info("decesion record found real domian   : %s", record)
#     #     except Exception as e:
#     #         _logger.info("except in odoo domain : while searching record: %s", str(e))
#     #     update_stage_name = rec.next_stage
#     #     update_stage_value = rec.next_stage.replace(' ','_').lower()
#     #     _logger.info("***** process statusbar table rec object: %s ",rec )
#     #     _logger.info("***** process statusbar table next step name: %s ",update_stage_name )
#     #     _logger.info("***** process statusbar table next step value  %s ",update_stage_value )
        
#     #     # before fetch via node id: 
#     #     # updated_state_value = process.search([('stage_name','=',update_stage_name)],limit=1)
#     #     print(" xxxxxxxxxxxxxxxxx.modelname; ",model_name)
#     #     updated_state_value = process.search([('process_node_id','=',rec.next_stage_id),('model_name','=',model_name)],limit=1)
#     #     _logger.info("*** finding current stage in statusbar table %s %s:",process,updated_state_value)
#     #     _logger.info("**** actucal value in statusbar table %s and %s",updated_state_value.stage_name,updated_state_value.stage_value)
#     #     current_remark_field = self.env['ir.model.fields'].sudo().search(['&',('name','=','x_remark'),('model','=',model_name)])
#     #     _logger.info(" ** model have remark field or not: %s ", str(current_remark_field))
#     #     if record and updated_state_value :
#     #         for data in record:
#     #             _logger.info("updated records:1199 %s and stage is: %s  stage is : ", data,update_stage_value)
#     #             if current_remark_field:
#     #                 data.sudo().write({
#     #                 'x_o2b_stage': updated_state_value.stage_value,
#     #                 'x_remark'   : '',
#     #                 'x_decision' : '',
#     #                 'x_done': True,
#     #                 })

#     #             else:
#     #                 data.sudo().write({
#     #                 'x_o2b_stage': updated_state_value.stage_value,
#     #                 'x_done': True,
#     #                 })
#     #             # creating new record in process manager table if next step is email after decesion making
#     #             if updated_state_value.node_type == 'email':
#     #                 print("fdddddddddddddddddd object upe", updated_state_value)
#     #                 print("fdddddddddddddddddd tupe", updated_state_value.node_type)
#     #                 print("fdddddddddddddddddd nod id", updated_state_value.process_node_id)
#     #                 print("fdddddddddddddddddd recod ", updated_state_value.node_type)
#     #                 print("fdddddddddddddddddd model nan", updated_state_value.model_name)
#     #                 vals= {
#     #                     'record_id'     : data.id,
#     #                     'model_stage'   : data.x_o2b_stage ,
#     #                     'current_id'    : updated_state_value.process_node_id,
#     #                     'model'         : updated_state_value.model_name ,
#     #                     'current_name'  : updated_state_value.stage_name ,
#     #                     # 'next_id'       : p_stage.next_stage_id ,
#     #                     # 'next_name'     : p_stage.next_stage ,
#     #                 }
#     #                 # rec.write(vals)
#     #                 print(" *******************next tupe is email with snatosh ")
#     #                 p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',data.id),('model','=',updated_state_value.model_name)])
#     #                 print(" ** email curent valuse : process manager record id is: ", p_record.current_id , p_record.model)
#     #                 print(" ** email before write value: domain attache:record for next value : ", data.id, "model : ",updated_state_value.model_name)
#     #                 print(" *** email next id after decision: ", updated_state_value.process_node_id)
#     #                 if not p_record:
#     #                     self.env['o2b.process.manager'].create(vals)
#     #                 else:
#     #                     p_record.write(vals)
#     #                 print(" ** email before write : process manager record id is: ", p_record.current_id , p_record.model)
#     #                 # self.process_manager_crud(updated_state_value.model_name, p_record.id,updated_state_value.process_node_id)
#     #                 record_mail = self.env['o2b.process.modular.email'].search([('model_name','=',p_record.model),('current_node_id','=', updated_state_value.process_node_id)],limit=1)
#     #                 # create record in mail template:
#     #                 new_mail_record = self.env['o2b.process.email'].sudo().create({
#     #                             'record_id'     : p_record.record_id,
#     #                             'model'         : p_record.model,
#     #                             'current_id'    : p_record.current_id,
#     #                             'next_id'       : record_mail.next_step_id,
#     #                             'recipient'     : record_mail.recipient ,
#     #                             'mail_subject'  : record_mail.mail_subject ,
#     #                             'mail_body'     : record_mail.mail_body ,
#     #                             # 'create_date'   : record_mail.next_stage_id ,
#     #                             # 'mail_send_date': record_mail.next_stage_id ,
#     #                             # 'attachment_ids': record_mail.next_stage_id ,
#     #                             'mail_count'    : record_mail.mail_limit ,
#     #                             'is_active'     : True ,
#     #                             'is_sent'       : False ,
#     #                             'mail_trigger'  : record_mail.mail_trigger ,
#     #                             })
#     #                 # call fetch attachment and update email table record
#     #                 self._fetch_attachment(record_mail,new_mail_record)
                    
#     #             if updated_state_value.node_type != 'email':
#     #                 _logger.info(" **we ain in not in email for next record is deleteing")
#     #                 p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',data.id),('model','=',updated_state_value.model_name)])
#     #                 print(" ** not email before deleting: domain attache:record id: ", data.id, "model : ",updated_state_value.model_name)
#     #                 print(" ** not email before deleting: process manager record id is: ", p_record)
#     #                 # p_record.sudo().unlink()
#     #                 p_record.write({'active' : False})
#     #                 # p_record.save()

#     #         return [True , sequence]
#     #     else:
#     #         print("model  decisin exception of current data:", model)
#     #         model.with_user(2).sudo().write({
#     #         # 'x_o2b_stage': 'decision_exception',
#     #         'x_done': True,
#     #         })
#     #         return [False , None]
#     # # advance rule engine end here
#     # # ********************************code for old decision stage handling end here***************************