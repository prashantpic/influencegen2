/** @odoo-module **/

import { Component, useState, onWillStart, onMounted, useRef } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";

const portalService = registry.category("services").get("influence_gen_portal.portal_service", { optional: true }) || {
    // Fallback if service not fully loaded or in test env
    async rpc(route, params) { console.warn('portal_service.rpc fallback used'); return ajax.rpc(route, params); },
    notify(message, type = 'info', sticky = false) { console.warn(`portal_service.notify fallback: ${type} - ${message}`); }
};


export class AbstractFormComponent extends Component {
    static template = "influence_gen_portal.AbstractFormComponentTemplate"; // To be defined in XML
    static props = {
        submitUrl: { type: String, optional: false },
        initialData: { type: Object, optional: true, default: {} },
        validationRules: { type: Object, optional: true, default: {} }, // e.g., { fieldName: [{ type: 'required' }, { type: 'email' }, {type: 'minLength', value: 5}] }
        successRedirectUrl: { type: String, optional: true },
        successMessage: { type: String, optional: true, default: _t("Form submitted successfully!") },
        errorMessage: { type: String, optional: true, default: _t("An error occurred. Please try again.") },
        slots: { type: Object, optional: true },
        formRef: { type: Object, optional: true }, // ref to pass to the form element
    };

    setup() {
        this.state = useState({
            formData: { ...this.props.initialData },
            formErrors: {}, // { fieldName: "Error message" }
            isSubmitting: false,
            globalError: "",
        });

        if (this.props.formRef) {
            this.form = useRef(this.props.formRef.name);
        } else {
            this.form = useRef("abstractForm");
        }


        onWillStart(async () => {
            // Initialization logic if needed
        });

        onMounted(() => {
            // Post-render logic, e.g., focusing first field
        });
    }

    _onInputChange(event) {
        const { name, value, type, checked } = event.target;
        this.state.formData[name] = type === 'checkbox' ? checked : value;
        if (this.state.formErrors[name]) {
            delete this.state.formErrors[name]; // Clear error on input change
        }
        this.state.globalError = ""; // Clear global error on input change
        // Optionally, trigger field validation on blur or change
        // this._validateField(name, this.state.formData[name]);
    }

    _validateField(fieldName, value) {
        const rules = this.props.validationRules[fieldName] || [];
        for (const rule of rules) {
            if (rule.type === 'required' && !value && value !== false) { // Ensure boolean false is not considered empty for checkboxes
                this.state.formErrors[fieldName] = rule.message || _t("This field is required.");
                return false;
            }
            if (rule.type === 'email') {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (value && !emailRegex.test(value)) {
                    this.state.formErrors[fieldName] = rule.message || _t("Invalid email address.");
                    return false;
                }
            }
            if (rule.type === 'minLength' && value && value.length < rule.value) {
                this.state.formErrors[fieldName] = rule.message || _t("Must be at least %s characters.", rule.value);
                return false;
            }
            if (rule.type === 'maxLength' && value && value.length > rule.value) {
                this.state.formErrors[fieldName] = rule.message || _t("Cannot exceed %s characters.", rule.value);
                return false;
            }
            if (rule.type === 'pattern' && value && !new RegExp(rule.value).test(value)) {
                 this.state.formErrors[fieldName] = rule.message || _t("Invalid format.");
                 return false;
            }
            if (rule.type === 'custom' && typeof rule.validator === 'function') {
                const customError = rule.validator(value, this.state.formData);
                if (customError) {
                    this.state.formErrors[fieldName] = customError;
                    return false;
                }
            }
        }
        delete this.state.formErrors[fieldName];
        return true;
    }

    _validateForm() {
        this.state.formErrors = {}; // Reset errors
        let isValid = true;
        for (const fieldName in this.props.validationRules) {
            if (!this._validateField(fieldName, this.state.formData[fieldName])) {
                isValid = false;
            }
        }
        return isValid;
    }

    async _onSubmit(event) {
        event.preventDefault();
        this.state.isSubmitting = true;
        this.state.globalError = "";
        this.state.formErrors = {};

        if (!this._validateForm()) {
            this.state.isSubmitting = false;
            // Optionally focus the first invalid field
            const firstErrorField = Object.keys(this.state.formErrors)[0];
            if (firstErrorField && this.form.el) {
                const fieldElement = this.form.el.querySelector(`[name="${firstErrorField}"]`);
                if (fieldElement) fieldElement.focus();
            }
            return;
        }

        try {
            // Odoo's RPC service automatically handles CSRF if controller has csrf=True
            const result = await portalService.rpc(this.props.submitUrl, this.state.formData, 'POST'); // Assuming POST, adjust if needed

            if (result && result.error) { // Server-side validation errors or operational errors
                if (result.fields_errors) { // Odoo-style field errors
                    for (const err of result.fields_errors) {
                         this.state.formErrors[err.field_name] = err.message;
                    }
                } else {
                    this.state.globalError = result.error.message || result.error.data?.message || this.props.errorMessage;
                }
                portalService.notify(this.state.globalError || _t("Please correct the errors below."), 'danger');

            } else if (result && result.redirect_url) { // Server explicitly asks for redirect
                 window.location.href = result.redirect_url;
            }
            else { // Success
                portalService.notify(this.props.successMessage, 'success');
                this.env.bus.trigger('form-submitted', { component: this, response: result });

                if (this.props.successRedirectUrl) {
                    window.location.href = this.props.successRedirectUrl;
                } else if (result && result.message) { // Display server success message if no redirect
                    this.state.globalError = ""; // Clear errors
                }
                // Optionally reset form: this.state.formData = { ...this.props.initialData };
            }
        } catch (error) {
            console.error("Form submission error:", error);
            this.state.globalError = error.data?.message || error.message || this.props.errorMessage;
            portalService.notify(this.state.globalError, 'danger');
        } finally {
            this.state.isSubmitting = false;
        }
    }
}

registry.category("public_components").add("influence_gen_portal.AbstractFormComponent", AbstractFormComponent);