/** @odoo-module **/

import { Component, useState, useRef } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

export class AbstractFormComponent extends Component {
    static template = "influence_gen_portal.AbstractFormComponentTemplate";
    static props = {
        submitUrl: { type: String },
        initialData: { type: Object, optional: true, default: () => ({}) },
        validationRules: { type: Object, optional: true, default: () => ({}) }, // e.g., {fieldName: [{type: 'required', message: '...'}, {type: 'email', message: '...'}]}
        successRedirectUrl: { type: String, optional: true },
        successMessage: { type: String, optional: true, default: () => _t("Form submitted successfully.") },
        slots: {
            default: {}, // For form fields
        },
    };

    setup() {
        this.rpcService = useService("rpc"); // Odoo's core RPC service
        this.notificationService = useService("notification");
        this.router = useService("router"); // Odoo's router service for navigation

        this.state = useState({
            formData: { ...this.props.initialData },
            formErrors: {}, // { fieldName: "Error message" }
            isSubmitting: false,
            globalError: null,
        });

        this.formRef = useRef("formElement"); // If form is the root of the template
    }

    _onInputChange(event) {
        const { name, value, type, checked, files } = event.target;
        let newValue;
        if (type === 'checkbox') {
            newValue = checked;
        } else if (type === 'file') {
            newValue = this.props.multipleFiles ? files : files[0]; // Handle single/multiple files if needed by this abstract component
        } else {
            newValue = value;
        }

        this.state.formData[name] = newValue;
        if (this.state.formErrors[name]) {
            this.state.formErrors[name] = null; // Clear error on input change
        }
        // Optional: validate on change
        // this._validateField(name, newValue);
    }

    _validateField(fieldName, value) {
        const rules = this.props.validationRules[fieldName];
        if (!rules) return true;

        for (const rule of rules) {
            if (rule.type === 'required' && (!value || (typeof value === 'string' && value.trim() === ''))) {
                this.state.formErrors[fieldName] = rule.message || _t("This field is required.");
                return false;
            }
            if (rule.type === 'email' && value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                this.state.formErrors[fieldName] = rule.message || _t("Invalid email format.");
                return false;
            }
            if (rule.type === 'minLength' && value && value.length < rule.value) {
                this.state.formErrors[fieldName] = rule.message || _t("Must be at least %s characters.", rule.value);
                return false;
            }
            // Add more validation rules as needed: regex, custom function, etc.
        }
        this.state.formErrors[fieldName] = null; // Clear error if all rules pass
        return true;
    }

    _validateForm() {
        let isValid = true;
        this.state.formErrors = {}; // Reset errors
        for (const fieldName in this.props.validationRules) {
            if (!this._validateField(fieldName, this.state.formData[fieldName])) {
                isValid = false;
            }
        }
        // HTML5 validation check (basic, use validationRules for better UX)
        if (this.formRef.el && !this.formRef.el.checkValidity()) {
            isValid = false;
            // Optionally iterate and populate formErrors based on native validity
            // This is complex as native messages are not easily customizable via JS here.
        }
        return isValid;
    }

    async _onSubmit(event) {
        event.preventDefault();
        if (this.state.isSubmitting) return;

        if (!this._validateForm()) {
            this.state.globalError = _t("Please correct the errors in the form.");
            // Focus on the first invalid field (optional enhancement)
            const firstErrorField = Object.keys(this.state.formErrors).find(key => this.state.formErrors[key]);
            if (firstErrorField && this.formRef.el && this.formRef.el.elements[firstErrorField]) {
                 this.formRef.el.elements[firstErrorField].focus();
            }
            return;
        }

        this.state.isSubmitting = true;
        this.state.globalError = null;

        try {
            // Use Odoo's rpcService which handles CSRF for POST to @http.route type='http' or type='json'
            // For file uploads, this abstract component might need to be more specialized or use a dedicated file uploader.
            // Assuming form data is serializable for a typical JSON/HTTP POST.
            const result = await this.rpcService(this.props.submitUrl, this.state.formData);

            // Assuming the backend returns a success message or specific data
            // If the controller handles redirection, this part might not be needed.
            if (result && result.error) { // Backend returned a business error in JSON
                this.state.globalError = result.error;
                if (result.errors) { // Field specific errors
                    this.state.formErrors = result.errors;
                }
            } else {
                this.notificationService.add(this.props.successMessage, { type: "success" });
                if (this.props.successRedirectUrl) {
                    this.router.navigate(this.props.successRedirectUrl);
                }
                this.trigger('form-submitted', { response: result });
                // Optionally reset form: this.state.formData = { ...this.props.initialData };
            }
        } catch (error) {
            _logger.error("Abstract Form Submission Error:", error);
            const errorMessage = error.message?.data?.message || error.message || _t("An unexpected error occurred.");
            this.state.globalError = errorMessage;
            this.notificationService.add(errorMessage, { type: "danger" });
            if (error.message?.data?.errors) {
                this.state.formErrors = error.message.data.errors;
            }
        } finally {
            this.state.isSubmitting = false;
        }
    }
}