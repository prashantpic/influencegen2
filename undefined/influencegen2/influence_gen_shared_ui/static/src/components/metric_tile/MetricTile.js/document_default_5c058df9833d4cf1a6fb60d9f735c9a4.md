/** @odoo-module **/

import { Component } from "@odoo/owl";

/**
 * MetricTile Component
 *
 * Displays a single key metric, often used in dashboards.
 * REQ-UIUX-019, REQ-UIUX-001
 */
export class MetricTile extends Component {
    static template = "InfluenceGen.Odoo.Shared.UI.Components.MetricTile";

    /**
     * Props for the MetricTile component.
     * @type {Object}
     * @property {String} label - The label for the metric.
     * @property {String|Number} value - The value of the metric.
     * @property {String} [unit] - Unit for the value (e.g., '%', 'USD').
     * @property {String} [trend] - Trend indicator ('up', 'down', 'neutral').
     * @property {String|Number} [trendValue] - Value associated with the trend (e.g., "+5%").
     * @property {String} [iconClass] - CSS class for an icon to display (e.g., Font Awesome class).
     * @property {String} [infoText] - Additional contextual information or comparison text.
     */
    static props = {
        label: { type: String, required: true },
        value: { type: [String, Number], required: true },
        unit: { type: String, optional: true },
        trend: { type: String, optional: true, validate: t => ['up', 'down', 'neutral'].includes(t) },
        trendValue: { type: [String, Number], optional: true },
        iconClass: { type: String, optional: true },
        infoText: { type: String, optional: true },
    };

    /**
     * Setup method for the component.
     */
    setup() {
        super.setup();
    }

    /**
     * Computed property to determine the CSS class for the trend icon.
     * @returns {String} CSS class for the trend icon.
     */
    get trendIconClass() {
        let baseClass = "fa"; // Assuming Font Awesome
        switch (this.props.trend) {
            case 'up':
                return `${baseClass} fa-arrow-up text-success`;
            case 'down':
                return `${baseClass} fa-arrow-down text-danger`;
            case 'neutral':
                return `${baseClass} fa-minus text-muted`; // Example for neutral
            default:
                return "";
        }
    }
}