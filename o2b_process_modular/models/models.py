import time
from odoo import models, fields,api,_,os
from odoo.exceptions import ValidationError, UserError
import ast
import random
import requests
import base64
import logging
import re
import dns.resolver
from datetime import datetime, date,timedelta
import json
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
# from email_validator import validate_email, EmailNotValidError

_logger = logging.getLogger(__name__)


class O2bHandleEmailTemplate(models.Model):
    _name = 'o2b.send.email.template'
    _description = 'O2b Send Email template'

    process_id = fields.Char(string='Process Id')
    process_name = fields.Char(string='Process Id')
    model = fields.Char(string='Model')
    node_id = fields.Char(string='Node Id')
    node_name = fields.Char(string='Node Name')
    template_name = fields.Char(string='Template name')
    template_id = fields.Char(string='Template id')
    active = fields.Boolean(string = 'Active',default =True)
    data = fields.Char(string="Email data")
    send_email_lines = fields.Many2one('o2b.process.modular', string='O2b Send Email Lines', ondelete='cascade',invisible=1)



# ****Todo and documents models
class o2bTodos(models.Model):
    _name = 'o2b.todos'
    _description = 'O2b Todo Data'

    todo_name = fields.Char(string='Todo name')
    todo_description = fields.Char(string='Todo description')
    active = fields.Boolean(string = 'Active',default =True)

class o2bDocuments(models.Model):
    _name = 'o2b.documents'
    _description = 'O2b documents Data'

    doc_name = fields.Char(string='Todo name')
    doc_description = fields.Char(string='Todo description')
    active = fields.Boolean(string = 'Active',default =True)
    file = fields.Binary(string="File", attachment=True)
    file_name = fields.Char(string="File Name")
    

# ****Todo documents models

class o2bProcessLock(models.Model):
    _name = 'o2b.process.lock'
    _description = 'O2b Process modular lock data'

    record_id = fields.Char(string='Record ID')
    model = fields.Char(string='Model')
    active = fields.Boolean(string = 'Active',default =True)
    user_id = fields.Char(string='user ID')
    lock_date = fields.Datetime(string='Record Lock Date', default=fields.Datetime.now)
    release_date= fields.Datetime(string='Release Date', default=fields.Datetime.now)


class o2bProcessModularStageEmailVerified(models.Model):
    _name = 'o2b.process.modular.emailverified'
    _description = 'O2b Process Modular Email Verified'
    process_id = fields.Char()
    process_name = fields.Char()
    email_verified_line = fields.Many2one('o2b.process.modular', string='O2b Proces Email Verified', ondelete='cascade',invisible=1)
    current_stage = fields.Char()
    current_id = fields.Char()
    email_verify_list = fields.Char(string = 'Email list')
   

class o2bProcessEmail(models.Model):
    _name = 'o2b.process.email'
    _description = 'O2b Process email'

    record_id = fields.Char()
    model = fields.Char()
    current_id = fields.Char(string="Current ID")
    next_id = fields.Char(string = 'Next Id')
    recipient = fields.Char(string='Email to')
    mail_subject = fields.Char(string='Mail Subject')
    mail_body = fields.Char(string=' Body')
    create_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)
    mail_send_date = fields.Datetime(string='Send Date', default=fields.Datetime.now)
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    mail_count = fields.Char(string = 'Mail limit')
    is_active = fields.Boolean(string = 'Status', default =True)
    is_sent = fields.Boolean(string = 'Mail sent'  , default = False)
    mail_trigger = fields.Char(string = 'Mail trigger')
    active = fields.Boolean(string = 'Active',default =True)


class o2bProcessManagerTable(models.Model):
    _name = 'o2b.process.manager'
    _description = 'O2b Process Modular'

    record_id = fields.Char(string='Record ID')
    model = fields.Char(string='Model')
    model_stage = fields.Char(string='Model Stage')
    prev_id = fields.Char(string='Previous ID')
    pre_name = fields.Char(string='Previous Name')
    pre_type = fields.Char(string='Previous Type')
    current_id = fields.Char(string='Current ID')
    current_name = fields.Char(string='Current Name')
    current_type = fields.Char(string='Current Type')
    next_id = fields.Char(string='Next ID')
    next_name = fields.Char(string='Next Name')
    next_type = fields.Char(string='Next Type')
    record_lock = fields.Boolean(string='Record Lock', default=False)
    active = fields.Boolean(string = 'Active',default =True)

   

class o2bProcessModularEmail(models.Model):
    _name = 'o2b.process.modular.email'
    _description = 'O2b Process Modular email'

    process_id = fields.Char()
    process_name = fields.Char()
    model_name = fields.Char()
    process_email_line = fields.Many2one('o2b.process.modular', string='O2b Proces Email', ondelete='cascade',invisible=1)
    prev_step = fields.Char(string="Previous step")
    next_step = fields.Char(string = 'Next step')
    next_step_id = fields.Char(string = 'Next Id')
    current_step = fields.Char(string='current step')
    current_node_id = fields.Char(string='Current Id')
    recipient = fields.Char(string='Email to')
    mail_subject = fields.Char(string='Mail Subject')
    mail_body = fields.Char(string=' Body')
    template_id = fields.Char(string='Template Id')
    mail_trigger = fields.Char(string='Mail trigger')
    mail_limit = fields.Char(string='Mail limit')


class o2bProcessModularFieldMethod(models.Model):
    _name = 'o2b.process.modular.field.method'
    _description = 'O2b Process Modular Field method'

    process_id = fields.Char()
    process_name = fields.Char()
    model_name = fields.Char()
    field_name = fields.Char()
    field_label = fields.Char()
    field_id = fields.Char()
    field_type = fields.Char()
    field_method = fields.Char()
    is_required = fields.Boolean(string = 'Required', default=False)
    activity_name = fields.Char()
    activity_type = fields.Char()
    form_id = fields.Char(string = 'Form Id')
    process_field_line = fields.Many2one('o2b.process.modular', string ='Process Fields', ondelete='cascade',invisible=1)
    default_value = fields.Char(string = 'Default Value')
    set_unset_value = fields.Char(string = 'Set Value')
    is_todo_field = fields.Boolean(string = 'Is Todo', default=False)
    is_document_field = fields.Boolean(string = 'Is doc', default=False)



class o2bProcessModularView(models.Model):
    _name = 'o2b.process.modular.view'
    _description = 'O2b Process Modular view '

    process_id = fields.Char()
    process_name = fields.Char()
    model_name = fields.Char()
    activity_name = fields.Char()
    view_id = fields.Char(string ='View Id')
    view_name = fields.Char(string ='Name')
    view_type = fields.Char(string = 'Type')
    view_data = fields.Char(string ='Data')
    activity_type = fields.Char(string = 'Type')
    node_id = fields.Char(string = 'Node Id')
    process_views = fields.Many2one('o2b.process.modular', string='O2b Process group', ondelete='cascade',invisible=1)

class o2bProcessModularAction(models.Model):
    _name = 'o2b.process.modular.action'
    _description = 'O2b Process Modular Actions'

    process_id = fields.Char()
    process_name = fields.Char()
    model_name = fields.Char()
    activity_name = fields.Char()
    action_id = fields.Char(string ='Action Id')
    action_name = fields.Char(string ='Name')
    domain = fields.Char(string ='Domain')
    activity_type = fields.Char(string = 'Type')
    context = fields.Char(string = 'Context')
    node_id = fields.Char(string = 'Node Id')
    process_actions = fields.Many2one('o2b.process.modular', string='O2b Process group', ondelete='cascade',invisible=1)



class o2bProcessModularMenuGroup(models.Model):
    _name = 'o2b.process.modular.group'
    _description = 'O2b Process Modular group '

    process_id = fields.Char()
    process_name = fields.Char()
    model_name = fields.Char()
    activity_name = fields.Char()
    group = fields.Char(string ='Group')
    process_groups = fields.Many2one('o2b.process.modular', string='O2b Process group', ondelete='cascade',invisible=1)
    activity_type = fields.Char()
    node_id = fields.Char(string = 'Node Id')
    action_id = fields.Char(string = 'Action Id')
    menu_id = fields.Char(string ='Menu Id')
    parent_id = fields.Char(string ='Parrent Id')
    # status = fields.Boolean(string = 'Active Status' , default=False)
    # prev_menu_name = fields.Char(string = 'Prev Name')
    # curr_menu_name = fields.Char(string = 'Curr Name')
    # prev_menu_id = fields.Char(string = 'Pre Menu id')
    # count = fields.Integer(string = 'Count', default=0)

class o2bProcessModularMenu(models.Model):
    _name = 'o2b.process.modular.menu'
    _description = 'O2b Process Modular Menu '

    process_id = fields.Char()
    process_name = fields.Char()
    model_name = fields.Char()
    menu_name = fields.Char()
    menu_id = fields.Char(string ='Menu Id')
    parent_id = fields.Char(string ='Parrent Id')
    node_id = fields.Char(string = 'Node Id')
    action_id = fields.Char(string = 'Action Id')
    activity_type = fields.Char()
    menu_type = fields.Char(string = 'Menu')
    status = fields.Boolean(string = 'Active Status' , default=True)
    pre_menu_id = fields.Char(string = 'Prev id')
    pre_parent_menu_id = fields.Char(string = 'Pre Parrent id')
    count = fields.Integer(string = 'Count', default=0)
    process_menus = fields.Many2one('o2b.process.modular', string='O2b Process menu', ondelete='cascade',invisible=1)


class o2bProcessModularRemarkHistory(models.Model):
    _name = 'o2b.process.modular.remark.history'
    _description = 'O2b Process Modular Remark History'

    serial_id = fields.Char(string ="Serial No")
    remark = fields.Char(string = 'Remarks')
    decision = fields.Char(string='Decision')
    current_stage = fields.Char(string='Current Stage')
    remark_uid = fields.Many2one('res.users', string="User", default=lambda self: self.env.user.id)
    
  
class o2bProcessModularStatusBar(models.Model):
    _name = 'o2b.process.modular.statusbar'
    _description = 'O2b Process Modular Stage Statusbar'

    process_id = fields.Char()
    process_name = fields.Char()
    model_name = fields.Char()
    process_stage_line = fields.Many2one('o2b.process.modular', string='Process Status Bar', ondelete='cascade',invisible=1)
    # process_stage_name = fields.Char(string = 'Stage Name')
    process_node_id= fields.Char(string = 'Process Node Id')
    stage_name = fields.Char(string = 'Stage Name')
    stage_value = fields.Char(string = 'Stage Value')
    node_type = fields.Char(string = 'Stage Type')
    set_unset = fields.Json(string="Set/Unset")
  
class o2bProcessModularStageDecesion(models.Model):
    _name = 'o2b.process.modular.stage.decision'
    _description = 'O2b Process Modular stages decision'
    process_id = fields.Char()
    process_name = fields.Char()
    process_decision_line = fields.Many2one('o2b.process.modular', string='O2b Proces decision', ondelete='cascade',invisible=1)
    o2b_sequence = fields.Char()
    o2b_operand = fields.Char()
    o2b_operator = fields.Char()
    o2b_value= fields.Char()
    previous_id = fields.Char()
    previous_stage = fields.Char()
    next_stage = fields.Char()
    current_stage_id = fields.Char()
    next_stage_id = fields.Char()
    domain = fields.Char(string='Domain')
    decision_name = fields.Char(string='Decision State')
    decision_id = fields.Char()
    exception_state = fields.Char(string='Exception State')
    exception_state_id = fields.Char(string='Exception Id')
    odoo_domain = fields.Char(string=' Parse Domain')


# modal class for process store process stages
class o2bProcessModularStage(models.Model):
    _name = 'o2b.process.modular.stage'
    _description = 'O2b Process Modular stages'
    process_id = fields.Char()
    activity_name = fields.Char()
    model_name = fields.Char()
    previous_stage = fields.Char()
    previous_stage_id = fields.Char()
    current_stage = fields.Char()
    current_stage_id = fields.Char()
    next_stage = fields.Char()
    next_stage_id = fields.Char()
    process_name = fields.Char()
    python_code = fields.Text(string='Python Code', default=False)
    process_stages = fields.Many2one('o2b.process.modular', string='O2b Process', ondelete='cascade',invisible=1)
    activity_type = fields.Char()


class o2bProcessModular(models.Model):
    _name = 'o2b.process.modular'
    _description = 'O2b Process Modular'
    _rec_name = 'process_name'

    #request field
    current_user = fields.Many2one('res.users', string='Current User', default=lambda self: self.env.user.id)
    process_id = fields.Char()
    model_detail = fields.Char()
    model_name = fields.Char()
    fields_data = fields.Char()
    menu_data = fields.Char()
    action_data = fields.Char()
    access_right_data = fields.Char()
    user_name = fields.Char()
    user_request = fields.Char()
    button_data = fields.Char()
    registry_status = fields.Boolean('Registry Status', default=True)
    #internal user field
    activity_name = fields.Char()
    previous_stage = fields.Char()
    current_stage = fields.Char()
    next_stage = fields.Char()
    process_name = fields.Char()
    process_menu_name_list = fields.Char()
    process_menu_node_list = fields.Char()
    process_temp_url = fields.Char()
    process_stages_ids = fields.One2many('o2b.process.modular.stage', 'process_stages', string='Process Stage ID')
    process_stages_decision_ids = fields.One2many('o2b.process.modular.stage.decision', 'process_decision_line', string='Process Decision ID')
    process_stages_field_ids = fields.One2many('o2b.process.modular.field.method', 'process_field_line', string='Stage Field ID',)
    process_state_ids = fields.One2many('o2b.process.modular.statusbar', 'process_stage_line', string='Field ID')
    process_group_ids = fields.One2many('o2b.process.modular.group', 'process_groups', string='Group Ids')
    process_menu_ids = fields.One2many('o2b.process.modular.menu', 'process_menus', string='menu Ids')
    process_view_ids = fields.One2many('o2b.process.modular.view', 'process_views', string='View Ids')
    process_action_ids = fields.One2many('o2b.process.modular.action', 'process_actions', string='Action Ids')
    process_email_ids = fields.One2many('o2b.process.modular.email', 'process_email_line', string='Email Ids')
    process_email_verified_ids = fields.One2many('o2b.process.modular.emailverified', 'email_verified_line', string='Email verified Ids')
    basic_start_template = fields.Text(string='XML Content', default=''' ''')
    auto_process_api_status = fields.Boolean('Json API next step status', default=False)
    auto_process_webform_status = fields.Boolean('Web form next step status', default=False)
    client_rule_engine_enable = fields.Boolean('Client Rule Engine Status', default=False)
    send_email_ids = fields.One2many('o2b.send.email.template', 'send_email_lines', string='Send Email Ids')



    @api.model
    def list_view_admin_data_process(self,count,objs,model,node_id,uid,o2b_module):
        # print(" total count : ", count)
        # print(" total objs : ", objs)
        # print(" total model : ", model)
        # print(" total node_id : ", node_id)
        # print(" total uid : ", uid)
        # print(" total o2b_module : ", o2b_module)
        if node_id and o2b_module == 'yes':
            for rec in objs:
                if rec:
                    obj = self.env[model].sudo().browse(int(rec))
                    self.admin_panel(obj,node_id)
        return True;

    @api.model
    def update_admin_panel(self, obj):
        if obj:
            print(" ** we are in update_admin_panel : ", obj)
            total_work_tat_diff = fields.Datetime.now() - obj.total_tat_datetime
            total_tat_second = total_work_tat_diff.total_seconds()
            previous_tat = obj.total_tat_in_seconds
            total_tat_in_seconds = int(float(previous_tat)) + total_tat_second
            # set preivoust time
            
            obj.sudo().write({
                'arrival_date_time': fields.Datetime.now(), 
                'pending_since': fields.Datetime.from_string(fields.Datetime.now()).date(),
                'work_step_tat': self.time_calculator(0.1),
                'total_tat_datetime': fields.Datetime.now(),  
                'total_tat_in_seconds': total_tat_in_seconds ,       
                })
            time.sleep(0.1)
            obj.sudo().write({
                'total_tat': self.time_calculator(total_tat_in_seconds),       
            })

    @api.model
    def admin_panel(self,obj,node_id):
        if obj:
            # print(" ** we are in admin panel data : ",obj)
            # print(" *** data prinitng arival: ", obj.arrival_date_time)
            # print(" *** data prinitng pending_since_test: ", obj.pending_since)
            # print(" *** data prinitng work_step_tat_test: ", obj.work_step_tat)
            # print(" *** data prinitng total_tat_test: ", obj.total_tat)
            # print(" *** data prinitng total_tat_datetime: ", obj.total_tat_datetime)
            stage = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',obj._name),('process_node_id','=',node_id)],limit=1)
            if stage.node_type not in [ "end", "discard", "exception", "reject"]:
                pending_since_date_only = fields.Datetime.from_string(obj.arrival_date_time).date()
                # print(" pending since date only ", pending_since_date_only)
                work_tat_diff = fields.Datetime.now() - obj.arrival_date_time
                work_tat_seconds = work_tat_diff.total_seconds()
                work_step_tat = self.time_calculator(work_tat_seconds)

                total_work_tat_diff = fields.Datetime.now() - obj.total_tat_datetime
                previous_tat = obj.total_tat_in_seconds
                # print(" previous time in seconds ", previous_tat)
                total_tat_second = total_work_tat_diff.total_seconds()
                total_tat_second = int(float(previous_tat)) + total_tat_second
                total_tat = self.time_calculator(total_tat_second)
                # print("********** total_tat", total_tat)
                # print("********** work_step_tat", work_step_tat)
                obj.sudo().write({
                    'pending_since' : pending_since_date_only,
                    'work_step_tat' : work_step_tat,
                    'total_tat'     : total_tat,
                    })

    @api.model
    def time_calculator(self,total_seconds):
        delta_seconds = total_seconds
        days = int(delta_seconds // 86400)
        hours = int((delta_seconds % 86400) // 3600)
        minutes = int((delta_seconds % 3600) // 60)
        seconds = int(delta_seconds % 60)
        date_time_second = f"{days} days, {int(hours)} hours, {int(minutes)} minutes"
        return date_time_second

    @api.model
    def dynamic_field_xml(self,model, node_id,action_type,view_content):
        form_heading = 'Todos Form'
        if action_type =='todos':
            records = self.env['o2b.process.modular.field.method'].sudo().search([('model_name', '=',model),('form_id','=',node_id),('is_todo_field','=',True)])
            field_content = ""
            for rec in records:
                required_start_tag = '<group>'
                required_end_tag = '</group>'
                if rec.is_required:
                    required_start_tag = '<group class="requiredField">'

                lines = '<field name="'+ rec.field_name + '" string="' +rec.field_label+ '"/> \n'
                newline  = required_start_tag + lines + required_end_tag
                field_content = field_content + '<group col="1">' + newline + '</group>'

            start_tag = '<sheet>'
            end_tag = '</sheet>'
            mid_content =' <h1><center>Todos Form</center></h1>'

            field_content = start_tag + mid_content +'<group col="1">' + field_content + '</group>' +end_tag
            new_view = self.update_xml_content(view_content,start_tag,end_tag,field_content)
            # new_view = new_view.replace('Document Form',form_heading)
            return new_view
        
        if action_type =='documents':
            form_heading = 'Document Form'
            records = self.env['o2b.process.modular.field.method'].sudo().search([('model_name', '=',model),('form_id','=',node_id),('is_document_field','=',True)])
        field_content = ""
        for rec in records:
            required_start_tag = '<group>'
            required_end_tag = '</group>'
            if rec.is_required:
                    required_start_tag = '<group class="requiredField">'

            lines =  '<field name="'+ rec.field_name+'_filename"  invisible="1" />\n <field name="'+ rec.field_name + '" string="' +rec.field_label+ '" widget="file" filename="'+ rec.field_name+ '_filename"/>\n'
            newline = required_start_tag + lines + required_end_tag
            field_content = field_content + '<group col="1">' + newline + '</group>'
        start_tag = '<sheet>'
        end_tag = '</sheet>'
        mid_content =' <h1><center>Document Form</center></h1>'
        field_content = start_tag + mid_content +'<group col="1">' + field_content + '</group>' +end_tag
        new_view = self.update_xml_content(view_content,start_tag,end_tag,field_content)
        # new_view = new_view.replace('Todos Form',form_heading )
        return new_view


    @api.model
    def update_xml_content(self, source_xml, start_node, end_node, replacement_content):
        node_start_index = source_xml.find(start_node)
        node_end_index = source_xml.find(end_node) + len(end_node)
        updated_arch = source_xml[:node_start_index] + replacement_content + source_xml[node_end_index:]
        dom = parseString(updated_arch)
        # pretty_xml_as_string = dom.toprettyxml(indent="  ")
        # return pretty_xml_as_string
        return updated_arch

    
    @api.model
    def logged_in_user(self, model, record_id,user_id,node_id):
        _logger.info("** logged in user update : model is:%s  and record id: %s", model,record_id)
        _logger.info("** lgged in user id %s ", user_id)
        if model:
            model = model.strip()

        current_model = self.env[model].sudo().browse(record_id)
        if hasattr(current_model, 'logged_in_user'):
            # call admin panel update data method
            self.admin_panel(current_model,node_id)
            if record_id:
                _logger.info(" ** record with found or not: %s", record_id)
                record_id = int(record_id)
                obj = self.env[model].search([('id','=',record_id)])
                obj.sudo().write({
                    'logged_in_user': int(user_id)
                })

                e_id = obj.logged_in_user.employee_id.id
                d_id =  obj.logged_in_user.employee_id.department_id.id
                _logger.info(" *** if block employee id %s ", str(obj.logged_in_user.employee_id))
                _logger.info(" *** if block department_id %s ", str(obj.logged_in_user.employee_id.department_id))
                if hasattr(current_model, 'employee_id'):
                    obj.sudo().write({
                    'employee_id'   : str(e_id) if e_id else '',
                    'employee_name' : e_id,
                })
                if hasattr(current_model, 'department'):
                    obj.sudo().write({
                    'department': d_id
                })
            else:
                res_user = self.env['res.users'].browse(int(user_id))
                e_id = res_user.employee_id.id
                d_id =  res_user.employee_id.department_id.id
                objects = self.env[model].search([]).sudo().write({
                    'logged_in_user': int(user_id),
                    })
                if hasattr(current_model, 'department'):
                    objects = self.env[model].search([]).sudo().write({
                        'employee_id'   : str(e_id) if e_id else '',
                        'employee_name' : e_id,
                        })  
                if hasattr(current_model, 'employee_id'):
                    objects = self.env[model].search([]).sudo().write({
                        'department': d_id,

                        })           
        return True


    # method to check record is lock by another user in list view
    @api.model
    def check_recod_is_locked(self, model, record_id,user_id,node_id):
        _logger.info("** lock_record : model is:%s  and record id: %s", model,record_id)
        _logger.info("** lock_record userid %s ", user_id)
        if model:
            model = model.strip()
        if record_id:
            print(" ** record lck type of reocrd id: ", type(record_id))
            record_id = str(record_id)

        lock_data_search = self.env['o2b.process.lock'].sudo().search(['&',('model','=',model.strip()),('record_id','=',record_id)],limit =1)
        response = None
        
        user = self.env['res.users'].sudo().browse(int(lock_data_search.user_id))
        if lock_data_search and lock_data_search.user_id != str(user_id) and lock_data_search.user_id != False:
            _logger.info(" show alert to this record is pending on other user id :: %s ", lock_data_search.user_id)
            response = ['LOCK',user.name]
        else:
            response = ['UNLOCK',user.name]

        return response


    # method to check record is lock by another user in form view
    @api.model
    def lock_record(self, model, record_id,user_id,node_id):
        _logger.info("** lock_record : model is:%s  and record id: %s", model,record_id)
        _logger.info("** lock_record userid %s ", user_id)
        if model:
            model = model.strip()
        if record_id:
            print(" ** record lck type of reocrd id: ", type(record_id))
            record_id = str(record_id)

        lock_data_search = self.env['o2b.process.lock'].sudo().search(['&',('model','=',model.strip()),('record_id','=',record_id)],limit =1)
        response = None
        if lock_data_search and lock_data_search.user_id == str(user_id):
            print(" ** current record lock is in your queue. after filling records please release this record via cliking done button",lock_data_search )
            response = ['USER_QUEUE']
            return response
        elif lock_data_search and lock_data_search.user_id != str(user_id) and lock_data_search.user_id != False:
            print(" show alert to this record is pending on other user id ::", lock_data_search.user_id)
            user = self.env['res.users'].sudo().browse(int(lock_data_search.user_id))

            response = ['OTHER_QUEUE',user.name]
            return response
        else:
            process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',model.strip()),('current_stage_id','=',node_id)])
            data = {
                    'record_id'     : record_id ,
                    'model'         : model,
                    'user_id'       : str(user_id),
                    }
            # if process.next_stage_id:
            #     _logger.info(" ** writing new lock record")
            #     new_lock_record  = self.env['o2b.process.lock'].sudo().create(data)
            #     response = ['FINAL']
            #     return response
            _logger.info(" ** writing new lock record")
            new_lock_record  = self.env['o2b.process.lock'].sudo().create(data)
            response = ['FINAL']
            return response
        return response

    @api.model
    def lock_release(self, model, record_id,user_id):
        _logger.info("** lock_release : model is:%s  and record id: %s", model,record_id)
        try:
            if model:
                model = model.strip()
            if record_id:
                record_id = int(record_id)
            if user_id:
                user_id = int(user_id)
            release_record = self.env['o2b.process.lock'].sudo().search(['&',('model','=',model.strip()),('record_id','=',record_id),('user_id','=',user_id)],limit =1)
            _logger.info(" ** releasing records %s ", str(release_record))
            if release_record:
                release_record.sudo().write({'active':False})
                _logger.info(" *** release final line executed.")
            return True
        except Exception as e:
            logger.error("release Error during lock release: %s", e)
            return False
            
        

    @api.model
    def update_app_list(self,process_name):
        try:
            count = 0
            _logger.info("process name: %s", process_name)
            module_name = 'o2b_' + process_name.replace(' ','_').lower()
            result = self.env['base.module.update'].with_user(2).sudo().update_module()
            # calling method to upgrade button: 
            current_module = self.env['ir.module.module'].sudo().search([('name','=',module_name)],limit=1)
            current_module.with_user(1).sudo().button_immediate_install()
            current_module.with_user(1).sudo().button_immediate_upgrade()
            
            model = 'o2b.' + process_name.replace(' ','_').lower()
            current_model = self.env['ir.model'].sudo().search([('model','=',model)],limit=1)
            if not current_model:
                result = self.env['base.module.update'].with_user(2).sudo().update_module()
                _logger.info("calling update_module base method: %s", result)
                # calling method to upgrade button: 
                current_module = self.env['ir.module.module'].sudo().search([('name','=',module_name)],limit=1)
                current_module.with_user(1).sudo().button_immediate_install()
                result = self.env['base.module.update'].with_user(2).sudo().update_module()
        except Exception as e:
            _logger.info(" *** error while install, upgrade module : %s ", str(e))
            pass


    @api.model
    def upgrade_app_list(self,process_name):
        try:
            count = 0
            _logger.info("process name: %s", process_name)
            module_name = 'o2b_' + process_name.replace(' ','_').lower()
            result = self.env['base.module.update'].with_user(2).sudo().update_module()
            # calling method to upgrade button: 
            current_module = self.env['ir.module.module'].sudo().search([('name','=',module_name)],limit=1)
            current_module.with_user(1).sudo().button_immediate_upgrade()
            
            model = 'o2b.' + process_name.replace(' ','_').lower()
            current_model = self.env['ir.model'].sudo().search([('model','=',model)],limit=1)
            if not current_model:
                _logger.info("calling update_module base method: %s", result)
                current_module = self.env['ir.module.module'].sudo().search([('name','=',module_name)],limit=1)
                current_module.with_user(1).sudo().button_immediate_upgrade()
            time.sleep(0.5)
        except Exception as e:
            _logger.info(" ***** error while upgrading only : %s ", str(e))
            pass



    @api.model
    def update_module_state(self):
        _logger.info("We are in update stage moudle %s",self)
        print("we are in update")
        cr = self.env.cr
        sql_query = """
        UPDATE ir_module_module
        SET state='installed'
        WHERE name LIKE 'o2b_%'
        AND state='to upgrade';
        """
        cr.execute(sql_query)
        self.env.cr.commit()

    # fetch process moder object vie process id or process name
    def fetch_process_obj(self,process_id,process_name):
        _logger.info("fetching process modular objprocess : %s",process_id)
        if process_id:
            process_id = process_id.strip()

        if process_name:
            process_name = process_name.strip()

        obj_via_id = self.env['o2b.process.modular'].sudo().search([('process_id', '=',process_id)], order='id desc',limit=1)
        if obj_via_id:
            decision_url = obj_via_id.process_temp_url
            if decision_url:
                return decision_url
            else:
                obj_via_name = self.env['o2b.process.modular'].sudo().search([('process_name', '=',process_name)], order='id desc',limit=1)
                if obj_via_name:
                    decision_url = obj_via_name.process_temp_url
                    if decision_url:
                        return decision_url
                    else:
                        return None    


    # **************uitility method start here*******************
    
    # update domian if contain datetime
    def process_datetime_string(self, input_string):
        user = self.env['res.users'].with_user(1).browse(2) 
        timezone = user.tz
        hour = 0
        minute = 0
        if timezone and timezone == 'Asia/Calcutta':
            hour = 5
            minute = 30
        datetime_pattern = r'"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2})"'
        datetime_domain = re.sub(
            datetime_pattern,
            lambda match: '"{}"'.format(
                (datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M") - timedelta(hours=hour, minutes=minute))
                .strftime("%Y-%m-%d %H:%M:%S")
            ),
            input_string
        )

        # extra parsing
        # for i, condition in enumerate(datetime_domain):
        #     field, operator, value = condition
        #     # Check if the value is a string representing a datetime
        #     if isinstance(value, str):
        #         try:
        #             value = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
        #             # Update the domain with the datetime object
        #             datetime_domain[i] = (field, operator, value)
        #         except ValueError:
        #             # If the string cannot be converted to datetime, just ignore it
        #             pass
        # extra parsing

        print("**** new updated string : ", datetime_domain)
        return datetime_domain
    # update domian if contain datetime

    # write code for ugraded_rule_engine start here
    def upgraded_rule_engine(self,process_mng_ob,statusbar_obj,rule_rec_obj):
        _logger.info(" **upgraded_rule_engineprocess_mng_ob %s", process_mng_ob)
        _logger.info(" **statusbar obj : %s ", statusbar_obj)
        _logger.info(" **decision rule obje: %s ", rule_rec_obj)
        node_domain = rule_rec_obj.get('domain')
        dummy_domain = rule_rec_obj.get('node_domain')
        odoo_domain = self.domain_parse(rule_rec_obj.get('domain'))
        record_next_name = rule_rec_obj.get('next_name')
        record_next_id = rule_rec_obj.get('next_id')
        record_exception_name = rule_rec_obj.get('exception_name')
        record_exception_id = rule_rec_obj.get('exception_id')
        record_prev_id = rule_rec_obj.get('Pre_id')
        if record_prev_id:
            record_prev_id.strip()
        _logger.info(" ***node domian: %s ", str(node_domain))
        _logger.info(" ***node parse domian: %s ", str(dummy_domain))
        _logger.info(" ***odoo_domain: %s ", str(odoo_domain))
        
        dummy_domain = dummy_domain.replace(", & ,",",")
        print(" &&&&&&&& dummin doman after remoe and ",dummy_domain )
        or_count =  dummy_domain.count('|')
        dummy_domain = dummy_domain.replace(", '|',"," ,")
        or_data = '['
        if or_count:
            for  i in range(or_count):
                or_data = or_data + "'|',"
        dummy_domain = dummy_domain.replace('[', or_data)
        # replace 'false' to False and 'true' to True
        dummy_domain = dummy_domain.replace('"true"','True')
        dummy_domain = dummy_domain.replace('"false"','False')

        # call datetime handle method 
        datetime_result = self.process_datetime_string(dummy_domain)
        if datetime_result:
            dummy_domain = datetime_result
            print(" ** after localdatetime format :", dummy_domain)
        # call datetime handle method 
        dummy_domain =  ast.literal_eval(dummy_domain)
        dummy_domain.append(('id', '=', int(process_mng_ob.record_id)))
        _logger.info("after parse nodedomain converted final dummy domain : %s and type of %s", dummy_domain, type(dummy_domain))
        actual_list = odoo_domain
        actual_list.append(('id', '=', int(process_mng_ob.record_id)))
        model_obj = self.env[process_mng_ob.model].sudo().browse(int(process_mng_ob.record_id))

        # if model_obj._name =='o2b.expense_track':
        #     print(" model objec;YYYYYYYYYYYYYYYYYYYYYYYYYYY: ", model_obj)
        #     print(" *** model,x_o2b_user_email_status", model_obj.x_o2b_user_email_status)
        #     print(" *** modelx_o2b_decision,", model_obj.x_o2b_decision)
        #     print(" *** model,", model_obj.x_o2b_user_email_status)

        record = None
        try:
            record = model_obj.search(dummy_domain)
            _logger.info(" *** dmmy domain which is applied %s  and type %s  ",dummy_domain, type(dummy_domain))
            if not record:
                record1 = model_obj.search(actual_list)
                _logger.info(" *** actual domain which is applied %s  and type %s  ",actual_list, type(actual_list))
                _logger.info("decision  record found via actual_list  : %s", record1)

            _logger.info("decesion record found dummy_domain   : %s", record)
        except Exception as e:
            _logger.info(" ** after applying data is not found moving previous states")
  
        if record:
            updated_state_value = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',process_mng_ob.model.strip()),('process_node_id','=',record_next_id)],limit=1)
            _logger.info("*** finding current stage in statusbar table %s:",updated_state_value)
            current_remark_field = self.env['ir.model.fields'].sudo().search(['&',('name','=','x_decision'),('model','=',process_mng_ob.model.strip())])
            if updated_state_value:
                self.write_decision_stage(record,updated_state_value.stage_value)
                self.handle_set_unset(process_mng_ob,updated_state_value,updated_state_value)
                if current_remark_field:
                    record.sudo().write({
                    'x_o2b_stage': updated_state_value.stage_value,
                    'x_remark'   : '',
                    'x_decision' : '',
                    'x_done': True,
                    })
                else:
                    record.sudo().write({
                    'x_o2b_stage': updated_state_value.stage_value,
                    'x_done': True,
                    })

            
            #  check if previos stage is emal type
            print(" fidning previidfdfd  ", record_prev_id)
            prev_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',process_mng_ob.model.strip()),('process_node_id','=',record_prev_id)],limit=1)
            print(" stupid full ojbect ", prev_obj)
            if prev_obj:
                print("prvios id is email hide the step until the emaail shedular is not show this record ",record.x_o2b_stage, " or visible value ", record.x_done)
                if prev_obj.node_type == 'email':
                    record.sudo().write({
                    'x_done': False,
                    })
                print(" if previous is email the shide ", record.x_done)


            #creating record in process manager table if agian next step is decision
            if updated_state_value.node_type == 'decision':
                next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',process_mng_ob.model.strip()),('process_node_id','=',updated_state_value.process_node_id)],limit=1)
                # record.sudo().write({
                #     'x_o2b_stage': next_obj.stage_value,
                #     })
                self.write_decision_stage(record,next_obj.stage_value)
                self.handle_decision_records(process_mng_ob,next_obj)
               
            # creating new record in process manager table if next step is email after decesion making
            if updated_state_value.node_type == 'email':
                print(" ******** yes anuj faultl ***************")
                self.write_decision_stage(record,updated_state_value.stage_value)
                self.handle_set_unset(process_mng_ob,updated_state_value,updated_state_value)
                vals= {
                    'record_id'     : record.id,
                    'model_stage'   : record.x_o2b_stage ,
                    'current_id'    : updated_state_value.process_node_id,
                    'model'         : updated_state_value.model_name ,
                    'current_name'  : updated_state_value.stage_name ,
                    }
                p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',record.id),('model','=',updated_state_value.model_name)])
                if not p_record:
                    
                    self.env['o2b.process.manager'].create(vals)
                else:
                    new_p_rect = self.env['o2b.process.manager'].create(vals)
                    p_record.write({ 
                        'current_id'    : updated_state_value.process_node_id,
                        'active'        : False
                        })

                # self.process_manager_crud(updated_state_value.model_name, p_record.id,updated_state_value.process_node_id)
                record_mail = self.env['o2b.process.modular.email'].search([('model_name','=',p_record.model),('current_node_id','=', updated_state_value.process_node_id)],limit=1)
                # create record in mail template:
                new_mail_record = self.env['o2b.process.email'].sudo().create({
                            'record_id'     : p_record.record_id,
                            'model'         : p_record.model,
                            'current_id'    : p_record.current_id,
                            'next_id'       : record_mail.next_step_id,
                            'recipient'     : record_mail.recipient ,
                            'mail_subject'  : record_mail.mail_subject ,
                            'mail_body'     : record_mail.mail_body ,
                            'mail_count'    : record_mail.mail_limit ,
                            'is_active'     : True ,
                            'is_sent'       : False ,
                            'mail_trigger'  : record_mail.mail_trigger ,
                            })
                # call fetch attachment and update email table record
                self._fetch_attachment(record_mail,new_mail_record)
            if updated_state_value.node_type not in ['decision','email']:
                _logger.info(" **we ain in not in email for next record is deleteing %s and model%s",record.id,updated_state_value.model_name)
                p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',record.id),('model','=',updated_state_value.model_name)])
                p_record.write({'active' : False})
            return 1
        else:
            _logger.info(" \n ******rule engine failed for record *****\n%s: and stage value is %s  ",model_obj,model_obj.x_o2b_stage )
            # model_obj.with_user(2).sudo().write({
            # 'x_done': True,
            # })
            return 0
    # advance rule engine end here
    
    # domain parse method for odoo
    def domain_parse(self,domain):
        data_list = []
        for record in domain:
            if len(record) == 1:
                data_list.append((record))
            if len(record)>1:
                data_list.append(tuple(record))
        return data_list;
    # end here


    # ***** client rule engine domain parser engine
    def client_domain_parser(self,rec,domain,odoo_domain,decision_obj):
        dummy_domain = odoo_domain.replace(", '&',",",")
        or_count =  dummy_domain.count('|')
        dummy_domain = dummy_domain.replace(", '|',"," ,")
        or_data = '['
        if or_count:
            for  i in range(or_count):
                or_data = or_data + "'|',"
        dummy_domain = dummy_domain.replace('[', or_data)
        dummy_domain =  ast.literal_eval(dummy_domain)
        dummy_domain.append(('id', '=', rec.record_id))
        actual_list = ast.literal_eval(odoo_domain)
        actual_list.append(('id', '=', rec.record_id))
        model_obj = self.env[rec.model].browse(int(rec.record_id))
        record = None
        print(" model_obj ", model_obj)
        print(" dummy_domain  ", dummy_domain)
        print(" actual_list  ", actual_list)
        actual_record = model_obj.search(actual_list)
        if actual_record:
            record = actual_record
        if not actual_record:
            dummy_record = model_obj.search(dummy_domain)
            if dummy_record:
                record = dummy_record
            _logger.info("\n ** record via dumming domain:  : %s", dummy_record)
        _logger.info("*** record via reald domain:    : %s", actual_record)
        
        if record:
            updated_state_value = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',decision_obj.next_stage_id)],limit=1)
            _logger.info("*** finding current stage in statusbar table %s:",updated_state_value)
            current_remark_field = self.env['ir.model.fields'].sudo().search(['&',('name','=','x_decision'),('model','=',rec.model.strip())])
            if updated_state_value:
                self.write_decision_stage(record,updated_state_value.stage_value)
                self.handle_set_unset(rec,updated_state_value,updated_state_value)
                if current_remark_field:
                    record.sudo().write({
                    'x_o2b_stage': updated_state_value.stage_value,
                    'x_remark'   : '',
                    'x_decision' : '',
                    'x_done': True,
                    })
                else:
                    record.sudo().write({
                    'x_o2b_stage': updated_state_value.stage_value,
                    'x_done': True,
                    })

            #  check if previos stage is emal type
            print(" fidning previidfdfd  ", decision_obj.previous_id)
            prev_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',decision_obj.previous_id)],limit=1)
            print(" stupid full ojbect ", prev_obj)
            if prev_obj:
                print("prvios id is email hide the step until the emaail shedular is not show this record ",record.x_o2b_stage, " or visible value ", record.x_done)
                if prev_obj.node_type == 'email':
                    record.sudo().write({
                    'x_done': False,
                    })
                print(" if previous is email the shide ", record.x_done)
            #creating record in process manager table if agian next step is decision
            if updated_state_value.node_type == 'decision':
                next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',updated_state_value.process_node_id)],limit=1)
                # record.sudo().write({
                #     'x_o2b_stage': next_obj.stage_value,
                #     })
                self.write_decision_stage(record,next_obj.stage_value)
                self.handle_decision_records(process_mng_ob,next_obj)
               
            # creating new record in process manager table if next step is email after decesion making
            if updated_state_value.node_type == 'email':
                self.write_decision_stage(record,updated_state_value.stage_value)
                self.handle_set_unset(rec,updated_state_value,updated_state_value)
                vals= {
                    'record_id'     : record.id,
                    'model_stage'   : record.x_o2b_stage ,
                    'current_id'    : updated_state_value.process_node_id,
                    'model'         : updated_state_value.model_name ,
                    'current_name'  : updated_state_value.stage_name ,
                    }
                p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',record.id),('model','=',updated_state_value.model_name)])
                if not p_record:
                    
                    self.env['o2b.process.manager'].create(vals)
                else:
                    new_p_rect = self.env['o2b.process.manager'].create(vals)
                    p_record.write({ 
                        'current_id'    : updated_state_value.process_node_id,
                        'active'        : False
                        })

                # self.process_manager_crud(updated_state_value.model_name, p_record.id,updated_state_value.process_node_id)
                record_mail = self.env['o2b.process.modular.email'].search([('model_name','=',p_record.model),('current_node_id','=', updated_state_value.process_node_id)],limit=1)
                # create record in mail template:
                new_mail_record = self.env['o2b.process.email'].sudo().create({
                            'record_id'     : p_record.record_id,
                            'model'         : p_record.model,
                            'current_id'    : p_record.current_id,
                            'next_id'       : record_mail.next_step_id,
                            'recipient'     : record_mail.recipient ,
                            'mail_subject'  : record_mail.mail_subject ,
                            'mail_body'     : record_mail.mail_body ,
                            'mail_count'    : record_mail.mail_limit ,
                            'is_active'     : True ,
                            'is_sent'       : False ,
                            'mail_trigger'  : record_mail.mail_trigger ,
                            })
                # call fetch attachment and update email table record
                self._fetch_attachment(record_mail,new_mail_record)
            if updated_state_value.node_type not in ['decision','email']:
                _logger.info(" **we ain in not in email for next record is deleteing %s and model%s",record.id,updated_state_value.model_name)
                p_record = self.env['o2b.process.manager'].sudo().search([('record_id','=',record.id),('model','=',updated_state_value.model_name)])
                p_record.write({'active' : False})
            return 1
        else:
            _logger.info(" \n ******rule engine failed for record *****\n%s: and stage value is %s  ",model_obj,model_obj.x_o2b_stage )
            # model_obj.with_user(2).sudo().write({
            # 'x_done': True,
            # })
            return 0

    # clinet rule engine method
    @api.model
    def client_rule_engine(self,rec,next_obj,process_obj):
        _logger.info(" \n**** *********************************we are in client rule engine **** ")
        _logger.info("handle decison_recordds process manger table data : %s",rec)
        _logger.info("rec model : %s",rec.model)
        _logger.info("next object record: %s", str(next_obj))
        _logger.info("next_obj.process_node_id %s",next_obj.process_node_id)
        _logger.info("next_obj.stage_name %s",next_obj.stage_value)
        _logger.info("next_obj.node_type %s",next_obj.node_type)
        print(" all decsion record assosicate iwth prc", process_obj.process_stages_decision_ids)
        if process_obj.process_stages_decision_ids:
            cur_decsions = process_obj.process_stages_decision_ids.sudo().search([('process_id','=',process_obj.process_id),('decision_id','=',next_obj.process_node_id)])
            print(" applying rule base of givne conditon: ",cur_decsions)
            model_obj = self.env[rec.model].sudo().browse(int(rec.record_id))
            if model_obj._name =='o2b.expense_management_test_v1':
                print(" model objec;YYYYYYYYYYYYYYYYYYYYYYYYYYY: ", model_obj)
                print(" *** model,x_o2b_user_email_status", model_obj.x_o2b_user_email_status)
                print(" *** modelx_o2b_decision,", model_obj.x_decision)
                print(" *** model,", model_obj.x_o2b_user_email_status)
            decision_status = []
            for record in cur_decsions:
                print(" currend decsion  : ", record.process_name)
                # print("previsou id ", record.previous_id, ' name : ', record.previous_stage)
                # print("decesion id ", record.decision_id, ' name : ', record.decision_name)
                # print("next id ", record.next_stage_id, ' name : ', record.next_stage)
                # print("exep id ", record.exception_state_id, ' name : ', record.exception_state)
                # print("domain id ", record.domain, ' name : ', record.odoo_domain)
                rule_engine_status = self.client_domain_parser(rec,record.domain,record.odoo_domain,record)
                decision_status.append(rule_engine_status)
                _logger.info("** dicision_status %s", decision_status)
            atleast_one_execution = 1 in decision_status
            _logger.info(" ** check atleast_one_execution value : %s ",atleast_one_execution)
            if not atleast_one_execution:
                _logger.info(" all rule failded we are checking if there is any exception state in condition.")
                if record.exception_state_id:
                    current_stage = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record.exception_state_id)],limit=1)
                    self.write_decision_stage(model_obj,current_stage.stage_value)
                    self.handle_set_unset(rec,current_stage,current_stage)
                    model_obj.with_user(2).sudo().write({
                        'x_o2b_stage'   : current_stage.stage_value,
                        'x_done'        : True,
                    })
                else:
                    _logger.info(" no decision rule applied that why make record visible")
                    model_obj.with_user(2).sudo().write({
                        'x_done': True,
                        })
       
    # fetch all decision rule from server and processed it
    @api.model
    def handle_decision_records(self,rec,next_obj):
        # _logger.info("handle decison_recordds process manger table data : %s",rec)
        # _logger.info("rec model : %s",rec.model)
        # _logger.info("next object record: %s", str(next_obj))
        # _logger.info("next_obj.process_node_id %s",next_obj.process_node_id)
        # _logger.info("next_obj.stage_name %s",next_obj.stage_value)
        # _logger.info("next_obj.node_type %s",next_obj.node_type)

        # ***********deciding rule  fetch from client server or node server
        process_id = next_obj.process_id
        # print(" ** process node Id; ", process_id)
        process_obj = self.env['o2b.process.modular'].search([('process_id', '=',process_id)],limit=1)
        _logger.info(" proecess ogj %s :", process_obj)
        print(" proecess ogj enable client rule ", process_obj.client_rule_engine_enable)
        if process_obj and process_obj.client_rule_engine_enable:
            result = self.client_rule_engine(rec,next_obj,process_obj)
            _logger.info(" *** client rule engine run completely *** .")
            return True

        # ***********deciding rule  fetch from client server or node server

        # ******calling middleware api to fetch deciion rules******
        # try:
        _logger.info("** we are in fetching node decision from middleware service")
        # fetch middleware base url
        mid_base_url = self.fetch_process_obj(next_obj.process_id,next_obj.process_name)
        _logger.info("  *** middleware base url: %s ", mid_base_url)
        if not mid_base_url:
            mid_base_url = 'http://192.168.1.38:3636'
            mid_base_url = 'http://122.160.26.224:3636' 
            mid_base_url = 'https://node.oflowai.com'
        end_point = '/decision/fetch'
        url = mid_base_url + end_point
        _logger.info(" **final url for decision fetching : %s ", url)
        # fetch middleware base url
        headers = {
        'Content-Type': 'application/json',
        }
        data = {
        'key': 'o2b_technologies',
        'process_id'    : next_obj.process_id,
        'curr_id'       : next_obj.process_node_id,
        'curr_name'     : next_obj.stage_name
        }
        _logger.info(" ** complete request body: %s ", data)
        response = requests.post(url, json=data, headers=headers)
        records = response.json().get('message',)
        _logger.info("** fetch decision rule reponse %s", str(records))
        if records != 'NOT_FOUND':
            decision_status = []
            for record in records:
                _logger.info("\n decision  next name :%s ", record.get('next_name'))
                _logger.info("\n decision  next id: %s ", record.get('next_id'))
                _logger.info("\n decision  exception name :%s ", record.get('exception_name'))
                _logger.info("\n decision  next exception id: %s ", record.get('exception_id'))
                _logger.info("\ndecision  domain: %s ", record.get('domain'))
                _logger.info("\ndecision  domain parse: %s ", self.domain_parse(record.get('domain')))
                _logger.info("********end process records**************")
                # call upgraded decision rule method here
                record_acutal_condition = record.get('domain')
                record_parse_condition = self.domain_parse(record.get('domain'))
                record_next_name = record.get('next_name')
                record_next_id = record.get('domain')
                record_exception_name = record.get('exception_name')
                record_exception_id = record.get('exception_id')
                rule_engine_status = self.upgraded_rule_engine(rec,next_obj,record)
                decision_status.append(rule_engine_status)

            _logger.info("** dicision_status %s", decision_status)
            atleast_one_execution = 1 in decision_status
            _logger.info(" ** check atleast_one_execution value : %s ",atleast_one_execution)
            model_obj = self.env[rec.model].sudo().browse(int(rec.record_id))
            if not atleast_one_execution:
                _logger.info(" all rule failded we are checking if there is any exception state in condition.")
                if record_exception_id:
                    current_stage = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_exception_id)],limit=1)
                    self.write_decision_stage(model_obj,current_stage.stage_value)
                    self.handle_set_unset(rec,current_stage,current_stage)
                    model_obj.with_user(2).sudo().write({
                        'x_o2b_stage'   : current_stage.stage_value,
                        'x_done'        : True,
                    })
                else:
                    _logger.info(" no decision rule applied that why make record visible")
                    model_obj.with_user(2).sudo().write({
                        'x_done': True,
                        })
           
            # except Exception as e:
            #     _logger.info(" *** while connecting with api . there is some errro." + str(e))
       
        
    # this method is calling on clicking done button via
    @api.model
    def decision_action(self, model, record_id, fields,node_id,user_id):
        _logger.info("done method called %s", model)
        if model:
            model = model.strip()
        self.env[model].sudo().pre(self)
        if record_id:
            record_id = int(record_id)
            current_record_model = self.env[model].sudo().browse(record_id)
            current_stage = current_record_model.x_o2b_stage
            _logger.info("*** decision action : %s  for model %s : ",current_stage,model)
            # comment below line if end stage done button hide:
            process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',model.strip()),('current_stage_id','=',node_id)] , order='id desc',limit=1)
            if process.next_stage_id:
                code = process.model_name.replace('.','_').lower()
                if hasattr(current_record_model, 'x_reference_no'):
                    reference_exist = getattr(current_record_model, 'x_reference_no')
                current_record_model.sudo().write({
                    'x_done'            : False,
                    'x_reference_no'    : reference_exist if reference_exist else self.env['ir.sequence'].next_by_code(code),
                    # extra code to pending since field
                    # 'work_step_tat_test'    : self.time_calculator(current_record_model.create_date,datetime.utcnow())
                    })
            statusbar = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',model),('process_node_id','=',node_id)],limit=1)
            base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            domain = ''
            if statusbar:
                domain = '[("x_o2b_stage","=","'+ statusbar.stage_value + '"),("x_done","=",True)]'
            action_id = self.env['ir.actions.act_window'].sudo().search(
            [('res_model', '=', model.strip()), ('domain', '=', domain)],
            order='id desc',
            limit=1
            )
            print("action_id :" , action_id)
            redirect_url = ''
            if action_id:
                redirect_url = '{}/web#action={}&model={}&view_type=list'.format(base_url, action_id.id, model)
                _logger.info(" decision node Record URL: %s", redirect_url)
            msg = ""
            response = ['normal', redirect_url,msg]
            self.env[model].sudo().post(self)
            self.process_manager_crud(model, record_id,node_id)
            self.lock_release(model, record_id,user_id)
            return response


    # write method which confirm reuired field is emply or not:
    @api.model
    def required_field_check(self, model, record_id, fields,node_id):
        response = []
        _logger.info("required_field_check model %s", model)
        _logger.info("required_field_check node id %s", node_id)
        if model:
            model = model.strip()
        if record_id and node_id:
            _logger.info("**********record id: %s ", record_id)
            record_id = int(record_id)
            current_record_model = self.env[model].sudo().browse(record_id)
            required_form_fields = self.env['o2b.process.modular.field.method'].sudo().search([('model_name', '=',model),('form_id','=',node_id),('is_required','=',True)])
            _logger.info("** all required fields on current form %s ", str(required_form_fields))
            response = ['Pass', '','','']
            for rec_field in required_form_fields:
                if hasattr(current_record_model, rec_field.field_name):
                    check_type ='NORMAL'
                    if rec_field.is_todo_field:
                        check_type = "TODO"
                    if rec_field.is_document_field:
                        check_type = "DOCUMENT"
                    field_value = getattr(current_record_model, rec_field.field_name)
                    if not field_value:
                        response = ['Failed', rec_field.field_name,rec_field.field_label,check_type]
                        return response

            return response

    # create process manager record : responisble to update and create record in process manager table
    def process_manager_crud(self, model, record_id,node_id):
        _logger.info("** process manager insert rec id: %s ",record_id)
        _logger.info(" **p_manager model name : %s ", model)
        process_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',model.strip()),('current_stage_id','=',node_id)])

        if process_stage:
            p_manager_record = self.env['o2b.process.manager'].sudo().search(['&',('model','=',model.strip()),('record_id','=',record_id)])
            current_model = self.env[model].sudo().search([('id','=',record_id)])
            if p_manager_record:
                _logger.info(" ** process record model%s: and current step %s  ", p_manager_record.model,p_manager_record.current_id)
                # update
                p_manager_record.sudo().write({
                    'record_id'     : record_id ,
                    'model'         : model ,
                    'current_id'    : process_stage.current_stage_id ,
                    })
            else:
                # create
                p_manager_record.sudo().create({
                    'record_id'     : record_id ,
                    'model'         : model ,
                    'current_id'    : process_stage.current_stage_id ,
                    })

    # Remark history save function call:
    def remark_history(self,model,record_id,fields,process):
        _logger.info("*** remark_history : %s", process)
        _logger.info("*** remark_history: %s", model)
        _logger.info("*** record id :  %s", record_id)
        _logger.info("*** process activity_type:  %s", process.activity_type)
        _logger.info("*** process activity name next name:  %s", process.next_stage)
        if model:
            model = model.strip()
        if record_id:
            record_id = int(record_id)
        model_exist = self.env['ir.model'].sudo().search([('model','=',model)])
        current_model = self.env[model].sudo().search([('id','=',record_id)])
        _logger.info("*** current record: in remark history: %s ", current_model)
        current_record_field = self.env['ir.model.fields'].sudo().search(['&',('name','=','x_decision'),('model','=',model)])
        _logger.info("***** current record : x_o2b_decision check %s ", current_record_field)
        if current_model and current_record_field:
            field = model.split('.')[-1]
            relation_field = 'x_o2b_' + field +'_in_remark_history'
            if current_model.x_remark or current_model.x_decision:
                current_step = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',current_model._name),('process_node_id','=',process.current_stage_id)],limit=1)

                remark_obj = self.env['o2b.process.modular.remark.history'].create({
                    relation_field  : record_id,
                    'decision'      : current_model.x_decision,
                    'remark'        : current_model.x_remark,
                    'current_stage' : current_step.stage_name,
                    })
                current_uid = current_model.remark_user.id
                remark_obj.write({
                     'remark_uid'   : current_uid if current_uid else 2,
                        })
                print(" ********* current stage change " , current_model.x_o2b_stage)
                msg = None
                next_step_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',current_model._name),('process_node_id','=',process.next_stage_id)],limit=1)

                # if next_step_obj.node_type in ['email_verify','email','decision']:
                #     step_obj = self.env['o2b.process.modular.stage'].sudo().search([('model_name', '=',current_model._name),('current_stage_id','=',next_step_obj.process_node_id)],limit=1)
                #     print(" step_obj.activity type", step_obj.activity_type)
                #     if step_obj.activity_type not in ['decision']:
                #         current_model.sudo().write({
                #         'x_remark'   : '',
                #         'x_decision' : '',
                #         })
                # elif next_step_obj.node_type not in ['decision']:
                #         rrrr
                #         current_model.sudo().write({
                #         'x_remark'   : '',
                #         'x_decision' : '',
                #         })

                if next_step_obj.node_type not in ['email_verify','email','decision']:
                    _logger.info(" ** setting decsion blank next step is : %s ", next_step_obj.node_type)
                    current_model.sudo().write({
                        'x_remark'   : '',
                        'x_decision' : '',
                        })



                    
    # Remark history save function call:

    def convert_to_odoo_domain(self,expr):
        pattern = r'\(([^,]+),([=><!]+),([^,]+)\)'
        domain = []
        or_conditions = expr.split('|')
        for or_condition in or_conditions:
            and_conditions = or_condition.split('&')
            and_domain = []

            for condition in and_conditions:
                condition = condition.strip("()")
                match = re.match(pattern, condition)
                if match:
                    field = match.group(1)   # Field name
                    operator = match.group(2)  # Operator
                    value = match.group(3)    # Value
                    try:
                        value = int(value)
                    except ValueError:
                        pass  
                    and_domain.append((field, operator, value))
            if and_domain:
                if len(and_domain) > 1:
                    domain.append(and_domain)
                else:
                    domain.extend(and_domain)
            if len(or_conditions) > 1:
                domain.append('|')
        return domain


    def handle_set_unset(self,rec,process,next_obj):
        try:
            user = self.env['res.users'].with_user(1).browse(2) 
            timezone = user.tz
            _logger.info("*** handle_set_unset rec : %s", rec)
            _logger.info("*** handle_set_unset process : %s", process)
            current_model = self.env[rec.model].sudo().browse(int(rec.record_id))
            _logger.info("*** current record: in handle_set_unset %s ", current_model)
            statusbar_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',rec.current_id)],limit=1)
            if next_obj:
                statusbar_obj = next_obj
            else:
                return True

            if statusbar_obj and statusbar_obj.set_unset:
                set_data = statusbar_obj.set_unset.get('set') 
                _logger.info(" statusbar set and unset value : %s", str(set_data))
                field_name = None
                for data in set_data:
                    field = data['field']
                    value = data['value']
                    condition = data['condition']
                    print(" ** on field name**", field)
                    print(" **  on field value **", value)
                    print(" **  on field condition **", condition)
                    if condition and condition != '':
                        expression = condition
                        # print(" ** current expression")
                        or_count = expression.count('|')
                        if '&' in expression:
                            parts = expression.split('&')
                            # print(" ** now checking expression : ", expression)
                            # parts = re.split(r'(&|\|)', expression)
                            domain = []
                            domain.append(('id', '=', int(current_model.id)))
                            for part in parts:
                                print(" and conditiond &&", part)
                                if 'in' in part:
                                    print(" ==================")
                                    part =  part.strip('()')
                                    part = part.split(',')
                                    index_in = part.index('in')
                                    new_list = part[index_in + 1:]
                                    new_list = [item.strip('()') for item in new_list]
                                    field_name = part[0]
                                    operator = part[1] 
                                    # c_value = part[2] 
                                    domain.append((field_name+'.name', operator, new_list))
                                    print(" &&& domain; ", domain)
                                if 'not in' in part:
                                    part =  part.strip('()')
                                    part = part.split(',')
                                    index_in = part.index('not in')
                                    new_list = part[index_in + 1:]
                                    new_list = [item.strip('()') for item in new_list]
                                    field_name = part[0] 
                                    operator = part[1] 
                                    # c_value = part[2] 
                                    domain.append((field_name+'.name', operator, new_list))
                                    # print(" not in &&&inin domain; ", domain)
                                if 'not in' not in part and 'in' not in part:
                                    print("++++++++++++++++")
                                    print("+++++++++++++++&&& in parts ", part)
                                    part =  part.strip('()')
                                    # print(" part.strip('()')====>", part)
                                    part = part.split(',')
                                    # print("part.split(',')===>",part)
                                    field_name = part[0]  
                                    operator = part[1] 
                                    c_value = part[2] 
                                    # print(" condtion field name &", field_name)
                                    # print(" condtion operator name & ", operator)
                                    # print(" condtion field value &", c_value)
                                    # check field type first
                                    if hasattr(current_model, field_name):
                                        saved_value = getattr(current_model, field_name)
                                        field_type = current_model._fields.get(field_name).__class__.__name__
                                        if field_type:
                                            field_type = field_type.lower()
                                            if field_type in ['datetime'] and c_value:
                                                try:
                                                    hour = 0
                                                    minute = 0
                                                    if timezone and timezone == 'Asia/Calcutta':
                                                        hour = 5
                                                        minute = 30
                                                    default_datetime = datetime.strptime(c_value, '%Y-%m-%dT%H:%M')
                                                    default_value = default_datetime  - timedelta(hours = hour, minutes = minute)
                                                    default_value = default_value.strftime('%Y-%m-%d %H:%M:%S')
                                                    c_value = default_value
                                                except Exception as e:
                                                    c_value = c_value
                                                    _logger.info(" set unset seting datetime error in condtion and %s ", str(e))
                                    # check field type first
                                    domain.append((field_name, operator, c_value))
                        if '|' in expression:
                            parts = expression.split('|')
                            domain = []
                            domain.append(('id', '=', int(current_model.id)))
                            domain.insert(1, '|')
                            for part in parts:
                                print(" and conditiond &&", part)
                                if 'in' in part:
                                    print(" ================== or ||")
                                    part =  part.strip('()')
                                    part = part.split(',')
                                    index_in = part.index('in')
                                    new_list = part[index_in + 1:]
                                    new_list = [item.strip('()') for item in new_list]
                                    field_name = part[0]
                                    operator = part[1] 
                                    # c_value = part[2] 
                                    domain.append((field_name+'.name', operator, new_list))
                                    print(" &&& domain; ", domain)
                                if 'not in' in part:
                                    part =  part.strip('()')
                                    part = part.split(',')
                                    index_in = part.index('not in')
                                    new_list = part[index_in + 1:]
                                    new_list = [item.strip('()') for item in new_list]
                                    field_name = part[0] 
                                    operator = part[1] 
                                    # c_value = part[2] 
                                    domain.append((field_name+'.name', operator, new_list))
                                    # print(" not in &&&inin domain; ", domain)
                                if 'not in' not in part and 'in' not in part:
                                    print("++++++++++++++++ other operator")
                                    # print("+++++++++++++++&&& in parts ", part)
                                    part =  part.strip('()')
                                    # print(" part.strip('()')====>", part)
                                    part = part.split(',')
                                    # print("part.split(',')===>",part)
                                    field_name = part[0]  
                                    operator = part[1] 
                                    c_value = part[2] 
                                    # print(" condtion field name &", field_name)
                                    # print(" condtion operator name & ", operator)
                                    # print(" condtion field value &", c_value)
                                    # handle datetime in conditon
                                    if hasattr(current_model, field_name):
                                        saved_value = getattr(current_model, field_name)
                                        field_type = current_model._fields.get(field_name).__class__.__name__
                                        if field_type:
                                            field_type = field_type.lower()
                                            if field_type in ['datetime'] and c_value:
                                                try:
                                                    hour = 0
                                                    minute = 0
                                                    if timezone and timezone == 'Asia/Calcutta':
                                                        hour = 5
                                                        minute = 30
                                                    default_datetime = datetime.strptime(c_value, '%Y-%m-%dT%H:%M')
                                                    default_value = default_datetime  - timedelta(hours = hour, minutes = minute)
                                                    default_value = default_value.strftime('%Y-%m-%d %H:%M:%S')
                                                    c_value = default_value
                                                except Exception as e:
                                                    c_value = c_value
                                                    _logger.info(" set unset seting datetime error in condtion or %s ", str(e))
                                    # handle datetime in conditon
                                    domain.append((field_name, operator, c_value))
                        print(" just printing whole exression: ", expression ,"type of rexpression ", type(expression))
                        if ('in' in expression or 'not in' in expression) and ('|' not in expression and '&' not in expression):
                            print(" whoel parsts :", expression)
                            parts = expression.split(",")
                            print(" whole parsfsf ", parts)
                            domain = []
                            new_list = []
                            # domain.append(('id', '=', int(current_model.id)))
                            if 'in' in parts:
                                index_in = parts.index('in')
                                new_list = parts[index_in + 1:]
                                new_list = [item.strip('()') for item in new_list]
                                field_name = parts[0].strip('()') 
                                operator = parts[1] 
                                # c_value = part[2] 
                                domain.append((field_name+'.name', operator, new_list))
                                # print(" inin domain; ", domain)
                            if 'not in' in parts:
                                index_in = parts.index('not in')
                                new_list = parts[index_in + 1:]
                                new_list = [item.strip('()') for item in new_list]
                                field_name = parts[0].strip('()') 
                                operator = parts[1] 
                                # c_value = part[2] 
                                domain.append((field_name+'.name', operator, new_list))

                        if ('in' not in expression and 'not in' not in expression) and ('|' not in expression and '&' not in expression):
                            print(" ye we are in right block ", expression)
                            output_list = expression.strip("()").split(",")
                            field_name = output_list[0] 
                            operator = output_list[1] 
                            c_value = output_list[2]
                            domain = []
                            domain.append(('id', '=', int(current_model.id))) 
                            print(" effro field name : ", field_name," operator ", operator , " value ", c_value)   
                            print(" effro current model  name : ", current_model)
                            if hasattr(current_model, field_name):
                                saved_value = getattr(current_model, field_name)
                                field_type = current_model._fields.get(field_name).__class__.__name__
                                if field_type:
                                    field_type = field_type.lower()
                                    if field_type in ['datetime'] and c_value:
                                        # try:
                                            hour = 0
                                            minute = 0
                                            if timezone and timezone == 'Asia/Calcutta':
                                                hour = 5
                                                minute = 30
                                            default_datetime = datetime.strptime(c_value, '%Y-%m-%dT%H:%M')
                                            default_value = default_datetime  - timedelta(hours = hour, minutes = minute)
                                            # default_value = default_value.strftime('%Y-%m-%d %H:%M:%S')
                                            c_value = default_value
                                            _logger.info(" ** actual datetime give by user: %s ",c_value)
                                            _logger.info(" ** actual datetime string to data %s",default_datetime)
                                            _logger.info(" ** actual datetime minuse 5.30 hour %s ",c_value)
                                         
                                        # except Exception as e:
                                        #     c_value = c_value
                                        #     _logger.info(" set unset seting datetime error in condtion or %s ", str(e))
                            domain.append((field_name, operator, c_value)) 
                            
                        if hasattr(current_model, field_name) and field_name:
                            db_value = getattr(current_model, field_name)
                            _logger.info(" **database value; %s", db_value)
                            # domain.append(('id', '=', int(current_model.id)))
                            print(" ** final domain  ", domain ," domain tupe: ", type(domain))
                            record_match  = self.env[rec.model].sudo().search(domain,limit=1)
                            print("** record match vie condtion ", record_match)
                            if record_match and record_match.id == current_model.id:
                                udpate_dict = self.return_dict(current_model,field,value,timezone)
                                if udpate_dict:
                                    current_model.sudo().write(udpate_dict)
                    else:
                        udpate_dict = self.return_dict(current_model,field,value,timezone)
                        if udpate_dict:
                            current_model.sudo().write(udpate_dict)
        except Exception as e:
            _logger.info("***set unset error: %s", str(e) )
            pass

    def return_dict(self,current_model,field,value,timezone):
        udpate_dict = {}
        if hasattr(current_model, field):
            saved_value = getattr(current_model, field)
            field_type = current_model._fields.get(field).__class__.__name__
            if field_type:
                field_type = field_type.lower()
            
            if field_type == 'boolean' and value:
                udpate_dict[field] = True

            if field_type in ['char','html','text'] and value:
                udpate_dict[field] = str(value)

            if field_type == 'float' and value:
                udpate_dict[field] = float(value)

            if field_type == 'integer' and value:
                udpate_dict[field] = int(value)

            if field_type in ['date'] and value:
                print("***** my data tiem data")
                try:
                    udpate_dict[field] = datetime.strptime(value, '%Y-%m-%d').date()
                except Exception as e:
                    udpate_dict[field] = date.today()
                    _logger.info(" set unset seting date error %s ", str(e))


            if field_type in ['datetime'] and value:
                print("***** my data tiem datetime" , value, " tiemzone : ", timezone)
                try:
                    hour = 0
                    minute = 0
                    if timezone and timezone == 'Asia/Calcutta':
                        hour = 5
                        minute = 30
                    default_datetime = datetime.strptime(value, '%Y-%m-%dT%H:%M')
                    default_value = default_datetime  - timedelta(hours = hour, minutes = minute)
                    default_value = default_value.strftime('%Y-%m-%d %H:%M:%S')
                    udpate_dict[field] = default_value

                except Exception as e:
                    udpate_dict[field] = datetime.today()
                    _logger.info(" set unset seting datetime error %s ", str(e))

            if field_type == 'json' and value:
                udpate_dict[field] = json.dumps(value, ensure_ascii=False)

            if field_type == 'selection' and value:
                udpate_dict[field] = str(value.replace(' ','_').lower())
          
            if field_type in ['many2many','many2one'] and value:
                _logger.info("** 'many2many','many2one'set/unset")
                if field_type == 'many2many':
                    try:
                        elements = value.split(',')
                        m2m_ids = []
                        relation_model = None
                        if hasattr(current_model, field):
                            exist_field = current_model._fields.get(field)
                            print(" Yes wrolds  ", exist_field)
                            if exist_field:
                                if exist_field.type in ['many2many']:
                                    print(" yes this is trying to worst case ", exist_field.comodel_name )
                                    relation_model = exist_field.comodel_name
                        for element in elements:
                            element = element.strip()
                            if element.isdigit() and relation_model:
                                record_search = self.env[relation_model].sudo().search([('id','=', int(element))],limit=1)
                                if record_search:
                                    m2m_ids.append(int(record_search.id))
                            else:
                                if relation_model:
                                    record_search = self.env[relation_model].sudo().search([('name', '=', element)], limit=1)
                                    if not record_search:
                                        record_search = self.env[relation_model].sudo().create({'name':element})
                                    if record_search:
                                        m2m_ids.append(record_search.id)
                        udpate_dict[field] = [(6, 0, m2m_ids)]
                    except Exception as e:
                        _logger.info("set unset error for many2many %s : ",str(e))
                if field_type == 'many2one':
                        try:
                            many2one_id = None
                            relation_model = None
                            if hasattr(current_model, field):
                                exist_field = current_model._fields.get(field)
                                print(" Yes wrolds  ", exist_field)
                                if exist_field:
                                    if exist_field.type in ['many2one']:
                                        print(" yes this is trying to worst case ", exist_field.comodel_name )
                                        relation_model = exist_field.comodel_name
                            if value.isdigit():
                                if relation_model:
                                    record_search = self.env[relation_model].sudo().search([('id','=', int(value))],limit=1)
                                    if record_search:
                                        many2one_id = record_search.id
                            else:
                                if relation_model:
                                    search_id = self.env[relation_model].search([('name', '=', value)],limit=1)
                                    if search_id:
                                        many2one_id = search_id.id
                            udpate_dict[field] = many2one_id
                        except Exception as e:
                            _logger.info("set unset error for many2one_id %s :", str(e))

            if field_type in ['binary','many2one_reference','one2many','reference'] and value:
                _logger.info("** we will handle after get proper request in set/unset")

            if field_type and not value:
                udpate_dict[field] = ''

            return udpate_dict
     
      

    def write_decision_stage(self,record_obj,value):
        print(" in write_decision_stage value ;", value)
        time.sleep(0.5)
        _logger.info(" previsu stage : %s", record_obj.x_o2b_stage)
        msg = record_obj.x_o2b_stage + '---> ' + value + '( Stage )'
        from_stage = record_obj.x_o2b_stage.replace('_', ' ').upper() if record_obj.x_o2b_stage else record_obj.x_o2b_stage
        to_stage = value.replace('_', ' ').upper() if value else value
        
        msg = html_msg = f"""
            <div>
                <h5><b>&#x2022;</b> {from_stage} <b>&#x2794; </b><span style="color: #158181;"> {to_stage}</span> ( Stage )</h5>
            </div>
            """
        if record_obj.x_o2b_stage != value:
            record_obj.with_user(1).sudo().message_post(body=msg)
        record_obj.sudo().write({'x_o2b_stage': value})
        _logger.info("after change decisons step value %s",record_obj.x_o2b_stage)

        # call process manger method to update admin panel data
        self.update_admin_panel(record_obj)
        # call process manger method to update admin panel data

    # Univarsal Schedular
    def _universal_schedular(self,model_obj, model_name):
        # _logger.info(" ****process manager schedular is running*****")
        # try:
            p_record = self.env['o2b.process.manager'].sudo().search([('model','=',model_name)])
            _logger.info("*** process manager have record count: %s : ",len(p_record))
            for rec in p_record:
                _logger.info(" ** record : %s and model: %s  and node id : %s ",rec.record_id,rec.model,rec.current_id)
                record_id = int(rec.record_id)
                cur_record_model = self.env[rec.model].sudo().browse(record_id)
                current_stage = cur_record_model.x_o2b_stage
                _logger.info("*** Univeral model current stage : %s  for model %s : ",current_stage,rec.model)
                curr_id = ''
                cur_step = ''
                curr_type = ''
                next_id = ''
                next_step = ''
                next_type  = ''
                # process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model),('current_stage','=',current_stage)])
                process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model),('current_stage_id','=',rec.current_id)])
                _logger.info(" ** current process record exist or not: %s ", str(process))
                if process:
                    curr_id = process.current_stage_id
                    cur_step = process.current_stage
                    curr_type = process.activity_type
                    next_id = process.next_stage_id
                    next_step = process.next_stage
                    _logger.info(" ** universal schedular next id is %s : ", next_id)
                    if next_id:
                        self.remark_history(rec.model,rec.record_id,None,process)
                        next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',next_id)],limit=1)
                
                        self.handle_set_unset(rec,process,next_obj)
                        if next_obj.node_type not in ['decision','email','email_verify']:
                            print(" satnsoh ", next_obj)
                            print(" satnsoh ", next_obj.node_type)
                            _logger.info(" ** in normal stage move and type is :: %s ",next_obj.node_type,)
                            _logger.info(" ** in normal stage value is %s :",next_obj.stage_value,)
                            self.write_decision_stage(cur_record_model,next_obj.stage_value)
                            cur_record_model.sudo().write({
                                'x_o2b_stage': next_obj.stage_value,
                                'x_done': True,
                                })
                            rec.write({'active' : False})

                        if next_obj.node_type in ['decision']:
                            _logger.info(" ** in decision next step is desision: %s ", next_obj.node_type)
                            _logger.info(" ** in decision stage value is %s :",next_obj.stage_value,)
                            p_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model.strip()),('current_stage_id','=',next_id)])
                            p_curr = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',next_id)],limit=1)
                            vals= {
                                'model_stage'   : cur_record_model.x_o2b_stage ,
                                'current_id'    : p_stage.current_stage_id,
                                'current_name'  : p_stage.current_stage ,
                                'next_id'       : p_stage.next_stage_id ,
                                'next_name'     : p_stage.next_stage ,
                                }

                            print(" after writing new value ", cur_record_model.x_o2b_stage)
                            print(" next object value: ", next_obj.stage_value)
                            self.write_decision_stage(cur_record_model,next_obj.stage_value)
                            rec.sudo().write(vals)
                            # self.remark_history(rec.model,rec.record_id,None,process)
                            self.handle_decision_records(rec,next_obj)
                          
                        if next_obj.node_type in['email']:
                            _logger.info(" ** we are in email step reocrd for current record id %s : ", rec.record_id)
                            email_current_id_obj = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model.strip()),('current_stage_id','=',rec.current_id)],limit=1)
                            record_mail = self.env['o2b.process.modular.email'].search([('model_name','=',rec.model.strip()),('current_node_id','=', email_current_id_obj.next_stage_id)],limit=1)
                            _logger.info("** all mail triiger list * %s ", str(record_mail))
                            current_step = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_mail.current_node_id)],limit=1)
                            next_step = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_mail.next_step_id)],limit=1)
                            email_next_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',record_mail.next_step_id)],limit=1)
                            if email_next_obj.node_type not in ['decision']:
                                self.write_decision_stage(cur_record_model,next_step.stage_value)
                                self.handle_set_unset(rec,next_obj,next_obj)
                                cur_record_model.sudo().write({
                                    'x_o2b_stage': next_step.stage_value,
                                    'x_done': False,
                                    })
                                # handle mail content here and sending mail
                                new_mail_record = self.env['o2b.process.email'].sudo().create({
                                    'record_id'     : rec.record_id,
                                    'model'         : rec.model,
                                    'current_id'    : rec.current_id,
                                    'next_id'       : record_mail.next_step_id,
                                    'recipient'     : record_mail.recipient ,
                                    # 'recipient'     : record_mail.recipient ,
                                    'mail_subject'  : record_mail.mail_subject ,
                                    'mail_body'     : record_mail.mail_body ,
                                    # 'create_date'   : record_mail.next_stage_id ,
                                    # 'mail_send_date': record_mail.next_stage_id ,
                                    # 'attachment_ids': record_mail.next_stage_id ,
                                    'mail_count'    : record_mail.mail_limit ,
                                    'is_active'     : True ,
                                    'is_sent'       : False ,
                                    'mail_trigger'  : record_mail.mail_trigger ,
                                    })
                                # call fetch attachment and update email table record
                                self._fetch_attachment(record_mail,new_mail_record)
                            if email_next_obj.node_type in['decision']:
                                print(" ** after email next step is decion type is:: ", email_next_obj.node_type)
                                print(" **** we are in emain next decision: next:",email_next_obj.process_node_id)
                                # create new record in email table
                                new_mail_record = self.env['o2b.process.email'].sudo().create({
                                'record_id'     : rec.record_id,
                                'model'         : rec.model,
                                'current_id'    : rec.current_id,
                                'next_id'       : record_mail.next_step_id,
                                'recipient'     : record_mail.recipient ,
                                'mail_subject'  : record_mail.mail_subject ,
                                'mail_body'     : record_mail.mail_body ,
                                # 'create_date'   : record_mail.next_stage_id ,
                                # 'mail_send_date': record_mail.next_stage_id ,
                                # 'attachment_ids': record_mail.next_stage_id ,
                                'mail_count'    : record_mail.mail_limit ,
                                'is_active'     : True ,
                                'is_sent'       : False ,
                                'mail_trigger'  : record_mail.mail_trigger ,
                                })
                                # call fetch attachment and update email table record
                                self._fetch_attachment(record_mail,new_mail_record)
                                # call new decsion handling method
                                self.write_decision_stage(cur_record_model,email_next_obj.stage_value)
                                self.handle_decision_records(rec,email_next_obj)
                                
                                # my code for email
                            if email_next_obj.node_type in['email']:
                                _logger.info(" ** again email type  %s : ", rec.record_id)
                                record_mail = self.env['o2b.process.modular.email'].search([('model_name','=',rec.model.strip()),('current_node_id','=', email_next_obj.process_node_id)],limit=1)
                                # print(" santosh record main::", record_mail.current_step)
                                # print(" santosh rec.currend",rec.current_id)
                                # print(" santosh rec.currend id ",rec)
                                rec.write({
                                    'current_id': email_next_obj.process_node_id
                                    })
                                
                                time.sleep(1)
                                print(' after chanign rec id ', rec.current_id)

                                print(" record main triiger vaoue ", record_mail.mail_trigger)
                                mail_queue = self.env['o2b.process.email'].sudo().create({
                                    'record_id'     : rec.record_id,
                                    'model'         : rec.model,
                                    'current_id'    : rec.current_id,
                                    'next_id'       : record_mail.next_step_id,
                                    'recipient'     : record_mail.recipient ,
                                    'mail_subject'  : record_mail.mail_subject ,
                                    'mail_body'     : record_mail.mail_body ,
                                    'mail_count'    : record_mail.mail_limit ,
                                    'is_active'     : True ,
                                    'is_sent'       : False ,
                                    'mail_trigger'  : record_mail.mail_trigger ,
                                    })
                                # call fetch attachment and update email table record
                                self._fetch_attachment(record_mail,new_mail_record)
                                # my code for email
                            else:
                                rec.write({'active' : False})

                        if next_obj.node_type in['email_verify']:
                            _logger.info(" ** we are in email_verified next id %s : ", rec.record_id)
                            self.handle_email_verify(process,next_obj,rec.record_id)
                            email_current_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model),('current_stage_id','=',next_obj.process_node_id)])
                            email_verified_obj = self.env['o2b.process.modular.statusbar'].sudo().search([('model_name', '=',rec.model.strip()),('process_node_id','=',email_current_stage.next_stage_id)],limit=1)
                            if email_verified_obj.node_type not in ['decision','email','email_verify']:
                                print(" ** after email this is simple step to forward simply type : ", email_verified_obj.node_type)
                                self.write_decision_stage(cur_record_model, email_verified_obj.stage_value)
                                self.handle_set_unset(rec,email_verified_obj,email_verified_obj)
                                cur_record_model.sudo().write({
                                    'x_o2b_stage': email_verified_obj.stage_value,
                                    'x_done': True,
                                    })
                                # self.remark_history(rec.model,rec.record_id,None,process)
                            if email_verified_obj.node_type in['decision']:
                                # # create new change stage
                                # cur_record_model.sudo().write({
                                # 'x_o2b_stage': email_verified_obj.stage_value,
                                # # 'x_done': True,
                                # })
                                print(" yes email verfiyfed  next id deciosn: ")
                                self.write_decision_stage(cur_record_model,email_verified_obj.stage_value)
                                self.handle_decision_records(rec,email_verified_obj)
                            else:
                                rec.write({'active' : False})
                              
                            if email_verified_obj.node_type in['email']:
                                self.write_decision_stage(cur_record_model,email_verified_obj.stage_value)
                                print(" ******we are in type mail emailverified ====>email rec.current_id : ",rec.current_id )
                                email_current_id_obj = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model.strip()),('current_stage_id','=',rec.current_id)],limit=1)
                                vals= {
                                'record_id'     : rec.record_id,
                                'model'         : rec.model ,
                                'current_id'    : email_current_id_obj.next_stage_id,
                                }
                                p_manager_record = self.env['o2b.process.manager'].sudo().create(vals)
                                rec.write({'active':False})
                            else:
                                rec.write({'active' : False})
                    else:           
                        _logger.info("next id false means end or stuck in process manager due next id false %s ", next_id)
                        pre_step = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',rec.model.strip()),('current_stage_id','=',rec.current_id)],limit=1)
                        # print(" *** pre step  ", pre_step.previous_stage_id)
                        # print(" *** next step  ", pre_step.next_stage_id)
                        # print(" *** current step  ", pre_step.current_stage_id)
                        # print(" *** current step  ", pre_step.previous_stage, pre_step.current_stage,pre_step.next_stage)
                        rec.write({
                            'current_id': pre_step.previous_stage_id if pre_step.previous_stage_id else rec.current_id
                            })

                        cur_record_model.write({
                            'x_done': True
                            })
        # except Exception as e:
        #     _logger.info(" ** process manager table %s ",str(e))
        #     cur_record_model.write({'x_done': True})
        #     pass                  

# o2b mail sender service method
    def _mail_sender(self):
        ex_email_obj = None
        ex_mode_obj = None
        ex_receipent = None
        try:
            _logger.info("** we are in mail sender service:")
            email_records = self.env['o2b.process.email'].sudo().search([('is_sent','=',False)])
            for email_queue in email_records:
                mail_create_time = email_queue.create_date
                _logger.info("mail queue current data: %s", email_queue)
                recipient  = ""
                msg_body = ""
                msg_subject = ""
                if email_queue:
                    record_model = self.env[email_queue.model].sudo().browse(int(email_queue.record_id))
                    ex_email_obj = email_queue
                    ex_mode_obj = record_model
                    if record_model:
                        _logger.info("**** acutal email extact from node value() %s", email_queue.recipient)
                        if email_queue.recipient:
                            match = re.match(r'^[a-zA-Z0-9_]+', email_queue.recipient)
                            if match:
                                result = match.group(0)
                                if hasattr(record_model, result):
                                    recipient = getattr(record_model, result)
                                    ex_receipent = getattr(record_model, result)
                            else:
                                if hasattr(record_model, 'x_o2b_email'):
                                    recipient = getattr(record_model, 'x_o2b_email')
                                    ex_receipent = getattr(record_model, 'x_o2b_email')
                        _logger.info("** acutual email address where email send : %s ",recipient)
                    msg_body = email_queue.mail_body
                    msg_subject = email_queue.mail_subject
                    _logger.info(" trying to recepient : %s: for record id: %s ", recipient,str(email_queue))
                    # trying to create new template oject to send mail
                    model_record = self.env['ir.model'].sudo().search([('model','=',email_queue.model)],limit=1)
                    _logger.info(" ** email model applied id found or not %s and model name %s  ", str(model_record),email_queue.model)
                    pattern = r'{{\s*object\.(\w+(?:\.\w+)*)\s*}}'
                    # Find all matches and create a list of tuples (object, field_name)
                    matches = re.findall(pattern, msg_body)
                    # Create a list of tuples (object, field_name)
                    object_field_pairs = [('object', match) for match in matches]
                    # replace {{object.
                    msg_body =  msg_body.replace("{{object.","")
                    msg_body = msg_body.replace("}}"," ")
                    for data in object_field_pairs:
                        dynamic_obj,technical_field = data
                        target_string = technical_field
                        if hasattr(record_model, technical_field):
                            field_value = getattr(record_model, technical_field)
                            msg_body = msg_body.replace(technical_field,str(field_value))
                            print(" ** compelte dynamic emai template: ", msg_body)
                        elif '.' in technical_field:
                            base_field, sub_field = technical_field.split('.', 1)
                            _logger.info(" in relation fields base field : %s and subfiled :%s", str(base_field),str(sub_field))
                            if hasattr(record_model, base_field):
                                parent_obj = getattr(record_model, base_field)
                                parent_obj = parent_obj[:1]
                                
                                _logger.info(" ** parent_obj %s", str(parent_obj))
                                _logger.info(" ** parent_obj %s", str(parent_obj._name))
                          
                                if hasattr(parent_obj, sub_field):
                                    child_obj = getattr(parent_obj, sub_field)
                                    _logger.info(" ** child object : %s", child_obj)
                                    msg_body = msg_body.replace(technical_field,str(child_obj))
                                    _logger.info(' ** final msg_body in relational %s', msg_body)
                    print(" all pais of oject ::::::::",object_field_pairs )
                    context = {
                        'object'    : record_model,  
                    }
                    odoo_mail_template = self.env['mail.template'].search([('name', '=', 'oflow_email_template')], limit=1)
                    if odoo_mail_template:
                        _logger.info(" ** updating existing mail template ")
                        rendered_body_html = odoo_mail_template.body_html
                        # Prepare the email template dictionary to update it
                        email_template = {
                            'name'          : 'oflow_email_template',
                            'model_id'      : model_record.id if model_record else 97,  
                            'subject'       : msg_subject,
                            'description'   : msg_subject,  
                            'body_html'     : msg_body,  
                            'email_from'    : 'info@oflowai.com',
                            'use_default_to': False,
                            'email_to'      : recipient,
                        }
                        odoo_mail_template.sudo().write(email_template)
                    else:
                        _logger.info(" ** creating new mail template ")
                        rendered_body_html = odoo_mail_template.body_html
                        # Create the email template
                        email_template = {
                            'name'          : 'oflow_email_template',
                            'model_id'      : model_record.id if model_record else 97,
                            'subject'       : msg_subject,
                            'description'   : msg_subject,
                            'body_html'     : msg_body,
                            'email_from'    : 'info@oflowai.com',
                            'use_default_to': False,
                            'email_to'      : recipient,
                        }
                        odoo_mail_template = self.env['mail.template'].sudo().create(email_template)
                    # Handle attachments
                    attachment_tuples = [(4, attachment.id) for attachment in email_queue.attachment_ids]
                    odoo_mail_template.attachment_ids = attachment_tuples
                    time_count = 0
                    data_format = 'minutes'
                    # scheduled when email should trigger
                    _logger.info("*** schedual data from table %s", email_queue.mail_trigger)
                   
                    if not email_queue.mail_trigger.isdigit():
                        schedule_data = json.loads(email_queue.mail_trigger)
                        time_count = int(schedule_data['timeCount'])
                        data_format = schedule_data['timeFormat']
                    else:
                        time_count = 0
                        data_format = 'minutes'

                    if time_count > 0 :
                        time_units = {
                            'second'    : 1,
                            'minutes'   : 60,
                            'hours'     : 3600,
                            'days'      : 86400,
                            'weeks'     : 604800,
                            'months'    : 2628000  
                            }
                        time_in_seconds = time_count * time_units[data_format]
                        print("time in seconds ", time_in_seconds)
                        current_time = datetime.now()
                        mail_scheduled_time = mail_create_time
                        try:
                            future_time = mail_scheduled_time + timedelta(seconds=time_in_seconds)
                            _logger.info("Current time %s:" ,str(current_time))
                            _logger.info("future  time %s:" ,str(future_time))
                           
                            # Compare current time with future time (if the current time has passed the future time)
                            if current_time >= future_time:
                                # send record and show record before mail sending
                                record_model.write({
                                    'x_done': True,
                                    })
                                _logger.info("Time condition met. email is sending")
                                mail_id = odoo_mail_template.sudo().with_context(context).send_mail(record_model.id, force_send=True)
                                email_queue.sudo().write({
                                    'is_sent':True,
                                    'active' :False
                                    })
                            else:
                                _logger.info("Time condition not met yet.")
                        except ValueError as e:
                            _logger.info("error while schedular the email %s", str(e))
                    else:
                        _logger.info(" email is schedulad immediate. count value is %s",str(time_count))
                        # send record and show record before mail sending
                        record_model.write({
                            'x_done': True,
                            })
                        mail_id = odoo_mail_template.sudo().with_context(context).send_mail(record_model.id, force_send=True)
                        email_queue.sudo().write({
                        'is_sent':True,
                        'active' :False
                        })
                        _logger.info(" mail sent status : %s", str(mail_id))
                    # Clean up attachments (clear the attachment relation)
                    odoo_mail_template.attachment_ids = [(5, 0, 0)]          
        except Exception as e:
            ex_msg_body = "<p> Sorry there is some error in email template .please contact to administrator.</p><p>For now we will send the record to next stage and clear email queue.</p><p> Exception is " + str(e) + " </p> <p> Your Content is "+ex_email_obj.mail_body + "</p>" 
            ex_email_obj.write({'active':False})
            mail_values = {
            'subject'   : ex_email_obj.mail_subject,
            'body_html' : ex_msg_body ,
            'email_to'  : ex_receipent,
            'email_from': 'info@oflowai.com',
            }
            mail = self.env['mail.mail'].sudo().create(mail_values)
            mail_sent = mail.sudo().send(auto_commit=True)
            ex_mode_obj.write({
                'x_done': True,
                })
            _logger.info(" some error in sending email :%s",str(e))

    # o2b mail sender service method
    def _fetch_attachment(self,record_mail,new_mail_record):
        try:
            _logger.info("** we are in fetching attachment from middleware service")
            # call node fetch api to get attachents and update process email table
            mid_base_url = self.fetch_process_obj(record_mail.process_id,record_mail.process_name)
            _logger.info("  *** middleware base url for attachment: %s ", mid_base_url)
            if not mid_base_url:
                mid_base_url = 'http://192.168.1.38:3636'
                mid_base_url = 'http://122.160.26.224:3636' 
                mid_base_url = 'https://node.oflowai.com'
            end_point = '/fetch/attachment'
            url = mid_base_url + end_point
            _logger.info(" **final url for attachment : %s ", url)
            headers = {
            'Content-Type': 'application/json',
            }
            data = {
            'key'   : 'o2b_technologies',
            'id'    : record_mail.template_id
            }

            response = requests.post(url, json=data, headers=headers)
            _logger.info(" attachment fetch response  : %s", str(response.status_code))
            if response.status_code == 200 and response.status_code != 404:
                response_data = response.json()
                # Extract attachment_file data
                attachment_files = response_data.get('message', [{}])[0].get('attachment_file', [])
                attachment_id = []
                if attachment_files:
                    for file in attachment_files:
                        file_data = bytes(file['data'])
                        # encoded_data = base64.b64encode(file_data).decode('utf-8')
                        new_file = self.env['ir.attachment'].sudo().create({
                        'name': random.randint(1, 100),
                        'type': 'binary',
                        'datas': base64.encodebytes(file_data),
                        'res_model': 'o2b.process.mail',
                        'res_id': new_mail_record.id,
                        'mimetype': 'application/pdf'
                        })
                        print(" *** new file: ", new_file)
                        attachment_id.append(new_file.id)
                        new_mail_record.sudo().write({
                        'attachment_ids': attachment_id,
                        })
                        print(" attachmetn id update or nO : ", new_mail_record.attachment_ids)
        except Exception as error:
            _logger.info("=====Exception while fetching and updating email table template %s", str(error))
            pass



# ****************email verifiy that email is exist or ot***************************
    @api.model
    def handle_email_verify(self, cur_obj, next_obj, record_id):
        # _logger.info("Just validating email verify step cur_obj: %s", str(cur_obj))
        _logger.info("Just validating email verify step main_obj: %s and record_id: %s", str(next_obj), str(record_id))
        process_id = cur_obj.process_id
        model = cur_obj.model_name
        current_id = next_obj.process_node_id
        # Search for the email verification object
        email_verified_obj = self.env['o2b.process.modular.emailverified'].sudo().search([
            ('process_id', '=', process_id),
            ('current_id', '=', current_id)
        ],limit=1)
        
        email_list = None
        if email_verified_obj:
            try:
                # Safely parse the email list stored in the record
                if email_verified_obj.email_verify_list:
                    email_list = ast.literal_eval(email_verified_obj.email_verify_list)
            except (ValueError, SyntaxError) as e:
                _logger.error("Failed to parse email_verify_list. Error: %s", e)
        _logger.info(" ########## email verfify list %s ", str(email_list))
        if email_list:
            # Fetch the target record model
            record_model = self.env[model].sudo().browse(int(record_id))
            print("Current record in model:", record_model)
            for email in email_list:
                # Check if the field exists in the model
                if hasattr(record_model, email):
                    field_value = getattr(record_model, email)
                    print(f"Actual value for email {email}: {field_value}")
                    
                    if field_value:
                        # Proceed with email verification (e.g., call verify_email_exist function)
                        print(f"Email check status for {email}: {field_value}")
                        # email_result = self.verify_email_exist(field_value)
                        email_result = self.validate_email_address(field_value)
                        update_dict = {}
                        print(" email result ", email_result)
                        if email_result and email_result == True:
                            update_dict[email+'_status'] = email_result
                        else:
                            update_dict[email+'_status'] = email_result
                        record_model.write(update_dict)
                    else:
                        _logger.warning("Field value for %s is empty or None.", email)
                else:
                    _logger.warning("Field %s does not exist in the model %s.", email, model)
# ****************email verifiy that email is exist or ot***************************

    @api.model
    def verify_email_exist(self,email):

        email_verified_status = False
        format_verifty_status = False
        dns_check_status  = False
        _logger.info("*** in verify_email_exist : %s",email)
        
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        format_verifty_status = re.match(regex, email) is not None
        try:
            dns_check_status = validate_email(email, check_deliverability=False)
            email = dns_check_status.normalized

        except EmailNotValidError as e:
            _logger.info("email respose check staus %s", str(e))

        if dns_check_status and format_verifty_status:
            email_verified_status = True
            return email_verified_status
        else:
            return False

# calling o2b technologies com email validator
    def validate_email_address(self, email):
        validation = False
        _logger.info(" validation of current email address is : %s ", email)
        url = f"https://crm.o2btechnologies.com/email/validation?email={email}"
        _logger.info(" ** complete url %s", url)

        try:
            response = requests.get(url)
            print(" compltet response ",response)
            
            if response.status_code == 200:
                result = response.json()
                _logger.info(" o2b api response for email verify %s", result)
                validation = result.get('validation', False)
            else:
                validation = False
               
        except requests.exceptions.RequestException as e:
            validation = False
        return validation
          

    # schedualr for release after specefied time. here specefied time is 5 minutes **** start here
    @api.model
    def _global_lock_release_schedular(self):
        SPECIFIED_TIME = 1
        current_time = datetime.now()
        lock_records= self.env['o2b.process.lock'].sudo().search([])
        for record in lock_records:
            _logger.info(" lock record id : %s  is processing to relase the record .", str(record))
            if record.lock_date <=  current_time - timedelta(minutes=SPECIFIED_TIME):
                record.write({
                    'active' : False
                    })
        # sening pending emails
        # self.sudo()._mail_sender()
        try:
            self.sudo()._mail_sender()
        except Exception as e:
            _logger.info(" calling self.sudo()._mail_sender() %s ",str(e))

    # schedualr for release after specefied time. here specefied time is 5 minutes **** end here

    # schedualr for sending email which are pending in process email table**** start here
    # @api.model
    # def _global_lock_release_schedular(self):
    #     self._mail_sender()
    # # schedualr for sending email which are pending in process email table**** end here


    # create process manager record :for accepting request from json api  or web form api
    def process_manager_insert(self,process_id,record_id,request_type):
        _logger.info("** process manager insert for webform and json api: %s ",record_id)
        print(" process id : ", process_id)
        print(" process record_id : ", record_id)
        print(" process request type : ", request_type)

        process_stage = None
        if request_type == 'json_api':
            process_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('process_id','=',process_id.strip()),('activity_type','=','start')],limit=1)
        if request_type == 'webform':
            process_stage = self.env['o2b.process.modular.stage'].sudo().search(['&',('process_id','=',process_id.strip()),('activity_type','=','webform')],limit=1)

        print(" insert in process mangaer dta ", process_stage)
        if process_stage:
            print(" process_stage",process_stage)
            p_manager_record = self.env['o2b.process.manager'].sudo().search(['&',('model','=',process_stage.model_name.strip()),('record_id','=',record_id)])
            if p_manager_record:
                _logger.info(" ** process record model%s: and current step %s  ", p_manager_record.model,p_manager_record.current_id)
                # update
                p_manager_record.sudo().write({
                    'record_id'     : record_id ,
                    'model'         : process_stage.model_name.strip() ,
                    'current_id'    : process_stage.current_stage_id ,
                    })
            else:
                # create
                p_manager_record.sudo().create({
                    'record_id'     : record_id ,
                    'model'         : process_stage.model_name.strip() ,
                    'current_id'    : process_stage.current_stage_id ,
                    })


# *************************** LIST VIEW METHOD *******************************
    # THIS METHOD WILL CALL WHEN DONE BUTTON CLICK VIA LIST VIEW
    @api.model
    def process_list_record(self, selected_ids, node_id, model,user_id):
        _logger.info("done method called process_list_record %s", model)
        print(" selected records : ", selected_ids  , " type of records is ", type(selected_ids))
        print(" selected node_id : ", node_id)
        print(" selected model : ", model)
        print(" selected user_id : ", user_id)
        if model:
            model = model.strip()

        if node_id:
            node_id = node_id.strip()

        pass_record = []
        fail_record = []
        fail_msg  = ''
        pass_msg = ''
        for record_id in selected_ids:
            # self.env[model].sudo().pre(self)
            if record_id:
                record_id = int(record_id)
                current_record_model = self.env[model].sudo().browse(record_id)
                current_stage = current_record_model.x_o2b_stage
                _logger.info("*** process_list_record : %s  for model %s : ",current_stage,model)
                # comment below line if end stage done button hide:
                process = self.env['o2b.process.modular.stage'].sudo().search(['&',('model_name','=',model.strip()),('current_stage_id','=',node_id)] , order='id desc',limit=1)
                # ***field check that is require
                res = self.list_view_required_field_check(model,record_id,node_id)
                # for cross symbol code: \u2716 and right heavy symbol : \u2714
                if res:
                    label = ''
                    if res[0] == 'Failed':
                        fail_record.append(record_id)
                        if res[3]=='TODO':
                            label = ' On Todo form.'
                        if res[3] == 'DOCUMENT':
                            label = ' On Document Form.'
                        # fail_msg = fail_msg + '\n 🔴 Record ID : ' + str(record_id) + ' could not be processed. Please provide a value for the "' +  res[2] + '" field.  ❌'
                        fail_msg += f'\n❌ Record ID: {record_id} could not be processed. Please provide a value for the "{res[2]}" field. {label}'
                    else:
                        result = self.check_recod_is_locked(model, record_id,user_id,node_id)
                        print(" check record is locker result ", result)
                        if result[0]=='LOCK':
                            fail_msg += f'\n❌ Record ID: {record_id} could not be processed. Record is Locked by Another User ({result[1]})'

                        if res[0] == 'Pass' and result[0] =='UNLOCK':
                            pass_record.append(record_id)
                            # pass_msg = pass_msg + '\n 🟢  Record ID : ' + str(record_id) + ' has been processed successfully.  ✅' 
                            pass_msg += f'\n✅ Record ID: {record_id} has been processed successfully.'
                            print(" list view field check : ", res)
                # ***field check that is require
                            if process.next_stage_id:
                                code = process.model_name.replace('.','_').lower()
                                reference_exist = None
                                if hasattr(current_record_model, 'x_reference_no'):
                                    reference_exist = getattr(current_record_model, 'x_reference_no')
                                current_record_model.sudo().write({
                                    'x_done'         : False,
                                    'x_reference_no' : reference_exist if reference_exist else self.env['ir.sequence'].next_by_code(code),
                                    })
                                self.process_manager_crud(model, record_id,node_id)
        return [True,pass_record,fail_record,pass_msg,fail_msg]


    # write method which confirm reuired field is emply or not:
    @api.model
    def list_view_required_field_check(self, model, record_id,node_id):
        response = []
        _logger.info("required_field_check model %s", model)
        _logger.info("required_field_check node id %s", node_id)
        if model:
            model = model.strip()
        if record_id and node_id:
            _logger.info("**********record id: %s ", record_id)
            record_id = int(record_id)
            current_record_model = self.env[model].sudo().browse(record_id)
            current_stage = current_record_model.x_o2b_stage
            _logger.info("*** decision action : %s  for model %s : ",current_stage,model)
            model_field = self.env['ir.model.fields'].sudo().search(['&',('model','=',model.strip()),('ttype','=','selection'),('name','=','x_o2b_stage')])
            selection_field = self.env['ir.model.fields.selection'].sudo().search(['&',('field_id','=',model_field.id),('value','=',current_stage.strip())])
            required_form_fields = self.env['o2b.process.modular.field.method'].sudo().search([('model_name', '=',model),('form_id','=',node_id),('is_required','=',True)])
            _logger.info("** all required fields on current form %s ", str(required_form_fields))
            response = ['Pass', '','','']
            for rec_field in required_form_fields:
                check_type ='NORMAL'
                if rec_field.is_todo_field:
                    check_type = "TODO"
                if rec_field.is_document_field:
                    check_type = "DOCUMENT"
                if hasattr(current_record_model, rec_field.field_name):
                    field_value = getattr(current_record_model, rec_field.field_name)
                    if not field_value:
                        response = ['Failed', rec_field.field_name,rec_field.field_label,check_type]
                        return response
            return response
# *************************** LIST VIEW REQUIRED METHOD *******************************
