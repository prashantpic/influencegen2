<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="InfluenceGen.Odoo.Shared.UI.Components.ProfileSnippet" owl="1">
        <t t-if="props.influencer.profileUrl">
            <a t-att-href="props.influencer.profileUrl" class="o_profile_snippet d-flex align-items-center text-decoration-none text-body">
                <div class="o_profile_snippet_avatar me-2">
                    <t t-if="props.influencer.avatarUrl">
                        <img t-att-src="props.influencer.avatarUrl" t-att-alt="props.influencer.name" class="rounded-circle"/>
                    </t>
                    <t t-elif="initials">
                        <div class="o_profile_snippet_initials rounded-circle d-flex align-items-center justify-content-center" t-esc="initials"/>
                    </t>
                    <t t-else=""> <!-- Fallback if no avatar and no name for initials -->
                         <div class="o_profile_snippet_initials o_profile_snippet_initials--placeholder rounded-circle d-flex align-items-center justify-content-center">
                            <i class="fa fa-user"/>
                         </div>
                    </t>
                </div>
                <div class="o_profile_snippet_info">
                    <div class="o_profile_snippet_name fw-bold" t-esc="props.influencer.name"/>
                    <t t-if="props.influencer.mainNiche">
                        <div class="o_profile_snippet_niche small text-muted" t-esc="props.influencer.mainNiche"/>
                    </t>
                </div>
            </a>
        </t>
        <t t-else="">
            <div class="o_profile_snippet d-flex align-items-center">
                <div class="o_profile_snippet_avatar me-2">
                    <t t-if="props.influencer.avatarUrl">
                        <img t-att-src="props.influencer.avatarUrl" t-att-alt="props.influencer.name" class="rounded-circle"/>
                    </t>
                    <t t-elif="initials">
                        <div class="o_profile_snippet_initials rounded-circle d-flex align-items-center justify-content-center" t-esc="initials"/>
                    </t>
                     <t t-else=""> <!-- Fallback if no avatar and no name for initials -->
                         <div class="o_profile_snippet_initials o_profile_snippet_initials--placeholder rounded-circle d-flex align-items-center justify-content-center">
                            <i class="fa fa-user"/>
                         </div>
                    </t>
                </div>
                <div class="o_profile_snippet_info">
                    <div class="o_profile_snippet_name fw-bold" t-esc="props.influencer.name"/>
                    <t t-if="props.influencer.mainNiche">
                        <div class="o_profile_snippet_niche small text-muted" t-esc="props.influencer.mainNiche"/>
                    </t>
                </div>
            </div>
        </t>
    </t>
</templates>