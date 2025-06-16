/** @odoo-module **/

import { registry } from "@web/core/registry";
import { rpcService } from "@web/core/network/rpc_service";
import { notificationService } from "@web/core/notifications/notification_service";
import { _t } from "@web/core/l10n/translation";

// This is a simplified way to make services available globally if needed by non-OWL JS,
// or to be consumed by OWL components via `this.env.services`.
// For OWL components, it's better to add them to the service registry.

const portalService = {
    /**
     * Makes an RPC call to an Odoo backend controller.
     * @param {string} route The backend route.
     * @param {Object} params Parameters for the call.
     * @param {string} method HTTP method (usually 'call' for Odoo RPC, or 'POST'/'GET' for http type routes).
     * @returns {Promise<any>}
     */
    async rpc(route, params = {}, method = 'call') {
        // Assuming rpcService is set up in the environment.
        // If this service is used outside OWL, direct import and use of ajax.rpc might be needed.
        // However, Odoo 16+ encourages use of services.
        // This is a placeholder for how rpcService would be accessed if this was an OWL service.
        // For a simple JS object service, you might need to instantiate rpcService or use legacy ajax.rpc
        
        // Using a direct reference to ajax if rpcService is not easily available in this context
        // This pattern is more common for legacy JS or utilities outside component context
        const { jsonrpc } = require('web.ajax'); // Legacy way
        if (method && method.toLowerCase() === 'post' && route.startsWith('/my/')) { // Assuming JSON controller
             return jsonrpc(route, params); // Odoo 18, type='json' routes are direct JSON-RPC
        }
        // For type='http' routes, especially if they return HTML or redirects,
        // it's usually handled by form submissions or window.location, not direct RPC here.
        // This RPC is mostly for JSON endpoints.
        return jsonrpc(route, params);
    },

    /**
     * Displays a UI notification.
     * @param {string} message The message to display.
     * @param {string} type 'info', 'success', 'warning', 'danger'.
     * @param {boolean} sticky Whether the notification should be sticky.
     */
    notify(message, type = 'info', sticky = false, title = '') {
        // Similar to RPC, accessing notificationService.
        // For non-OWL JS, this might need direct access to Odoo's notification mechanisms.
        const notification = registry.category("services").get("notification");
        const options = {
            type: type,
            sticky: sticky,
            title: title || (type === 'success' ? _t("Success") : type === 'danger' ? _t("Error") : type === 'warning' ? _t("Warning") : _t("Information"))
        };
        notification.add(message, options);
    }
};

// Registering the service so it can be used in OWL components via this.env.services.portal
registry.category("services").add("influence_gen_portal.portal_service", {
    dependencies: ["rpc", "notification"],
    start(env, { rpc, notification }) {
        return {
            async rpc(route, params = {}, httpMethod = 'POST') {
                 // For JSON controllers (type='json')
                if (route.startsWith('/my/ai/')) { // Example
                    return rpc(route, params);
                }
                // For other custom calls, or if you have specific http type routes that return JSON
                // This might need more specific handling based on Odoo version and route type
                // Typically, for 'http' routes that render templates, you don't call them via JS RPC
                // but navigate or submit forms to them.
                console.warn(`Attempting RPC to non-standard JSON route: ${route}. Ensure it's a JSON endpoint.`);
                return rpc(route, params); // Fallback to Odoo's default RPC
            },
            notify(message, type = 'info', sticky = false, title = '') {
                 const options = {
                    type: type,
                    sticky: sticky,
                    title: title || (type === 'success' ? _t("Success") : type === 'danger' ? _t("Error") : type === 'warning' ? _t("Warning") : _t("Information"))
                };
                notification.add(message, options);
            }
        };
    }
});


// Exporting for potential use in non-OWL JS if absolutely necessary, but prefer service registry.
export default portalService;