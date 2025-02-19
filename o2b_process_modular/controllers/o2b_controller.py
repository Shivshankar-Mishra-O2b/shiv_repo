from odoo import api,fields,models, tools
from odoo import http
from odoo.http import request
from odoo.http import Response
import json,os
import base64
from base64 import b64encode
from bs4 import BeautifulSoup
import re
from io import BytesIO
from odoo.exceptions import AccessDenied
from ast import literal_eval
import logging
import xml.etree.ElementTree as ET
import ast
import random
# import for inbuit sql method for database query validation
from odoo.modules.db import FunctionStatus
from odoo.osv.expression import get_unaccent_wrapper
from odoo.sql_db import TestCursor
from odoo.tools import (config, existing_tables, lazy_classproperty,
                        lazy_property, sql, Collector, OrderedSet)
from odoo.tools.func import locked
from odoo.tools.lru import LRU
import datetime
from xml.dom.minidom import parseString
from odoo.service import db, security
import werkzeug
import contextlib
import time
import subprocess
from odoo import fields
from odoo import tools

# from datetime import datetime


# end import for sql related
_logger = logging.getLogger(__name__)
class O2bDragDrop(http.Controller):
    odoo_start_tag = '''
    <odoo>

    <data>
    '''
    odoo_end_tag = '''
    </data>
    </odoo>
    '''
    odoo_form_tag_start = '''
    <record model="ir.ui.view" id="form_id">
    <field name="name">form_name</field>
    <field name="model">test.model</field>
    <field name="arch" type="xml">
    <form string="form_name">
    <sheet>
    <group>
    '''
    odoo_form_tag_end = '''
    </group>
    </sheet>            
    </form>
    </field>
    </record>
    '''
    
#========================project start code ================================================


    # def admin_mdm_group_category(self,process,custom_model,mdm,admin):
    def admin_mdm_group_category(self,process,custom_model):
        _logger.info(" ** we are in admin_mdm_group_category")
        print(" ** we are in admin_mdm_group_category **",process,custom_model)
        admin_group  = process.strip().lower().replace(' ','_') + '_admin'
        mdm_group  = process.strip().lower().replace(' ','_') + '_mdm'
        
        FIXED_CATEGORY = 'Oflow'
        is_category_exist = request.env['ir.module.category'].sudo().search([('name','=',FIXED_CATEGORY )],order='create_date asc, id asc', limit=1)
        if not is_category_exist:
            is_category_exist.with_user(2).sudo().create({
            'name':FIXED_CATEGORY,
            'sequence': '',
            })
        is_admin_group = request.env['res.groups'].sudo().search([('name','=',admin_group )],order='create_date asc, id asc', limit=1)
        if not is_admin_group:
            is_admin_group.with_user(2).sudo().create({
            'name':admin_group,
            'category_id':is_category_exist.id ,
            })
          
        is_mdm_group = request.env['res.groups'].sudo().search([('name','=',mdm_group )],order='create_date asc, id asc', limit=1)
        if not is_mdm_group:
            is_mdm_group.with_user(2).sudo().create({
            'name':mdm_group,
            'category_id':is_category_exist.id ,
            })
          
        ir_model_data_admin = request.env['ir.model.data'].sudo().search([('name','=', admin_group)])
        if not ir_model_data_admin:
           ir_model_data_admin.with_user(2).sudo().create({
            'name'      : admin_group,
            'res_id'    : is_admin_group.id,
            'module'    : 'base',
            'model'     : 'res.groups'  
            })

        ir_model_data_mdm = request.env['ir.model.data'].sudo().search([('name','=', mdm_group)])
        if not ir_model_data_mdm:
           ir_model_data_mdm.with_user(2).sudo().create({
            'name'      : mdm_group,
            'res_id'    : is_mdm_group.id,
            'module'    : 'base',
            'model'     : 'res.groups'  
            })

        _logger.info("*** category obj %s ,admin group obj: %smodel data: %s",is_category_exist,is_admin_group, ir_model_data_admin)
        _logger.info("*** category obj %s ,mdm group obj: %smodel data: %s",is_category_exist,is_mdm_group, ir_model_data_mdm)

        # code to give process main access group
        main_app_group = []
        record_process_group = request.env['o2b.process.modular.group'].sudo().search([('process_name', '=',process),('activity_type','in',['main app'])])
        _logger.info(" ***admin and mdm access group obj  %s",record_process_group)
        if record_process_group:
            for data in record_process_group:
                if data.activity_name == 'main app':
                    if data.group:
                        group_name = data.group.split('.')[-1]
                        _logger.info("*** group name %s and %s  \n", data.group,group_name)
                        main_group_record = request.env['res.groups'].sudo().search([('name', '=',group_name)],limit=1)
                        _logger.info("**** main grup obj ; %s \n",main_group_record)
                        if main_group_record:
                            main_app_group.append(main_group_record.id)
        _logger.info(" ***admin & mdm access list %s",main_app_group)
        is_admin_group.sudo().write({
            'implied_ids': main_app_group
            })
        is_mdm_group.sudo().write({
            'implied_ids': main_app_group
            })
        # code to give process main access group

    def mdm_view_action(self,model):
        _logger.info(" ** we are in mdm view action creation name : *** %s  and model %s",model.name, model.model)
        form_name = 'MDMFORM' + model.model.lower().replace('.','_').strip()
        tree_name = 'MDMTREE' + model.model.lower().replace('.','_').strip()
        print(" form name : ", form_name, " tree name : ",tree_name)
        form_view = f'''
        <form>
        <sheet>
        <h1><center>MDM Form</center></h1> 
        <group>
        <field name="x_name"/>
        </group>
        </sheet>
        </form>
        '''
        tree_view = f'''
        <tree string="MDM LIST">
        <field name="x_name" string='Name'/>
        </tree>
        '''
        form = request.env['ir.ui.view'].sudo().search(['&',('model', '=',model.model),('type','=','form'),('name','=',form_name)],limit=1)
        if not form:
            form = request.env['ir.ui.view'].with_user(2).sudo().create({
                'name'         : form_name,
                'model'        : model.model,
                'type'         :'form',
                'arch_db'      : form_view,
                'arch_prev'    : form_view,
                })
        tree = request.env['ir.ui.view'].sudo().search(['&',('model', '=',model.model),('type','=','tree'),('name','=',tree_name)],limit=1)

        if not tree:
            tree = request.env['ir.ui.view'].with_user(2).sudo().create({
                'name'         : tree_name,
                'model'        : model.model,
                'type'         :'tree',
                'arch_db'      : tree_view,
                'arch_prev'    : tree_view,
                })


        action_name = 'MDMACTION' + model.model.lower().replace('.','_').strip()
        print("action name is : %s ", action_name)
        action = request.env['ir.actions.act_window'].sudo().search(['&',('name','=',action_name),('res_model','=',model.model)],order="id desc" , limit=1)
        if not action:
                action = request.env['ir.actions.act_window'].sudo().create({
                'name'      : action_name,
                'res_model' : model.model ,
                'type'      : 'ir.actions.act_window',
                'view_mode' : 'tree,form' ,
                'view_id'   : tree.id,
                'domain'    : '',
                'context'   : json.dumps({}),
                })

        print("action id :", action)



    def is_string_in_file(self,file_path, search_string):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            if search_string in content:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error: {e}")
            return False

    def rectify_python_code(self,process_modular_obj):
        obj = process_modular_obj
        print(" ****** hello ", obj)
        print(" ****** hello process name ", obj.process_name)
        _logger.info(" ** we in rectify file path: %s",obj.process_name)
        checklist = ['x_reference_no','employee_id','department','employee_name','arrival_date_time','pending_since','work_step_tat','total_tat','total_tat_datetime','total_tat_in_seconds','total_tat = fields.']

        field_content = ''
        for field in checklist:
            _logger.info(" **field name is checking :%s", field)
            proceed = self.is_string_in_file(self.get_module_dir(obj.process_name),field)
            _logger.info(f"proceed condition is {proceed}")
            if not proceed:
                if field =='x_reference_no':
                    field_content += f'''
    x_reference_no = fields.Char(string = 'Record reference Number')
    '''
                elif field =='employee_id':
                    field_content+= f'''
    employee_id = fields.Char(string='Employee ID',default=lambda self: str(self.env.user.employee_id.id))
    '''
                elif field =='department':
                    field_content+= f'''
    department = fields.Many2one('hr.department',string = 'User Department' , default=lambda self: self.env.user.employee_id.department_id)
    '''
                elif field =='employee_name':
                    field_content +=f'''
    employee_name = fields.Many2one('hr.employee',string = 'User Employee' ,default=lambda self: self.env.user.employee_id)
    '''
                elif field =='arrival_date_time':
                    field_content +=f'''
    arrival_date_time = fields.Datetime(string='Arrival Time', default=lambda self: datetime.now())
    '''
                elif field =='pending_since':
                    field_content+= f'''
    pending_since = fields.Date(string='Pending since', default=lambda self: datetime.now())
    '''
                elif field =='work_step_tat':
                    field_content+= f'''
    work_step_tat = fields.Char(string='Work step tat', default=lambda self: '0 days,0 hours, 0 minutes')
    '''
                elif field in ['total_tat','total_tat = fields.']:
                    field_content+= f'''
    total_tat = fields.Char(string='Total TAT', default=lambda self: '0 days,0 hours, 0 minutes')
    '''
                elif field =='total_tat_datetime':
                    field_content +=f'''
    total_tat_datetime = fields.Datetime(string='Total TAT Time', default=lambda self: datetime.now())
    '''
                elif field =='total_tat_in_seconds':
                    field_content +=f'''
    total_tat_in_seconds = fields.Char(string='TAT in Seconds',default=lambda self: '0')
    '''
                else:
                    _logger.info(" no case found to handle %s:", field)

        _logger.info(" ****final field creation string %s ",field_content)
        self.field_declartion(self.get_module_dir(obj.process_name),"_inherit = ['mail.thread', 'mail.activity.mixin']",field_content)


        # writing missing import statement
        imp_statement = f'''
from datetime import datetime'''
        
        import_exist = self.is_string_in_file(self.get_module_dir(obj.process_name),imp_statement)
        if not import_exist:
            self.field_declartion(self.get_module_dir(obj.process_name),"from odoo import models, fields,api,_,os",imp_statement)


        # writing missing method:
        openbraces = '{'
        closebraces = '}'
        search_parameter = 'def oflow_mail_send(self):'
        method = f'''
    # oflow mail send method start here
    def oflow_mail_send(self):
        if self.env.context:
            node_id = self.env.context.get('o2b_node_id')
            if node_id: 
                rec_obj = self.env['o2b.send.email.template'].sudo().search([('model', '=',self._name),('node_id','=',node_id)], limit=1)
                ctx = {openbraces}
                    "default_template_id": int(rec_obj.template_id) if rec_obj else None
                    {closebraces}
                return {openbraces}
                    'type'      : 'ir.actions.act_window',
                    'view_mode' : 'form',
                    'res_model' : 'mail.compose.message',
                    'views'     : [(False, 'form')],
                    'view_id'   : False,
                    'target'    : 'new',
                    'context'   : ctx,
                {closebraces}
    # oflow mail send method end here 
            '''
        method_exist= self.is_string_in_file(self.get_module_dir(obj.process_name),search_parameter)
        if not method_exist:
            self.write_method(self.get_module_dir(obj.process_name), search_parameter,method)


        search_parameter = 'def invoke_todo_list_action(self):'
        method = f'''
    # doc or todo list method start here
    def invoke_todo_list_action(self):
        view_id = self.env.ref('o2b_patient_admission_request_for_lab.o2b_patient_admission_request_for_lab_checklist').id
        form_view = self.env['ir.ui.view'].sudo().browse(view_id)
        if form_view :
            if form_view.model == self._name:
                model= self._name
                node_id = self.env.context.get('o2b_node_id') if self.env.context else None
                action_type = self.env.context.get('action_type') if self.env.context else None
                updated_view = self.env['o2b.process.modular'].dynamic_field_xml(model,node_id,action_type,form_view.arch_db)
                form_view.write({openbraces}
                    'arch_db'   :updated_view,
                    'arch_prev' :updated_view,
                    {closebraces})
            self.ensure_one()
            return {openbraces}
            'type'      : 'ir.actions.act_window',
            'name'      : 'To Do',
            'view_mode' : 'form',
            'res_model' : self._name,
            'views'     : [(view_id, 'form')],
            'target'    : 'current',
            'res_id'    : self.id,
            'domain'    : [('id', '=', self.id)],
            {closebraces}
     # doc or todo list method end here
     '''
        method_exist= self.is_string_in_file(self.get_module_dir(obj.process_name),search_parameter)
        if not method_exist:
            self.write_method(self.get_module_dir(obj.process_name), search_parameter,method)


    def get_module_dir(self,process_name):
        _logger.info(" **** process name for finding file path %s ", process_name)
        module_path = os.path.dirname(__file__)
        parent_dir = os.path.dirname(module_path)
        addon_path = os.path.dirname(parent_dir)
        module_dir = 'o2b_'+process_name.replace(' ','_').lower()
        path = addon_path + '/'+ module_dir+'/models' + '/' + 'models.py'
        _logger.info(" ** model_file path is %s : ", path)
        return path;


    # method to write missing base field of processes
    def field_declartion(self, file_path, search_string, content_to_append):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            line_found = False
            for i, line in enumerate(lines):
                if search_string in line:
                    line_found = True
                    lines.insert(i + 1, '\n' +content_to_append + '\n')
                    break
            if line_found:
                with open(file_path, 'w') as file:
                    file.writelines(lines)
                print(f"Content appended after the line containing '{search_string}'.")
            else:
                print(f"String '{search_string}' not found in {file_path}.")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    
    # method to write method in model.py
    def write_method(self,file_path, search_string,method_content):
        try:
            with open(file_path, 'r') as file:
                content = file.readlines()

            found = any(search_string in line for line in content)

            if not found:
                with open(file_path, 'a') as file:
                    file.write(method_content + '\n')
                _logger.info(f"The string '{search_string}' was not found and has been appended.")
            else:
                _logger.info(f"The string '{search_string}' was already present in the file.")
        
        except Exception as e:
            _logger.error(f"Error: {e}")


    # create method to insert field data into ir.model.field 
    def handle_doctype(self,doc,custom_model,node_id,node_name,process,activity_type):
        _logger.info("**** handle doctype *** ")
        p_id = process.get('process_id')
        p_name = process.get('process_name')
        doc_fields = request.env['o2b.process.modular.field.method'].sudo().search([('process_id', '=',p_id),('is_document_field','=',True),('form_id','=',node_id)])
        if doc_fields:
            doc_fields.unlink()

        for data in doc:
            doc_name = data.get('docType_type')
            doc_desc = data.get('docType_description')
            is_mandaory = data.get('isMandatory')

            technical_field = 'x_'+ doc_name.lower().replace(' ','_').strip() if doc_name else None
            file_name = technical_field+'_filename' if technical_field else None
            if technical_field:
                field = request.env['ir.model.fields'].sudo().search(['&',('name','=',technical_field),('model','=',custom_model.model)],limit=1)
                if not field:
                    field = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name':technical_field,
                    'model':custom_model.model,
                    'model_id':custom_model.id,
                    'ttype':'binary',
                    'copied' : True,
                    'tracking' : 1,
                    'field_description' : doc_name,
                    })
                file_field = request.env['ir.model.fields'].sudo().search(['&',('name','=',file_name),('model','=',custom_model.model)],limit=1)
                if not file_field:
                    file_field = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name':file_name,
                    'model':custom_model.model,
                    'model_id':custom_model.id,
                    'ttype':'char',
                    'copied' : True,
                    'tracking' : 0,
                    'field_description' : doc_name + ' name',
                    })
                # update procees field table
                process_field = request.env['o2b.process.modular.field.method'].sudo().search([('process_id', '=',p_id),('field_name','=',field.name),('form_id','=',node_id),('is_document_field','=',True)])
                if not process_field:
                    record_process = request.env['o2b.process.modular'].sudo().search([('process_id', '=',p_id)],limit=1)
                    request.env['o2b.process.modular.field.method'].sudo().create({
                    'process_id'        : p_id,
                    'process_name'      : p_name,
                    'model_name'        : custom_model.model,
                    'field_name'        : field.name ,
                    'field_label'       : doc_name,
                    'field_id'          : field.id,
                    'field_type'        : 'binary',
                    'field_method'      : None,
                    'is_required'       : is_mandaory,
                    'activity_name'     : node_name,
                    'activity_type'     : activity_type,
                    'form_id'           : node_id,
                    'process_field_line': record_process.id,
                    'default_value'     : None,
                    'is_document_field' : True,
                    })
                print(" field created or id id s; ", field)


    # create method to insert field data into ir.model.field 
    def handle_todos(self,todo,custom_model,node_id,node_name,process,activity_type):
        _logger.info("**** handle todo ")
        p_id = process.get('process_id')
        p_name = process.get('process_name')
        todo_fields = request.env['o2b.process.modular.field.method'].sudo().search([('process_id', '=',p_id),('is_todo_field','=',True),('form_id','=',node_id)])
        if todo_fields:
            todo_fields.unlink()

        for data in todo:
            todo_name = data.get('todos_name')
            todo_desc = data.get('todos_detail')
            is_mandaory = data.get('isMandatory')

            technical_field = 'x_'+ todo_name.lower().replace(' ','_').strip() if todo_name else None
            if technical_field:
                field = request.env['ir.model.fields'].sudo().search(['&',('name','=',technical_field),('model','=',custom_model.model)],limit=1)
                if not field:
                    field = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name':technical_field,
                    'model':custom_model.model,
                    'model_id':custom_model.id,
                    'ttype':'boolean',
                    'copied' : True,
                    'tracking' : 1,
                    'field_description' : todo_name,
                    })
                # update procees field table
                process_field = request.env['o2b.process.modular.field.method'].sudo().search([('process_id', '=',p_id),('field_name','=',field.name),('form_id','=',node_id),('is_todo_field','=',True)])
                if not process_field:
                    record_process = request.env['o2b.process.modular'].sudo().search([('process_id', '=',p_id)],limit=1)
                    request.env['o2b.process.modular.field.method'].sudo().create({
                    'process_id'        : p_id,
                    'process_name'      : p_name,
                    'model_name'        : custom_model.model,
                    'field_name'        : field.name ,
                    'field_label'       : todo_name,
                    'field_id'          : field.id,
                    'field_type'        : 'boolean',
                    'field_method'      : None,
                    'is_required'       : is_mandaory,
                    'activity_name'     : node_name,
                    'activity_type'     : activity_type,
                    'form_id'           : node_id,
                    'process_field_line': record_process.id,
                    'default_value'     : None,
                    'is_todo_field'     : True,
                    })
                print(" field created or id id s; ", field)



# method to create new file and add new class its field
    def create_file(self,model_path,init_path,content,file_type,file_name,model_name):
        _logger.info(" ###n#ew table file is creating ..")
        py_import_content = f'''from . import {file_name}
'''
        content = f'''\
from odoo import models, fields,api,_,os
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class {file_name}(models.Model):
    _name = 'o2b.{file_name}'
    _description = '{file_name}'
    _rec_name = 'display_name'
    # _inherit = '{model_name}'

    {content}

    '''
        if  True:
            with open(model_path, 'w') as f:
                f.write(content)  
            print(f"File '{model_path}' created successfully.")
        if True:
            with open(init_path, 'r') as file:
                existing_content = file.read()
            if py_import_content.strip() not in existing_content:
                with open(init_path, 'a') as file:
                    file.write('\n' +py_import_content + '\n')
            else:
                print(f"Content '{py_import_content}' already exists in the file.")
        self.initiate_access('o2b.'+file_name)
    # end file creating: 


    # method to update file
    def update_file(self,path,content,start_tag,end_tag):
        _logger.info(" *** update file for overriding create method: %s", path)
        with open(path, 'r') as file:
            existing_content = file.read()

        if start_tag not in existing_content and end_tag not in existing_content:
            with open(path, 'a') as file:
                file.write(content + '\n')
        else:
            print(f"Content '{path}' already exists in the file.")
        
    # end file creating: 
    
    # save image in process modular description folder
    def save_image_from_buffer(self,buffer_data, process_name):
        if buffer_data:
            if buffer_data['type'] == 'Buffer':
                # Convert buffer data to bytes
                byte_data = bytes(buffer_data['data'])

                # Ensure the directory exists
                module_path = os.path.dirname(__file__)
                #  # print("Module path :", module_path)
                parent_dir = os.path.dirname(module_path)
                create_icon_path = parent_dir +  '/static/description/' + process_name.replace(' ','_').lower()
                 # print("icon created path : ", create_icon_path)
                if not os.path.exists(create_icon_path):
                    os.makedirs(create_icon_path)
                # Write the byte data to a file
                with open(create_icon_path + '/icon.png', 'wb') as file:
                    file.write(byte_data)
                return True;
        else:
            return False;
   # create module folder sturucte in odoo addons path
    def create_module_folder(self, process_name):
        addons_paths = tools.config['addons_path']
        module_path = os.path.dirname(__file__)
        parent_dir = os.path.dirname(module_path)
        addon_path = os.path.dirname(parent_dir)
        module_dir = 'o2b_'+ process_name.replace(' ','_').lower()
        directories = [
        module_dir,
        module_dir+"/models",
        module_dir+"/controllers",
        module_dir+"/security",
        module_dir+"/static",
        module_dir+"/views",
        ]
        for directory in directories:
            path = os.path.join(addon_path+'/', directory)
            os.makedirs(path, exist_ok=True)  # exist_ok=True
        # for web controllers field start here
        controller_path = addon_path + '/'+ module_dir+'/controllers' + '/' + 'controllers.py'
        controller_init_path = addon_path + '/'+ module_dir+'/controllers' + '/' + '__init__.py'
        view_path = addon_path + '/'+ module_dir+'/views' + '/' + 'views.xml'
        controller_init_content = 'from . import controllers'
        controller_content = 'from . import controllers'
        view_content = 'from . import controllers'
        # for web controllers field end here
        # start creating file content:
        # create_model_path = addon_path + '/'+ module_dir+'/models' + '/' + process_name.replace(' ','_').lower()+ '.py'
        create_model_path = addon_path + '/'+ module_dir+'/models' + '/' + 'models.py'
        class_name = 'o2b_' + process_name.replace(' ','_').lower()
        model_name = 'o2b.' + process_name.replace(' ','_').lower()
        inherit_classes = ['mail.thread', 'mail.activity.mixin']
        # inherit_classes = "'oflow_app'"
        # inherit_classes.append(custom_model.model)
        # create_init_path = parent_dir +  '/models/' + '__init__.py'
        create_init_path = addon_path + '/'+ module_dir + '/models' + '/' + '__init__.py'
        create_menifest_path = addon_path + '/' + module_dir +  '/' + '__manifest__.py'
        create_main_init_path = addon_path + '/' + module_dir + '/'+ '__init__.py'
        init_content = 'from . import models'
        openbraces = '{'
        closebraces = '}'
        menifest_name = '"o2b_'+process_name.replace(' ','_').lower()+ '"'
        # menifest_name = '"'+ process.get('process_name')+ '"'
        menifest_contetn = f'''\
# -*- coding: utf-8 -*-
##########################################################################
# Author      : O2b Technologies Pvt. Ltd. (<www.o2btechnologies.com>)
# Copyright(c): 2016-Present O2b Technologies Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can’t redistribute it and/or modify it.
#
##########################################################################
{openbraces}
    'name': {menifest_name},
    'summary': """
        O2B Process Modular is a module that facilitates users to create modules in the Odoo platform.
        This is a low-code platform for Odoo automation.""",
    'description': """
        Long description of module's purpose
    """,
    'author': "O2b Technologies",
    'website': "https://www.o2btechnologies.com/",
    'category': 'Uncategorized',
    'license': 'OPL-1',
    'version': '0.1',
    'depends': ['base', 'mail' , 'product', 'hr'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
{closebraces}
'''
         # print("manifest content: ", menifest_contetn)
        # main_init_content = 'from . import models'
        main_init_content = '''from . import models
from . import controllers'''
        
        content = f'''\n
from datetime import datetime
from odoo import models, fields,api,_,os
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class {class_name}(models.Model):
    _name = '{model_name}'
    _description = '{process_name}'
    _rec_name = 'display_name'
    _inherit = {inherit_classes}

    logged_in_user = fields.Many2one('res.users', string="Logged User", default=lambda self: self.env.user.id , readonly=True)
    remark_user = fields.Many2one('res.users', string="Remark User")
    x_remark = fields.Char(string="Remark", tracking=True)
    active = fields.Boolean(string = 'Active',default =True)
    is_lock = fields.Boolean(string = 'Record Lock'  , default = False)
    x_reference_no = fields.Char(string = 'Record reference Number')
    employee_id = fields.Char(string='Employee ID',default=lambda self: str(self.env.user.employee_id.id))
    department = fields.Many2one('hr.department',string = 'User Department' , default=lambda self: self.env.user.employee_id.department_id)
    employee_name = fields.Many2one('hr.employee',string = 'User Employee' ,default=lambda self: self.env.user.employee_id)
    arrival_date_time = fields.Datetime(string='Arrival Time', default=lambda self: datetime.now())
    pending_since = fields.Date(string='Pending since', default=lambda self: datetime.now())
    work_step_tat = fields.Char(string='Work step tat', default=lambda self: '0 days,0 hours, 0 minutes')
    total_tat = fields.Char(string='Total TAT', default=lambda self: '0 days,0 hours, 0 minutes')
    total_tat_datetime = fields.Datetime(string='Total TAT Time', default=lambda self: datetime.now())
    total_tat_in_seconds = fields.Char(string='TAT in Seconds',default=lambda self: '0')

    # oflow mail send method start here
    def oflow_mail_send(self):
        if self.env.context:
            node_id = self.env.context.get('o2b_node_id')
            if node_id: 
                rec_obj = self.env['o2b.send.email.template'].sudo().search([('model', '=',self._name),('node_id','=',node_id)], limit=1)
                ctx = {openbraces}
                    "default_template_id": int(rec_obj.template_id) if rec_obj else None
                    {closebraces}
                return {openbraces}
                    'type'      : 'ir.actions.act_window',
                    'view_mode' : 'form',
                    'res_model' : 'mail.compose.message',
                    'views'     : [(False, 'form')],
                    'view_id'   : False,
                    'target'    : 'new',
                    'context'   : ctx,
                {closebraces}
    # oflow mail send method end here 


    @api.onchange('x_remark')
    def _onchange_x_remark(self):
        self.remark_user = self.env.user.id

    @api.model
    def pre(self,data):
        # print("We are in pre method.",data)
        # write code that will execute before done button action.
        # UserError("Pre method is runing ")
        
        return True;
    

    @api.model
    def post(self,data):
        # print("We are in post method.",data)
        # write code that will execute after done button action.
        # raise UserError(_("Post methed is running"))
        
        return True;


    # default for logged in user method user .
    # def read(self, fields=None, load='_classic_read'):
    #     _logger.info(" *** for lock feature ***: %s ", self.env.context)
    #     res = super({class_name}, self).read(fields=fields, load=load)
    #     param = self.env.context.get('params')
    #     if param:
    #         record_id = param.get('id')
    #         _logger.info(" *** Retrieved ID from context: %s", record_id)
            # if record_id:
            #     current_record  = self.env[self._name].sudo().search([('id','=',record_id)])
            #     if current_record:
            #         current_record.sudo().write({{'logged_in_user': self.env.user.id }})
        # return res

    # doc or todo list method start here
    def invoke_todo_list_action(self):
        view_id = self.env.ref('{class_name}.{class_name}_checklist').id
        form_view = self.env['ir.ui.view'].sudo().browse(view_id)
        if form_view :
            if form_view.model == self._name:
                model= self._name
                node_id = self.env.context.get('o2b_node_id') if self.env.context else None
                action_type = self.env.context.get('action_type') if self.env.context else None
                updated_view = self.env['o2b.process.modular'].dynamic_field_xml(model,node_id,action_type,form_view.arch_db)
                form_view.write({openbraces}
                    'arch_db'   :updated_view,
                    'arch_prev' :updated_view,
                    {closebraces})
            self.ensure_one()
            return {openbraces}
            'type'      : 'ir.actions.act_window',
            'name'      : 'To Do',
            'view_mode' : 'form',
            'res_model' : self._name,
            'views'     : [(view_id, 'form')],
            'target'    : 'current',
            'res_id'    : self.id,
            'domain'    : [('id', '=', self.id)],
            {closebraces}
     # doc or todo list method end here


    # override create method start here
    @api.model
    def create(self, vals):
        if 'x_reference_no' not in vals or not vals.get('x_reference_no'):
            vals['x_reference_no'] = self.env['ir.sequence'].next_by_code('{class_name}')
        return super({class_name}, self).create(vals)
    
    def copy(self, default=None):
        if default is None:
            default = {openbraces}{closebraces}
            default['x_reference_no'] = self.env['ir.sequence'].next_by_code('{class_name}')
            return super({class_name}, self).copy(default)

    # override create method end here
        
       
    '''
        # model file creation
        with open(create_model_path, 'w') as f:
            f.write(content)  # You can write initial content here if needed
        print(f"File '{create_model_path}' model/model.py created successfully.")
         # _logger.info(" create modelpath: %s ",create_model_path)

        # __init__.py file creation
        with open(create_init_path, 'w') as f:
            f.write(init_content)  # You can write initial content here if needed
        print(f"File '{create_init_path}' model/__init__.py created successfully.")

         #  main __init__.py file creation
        with open(create_main_init_path, 'w') as f:
            f.write(main_init_content)  # You can write initial content here if needed
        print(f"File '{create_main_init_path}' __init__.py created successfully.")

        # menifest  file creation
        with open(create_menifest_path, 'w') as f:
            f.write(menifest_contetn)  # You can write initial content here if needed
        print(f"File '{create_menifest_path}'__menifest__.py created successfully.")
        # controller init file  file and content creat
        with open(controller_init_path, 'w') as f:
            f.write(controller_init_content)  # You can write initial content here if needed
        print(f"File '{controller_init_path}'controller __init-- file created successfully.")

        # view creation
        view_content =f'''\
<odoo>
<template id="{class_name}">
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"/>
<title>Oflow</title>
</head>
<body>
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>
</template>

<record id="{class_name}_checklist" model="ir.ui.view">
    <field name="name">To do check list</field>
    <field name="model">{model_name}</field>
    <field name="arch" type="xml">
    <form create="false">
     <style>
        .requiredField label::after {openbraces}
          content: "* ";
          color: red;
      {closebraces}
      </style>
    <sheet>
    <h1><center>Todos Form</center></h1> 
        <group>
            <field name="id"/>
        </group>
    </sheet>
    </form>
    </field>
</record>

<record id="{class_name}_doclist" model="ir.ui.view">
    <field name="name">Document form</field>
    <field name="model">{model_name}</field>
    <field name="arch" type="xml">
    <form create="false">
    <style>
        .requiredField label::after {openbraces}
          content: "* ";
          color: red;
      {closebraces}
      </style>
    <sheet>
    <h1><center>Document Form</center></h1> 
        <group>
            <field name="id"/>
        </group>
    </sheet>
    </form>
    </field>
</record>

</odoo>
'''

        with open(view_path, 'w') as f:
            f.write(view_content) 
        print(f"File '{view_path}' views.xml created successfully.")

        # controller.py and its content creation
        controller_content =f'''\
from odoo import http, _
from odoo.http import request
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from werkzeug.wrappers import Response
import json
import logging
import random
from odoo.service import db, security
import werkzeug
import contextlib
from hashlib import sha256
import passlib.context
import re
import os
from odoo.exceptions import AccessDenied
import mimetypes
from urllib.parse import urlencode
_logger = logging.getLogger(__name__)
import base64
try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes
from ast import literal_eval

class {class_name}(http.Controller):
    @http.route('/{class_name}/view', auth='public', website=True,csrf=False)
    def view(self, **kw):
        _logger.info("***webform fetch successfully.")
        return http.request.render('{class_name}.{class_name}')


    @http.route('/{class_name}/view/submit', auth='public', website=True,csrf=False)
    def view_submit(self, **kw):
        _logger.info("***webform updated successfully.")
        end_point = request.httprequest.path
        email = kw.get('email')
        password = kw.get('password')
        # alert_script = """
        #             <script>
        #                 alert("Form data updated successfully.");
        #                 # window.location.href = '/{class_name}/view';
        #             </script>
        #             """
        # return alert_script
        return http.request.render('{class_name}.{class_name}')

'''
        with open(controller_path, 'w') as f:
            f.write(controller_content)  
        print(f"File '{controller_path}'controlers.py created successfully.")


    # add new content to _init_ file 
        with open(create_init_path, 'r') as file:
            existing_content = file.read()

        if init_content.strip() not in existing_content:
            with open(create_init_path, 'a') as file:
                file.write(init_content + '\n')
        else:
            print(f"Content '{init_content}' already exists in the file.")

        self.update_app_list_upgrade(process_name)
      

    # method to call update app list or upgrade module
    def update_app_list_upgrade(self, process_name):
        update_list = request.env['o2b.process.modular'].update_app_list(process_name)


    # method to call update app list or upgrade module
    def only_upgrade(self, process_name):
        update_list = request.env['o2b.process.modular'].upgrade_app_list(process_name)


    def _login_redirect(self, uid, redirect=None):
         # _logger.info(" *** redirect url : %s ", redirect)
        # return redirect if redirect else '/web/login'
        return json.dumps( {"message":redirect,'code':'201'})

    @http.route('/process/authenticate/user', auth='user', type='json', methods=['POST'] , csrf=False)
    def user_connect(self, **kw):
        # _logger.info("**** we are in user connect controller")
        # Access request headers
        headers = {key: value for key, value in request.httprequest.headers.items()}
         # _logger.info("Request Headers: %s", headers)
        security_key = headers.get('X-Security-Key')  # Ensure this matches the key you sent
         # _logger.info("Security Key: %s", security_key)

        if security_key != 'o2b_technologies':
            return json.dumps( {"message":"Security key is Invalid.",'code':'401'})
        # Access request body
        body = json.loads(request.httprequest.data.decode('utf-8'))
         # _logger.info("Request Body: %s", body)
        
        uid = request.session.uid = 2
        request.session.session_token = security.compute_session_token(
            request.session, request.env)
        database_setup_key = request.env['ir.config_parameter'].sudo().search([('key','=', 'web.base.url')],limit=1)
        redirect = database_setup_key.value + '/web#cids=1&action=menu'
        # request.redirect(self._login_redirect(uid, redirect=redirect))
        # self._login_redirect(uid, redirect=redirect)
        # return json.dumps( {"message":redirect,'code':request.session.session_token})
        return request.redirect(redirect_url)
                      




    # controller for publish reflection issue on UI
    @http.route('/process/publish/status/change/active', auth='none', type='http',methods=['GET','OPTIONS'] , csrf=False , cors='*')
    def module_status_changedActive(self, **kw):
        try:
            _logger.info("******* /process/publish/status/change/active api ***** , %s ", str(kw))
            process_name = kw.get('name')
            security_key = kw.get('key')
            status = kw.get('status')
            if process_name:
                process_name = process_name.strip()
            if status:
                status = status.strip()
            if security_key:
                security_key = security_key.strip()
            model_name = 'o2b.' + process_name.replace(' ','_').lower()
            model = request.env['ir.model'].sudo().search([('model','=',model_name)],limit=1)
             # _logger.info("****model object is there or not: %s", model)
            database_setup_key = request.env['ir.config_parameter'].sudo().search([('key','=', 'oflow_security_key')],limit=1)

            if not database_setup_key:
                return json.dumps({'message': "Security key not found."})

            if security_key and  security_key !=database_setup_key.value:
                return json.dumps( {"message":"Security key is Invalid.",'code':'401'})

            if not model:
                return json.dumps( {"message":"Module is not installed yet.",'code':'401'})

            menu_status = False
            if status == 'true':
                menu_status = True
            # menu_obj = request.env['ir.ui.menu'].sudo().search([('name','=',process_name),('parent_id','=',None)], limit=1)
            menu_obj = request.env['ir.ui.menu'].sudo().search([('name','=',process_name)], limit=1)
             # _logger.info("menu from process name: %s ", menu_obj)
            if menu_obj:
                menu_obj.sudo().write({
                    'active':menu_status
                    })
                 # print("write or not not, ", menu_obj.active)
            if not menu_obj:
                 # _logger.info("menu object from archided status from process name: %s ", menu_obj)
                query = """
                SELECT id
                FROM ir_ui_menu
                WHERE name->>'en_US' = %s and parent_id is null
                """
                # Execute the query with the dynamic value
                request.env.cr.execute(query, (process_name,))
                result = request.env.cr.fetchone()
                 # _logger.info("*********** database result:  %s", result)
                new_active_status='f'
                if status == 'true':
                    new_active_status='t'

                if result and result[0]:
                    menu = request.env['ir.ui.menu'].sudo().browse(result[0])
                     # _logger.info("*********** menu object via browse methodo %s", menu_obj)
                    update_query = """
                    UPDATE ir_ui_menu
                    SET active = %s
                    WHERE id = %s
                    """
                    request.env.cr.execute(update_query, (new_active_status, result[0]))
                    request.env.cr.commit()
            return json.dumps( {"message":"Publish status changed to Active",'code':'200'})
        except Exception as e:
             # print("creat module not run successfully.", e)
            return json.dumps(
                {'message' : 'Error : ' + str(e),})
          


    # controller for publish and unpublish
    @http.route('/process/publish/status/change/inactive', auth='none', type='http',methods=['GET','OPTIONS'] , csrf=False , cors='*')
    def module_status_changed_inactive(self, **kw):
        try:
            _logger.info("******* /process/publish/status/change/inactive api ***** , %s ", str(kw))
            process_name = kw.get('name')
            security_key = kw.get('key')
            status = kw.get('status')
            if process_name:
                process_name = process_name.strip()
            if status:
                status = status.strip()
            if security_key:
                security_key = security_key.strip()
            model_name = 'o2b.' + process_name.replace(' ','_').lower()
            model = request.env['ir.model'].sudo().search([('model','=',model_name)],limit=1)
             # _logger.info("****model object is there or not: %s", model)
            database_setup_key = request.env['ir.config_parameter'].sudo().search([('key','=', 'oflow_security_key')],limit=1)

            if not database_setup_key:
                return json.dumps({'message': "Security key not found."})

            if security_key and  security_key !=database_setup_key.value:
                return json.dumps( {"message":"Security key is Invalid.",'code':'401'})

            if not model:
                return json.dumps( {"message":"Module is not installed yet.",'code':'401'})

            menu_status = False
            if status == 'true':
                menu_status = True
            # menu_obj = request.env['ir.ui.menu'].sudo().search([('name','=',process_name),('parent_id','=',None)], limit=1)
            menu_obj = request.env['ir.ui.menu'].sudo().search([('name','=',process_name)], limit=1)
             # _logger.info("menu from process name: %s ", menu_obj)
            if menu_obj:
                menu_obj.sudo().write({
                    'active':menu_status
                    })
                 # print("write or not not, ", menu_obj.active)
            if not menu_obj:
                 # _logger.info("menu object from archided status from process name: %s ", menu_obj)
                query = """
                SELECT id
                FROM ir_ui_menu
                WHERE name->>'en_US' = %s and parent_id is null
                """
                # Execute the query with the dynamic value
                request.env.cr.execute(query, (process_name,))
                result = request.env.cr.fetchone()
                 # _logger.info("*********** database result:  %s", result)
                new_active_status='f'
                if status == 'true':
                    new_active_status='t'

                if result and result[0]:
                    menu = request.env['ir.ui.menu'].sudo().browse(result[0])
                     # _logger.info("*********** menu object via browse methodo %s", menu_obj)
                    update_query = """
                    UPDATE ir_ui_menu
                    SET active = %s
                    WHERE id = %s
                    """
                    request.env.cr.execute(update_query, (new_active_status, result[0]))
                    request.env.cr.commit()
                    
            return json.dumps( {"message":"Publish status changed to inactive",'code':'200'})
        except Exception as e:
             # print("creat module not run successfully.", e)
            return json.dumps(
                {'message' : 'Error : ' + str(e)})
          

    # create module controllers start here
    @http.route('/parse/create/module', auth='none', type='json',methods=['POST','OPTIONS'] , csrf=False , cors='*')
    def create_process_module(self, **kw):
        #  # print("current user di: ", request.env.user)
        try:
            json_data = json.loads(request.httprequest.data.decode('utf-8'))
            process_id = json_data.get('process_id')
            process_name = json_data.get('process_name')
            user_id = json_data.get('user_id')
            security_key = json_data.get('secret_key')
            #  # _logger.info("Received data: in process module creation\n %s ", json_data)
     
            database_setup_key = request.env['ir.config_parameter'].sudo().search([('key','=', 'oflow_security_key')],limit=1)

            if not database_setup_key:
                return json.dumps({'message': 'Security key not found.','code':'400'})

             # print("database setup key: ",database_setup_key.key,database_setup_key.value)
            # code for gettng user license security key end here

            if security_key and  security_key !=database_setup_key.value:
                return json.dumps( {"message":"Security key is Invalid.",'code':'400'})
            self.create_module_folder(process_name)
            return json.dumps( {"message":"Module created successfully.",'code':'200'})
        except Exception as e:
             # print("creat module not run successfully.", e)
            return json.dumps(
                {'message' : 'Error : ' + str(e),
                'code': '500'})


    @http.route('/parse/create/test', auth='none', type='json',methods=['POST','OPTIONS'] , csrf=False , cors='*')
    def create_process(self, **kw):
        # print(" my current url stupid create process ",request.httprequest.path)
        # time.sleep(1)
        # _logger.info(" *** current user in /create/test currsor nmae   %s", str(request.env.cr))
        try:
            _logger.info(" **********************we are in second api ******************")
            if request.env.cr.closed:
                # Re-initialize the cursor (get a new one from the environment)
                request.env.cr = request.env.cr
            end_point = request.httprequest.path
            json_data = json.loads(request.httprequest.data.decode('utf-8'))
            process = json_data.get('process')
            process_image = json_data.get('process_image')
            mdm = json_data.get('mdm')
            database_setup_key = request.env['ir.config_parameter'].sudo().search([('key','=', 'oflow_security_key')],limit=1)

            if not database_setup_key:
                return json.dumps({'message': "Security key not found."})
            
            activities = json_data.get('activities')
            #start generation unique process id :
            result = self.is_valid_process(process,database_setup_key)
            process_token = result[0]
            alert_message = result[0] 
            is_valid = result[1]
            
            process_token = process.get('process_id').strip()
            if not is_valid:
                return json.dumps({'message': alert_message})

            record_process = None
            if is_valid == True:
                # start code for registring process
                internal_model_name = 'o2b.'+ process.get('process_name').replace(" ","_").lower().rstrip()
                record_process = request.env['o2b.process.modular'].sudo().search([('process_id', '=',process_token)])
            custom_app  = request.env['ir.module.module'].sudo().search([('name', '=',internal_model_name)])
            
            custom_model = request.env['ir.model'].sudo().search([('model', '=',internal_model_name)])
            if not custom_model:
                return json.dumps( {"message":"Module installation wat not upgraded last time. please click deploy button again."})

            node_length = len(activities)
            self.create_status_bar(activities,node_length,process,custom_model)
            for i in range(node_length):
                print("cccnode position data : %s and itd data is %s", i, activities[i].get('activity_name'))
                activity_name = activities[i].get('activity_name')
                activity_type = activities[i].get('activity_type')
                assigned_form = activities[i].get('assigned_form')
                node_id = activities[i].get('activity_id')
                form_view = activities[i].get('form_view')
                list_view = activities[i].get('list_view')
                activity_group = activities[i].get('activity_group')
                activity_todos = activities[i].get('activity_todos')
                activity_doctype = activities[i].get('activity_doctype')
                edit_status = activities[i].get('activity_isFormReadOnly')

                if activity_type =='webform':
                    print(" activity type", activity_type)

                form_length = 0
                if True:
                    if assigned_form is None:
                        form_length = 0 
                    else:
                        form_length = len(assigned_form)
                    for data in range(form_length):
                        for counter in range(len(assigned_form[data])):
                            input_field = assigned_form[data]
                            if assigned_form[data][counter].get('type')!= 'button' and  assigned_form[data][counter].get('type')!= 'separator' and  assigned_form[data][counter].get('type')!= 'table':
                                create_field = 'x_o2b_'+ assigned_form[data][counter].get('title').replace(' ','_').lower()
                                selection_value = None if not assigned_form[data][counter].get('options') else assigned_form[data][counter].get('options')
                                self.create_field(create_field,custom_model,assigned_form[data][counter].get('type'),assigned_form[data][counter].get('technicalName'),selection_value,input_field[counter],assigned_form[data][counter].get('title'),assigned_form[data][counter].get('domain'),process_token,activity_name,activity_type,node_id)
                            if assigned_form[data][counter].get('type') == 'tab':
                                for item in assigned_form[data]:
                                    for tab in item['tabs']:
                                        for content_list in tab['content']:
                                            print(" tab['content'] " ,tab['content'])
                                            for content_dict in content_list:
                                                tab_field = 'x_o2b_'+ content_dict['title'].replace(' ','_').lower()
                                                selection_value = None
                                                if content_dict['type'] =='selection':
                                                    selection_value = None if not content_dict['options'] else content_dict['options']
                                                
                                                if content_dict['type'] not in ['group']:
                                                    if content_dict['type'] == 'table' and content_dict['tableType'] =='new':
                                                        self.create_new_table(content_list,content_dict['columns'],custom_model)
                                                    self.create_field(tab_field,custom_model,content_dict['type'],content_dict['technicalName'],selection_value,content_dict,content_dict['title'],None,process_token,activity_name,activity_type,node_id)
                                                if content_dict['type'] in ['group']:
                                                    for record in content_dict['fields']:
                                                        for rec in record:
                                                            if rec.get('type') == 'table' and rec.get('tableType') =='new':
                                                                _logger.info(" tab->group_newtable record reocd : %s", str(record))
                                                                self.create_new_table(record,rec.get('columns'),custom_model)
                                                            self.create_field(rec.get('technicalName'),custom_model,rec.get('type'),rec.get('technicalName'),selection_value,rec,rec.get('title'),None,process_token,activity_name,activity_type,node_id)
                            if assigned_form[data][counter].get('type') == 'group': 
                                object_data = assigned_form[data][counter].get('fields')
                                for obj in object_data:
                                    for rec in obj:
                                        if rec.get('type') == 'table' and rec.get('tableType') =='new':
                                            self.create_new_table(obj,rec.get('columns'),custom_model)
                                        self.create_field(rec.get('technicalName'),custom_model,rec.get('type'),rec.get('technicalName'),None,rec,rec.get('title'),rec.get('domain'),process_token,activity_name,activity_type,node_id)
                                        # time.sleep(1)
                            
                            # for handling table data new creation
                            if assigned_form[data][counter].get('type') == 'table'  and assigned_form[data][counter].get('tableType')== 'new':
                                self.create_new_table(assigned_form[data],assigned_form[data][counter].get('columns'),custom_model)

                            # for remark history form field handling
                            if assigned_form[data][counter].get('type') == 'remark_history':
                                if assigned_form[data][counter].get('tabs'):
                                    if assigned_form[data][counter].get('tabs')[0].get('content'):
                                        data_list = assigned_form[data][counter].get('tabs')[0].get('content')
                                        for data in data_list:
                                            t_name =  data[0].get('technicalName')
                                            self.create_field(t_name,custom_model,data[0].get('type'),t_name,data[0].get('options'),data[0],data[0].get('title'),None,process_token,activity_name,activity_type,node_id)
            
                        
                first_field = 'id'   
                self.create_view(custom_model,activity_name,activity_type,node_id,assigned_form,i,custom_app.name,activities,first_field,form_view,list_view,record_process.id,process_token,activity_todos,activity_doctype,edit_status) 
                self.action_create(custom_model,activity_name,activity_type,node_id,assigned_form,process.get('process_name'),record_process.id,process_token)  
                menu_sequence = 10
                self.create_menu_arragement(activities,node_length,process,custom_model,process.get('process_name'),process_image,process.get('process_group'),activity_name,activity_type,node_id,record_process.id,process_token,activity_group,menu_sequence)
                menu_sequence = menu_sequence+1 
            self.create_schedular(activities,node_length,process,custom_model)
           
            _logger.info(" *** grop_implies runing start seceesfyully: ")
            self.grop_implies(process,custom_model,process.get('process_name'))
            _logger.info(" *** grop_implies run seceesfyully: ")
            time.sleep(1)

            print("update menu access start")
            self.menu_access(process,custom_model,process.get('process_name'))
            time.sleep(1)
            print(" Update menu access ")

            _logger.info(" *** create_menu_arragement_archive runing start seceesfyully: ")
            self.create_menu_arragement_archive(process,custom_model,process.get('process_name'))
            _logger.info(" *** create_menu_arragement_archive run seceesfyully: ")
            time.sleep(1)

            _logger.info(" *** setting_default_value runing start seceesfyully: ")
            self.setting_default_value(process,custom_model,process.get('process_name'))
            _logger.info(" *** setting_default_value run seceesfyully: ")
            time.sleep(1)
            _logger.info(" *** update_app_list_upgrade runing start seceesfully: ")
            
            _logger.info(" ** creating admin panel ***")
            self.create_admin_panel(process,custom_model,process.get('process_name'),activities,mdm)
            _logger.info(" ** creating admin panel method run successfully.***")

            self.only_upgrade(process.get('process_name'))
            _logger.info(" *** update_app_list_upgrade run seceesfully: ")
            time.sleep(2)

            self.orphan_access()
            print("app created successfully")
            return json.dumps(
                {'message': 'User can access newly created model via Menu Name : ('+ process.get('process_name')+ ')',
                'code': '200'
                    })
        except Exception as e:
            print("not run successfully.", e)
            return json.dumps(
                {'message' : 'Error : ' + str(e),
                'code': '500'})

    #****************utilities function that help to perfom specific task and return to caller function**********************
   
    def orphan_access(self):
        table_list = request.session.get('orphan_table', [])
        _logger.info(" orphan table list: %s", table_list)
        for rec in table_list:
            self.initiate_access(rec)
        request.session['orphan_table'] = []
       

    def create_admin_panel(self,process,custom_model,process_name,activities,mdm):
        # self.admin_mdm_group_category(process_name,custom_model,p_menu,admin_menu)
        self.admin_mdm_group_category(process_name,custom_model)
        _logger.info(" **********************amdin panel %s: ",str(mdm))
        _logger.info(" ** admin panel process :%s and custom_model %s and name %s  ", process, custom_model,process_name)
        tree_view_name = process_name.lower().strip().replace(' ','_')+ '_admin'
        list_view = '''
        <tree string="Admin Panel" create="false">
        <field name="id"/>
        <field name="create_uid" string="Created By"/>
        <field name="create_date" string="Created Date"/>
        <field name="x_reference_no" string="Reference No"/>
        <field name="x_o2b_stage" string="Pending On"/>

        <!--<field name="arrival_date_time" string="Arrival date time"/>-->
        <field name="pending_since" string="Pending Since"/>
        <field name="work_step_tat" string="Work Step TAT"/>
        <field name="total_tat" string="Total TAT"/>
        <!--<field name="total_tat_datetime" string="Total TAT Date"/>-->
        <!--<field name="total_tat_in_seconds" string="Total TAT in seconds"/>-->
        </tree>
        '''
        admin_list = request.env['ir.ui.view'].sudo().search([('name','=', tree_view_name),('model','=',custom_model.model)],limit=1)
        if admin_list:
            admin_list.with_user(2).sudo().write({
                'arch_db'      : list_view ,
                'arch_prev'    : list_view ,
                })
        else:
            admin_list = request.env['ir.ui.view'].with_user(2).sudo().create({
                    'name'         : tree_view_name,
                    'model'        : custom_model.model,
                    'type'         :'tree',
                    'arch_db'      : list_view ,
                    'arch_prev'    : list_view ,
                    })
        
        # ** creating admin panel action
        action_id = request.env['ir.actions.act_window'].sudo().search(['&',('name','=',tree_view_name),('res_model','=',custom_model.model)],order="id desc" , limit=1)
        if not action_id:
            action_id = request.env['ir.actions.act_window'].sudo().create({
            'name'      : tree_view_name,
            'res_model' : custom_model.model ,
            'type'      : 'ir.actions.act_window',
            'view_mode' : 'tree',
            'view_id'   : admin_list.id,
            'domain'    : '',
            'context'   : json.dumps({'o2b_module': 'no'}),
            })

        #creating menu:
        p_menu_id = request.env['o2b.process.modular.menu'].sudo().search([('process_name', '=',process_name),('menu_type','=','main app')],limit=1)



        # delete all previsouly menu of admin panel
        admin_group  = process_name.strip().lower().replace(' ','_') + '_admin'
        mdm_group  = process_name.strip().lower().replace(' ','_') + '_mdm'
        is_mdm_group = request.env['res.groups'].sudo().search([('name','=',mdm_group)],order='create_date asc, id asc', limit=1)
        is_admin_group = request.env['res.groups'].sudo().search([('name','=',admin_group)],order='create_date asc, id asc', limit=1)
        
        query = """
        DELETE FROM ir_ui_menu
        WHERE name->>'en_US' = %s AND action = %s
        """
        request.env.cr.execute(query, ('Admin panel', 'ir.actions.act_window,' + str(action_id.id)))

        # delete all previsouly menu of admin panel

        admin_menu = request.env['ir.ui.menu'].sudo().search([('name','=','Admin panel'),('action','=','ir.actions.act_window,'+ str(action_id.id))],limit=1)
        print(" admin menu exist  ", admin_menu)

        if not admin_menu:
            admin_menu = request.env['ir.ui.menu'].with_user(2).sudo().create({
            'name'      : 'Admin panel',
            'parent_id' : p_menu_id.menu_id,
            'action'    : 'ir.actions.act_window,'+ str(action_id.id),
            'groups_id' : [is_admin_group.id]
            }) 

        
        parent_menu_name = 'MDB (' + process_name  + ')'
        p_menu = request.env['ir.ui.menu'].sudo().search([('name','=','MDM'),('action','=','ir.actions.act_window,'+ str(action_id.id))],limit=1)

        query = """
        SELECT id
        FROM ir_ui_menu
        WHERE name->>'en_US' = %s and action = %s
        """
        request.env.cr.execute(query, ('MDM','ir.actions.act_window,' + str(action_id.id)))
        result = request.env.cr.fetchone()
        print(" result of native query: mdm", result)
        if result and result[0] and not p_menu:
            p_menu = request.env['ir.ui.menu'].sudo().browse(result[0])
            print("p menu for mdm ", p_menu)
        
        if not p_menu:
            p_menu = request.env['ir.ui.menu'].with_user(2).sudo().create({
            'name'      : 'MDM',
            'parent_id' : p_menu_id.menu_id,
            'action'    : 'ir.actions.act_window,'+ str(action_id.id),
            'groups_id' : [is_mdm_group.id]
            })

        for mdm_data in mdm:
            print("mdm_data id ",  mdm_data)
            print("mdm_data id ",  mdm_data.get('model'))
            action_name = 'MDMACTION' + mdm_data.get('model').lower().replace('.','_').strip()
            model = mdm_data.get('model')
            print("action name is : %s ", action_name)
            action = request.env['ir.actions.act_window'].sudo().search(['&',('name','=',action_name),('res_model','=',model)],order="id desc" , limit=1)
            if action:
                menu_name = mdm_data.get('model_name') +'( ' + process_name + ')'
                action_id = str(action.id)
                mdm = request.env['ir.ui.menu'].sudo().search([('name','=',menu_name),('action','=','ir.actions.act_window,'+ str(action_id))],limit=1)
                print(" **** sub menu mdm naem ", mdm)
                
                query = """
                SELECT id FROM ir_ui_menu WHERE name->>'en_US' = %s and action = %s
                """
                request.env.cr.execute(query, (menu_name,'ir.actions.act_window,'+ str(action_id)))
                result = request.env.cr.fetchone()
                print(" result of native query: sub mdm", result)
                if result and result[0] and not mdm:
                    mdm = request.env['ir.ui.menu'].sudo().browse(result[0])
                    print("after native query sub mdm is ", mdm)
        
                if not mdm:
                    mdm = request.env['ir.ui.menu'].with_user(2).sudo().create({
                    'name'      : menu_name,
                    'parent_id' : p_menu.id,
                    'action'    : 'ir.actions.act_window,'+ str(action_id),
                    'groups_id' : [is_mdm_group.id]
                    }) 

        # create default sequence *****
        for data in activities:
            if data.get('activity_type') == 'start':
                if (data.get('isCustomReferenceNumber') == False) and  (data.get('defaultReferenceNumber')):
                    digit = data.get('defaultReferenceNumber')
                    prefix = 'OFLOWSEQ-'
                    suffix = '-AI'
                    class_name = 'o2b_' + process_name.replace(' ','_').lower()
                    sequence = request.env['ir.sequence'].with_user(2).sudo().search([('code','=',class_name),('name','=', process_name.strip())])
                    _logger.info(" **** default reference number %s ",str(digit))
                    if not sequence:
                        sequence = request.env['ir.sequence'].with_user(2).sudo().create({
                        'name'              : process_name,
                        'code'              : class_name,  
                        'padding'           : digit,
                        'prefix'            : '',
                        'suffix'            : '',
                        'number_increment'  : 1,
                        })
                    else:
                        sequence.with_user(2).sudo().write({
                        'name'              : process_name,
                        'code'              : class_name,  
                        'padding'           : digit,
                        'prefix'            : '',
                        'suffix'            : '',
                        'number_increment'  : 1,
                        })
        



    def grop_implies(self,process,custom_model,process_name):
        _logger.info("*** in grop_implies %s ",process)
        main_app_group = []
        record_process_group = request.env['o2b.process.modular.group'].sudo().search([('process_name', '=',process.get('process_name').strip()),('activity_type','not in',['start app'])])
        print(" *** record_process_group ",record_process_group)

        if record_process_group:
            for data in record_process_group:
                if data.activity_name == 'main app':
                    if data.group:
                        group_name = data.group.split('.')[-1]
                        _logger.info("*** group name %s and %s  \n", data.group,group_name)
                        main_group_record = request.env['res.groups'].sudo().search([('name', '=',group_name)],limit=1)
                        _logger.info("**** main grup obj ; %s \n",main_group_record)
                        if main_group_record:
                            main_app_group.append(main_group_record.id)
                # if data.node_id == 'node-1':
                #     actual_list = ast.literal_eval(data.group)
                #     print("*****actual_list in node_id ", actual_list)
                #     print("*****fype of ", type(data.group))
                #     for rec in actual_list:
                #         group_name = rec.split('.')[-1]
                #          # _logger.info("*** group name for start node %s and %s  ", data.group,group_name)
                #         stage_group = request.env['res.groups'].sudo().search([('name', '=',group_name)],limit=1)
                #         if stage_group:
                #             main_app_group.append(stage_group.id)
            print(" *** final group main_app gorup list : ", main_app_group)

            for data in record_process_group:
                if data.activity_name not in ['main app','start app']:
                    if data.group:
                        actual_list = ast.literal_eval(data.group)
                        # print("*** group data  ","and group ", data.group,group_name)
                        # print("*****fype of ", type(data.group))
                        # print("*****factual_list ", actual_list)
                        for rec in actual_list:
                            group_name = rec.split('.')[-1]
                            stage_group = request.env['res.groups'].sudo().search([('name', '=',group_name)],limit=1)
                            # print(" stage goru id fount or not ", stage_group)
                            if stage_group and main_app_group:
                                _logger.info("** main gorup app: %s", main_app_group)
                                stage_group.sudo().write({
                                    'implied_ids': main_app_group
                                    })
                                # print(" after save group implied id:", stage_group.implied_ids)


    # handle new table or one2many table in same model for computational field
    def handle_calculation_compute_method_for_field(self,table_data,table_colum,custom_model):
        _logger.info("******* handle calculation field computed method %s  model:%s", str(table_data),str(custom_model))
        new_table_name = table_data[0].get('tableRelatedField') if table_data else None
        is_total_exist  = table_data[0].get('isTotalField') if table_data else None
        reflection_field = table_data[0].get('totalfield_field') if table_data else None
        cur_operator = table_data[0].get('totalfield_operator') if table_data else None
        default_value = None
        if cur_operator =='+':
            default_value = 0
        if cur_operator =='-':
            default_value = 0
        if cur_operator =='*':
            default_value = 1
        if cur_operator =='/':
            default_value = 0

        # _logger.info("***** calculationtalbe name: %s ,proceed: %s ,relection_field : %d, cur_operators %s ",new_table_name,is_total_exist,reflection_field,cur_operator) 
        module_path = os.path.dirname(__file__)
        parent_dir = os.path.dirname(module_path)
        addon_path = os.path.dirname(parent_dir)
        process_model = request.env['o2b.process.modular.stage'].sudo().search([('model_name','=',custom_model.model)],limit=1)
        module_dir = 'o2b_'+ process_model.process_name.replace(' ','_').lower()
        create_model_path = addon_path + '/'+ module_dir+'/models' + '/' + 'models.py'
        # if is_total_exist == None:
        #     return  True

        if table_colum:
            field_name = "'"+new_table_name + "'"
            method_name = "_compute_" + new_table_name.replace(' ','_')
            start_tag = '# start compute calculation creation ' +new_table_name
            end_tag = '# end compute calculation for ' +new_table_name
            match_content = start_tag
            field_name = "'"+new_table_name + "'"
            method_name = "_compute_" + new_table_name
            virtual_total = 'x_total_'+new_table_name
            if reflection_field:
                assignment = 'rec.'+ reflection_field
                if cur_operator in ['*','/']:
                    assignment =  '(rec.'+reflection_field +' if rec.'+reflection_field +' else 1)'
            # virtual_total = 'x_o2b_my_price'
            relation_field = new_table_name+'new_table_model'
            if os.path.isfile(create_model_path):
                print(f"The file {create_model_path} exists.")
                content = f'''\n
    # start compute calculation creation {new_table_name}
    {new_table_name} = fields.One2many('o2b.{new_table_name}', '{relation_field}', string='{new_table_name}')
    {virtual_total} = fields.Float(string='Total')
    # end compute calculation creation {new_table_name}
            '''
            # read model file and check content is already exist
                with open(create_model_path, 'r') as file:
                    existing_content = file.read()

                if match_content not in existing_content:
                    with open(create_model_path, 'a') as file:
                        file.write(content + '\n')
                else:
                    print(f"Content '{create_model_path}' already exists in the file.")
            else:
                print(f"The file {create_model_path} does not exist.")
                return;
        
        if not is_total_exist and is_total_exist == False and not table_colum:
            _logger.info(" remove calculation field if exist in model.py file isTotalField:%s ", is_total_exist)
            start_tag = '# start compute calculation creation ' +new_table_name
            end_tag = '# end compute calculation creation ' +new_table_name
            if os.path.isfile(create_model_path):
                with open(create_model_path, 'r') as file:
                    lines = file.readlines()
                # Prepare to remove the existing block
                new_lines = []
                inside_block = False
                for line in lines:
                    if start_tag in line:
                        inside_block = True 
                    elif inside_block and end_tag in line:
                        inside_block = False 
                    elif not inside_block:
                        new_lines.append(line)  # Keep lines outside the block
                with open(create_model_path, 'w') as file:
                    file.writelines(new_lines)
                _logger.info("Removed the computational block completely in first block")
        # calling method to handle onchange in new table field that is relation or subtotal
        # time.sleep(2)
        self.handle_depends_in_table(table_data,table_colum,custom_model)


    # handle new table onchange method same model
    def handle_depends_in_table(self,table_data,table_colum,custom_model):
        print(" we are in subtotal rewrite mthod")
        end_point = request.httprequest.path
        _logger.info("\n ******* we are in handle_depends_in_table url %s :", str(end_point))
        # _logger.info("\n ******* handle onchange in table field :tabledata: %s  model:%s", str(table_data),str(custom_model))
        # _logger.info("\n ******* handle onchange in table field :column data :%s",   table_colum)
        onchage_field_name = table_data[0].get('tableRelatedField') if table_data else None
        on_change = None
        equation = None
        module_path = os.path.dirname(__file__)
        parent_dir = os.path.dirname(module_path)
        addon_path = os.path.dirname(parent_dir)
        process_model = request.env['o2b.process.modular.stage'].sudo().search([('model_name','=',custom_model.model)],limit=1)
        module_dir = 'o2b_'+ process_model.process_name.replace(' ','_').lower()
        create_model_path = addon_path + '/'+ module_dir+'/models' + '/' + 'models.py'
        new_model_file = addon_path + '/'+ module_dir+'/models' + '/' + onchage_field_name+ '.py'
        init_path = addon_path + '/'+ module_dir+'/models' + '/' + '__init__.py'
        many2one = onchage_field_name + 'new_table_model'
        model_field_element= f'''
    {many2one} = fields.Many2one('{process_model.model_name}',string = '{onchage_field_name}',ondelete='cascade',invisible=1)
        '''
        if table_colum:
            for item in table_colum:
                title = item['title']
                type_ = item['type']
                technical_field = item['technicalName']
                odoo_field_type = type_.capitalize()
                if type_ =='many2one':
                    model_field_element+= f'''
    # Identity {technical_field} start
    {technical_field} = fields.{odoo_field_type}('{item['relatedModel']}',string = '{title}' ,ondelete='cascade',invisible=1)
    # Identity {technical_field} end
        '''     
                elif type_ =='selection':
                    keys = item['options']
                    data = [(key.lower().strip().replace(' ','_'), key) for key in keys]
                    _logger.info(" selection acutal data %s  ", data)
                    model_field_element+= f'''
    # Identity {technical_field} start
    {technical_field} = fields.{odoo_field_type}({data},string = '{title}')
    # Identity {technical_field} end
            '''
                elif type_ =='many2many':
                    print(" item *******************88", item)
                    related_model = item['relatedModel']
                    print(" yes relatedModel ", related_model)
                    if related_model:
                        model_field_element+= f'''
    # Identity {technical_field} start
    {technical_field} = fields.{odoo_field_type}('{related_model}',string = '{title}')
    # Identity {technical_field} end
            '''

                else:
                    model_field_element+= f'''
    # Identity {technical_field} start
    {technical_field} = fields.{odoo_field_type}(string = '{title}')
    # Identity {technical_field} end
            '''
            print(" *****************calling create fiel method: ")
            self.create_file(new_model_file,init_path,model_field_element,'w',onchage_field_name,process_model.model_name)
            # time.sleep(0.2)
    
    def handle_calculation_compute_method(self,table_data,table_colum,custom_model):
        # _logger.info("******* handle calculation field computed method %s  model:%s", str(table_data),str(custom_model))
        new_table_name = table_data[0].get('tableRelatedField') if table_data else None
        is_total_exist  = table_data[0].get('isTotalField') if table_data else None
        reflection_field = table_data[0].get('totalfield_field') if table_data else None
        cur_operator = table_data[0].get('totalfield_operator') if table_data else None
        print('********************* tititntn: ','o2b.'+new_table_name)
        self.initiate_access('o2b.'+new_table_name)
        default_value = None
        if cur_operator =='+':
            default_value = 0
        if cur_operator =='-':
            default_value = 0
        if cur_operator =='*':
            default_value = 1
        if cur_operator =='/':
            default_value = 0

        # _logger.info("***** calculationtalbe name: %s ,proceed: %s ,relection_field : %d, cur_operators %s ",new_table_name,is_total_exist,reflection_field,cur_operator) 
        module_path = os.path.dirname(__file__)
        parent_dir = os.path.dirname(module_path)
        addon_path = os.path.dirname(parent_dir)
        process_model = request.env['o2b.process.modular.stage'].sudo().search([('model_name','=',custom_model.model)],limit=1)
        module_dir = 'o2b_'+ process_model.process_name.replace(' ','_').lower()
        create_model_path = addon_path + '/'+ module_dir+'/models' + '/' + 'models.py'
        if is_total_exist == None:
            return

        if is_total_exist and is_total_exist == True and reflection_field and cur_operator:

            # removing previous created field for computed field start here
            _logger.info(" remove calculation field to rewrite actually field :%s ", is_total_exist)
            start_tag = '# start compute calculation creation ' +new_table_name
            end_tag = '# end compute calculation creation ' +new_table_name
            if os.path.isfile(create_model_path):
                with open(create_model_path, 'r') as file:
                    lines = file.readlines()
                # Prepare to remove the existing block
                new_lines = []
                inside_block = False
                for line in lines:
                    if start_tag in line:
                        inside_block = True 
                    elif inside_block and end_tag in line:
                        inside_block = False 
                    elif not inside_block:
                        new_lines.append(line)  # Keep lines outside the block
                with open(create_model_path, 'w') as file:
                    file.writelines(new_lines)
                _logger.info("Removed the computational pre field block")

            # removing previous created field for computed field end  here
            
            # create field for storing dynamic field value:
            # self.create_field('x_total_'+new_table_name,custom_model,'float','x_total_'+new_table_name,None,{},'Total',None,None,None,None,None)
            
        # write code to create computation store field start here
            # print(" :'x_total_'+new_table_name" ,'x_total_'+new_table_name)
            # print(" :'+new_table_name:" ,new_table_name)
            # field_record = request.env['ir.model.fields'].sudo().search(['&',('name','=','x_total_'+new_table_name),('model','=',custom_model.model)])
            # if field_record:
            #     _logger.info(" calculation field exist name is %s ", str(field_record.name))
            # else:

            #     field_record_new = request.env['ir.model.fields'].with_user(2).sudo().create({
            #         'name'      : 'x_total_'+new_table_name,
            #         'model'     : custom_model.model,
            #         'model_id'  : custom_model.id,
            #         'ttype'     : 'float',
            #         'copied'    : True,
            #         'tracking'  : 1,
            #         'field_description' : 'Total',
            #         'store'     : True,
            #         'depends'   : new_table_name,
            #         # 'compute'   : '_compute_' + new_table_name.replace(' ','_')
            #         })
        # write code to create computation store field end here


            field_name = "'"+new_table_name + "'"
            method_name = "_compute_" + new_table_name.replace(' ','_')
            start_tag = '# start compute calculation for ' +new_table_name
            end_tag = '# end compute calculation for ' +new_table_name
            match_content = start_tag
            field_name = "'"+new_table_name + "'"
            method_name = "_compute_" + new_table_name
            virtual_total = 'x_total_'+new_table_name
            assignment = 'rec.'+reflection_field
            if cur_operator in ['*','/']:
                assignment =  '(rec.'+reflection_field +' if rec.'+reflection_field +' else 1)'
            relation_field = new_table_name+ 'new_table_model'
            if os.path.isfile(create_model_path):
                print(f"The file {create_model_path} exists.")
                content = f'''\n
    # start compute calculation for {new_table_name}
    {new_table_name} = fields.One2many('o2b.{new_table_name}', '{relation_field}', string='{new_table_name}')
    {virtual_total} = fields.Float(string='Total',compute='{method_name}', store=True)
    @api.depends('{new_table_name}')
    # @api.depends('{new_table_name}.{table_colum[0].get('technicalName')}')
    def {method_name}(self):
        for record in self:
            _logger.info("### compute for parrent model{new_table_name} %s", record)
            if record.{new_table_name}:
                record.{virtual_total} = {default_value}
                for rec in record.{new_table_name}:
                    record.{virtual_total} = record.{virtual_total} {cur_operator} {assignment}
    # end compute calculation for {new_table_name}
            '''
            # read model file and check content is already exist
                with open(create_model_path, 'r') as file:
                    existing_content = file.read()

                if match_content not in existing_content:
                    with open(create_model_path, 'a') as file:
                        file.write(content + '\n')
                else:
                    print(f"Content '{create_model_path}' already exists in the file.")
            else:
                print(f"The file {create_model_path} does not exist.")
                return;
        
        if not is_total_exist and is_total_exist == False:
            _logger.info(" remove calculation field if exist in model.py file isTotalField:%s ", is_total_exist)
            start_tag = '# start compute calculation for ' +new_table_name
            end_tag = '# end compute calculation for ' +new_table_name
            if os.path.isfile(create_model_path):
                with open(create_model_path, 'r') as file:
                    lines = file.readlines()
                # Prepare to remove the existing block
                new_lines = []
                inside_block = False
                for line in lines:
                    if start_tag in line:
                        inside_block = True 
                    elif inside_block and end_tag in line:
                        inside_block = False 
                    elif not inside_block:
                        new_lines.append(line)  # Keep lines outside the block
                with open(create_model_path, 'w') as file:
                    file.writelines(new_lines)
                _logger.info("Removed the computational block completely.")
        # calling method to handle onchange in new table field that is relation or subtotal
        # time.sleep(2)
        self.handle_onchage_in_table(table_data,table_colum,custom_model)

    # handle new table onchange method same model
    def handle_onchage_in_table(self,table_data,table_colum,custom_model):
        end_point = request.httprequest.path
        _logger.info("\n ******* we are in handle_onchage_in_table url %s :", str(end_point))
        # _logger.info("\n ******* handle onchange in table field :tabledata: %s  model:%s", str(table_data),str(custom_model))
        # _logger.info("\n ******* handle onchange in table field :column data :%s",   table_colum)
        onchage_field_name = table_data[0].get('tableRelatedField') if table_data else None
        module_path = os.path.dirname(__file__)
        parent_dir = os.path.dirname(module_path)
        addon_path = os.path.dirname(parent_dir)
        process_model = request.env['o2b.process.modular.stage'].sudo().search([('model_name','=',custom_model.model)],limit=1)
        module_dir = 'o2b_'+ process_model.process_name.replace(' ','_').lower()
        create_model_path = addon_path + '/'+ module_dir+'/models' + '/' + 'models.py'
        new_model_file = addon_path + '/'+ module_dir+'/models' + '/' + onchage_field_name+ '.py'
        on_change = None
        equation = None
        if table_colum:
            for item in table_colum:
                title = item['title']
                type_ = item['type']
                technical_field = item['technicalName']
                if 'isOnChange' in item:
                    on_change = item['isOnChange']
                    if on_change:
                        print(f'Title: {title}, Type: {type_},isOnChange {on_change}')
                        # start onchange in table 
                        field_name = "'"+technical_field + "'"
                        method_name = "_onchange_" + title.replace(' ','_').lower()
                        match_content = f'def {method_name}(self):'
                        value_fetch = item['on_change_relation']
                        which_value = item['on_change_relation_model_field']
                        if os.path.isfile(create_model_path) and value_fetch and which_value:
                            content = f'''\n
    # start table onchage : {technical_field} with {technical_field}
    @api.onchange('{onchage_field_name}')
    def {method_name}(self):
        for record in self:
            for rec in record.{onchage_field_name}:
                rec.{technical_field} = rec.{value_fetch}.{which_value}
    # end table onchage : {technical_field} with {technical_field}

            '''
                            # read model file and check content is already exist
                            with open(create_model_path, 'r') as file:
                                existing_content = file.read()

                            if match_content.strip() not in existing_content:
                                with open(create_model_path, 'a') as file:
                                    file.write(content + '\n')
                            else:
                                print(f"Content '{create_model_path}' already exists in the file.")
                        else:
                            print(f"The file {create_model_path} does not exist.")
                            return True

                    else:
                        # _logger.info(" *** onchage table false value: ", on_change)
                        if not process_model:
                            return
                        start_tag_change_field = '# start table onchage : ' +technical_field +' with ' + technical_field
                        end_tag_change_field = '# end table onchage : ' +technical_field + ' with ' + technical_field
                        if os.path.isfile(create_model_path):
                            with open(create_model_path, 'r') as file:
                                lines = file.readlines()
                            # Prepare to remove the existing block
                            new_lines = []
                            inside_block = False
                            for line in lines:
                                if start_tag_change_field in line:
                                    inside_block = True  # Start skipping lines
                                elif inside_block and end_tag_change_field in line:
                                    inside_block = False  # Stop skipping lines
                                elif not inside_block:
                                    new_lines.append(line)  # Keep lines outside the block

                            with open(create_model_path, 'w') as file:
                                file.writelines(new_lines)
                            _logger.info("Removed the onchange block completely.")
                            # end onchange in table 

                if 'equation' in item:
                    equation = item['equation']
                    print(f'Title: {title}, Type: {type_},equation {equation}')
                    # start code for removing previously created sub total field
                    _logger.info(" trying to remove if partialy sub total field is created :%s ", technical_field)
                    start_tag = f'# Identity {technical_field} start'
                    end_tag = f'# Identity {technical_field} end'
                    if os.path.isfile(new_model_file):
                        with open(new_model_file, 'r') as file:
                            lines = file.readlines()
                        new_lines = []
                        inside_block = False
                        for line in lines:
                            if start_tag in line:
                                inside_block = True 
                            elif inside_block and end_tag in line:
                                inside_block = False 
                            elif not inside_block:
                                new_lines.append(line)  # Keep lines outside the block
                        with open(new_model_file, 'w') as file:
                            file.writelines(new_lines)
                        _logger.info("Removed the computational pre field block")
                    # end code for removing previously created sub total field
                    match = re.match(r'(\w+)\s*(\+|\-|\*|\/)\s*(\w+)', equation)
                    if match:
                        operand_1 = match.group(1)
                        operator = match.group(2)
                        operand_2 = match.group(3)
                        process_model = request.env['o2b.process.modular.stage'].sudo().search([('model_name','=',custom_model.model)],limit=1)
                        if not process_model:
                            return
                       
                        field_name = "'"+technical_field + "'"
                        method_name = "_onchange_" + title.replace(' ','_')
                        match_content = None
                        addons_match_content = None
                        related_model = None
                        related_model_field = None
                        assignment = None
                        start_tag_change_field = '# start table onchage subtotal :' +technical_field +'with ' + technical_field
                        end_tag_change_field = '# end table onchage subtotal :' +technical_field + 'with ' + technical_field
                        
                        if onchage_field_name and operand_1 and operator and operand_2:
                            assignment = 'record.'+operand_1 + operator + 'record.'+operand_2
                            # if operator in ['*','/']:
                            if operator in ['/']:
                                assignment = '(record.'+operand_1 +' if record.'+operand_1 +' else 1)' + operator + '(record.'+operand_2 +' if record.'+operand_2 +' else 1)'

                            field_name = "'"+ onchage_field_name + "'"
                            method_name = "_compute_" + technical_field
                            match_content = f'def {method_name}(self):'
                            if os.path.isfile(new_model_file):
                                print(f"The file {new_model_file} exists.")
                                content = f'''\n
    # start table onchage subtotal : {technical_field} 'with '  {technical_field}
    {technical_field} = fields.Float(string='{title}',compute='{method_name}', store=True)
    @api.depends('{operand_1}','{operand_2}')
    def {method_name}(self):
        for record in self:
            record.{technical_field} = {assignment}
    # end table onchage subtotal : {technical_field} 'with '  {technical_field}

            '''
                            # read model file and check content is already exist
                                with open(new_model_file, 'r') as file:
                                    existing_content = file.read()

                                if match_content.strip() not in existing_content:
                                    with open(new_model_file, 'a') as file:
                                        file.write(content + '\n')
                                else:
                                    print(f"Content '{new_model_file}' already exists in the file.")
                            else:
                                print(f"The file {new_model_file} does not exist.")
                                return True

                else:
                    _logger.info(" *** subtotal else field")
                    process_model = request.env['o2b.process.modular.stage'].sudo().search([('model_name','=',custom_model.model)],limit=1)
                    if not process_model:
                        return
                    start_tag_change_field = '# start table onchage subtotal :' +technical_field +'with ' + technical_field
                    end_tag_change_field = '# end table onchage subtotal :' +technical_field + 'with ' + technical_field
                    if os.path.isfile(new_model_file):
                        with open(new_model_file, 'r') as file:
                            lines = file.readlines()
                        # Prepare to remove the existing block
                        new_lines = []
                        inside_block = False
                        for line in lines:
                            if start_tag_change_field in line:
                                inside_block = True 
                            elif inside_block and end_tag_change_field in line:
                                inside_block = False 
                            elif not inside_block:
                                new_lines.append(line)
                        with open(new_model_file, 'w') as file:
                            file.writelines(new_lines)
                        _logger.info("Removed the onchange block completely.")
        # time.sleep(2)

    # handle new table or one2many table in same model
    def create_new_table(self,table_data,table_colum,custom_model):
        end_point = request.httprequest.path
        print("  end point ", end_point)
        _logger.info("we are in create_new_table method ")
        # _logger.info("******* new table data : %s  and type :%s", table_data, type(table_data))
        # _logger.info("******* table colum data: %s and type :%s", table_colum, type(table_colum))
        # _logger.info("******* custom model :%s ", custom_model)
        # creating new model for new table 
        new_table_name = table_data[0].get('tableRelatedField') if table_data else None
        if new_table_name:
            new_table_name = new_table_name.strip()
        new_model_table = request.env['ir.model'].sudo().search([('model', '=',new_table_name)])
        options = None
        # if not new_model_table:
        #     new_model_table = request.env['ir.model'].with_user(2).sudo().create({
        #         # 'model'             : new_table_name,
        #         'model'             : 'x_o2b.'+ new_table_name,
        #         'name'              : new_table_name,
        #         'is_mail_thread'    : True,
        #         'is_mail_activity'  : True,
        #         })
        #     # create new model
        #      # _logger.info("*** new tabale model is create %s :",new_table_model)
        #     new_model_field_many2one = request.env['ir.model.fields'].with_user(2).sudo().create({
        #         'name'              :new_table_name +'new_table_model',
        #         'model'             :new_model_table.model,
        #         'model_id'          :new_model_table.id,
        #         'ttype'             :'many2one',
        #         'relation'          :custom_model.model,
        #         'on_delete'         :'set null',
        #         'field_description' :new_table_name,
        #         # 'domain'            : []
        #         })
        #     # creating new model fields:
        #     if table_colum:
        #         for item in table_colum:
        #             title = item['title']
        #             type_ = item['type']
        #             # field_info = None
        #             technical_field = item['technicalName']
        #             # print(f'Title: {title}, Type: {type_}')
        #             if type_ =='selection':
        #                 options = item['options']
        #             if type_ =='many2many':
        #                 print(" **********new table fo many to many: in loop",table_data,table_colum)
        #             else:
        #                 options = None
        #             if type_ == 'one2many':
        #                 _logger.info(" **new table one2many field creation %s", type_)
        #             else:
        #                 self.create_field(technical_field,new_model_table,type_,technical_field,options,item,title,None,None,None,None,None)
            
        #     one2many_in_app  = request.env['ir.model.fields'].with_user(2).sudo().create({
        #         'name'          :new_table_name,
        #         'model'         :custom_model.model,
        #         'model_id'      :custom_model.id,
        #         'ttype'         :'one2many',
        #         'relation'      :new_model_table.model,
        #         'relation_field':new_model_field_many2one.name,
        #         'field_description' : new_table_name
        #         })
        #     self.initiate_access(new_model_table.model)
        # if table_colum:
        #     for item in table_colum:
        #         title = item['title']
        #         type_ = item['type']
        #         technical_field = item['technicalName']
        #         if type_ =='many2many':
        #                 print(" **********new table fo many to many: outer loop",table_data,table_colum)
        #         if type_ =='selection':
        #             options = item['options']
        #         else:
        #             options = None
        #         if type_ == 'one2many':
        #             if item['relatedModel'] and item['relationField']:
        #                 related_model = item['relatedModel']
        #                 relation_field = item['relationField']
        #                 domain = item['domain']
        #                 m2o_field = request.env['ir.model.fields'].sudo().search(['&',('name','=','x_o2b_' + relation_field.strip().replace(' ','_').lower()),('model','=',related_model.strip())])
        #                 model_id = request.env['ir.model'].sudo().search([('model','=',related_model.strip())])
        #                 if not m2o_field:
        #                     model_id = request.env['ir.model'].sudo().search([('model','=',related_model.strip())])
        #                     new_m2o_field = request.env['ir.model.fields'].sudo().create({
        #                             'name'              : 'x_o2b_' + relation_field.strip().replace(' ','_').lower(),
        #                             'model'             : related_model,
        #                             'model_id'          : model_id.id,
        #                             'ttype'             : 'many2one',
        #                             'relation'          : new_model_table.model,
        #                             'on_delete'         : 'cascade',
        #                             'field_description' : title,
        #                             'domain'            : self.domain_parse_for_field(domain) if domain else [],
        #                             # 'tracking'          : tracking_value
        #                             })
        #                     field_id = new_m2o_field.id
        #                     m2o_field = new_m2o_field
        #                     field_record_new = request.env['ir.model.fields'].with_user(2).sudo().create({
        #                                 'name'          :technical_field,
        #                                 'model'         :new_model_table.model,
        #                                 'model_id'      :new_model_table.id,
        #                                 'ttype'         :type_,
        #                                 'relation'      :model_id.model,
        #                                 'relation_field':'x_o2b_' + relation_field.strip().replace(' ','_').lower(),
        #                                 # 'tracking' : tracking_value,
        #                                 'field_description' : title
        #                                 })
        #         else:
        #             self.create_field(technical_field,new_model_table,type_,technical_field,options,item,title,None,None,None,None,None)
        #     time.sleep(1)
        if end_point == '/parse/create/test':
            self.handle_calculation_compute_method(table_data,table_colum,custom_model)
        if end_point == '/parse/create/field':
            self.handle_calculation_compute_method_for_field(table_data,table_colum,custom_model)


    def action_create(self,custom_model,activity_name,activity_type,node_id,assigned_form,process_name,record_id,process_id):
        _logger.info("****** in action_create  methdod \nmodel : %s \nactivity name: %s \nactivity_type : %s \nprocee name : %s",custom_model,activity_name,activity_type,process_name)
        if process_name:
            process_name = process_name.strip()
        cur_stage = request.env['o2b.process.modular.statusbar'].sudo().search([('process_name', '=',process_name),('stage_name','=',activity_name.strip())],limit=1)
        _logger.info(" ******************************action stage value %s ", cur_stage.stage_value)
        cur_view_form = request.env['o2b.process.modular.view'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id),('view_type','=','form')])
        cur_view_tree = request.env['o2b.process.modular.view'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id),('view_type','=','tree')])

        model_name = custom_model.model
        tree_view = custom_model.model + activity_name + '_tree_view'
        form_view = custom_model.model + activity_name + '_form_view'
        record_existence2 = request.env['ir.ui.view'].sudo().search(['&',('model', '=',model_name),('name','=',tree_view)],order="id desc" , limit=1)
        tree_view_record = request.env['ir.ui.view'].sudo().search(['&',('model', '=',model_name),('name','=',tree_view)],order="id desc" , limit=1)
        form_view_record = request.env['ir.ui.view'].sudo().search(['&',('model', '=',model_name),('name','=',form_view)],order="id desc" , limit=1)
        record_action = request.env['ir.actions.act_window'].sudo().search(['&',('name','=',activity_name),('res_model','=',model_name)],order="id desc" , limit=1)
        saved_action = request.env['o2b.process.modular.action'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id),('activity_type','=','action')])
        if saved_action:
            saved_action.unlink()
        
        record_action_id = ''
        record_tree_id =  int(cur_view_tree.view_id) if cur_view_tree.view_id else tree_view_record.id
        record_form_id =  int(cur_view_form.view_id) if cur_view_form.view_id else form_view_record.id
        
        if record_action:
            record_action.sudo().write({
                'name'      : activity_name,
                'res_model' : model_name ,
                'type'      : 'ir.actions.act_window',
                'view_mode' : 'tree' if  activity_type =='decision' else 'tree,form' ,
                # 'view_id' : record_existence2.id,
                'view_id'   : record_tree_id,
                'domain'    : '[("x_o2b_stage","=","' + cur_stage.stage_value + '"),("x_done","=",True)]',
                'context'   : json.dumps({'o2b_module': 'yes','o2b_node_id': node_id,'activity_type':activity_type}),
                })
            record_action_id = record_action.id
        else:
            record_action_new = request.env['ir.actions.act_window'].sudo().create({
                'name'      : activity_name,
                'res_model' : model_name ,
                'type'      : 'ir.actions.act_window',
                'view_mode' : 'tree' if  activity_type =='decision' else 'tree,form' ,
                # 'view_id' : record_existence2.id,
                'view_id'   : record_tree_id,
                'domain'    : '[("x_o2b_stage","=","' + cur_stage.stage_value +  '"),("x_done","=",True)]',
                'context'   : json.dumps({'o2b_module': 'yes','o2b_node_id': node_id,'activity_type':activity_type}),
                })
            record_action_id = record_action_new.id
      
        action_table = request.env['o2b.process.modular.action'].with_user(2).sudo().create({
                        'process_actions':record_id,
                        'process_id'    : process_id,
                        'process_name'  : activity_name,
                        'model_name'    : custom_model.model,
                        'activity_name' : activity_name,
                        'action_id'     : record_action_id,
                        'action_name'   : activity_name,
                        'domain'        : '[("x_o2b_stage","=","' + cur_stage.stage_value +  '"),("x_done","=",True)]',
                        'activity_type' : 'action',
                        'context'       : json.dumps({'o2b_module': 'yes','o2b_node_id': node_id,'activity_type':activity_type}),
                        'node_id'       : node_id,
                        })

        # update menu group table: 
        record_process_group = ''
        record_process_group = request.env['o2b.process.modular.group'].sudo().search([('process_name', '=',process_name),('activity_type','=','main app')])
        if record_process_group and activity_type == 'start':
           record_process_group.with_user(2).sudo().write({
                    # 'process_groups'    : record_process.id,
                    # 'process_id'        : process_token,
                    # 'process_name'      : process.get('process_name').strip(),
                    # 'activity_name'     : 'main app',
                    # 'activity_type'     : 'main app',
                    # 'model_name'        : internal_model_name,
                    # 'node_id'           : None,
                    # 'group'             : process.get('process_group')
                    'action_id'           : record_action_id,
                    })
        record_process_group = request.env['o2b.process.modular.group'].sudo().search([('process_name', '=',process_name),('activity_type','=','start app')])
        if record_process_group and activity_type == 'start':
           record_process_group.with_user(2).sudo().write({
                    # 'process_groups'    : record_process.id,
                    # 'process_id'        : process_token,
                    # 'process_name'      : process.get('process_name').strip(),
                    # 'activity_name'     : 'main app',
                    # 'activity_type'     : 'main app',
                    # 'model_name'        : internal_model_name,
                    # 'node_id'           : None,
                    # 'group'             : process.get('process_group')
                    'action_id'           : record_action_id,
                    })
        # update menu group table: 
        record_process_group = request.env['o2b.process.modular.group'].sudo().search([('process_name', '=',process_name),('activity_type','=',activity_type)])
        if record_process_group:
           record_process_group.with_user(2).sudo().write({
                    # 'process_groups'    : record_process.id,
                    # 'process_id'        : process_token,
                    # 'process_name'      : process.get('process_name').strip(),
                    # 'activity_name'     : 'main app',
                    # 'activity_type'     : 'main app',
                    # 'model_name'        : internal_model_name,
                    # 'node_id'           : None,
                    # 'group'             : process.get('process_group')
                    'action_id'           : record_action_id,
                    })

        ir_act_window_view_tree = request.env['ir.actions.act_window.view'].sudo().search([('act_window_id','=',record_action_id)])
        if ir_act_window_view_tree:
            ir_act_window_view_tree.unlink()
        saved_action_view = request.env['o2b.process.modular.action'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id),('activity_type','=','view')])
        ir_act_window_view_tree = request.env['ir.actions.act_window.view'].sudo().create({
            'sequence'      : 1,
            # 'view_id'     : tree_view_record.id ,
            'view_id'       : int(cur_view_tree.view_id) if cur_view_tree.view_id else tree_view_record.id ,
            'act_window_id' : record_action_id,
            'view_mode'     :'tree' ,
            })
        saved_view = request.env['o2b.process.modular.action'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id),('activity_type','=','view')])
        if saved_view:
            saved_view.unlink()

        action_view_table = request.env['o2b.process.modular.action'].with_user(2).sudo().create({
                    'process_actions':record_id,
                    'process_id'    : process_id,
                    'process_name'  : activity_name,
                    'model_name'    : custom_model.model,
                    'activity_name' : activity_name,
                    'action_id'     : 'P: ' + str(record_action_id) + ' C: ' + str(ir_act_window_view_tree.id),
                    'action_name'   : activity_name,
                    'domain'        : 'null',
                    'activity_type' : 'view',
                    'context'       : 'Tree',
                    'node_id'       : node_id,
                    })
        
        if activity_type !='decision':
            ir_act_window_view_form = request.env['ir.actions.act_window.view'].sudo().create({
            'sequence'      : 1,
            'view_id'       : int(cur_view_form.view_id) if cur_view_form.view_id else form_view_record.id ,
            'act_window_id' : record_action_id,
            'view_mode'     :'form' ,
            })
            action_view_table = request.env['o2b.process.modular.action'].with_user(2).sudo().create({
                    'process_actions':record_id,
                    'process_id'    : process_id,
                    'process_name'  : activity_name,
                    'model_name'    : custom_model.model,
                    'activity_name' : activity_name,
                    'action_id'     : 'P: ' + str(record_action_id) + ' C: ' + str(ir_act_window_view_form),
                    'action_name'   : activity_name,
                    'domain'        : 'null',
                    'activity_type' : 'view',
                    'context'       : 'Form',
                    'node_id'       : node_id,
                    })
        
    # create stage progress field and selection field start here 
    def create_status_bar(self,activities, node_length,process,custom_model):
        end_point = request.httprequest.path
        if end_point == '/parse/create/test':
            return True
        _logger.info("***created status bar  %s ",custom_model)
        model_name = 'o2b_'+ custom_model.name.replace(" ","_").lower()
        process_name = process.get('process_name')
        if process_name:
            process_name = process_name.strip()

        # call create field method to create stage field:
        self.create_field('x_reference_no',custom_model,'char','x_reference_no',None,None,"Record reference Numeer",None,None,None,None,None)

        stage_field_record = self.create_field('x_o2b_stage',custom_model,'selection','x_o2b_stage',None,None,'Stage',None,None,None,None,None)
        counter = 0
        selection_fields_value = []
        for data in activities:
            node_id = data.get('activity_id')
            if node_id:
                node_id = node_id.strip()
            cur_stage = request.env['o2b.process.modular.statusbar'].sudo().search([('process_name', '=',process_name),('process_node_id','=',node_id),('stage_name','=',data.get('activity_name').strip())])
            if cur_stage:
                selection_record = request.env['ir.model.fields.selection'].sudo().search([('field_id', '=',stage_field_record.id),('value','=',cur_stage.stage_value)])
                if selection_record:
                    selection_record.with_user(2).sudo().write({
                        'name':cur_stage.stage_name,
                        })
                    selection_fields_value.append(selection_record.value)
                else:
                    new_stage = request.env['ir.model.fields.selection'].with_user(2).sudo().create({
                        'field_id'  : stage_field_record.id,
                        'sequence'  : str(counter),
                        'value'     : cur_stage.stage_value,
                        'name'      : cur_stage.stage_name,
                        })
                    selection_fields_value.append(new_stage.value)
            counter + counter + 1
        selection_exist = request.env['ir.default'].sudo().search([('field_id', '=', stage_field_record.id)])
        if selection_exist:
            defualt_record = request.env['ir.default'].sudo().write({
            'field_id'  : stage_field_record.id,         
            'json_value': json.dumps(selection_fields_value[0], ensure_ascii=False),
            })
        else:
            request.env['ir.default'].sudo().create({
            'field_id'  : stage_field_record.id,         
           'json_value': json.dumps(selection_fields_value[0], ensure_ascii=False),
            })

        # code for creating fixed field for done is click or not
        defualt_value_x_done = self.create_field('x_done',custom_model,'boolean','x_done',None,None,'Done',None,None,None,None,None)
        field_record = request.env['ir.model.fields'].sudo().search(['&',('name','=','x_done'),('model','=',custom_model.model)])
        # print("### x_done is exist or not: ",field_record )
        done_default = request.env['ir.default'].sudo().search([('field_id', '=', field_record.id)])
        if done_default:
            defualt_record = request.env['ir.default'].sudo().write({
            'field_id'  : field_record.id,         
            'json_value': json.dumps(True, ensure_ascii=False),
            })
        else:
            request.env['ir.default'].sudo().create({
            'field_id'  : field_record.id,         
           'json_value': json.dumps(True, ensure_ascii=False),
            })
        
    # create stage progress field and selection field end here here 

    # fetch all node id for selection field start her 
    def all_node_value(self,activities):
        all_node_id = ''
        for i in range(len(activities)):
            all_node_id += activities[i].get('activity_name').replace(' ','_').lower() + ','
        return all_node_id;
    # fetch all node id for selection field end  her 

  # domain parse method for odoo
    def domain_parse(self,domain):
        data_list = []
        for record in domain:
            if len(record) == 1:
                data_list.append((record))

            if len(record)>1:
                data_list.append(tuple(record))
        return data_list;
        # fetch all node id for selection field end  her 

  # domain parse for field method for odoo
    def domain_parse_for_field(self,domain):
        data_list = []
        for record in domain:
            if len(record) == 1:
                data_list.append((record))

        for record in domain:
            if len(record)>1:
                data_list.append(tuple(record))
        return data_list;
        # fetch all node id for selection field end  her 
    
    def create_schedular(self,activities,node_length,process,custom_model):
         # print("we are in schedular method: ", process, custom_model)
         # print("we are in schedular method: ",  custom_model.name)
         # print("we are in schedular method: ",  custom_model.model)
#         scheduler_code = f'''
# decisions_nodes = env['o2b.process.modular.stage'].search([('model_name', '=', '{custom_model.model}'), ('activity_type', '=', 'decision')])
# for rec in decisions_nodes:
#     desision_records = model.search([('x_o2b_stage', '=', rec.current_stage)])
#     env['o2b.process.modular'].action_test(model, record, records, desision_records, decisions_nodes,rec.current_stage)
#     '''
        scheduler_code = f'''
env['o2b.process.modular']._universal_schedular(model,'{custom_model.model}')
    '''

        # check first schedular is already created but archived
        cron_name = process.get('process_name').rstrip() + '_schedular'
        query = """
                SELECT id
                FROM ir_cron
                WHERE cron_name->>'en_US' = %s
                ORDER BY id DESC
                LIMIT 1
                """
        request.env.cr.execute(query, (cron_name,))
        result = request.env.cr.fetchone()

        print(" result of cron jobs : ", result)
        # check first schedular is already created but archived
        # server_cron = request.env['ir.cron'].sudo().search([('model_id','=',custom_model.id)])
        # if server_cron:
        #     server_cron.unlink()

        server_action = request.env['ir.actions.server'].sudo().search([('model_id','=',custom_model.id),('usage','=','ir_cron')])
        if not server_action:
            # server_action.unlink()
            server_action_new = request.env['ir.actions.server'].with_user(2).sudo().create({
                'type'                  :  'ir.actions.server',
                'binding_type'          :  'action',
                'binding_view_types'    :  'list,form',
                'name'                  :   process.get('process_name').rstrip() + '_schedular',
                'model_id'              :   custom_model.id,
                'binding_model_id'      :   custom_model.id,
                'usage'                 :  'ir_cron',
                'state'                 :  'code',
                'model_name'            :   custom_model.model  ,   
                'code'                  :   scheduler_code,
                # 'code'                :  "env['o2b.process.modular'].action_test(model,record,records)",


                })
            server_action = server_action_new
       
        if not result:
            server_cron = request.env['ir.cron'].with_user(2).sudo().create({
                'ir_actions_server_id'  :  server_action.id,
                'user_id'               :  1,
                'interval_number'       :  5,
                'numbercall'            :  -1,
                'priority'              :  5,
                'interval_type'         :  'minutes',
                'cron_name'             :  process.get('process_name').rstrip() + '_schedular',
                'active'                :  False,
                # 'doall'                 :  'code',
                # 'nextcall'              :  ''  , 
                # 'lastcall'              :  '', 
                })
            
    # setting default value to process model
    def setting_default_value(self,process,custom_model,process_name):
        _logger.info(" ** we in setting defualt value: ")
        # _logger.info("**************process: %s and custom_model %s : ",process,custom_model )
        # _logger.info("process name is %s ", process_name)
        model_name = custom_model.model
        record_process_field = request.env['o2b.process.modular.field.method'].sudo().search([('model_name', '=',custom_model.model),('default_value','not in',(None,''))])
        _logger.info(" ** we have total field found to set defaut value %s :",record_process_field)
        _logger.info(" ** we have total field found to set defaut value %s :",len(record_process_field))
        for record in record_process_field:
            field_record = request.env['ir.model.fields'].sudo().search(['&',('name','=',record.field_name),('model','=',custom_model.model)],limit=1)
            if record.field_type not in  ['many2one','one2many', 'many2many','newtable','selection','remark_history']:
                # _logger.info(" ** yes default setting field exist: %s ",str(field_record))
                if field_record:
                    default_record = request.env['ir.default'].sudo().search([('field_id', '=', field_record.id)])
                    # _logger.info(" **default field id:%s default rec: %s  and value: %s ",field_record, default_record,record.default_value)
                    default_value = record.default_value

                    if record.field_type == 'datetime':
                        default_datetime = datetime.datetime.strptime(default_value, '%Y-%m-%dT%H:%M')
                        default_value = default_datetime.strftime('%Y-%m-%d %H:%M:%S')

                    if default_record:
                        default_record.sudo().write({
                        # 'field_id'  : field_record.id,         
                        'json_value': json.dumps(default_value, ensure_ascii=False),
                        })
                    else:
                        request.env['ir.default'].sudo().create({
                        'field_id'  : field_record.id,          
                        'json_value': json.dumps(default_value, ensure_ascii=False),
                        })
        no_defaut_value_records = request.env['o2b.process.modular.field.method'].sudo().search([('model_name', '=',custom_model.model),('default_value','in',(None,''))])
        for rec in no_defaut_value_records:
            # _logger.info(" ** delete all record from default table which have no default set.")
            field_existance = request.env['ir.model.fields'].sudo().search(['&',('name','=',rec.field_name),('model','=',custom_model.model)],limit=1)
            if field_existance:
                dump_records = request.env['ir.default'].sudo().search([('field_id', '=', field_existance.id)])
                if dump_records:
                    dump_records.unlink()


                   
                    
    # CREATE MENU METHOD
    def create_menu_arragement_archive(self,process,custom_model,process_name):
        _logger.info("process name is %s ", process_name)
        model_name = custom_model.model
        process_obj = request.env['o2b.process.modular'].sudo().search([('process_id', '=',process.get('process_id'))],limit=1)
        menu_name_list = process_obj.process_menu_name_list
        if menu_name_list:
            menu_name_list = ast.literal_eval(menu_name_list)

        menu_node_list = process_obj.process_menu_node_list
        if menu_node_list:
            menu_node_list = ast.literal_eval(menu_node_list)

        serial_sequence = 11
        for node_id in menu_node_list:
            saved_menu = request.env['o2b.process.modular.menu'].sudo().search([('process_id', '=',process.get('process_id')),('menu_type','not in',['main app','start app']),('node_id','=',node_id)],limit=1)
            menu_exist= request.env['ir.ui.menu'].sudo().search([('id','=',int(saved_menu.menu_id))],limit=1)
          
            if menu_exist:
                menu_exist.with_user(2).sudo().write({
                'sequence': serial_sequence
                })
            serial_sequence = serial_sequence +1


    # CREATE MENU METHOD
    def create_menu_arragement(self,activities, node_length,process,custom_model,process_name,process_image,process_group,activity_name,activity_type,node_id,record_process,process_token,activity_group,menu_sequence):
        _logger.info("**************create_menu: and node id %s and activity_name %s : ",node_id,activity_name )
        model_name = custom_model.model
        app_menu_id  = ''
        start_menu_id = ''
        main_start = request.session.get('start_menu')
        result = self.save_image_from_buffer(process_image, process.get('process_name'))
        web_icon_path = ''
        
        if result:
            web_icon_path = 'o2b_process_modular,' + 'static/description/' +process_name.replace(' ','_').lower() + '/icon.png'
        else:
            web_icon_path = 'o2b_process_modular,static/description/icon.png'

        app_menu_count = request.env['o2b.process.modular.menu'].sudo().search([('process_name', '=',process_name),('activity_type','=','start')],limit=1)
         # _logger.info(" **** app menu count and its length: %s %s", app_menu_count ,app_menu_count.node_id)

        if app_menu_count.node_id != node_id and activity_type == 'start':
            request.env['o2b.process.modular.menu'].sudo().search([('process_name', '=',process_name)]).unlink()
        
        id_for_group =''
        if activity_type == 'start':
            record_process_group = request.env['o2b.process.modular.group'].sudo().search([('process_name', '=',process_name),('activity_type', '=','main app')],limit =1)
            app_menu = request.env['o2b.process.modular.menu'].sudo().search([('process_name', '=',process_name),('activity_type','=','start'),('node_id','=',node_id),('menu_type','=','main app')])
            if app_menu  and app_menu.count == 1:
                exist_menu = request.env['ir.ui.menu'].sudo().search([('id','=',int(app_menu.menu_id))])
                print(" iff block menu id: ", exist_menu)
                
                if exist_menu:
                    exist_menu.sudo().write({
                        'name': process.get('process_name').strip(),
                        })
                    id_for_group = exist_menu.id
            else:
                saved_action = request.env['o2b.process.modular.action'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id),('activity_type','=','action'),('context','not in',('tree','form'))])
                main_parrent_menu = request.env['ir.ui.menu'].with_user(2).sudo().create({
                            'name'      : process.get('process_name').strip(),
                            'parent_id' : False,
                            'action'    : 'ir.actions.act_window,'+ str(saved_action.action_id),
                            'web_icon'  : web_icon_path
                            })
                app_menu_id = main_parrent_menu.id
                request.env['o2b.process.modular.menu'].sudo().create({
                    'process_menus'     : record_process,
                    'process_id'        : process_token,
                    'process_name'      : process.get('process_name').strip(),
                    'menu_name'         : process.get('process_name').strip(),
                    'menu_id'           : app_menu_id,
                    'parent_id'         : None,
                    'node_id'           : node_id,
                    'action_id'         : saved_action.action_id,
                    'activity_type'     : activity_type,
                    'menu_type'         : 'main app',
                    # 'status'            : True
                    'pre_menu_id'       : main_parrent_menu.id,
                    'pre_parent_menu_id': None,
                    'count'             : 1
                    })
                id_for_group = app_menu_id
            # self.show_menu_group_wise(id_for_group,activity_name,record_process_group.group,'main_menu',custom_model)

            # for start main app
            start_mian_menu = request.env['o2b.process.modular.menu'].sudo().search([('process_name', '=',process_name),('activity_type','=','start'),('node_id','=',node_id),('menu_type','=','start app')])

            if start_mian_menu and start_mian_menu.count == 1:
                exist_menu = request.env['ir.ui.menu'].sudo().search([('id','=',int(start_mian_menu.menu_id))])

                if exist_menu:
                    exist_menu.sudo().write({
                    'name': process.get('process_name').strip(),
                    })
                    id_for_group = exist_menu.id
            else:
                saved_action = request.env['o2b.process.modular.action'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id),('activity_type','=','action'),('context','not in',('tree','form'))])
                start_mian_menu = request.env['ir.ui.menu'].with_user(2).sudo().create({
                            'name'      : process.get('process_name').strip(),
                            'parent_id' : app_menu_id,
                            'action'    : 'ir.actions.act_window,'+ str(saved_action.action_id),
                            # 'web_icon'  : web_icon_path
                            })
                start_menu_id = start_mian_menu.id
                request.env['o2b.process.modular.menu'].sudo().create({
                    'process_menus'     : record_process,
                    'process_id'        : process_token,
                    'process_name'      : process.get('process_name').strip(),
                    'menu_name'         : process.get('process_name').strip(),
                    'menu_id'           : start_menu_id,
                    'parent_id'         : app_menu_id,
                    'node_id'           : node_id,
                    'action_id'         : saved_action.action_id,
                    'activity_type'     : activity_type,
                    'menu_type'         : 'start app',
                    # 'status'            : True,
                    'pre_menu_id'       : start_menu_id,
                    'pre_parent_menu_id': None,
                    'count'             : 1
                    })
                id_for_group = start_menu_id
                request.session['start_menu'] = start_menu_id
            # self.show_menu_group_wise(id_for_group,activity_name,record_process_group.group,'main_menu',custom_model)
            start_sub_menu = request.env['o2b.process.modular.menu'].sudo().search([('process_name', '=',process_name),('activity_type','=','start'),('node_id','=',node_id),('menu_type','=','normal')])
             # _logger.info(" **** start sub menu data** %s ", str(start_sub_menu))

            if start_sub_menu and start_mian_menu.count == 1:
                 # _logger.info(" ** we are in edit mode exit start sub menu %s ", start_sub_menu.menu_id)
                exist_menu = request.env['ir.ui.menu'].sudo().search([('id','=',int(start_sub_menu.menu_id))])

                if exist_menu:
                    exist_menu.sudo().write({
                    'name'      : activity_name.strip(),
                    })
                    id_for_group = exist_menu.id
            else:
                saved_action = request.env['o2b.process.modular.action'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id),('activity_type','=','action'),('context','not in',('tree','form'))])
                start_sub_menu = request.env['ir.ui.menu'].with_user(2).sudo().create({
                            'name'      : activity_name.strip(),
                            'parent_id' : start_menu_id,
                            'action'    : 'ir.actions.act_window,'+ str(saved_action.action_id),
                            })
                start_sub_menu_id = start_sub_menu.id
                
                request.env['o2b.process.modular.menu'].sudo().create({
                    'process_menus'     : record_process,
                    'process_id'        : process_token,
                    'process_name'      : process.get('process_name').strip(),
                    'menu_name'         : activity_name.strip(),
                    'menu_id'           : start_sub_menu_id,
                    'parent_id'         : start_menu_id,
                    'node_id'           : node_id,
                    'action_id'         : saved_action.action_id,
                    'activity_type'     : activity_type,
                    'menu_type'         : 'normal',
                    # 'status'            : True,
                    'pre_menu_id'       : start_sub_menu_id,
                    'pre_parent_menu_id': None,
                    'count'             : 1,
                    })
                id_for_group = start_sub_menu_id
            # self.show_menu_group_wise(id_for_group,activity_name,activity_group,'sub_menu',custom_model)

        else:
            if activity_type not in ['decision','email','webform','email_verify']:
                main_start = request.session.get('start_menu')
                start_main_menu = request.env['o2b.process.modular.menu'].sudo().search([('process_name', '=',process_name),('activity_type','=','start'),('menu_type','=','start app')])
                except_start_menu = request.env['o2b.process.modular.menu'].sudo().search([('process_name', '=',process_name),('node_id','=',node_id),('menu_type','=','normal')])
                if except_start_menu and except_start_menu.count == 1:
                    exist_menu = request.env['ir.ui.menu'].sudo().search([('id','=',int(except_start_menu.menu_id))])
                    if exist_menu:
                        exist_menu.sudo().write({
                        'name'      : activity_name.strip(),
                        })
                        id_for_group = exist_menu.id
                else:
                    saved_action = request.env['o2b.process.modular.action'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id),('activity_type','=','action'),('context','not in',('tree','form'))])
                    except_start_menu = request.env['ir.ui.menu'].with_user(2).sudo().create({
                    'name'      : activity_name.strip(),
                    'parent_id' : start_main_menu.menu_id,
                    'action'    : 'ir.actions.act_window,'+ str(saved_action.action_id),
                    })
                    other_menu_id = except_start_menu.id
                     # print(" *** for other menu creation  ", other_menu_id)
                    request.env['o2b.process.modular.menu'].sudo().create({
                    'process_menus'     : record_process,
                    'process_id'        : process_token,
                    'process_name'      : process.get('process_name').strip(),
                    'menu_name'         : activity_name.strip(),
                    'menu_id'           : other_menu_id,
                    'parent_id'         : start_main_menu.menu_id,
                    'node_id'           : node_id,
                    'action_id'         : saved_action.action_id,
                    'activity_type'     : activity_type,
                    'menu_type'         : 'normal',
                    # 'status'            : True,
                    'pre_menu_id'       : '',
                    'pre_parent_menu_id': None,
                    'count'             : 1,
                    })
                    id_for_group = other_menu_id
            # self.show_menu_group_wise(id_for_group,activity_name,activity_group,'sub_menu',custom_model)
        self.initiate_access(custom_model.model)

    # method to create record for menu hide according to user group
    def show_menu_group_wise(self,menu_id,menu_name,group,menu_type,current_model):
        _logger.info("***in show_menu_group_wise menuId : %s,name:%s,group: %s type:%s",menu_id,menu_name,group,menu_type)
        group_list = []
        return True
        if group and menu_type != 'main_menu':
            extracted_group = [s.split('.')[1] for s in group]
            for group in extracted_group:
                ir_model_data = request.env['ir.model.data'].sudo().search([('name','=', group),('model','=', 'res.groups')], limit=1)
                group_record = request.env['res.groups'].sudo().search([('id', '=',ir_model_data.res_id)])
                table_name = 'ir_ui_menu_group_rel'
                gid = group_record.id
                if gid and menu_id:
                    insert_query = """
                    INSERT INTO %s (menu_id, gid) VALUES (%s, %s)
                    """ % (table_name, menu_id, gid)
                    request.env.cr.execute(insert_query)
                    request.env.cr.commit()
                # call initiate_access_group_wise to give model access to every group
                self.initiate_access_group_wise(current_model,gid)
        else:
            if group and menu_type == 'main_menu':
                extracted_group = group.split('.')[-1]
                ir_model_data = request.env['ir.model.data'].sudo().search([('name','=', extracted_group),('model','=', 'res.groups')], limit=1)
                group_record = request.env['res.groups'].sudo().search([('id', '=',ir_model_data.res_id)])
                table_name = 'ir_ui_menu_group_rel'
                gid = group_record.id
                if gid and menu_id:
                    insert_query = """
                    INSERT INTO %s (menu_id, gid) VALUES (%s, %s)
                    """ % (table_name, menu_id, gid)
                    request.env.cr.execute(insert_query)
                    request.env.cr.commit()
                # call initiate_access_group_wise to give model access to every group
                self.initiate_access_group_wise(current_model,gid)
                           

     #****************utilities function that help to perfom specific task and return to caller function**********************
    def menu_access(self,process,custom_model,process_name):
        _logger.info("*** menu_access %s ",process)
        main_app_group = []
        main_group_id = None
        record_process_group = request.env['o2b.process.modular.group'].sudo().search([('process_name', '=',process.get('process_name').strip()),('activity_type','not in',['start app'])])

        if record_process_group:
            for data in record_process_group:
                if data.activity_name == 'main app':
                    if data.group:
                        group_name = data.group.split('.')[-1]
                        # _logger.info("*** group name %s and %s  \n", data.group,group_name)
                        main_group_record = request.env['res.groups'].sudo().search([('name', '=',group_name)],limit=1)
                        _logger.info("**** main grup obj ; %s \n",main_group_record)
                        if main_group_record:
                            main_app_group.append(main_group_record.id)
                            main_group_id = main_group_record.id
            print(" *** final group main_app gorup list : ", main_app_group)

            for data in record_process_group:
                sub_group_ids = []
                if data.activity_name not in ['main app','start app']:
                    if data.group:
                        actual_list = ast.literal_eval(data.group)
                        # print("***** data.groupff ", data)
                        # print("***** type of ff", type(data.group))
                        # print("***** sub factual_listff ", actual_list)
                        for rec in actual_list:
                            # print(" *** submentu realy exist group ",rec)
                            group_name = rec.split('.')[-1]
                            sub_menu_group = request.env['res.groups'].sudo().search([('name', '=',group_name)],limit=1)
                            if sub_menu_group:
                                sub_group_ids.append(sub_menu_group.id)
                    cur_menu_obj = request.env['o2b.process.modular.menu'].sudo().search([('process_id', '=',data.process_id),('menu_type','not in',['main app','start app']),('node_id','=', data.node_id)],limit=1)
                    # print(" we are woking on curretn menu name or menu ide", cur_menu_obj.menu_name, cur_menu_obj.menu_id)
                    if cur_menu_obj:
                        menu_id = cur_menu_obj.menu_id
                        if menu_id:
                            menu_id = int(menu_id)
                        menu_obj = request.env['ir.ui.menu'].sudo().search([('id','=',menu_id)], limit=1)
                        if not menu_obj:
                            menu_obj = request.env['ir.ui.menu'].sudo().browse(menu_id)
                        # print(" ** current saved  menu ojbect &&&", menu_obj.id, menu_obj.name)
                        # print(" ** writing sub_group_ids in ir.ui.menu ", sub_group_ids)
                        # print("before updating value ", menu_obj.groups_id)
                        if menu_obj:
                            menu_obj.sudo().write({
                            'groups_id': [(6, 0, sub_group_ids)]
                            })
                        print("after updating value ", menu_obj.groups_id)
                        print("**sub_group_ids ", sub_group_ids)
                        if sub_group_ids:
                            for gid in sub_group_ids:
                                self.initiate_access_group_wise(custom_model,gid,cur_menu_obj.node_id)
                                # print(" access is givent to this model custom model ", custom_model," gid ", gid)
                        else:
                             self.initiate_access_group_wise(custom_model,main_group_id,'node-1')

                    # time.sleep(2)

                

    # METHOD TO CREATE ACCESS RECORD IN ACCESS TABLE
    def initiate_access(self,model_name):
        # create access right for newly created menu
        current_model = request.env['ir.model'].sudo().search([('model', '=',model_name)])
        _logger.info(" ###initiate current model exist or not : %s", current_model.model )
        if current_model:
            record_access = request.env['ir.model.access'].sudo().search([('model_id', '=',current_model.id),('group_id','=',2)],limit=1)
            if record_access:
                record_access.with_user(2).sudo().write({
                        'name'          : model_name,
                        # 'model_id'      : current_model.id,
                        # 'group_id'      : 2,
                        # 'perm_read'     : 1,
                        # 'perm_write'    : 1,
                        # 'perm_create'   : 1,
                        # 'perm_unlink'   : 1,
                        })
                print("we are in if condition in  record_access  exist",record_access)
            else:
                record_access_new = request.env['ir.model.access'].with_user(2).sudo().create({
                        'name'          : model_name,
                        'model_id'      : current_model.id,
                        'group_id'      : 2,
                        'perm_read'     : 1,
                        'perm_write'    : 1,
                        'perm_create'   : 1,
                        'perm_unlink'   : 1,
                        })
                print("==========we are in else condition in  record_access",record_access_new)
        else:
            table_list = request.session.get('orphan_table', [])
            table_list.append(model_name)
            request.session['orphan_table'] = table_list

    # METHOD TO CREATE ACCESS RECORD IN ACCESS TABLE from access newly created module for particular group
    def initiate_access_group_wise(self,current_model,group_id,node_id):
        print(" issue with group id : ", group_id, " nod id : ", node_id)
        record_access = request.env['ir.model.access'].sudo().search([('model_id', '=',current_model.id),('group_id','=',group_id)])
        perm_write_value = 0
        if node_id and node_id == 'node-1':
            perm_write_value = 1

        if record_access:
            record_access.with_user(2).sudo().write({
                    'name'          : current_model.model,
                    'model_id'      : current_model.id,
                    'group_id'      : group_id,
                    'perm_read'     : 1,
                    'perm_write'    : 1,
                    'perm_create'   : perm_write_value,
                    # 'perm_create'   : 1,
                    'perm_unlink'   : 1,
                    })
        else:
            record_access_new = request.env['ir.model.access'].with_user(2).sudo().create({
                    'name'          : current_model.model,
                    'model_id'      : current_model.id,
                    'group_id'      : group_id,
                    'perm_read'     : 1,
                    'perm_write'    : 1,
                    'perm_create'   : perm_write_value,
                    # 'perm_create'   : 1,
                    'perm_unlink'   : 1,
                    })
            record_access = record_access_new


    # create simple method to create field
    def create_model_fied(self,create_field,custom_model,ttype,field_technical_name,options,field_info,label,domain,process_id,activity_name,activity_type,node_id):
        _logger.info(" *** in create_model_fied %s ", field_technical_name)
        date_technical_name = field_technical_name +'_date'
        month_technical_name = field_technical_name +'_month'
        year_technical_name = field_technical_name +'_year'
        parrent_age = request.env['ir.model.fields'].sudo().search(['&',('name','=',field_technical_name),('model','=',custom_model.model)])

        _logger.info(" ** parente is exist: %s", parrent_age)
        if parrent_age:
                date = request.env['ir.model.fields'].sudo().search(['&',('name','=',date_technical_name),('model','=',custom_model.model)])
                if not date:
                    date = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name':date_technical_name,
                    'model':custom_model.model,
                    'model_id':custom_model.id,
                    'ttype':'integer',
                    'copied' : True,
                    'tracking' : 1,
                    'field_description' : 'Age Date',
                    })
                _logger.info(" ** parente date is exist: %s", date)
                month = request.env['ir.model.fields'].sudo().search(['&',('name','=',month_technical_name),('model','=',custom_model.model)])
                if not month:
                    date = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name':month_technical_name,
                    'model':custom_model.model,
                    'model_id':custom_model.id,
                    'ttype':'integer',
                    'copied' : True,
                    'tracking' : 1,
                    'field_description' : 'Age Month',
                    })
                _logger.info(" ** parente month is exist: %s", month)
                year = request.env['ir.model.fields'].sudo().search(['&',('name','=',year_technical_name),('model','=',custom_model.model)])
                if not year:
                    year = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name':year_technical_name,
                    'model':custom_model.model,
                    'model_id':custom_model.id,
                    'ttype':'integer',
                    'copied' : True,
                    'tracking' : 1,
                    'field_description' : 'Age year',
                    })
                _logger.info(" ** parente year is exist: %s", year)

                # write onchange method to subsitute in age date, month, year field
                module_path = os.path.dirname(__file__)
                parent_dir = os.path.dirname(module_path)
                addon_path = os.path.dirname(parent_dir)
                process_model = request.env['o2b.process.modular.stage'].sudo().search([('model_name','=',custom_model.model)],limit=1)
                module_dir = 'o2b_'+ process_model.process_name.replace(' ','_').lower()
                create_model_path = addon_path + '/'+ module_dir+'/models' + '/' + 'models.py'
                method_name =  'age_substitution_'+ field_technical_name
                match_content = '# start age field subtitution ' + field_technical_name 
           
                if os.path.isfile(create_model_path):
                    content = f'''\n
    # start age field subtitution {field_technical_name}
    @api.onchange('{field_technical_name}')
    def {method_name}(self):
        if self.{field_technical_name}:
            string_date = str(self.{field_technical_name})
            year, month, day = string_date.split("-")
            year = int(year)
            month = int(month)
            day = int(day)
            self.{field_technical_name}_date = day
            self.{field_technical_name}_month = month
            self.{field_technical_name}_year = year   
    # end age field subtitution {field_technical_name}

            '''
                    with open(create_model_path, 'r') as file:
                        existing_content = file.read()
                    if match_content.strip() not in existing_content:
                        with open(create_model_path, 'a') as file:
                            file.write(content + '\n')
                    else:
                        print(f"Content '{create_model_path}' already exists in the file.")
                else:
                    print(f"The file {create_model_path} does not exist.")
                    return True

    

    # handle email template data in send email button
    def handle_email_template(self,custom_model,field_info,activity_name,activity_type,node_id,process_id):
        _logger.info(" **** handle send email tempalte data : %s ",custom_model)
        model_id = custom_model.id
        template = field_info.get('template')
        if template:
            email_to = template.get('mail_to')
            subject = template.get('mail_subject')
            msg_body = template.get('mail_body')
            if not msg_body:
                msg_body = " "
            parse_mail_body = msg_body.replace('{{' ,'<t t-out="')
            parse_mail_body = parse_mail_body.replace('}}','"> </t> ')
            parse_mail_body = parse_mail_body.replace('<br>','<br/>')
            parse_mail_body = parse_mail_body.replace('<hr>','<hr/>')
            _logger.info(" ####final send email template %s ", str(parse_mail_body))
            # name = custom_model.name
            name = activity_name + 'Email Template'
            _logger.info(" *** email template name %s ", name)
            template_obj = request.env['mail.template'].with_user(1).search([('name', '=', name)], limit=1)
            email_template = {
            'name'          : name,
            'model_id'      : model_id,  
            'subject'       : subject,
            'description'   : subject,  
            'body_html'     : parse_mail_body,  
            'email_from'    : 'info@oflowai.com',
            'use_default_to': False,
            'email_to'      : email_to,
            }
            if not template_obj:
                template_obj.with_user(1).sudo().create(email_template)
                _logger.info(" ** creating new  mail template %s ",str(template_obj))
            else:
                template_obj.with_user(1).sudo().write(email_template)
                _logger.info(" ** updating existing mail template %s : ", str(template_obj))

            # save data for futher user 
            print(" *** geting process id: ", process_id)
            email_obj = request.env['o2b.send.email.template'].sudo().search([('process_id', '=',process_id),('node_id','=',node_id)], limit=1)
            process_obj = request.env['o2b.process.modular'].sudo().search([('process_id', '=', process_id)],limit=1)

            if not email_obj:
                email_obj.with_user(2).sudo().create({
                'send_email_lines'  : process_obj.id,
                'process_id'        : process_id,
                'process_name'      : process_obj.process_name,
                'model'             : custom_model.model,
                'node_id'           : node_id,
                'node_name'         : activity_name,
                'template_name'     : activity_name + 'Email Template',
                'template_id'       : template_obj.id,
                'data'              : template,
                })
            else:
                email_obj.with_user(2).sudo().write({
                'send_email_lines'  : process_obj.id,
                'process_id'        : process_id,
                'process_name'      : process_obj.process_name,
                'model'             : custom_model.model,
                'node_id'           : node_id,
                'node_name'         : activity_name,
                'template_name'     : activity_name + 'Email Template',
                'template_id'       : template_obj.id,
                'data'              : template,
                })

            
    # create method to insert field data into ir.model.field 
    def create_field(self,create_field,custom_model,ttype,field_technical_name,options,field_info,label,domain,process_id,activity_name,activity_type,node_id):
        if request.env.cr.closed:
            request.env.cr = request.env.cr

        end_point = request.httprequest.path
        if end_point == '/parse/create/test':
            return True
        # _logger.info("***create_field method ***\n model  %s create_field: %s and technical_name %s ",custom_model.model ,create_field,field_technical_name)
        # _logger.info(" ** field info : %s", field_info)
        # _logger.info(" ** field options : %s", options)
        # _logger.info(" ** field label: %s", label)
        # _logger.info(" ** field doamin: %s type :%s, technical: %s", domain , ttype,field_technical_name)
        # _logger.info(" ** process id %s,%s", ttype,field_technical_name)
        # _logger.info(" ** field is rquired or not::  %s ",field_info.get('isRequired'))


        if ttype =='header-button':
            print(' *** full data of email template or ', field_info)
            self.handle_email_template(custom_model,field_info,activity_name,activity_type,node_id,process_id)
            
        tracking_value = 0
        if not domain:
            domain = []
        if not label:
            label = ''
        if ttype in ['label', 'tab', 'chatter', 'ribbon', 'object', 'static_image', 'table', 'separator','group','email','write_uid','write_date','create_date', 'create_uid','logged_in_user','x_remark','employee_id','department','employee_name','header-button']:
            return True

        if ttype in ['age']:
            self.create_model_fied(create_field,custom_model,ttype,field_technical_name,options,field_info,label,domain,process_id,activity_name,activity_type,node_id)


        field_id = ''

        if field_info:
            if field_info.get('isTracking') is not None and field_info.get('isTracking') == True:
                tracking_value = 1
        if field_technical_name =='x_o2b_stage':
            tracking_value = 0
        if field_technical_name == 'x_remark':
            return True
        if field_technical_name == 'x_reference_no':
            return True

        # call file write method for  create method for onchagne field
        if field_info:
            # _logger.info(" ** field info for onchange : %s", field_info)
            on_change_status = field_info.get('isOnChange')
            on_change_reflection_field = field_info.get('on_change_relation')
            on_change_model_relate = field_info.get('relatedModel')
            on_change_model_related_field = field_info.get('on_change_relation_model_field')
            if field_info.get('isOnChange'):
                self.modify_file(custom_model,field_technical_name,label, on_change_status,on_change_reflection_field,on_change_model_relate,on_change_model_related_field)
            else:
                self.modify_file(custom_model,field_technical_name,label, on_change_status,on_change_reflection_field,on_change_model_relate,on_change_model_related_field)

            if field_info.get('widget') == 'email':
                email_technical_name = field_info.get('technicalName')+'_status'
                email_label = field_info.get('title') + ' Status'
                email_field = request.env['ir.model.fields'].sudo().search(['&',('name','=',email_technical_name),('model','=',custom_model.model)])
                # try:
                if not email_field:
                    email_status_field = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name'      : email_technical_name,
                    'model'     : custom_model.model,
                    'model_id'  : custom_model.id,
                    'ttype'     : 'boolean',
                    'copied'    : True,
                    'tracking'  : 1,
                    'field_description' : email_label,
                    })
                # except Exception as e:
                #     _logger.info(" *** error while creating email status field %s", str(e))

        # time.sleep(0.5)
        field_record = request.env['ir.model.fields'].sudo().search(['&',('name','=',field_technical_name),('model','=',custom_model.model)])
        
        print(" field records ", field_record)
        if field_record:
            field_id = field_record.id                
            # try:
            field_record.with_user(2).sudo().write({
            'name'      : field_technical_name,
            'model'     : custom_model.model,
            'model_id'  : custom_model.id,
            'copied'    : True,
            'tracking'  : tracking_value if ttype not in  ['one2many', 'many2many'] else 0,
            'field_description' : label
            })

            # for editing selection field start here
            if ttype == 'selection':
                _logger.info(" *** selection edit: %s and type is %s and p_record is %s" , field_technical_name, ttype,field_record.id)
                if not options and field_info:
                    options = field_info.get('options')
                if options:
                    selection_record = request.env['ir.model.fields.selection'].sudo().search([('field_id', '=',field_record.id)])
                    saved_selection = []
                    for menu_rec in selection_record:
                        if not menu_rec.name in options:
                            menu_rec.unlink()
                        else:
                            saved_selection.append(menu_rec.name)

                    sequence = 0
                    for curr_menu in options:
                        if not curr_menu in saved_selection:
                            request.env['ir.model.fields.selection'].sudo().create({
                            'field_id'  : field_record.id,
                            'sequence'  : str(sequence),
                            'value'     : curr_menu.replace(' ','_').lower(),
                            'name'      : curr_menu,
                            })
                        sequence = sequence + 1
            # except Exception as e:
            #     _logger.info("Error while creating model fields recode already exist: %s ", str(e))
        else:
            # try:
            if ttype =='many2one':
                # time.sleep(0.5)
                if field_info and field_info.get('relatedModel'):
                    # handle many2many fields
                     # print("We are many2one field creation block ", field_info,"related model name :", field_info.get('relatedModel'))
                    field_record_new = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name'              : field_technical_name,
                    'model'             : custom_model.model,
                    'model_id'          : custom_model.id,
                    'ttype'             : ttype,
                    'relation'          : field_info.get('relatedModel'),
                    'on_delete'         :'set null',
                    'tracking'          : tracking_value,
                    'field_description' : label,
                    'domain'            : self.domain_parse_for_field(domain) if domain else []
                    })
                    field_id = field_record_new.id
            if ttype =='one2many':
                # time.sleep(0.5)
                if field_info and field_info.get('relatedModel'):
                    m2o_field = request.env['ir.model.fields'].sudo().search(['&',('name','=','x_o2b_' + field_info.get('relationField').strip().replace(' ','_').lower()),('model','=',field_info.get('relatedModel').strip())])
                    if not m2o_field:
                        model_id = request.env['ir.model'].sudo().search([('model','=',field_info.get('relatedModel').strip())])
                         # print("res user model Id; we are creating new many2one field:  ", model_id)
                        new_m2o_field = request.env['ir.model.fields'].sudo().create({
                                'name'              : 'x_o2b_' + field_info.get('relationField').strip().replace(' ','_').lower(),
                                'model'             : field_info.get('relatedModel').strip(),
                                'model_id'          : model_id.id,
                                'ttype'             : 'many2one',
                                'relation'          : custom_model.model,
                                'on_delete'         : 'cascade',
                                'field_description' : label,
                                'domain'            : self.domain_parse_for_field(domain) if domain else [],
                                # 'tracking'          : tracking_value
                                })
                        field_id = new_m2o_field.id
                        m2o_field = new_m2o_field
                    field_record_new = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name'          :field_technical_name,
                    'model'         :custom_model.model,
                    'model_id'      :custom_model.id,
                    'ttype'         :ttype,
                    'relation'      :field_info.get('relatedModel'),
                    'relation_field':'x_o2b_' + field_info.get('relationField').strip().replace(' ','_').lower(),
                    # 'tracking' : tracking_value,
                    'field_description' : label
                    })
            if ttype =='many2many':
                # time.sleep(1)
                related_model = field_info.get('relatedModel')
                relation_table = field_info.get('relationTable')
                if related_model:
                    related_model = related_model.strip()

                if relation_table:
                    relation_table = relation_table.strip()
                else:
                    relation_table ='x_o2b_new_table_relation'

                
                base_model= custom_model.model.replace('.','_')
                ref_model = related_model.replace('.','_').strip()
                column1 = custom_model.model.replace('.','_').strip()+ '_id'
                column2 = ref_model + '_id'

                if field_info and related_model:
                    field_record_new = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name'              : field_technical_name,
                    'model'             : custom_model.model,
                    'model_id'          : custom_model.id,
                    'ttype'             : ttype,
                    'relation'          : related_model,
                    'column1'           : column1,
                    'column2'           : column2,
                    # 'tracking'          : tracking_value,
                    'field_description' : label,
                    'domain'            : self.domain_parse_for_field(domain) if domain else []
                    })
                    field_id = field_record_new.id
                    # write native query for create relation table for many2many field
                    query = """
                    CREATE TABLE IF NOT EXISTS {table_name} (
                        {field1} INTEGER REFERENCES {model1}(id),
                        {field2} INTEGER REFERENCES {model2}(id),
                        PRIMARY KEY ({field1}, {field2})
                    );
                    """.format(
                        table_name='{}_{}'.format(base_model, ref_model),
                        field1=column1,
                        field2=column2,
                        model1=base_model,
                        model2=ref_model
                    )
                     # print("queyr: :::::::::::::;;;;;;", query)
                    request.env.cr.execute(query)
                    # end here native sql query
            
            _logger.info(" ######################, type: %s and technical name: %s lave: %s",ttype, field_technical_name,label)                
            if ttype not in  ['many2one','one2many', 'many2many','newtable','selection','remark_history','write_uid','write_date']:
                if ttype == 'age':
                    ttype = 'date'
                field_record_new = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name':field_technical_name,
                    'model':custom_model.model,
                    'model_id':custom_model.id,
                    'ttype':'binary' if ttype in ['oe_avatar'] else ttype,
                    'copied' : True,
                    'tracking' : tracking_value,
                    'field_description' : label,
                    })
                field_id = field_record_new.id
                # for file name
                if field_info:
                    if field_info.get('widget'):
                        if field_info.get('widget') == 'file':
                            field_file_name = request.env['ir.model.fields'].with_user(2).sudo().create({
                            'name'      : field_technical_name + '_filename',
                            'model'     : custom_model.model,
                            'model_id'  : custom_model.id,
                            'ttype'     : 'char',
                            'copied'    : True,
                            'tracking'  : tracking_value,
                            'field_description' : 'File Name',
                            })
            if ttype == 'selection':
                # time.sleep(0.5)
                field_record_new = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name'          : field_technical_name,
                    'model'         : custom_model.model,
                    'model_id'      : custom_model.id,
                    'ttype'         :'binary' if ttype in ['oe_avatar'] else ttype,
                    'copied'        : True,
                    'tracking'      : tracking_value,
                    'field_description' : label,
                    })
                field_record = field_record_new
                field_id = field_record_new.id
                if not options and field_info:
                    options = field_info.get('options')
                if options:
                    counter = 0
                    for rec in options:
                        request.env['ir.model.fields.selection'].sudo().create({
                        'field_id'  : field_record.id,
                        'sequence'  : str(counter),
                        'value'     : rec.replace(' ','_').lower(),
                        'name'      : rec,
                        })
                        counter = counter + 1
                
            if ttype == 'remark_history':
                remark_field_name_in_app = 'x_'+ custom_model.model.replace('.','_').replace(' ','_')
                remark_table = request.env['ir.model'].sudo().search([('model', '=','o2b.process.modular.remark.history')])
                remark_field = request.env['ir.model.fields'].sudo().search(['&',('name','=',remark_field_name_in_app +'_in_remark_history'),('model','=','o2b.process.modular.remark.history')])
                if not remark_field:
                    new_remark_history_many2one = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name'              :remark_field_name_in_app +'_in_remark_history',
                    'model'             :remark_table.model,
                    'model_id'          :remark_table.id,
                    'ttype'             :'many2one',
                    'relation'          :custom_model.model,
                    'on_delete'         :'set null',
                    'field_description' : 'Remark History IDS',
                    })
                app_field = request.env['ir.model.fields'].sudo().search(['&',('name','=',remark_field_name_in_app +'_remark_history'),('model','=',custom_model.model)])
                if not app_field:
                    one2many_in_app  = request.env['ir.model.fields'].with_user(2).sudo().create({
                    'name'          :remark_field_name_in_app +'_remark_history',
                    'model'         :custom_model.model,
                    'model_id'      :custom_model.id,
                    'ttype'         :'one2many',
                    'relation'      :remark_table.model,
                    'relation_field':remark_field_name_in_app +'_in_remark_history',
                    'tracking' : 1,
                    'field_description' : 'Remark History'
                    })
            # except Exception as e:
            #     _logger.info("****Error while creating model fields %s :", str(e))
            #     return json.dumps({"Message":"Error while creating field ."+ str(e)})
                

        # code for saving required field
        _logger.info(" ** insert in process field table field Id : %s and field_record: %s", field_id,field_record)
        if process_id:
            # try:
            record_process = request.env['o2b.process.modular'].sudo().search([('process_id', '=', process_id)])
            if record_process:
                if ttype == 'write_uid':
                    field_technical_name = 'write_uid'
                if ttype == 'create_uid':
                    field_technical_name = 'create_uid'
                if ttype == 'write_date':
                    field_technical_name = 'write_date'
                if ttype == 'create_date':
                    field_technical_name = 'create_date'
                if ttype == 'logged_in_user':
                    field_technical_name = 'logged_in_user'

                record_process_field = request.env['o2b.process.modular.field.method'].sudo().search([('process_id', '=',process_id),('field_name','=',field_technical_name),('form_id','=',node_id)])
                if not record_process_field:
                    request.env['o2b.process.modular.field.method'].sudo().create({
                    'process_id'        : process_id,
                    'process_name'      : record_process.process_name,
                    'model_name'        : custom_model.model,
                    'field_name'        : field_technical_name ,
                    'field_label'       : label,
                    'field_id'          : field_record.id,
                    'field_type'        : ttype,
                    'field_method'      : field_info.get('isOnChange') if field_info else None,
                    'is_required'       : field_info.get('isRequired') if field_info else None,
                    'activity_name'     : activity_name,
                    'activity_type'     : activity_type,
                    'form_id'           : node_id,
                    'process_field_line': record_process.id,
                    'default_value'     : field_info.get('defaultValue') if field_info else None,
                    })
                else:
                    record_process_field.sudo().write({
                    'process_id'        : process_id,
                    'process_name'      : record_process.process_name,
                    'model_name'        : custom_model.model,
                    'field_name'        : field_technical_name ,
                    'field_label'       : label,
                    'field_id'          : field_record.id,
                    'field_type'        : ttype,
                    'field_method'      : field_info.get('isOnChange') if field_info else None,
                    'is_required'       : field_info.get('isRequired') if field_info else None,
                    'activity_name'     : activity_name,
                    'activity_type'     : activity_type,
                    'form_id'           : node_id,
                    'process_field_line': record_process.id,
                    'default_value'     : field_info.get('defaultValue') if field_info else None,
                    })
            # except Exception as e:
            #     _logger.error(f"Error while searching for process: {e}")
        return field_record;

# defination of create file method onchage:
    def modify_file(self,custom_model,field_technical_name,label, onchange,on_which_field,relation_model,relation_model_field):
        _logger.info(" *** modify_file method ")
        # _logger.info("**we are in create file %s field technical name;: %s  label : %s and onchange %s", custom_model.model, field_technical_name, onchange)
        # _logger.info("** onwhich field: %s and related :%s and related model field: %s ", on_which_field,relation_model,relation_model_field)
        # Ensure the directory exists
        module_path = os.path.dirname(__file__)
        parent_dir = os.path.dirname(module_path)
        addon_path = os.path.dirname(parent_dir)
        if onchange == None:
            _logger.info(" onchagne value will None: %s ", onchange)
            return

        process_model = request.env['o2b.process.modular.stage'].sudo().search([('model_name','=',custom_model.model)],limit=1)
        if not process_model:
            _logger.info(" No process bind this model id")
            return
        module_dir = 'o2b_'+ process_model.process_name.replace(' ','_').lower()
        create_model_path = addon_path + '/'+ module_dir+'/models' + '/' + 'models.py'
        field_name = "'"+field_technical_name + "'"
        method_name = "_onchange_" + label.replace(' ','_')
        match_content = None
        addons_match_content = None
        start_tag = '# start onchange for ' +field_technical_name
        end_tag = '# end onchange for ' +field_technical_name
        apply_field = None
        related_model = None
        related_model_field = None

        if on_which_field:
            apply_field = on_which_field

        if relation_model:
            related_model = relation_model

        if relation_model_field:
            related_model_field = relation_model_field
            
        if apply_field:
            field_name = "'"+apply_field + "'"
            method_name = "_onchange_" + field_technical_name
            start_tag = '# start onchange for ' +field_technical_name
            end_tag = '# end onchange for ' +field_technical_name
            start_tag_change_field = '# start reflected field :' +field_technical_name +'with ' + apply_field
            end_tag_change_field = '# end reflected field :' +field_technical_name + 'with ' + apply_field
            # match_content = f'@api.onchange({field_name})'
            match_content = f'def {method_name}(self):'
            addons_match_content =  f'self.{field_technical_name} = self.{apply_field}.{related_model_field}'

        if onchange and onchange == True and apply_field:
        # Check if the file exists
            if os.path.isfile(create_model_path):
                content = f'''\n
    # start onchange for {field_technical_name}
    @api.onchange({field_name})
    def {method_name}(self):
        self.{field_technical_name} = self.{apply_field}.{related_model_field}
    # end onchange for {field_technical_name}

            '''
            # read model file and check content is already exist
                with open(create_model_path, 'r') as file:
                    existing_content = file.read()

                if match_content.strip() not in existing_content and onchange:
                    with open(create_model_path, 'a') as file:
                        file.write(content + '\n')
                else:
                    print(f"Content '{create_model_path}' already exists in the file.")
            else:
                print(f"The file {create_model_path} does not exist.")
                return;

        if onchange == False:
            start_tag_change_field = "# start onchange for " + field_technical_name
            end_tag_change_field = "# end onchange for " + field_technical_name 
            _logger.info(" we are in on change false %s ",onchange)
            if os.path.isfile(create_model_path):
                with open(create_model_path, 'r') as file:
                    lines = file.readlines()
                # Prepare to remove the existing block
                new_lines = []
                inside_block = False
                for line in lines:
                    if start_tag_change_field in line:
                        inside_block = True  # Start skipping lines
                    elif inside_block and end_tag_change_field in line:
                        inside_block = False  # Stop skipping lines
                    elif not inside_block:
                        new_lines.append(line)  # Keep lines outside the block

                # Write the updated content back to the file, effectively removing the block
                with open(create_model_path, 'w') as file:
                    file.writelines(new_lines)
                _logger.info("Removed the onchange block completely.")
        # time.sleep(0.5)
    # end file creating: 

    def create_view(self ,custom_model,activity_name,activity_type,node_id,assigned_form,index,module,activities,first_field,ui_form_view,list_view,record_process_id,process_token,activity_todos,activity_doctype,edit_status):
        # _logger.info(" **** we in create view: *** ")
        # _logger.info(" **** model name : %s", custom_model)
        # _logger.info(" **** activity type  : %s",activity_type)
        # _logger.info(" **** activity name  : %s",activity_name)
        # _logger.info(" **** node_id : %s",node_id)
        # _logger.info(" actual ui_form_view : %s", ui_form_view)
        # _logger.info(" actual list_view : %s", list_view)
        # print(" **************************************************doctype ", activity_doctype)
        # print(" **************************************************todo ", activity_todos)
        last_form_editable = ' delete="false" edit="true"'
        if activity_type:
            activity_type = activity_type.strip()
        if activity_name:
            activity_name = activity_name.strip()
        if node_id:
            node_id = node_id.strip()

        model_field = request.env['ir.model.fields'].sudo().search([('model','=',custom_model.model)])
         # print("currnent field model for generating xml form and tree: ", model_field, custom_model.model)
         # print("create view ====================", assigned_form)
        xml_content = ''
        form_view = '''
        <form create="false" delete="false">
        <header>
        </header>
        <sheet>
        <group>
        </group>
        <hr/>
        <div style="text-align:center;padding:10px;">
        </div>
        </sheet>
        </form>
        '''
        form_view_new_button = '''
        <form create="false" delete="false">
        <header>
        </header>
        <sheet>
        <group>
        </group>
        <hr/>
        <div style="text-align:center;padding:10px;">
        </div>
        </sheet>
        </form>
        '''
    
        # adding odoo xml tree view tag
        tree_view = '''
        <tree delete="false">
        </tree>
        '''
        tree_view_new_button = '''
        <tree create="false" delete="false">
        </tree>
        '''
        form_length = 0 
        if assigned_form is None:
            form_length = 0 
        else:
            form_length = len(assigned_form)
        xml_button =''
        # tree view content in xml parsing
        xml_content_tree_view = ''
        if assigned_form:
            for i in assigned_form:
                for j in i:
                    if j.get('type') not in['label', 'button','tab','separator','group','chatter','table','ribbon','object','static_image','remark_history','logged_in_user','write_uid','create_uid','write_date','create_date','email','webform' ,'employee_id','department','employee_name','header-button']:
                        create_field = 'x_o2b_'+ j.get('title').replace(' ','_').lower()
                        field_label = j.get('title')
                        
                        if field_label:
                            field_label = field_label.replace('&', ' &amp; ')

                        if   j.get('widget') == 'file' :
                            file_name =  j.get('technicalName')+ '_filename'
                            xml_content_tree_view =  xml_content_tree_view + '\n <field name="' +  file_name + '" string="' + field_label +  ' "/>\n'
                        
                        if   j.get('widget') == 'password' :
                            xml_content_tree_view =  xml_content_tree_view + '\n <field name="' +  j.get('technicalName')+  '" widget="' +  j.get('widget')+ '" string="' + field_label +  '" password="true" />\n'

                        if j.get('widget') not in ['password','file']:
                            xml_content_tree_view =  xml_content_tree_view + '\n <field name="' +  j.get('technicalName')+  '" widget="' +  j.get('widget')+ '" string="' + field_label +  '" />\n'
                             # _logger.info(" xml content in for j in i: %s  ", str(xml_content_tree_view))
        first_field = 'id'
        first_field_label = 'Record Id'
        if True:
            first_field = '<field name="'  + first_field + '" string="' + first_field_label +  '"/>\n'
            reference_no = '<field name="x_reference_no" string="Reference No"/>\n'
            xml_content_tree_view = first_field +reference_no + xml_content_tree_view

        status = '<field name="x_o2b_stage"  string="Status"/>\n'
        xml_content_tree_view = xml_content_tree_view + status

        if index == 0:
            odoo_tree_view_xml  = self.update_xml_content(tree_view,'<tree delete="false">','</tree>',xml_content_tree_view)
        else:
            odoo_tree_view_xml  = self.update_xml_content(tree_view_new_button,' <tree create="false" delete="false">','</tree>',xml_content_tree_view)
        if odoo_tree_view_xml:
             odoo_tree_view_xml = odoo_tree_view_xml.replace('<?xml version="1.0" ?>','')


        # insert form view as it is from reat UI start here
        if ui_form_view  and activity_type !='webform':
            ui_form_view = ui_form_view.replace('<?xml version=\"1.0\"?>','')
            if index == 0:
                ui_form_view = ui_form_view.replace('<form>','<form create="true" delete="false">')
            else:
                ui_form_view = ui_form_view.replace('<form>','<form create="false" delete="false">')


        if activity_type in [ "end", "discard", "exception", "reject"]:
            _logger.info(" check edit status %s", str(edit_status))
            if edit_status:
                last_form_editable = 'delete="false"  edit="false"'
                ui_form_view = ui_form_view.replace('delete="false"',last_form_editable)

        if activity_doctype:
            context = {'action_type': 'documents'}
            checklist_button = f'<button name="invoke_todo_list_action" string="Document" type="object" class="oe_stat_button" icon="fa-upload" context="{context}" />'
            ui_form_view = ui_form_view.replace('<todolist/>',checklist_button)
        if activity_todos:
            context = {'action_type': 'todos'}
            document_button = f'<button name="invoke_todo_list_action" string="Todos" type="object" class="oe_stat_button" icon="fa-list" context="{context}" />'
            ui_form_view = ui_form_view.replace('<checklist/>',document_button)

        if ui_form_view:
            method_name ='name="oflow_mail_send"'
            ui_form_view = ui_form_view.replace('name="pre"',method_name)
        # print(" final form view ***********************8: ", ui_form_view)


        # for list view update content
        if list_view  and activity_type !='webform':
            list_view = list_view.replace('<?xml version=\"1.0\"?>','')
            # list_view = list_view.replace('<form>','<form create="false">')

        

        # print(" update findl form view : ", ui_form_view)
        # print(" update findl list view : ", list_view)
        # print(" update findl odoo_tree_view_xml : ", odoo_tree_view_xml)
        # delte all view
        form_view_name = custom_model.model + activity_name +  '_form_view'
        tree_view_name = custom_model.model + activity_name + '_tree_view'
        record_form_view = request.env['ir.ui.view'].sudo().search(['&',('model', '=',custom_model.model),('type','=','form'),('name','=',form_view_name)])
        if record_form_view:
            record_form_view.unlink()
            
        record_tree_view = request.env['ir.ui.view'].sudo().search(['&',('model', '=',custom_model.model),('type','=','tree'),('name','=',tree_view_name)])
        if record_tree_view:
            record_tree_view.unlink()

        cur_view_form = request.env['o2b.process.modular.view'].sudo().search([('model_name', '=',custom_model.model),('node_id','=',node_id)])
        if cur_view_form:
            cur_view_form.unlink()
        try:
            if activity_type !='webform':
                record_form_view_new = request.env['ir.ui.view'].with_user(2).sudo().create({
                            'name'         : form_view_name,
                            'model'        : custom_model.model,
                            'type'         :'form',
                            'arch_db'      : ui_form_view,
                            'arch_prev'    : ui_form_view,
                            })
                new_rec_view = request.env['o2b.process.modular.view'].with_user(2).sudo().create({
                            'process_views': record_process_id,
                            'process_id'   : process_token,
                            'process_name' : activity_name,
                            'model_name'   : custom_model.model,
                            'node_id'      : node_id,
                            'activity_type': activity_type,
                            'activity_name': activity_name,
                            'view_id'      : record_form_view_new.id,
                            'view_name'    : form_view_name,
                            'view_type'    : 'form',
                            'view_data'    : ui_form_view,

                            })
        except Exception as e:
            _logger.info(" Error is in view modification %s  ",str(e))
            view_error_msg = str(e)


        # process view table data and create tree view start  here
        record_tree_view_new = request.env['ir.ui.view'].with_user(2).sudo().create({
                'name'         : tree_view_name,
                'model'        : custom_model.model,
                'type'         :'tree',
                'arch_db'      : list_view if list_view else odoo_tree_view_xml,
                'arch_prev'    : list_view if list_view else odoo_tree_view_xml,
                })
        new_rec_view = request.env['o2b.process.modular.view'].with_user(2).sudo().create({
               'process_views' : record_process_id,
                'process_id'   : process_token,
                'process_name' : activity_name,
                'model_name'   : custom_model.model,
                'node_id'      : node_id,
                'activity_type': activity_type,
                'activity_name': activity_name,
                'view_id'      : record_tree_view_new.id,
                'view_name'    : tree_view_name,
                'view_type'    : 'tree',
                'view_data'    : odoo_tree_view_xml,
                })

    # Generate Unique Process Id and validate process and its required fields
    def is_valid_process(self,process,key_obj):
        process_name = process.get('process_name')
        process_detail = process.get('process_detail')
        user_id = process.get('user_id')
        secret_key = process.get('secret_key')
        message =''
        valid = True
        if not process_name:
            message = 'Process name required.'
            valid = False
        if not user_id:
            message  = 'User Id  required.'
            valid = False
        if not secret_key :
            message  = 'Security key required.'
            valid = False

        if secret_key and  secret_key !=key_obj.value:
            message  = 'Invalid secret key.'
            valid = False

        if valid:
            #start generation unique process id and store in database for future use
            current_date = datetime.date.today()
            date = current_date.strftime("%Y%m%d")
            process_id = user_id + date + process_name.replace(" ","_")
            result = [process_id, valid]
            return result
        else:
            result = [message, valid]
            return result


    # method to create server action for button type in assigned form:
    def create_server_action_for_button(self,custom_model):
        pass
         # print("we are in create_server_action_for_button", custom_model, " name", custom_model.model)

    # update the existing xml format data and return to caller function
    def update_xml_content(self,source_xml,start_node, end_node,append_node):
        #  # print("we are in xml updator function   ",source_xml, "\nstart node: ", start_node ,"\nend node : ", end_node)
        node_start_index = source_xml.find(start_node) + len(start_node)
        node_end_index = source_xml.find(end_node)
        updated_arch = source_xml[:node_start_index] + append_node + source_xml[node_start_index:node_end_index] + source_xml[node_end_index:]
        dom = parseString(updated_arch)
        # Pretty print the XML
        pretty_xml_as_string = dom.toprettyxml()
        #  # print("final update xml file: ", pretty_xml_as_string)
        return pretty_xml_as_string;


#========================project end code ==================================================

# start controller for fetching existing group
    @http.route('/o2b/groups', auth='none', type='http',methods=['GET','OPTIONS'] , csrf=False , cors='*')
    def fetch_groups(self, **kw):
        # print("we are in group fetch controller.", )
        groups_obj = request.env['res.groups'].sudo().search([('category_id', 'not in',[False,1,104,105,102])])
        # groups_obj = request.env['res.groups'].sudo().search([])
         # print("total number of groups: ", groups_obj, len(groups_obj))
        groups_data = []
        for group_obj in groups_obj:
            data = {
                'id'         : group_obj.id,
                'name'       : group_obj.name,
                'category_id': group_obj.category_id.id,
                'category_name': group_obj.category_id.name
                # Add more fields as needed
            }
            groups_data.append(data)
        return json.dumps(groups_data)

# start controller for fetching existing users
    @http.route('/o2b/users', auth='none', type='http',methods=['GET','OPTIONS'] , csrf=False , cors='*')
    def fetch_users(self, **kw):
         # print("we are in users fetch controller.")
        user_obj = request.env['res.users'].sudo().search([])
         # print("total number of user: ", user_obj  , len(user_obj))
        users_data = []
        for user_data in user_obj:
            data = {
                'id'        : user_data.id,
                'name'      : user_data.name,
                'email'     : user_data.login,
                'partner_id': user_data.partner_id.id,
                # 'partner_name': user_data.partner_id.name,
                # Add more fields as needed
            }
            users_data.append(data)
        # Return JSON response
        return json.dumps(users_data)

# start controller for fetching existing models
    @http.route('/o2b/models', auth='none', type='http',methods=['GET','OPTIONS'] , csrf=False , cors='*')
    def fetch_models(self, **kw):
         # print("we are in model fetch controller.")
        # json_data = json.loads(request.httprequest.data.decode('utf-8'))
        #  # _logger.info("Received data:\n %s ", json_data)
        model_obj = request.env['ir.model'].sudo().search([])
         # print("total number of model: ", model_obj, len(model_obj))
        models_data = []
        for model in model_obj:
            data = {
                'id'        : model.id,
                'name'      : model.name,
                'model'     : model.model,
                # Add more fields as needed
            }
            models_data.append(data)
        # Return JSON response
        return json.dumps(models_data)


# start controller for fetching existing models fields
    @http.route(['/o2b/fields','/o2b/field'], auth='none', type='http',methods=['GET','OPTIONS'] , csrf=False , cors='*')
    def fetch_fields(self, **kw):
        end_point = request.httprequest.path
        if end_point == '/o2b/fields':
             # print("we are in field fetch controller.")
            model_name = kw.get('model').strip()
            if model_name:
                try:     
                    partner_model =request.env['ir.model.fields'].sudo().search(['&',('model','=',model_name),('ttype','=','many2one')])
                    models_data = []
                    for model in partner_model:
                        data = {
                            'id'        : model.id,
                            'name'      : model.name,
                            # 'type'     : model.ttype,
                            # Add more fields as needed
                        }
                        models_data.append(data)
                    # Return JSON response
                    return json.dumps(models_data)
                    
                except Exception as e:
                    return json.dumps({"Message":"Invalid Model Name."})
        if end_point == '/o2b/field':
             # print("we are in field fetch controller.")
            model_name = kw.get('model').strip()
            if model_name:
                try:     
                    partner_model = request.env[model_name]
                    model_fields = partner_model.fields_get()
                    field_names = list(model_fields.keys()) 
                    return  json.dumps(field_names)
                except Exception as e:
                    return json.dumps({"Message":"Invalid Model Name."})

        
# start controller for fetching existing models
    @http.route('/o2b/category', auth='none', type='http',methods=['GET','OPTIONS'] , csrf=False , cors='*')
    def fetch_category(self, **kw):
         # print("we are in category fetch controller.")
        # json_data = json.loads(request.httprequest.data.decode('utf-8'))
        #  # _logger.info("Received data:\n %s ", json_data)
        model_obj = request.env['ir.module.category'].sudo().search([])
         # print("total number of category: ", model_obj, len(model_obj))
        models_data = []
        for model in model_obj:
            data = {
                'id'              : model.id,
                'parent_id'       : model.parent_id.id,
                'name'            : model.name,
                'sequence'        : model.sequence
                # Add more fields as needed
            }
            models_data.append(data)
        # Return JSON response
        return json.dumps(models_data)


# start controller for fetching existing models
    @http.route('/o2b/delete_group_category', auth='none', type='json',methods=['POST','OPTIONS'] , csrf=False , cors='*')
    def delete_group_category(self, **kw):
         # print("we are in delete group category controller.")
        #  # print("all request body ; ", json.loads(request.httprequest.data.decode('utf-8')))
        complete_req = json.loads(request.httprequest.data.decode('utf-8'))
         # print(" ****** delete group api in odoo"  ,  complete_req )
        group_name = complete_req.get('group_name').strip() if complete_req.get('group_name') else complete_req.get('group_name')
         # print(" ** group name : ", group_name)
        is_group_exist = request.env['res.groups'].sudo().search([('name','=',group_name )],order='create_date asc, id asc', limit=1)
         # print("group is found or not: ",is_group_exist)
        if is_group_exist:
            is_group_exist.unlink()
        return json.dumps({"status" : True})


# start controller for fetching existing models
    @http.route('/o2b/create_group_category', auth='none', type='json',methods=['POST','OPTIONS'] , csrf=False , cors='*')
    def create_group_category(self, **kw):
        complete_req = json.loads(request.httprequest.data.decode('utf-8'))
        _logger.info(" complete grop request : %s",str(complete_req))
        group_type  = complete_req.get('group_type').strip() if complete_req.get('group_type') else complete_req.get('group_type') 
        group_id    = complete_req.get('group_id').strip() if complete_req.get('group_id') else complete_req.get('group_id')
        group_name  = complete_req.get('group_name').strip() if complete_req.get('group_name') else complete_req.get('group_name')
        category_id = complete_req.get('category_id').strip() if complete_req.get('category_id') else complete_req.get('category_id')
        category_name = complete_req.get('category_name').strip() if complete_req.get('category_name') else complete_req.get('category_name')
        sub_group = complete_req.get('sub_group')
        
        if not category_name:
            category_name = 'Extra Rights'
        # FIXED_CATEGORY = 'Oflow'
        # category_name = FIXED_CATEGORY

        if group_name:
            group_name = group_name.replace(' ','_').lower()

        if not group_id and not category_id and category_name and group_name:
            is_category_exist = request.env['ir.module.category'].sudo().search([('name','=',category_name )],order='create_date asc, id asc', limit=1)
            if not is_category_exist:
                new_category = request.env['ir.module.category'].with_user(2).sudo().create({
                'name':category_name,
                'sequence': '',
                })
                is_category_exist = new_category
            is_group_exist = request.env['res.groups'].sudo().search([('name','=',group_name )],order='create_date asc, id asc', limit=1)
            if not is_group_exist:
                new_group = request.env['res.groups'].with_user(2).sudo().create({
                'name':group_name,
                'category_id':is_category_exist.id ,
                })
                is_group_exist = new_group
            # insert data in ir_model_data
            ir_model_data = ''
            if group_type=='new':
                ir_model_data = request.env['ir.model.data'].sudo().search([('name','=', group_name.replace(' ','_').lower())])
                if ir_model_data:
                    ir_model_data.unlink()

                ir_model_data = request.env['ir.model.data'].with_user(2).sudo().create({
                'name'      : is_group_exist.name.replace(' ','_').lower(),
                'res_id'    : is_group_exist.id,
                'module'    : 'base',
                'model'     : 'res.groups'  
                })
            if group_type=='existing':
                ir_model_data = request.env['ir.model.data'].sudo().search([('res_id','=', is_group_exist.id)])

            if sub_group:
                sub_group_id = []
                for rec in sub_group:
                    group = rec.split('.')[-1]
                    find_sub_group = request.env['res.groups'].sudo().search([('name','=',group )],order='create_date asc, id asc', limit=1)
                    if find_sub_group:
                        sub_group_id.append(find_sub_group.id)
                is_group_exist.sudo().write({
                    'implied_ids': sub_group_id
                    })
            data_list = {
                'group_id'      : is_group_exist.id,
                'group_name'    : is_group_exist.name,
                'category_id'   : is_category_exist.id,
                'category_name' : is_category_exist.name,
                'group_type'    : group_type,
                'status'        : True,
                'internal_name' : ir_model_data.name
                }
            return json.dumps(data_list)
        return json.dumps({"status" : False})

    @http.route('/restart_oflow', type='json', auth='none', methods=['POST'], csrf=False)
    def restart_oflow(self):
        try:
            _logger.info("######SERVER STOP AND START BLOCK##############")
            headers = {key: value for key, value in request.httprequest.headers.items()}
            security_key = headers.get('X-Security-Key')
            if security_key != 'o2b_technologies':
                return json.dumps( {"message":"Security key is Invalid.",'code':'401'})
            body = json.loads(request.httprequest.data.decode('utf-8'))
        
            subprocess.Popen(['bash', '/opt/restart_oflow.sh'])
            # time.sleep(1)
            _logger.info("Oflow service restarted successfully.")
        except subprocess.CalledProcessError as e:
            _logger.error(f"Error restarting service: {e}")

    def restart_server(self):
        try:
            _logger.info(" **method to restart server")
            subprocess.Popen(['bash', '/opt/restart_oflow.sh'])
            _logger.info("Oflow service restarted successfully.")
        except subprocess.CalledProcessError as e:
            _logger.error(f"Error restarting service: {e}")
            # return "Error restarting service", 500



    @http.route('/upgrade/module', type='json', auth='none', methods=['POST'], csrf=False)
    def upgrade_module(self):
        try:
            _logger.info("######upgrade command initiated.K##############")
            headers = {key: value for key, value in request.httprequest.headers.items()}
            security_key = headers.get('X-Security-Key')
            if security_key != 'o2b_technologies':
                return json.dumps( {"message":"Security key is Invalid.",'code':'401'})
            body = json.loads(request.httprequest.data.decode('utf-8'))
            process_name = body.get('process_name')
            if process_name:
                process_name = process_name.strip()
        
            self.update_app_list_upgrade(process_name)
            _logger.info("Oflow  module upgraded successfully.")
            return {"message":"Upgraded command initiated.",'code':'201'}
        except Exception as e:
            _logger.error(f"Error restarting service: {e}")
            return {"message":"Upgraded command stuck ."+ str(e),'code':'500'}


    @http.route('/post/data', type='json', auth='none', methods=['POST'], csrf=False)
    def global_create_record_json_api(self):
        try:
            user = request.env['res.users'].with_user(1).browse(2) 
            timezone = user.tz
            print("Odoobot's Timezone:", timezone)
            _logger.info(" ** global_create_record_json_api")
            headers = {key: value for key, value in request.httprequest.headers.items()}
            security_key = headers.get('X-Security-Key')
            if security_key != 'o2b_technologies':
                return json.dumps( {"message":"Security key is Invalid.",'code':'401'})

            body = json.loads(request.httprequest.data.decode('utf-8'))
            process_detail = body.get('processDetail')
            fields = body.get('fields')
            # table_fields = body.get('tableFields')
            table_fields = body.get('tableFieldData')
            _logger.info(" ** process_detail  : %s ", process_detail)
            _logger.info(" ** fields data  : %s ", fields)
            model = None
            record = None
            if process_detail:
                process_id = process_detail.get('process_id')
                process_name = process_detail.get('process_name')
                stage_id = process_detail.get('process_stage_id')
                # check json api is enable
                process_obj = request.env['o2b.process.modular'].sudo().search([('process_id', '=', process_id.strip())],limit=1)
                auto_next_step = process_obj.auto_process_api_status
                print(" *** auto process api status ", auto_next_step)

                # if not auto_next_step:
                #     # return "AutoNextStep  option is disable for this process.Enable and redeploy the process again."
                #     return json.dumps( {"message":"AutoNextStep  option is disable for this process.Enable and redeploy the process again.",'code':'401'})
                
                if process_id and process_name:
                    statusbar = request.env['o2b.process.modular.statusbar'].sudo().search([('process_name', '=',process_name.strip()),('process_id','=',process_id.strip()),('process_node_id','=',stage_id.strip())])
                    print(" process id ", process_id)
                    print(" process name ", process_name)
                    print(" process stage_id ", stage_id)
                    print(' status basrr finding', statusbar)
                    if not statusbar:
                        return "Process id does not exist.Please check and try again."
                    if statusbar:
                        # create record with one field with stages
                        model = request.env['ir.model'].sudo().search([('model','=',statusbar.model_name)],limit=1)
                        _logger.info("*** model exist or not: %s", str(model))
                        record = request.env[statusbar.model_name].with_user(1).sudo().create({
                                'x_o2b_stage' : statusbar.stage_value,
                                # 'create_uid'  : 2
                                })
                        _logger.info(" ** record create  with object %s ",str(record))
                        # check how many field is there to update newly created record
                        udpate_dict = {}
                        for key, value in fields.items():
                            _logger.info(" ** current model field name :%s and value is : %s", key, value)
                            field_existance = request.env['ir.model.fields'].sudo().search(['&',('name','=',key),('model','=',statusbar.model_name)],limit=1)
                            _logger.info(' ** database have field name %s and type : %s ',field_existance.name, field_existance.ttype)
                            if field_existance:
                                if field_existance.ttype == 'boolean' and value:
                                    udpate_dict[key] = True

                                if field_existance.ttype in ['char','html','text'] and value:
                                    udpate_dict[key] = str(value)

                                if field_existance.ttype == 'float' and value:
                                    udpate_dict[key] = float(value)

                                if field_existance.ttype == 'integer' and value.isdigit():
                                    udpate_dict[key] = int(value)

                                if field_existance.ttype in ['date'] and value:
                                    try:
                                        udpate_dict[key] = datetime.datetime.strptime(value, '%d/%m/%Y').date()
                                    except Exception as e:
                                        udpate_dict[key] = datetime.date.today()

                                if field_existance.ttype in ['datetime'] and value:
                                    try:
                                        print("My current time: ", datetime.datetime.now())
                                        print("User input value: ", value)
                                        hour = 0
                                        minute = 0
                                        if timezone and timezone == 'Asia/Calcutta':
                                            hour = 5
                                            minute = 30
                                        user_datetime = datetime.datetime.strptime(value, '%d/%m/%Y %H:%M')
                                        adjusted_datetime = user_datetime - datetime.timedelta(hours = hour, minutes = minute)
                                        udpate_dict[key] = adjusted_datetime.strftime('%Y-%m-%d %H:%M:%S')
                                        print("Adjusted datetime: ", adjusted_datetime)
                                    except Exception as e:
                                        udpate_dict[key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                        print("Error occurred: ", str(e))
                                        print("Fallback to current time: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


                                if field_existance.ttype == 'json' and value:
                                    udpate_dict[key] = json.dumps(value, ensure_ascii=False)

                                if field_existance.ttype == 'selection' and value:
                                    selection_field = request.env['ir.model.fields.selection'].sudo().search([('field_id', '=',field_existance.id),('name', '=',value)],limit=1)
                                    if selection_field:
                                        udpate_dict[key] = str(selection_field.value)

                                if field_existance.ttype in ['many2one'] and value:
                                    _logger.info("** handle many2one field %s ", value)
                                    if field_existance.relation:
                                        record_id = None
                                        try:
                                            if value.isdigit():
                                                print("The string contains only numbers.")
                                                record_search = request.env[field_existance.relation].sudo().search([('id','=', int(value))],limit=1)
                                                record_id= record_search.id
                                            else:
                                                record_search = request.env[field_existance.relation].sudo().search([('name','=',value)],limit=1)
                                                record_id= record_search.id
                                            if record_id:
                                                udpate_dict[key] = record_id
                                        except Exception as e:
                                            _logger.info("** error while handlin m2o field %s", str(e))
                                    else:
                                        _logger.info(" ** field relation model name is: %s", field_existance.relation)

                                if field_existance.ttype in ['many2many'] and value:
                                    _logger.info("** handle many2many field %s ", value)
                                    print("many2many man", field_existance.relation)
                                    if field_existance.relation and field_existance.relation_table and field_existance.column1 and field_existance.column2:
                                        record_id = None
                                        try:
                                            elements = value.split(',')
                                            user_ids = []
                                            for element in elements:
                                                element = element.strip()
                                                if element.isdigit():
                                                    record_search = request.env[field_existance.relation].sudo().search([('id','=', int(element))],limit=1)
                                                    if record_search:
                                                        user_ids.append(int(record_search.id))
                                                else:
                                                    record_search = request.env[field_existance.relation].sudo().search([('name', '=', element)], limit=1)
                                                    if not record_search:
                                                        record_search = request.env[field_existance.relation].sudo().create({'name':element})
                                                    if record_search:
                                                        user_ids.append(record_search.id)
                                            udpate_dict[key] = [(6, 0, user_ids)]
                                        except Exception as e:
                                            _logger.info("** error while handlin m2m field %s", str(e))
                                    else:
                                        _logger.info(" ** field relation model name is: %s", field_existance.relation)
                              
                                if field_existance.ttype in ['binary','many2one_reference','one2many','reference'] and value:
                                    _logger.info("** we will handle after proper request get")

                        _logger.info("** updated new dictionary to be udpated %s",udpate_dict )
                        record.with_user(1).write(udpate_dict)
                        # handle table_fields data and update record 
                        # print(" ***** handled table_fields table_fields ", table_fields)
                        if table_fields:
                            for entry in table_fields:
                                print(" Entery Erntyer ", entry)
                                model_name = next(iter(entry))
                                dummy_model_name = model_name
                                print(" #### mdle name ", model_name)
                                my_table_data = entry.get(model_name)
                                print(" my_table_data : ", my_table_data)
                                if my_table_data:
                                    print(f"Processing {model_name}:")
                                    model_name = 'o2b.'+ model_name
                                    print(f"Processing chage naem to latest modle name {model_name}:")
                                    result_id = self.handle_table_data_json_api(record,model_name,key,value,my_table_data,dummy_model_name,timezone)
                        # check json api is enable
                        code = 'o2b_' + process_name.replace(' ','_').lower()
                        reference_no = False
                        if hasattr(record, 'x_reference_no'):
                            record.with_user(2).sudo().write({
                                'x_reference_no' :request.env['ir.sequence'].with_user(2).sudo().next_by_code(code)
                                })
                            reference_no = getattr(record, "x_reference_no")

                        process_obj = request.env['o2b.process.modular'].sudo().search([('process_id', '=', process_id.strip())],limit=1)
                        auto_next_step = process_obj.auto_process_api_status
                        if auto_next_step:
                            request.env['o2b.process.modular'].process_manager_insert(process_id,record.id,'json_api')
                            record.write({'x_done':False})
                        
                        response = json.dumps({"message":"Record created successfully with record id : " + str(record.id)})
                        if reference_no:
                            response = json.dumps({"message":"Record created successfully with reference id : "+str(reference_no)})
                        return response
        except Exception as e:
            _logger.error(f"Error restarting service: {e}")
            response = json.dumps({"message":"Record is created ."})
            return response;
            return Response(response, status=500, content_type='application/json')


    # handle talbe data if exist in json api
    # @http.route('/post/data', type='json', auth='none', methods=['POST'], csrf=False)
    def handle_table_data_json_api(self,record_id,model_name,key,value,my_table_data,dummy_model_name,timezone):

        try:
            print(" table table my model ", model_name)
            parent_obj = record_id
            udpate_dict = {}
            for key, value in my_table_data.items():
                print(f"{key}: {value}")
                _logger.info(" in try blocck model nae: %s and recod id %s amd field name %s ", record_id,model_name, key)
                field_existance = request.env['ir.model.fields'].sudo().search(['&',('name','=',key),('model','=',model_name)],limit=1)
                _logger.info(' ** database have field name %s and type : %s ',field_existance.name, field_existance.ttype)
                _logger.info(' ** field_existance object %s ',str(field_existance))
                if field_existance:
                    if field_existance.ttype == 'boolean' and value:
                        udpate_dict[key] = True

                    if field_existance.ttype in ['char','html','text'] and value:
                        udpate_dict[key] = str(value)

                    if field_existance.ttype == 'float' and value:
                        udpate_dict[key] = float(value)

                    if field_existance.ttype == 'integer' and value.isdigit():
                        udpate_dict[key] = int(value)

                    if field_existance.ttype in ['date'] and value:
                        try:
                            udpate_dict[key] = datetime.datetime.strptime(value, '%d/%m/%Y').date()
                        except Exception as e:
                            udpate_dict[key] = datetime.date.today()
                    
                    if field_existance.ttype in ['datetime'] and value:
                        try:
                            print("My current time: ", datetime.datetime.now())
                            print("User input value: ", value)
                            hour = 0
                            minute = 0
                            if timezone and timezone == 'Asia/Calcutta':
                                hour = 5
                                minute = 30
                            user_datetime = datetime.datetime.strptime(value, '%d/%m/%Y %H:%M')
                            adjusted_datetime = user_datetime - datetime.timedelta(hours = hour, minutes = minute)
                            udpate_dict[key] = adjusted_datetime.strftime('%Y-%m-%d %H:%M:%S')
                            print("Adjusted datetime: ", adjusted_datetime)
                        except Exception as e:
                            udpate_dict[key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print("Error occurred: ", str(e))
                            print("Fallback to current time: ", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


                    if field_existance.ttype == 'json' and value:
                        udpate_dict[key] = json.dumps(value, ensure_ascii=False)

                    if field_existance.ttype == 'selection' and value:
                        selection_field = request.env['ir.model.fields.selection'].sudo().search([('field_id', '=',field_existance.id),('name', '=',value)],limit=1)
                        if selection_field:
                            udpate_dict[key] = str(selection_field.value)

                    if field_existance.ttype in ['many2one'] and value:
                        _logger.info("** handle many2one field  in table %s ", value)
                        if field_existance.relation:
                            record_id = None
                            f_relation = field_existance.relation
                            if f_relation  and  f_relation =='_unknown':
                                f_relation = 'product.product'
                            else:
                                f_relation = field_existance.relation 
                            try:
                                if value.isdigit():
                                    record_search = request.env[f_relation].sudo().search([('id','=', int(value))],limit=1)
                                    record_id= record_search.id
                                else:
                                    record_search = request.env[f_relation].sudo().search([('name','=',value)],limit=1)
                                    record_id= record_search.id
                                if record_id:
                                    udpate_dict[key] = record_id
                            except Exception as e:
                                _logger.info("** error while handlin m2o field %s", str(e))
                        else:
                            _logger.info(" ** field relation model name is: %s", field_existance.relation)
                    
                    if field_existance.ttype in ['many2many'] and value:
                        _logger.info("** handle many2many field %s ", value)
                        print("many2many man", field_existance.relation)
                        if field_existance.relation and field_existance.relation_table and field_existance.column1 and field_existance.column2:
                            record_id = None
                            try:
                                elements = value.split(',')
                                user_ids = []
                                for element in elements:
                                    element = element.strip()
                                    if element.isdigit():
                                        record_search = request.env[field_existance.relation].sudo().search([('id','=', int(element))],limit=1)
                                        if record_search:
                                            user_ids.append(int(record_search.id))
                                    else:
                                        record_search = request.env[field_existance.relation].sudo().search([('name', '=', element)], limit=1)
                                        if not record_search:
                                            record_search = request.env[field_existance.relation].sudo().create({'name':element})
                                        if record_search:
                                            user_ids.append(record_search.id)
                                udpate_dict[key] = [(6, 0, user_ids)]
                            except Exception as e:
                                _logger.info("** error while handling m2m field in table : %s", str(e))
                        else:
                            _logger.info(" ** field relation model name is in table : %s", field_existance.relation)

                    if field_existance.ttype in ['binary','many2one_reference','one2many','reference'] and value:
                        _logger.info("** we will handle after proper request for table field.")
            udpate_dict[dummy_model_name+'new_table_model'] = parent_obj.id
            _logger.info("** update in table dictionary %s",udpate_dict )
            record = request.env[model_name].sudo().create(udpate_dict)
            return record.id
        except Exception as e:
            _logger.info(" **** handle table field %s ", e)

# *********************************server restart mid not view execute *****************************************************
    
    @http.route('/parse/create/field', auth='none', type='json',methods=['POST','OPTIONS'] , csrf=False , cors='*')
    def create_processfield(self, **kw):
        # try:
            _logger.info("\n ****** hited /parse/create/field  :%s ", request.httprequest.path)
            _logger.info("\n we are in first step ****")
            end_point = request.httprequest.path
            json_data = json.loads(request.httprequest.data.decode('utf-8'))
            # print("rfrfr **** ",json_data)

            process = json_data.get('process')
            process_image = json_data.get('process_image')
            database_setup_key = request.env['ir.config_parameter'].sudo().search([('key','=', 'oflow_security_key')],limit=1)
            temp_url = json_data.get('midurl')
            client_rule_engine = json_data.get('client_rule_engine')
            print(" hello test this is my furl testing: ", client_rule_engine)

            if not database_setup_key:
                return json.dumps({'message': "Security key not found."})
            activities = json_data.get('activities')
            result = self.is_valid_process(process,database_setup_key)
            process_token = result[0]
            alert_message = result[0] 
            is_valid = result[1]
            process_token = process.get('process_id').strip()
            if not is_valid:
                return json.dumps({'message': alert_message})

            if is_valid == True:
                internal_model_name = 'o2b.'+ process.get('process_name').replace(" ","_").lower().rstrip()
                record_process = request.env['o2b.process.modular'].sudo().search([('process_id', '=',process_token)])
                if record_process:

                    _logger.info(" ***** no name** %s ", str(record_process))
                    # this  method rectify previously deployee app by writing updated code -start
                    self.rectify_python_code(record_process)
                    # this  method rectify previously deployee app by writing updated code  -end 

                    record_process.sudo().write({
                        'process_id'    : process_token,
                        'process_name'  : process.get('process_name'),
                        'model_name'    : internal_model_name,
                        'model_detail'  : process.get('process_detail'),
                        'user_name'     : process.get('user_id'),
                        'fields_data'   : json_data.get('fields'),
                        'menu_data'     : json_data.get('menu'),
                        'action_data'   : json_data.get('action'),
                        'access_right_data': json_data.get('access'),
                        'button_data'   : json_data.get('button'),
                        'user_request'  : json_data,
                        'process_temp_url': temp_url,
                        'client_rule_engine_enable': client_rule_engine if client_rule_engine else False,
                        })                
                else:
                    record_process_new = request.env['o2b.process.modular'].sudo().create({
                       'process_id'     : process_token,
                       'process_name'   : process.get('process_name'),
                        'model_name'    : internal_model_name,
                        'model_detail'  : process.get('process_detail'),
                        'user_name'     : process.get('user_id'),
                        'button_data'   : json_data.get('button'),
                        'user_request'  : json_data,
                        'process_temp_url': temp_url,
                        'client_rule_engine_enable': client_rule_engine if client_rule_engine else False,
                        })
                    record_process = record_process_new
                record_process_stage = request.env['o2b.process.modular.stage'].sudo().search([('process_name', '=',process.get('process_name').strip())])
                if record_process_stage:
                    record_process_stage.unlink()
            counter = 0
            for data in activities:
                next_stage_new = data.get('activity_next_name')
                if next_stage_new  and data.get('activity_type') not in ['decision','email_verify']:
                    next_stage_new = data.get('activity_next_name').strip()
            
                record_process_new_stage = request.env['o2b.process.modular.stage'].with_user(2).sudo().create({
                    'process_stages'    : record_process.id,
                    'process_id'        : process_token,
                    'process_name'      : process.get('process_name').strip(),
                    'activity_name'     : data.get('activity_name').strip(),
                    'previous_stage'    : 'null' if data.get('activity_prev_name')== None else data.get('activity_prev_name').strip(),
                    'current_stage'     : data.get('activity_name').strip(),
                    'next_stage'        : next_stage_new,
                    'activity_type'     : data.get('activity_type') if data.get('activity_type') else 'null',
                    'model_name'        : internal_model_name,
                    'previous_stage_id' : data.get('activity_prev'),
                    'current_stage_id'  : data.get('activity_id'),
                    'next_stage_id'     : data.get('activity_next'),
                    })
                counter +=1
            # start code for insert and updagte user condition in condition table related to each process                
            record_decision = request.env['o2b.process.modular.stage.decision'].sudo().search([('process_name', '=',process.get('process_name').strip())])
            if record_decision:
                record_decision.unlink()
            for data in activities:
                if data.get('activity_type') == 'decision':
                    print(" decision data :: **** ", data)
                    print("In decision insertion ",data.get('activity_next_name'))
                    print("In decision insertion ",data.get('activity_next_name')[0])
                    
                    decision_data = data.get('activity_next_name')
                    if decision_data:
                        counter = 1
                        for rec in decision_data:
                            record_decision_new = request.env['o2b.process.modular.stage.decision'].with_user(2).sudo().create({
                                'process_decision_line': record_process.id,
                                'process_id'        : process_token,
                                'process_name'      : process.get('process_name').strip(),
                                'previous_id'    : data.get('activity_prev').strip() if data.get('activity_prev') else 'null',
                                'previous_stage'    : data.get('activity_prev_name').strip() if data.get('activity_prev_name') else 'null',
                                'next_stage'        : rec.get('nextStep').strip() if rec.get('nextStep') else 'null',
                                'next_stage_id'     : rec.get('nextStepId'),
                                'o2b_sequence'      : counter,
                                'domain'            : rec.get('condition'),
                                'odoo_domain'       : self.domain_parse(rec.get('condition')),
                                'decision_name'     : data.get('activity_name').strip(),
                                'decision_id'       : data.get('activity_id').strip(),
                                'exception_state'   : data.get('elseNextStep').get('nextStep') if data.get('elseNextStep') else  "null",
                                'exception_state_id': data.get('elseNextStep').get('nextStepId') if data.get('elseNextStep') else  "null",
                                })
                            counter +=1
            # end code for insert and updagte user condition in condition table related to each process
            exist_email_verified = request.env['o2b.process.modular.emailverified'].sudo().search([('process_name', '=',process.get('process_name').strip())])

            if exist_email_verified:
                exist_email_verified.unlink()
            for data in activities:
                if data.get('activity_type') == 'email_verify':
                    print(" **********we are in email verified : ", data)
                    email_data = data.get('email_verify_fields')
                    print(" email verified data ", email_data)
                
                    print(" email vaefiried data : ",email_data)
                    new_email_verified = request.env['o2b.process.modular.emailverified'].with_user(2).sudo().create({
                    'email_verified_line'   : record_process.id,
                    'process_id'            : process_token,
                    'process_name'          : process.get('process_name').strip(),
                    'current_stage'         : data.get('activity_name').strip(),
                    'current_id'            : data.get('activity_id').strip(),
                    'email_verify_list'     : data.get('email_verify_fields')
                    })
            # end code for insert and updagte user condition in condition table related to each process

            # start code for create statusbar stage in table
            p_name = process.get('process_name')
            if p_name:
                p_name = p_name.strip()

            
            for data in activities:
                 # _logger.info("*** insert statusbar table %s ", data)
                node_id = data.get('activity_id')
                if node_id:
                    node_id = node_id.strip()
                cur_stage = request.env['o2b.process.modular.statusbar'].sudo().search([('process_name', '=',p_name),('process_node_id','=',node_id)])
                if cur_stage:
                    if data.get('activity_type').strip() == cur_stage.node_type and data.get('activity_id') == cur_stage.process_node_id:
                        cur_stage.sudo().write({
                            'stage_name'        : data.get('activity_name').strip(),
                            'model_name'        : internal_model_name,
                            })
                if not cur_stage:
                    record_statusbar = request.env['o2b.process.modular.statusbar'].with_user(2).sudo().create({
                        'process_stage_line': record_process.id,
                        'process_id'        : process_token,
                        'model_name'        : internal_model_name,
                        'process_name'      : process.get('process_name').strip(),
                        'process_node_id'   : data.get('activity_id').strip(),
                        'stage_name'        : data.get('activity_name').strip(),
                        'stage_value'       : data.get('activity_name').replace(' ','_').lower(),
                        'node_type'         : data.get('activity_type').strip(),
                        })
            
            # # code to remove extra node monday
            store_ids = request.env['o2b.process.modular'].sudo().search([('process_id', '=',process_token)],limit=1)
            cur_node_id = []
            cur_node_name = []
            saved_node_id = []
            saved_node_name = []
            for data in activities:
                # _logger.info("*** insert statusbar table %s ", data)
                node_id = data.get('activity_id')
                node_name = data.get('activity_name')
                node_type = data.get('activity_type')
                if node_id and node_type not in ['email','email_verify','webform','decision']:
                    cur_node_id.append(node_id)
                    cur_node_name.append(node_name)
            filtered_objects = request.env['o2b.process.modular.menu'].sudo().search([('process_id', '=',process_token),('menu_type','not in',['main app','start app'])])
            store_ids.sudo().write({
                'process_menu_name_list' : cur_node_name,
                'process_menu_node_list' : cur_node_id,
                })
            
            for rec_data in filtered_objects:
                if rec_data.menu_name in cur_node_name:
                    # print(" ** this is active menudb", rec_data.menu_name )
                    _logger.info(" **find data filtered_objects.menu_name %s : and list menu %s", rec_data.menu_name,cur_node_name)
                else:
                    action_id = rec_data.action_id
                    menu_id =   rec_data.menu_id
                    extra_action_obj = request.env['ir.actions.act_window'].sudo().search(['&',('name','=',rec_data.menu_name),('id','=',action_id)], limit=1)
                    if extra_action_obj:
                        extra_action_obj.unlink()
            # code start for save group name for all node:
            record_process_group = request.env['o2b.process.modular.group'].sudo().search([('process_name', '=',process.get('process_name').strip())])
            if record_process_group:
                record_process_group.unlink()
            record_process_main_app = request.env['o2b.process.modular.group'].with_user(2).sudo().create({
                    'process_groups'    : record_process.id,
                    'process_id'        : process_token,
                    'process_name'      : process.get('process_name').strip(),
                    'activity_name'     : 'main app',
                    'activity_type'     : 'main app',
                    'model_name'        : internal_model_name,
                    'node_id'           : None,
                    'group'             : process.get('process_group')
                    })

            counter = 0
            for data in activities:
                if data.get('activity_type') == 'start':
                    record_process_start_app = request.env['o2b.process.modular.group'].with_user(2).sudo().create({
                    'process_groups'    : record_process.id,
                    'process_id'        : process_token,
                    'process_name'      : process.get('process_name').strip(),
                    'activity_name'     : data.get('activity_name').strip(),
                    'activity_type'     : 'start app',
                    'model_name'        : internal_model_name,
                    'node_id'           : data.get('activity_id'),
                    'group'             : process.get('process_group')
                    })

                record_process_new_group = request.env['o2b.process.modular.group'].with_user(2).sudo().create({
                    'process_groups'    : record_process.id,
                    'process_id'        : process_token,
                    'process_name'      : process.get('process_name').strip(),
                    'activity_name'     : data.get('activity_name').strip(),
                    'activity_type'     : data.get('activity_type') if data.get('activity_type') else 'null',
                    'model_name'        : internal_model_name,
                    'node_id'           : data.get('activity_id'),
                    'group'             : data.get('activity_group')
                    })
                counter +=1
            
            record_email = request.env['o2b.process.modular.email'].sudo().search([('process_name', '=',process.get('process_name').strip())])
            if record_email:
                record_email.unlink()


            # start code for deleting all store field start here
            record_fields = request.env['o2b.process.modular.field.method'].sudo().search([('process_id', '=',process_token)])
            if record_fields:
                record_fields.unlink()

            # start code for deleting all store field end
            for data in activities:
                # print(" datarrrrrrrrrrrrrrrrr data : ", data)
                # print(" datarrrrrrrrrrrrrrrrr data juston : ", json.dumps(data))
                if data.get('activity_type') == 'email':

                    email_template = data.get('template')
                    print(" email template : ", email_template)
                    print(" email template  json : ", json.dumps(email_template))
                    to = subject = message = ''
                    if email_template:
                        to = email_template.get('recipientEmail')
                        subject = email_template.get('mail_subject')
                        message = email_template.get('mail_body')
                        template_id = email_template.get('template_id')
                        mail_triger = email_template.get('mail_trigger')
                        # print(" while creating mail triiger : ", mail_triger)
                        # print(" while creating mail triigerffffffffffff : ", json.dumps(mail_triger))
                        mail_limit = email_template.get('mail_limit')
                        rec_email = request.env['o2b.process.modular.email'].with_user(2).sudo().create({
                            'process_email_line': record_process.id,
                            'process_id'        : process_token,
                            'process_name'      : process.get('process_name').strip(),
                            'model_name'        : internal_model_name,
                            'prev_step'         : data.get('activity_prev_name').strip() if data.get('activity_prev_name') else 'null',
                            'next_step'         : data.get('activity_next_name').strip(),
                            'next_step_id'      : data.get('activity_next').strip(),
                            'current_step'      : data.get('activity_name'),
                            'current_node_id'   : data.get('activity_id'),
                            'recipient'         : data.get('emailTo'),
                            'mail_subject'      : subject,
                            'mail_body'         : message,
                            'template_id'       : template_id,
                            'mail_trigger'      : mail_triger,
                            'mail_limit'        : mail_limit,
                            })
                        
            # block to update dynamic webform controller or view start here
            for data in activities:
                class_name = 'o2b_' + process.get('process_name').replace(' ','_').lower()
                process_name = process.get('process_name')
                x_value = {'x_done': True}
                sequence_status = False
                push_process_manager = False
                if data.get('activity_type') == 'webform':
                    _logger.info("** webform sequence value: %s and autostep %s ",data.get('isCustomReferenceNumber'),data.get('isAutoNextStep'))
                    custom_model = request.env['ir.model'].sudo().search([('model', '=',internal_model_name)])
                    self.create_field('x_reference_no',custom_model,'char','x_reference_no',None,None,"Record reference Numeer",None,None,None,None,None)
                    if data.get('thankyouPage'):
                        thankyou_page = data.get('thankyou_page')

                    if data.get('isCustomReferenceNumber')== True:
                        sequence_data = data.get('customReferenceNumber')
                        if sequence_data:
                            digit = sequence_data.get('digits')
                            prefix = sequence_data.get('prefix')
                            suffix = sequence_data.get('suffix')
                            sequence = request.env['ir.sequence'].with_user(2).sudo().search([('code','=',class_name),('name','=', process_name)])
                            if sequence:
                                sequence.with_user(2).sudo().write({
                                'name'              : process_name,
                                'code'              : class_name,  
                                'padding'           : digit,
                                'prefix'            : prefix,
                                'suffix'            : suffix,
                                'number_increment'  : 1,
                                })
                            else:
                                sequence = request.env['ir.sequence'].with_user(2).sudo().create({
                                'name'              : process_name,
                                'code'              : class_name,  
                                'padding'           : digit,
                                'prefix'            : prefix,
                                'suffix'            : suffix,
                                'number_increment'  : 1,
                                })
                            
                            if custom_model:
                                self.create_field('x_reference_no',custom_model,'char','x_reference_no',None,None,"Record reference Numeer",None,None,None,None,None)
                                sequence_status = True
                    if data.get('isAutoNextStep') and data.get('isAutoNextStep') == True:
                        x_value = {'x_done': False}
                        push_process_manager = True
                    dict_symbol = "{}"
                    dynamic_dictionary = ""
                    dic_vairalbe_name = 'dict_value'
                    dic_equalt_to_symbol = '='
                    dic_start_symbol = '{'
                    dic_end_symbol = '}'
                    dic_start_symbol = '{'
                    controller_content =f'''\
from odoo import http, _
from odoo.http import request
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError
from werkzeug.wrappers import Response
import json
import logging
import random
from odoo.service import db, security
import werkzeug
import contextlib
from hashlib import sha256
import passlib.context
import re
import os
from odoo.exceptions import AccessDenied
import mimetypes
from urllib.parse import urlencode
_logger = logging.getLogger(__name__)
import base64
try:
    from base64 import encodebytes
except ImportError:
    from base64 import encodestring as encodebytes
from ast import literal_eval

class {class_name}(http.Controller):
    @http.route('/{class_name}/view', auth='public', website=True,csrf=False)
    def view(self, **kw):
        _logger.info("***webform fetch successfully.")
        return http.request.render('{class_name}.{class_name}')


    @http.route('/{class_name}/view/submit', auth='public', website=True,csrf=False)
    def view_submit(self, **kw):
        _logger.info("***webform updated successfully.")
        end_point = request.httprequest.path
        process_id = kw.get('process_id')
        if not process_id:
            return http.request.render('{class_name}.{class_name}')
        '''
                    response_record = "{'reference_id':record}"
                    contoller_end_content = f'''\n
        try:
            statusbar = request.env['o2b.process.modular.statusbar'].sudo().search([('process_id','=',process_id.strip())],limit=1)
            if statusbar:
                model = request.env['ir.model'].sudo().search([('model','=',statusbar.model_name)],limit=1)
                _logger.info("*** model exist or not: %s", str(model))
                record = request.env[statusbar.model_name].sudo().create({x_value})
                _logger.info(" ** record create  with object %s ",str(record))
                # check how many field is there to update newly created record
                udpate_dict = {dict_symbol}
                for key, value in dict_value.items():
                    _logger.info(" ** current model field name :%s and value is : %s", key, value)
                    field_existance = request.env['ir.model.fields'].sudo().search(['&',('name','=',key),('model','=',statusbar.model_name)],limit=1)
                    _logger.info(' ** database have field name %s and type : %s ',field_existance.name, field_existance.ttype)
                    if field_existance:
                        if field_existance.ttype == 'boolean' and value:
                            udpate_dict[key] = True

                        if field_existance.ttype in ['char','html','text'] and value:
                            udpate_dict[key] = str(value)

                        if field_existance.ttype == 'float' and value:
                            udpate_dict[key] = float(value)

                        if field_existance.ttype == 'integer' and value:
                            udpate_dict[key] = int(value)

                        if field_existance.ttype in ['date','datetime'] and value:
                            try:
                                udpate_dict[key] = datetime.strptime(value, '%Y-%m-%d').date()
                            except Exception as e:
                                udpate_dict[key] = datetime.date.today()

                        if field_existance.ttype == 'json' and value:
                            udpate_dict[key] = json.dumps(value, ensure_ascii=False)

                        if field_existance.ttype == 'selection' and value:
                            selection_field = request.env['ir.model.fields.selection'].sudo().search([('field_id', '=',field_existance.id),('value', '=',value)],limit=1)
                            if selection_field:
                                udpate_dict[key] = str(selection_field.value)
                      
                        if field_existance.ttype in ['binary','many2many','many2one','many2one_reference','one2many','reference'] and value:
                            _logger.info("** we will handle after proper request get")
                # udpate sequence in table:
                if {sequence_status}:
                    udpate_dict['x_reference_no'] = request.env['ir.sequence'].next_by_code('{class_name}')
                record.write(udpate_dict)
                if {push_process_manager}:
                    request.env['o2b.process.modular'].process_manager_insert(process_id,record.id,'webform')
            _logger.info("** updated new dictionary to be udpated %s",udpate_dict )
            return http.request.render('{class_name}.{class_name}_success',{response_record})
        except Exception as e:
            return http.request.render('{class_name}.{class_name}')
            
                    '''
                    doc_or_document_content = f'''\n
<record id="{class_name}_checklist" model="ir.ui.view">
    <field name="name">To do check list</field>
    <field name="model">{model_name}</field>
    <field name="arch" type="xml">
    <form create="false">
     <style>
        .requiredField label::after {openbraces}
          content: "* ";
          color: red;
      {closebraces}
      </style>
    <sheet>
    <h1><center>Todos Form</center></h1> 
        <group>
            <field name="id"/>
        </group>
    </sheet>
    </form>
    </field>
</record>

<record id="{class_name}_doclist" model="ir.ui.view">
    <field name="name">Document form</field>
    <field name="model">{custom_model.model}</field>
    <field name="arch" type="xml">
    <form create="false">
    <style>
        .requiredField label::after {openbraces}
          content: "* ";
          color: red;
      {closebraces}
      </style>
    <sheet>
    <h1><center>Document Form</center></h1> 
        <group>
            <field name="id"/>
        </group>
    </sheet>
    </form>
    </field>
</record>

                    '''
                    template_start = f'''\n
<odoo>
<template id="{class_name}">
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"/>
<title>Oflow</title>
</head>
<body>
    <div class="container  mt-5">
    <h1 class="text-center mt-2">Welcome to OflowAI.COM!</h1>
    <h4 class="text-center mt-2">Please fill record for process : {process_name}</h4>
    <form action="/{class_name}/view/submit" method="POST">
    <input type="hidden" name="process_id" value="{process.get('process_id')}" />
    '''
                    
                    template_end = f'''\n
    <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    </div>
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>
</template>

<template id="{class_name}_success">
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous"/>
<title>Oflow</title>
</head>
<body>
<div class="container  mt-5">
<div class="alert alert-success" role="alert">
<h1 class="text-center mt-2">Welcome to OflowAI.COM!</h1>
<h5 class="alert-heading  mt-2">Well done! 
<p  class="mt-2">Thanks to be a part of OflowAI.COM.We have successfully create your record.
</p></h5>
<h5>User can track this record  
<t t-if="reference_id.x_reference_no">
        With reference id: 
    <t t-esc="reference_id.x_reference_no"/>
</t>
<t t-else="">
    <span>With record id:<t t-esc="reference_id.id"/></span>
</t>
</h5>
    { data.get('thankyouPage')}
<hr/>
<p class="mb-0">Whenever you need support.Feel free to contact us. <a href="/{class_name}/view">Create new Record.</a></p>
</div>
</div>
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>
</template>

{doc_or_document_content}
</odoo>

    '''
                    form_html = ""
                    controller_get_element = ""
                    for web in data.get('assigned_form'):
                        # _logger.info(" ** webform data %s", web)
                        for rec  in web:
                            label = rec.get('title')
                            input_type = rec.get('type')
                            input_id = rec.get('technicalName')
                            placeholder = rec.get('placeholder')
                            is_required = rec.get('isRequired')
                            is_readonly = rec.get('isReadOnly')
                            default_value = rec.get('defaultValue')
                            widget = rec.get('widget')
                            if input_type == 'boolean':
                                input_type = 'checkbox'
                            if input_type in ['char','html','text']:
                                input_type = 'text'
                            if input_type == 'float':
                                input_type = 'text'
                            if input_type == 'integer':
                                input_type = 'number'
                            if input_type in ['date','datetime']:
                               input_type = 'date'
                            if input_type == 'json':
                               input_type = 'text'
                            if input_type == 'selection':
                               input_type ='selection'
                            if input_type in ['binary','many2many','many2one','many2one_reference','one2many','reference','chatter','table']:
                                input_type ='neglect'
                            
                            if widget =='password':
                                input_type = 'password'

                            if widget =='email':
                                input_type = 'email'

                            if is_readonly and is_readonly ==True:
                                is_readonly = 'readonly'
                            else:
                                is_readonly = ''
                            if is_required and is_required ==True:
                                is_required = 'required'
                            else:
                                is_required = ''
                            if input_type not in ['checkbox','selection','neglect']:
                                form_html += f'''
    <div class="form-group">
    <label for="{input_id}">{label}</label>
    <input type="{input_type}" class="form-control" id="{input_id}" placeholder="{placeholder}" name="{input_id}"/>
    </div>
                                '''
                                controller_get_element+= f'''
        {input_id} = kw.get('{input_id}')

                                '''
                                dynamic_dictionary+= "'"+ input_id + "':" + input_id+","
                            elif input_type in ['checkbox']:
                                form_html += f'''
    <div class="form-check">
    <input type="{input_type}" class="form-check-input" id="{input_id}" name="{input_id}"/>
    <label class="form-check-label" for="{input_id}">{label}</label>
    </div>
                                '''
                                dynamic_dictionary+= "'"+ input_id + "':" + input_id+","
                                controller_get_element+= f'''
        {input_id} = kw.get('{input_id}')

                                '''
                            elif input_type in ['remark_history']:
                                if 'options' in rec:
                                    options = rec.get('options')
                                    select = ''
                                    for option in options:
                                        select += '<option value="'+option.strip().replace(' ','_').lower()+ '">' +option+ '</option>'
                                form_html += f'''
    <div class="form-check">
    <input type="text" class="form-check-input" id="x_remark"/>
    <label class="form-check-label" for="x_remark">Remark History</label>
    </div>
                                '''
                                controller_get_element+= f'''
        {input_id} = kw.get('{input_id}')

                                '''
                                dynamic_dictionary+= "'"+ input_id + "':" + input_id+","
                            elif input_type in ['selection']:
                                if 'options' in rec:
                                    options = rec.get('options')
                                    select = ''
                                    for option in options:
                                        select += '<option value="'+option.strip().replace(' ','_').lower()+ '">' +option+ '</option>'
                                form_html += f'''
    <div class="form-group">
    <label for="{input_id}">{label}</label>
    <select name="{input_id}" class="form-select" aria-label="multiple select example" style="width:100%;height:6%">
    {select}
    </select>
    </div>
                                '''
                                controller_get_element+= f'''
        {input_id} = kw.get('{input_id}')

                                '''
                                dynamic_dictionary+= "'"+ input_id + "':" + input_id+","

                        new_updae_dict = f'''
        {dic_vairalbe_name}{dic_equalt_to_symbol}{dic_start_symbol}{dynamic_dictionary}{dic_end_symbol}
                        '''

                        # replace all view content dynamically
                        final_view_content = template_start + form_html + template_end
                        controller_final_content = controller_content + controller_get_element + new_updae_dict+contoller_end_content
                        module_path = os.path.dirname(__file__)
                        # print("Module path :", module_path)
                        parent_dir = os.path.dirname(module_path)
                        addon_path = os.path.dirname(parent_dir)
                        # _logger.info("parent directory: %s ", parent_dir)
                        # _logger.info("current addone path directory addons aptch: %s ", addon_path)
                        module_dir = 'o2b_'+ process_name.replace(' ','_').lower()
                        controller_path = addon_path + '/'+ module_dir+'/controllers' + '/' + 'controllers.py'
                        view_path = addon_path + '/'+ module_dir+'/views' + '/' + 'views.xml'
                        # try:
                        # write view.xml fiel
                        with open(view_path, 'w', encoding='utf-8') as f:
                            f.write(final_view_content)
                        #     print(f"File content successfully replaced in: {view_path}")
                        # except Exception as e:
                        #     print(f"Error writing to file: {e}")
                        
                        # try:
                        # write controller.py
                        with open(controller_path, 'w', encoding='utf-8') as f:
                            f.write(controller_final_content)
                        #     print(f"File content successfully replaced in: {controller_path}")
                        # except Exception as e:
                        #     print(f"Error writing to file: {e}")

            # block to update dynamic webform controller or view end  here


            # code to to handle status for webform api and json api status for next step process or not
            for data in activities:
                class_name = 'o2b_' + process.get('process_name').replace(' ','_').lower()
                process_name = process.get('process_name')
                record_process = request.env['o2b.process.modular'].sudo().search([('process_id', '=',process_token)],limit=1)
                # if data.get('activity_type') == 'start' and data.get('activity_isApiEnable'):
                if data.get('activity_type') == 'start':
                    if record_process and  data.get('isAutoNextStep')== True:
                        record_process.sudo().write({'auto_process_api_status': True})
                    else:
                        record_process.sudo().write({'auto_process_api_status': False})

                    # handle reference number on start node
                    _logger.info("** webform sequence value: %s and autostep %s ",data.get('isCustomReferenceNumber'),data.get('isAutoNextStep'))
                    if data.get('isCustomReferenceNumber') == True:
                        sequence_data = data.get('customReferenceNumber')
                        if sequence_data:
                            digit = sequence_data.get('digits')
                            prefix = sequence_data.get('prefix')
                            suffix = sequence_data.get('suffix')
                            sequence = request.env['ir.sequence'].with_user(2).sudo().search([('code','=',class_name),('name','=', process_name)])
                            print(" checking sequence is avaialb e orn t:;", sequence)
                            if sequence:
                                print("##########################if ")
                                sequence.with_user(2).sudo().write({
                                'name'              : process_name,
                                'code'              : class_name,  
                                'padding'           : digit,
                                'prefix'            : prefix,
                                'suffix'            : suffix,
                                'number_increment'  : 1,
                                })
                            else:
                                sequence = request.env['ir.sequence'].with_user(2).sudo().create({
                                'name'              : process_name,
                                'code'              : class_name,  
                                'padding'           : digit,
                                'prefix'            : prefix,
                                'suffix'            : suffix,
                                'number_increment'  : 1,
                                })
                                print("##########################lee ",sequence)
                            # writing in new file
                            module_path = os.path.dirname(__file__)
                            parent_dir = os.path.dirname(module_path)
                            addon_path = os.path.dirname(parent_dir)
                            module_dir = 'o2b_'+ process.get('process_name').replace(' ','_').lower()
                            create_model_path = addon_path + '/'+ module_dir+'/models' + '/' + 'models.py'
                            start_tag = '# override create method start here'
                            end_tag = '# override create method end here'
                            braces = '{}'
                            content = f'''\n
    # override create method start here
    @api.model
    def create(self, vals):
        if 'x_reference_no' not in vals or not vals.get('x_reference_no'):
            vals['x_reference_no'] = self.env['ir.sequence'].next_by_code('{class_name}')
        return super({class_name}, self).create(vals)
    
    def copy(self, default=None):
        if default is None:
            default = {braces}
            default['x_reference_no'] = self.env['ir.sequence'].next_by_code('{class_name}')
            return super({class_name}, self).copy(default)
    # override create method end here
            '''             
                            self.update_file(create_model_path,content,start_tag,end_tag)


                if data.get('activity_type') == 'webform':
                    if record_process and  data.get('isAutoNextStep')== True:
                        record_process.sudo().write({'auto_process_webform_status': True})
                    else:
                        record_process.sudo().write({'auto_process_webform_status': False})


            if is_valid == False:
                return json.dumps({'success': 'No', 'message': process_token})
           
            custom_model = request.env['ir.model'].sudo().search([('model', '=',internal_model_name)])
            
            if not custom_model:
                return json.dumps( {"message":"Module installation wat not upgraded last time. please click deploy button again."})

            server_action = request.env['ir.actions.server'].sudo().search([('model_id','=',custom_model.id),('usage','=','ir_actions_server')])
            if server_action:
                server_action.unlink()
            server_action = request.env['ir.actions.server'].with_user(2).sudo().create({
                'type'                  :  'ir.actions.server',
                'binding_type'          :  'action',
                'binding_view_types'    :  'list,form',
                'name'                  :   process.get('process_name').rstrip() + 'server action',
                'model_id'              :   custom_model.id,
                'binding_model_id'      :   custom_model.id,
                'usage'                 :  'ir_actions_server',
                'state'                 :  'code',
                'model_name'            :   custom_model.model  ,   
                'code'                  :  "env['o2b.process.modular'].update_module_state()"

                })
            request.session['server_action_last'] = server_action.id
            custom_app  = request.env['ir.module.module'].sudo().search([('name', '=',internal_model_name)])
            node_length = len(activities)
            self.create_status_bar(activities,node_length,process,custom_model)
            for i in range(node_length):
                activity_name = activities[i].get('activity_name')
                activity_type = activities[i].get('activity_type')
                assigned_form = activities[i].get('assigned_form')
                node_id = activities[i].get('activity_id')
                form_view = activities[i].get('form_view')
                activity_group = activities[i].get('activity_group')
                activity_todos = activities[i].get('activity_todos')
                activity_doctype = activities[i].get('activity_doctype')
                # print(" activity todos : ", activity_todos)
                # print(" activity_doctype : ", activity_doctype)
                if activity_todos:
                    self.handle_todos(activity_todos,custom_model,node_id,activity_name,process,activity_type)
                if activity_doctype:
                    self.handle_doctype(activity_doctype,custom_model,node_id,activity_name,process,activity_type)

                if activity_type =='webform':
                    print("activity type: ", activity_type)
                
                form_length = 0
                if True:
                    if assigned_form is None:
                        form_length = 0 
                    else:
                        form_length = len(assigned_form)
                    for data in range(form_length):
                        for counter in range(len(assigned_form[data])):
                            input_field = assigned_form[data]
                            if assigned_form[data][counter].get('type')!= 'button' and  assigned_form[data][counter].get('type')!= 'separator' and  assigned_form[data][counter].get('type')!= 'table':
                                create_field = 'x_o2b_'+ assigned_form[data][counter].get('title').replace(' ','_').lower()
                                selection_value = None if not assigned_form[data][counter].get('options') else assigned_form[data][counter].get('options')
                                self.create_field(create_field,custom_model,assigned_form[data][counter].get('type'),assigned_form[data][counter].get('technicalName'),selection_value,input_field[counter],assigned_form[data][counter].get('title'),assigned_form[data][counter].get('domain'),process_token,activity_name,activity_type,node_id)
                            if assigned_form[data][counter].get('type') == 'tab':
                                for item in assigned_form[data]:
                                    for tab in item['tabs']:
                                        for content_list in tab['content']:
                                            print(" tab['content'] " ,tab['content'])
                                            for content_dict in content_list:
                                                tab_field = 'x_o2b_'+ content_dict['title'].replace(' ','_').lower()
                                                selection_value = None
                                                if content_dict['type'] =='selection':
                                                    selection_value = None if not content_dict['options'] else content_dict['options']
                                                
                                                if content_dict['type'] not in ['group']:
                                                    if content_dict['type'] == 'table' and content_dict['tableType'] =='new':
                                                        self.create_new_table(content_list,content_dict['columns'],custom_model)
                                                    self.create_field(tab_field,custom_model,content_dict['type'],content_dict['technicalName'],selection_value,content_dict,content_dict['title'],None,process_token,activity_name,activity_type,node_id)
                                                if content_dict['type'] in ['group']:
                                                    for record in content_dict['fields']:
                                                        for rec in record:
                                                            if rec.get('type') == 'table' and rec.get('tableType') =='new':
                                                                _logger.info(" tab->group_newtable record reocd : %s", str(record))
                                                                self.create_new_table(record,rec.get('columns'),custom_model)
                                                            self.create_field(rec.get('technicalName'),custom_model,rec.get('type'),rec.get('technicalName'),selection_value,rec,rec.get('title'),None,process_token,activity_name,activity_type,node_id)
                            if assigned_form[data][counter].get('type') == 'group': 
                                object_data = assigned_form[data][counter].get('fields')
                                for obj in object_data:
                                    for rec in obj:
                                        if rec.get('type') == 'table' and rec.get('tableType') =='new':
                                            self.create_new_table(obj,rec.get('columns'),custom_model)
                                        self.create_field(rec.get('technicalName'),custom_model,rec.get('type'),rec.get('technicalName'),None,rec,rec.get('title'),rec.get('domain'),process_token,activity_name,activity_type,node_id)
                                        # time.sleep(1)
                            
                            # for handling table data new creation
                            if assigned_form[data][counter].get('type') == 'table'  and assigned_form[data][counter].get('tableType')== 'new':
                                self.create_new_table(assigned_form[data],assigned_form[data][counter].get('columns'),custom_model)

                            # for remark history form field handling
                            if assigned_form[data][counter].get('type') == 'remark_history':
                                if assigned_form[data][counter].get('tabs'):
                                    if assigned_form[data][counter].get('tabs')[0].get('content'):
                                        data_list = assigned_form[data][counter].get('tabs')[0].get('content')
                                        for data in data_list:
                                            t_name =  data[0].get('technicalName')
                                            self.create_field(t_name,custom_model,data[0].get('type'),t_name,data[0].get('options'),data[0],data[0].get('title'),None,process_token,activity_name,activity_type,node_id)
            
            _logger.info(" \n*******initialising state is complete **********\n")
            # time.sleep(0.5)
            self.only_upgrade(process.get('process_name'))
            # self.update_app_list_upgrade(process.get('process_name'))
            # time.sleep(3)
            _logger.info("\nmodule is also upgraded successfully.")

            return json.dumps(
                    {
                    'message'   : 'All Model Related field is created successfully: ('+ process.get('process_name')+ ')',
                    'code'      : '200'
                    })
        # except Exception as e:
        #     _logger.info(" ** first api error :  %s ", str(e))
        #     pass
        #     return json.dumps(
        #         {
        #         'message'   : 'Error : ' + str(e),
        #         'code'      : '200'
        #         })


    # start test api that verify odoo is running successfully
    @http.route('/odoo/connection', auth='none', type='http',methods=['GET','OPTIONS'] , csrf=False , cors='*')
    def parse_hello(self, **kw):
        db_name = request.env.cr.dbname
        user_db = kw.get('db_name')
        user_api_key = kw.get('api_key')
        if user_api_key:
            user_api_key = user_api_key.strip()
        _logger.info("system db name: %s , user db : %s and user api key: %s ",db_name ,user_db,user_api_key)
        database_setup_key = request.env['ir.config_parameter'].sudo().search([('key','=', 'database.secret')],limit=1)
        if not database_setup_key:
            return json.dumps({'message': "Security key not found.",'code': '401'})

        if user_api_key and  user_api_key !=database_setup_key.value:
            return json.dumps({'message': 'Security key is Invalid.', 'code': '401'})
            
        if db_name and  db_name !=user_db.strip():
            return json.dumps({'message': 'Database name  is not matched.', 'code': '401'})

        return json.dumps({'message': 'Connection successfully', 'code': '201'})



    @http.route('/server/status', type='json', auth='none', methods=['POST'], csrf=False)
    def server_status(self):
        try:
            _logger.info(" ** we are server_status checking server is running or not")
            headers = {key: value for key, value in request.httprequest.headers.items()}
            security_key = headers.get('X-Security-Key')
            if security_key != 'o2b_technologies':
                return json.dumps( {"message":"Security key is Invalid.",'code':'401'})
            # Access request body
            body = json.loads(request.httprequest.data.decode('utf-8'))
            # time.sleep(2)
            return json.dumps( {"message":"Server is running",'code':'200'})
        except Exception as e:
            _logger.error(f"Error restarting service: {e}")
            return json.dumps( {"message":str(e),'code':'500'})



# **** controller for schedular on off ****
    @http.route(['/process/schedular/status/change/active','/process/schedular/status/change/inactive'], auth='none', type='http',methods=['GET','OPTIONS'] , csrf=False , cors='*')
    def module_schedular_changedActive(self, **kw):
        try:
            end_point = request.httprequest.path
            _logger.info("******* /process/schedular/status/change/active api ***** , %s ", str(kw))
            process_id = kw.get('process_id')
            security_key = kw.get('key')
            status = kw.get('status')
            if process_id:
                process_id = process_id.strip()
            if status:
                status = status.strip()
            if security_key:
                security_key = security_key.strip()
            database_setup_key = request.env['ir.config_parameter'].sudo().search([('key','=', 'oflow_security_key')],limit=1)
            if not database_setup_key:
                return json.dumps({'message': "Security key not found."})

            if security_key and  security_key !=database_setup_key.value:
                return json.dumps( {"message":"Security key is Invalid.",'code':'401'})

            record_process = request.env['o2b.process.modular'].sudo().search([('process_id', '=',process_id)],order="id desc" , limit=1)
            if not record_process:
                return json.dumps( {"message":"Process is not installed yet.",'code':'401'})

            # if record_process:
            #     model_name = 'o2b.' + record_process.process_name.replace(' ','_').lower()
            #     model_name = 'o2b.' + record_process.process_name.replace(' ','_').lower()
             # _logger.info("****model object is there or not: %s", model)
            # server_action_new = request.env['ir.actions.server'].with_user(2).sudo().create({
            # 'type'                  :  'ir.actions.server',
            # 'binding_type'          :  'action',
            # 'binding_view_types'    :  'list,form',
            # 'name'                  :   process.get('process_name').rstrip() + '_schedular',
            # 'model_id'              :   custom_model.id,
            # 'binding_model_id'      :   custom_model.id,
            # 'usage'                 :  'ir_cron',
            # 'state'                 :  'code',
            # 'model_name'            :   custom_model.model  ,   
            # 'code'                  :   scheduler_code
            # # 'code'                :  "env['o2b.process.modular'].action_test(model,record,records)"
            # })
            # server_action = server_action_new
            # server_action_id = request.env['ir.actions.server'].sudo().search([('name','=',record_process.process_name + '_schedular')], order = "id desc" , limit=1)

            schedular_status = False
            if status == 'true':
                schedular_status = True
            cron_name = record_process.process_name + '_schedular'
            _logger.info("chekcing cron name: %s", cron_name)
            server_cron = request.env['ir.cron'].sudo().search([('cron_name','=',cron_name)], order = "id desc" , limit=1)
             # _logger.info("menu from process name: %s ", menu_obj)
            if server_cron:
                server_cron.sudo().write({
                    'active':schedular_status
                    })
                 # print("write or not not, ", menu_obj.active)
            if not server_cron:
                 # _logger.info("menu object from archided status from process name: %s ", menu_obj)
                query = """
                    SELECT id
                    FROM ir_cron
                    WHERE cron_name->>'en_US' = %s
                    ORDER BY id DESC
                    LIMIT 1
                """
                request.env.cr.execute(query, (cron_name,))
                result = request.env.cr.fetchone()
                 # _logger.info("*********** database result:  %s", result)
                new_active_status='f'
                if status == 'true':
                    new_active_status='t'

                if result and result[0]:
                    menu = request.env['ir.cron'].sudo().browse(result[0])
                     # _logger.info("*********** menu object via browse methodo %s", menu_obj)
                    update_query = """
                    UPDATE ir_cron
                    SET active = %s
                    WHERE id = %s
                    """
                    request.env.cr.execute(update_query, (new_active_status, result[0]))
                    request.env.cr.commit()

            if end_point == '/process/schedular/status/change/active':
                _logger.info(" *** schedualr active api")
                return json.dumps( {"message":"schedular status changed to Active",'code':'200'})
            if end_point == '/process/schedular/status/change/inactive':
                _logger.info(" *** schedualr inactive api")
                return json.dumps( {"message":"schedular status changed to Inactive",'code':'200'})
        except Exception as e:
            _logger.info("creat module not run successfully. %s", e)
            return json.dumps(
                {'message' : 'Error : ' + str(e), 'code':'401'})
          


     # ***** create model and its field
    @http.route('/o2b/create/model', auth='none', type='json',methods=['POST'] , csrf=False , cors='*')
    def create_model_field(self, **kw):
        #  # print("current user di: ", request.env.user)
        try:
            json_data = json.loads(request.httprequest.data.decode('utf-8'))
            name = json_data.get('name')
            model_name = json_data.get('model')
            user_id = json_data.get('user_id')
            security_key = json_data.get('secret_key')
            model_fields = json_data.get('model_fields')
            _logger.info("Received data: in process module creation\n %s ", json_data)
     
            database_setup_key = request.env['ir.config_parameter'].sudo().search([('key','=', 'oflow_security_key')],limit=1)

            if not database_setup_key:
                return json.dumps({'message': 'Security key not found.','code':'400'})

             # print("database setup key: ",database_setup_key.key,database_setup_key.value)
            # code for gettng user license security key end here

            if security_key and  security_key !=database_setup_key.value:
                return json.dumps( {"message":"Security key is Invalid.",'code':'400'})

            if not model_name:
                return json.dumps({'message': 'Model name is not found.','code':'400'})


            if model_name and "x_" not in model_name:
                model_name = 'x_'+model_name.strip()
            print(" ****curremtn modle name : ", model_name)
            new_model = request.env['ir.model'].sudo().search([('model', '=',model_name)])
            if not new_model:
                new_model = request.env['ir.model'].with_user(2).sudo().create({
                    'model'             : model_name,
                    'name'              : name,
                    'is_mail_thread'    : True,
                    'is_mail_activity'  : True,
                    })

            _logger.info("*** model created or exits: %s ", new_model)
            # creating new model fields
            if model_fields:
                print(" model fielsd :: ", model_fields , " it type ", type(model_fields))
                for field_group in model_fields:
                    for item in field_group:
                        title = item.get('title')
                        create_field = item.get('technicalName')
                        field_type = item.get('type')
                        print(" *** first fied; ", item)
                        # self.create_field('x_reference_no',custom_model,'char','x_reference_no',None,None,"Record reference Numeer",None,None,None,None,None)
                        self.create_field(create_field,new_model,field_type,create_field,None,item,title,item.get('domain'),None,None,None,None)

            print(" *** current model is created or not:", new_model)
            # create access right
            self.initiate_access(new_model.model)
            # create access right
            # for mdm functionality start
            self.mdm_view_action(new_model)
            # for mdm functionality end 
            return json.dumps( {"message":"Model created successfully.",'code':'200','model_id':new_model.id,'model_name':new_model.model})
        except Exception as e:
            print("creat module not run successfully.", e)
            return json.dumps(
                {'message' : 'Error : ' + str(e),
                'code': '500'})


# *****model related api for configuration *****

    @http.route('/post/data/model', type='json', auth='none', methods=['POST'], csrf=False , cors='*')
    def global_create_record_in_model(self):
        body = json.loads(request.httprequest.data.decode('utf-8'))
        print(" body ", body)
        try:
            user = request.env['res.users'].with_user(1).browse(2) 
            timezone = user.tz
            print("Odoobot's Timezone:", timezone)
            _logger.info(" ** global_create_record_json_api")
            headers = {key: value for key, value in request.httprequest.headers.items()}
            security_key = headers.get('X-Security-Key')
            if security_key != 'o2b_technologies':
                return json.dumps( {"message":"Security key is Invalid.",'code':'401'})
            model_detail = body.get('modelDetail')
            fields = body.get('fields')
            # table_fields = body.get('tableFields')
            _logger.info(" ** model detail  : %s ", model_detail)
            _logger.info(" ** fields data  : %s ", fields)
            model_id = model_detail.get('model_id')
            if not model_id:
                return json.dumps( {"message":"Model Id can not be blank.",'code':'401'}) 

            if model_id:
                model_id = int(model_id)

            model = request.env['ir.model'].sudo().browse(model_id)

            proceed = False
            msg = ''
            udpate_dict = {}
            for key, value in fields.items():
                # check if x_name or name is duplicate then prevent creating name:
                if value:
                    search_name = request.env[model.model].with_user(1).sudo().search([('x_name','=', value)])
                    print(" fuck serach nam :", search_name)
                    if search_name.id:
                        proceed = False
                        _logger.info("Record is already exists with same name  %s ", value)
                        msg = "Record already exist with same name ."
                        response = json.dumps({"message":msg,'code':409})
                        return response
                else:
                    proceed = False
                    msg = " Name field can not be blank."
                    response = json.dumps({"message":msg,'code':409})
                    return response

                _logger.info(" ** current model field name :%s and value is : %s", key, value)
                field_existance = request.env['ir.model.fields'].sudo().search(['&',('name','=',key),('model_id','=',model_id)],limit=1)
                _logger.info(' ** database have field name %s and type : %s ',field_existance.name, field_existance.ttype)
                if field_existance:
                    proceed = True
                    if field_existance.ttype == 'boolean' and value:
                        udpate_dict[key] = True

                    if field_existance.ttype in ['char','html','text'] and value:
                        udpate_dict[key] = str(value)

                    if field_existance.ttype == 'float' and value:
                        udpate_dict[key] = float(value)

                    if field_existance.ttype == 'integer' and value.isdigit():
                        udpate_dict[key] = int(value)

                    if field_existance.ttype in ['date'] and value:
                        try:
                            udpate_dict[key] = datetime.datetime.strptime(value, '%d/%m/%Y').date()
                        except Exception as e:
                            udpate_dict[key] = datetime.date.today()

                    if field_existance.ttype in ['datetime'] and value:
                        try:
                            print("My current time: ", datetime.datetime.now())
                            print("User input value: ", value)
                            hour = 0
                            minute = 0
                            if timezone and timezone == 'Asia/Calcutta':
                                hour = 5
                                minute = 30
                            user_datetime = datetime.datetime.strptime(value, '%d/%m/%Y %H:%M')
                            adjusted_datetime = user_datetime - datetime.timedelta(hours = hour, minutes = minute)
                            udpate_dict[key] = adjusted_datetime.strftime('%Y-%m-%d %H:%M:%S')
                            print("Adjusted datetime: ", adjusted_datetime)
                        except Exception as e:
                            udpate_dict[key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            print("Error occurred: ", str(e))

                    if field_existance.ttype == 'json' and value:
                        udpate_dict[key] = json.dumps(value, ensure_ascii=False)

                    if field_existance.ttype == 'selection' and value:
                        selection_field = request.env['ir.model.fields.selection'].sudo().search([('field_id', '=',field_existance.id),('name', '=',value)],limit=1)
                        if selection_field:
                            udpate_dict[key] = str(selection_field.value)

                    if field_existance.ttype in ['many2one'] and value:
                        _logger.info("** handle many2one field %s ", value)
                        if field_existance.relation:
                            record_id = None
                            try:
                                if value.isdigit():
                                    print("The string contains only numbers.")
                                    record_search = request.env[field_existance.relation].sudo().search([('id','=', int(value))],limit=1)
                                    record_id= record_search.id
                                else:
                                    record_search = request.env[field_existance.relation].sudo().search([('name','=',value)],limit=1)
                                    record_id= record_search.id
                                if record_id:
                                    udpate_dict[key] = record_id
                            except Exception as e:
                                _logger.info("** error while handlin m2o field %s", str(e))
                        else:
                            _logger.info(" ** field relation model name is: %s", field_existance.relation)

                    if field_existance.ttype in ['many2many'] and value:
                        _logger.info("** handle many2many field %s ", value)
                        print("many2many man", field_existance.relation)
                        if field_existance.relation and field_existance.relation_table and field_existance.column1 and field_existance.column2:
                            record_id = None
                            try:
                                elements = value.split(',')
                                user_ids = []
                                for element in elements:
                                    element = element.strip()
                                    if element.isdigit():
                                        record_search = request.env[field_existance.relation].sudo().search([('id','=', int(element))],limit=1)
                                        if record_search:
                                            user_ids.append(int(record_search.id))
                                    else:
                                        record_search = request.env[field_existance.relation].sudo().search([('name', '=', element)], limit=1)
                                        if not record_search:
                                            record_search = request.env[field_existance.relation].sudo().create({'name':element})
                                        if record_search:
                                            user_ids.append(record_search.id)
                                udpate_dict[key] = [(6, 0, user_ids)]
                            except Exception as e:
                                _logger.info("** error while handlin m2m field %s", str(e))
                        else:
                            _logger.info(" ** field relation model name is: %s", field_existance.relation)
                  
                    if field_existance.ttype in ['binary','many2one_reference','one2many','reference'] and value:
                        _logger.info("** we will handle after proper request get")

            _logger.info("** updated new dictionary to be udpated %s",udpate_dict )
            if proceed:
                record = request.env[model.model].with_user(1).create(udpate_dict)
                response = json.dumps({"message":"Record created successfully with record id : " + str(record.id),'code': 201})
                return response
            else:
                response = json.dumps({"message":"Record  not created either duplicate name or blank name value : ", 'code': 409})
                return response

        except Exception as e:
            _logger.error(f"Error restarting service: {e}")
            response = json.dumps({"message":str(e),'code': 409})
            return response;



    @http.route(['/post/data/model/field/fetch','/post/data/model/field/delete','/post/data/model/field/upload'], type='json', auth='none', methods=['POST'], csrf=False , cors='*')
    def global_model_field_fetch(self):
        body = json.loads(request.httprequest.data.decode('utf-8'))
        try:
            _logger.info(" ** global_create_record_in mdm json_api")
            headers = {key: value for key, value in request.httprequest.headers.items()}
            security_key = headers.get('X-Security-Key')
            if security_key != 'o2b_technologies':
                return json.dumps( {"message":"Security key is Invalid.",'code':'401'})
            model_detail = body.get('modelDetail')
            fields = body.get('fields')
            # table_fields = body.get('tableFields')
            _logger.info(" ** model detail  : %s ", model_detail)
            _logger.info(" ** fields data  : %s ", fields)
            model_id = model_detail.get('model_id')
            record_id = model_detail.get('record_id')
            if not model_id:
                return json.dumps( {"message":"Model Id can not be blank.",'code':'401'}) 

            if model_id:
                model_id = int(model_id)

            model = request.env['ir.model'].sudo().browse(model_id)
            if not model:
                return json.dumps( {"message":"Model does not exist.",'code':'401'}) 

            end_point = request.httprequest.path
            if end_point == '/post/data/model/field/fetch':
                model_data = request.env[model.model].sudo().search([])
                models_data = []
                for model in model_data:
                    data = {
                        'id'        : model.id,
                        'model'     : model._name,
                        'name'      : model.x_name,
                    }
                    models_data.append(data)
                # Return JSON response
                return  {"message":models_data,'code':'201'}

            if end_point == '/post/data/model/field/delete':
                if not record_id:
                    return json.dumps( {"message":"record_id does not exist.",'code':'401'})

                delete_record = request.env[model.model].sudo().browse(int(record_id))

                if delete_record:
                    delete_record.unlink()

                return  {"message":"Record data deleted successfully",'code':'201'}


            if end_point == '/post/data/model/field/upload':
                # _logger.info(" *** in file uplaod data %s" ,body.get('fileData'))
                result = self.upload_xlsx_data(model,body.get('fileData'))
                if result and result == True:
                    return  {"message":"Record data uploaded successfully.",'code': 201}
                else:
                    return  {"message":"Record data uploaded unsuccessfully.Remove duplicate Record.",'code':401}

        except Exception as e:
            _logger.info(" *** errror occured in server api %s", str(e))
            return json.dumps( {"message": str(e),'code':'401'}) 

    # this method to resposible to spececied model bulk data upload
    def upload_xlsx_data(self,model,sheet_data):
        # print(" ** whole data to uplaod ", sheet_data)
        if not sheet_data:
            return False
        else:
            response = False
            udpate_dict = {}
            model_id = model.id
            for data in sheet_data:
                # print(" sheet data \n",data)
                for key, value in data.items():
                    search_name = request.env[model.model].with_user(1).sudo().search([('x_name','=', value)])
                    _logger.info(" ** duplicate name record: %s", search_name)
                    if search_name:
                        _logger.info("Record is already exists with same name  %s ", value)
                        response = json.dumps({"message":"Record already exist with same name ."})
                        return response
                    _logger.info(" ** current model field name :%s and value is : %s", key, value)
                    field_existance = request.env['ir.model.fields'].sudo().search(['&',('name','=',key),('model_id','=',model_id)],limit=1)
                    _logger.info(' ** database have field name %s and type : %s ',field_existance.name, field_existance.ttype)
                    if field_existance:
                        if field_existance.ttype == 'boolean' and value:
                            udpate_dict[key] = True

                        if field_existance.ttype in ['char','html','text'] and value:
                            udpate_dict[key] = str(value)

                        if field_existance.ttype == 'float' and value:
                            udpate_dict[key] = float(value)

                        if field_existance.ttype == 'integer' and value.isdigit():
                            udpate_dict[key] = int(value)

                        if field_existance.ttype in ['date'] and value:
                            try:
                                udpate_dict[key] = datetime.datetime.strptime(value, '%d/%m/%Y').date()
                            except Exception as e:
                                udpate_dict[key] = datetime.date.today()

                        if field_existance.ttype in ['datetime'] and value:
                            try:
                                print("My current time: ", datetime.datetime.now())
                                print("User input value: ", value)
                                hour = 0
                                minute = 0
                                # if timezone and timezone == 'Asia/Calcutta':
                                #     hour = 5
                                #     minute = 30
                                user_datetime = datetime.datetime.strptime(value, '%d/%m/%Y %H:%M')
                                adjusted_datetime = user_datetime - datetime.timedelta(hours = hour, minutes = minute)
                                udpate_dict[key] = adjusted_datetime.strftime('%Y-%m-%d %H:%M:%S')
                                print("Adjusted datetime: ", adjusted_datetime)
                            except Exception as e:
                                udpate_dict[key] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                print("Error occurred: ", str(e))

                        if field_existance.ttype == 'json' and value:
                            udpate_dict[key] = json.dumps(value, ensure_ascii=False)

                        if field_existance.ttype == 'selection' and value:
                            selection_field = request.env['ir.model.fields.selection'].sudo().search([('field_id', '=',field_existance.id),('name', '=',value)],limit=1)
                            if selection_field:
                                udpate_dict[key] = str(selection_field.value)

                        if field_existance.ttype in ['many2one'] and value:
                            _logger.info("** handle many2one field %s ", value)
                            if field_existance.relation:
                                record_id = None
                                try:
                                    if value.isdigit():
                                        print("The string contains only numbers.")
                                        record_search = request.env[field_existance.relation].sudo().search([('id','=', int(value))],limit=1)
                                        record_id= record_search.id
                                    else:
                                        record_search = request.env[field_existance.relation].sudo().search([('name','=',value)],limit=1)
                                        record_id= record_search.id
                                    if record_id:
                                        udpate_dict[key] = record_id
                                except Exception as e:
                                    _logger.info("** error while handlin m2o field %s", str(e))
                            else:
                                _logger.info(" ** field relation model name is: %s", field_existance.relation)

                        if field_existance.ttype in ['many2many'] and value:
                            _logger.info("** handle many2many field %s ", value)
                
                print(" before writing dictianly value: ", udpate_dict)
                record = request.env[model.model].with_user(1).sudo().create(udpate_dict)
                response = True
        return response
        
# *****model related api for configuration *****
