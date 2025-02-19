/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ListController } from "@web/views/list/list_controller";
import { useService } from "@web/core/utils/hooks";
import { _t } from '@web/core/l10n/translation';
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { WarningDialog } from "@web/core/errors/error_dialogs";

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

patch(ListController.prototype, "web.ListView", {
    setup() {

        // addons code today
        this.handleUserActivity = this.handleUserActivity.bind(this);
        this.checkIdleTimeout = this.checkIdleTimeout.bind(this);
        this.idleTime = 0;
        this.maxIdleTime = 15 * 60 * 1000;  
        console.log('setup method is called', this);
        onMounted(() => {
            window.addEventListener("mousemove", this.handleUserActivity);
            window.addEventListener("keypress", this.handleUserActivity);
            console.log(" ******* this.props.context.o2b_module", this.props.context.o2b_module)
            if (this.props.context.o2b_module == 'yes') {
                this.idleInterval = setInterval(this.checkIdleTimeout, 5000);
            }
            });
        // addons code today

        this._super.apply(this, arguments);
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.dialogService = useService("dialog");

        if (this.props.context.o2b_module == 'yes') {
            this.done = this.done.bind(this);
            this.done = this.done.bind(this);
            this._loggedInUserUpdate();
            this.loadSweetAlert(); 
         }

        // today addons
        onWillDestroy(() => {
            console.log(" automacticall call on depltyered: ")
            window.removeEventListener("mousemove", this.handleUserActivity);
            window.removeEventListener("keypress", this.handleUserActivity);
            clearInterval(this.idleInterval);
            });
        // today addons

    },

    // today addons
     handleUserActivity() {
             console.log("method called automactically when user press keyboard or move mouse.")
            },

    async checkIdleTimeout() {
        const recordCount = this.model.root.count;
        const records = this.model.root.records;
        const model = this.props.resModel;
        const node_id = this.props.context.o2b_node_id
        const uid = this.props.context.uid
        const o2b_module = this.props.context.o2b_module
        // const recordIds = records.map(record => record.data.id);
        const recordIds = records.map(record => record.data.id ?? record.resId);
        // console.log(" (**********records d", recordIds)
        // console.log(" ***** records",records)
        // console.log(" ***** recordCount",recordCount)
        // console.log(" ***** model",model)
        // console.log(" ***** o2b_module",o2b_module)
        
        const result = await this.orm.call('o2b.process.modular', "list_view_admin_data_process", [recordCount,recordIds,model,node_id,uid,o2b_module]);
    },
    // today addons

    async _loggedInUserUpdate() {
        let record_id = this.props.resId;
        const model = this.props.resModel;
        const node_id = this.props.context.o2b_node_id
        const uid = this.props.context.uid
        console.log(" we ain logged in user method: ",record_id)
        const result = await this.orm.call('o2b.process.modular', "logged_in_user", [model,record_id,uid,node_id]);
        console.log(" logged in user reponse rpc ", result)
        // console.log(" gggggggggggggggggggg", this)
        // console.log(" fffffffffffffffffff", this.model)
        const data = {
        logged_in_user: uid
        };
       this.model.notify("update", { data });
       this.render()
        }
    ,

    async loadSweetAlert() {
        // Dynamically load SweetAlert2 JavaScript and CSS
        if (!window.Swal) {
            const script = document.createElement("script");
            script.src = "https://cdn.jsdelivr.net/npm/sweetalert2@11";
            script.type = "text/javascript";
            document.head.appendChild(script);

            const link = document.createElement("link");
            link.rel = "stylesheet";
            link.href = "https://cdn.jsdelivr.net/npm/sweetalert2@11/dist/sweetalert2.min.css";
            document.head.appendChild(link);

            script.onload = () => {
                console.log("SweetAlert2 loaded.");
            };
        }
    },

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    },
    
    async processSelectedRecord(recordIds, nodeId, model, uid) {
        console.log("Processing selected records.");
        console.log("Record IDs:", recordIds);
        console.log("Node ID:", nodeId);
        console.log("Model:", model);
        console.log("User ID:", uid);

        try {
            const result = await this.orm.call('o2b.process.modular', "process_list_record", [recordIds, nodeId, model, uid]);
            console.log("Process result:", result);
            return result;
        } catch (error) {
            console.error("Error in processSelectedRecord:", error);
            throw error;
        }
    },
    
    async done() {
        console.log("Done button clicked in list view.");

        if (!window.Swal) {
            console.error("SweetAlert2 not loaded.");
            return;
        }

        // Retrieve the selected records
        const selectedRecords = this.model.root.selection;
        const selectedIds = selectedRecords.map(record => record.resId);
        const model = this.model.root.resModel;
        const node_id = this.props.context.o2b_node_id;
        const uid = this.props.context.uid;

        console.log("Model:", model);
        console.log("Selected IDs:", selectedIds);
        console.log("Node ID:", node_id);
        console.log("User ID:", uid);

        if (!selectedIds.length) {
            console.warn("No records selected.");
            Swal.fire({
                icon: "warning",
                text: "No Record selected. Please select at least one.",
            });
            const buttonDiv = document.getElementsByClassName("swal2-confirm")[0]
            buttonDiv.style.backgroundColor = "#007485";
            return;
        }

        try {
            const response = await this.processSelectedRecord(selectedIds, node_id, model, uid);
            console.log("Process response:", response);
            // odoo notification
            // this.showCenteredNotification("Records processed successfully!", "success");
            // this.notification.add("Records processed successfully.!", { type: "success" });
            // await this.sleep(3000);
            // window.location.reload();
            // odoo notification

           if (response) {
            const message = response[3] + response[4];
            this.dialogService.add(WarningDialog, {
                title: 'Warning',
                message: message,
                onClose: () => {
                    console.log("Dialog closed. Reloading...");
                    window.location.reload();
                },
            });
            await this.sleep(2000);
            window.location.reload();
        }

            // show complete log for all records
                // if(response)
                // {
                //     const message = response[3] + response[4]
                //     const { confirmed } = await this.dialogService.add(ConfirmationDialog, {
                //         body: _t(message),
                //         confirmLabel: _t("OK"),
                //         confirm: async () => {
                //             console.log("Record found and done code calling start here*** : ");
                //             try {
                //                 console.log("done method response****");
                //                 window.location.reload(); // Reload the page on confirmation
                //             } catch (error) {
                //                 console.error("Error in invokedBackend_done:", error);
                //                 this.notification.add(_t('An error occurred while processing your request.'), {
                //                     type: "danger",
                //                 });
                //             }
                //         },
                //     });

                // }
            // show complete log for all records
            
            // Swal.fire({
            //     icon: "success",
            //     title: "Done!",
            //     text: "Records processed successfully.",
            // }).then(async (result) => {
            //         const buttonDiv = document.getElementsByClassName("swal2-confirm")[0]
            //         buttonDiv.style.backgroundColor = "#007485";
            //     if (result.isConfirmed) {
            //         // If the user clicked "OK", proceed to reload the page
            //         // await this.sleep(1000);
            //         window.location.reload();
            //     }
            // });

        } catch (error) {
            Swal.fire({
                icon: "error",
                title: "Error!",
                text: "Failed to process records. Please try again.",
            });
            console.error("Error during processing:", error);
        }
    },

showCenteredNotification(message, type) {
        // Create a div element to hold the notification
        const notificationDiv = document.createElement('div');
        notificationDiv.className = 'centered-notification';
        notificationDiv.innerText = message;
        if (type === 'success') {
            notificationDiv.style.backgroundColor = '#4CAF50'; 
        } else if (type === 'error') {
            notificationDiv.style.backgroundColor = '#f44336'; 
        }
        document.body.appendChild(notificationDiv);
        setTimeout(() => {
            notificationDiv.remove();
        }, 3000);
    },

});
