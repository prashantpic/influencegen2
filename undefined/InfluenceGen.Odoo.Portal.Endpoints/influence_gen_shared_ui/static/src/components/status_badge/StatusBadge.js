/** @odoo-module **/

import { Component } from "@odoo/owl";

/**
 * StatusBadge Component
 *
 * Displays a status with configurable text and type-based styling.
 * REQ-UIUX-001
 */
export class StatusBadge extends Component {
    static template = "InfluenceGen.Odoo.Shared.UI.Components.StatusBadge";

    /**
     * Props for the StatusBadge component.
     * @type {Object}
     * @property {String} statusText - The text to display in the badge.
     * @property {String} [statusType='default'] - Type of status, influencing color ('info', 'success', 'warning', 'danger', 'neutral', 'primary', 'secondary', 'default').
     * @property {Boolean} [isPill=false] - If true, renders as a pill-shaped badge.
     */
    static props = {
        statusText: { type: String, required: true },
        statusType: { type: String, optional: true, validate: t => ['info', 'success', 'warning', 'danger', 'neutral', 'primary', 'secondary', 'default', 'light', 'dark'].includes(t) }, // Added light & dark for more options
        isPill: { type: Boolean, optional: true },
    };

    static defaultProps = {
        statusType: 'default',
        isPill: false,
    };

    /**
     * Setup method for the component.
     */
    setup() {
        super.setup();
    }

    /**
     * Computed property returning CSS classes for the badge.
     * @returns {String} CSS classes.
     */
    get badgeClass() {
        const classes = ['o_status_badge', `o_status_badge--${(this.props.statusType || 'default').toLowerCase()}`];
        if (this.props.isPill) {
            classes.push('o_status_badge--pill');
        }
        return classes.join(' ');
    }
}