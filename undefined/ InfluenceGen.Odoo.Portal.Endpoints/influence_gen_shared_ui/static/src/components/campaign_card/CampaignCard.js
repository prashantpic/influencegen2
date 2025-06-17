/** @odoo-module **/

import { Component } from "@odoo/owl";
import { StatusBadge } from "@influence_gen_shared_ui/components/status_badge/StatusBadge";
import { formatDate } from "@influence_gen_shared_ui/js/utils/ui_helpers";

/**
 * CampaignCard Component
 *
 * Displays a summary of a campaign in a card format.
 * REQ-UIUX-001
 */
export class CampaignCard extends Component {
    static template = "InfluenceGen.Odoo.Shared.UI.Components.CampaignCard";
    static components = { StatusBadge };

    /**
     * Props for the CampaignCard component.
     * @type {Object}
     * @property {Object} campaign - The campaign data object.
     * @property {Number|String} campaign.id - Campaign identifier.
     * @property {String} campaign.name - Campaign name.
     * @property {String} campaign.status - Campaign status (e.g., 'Published', 'Ongoing', 'Completed').
     * @property {String} [campaign.statusType] - Type for StatusBadge (e.g., 'success', 'info').
     * @property {String|Date} campaign.startDate - Campaign start date.
     * @property {String|Date} campaign.endDate - Campaign end date.
     * @property {String} [campaign.descriptionShort] - A brief description or excerpt.
     * @property {String} [campaign.budgetFormatted] - Formatted budget.
     * @property {String} [campaign.compensationModelText] - Text describing compensation.
     * @property {String} [campaign.imageUrl] - URL for a campaign image.
     * @property {String} [campaign.brandName] - Name of the brand.
     * @property {String} [campaign.targetAudienceSummary] - Brief summary of target audience.
     */
    static props = {
        campaign: { type: Object, required: true },
    };

    /**
     * Setup method for the component.
     * Initializes any component-specific logic.
     */
    setup() {
        super.setup();
        // The formatDate utility will be used directly in the template
        // for better readability and to handle potential prop updates.
    }

    /**
     * Handles the 'View Details' button click.
     * Emits a 'view-details' event with the campaign ID.
     */
    onViewDetailsClick() {
        this.trigger("view-details", { campaignId: this.props.campaign.id });
    }

    /**
     * Formats a date string or Date object.
     * @param {String|Date} dateValue - The date to format.
     * @returns {String} The formatted date string.
     */
    getFormattedDate(dateValue) {
        if (!dateValue) return "";
        return formatDate(dateValue);
    }
}