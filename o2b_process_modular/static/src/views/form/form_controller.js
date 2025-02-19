/** @odoo-module **/
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { _t } from '@web/core/l10n/translation';
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { useService } from "@web/core/utils/hooks";
import { WarningDialog } from "@web/core/errors/error_dialogs";

// import { Component, onWillStart } from "@odoo/owl";
const {
    onError,
    onMounted,
    onWillDestroy,
    useExternalListener,
    useRef,
    useState,
    useSubEnv,
    reactive,
    } = owl;

// Define global variable outside of any methods or lifecycle hooks
let globalVariable = reactive({
    value: true
});

let o2bModule = reactive({
    value: false
});

patch(FormController.prototype, 'web.FormView', {
    setup() {
        this.handleUserActivity = this.handleUserActivity.bind(this);
        this.checkIdleTimeout = this.checkIdleTimeout.bind(this);
        this.idleTime = 0;
        this.maxIdleTime = 15 * 60 * 1000;  
        // this.maxIdleTime = 5 * 1000;  
        console.log('setup method is called', this);
         // lock messge test code 
        onMounted(() => {
            window.addEventListener("mousemove", this.handleUserActivity);
            window.addEventListener("keypress", this.handleUserActivity);
            this.idleInterval = setInterval(this.checkIdleTimeout, 1000);
            });
        // lock messge test code 
        this._super.apply(this, arguments);
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.dialogService = useService("dialog");
        globalVariable.value = true

        if (this.props.context.o2b_module == 'yes') {
            this.done = this.done.bind(this);
            console.log(" ********stuck we have this.props :  ", this.props);
            console.log(" ********stuck we have :  this.model", this.model);
            console.log(" ********stuck we have :  this.model.root", this.props.resModel);
            // uncomment this method to apply lock and unlock
            this._loggedInUserUpdate();
            this._callRpcOnFormLoad();
            // this.release_record = this.release_record.bind(this);
            }

       
        onWillDestroy(() => {
            window.removeEventListener("mousemove", this.handleUserActivity);
            window.removeEventListener("keypress", this.handleUserActivity);
            clearInterval(this.idleInterval);
            console.log("We are in the destroyed method", this.props.context.o2b_module);
            console.log("Destroyed record ID for release:", this.props.resId);
            console.log(" **** globalVariable value : ", globalVariable.value)
            if(globalVariable.value && this.props.context.o2b_module == 'yes') {
                const res_release_lock = this.orm.call('o2b.process.modular', "lock_release", [
                    this.props.resModel,
                    this.props.resId,
                    this.props.context.uid
                ]);
                console.log("Destroyed record ID for release:1ee3", this.props.resId);
                console.log(" reponser from release record method ", res_release_lock);

                let showRecord = ""
                if(this.props.resId)
                {
                    showRecord = String(this.props.resId)
                }

                const msg = `System released the record ID ${showRecord} successfully.`;
                this.notification.add(msg, { type: "success" });
                globalVariable.value = true
                }
        });
    },


    handleUserActivity() {
             console.log("handleUserActivity")
            this.idleTime = 0;
            },

    async checkIdleTimeout() {
            console.log(" ** checkIdleTimeout ",this.props.context.o2b_module);
            if(this.props.context.o2b_module =='yes'){
            this.idleTime += 1000;
            if (this.idleTime >= this.maxIdleTime) {
            clearInterval(this.idleInterval);
            // try {
            // await this.orm.call('/web/session/destroy');
            // } catch (error) {
            // console.log("Error during session destroy:", error);
            // }
            // location.reload();
            this.notification.add(_t("You have been logged out due to inactivity."), { type: "danger" });
            // 
            const message = "You have been logged out due to inactivity."
            const { confirmed } = await this.dialogService.add(ConfirmationDialog, {
                body: _t(message),
                confirmLabel: _t("Confirm"),
                confirm: async () => {
                    window.history.back();
                    await this.sleep(2000);
                    window.location.href = '/web/session/logout';
                }
            });
            // window.location.href = '/web/login';
            }
            }
        }
            ,


    async _loggedInUserUpdate() {
        let record_id = this.props.resId;
        const model = this.props.resModel;
        const node_id = this.props.context.o2b_node_id;
        const uid = this.props.context.uid;
        console.log(" we are in logged in user method: ", record_id);
        const result = await this.orm.call('o2b.process.modular', "logged_in_user", [model, record_id, uid, node_id]);
        console.log("logged in user reponse rpc ", result);
        const data = {
            logged_in_user: uid
        };
        this.model.notify("update", { data });
        this.render();
    },

    async _callRpcOnFormLoad() {
        let record_id = this.props.resId;
        const model = this.props.resModel;
        const node_id = this.props.context.o2b_node_id
        const uid = this.props.context.uid
        const call_save_method = await $('.o_form_button_save').click();

        if (record_id === undefined || !record_id) {
            console.log("Record ID is missing.");
            // const call_save_method = await $('.o_form_button_save').click();
            await this.sleep(1000); 
            console.log("Record not found: ", record_id);
            const url = window.location.href; 
            console.log("Record url: ", url);
            const regex = /[?&]id=(\d+)/;
            const match = url.match(regex);
            record_id = match ? match[1] : null;
            // window.location.reload()
            }

            if(record_id)
            {
            try{
                // console.log(" ** going to invoce lock_record model:",model )
                // console.log(" ** going to invoce lock_record  recordid:",record_id )
                // console.log(" ** going to invoce lock_record uid:",uid )
                // console.log(" ** going to invoce lock_record node_id:",node_id )
                const result = await this.orm.call('o2b.process.modular', "lock_record", [model,record_id,uid,node_id]);
                console.log('RPC call result:', result);
                if(result)
                {
                if(result[0] == 'USER_QUEUE')
                {
                    this.notification.add("Current record in in your Queue. Please fill and release the record.", { type: "success" });
                    // const { confirmed } = await this.dialogService.add(ConfirmationDialog, {
                    // body: _t("Are you sure, you want to submit the record ?"),
                    // confirmLabel: _t("Confirm"),
                    // cancelLabel: _t("Cancel"),
                    // confirm: async () => {
                    // console.log("Record found and done code calling start here*** : ", record_id);
                    // try {
                    // let res = await this.invokedBackend_done(record_id);
                    // console.log("done method response****", res);
                    // // window.history.back()

                    // // Show success notification
                    // // this.notification.add(yes, {
                    // //     type: "success",
                    // // });
                    // } catch (error) {
                    // console.error("Error in invokedBackend_done:", error);
                    // this.notification.add(_t('An error occurred while processing your request.'), {
                    // type: "danger",
                    // });
                    // }
                    // },
                    // cancel: () => {
                    // console.log('User abrupt the current process.');
                    // this.notification.add(cancel, {
                    // type: "danger",
                    // });
                    // },
                    // });
                }
                if(result[0] == 'OTHER_QUEUE')
                {
                    // this.notification.add("Current record is locked by Another User.Please wait to release.!", { type: "danger" });
                    globalVariable.value = false;
                    const { confirmed } = await this.dialogService.add(ConfirmationDialog, {
                    body: _t("The selected record is currently pending in another user's queue and cannot be processed at this time .\n Pending on user: " + result[1]),
                    confirmLabel: _t("Confirm"),
                    cancelLabel: _t("Cancel"),
                    confirm: async () => {
                        window.history.back();
                    },
                    cancel: () => {
                            console.log('User abrupt the current process.');
                            this.notification.add('Please Choose Another records.', {
                            type: "danger",
                            });
                            window.history.back();
                        },
                    });
                }
                if(result[0] == 'FINAL')
                {
                    this.notification.add("Record is locked by You.!", { type: "warning" });
                }
            }
            } 
            catch (error) 
                {
                console.error("RPC call failed:", error);
                // this.notification.add("Failed to call RPC method", { type: "danger" });
            }
            }
    },

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },

    async invokedO2bFieldCheck(recordId) {
        const record = this.model.root;
        const model = this.model.root.resModel;
        let record_id = this.props.resId;
        console.log(" ** we are in required field check method:",this.props.context)
        console.log(" ** we are in required field check method:",this.props.context.o2b_node_id)
        console.log("pass record Id: **** ", recordId)
        console.log("this record: **** ", record)
        console.log("this model : **** ", model)
        console.log("this record id : **** ", record_id)
        console.log("try to change state:", this,recordId)
        console.log("============__fit his.model.root.resModel_fields", this.props.fields)
        if(!record_id)
        {
            record_id = recordId
        }
        const obj = this.props.fields;
        let response;
        let node_id = this.props.context.o2b_node_id
        try 
        {
            const action = await this.orm.call('o2b.process.modular', "required_field_check", [model,record_id,obj,node_id]);
            console.log(" required field check value", action)
            if(action)
            {   
                response = action
            }
            else
            {   
            Swal.fire({
            position: "top-center",
            text: "Internal server error.",
            showConfirmButton: true,
            // timer: 1500,
            background: '#f8d7da',  
            color: '#721c24',  
            });
            }
        } catch (error) {
            console.log("error while calling required_field_check backend method:", error);
        }
        if(response === undefined)
        {
            console.log("if reponse is undefined whill calling required_field_check ", response)
        }
        return response ? response : null;
    },


    async invokedBackend_done(recordId) {
        const record = this.model.root;
        const model = this.model.root.resModel;
        let record_id = this.props.resId;
        // console.log("pass record Id: **** ", recordId)
        // console.log("this record: **** ", record)
        // console.log("this model : **** ", model)
        // console.log("this record id : **** ", record_id)
        // console.log("try to change state:", this,recordId)
        // console.log("============__fithis.model.root.resModel_fields", this.props.fields)
        if(!record_id)
        {
            record_id = recordId
        }
        const obj = this.props.fields;
        let response;
        let universal_success_message = 'Record has been submitted successfully.'
        let universal_error_message = 'Record has been not submitted.'
        // console.log('Number of properties:', Object.entries(obj));
        for (let key in  obj) {
        if (obj.hasOwnProperty(key)) { 
        // console.log('Key:', key);
        // console.log('Value:', obj[key]); 
        // console.log('Sub-property name:', obj[key].name);
        } }
        try {
        const node_id = this.props.context.o2b_node_id
        const uid = this.props.context.uid
        const action = await this.orm.call('o2b.process.modular', "decision_action", [model,record_id,obj,node_id,uid]);
        // console.log(" decision_action", action)
        if(action)
        {   
            response = action
            // if(action[0] == 'condtional')
            // {    console.log(",condtional", action[1], action[0], action[2])
            //     // alert("Stage changed according  to engine rule.")
            //     Swal.fire({
            //     position: "top-center",
            //     // text: "Stage changed according  to engine rule." + action[2],
            //     text: universal_success_message,
            //     showConfirmButton: true,
            //     // // timer: 1500,
            //     // // background: '#ACECBB',   
            //     // // color: '#112C0E',  
            //     });
            // }
            // if(action[0] == 'normal')
            // {  console.log(",normal", action[1], action[0], action[2])
            //     // alert("Stage moved on to next stage.")
            //     Swal.fire({
              
            //     position: "top-center",
            //     // text: "Stage moved on to next stage." + action[2],
            //     text: universal_success_message,
            //     showConfirmButton: true,
            //     // timer: 1500,
            //     // background: '#ACECBB',   
            //     // color: '#112C0E',  
            //     });
            // }
            // if(action[0] == 'internal')
            // {
            //     alert("Something went wrong while executing the transaction.")
            // }
            // if(action[0] == 'notfound')
            // {
            //      console.log(",notfound", action[1], action[0], action[2])
            //     // alert("No suitable decision rule found for this record.")
            //     Swal.fire({
            //     position: "top-center",
            //     // text: "No suitable decision rule found for this record.",
            //     text: universal_success_message,
            //     showConfirmButton: true,
            //     // timer: 1500,
            //     background: '#f8d7da',  
            //     color: '#721c24',  
            //     });
            // }

            // if(action[0] == 'decision')
            // {
            //     console.log(",decision", action[1], action[0], action[2])
            //     // alert("No suitable decision rule found for this record.")
            //     Swal.fire({
            //     position: "top-center",
            //     // text: "Pending Record on Decision Stage: " + action[2],
            //     text: universal_success_message,
            //     showConfirmButton: true,
            //     // timer: 1500,
            //     background: '#f8d7da',  
            //     color: '#721c24',  
            //     });
            // }
            
            if(action[1])
                 console.log("href", action[1], action[0], action[2])
            {
                window.location.href = action[1];
                // window.history.back()

            }
        }
        else
            {   
            // alert("Internal server error.")
            Swal.fire({
                position: "top-center",
                text: "Internal server error.",
                showConfirmButton: true,
                // timer: 1500,
                background: '#f8d7da',  
                color: '#721c24',  
                });
        }
    } catch (error) {
        console.log("Failed to update state:", error);
    }
        console.log("final response done method: ", response)
        if(response === undefined)
        {
            console.log("if reponse is undefined: ", response)
            // Swal.fire({
            // position: "top-center",
            // text: "Internal server error.",
            // // text: "Record has been already pushed on last stage.",
            // showConfirmButton: true,
            // // timer: 1500,
            // // background: '#f8d7da',  
            // // color: '#721c24',  
            // });
        }
        return response ? response : null;
    },

    async done() {
      // for sweet alert start here 
        var script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11';
        script.type = 'text/javascript';
        document.head.appendChild(script);
        script.onload = function () {
        console.log('SweetAlert2 loaded.');
        };
    // end sweet alert cnd link
        // console.log("this***",$('.o_form_button_save'));
        const call_save_method = await $('.o_form_button_save').click();
        // console.log("Start   ",call_save_method);
        await this.sleep(1000); 
        // console.log("2 seconds later");
        let yes = _t("User clicked the confirm button.");
        let cancel = _t("User abrupt the current prcess.");
        const record = this.model.root;
        const model = this.model.root.resModel;
        let record_id = this.props.resId;
        console.log("this**** :", this);
        console.log("model**** :", model);
        console.log("this.props :", this.props);
        console.log("we have current record Id ", record_id);
        if (record_id === undefined || !record_id) {   
            console.log("Record not found: ", record_id);
            const url = window.location.href; 
            console.log("Record url: ", url);
            const regex = /[?&]id=(\d+)/;
            const match = url.match(regex);
            record_id = match ? match[1] : null;
        }
        console.log("Record found: 0000---", record_id);
        if (record_id){
            
            // start calling required field check
            let field_check_res = await this.invokedO2bFieldCheck(record_id);
            console.log(" **field_check_res ",field_check_res)
            if(field_check_res[0] == 'Failed')
            {   
                // let msg = 'Please fill mandatory field. ( ' + field_check_res[2] + ' )'
                let msg = '"' + field_check_res[2] + '" field is required on from.'
                if(field_check_res[3] ==='TODO')
                {
                    console.log(" *** we are in todo", field_check_res[2])
                    msg = '"' + field_check_res[2] + '" field is required on Todos form.'
                }
                if(field_check_res[3] === 'DOCUMENT')
                {   console.log(" *** we are in document", field_check_res[2])
                    msg = '"' + field_check_res[2] + '" field is required on Document form.'
                }
              
                Swal.fire({
                icon: "error",
                text: msg});
                const buttonDiv = document.getElementsByClassName("swal2-confirm")[0]
                buttonDiv.style.backgroundColor = "#007485";
                
                // odoo base notification
                // const { confirmed } = await this.dialogService.add(ConfirmationDialog, {
                // body: _t(msg),
                // confirmLabel: _t("Confirm"),
                // cancelLabel: _t("Cancel"),
                // confirm: async () => { // Mark the callback as async
                //         console.log("do if confirm button press  ", record_id);
                //         console.log("Record found and done code calling start here*** : ", record_id);
                //     },
                // cancel: () => {
                //     console.log('User abrupt the current process.');
                //     this.notification.add(cancel, {
                //     type: "danger",
                //     });
                //     },
                //     });
            }
            else
            {
                const { confirmed } = await this.dialogService.add(ConfirmationDialog, {
                body: _t("Are you sure, you want to submit the record ?"),
                confirmLabel: _t("Confirm"),
                cancelLabel: _t("Cancel"),
                confirm: async () => {
                console.log("Record found and done code calling start here*** : ", record_id);
                try {
                    let res = await this.invokedBackend_done(record_id);
                    console.log("done method response****", res);
                    // window.history.back()

                    // Show success notification
                    // this.notification.add(yes, {
                    //     type: "success",
                    // });
                } catch (error) {
                    console.error("Error in invokedBackend_done:", error);
                    this.notification.add(_t('An error occurred while processing your request.'), {
                        type: "danger",
                    });
                }
                },
                cancel: () => {
                    console.log('User abrupt the current process.');
                    this.notification.add(cancel, {
                    type: "danger",
                    });
                },
                });
            }
        }
        else
        {   
            // this.notification.add("Record ID is not found", {
            // type: "danger",
            // });
            return;
        }
        return; 
    }
});
