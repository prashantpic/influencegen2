/** @odoo-module **/

import { registry } from "@web/core/registry";
import { RPCError } from "@web/core/network/rpc_service"; // For error type checking
import { _t } from "@web/core/l10n/translation";

const portalService = {
    dependencies: ["rpc", "notification", "router"], // Declare dependencies on core Odoo services

    start(env, { rpc, notification, router }) {
        /**
         * Wrapper for Odoo's core RPC service, tailored for portal interactions.
         * @param {string} route - The Odoo route (e.g., controller path).
         * @param {Object} params - Parameters for the RPC call. For POST, these are the body. For GET, they form the query string.
         * @param {Object} [options={}] - Additional options for the RPC call.
         * @param {string} [options.method='POST'] - HTTP method, typically 'POST' for JSON RPCs. 'GET' can be used for fetching.
         * @returns {Promise<any>}
         */
        async function portalRpc(route, params = {}, options = {}) {
            const method = options.method || 'call'; // 'call' is generic for odoo rpc service, translates to POST for json routes
            try {
                // Odoo's rpc service automatically handles CSRF for POST type json/http routes.
                // It also stringifies JSON body for POST and constructs query for GET.
                const result = await rpc(route, params, options); // Pass options if any (like silent: true)
                return result;
            } catch (error) {
                _logger.error(`Portal RPC Error to ${route}:`, error);
                let userMessage = _t("An error occurred while processing your request.");
                if (error instanceof RPCError) { // Check if it's an Odoo specific RPCError
                    if (error.data && error.data.message) { // Odoo UserError or specific error message
                        userMessage = error.data.message;
                    } else if (error.message) { // Generic RPC error message
                        userMessage = error.message;
                    }
                } else if (error.message) { // Standard JS error
                    userMessage = error.message;
                }
                // Optionally, display a notification here for all RPC errors, or let caller handle
                // notify(userMessage, 'danger');
                throw { // Re-throw a structured error for components to handle
                    type: 'rpc_error',
                    message: userMessage,
                    originalError: error,
                };
            }
        }

        /**
         * Displays a UI notification.
         * @param {string} message - The message to display.
         * @param {Object} [options={}] - Options for the notification.
         * @param {string} [options.type='info'] - Type: 'info', 'success', 'warning', 'danger'.
         * @param {boolean} [options.sticky=false] - If true, notification requires manual dismissal.
         * @param {string} [options.title] - Optional title for the notification.
         * @param {Function} [options.onClose] - Callback when notification is closed.
         */
        function notify(message, options = {}) {
            notification.add(message, {
                type: options.type || 'info',
                sticky: options.sticky || false,
                title: options.title,
                onClose: options.onClose,
                className: options.className, // Custom class for styling
            });
        }

        /**
         * Navigates to a different portal route.
         * @param {string} route - The portal route to navigate to (e.g., '/my/dashboard').
         * @param {Object} [options={}] - Navigation options.
         */
        function navigate(route, options = {}) {
            router.navigate(route, options);
        }

        return {
            rpc: portalRpc,
            notify,
            navigate,
            // Expose env for components that might need it (e.g., for _t directly if not using hooks)
            // Note: Components should prefer useService or hooks to access env.
            // getEnv: () => env,
        };
    },
};

registry.category("services").add("influence_gen_portal.portal_service", portalService);

export default portalService; // For potential direct import if needed, though registry is preferred.