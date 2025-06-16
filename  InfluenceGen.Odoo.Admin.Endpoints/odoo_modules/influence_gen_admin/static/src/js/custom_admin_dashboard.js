/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillStart, useRef, onMounted, onWillUpdateProps, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

// REQ-2-012, REQ-PAC-016, REQ-UIUX-019, REQ-12-007

/**
 * Reusable KPI Widget Component
 * Displays a Key Performance Indicator.
 *
 * Props:
 * - title (String): The title of the KPI.
 * - value (String|Number): The value of the KPI.
 * - unit (String, optional): The unit for the KPI value.
 * - icon (String, optional): CSS class for an icon (e.g., Font Awesome).
 * - colorClass (String, optional): CSS class for styling the widget (e.g., 'bg-primary', 'text-white').
 * - action (Function, optional): A function to call when the widget is clicked.
 */
class AdminKPIWidget extends Component {
    static template = "influence_gen_admin.AdminKPIWidget";
    static props = {
        title: { type: String },
        value: { type: [String, Number] },
        unit: { type: String, optional: true },
        icon: { type: String, optional: true },
        colorClass: { type: String, optional: true },
        action: { type: Function, optional: true },
    };

    setup() {
        this.onClick = () => {
            if (this.props.action) {
                this.props.action();
            }
        };
    }
}

/**
 * Reusable Chart Widget Component
 * Displays a chart using Chart.js.
 *
 * Props:
 * - title (String): The title of the chart.
 * - chartType (String): Type of chart (e.g., 'bar', 'line', 'pie', 'doughnut').
 * - chartData (Object): Data object compatible with Chart.js.
 * - chartOptions (Object, optional): Options object compatible with Chart.js.
 * - height (String, optional): Height of the chart container.
 * - width (String, optional): Width of the chart container.
 */
class AdminChartWidget extends Component {
    static template = "influence_gen_admin.AdminChartWidget";
    static props = {
        title: { type: String },
        chartType: { type: String },
        chartData: { type: Object },
        chartOptions: { type: Object, optional: true },
        height: { type: String, optional: true },
        width: { type: String, optional: true },
    };

    setup() {
        this.canvasRef = useRef("canvas");
        this.chart = null;

        onMounted(() => {
            this.renderChart();
        });

        onWillUpdateProps((nextProps) => {
            if (this.chart) {
                // Check if data or type changed significantly to re-render or update
                if (JSON.stringify(this.props.chartData) !== JSON.stringify(nextProps.chartData) || this.props.chartType !== nextProps.chartType) {
                    this.chart.destroy();
                    this.renderChart(nextProps);
                } else {
                     // For minor updates, Chart.js can update directly
                    this.chart.data = nextProps.chartData;
                    this.chart.options = nextProps.chartOptions || this.getDefaultOptions();
                    this.chart.update();
                }
            }
        });

        onWillUnmount(() => {
            if (this.chart) {
                this.chart.destroy();
            }
        });
    }

    getDefaultOptions() {
        return {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: !!this.props.title,
                    text: this.props.title,
                },
            },
        };
    }

    renderChart(props = this.props) {
        if (this.canvasRef.el) {
            const ctx = this.canvasRef.el.getContext('2d');
            this.chart = new Chart(ctx, {
                type: props.chartType,
                data: props.chartData,
                options: props.chartOptions || this.getDefaultOptions(),
            });
        }
    }
}


/**
 * Main Admin Dashboard Component
 * Container for various dashboard widgets (KPIs, Charts).
 */
class AdminMainDashboard extends Component {
    static template = "influence_gen_admin.AdminMainDashboard";
    static components = { AdminKPIWidget, AdminChartWidget };

    setup() {
        this.rpc = useService("rpc");
        this.actionService = useService("action");

        this.state = useState({
            isLoading: true,
            systemHealth: null,
            campaignPerformance: null,
            opsLogSummary: null,
            kpiData: [],
            chartExamples: [], // To be populated with actual chart data
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });
    }

    async loadDashboardData() {
        this.state.isLoading = true;
        try {
            const [systemHealth, campaignPerformance, opsLogSummary] = await Promise.all([
                this.rpc("/influence_gen_admin/dashboard/system_health", {}),
                this.rpc("/influence_gen_admin/dashboard/campaign_performance", {}),
                this.rpc("/influence_gen_admin/dashboard/ops_log_summary", {}),
            ]);

            this.state.systemHealth = systemHealth;
            this.state.campaignPerformance = campaignPerformance;
            this.state.opsLogSummary = opsLogSummary;

            this.processDataForWidgets();

        } catch (error) {
            console.error("Error loading dashboard data:", error);
            // Optionally, set an error state to display a message in the UI
        } finally {
            this.state.isLoading = false;
        }
    }

    processDataForWidgets() {
        // Example: Transform fetched data into KPI and Chart structures
        this.state.kpiData = [];
        if (this.state.campaignPerformance) {
            this.state.kpiData.push({
                title: "Active Campaigns",
                value: this.state.campaignPerformance.active_campaigns_count || 0,
                icon: "fa fa-bullhorn",
                colorClass: "bg-info text-white",
                action: () => this.navigateToView('influence_gen_admin.action_campaign_admin', { domain: "[('status', '=', 'open')]" })
            });
            this.state.kpiData.push({
                title: "Pending Applications",
                value: this.state.campaignPerformance.pending_applications_count || 0,
                icon: "fa fa-file-text-o",
                colorClass: "bg-warning text-dark",
                 action: () => this.navigateToView('influence_gen_admin.action_campaign_application_admin', { domain: "[('status', '=', 'submitted')]" })
            });
        }
        if (this.state.systemHealth) {
             this.state.kpiData.push({
                title: "AI Service Status",
                value: this.state.systemHealth.ai_service_status || "Unknown",
                icon: "fa fa-cogs",
                colorClass: this.state.systemHealth.ai_service_status === 'Operational' ? 'bg-success text-white' : 'bg-danger text-white',
            });
        }
         this.state.kpiData.push({
            title: "Total Influencers",
            // This would typically come from another endpoint or be aggregated differently
            value: this.state.campaignPerformance?.total_influencers || "N/A", // Example
            icon: "fa fa-users",
            colorClass: "bg-primary text-white",
            action: () => this.navigateToView('influence_gen_admin.action_influencer_profile_admin')
        });


        // Example Chart Data
        this.state.chartExamples = [];
        if (this.state.campaignPerformance && this.state.campaignPerformance.campaign_stages_distribution) {
            this.state.chartExamples.push({
                title: "Campaigns by Stage",
                chartType: 'doughnut',
                chartData: {
                    labels: Object.keys(this.state.campaignPerformance.campaign_stages_distribution),
                    datasets: [{
                        label: 'Campaigns',
                        data: Object.values(this.state.campaignPerformance.campaign_stages_distribution),
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.7)',
                            'rgba(54, 162, 235, 0.7)',
                            'rgba(255, 206, 86, 0.7)',
                            'rgba(75, 192, 192, 0.7)',
                            'rgba(153, 102, 255, 0.7)',
                        ],
                    }]
                },
                height: "300px",
            });
        }

        if (this.state.campaignPerformance && this.state.campaignPerformance.applications_over_time) {
             this.state.chartExamples.push({
                title: "Applications Over Time (Last 7 Days)",
                chartType: 'line',
                chartData: {
                    labels: this.state.campaignPerformance.applications_over_time.labels, //  ['Day1', 'Day2', ...]
                    datasets: [{
                        label: 'Applications Received',
                        data: this.state.campaignPerformance.applications_over_time.data, // [10, 12, ...]
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                height: "300px",
            });
        }
    }

    navigateToView(actionXmlId, context = {}) {
        this.actionService.doAction(actionXmlId, {
            additionalContext: context,
        });
    }

    refreshDashboard() {
        this.loadDashboardData();
    }
}

registry.category("actions").add("influence_gen_admin.AdminDashboard", AdminMainDashboard);

// Export components if they need to be imported elsewhere, though for action registry it's not strictly necessary.
export { AdminMainDashboard, AdminKPIWidget, AdminChartWidget };