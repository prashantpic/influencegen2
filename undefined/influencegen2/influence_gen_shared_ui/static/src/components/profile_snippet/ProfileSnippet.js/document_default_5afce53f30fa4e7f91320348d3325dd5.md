/** @odoo-module **/

import { Component } from "@odoo/owl";
import { getInitials } from "@influence_gen_shared_ui/js/utils/ui_helpers";

/**
 * ProfileSnippet Component
 *
 * Displays a compact summary of an influencer's profile.
 * REQ-UIUX-001
 */
export class ProfileSnippet extends Component {
    static template = "InfluenceGen.Odoo.Shared.UI.Components.ProfileSnippet";

    /**
     * Props for the ProfileSnippet component.
     * @type {Object}
     * @property {Object} influencer - The influencer data object.
     * @property {String} influencer.name - Full name of the influencer.
     * @property {String} [influencer.avatarUrl] - URL for the avatar image.
     * @property {String} [influencer.mainNiche] - Primary area of influence.
     * @property {String} [influencer.profileUrl] - URL to the full influencer profile (makes snippet clickable).
     */
    static props = {
        influencer: { type: Object, required: true },
    };

    /**
     * Setup method for the component.
     */
    setup() {
        super.setup();
    }

    /**
     * Computed property to generate initials from the influencer's name
     * if an avatar URL is not provided.
     * @returns {String} The initials.
     */
    get initials() {
        if (this.props.influencer && !this.props.influencer.avatarUrl && this.props.influencer.name) {
            return getInitials(this.props.influencer.name);
        }
        return "";
    }
}