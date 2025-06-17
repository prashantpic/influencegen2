/** @odoo-module **/

import { Component } from "@odoo/owl";

/**
 * LoadingIndicator Component
 *
 * Displays a visual loading indicator (e.g., spinner).
 * REQ-UIUX-007, REQ-UIUX-001
 */
export class LoadingIndicator extends Component {
    static template = "InfluenceGen.Odoo.Shared.UI.Components.LoadingIndicator";

    /**
     * Props for the LoadingIndicator component.
     * @type {Object}
     * @property {String} [size='md'] - Size of the indicator ('sm', 'md', 'lg').
     * @property {String} [message] - Text message to display below the spinner.
     * @property {Boolean} [isFullScreen=false] - If true, the indicator covers the full parent relatively positioned element.
     */
    static props = {
        size: { type: String, optional: true, validate: s => ['sm', 'md', 'lg'].includes(s) },
        message: { type: String, optional: true },
        isFullScreen: { type: Boolean, optional: true },
    };

    static defaultProps = {
        size: 'md',
        isFullScreen: false,
    };

    /**
     * Setup method for the component.
     */
    setup() {
        super.setup();
    }

    /**
     * Computed property to return CSS classes for the indicator.
     * @returns {String} CSS classes.
     */
    get indicatorClass() {
        const classes = ['o_loading_indicator'];
        if (this.props.size) {
            classes.push(`o_loading_indicator--${this.props.size}`);
        }
        if (this.props.isFullScreen) {
            classes.push('o_loading_indicator--fullscreen');
        }
        return classes.join(' ');
    }
}