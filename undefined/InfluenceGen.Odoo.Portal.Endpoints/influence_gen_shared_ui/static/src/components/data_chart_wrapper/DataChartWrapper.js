/** @odoo-module **/

import { Component, useState, useRef, onMounted, onWillUpdateProps, onWillUnmount } from "@odoo/owl";

/**
 * DataChartWrapper Component
 *
 * Provides a reusable wrapper for rendering charts using a library like Chart.js.
 * REQ-UIUX-019, REQ-UIUX-001
 * Assumes Chart.js is globally available (e.g., loaded via Odoo assets).
 */
export class DataChartWrapper extends Component {
    static template = "InfluenceGen.Odoo.Shared.UI.Components.DataChartWrapper";

    /**
     * Props for the DataChartWrapper component.
     * @type {Object}
     * @property {String} chartId - Unique ID for the chart canvas element.
     * @property {String} chartType - Type of chart (e.g., 'bar', 'line', 'pie', 'doughnut').
     * @property {Object} chartData - Data object compatible with Chart.js.
     * @property {Object} [chartOptions] - Options object for Chart.js.
     */
    static props = {
        chartId: { type: String, required: true },
        chartType: { type: String, required: true },
        chartData: { type: Object, required: true },
        chartOptions: { type: Object, optional: true },
    };

    /**
     * Setup method for the component.
     * Initializes state and refs.
     */
    setup() {
        super.setup();
        this.state = useState({ chartInstance: null });
        this.canvasRef = useRef("chartCanvas");

        onMounted(() => this.renderChart());
        onWillUpdateProps((nextProps) => this.handlePropsUpdate(nextProps));
        onWillUnmount(() => this.destroyChart());
    }

    /**
     * Renders the chart using Chart.js.
     */
    renderChart() {
        if (this.canvasRef.el && typeof Chart !== 'undefined') {
            const ctx = this.canvasRef.el.getContext('2d');
            if (this.state.chartInstance) {
                this.state.chartInstance.destroy();
            }
            this.state.chartInstance = new Chart(ctx, {
                type: this.props.chartType,
                data: this.props.chartData,
                options: this.props.chartOptions || {},
            });
        } else {
            console.error("Chart.js is not loaded or canvas element not found for chartId:", this.props.chartId);
        }
    }

    /**
     * Handles updates to component props.
     * Re-renders the chart if data or options change.
     * @param {Object} nextProps - The new props.
     */
    handlePropsUpdate(nextProps) {
        if (!this.state.chartInstance) {
            this.renderChart(); // If chart wasn't rendered initially, try again
            return;
        }

        let needsUpdate = false;
        if (JSON.stringify(nextProps.chartData) !== JSON.stringify(this.props.chartData)) {
            this.state.chartInstance.data = { ...nextProps.chartData };
            needsUpdate = true;
        }
        if (JSON.stringify(nextProps.chartOptions) !== JSON.stringify(this.props.chartOptions)) {
            this.state.chartInstance.options = { ...(nextProps.chartOptions || {}) };
            needsUpdate = true;
        }

        if (nextProps.chartType !== this.props.chartType) {
            // If chart type changes, we need to destroy and re-create
            this.destroyChart();
            // Timeout to ensure canvas is ready for re-initialization after prop change cycle
            setTimeout(() => this.renderChart(), 0); 
        } else if (needsUpdate) {
            this.state.chartInstance.update();
        }
    }

    /**
     * Destroys the chart instance to prevent memory leaks.
     */
    destroyChart() {
        if (this.state.chartInstance) {
            this.state.chartInstance.destroy();
            this.state.chartInstance = null;
        }
    }
}