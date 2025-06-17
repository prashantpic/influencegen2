<odoo>
    <data>
        <!-- Campaign List View -->
        <record id="view_influence_gen_campaign_tree_admin" model="ir.ui.view">
            <field name="name">influence.gen.campaign.tree.admin</field>
            <field name="model">influence_gen.campaign</field>
            <field name="arch" type="xml">
                <tree string="Campaigns">
                    <field name="name"/>
                    <field name="brand_client"/>
                    <field name="start_date"/>
                    <field name="end_date"/>
                    <field name="status"/>
                    <field name="budget" sum="Total Budget"/>
                </tree>
            </field>
        </record>

        <!-- Campaign Form View -->
        <record id="view_influence_gen_campaign_form_admin" model="ir.ui.view">
            <field name="name">influence.gen.campaign.form.admin</field>
            <field name="model">influence_gen.campaign</field>
            <field name="arch" type="xml">
                <form string="Campaign">
                    <header>
                         <button name="action_publish" string="Publish" type="object" class="oe_highlight" attrs="{'invisible': [('status', '!=', 'draft')]}"/>
                         <button name="action_open_applications" string="Open Applications" type="object" class="oe_highlight" attrs="{'invisible': [('status', '!=', 'published')]}"/>
                         <button name="action_close_applications" string="Close Applications" type="object" attrs="{'invisible': [('status', '!=', 'open_for_applications')]}"/>
                         <button name="action_start_execution" string="Start Execution" type="object" class="oe_highlight" attrs="{'invisible': [('status', 'not in', ['published', 'applications_closed'])]}"/>
                         <button name="action_complete" string="Mark as Completed" type="object" attrs="{'invisible': [('status', '!=', 'in_execution')]}"/>
                         <button name="action_archive" string="Archive" type="object" attrs="{'invisible': [('status', 'not in', ['completed', 'cancelled'])]}"/>
                         <button name="action_cancel" string="Cancel Campaign" type="object" confirm="Are you sure you want to cancel this campaign?" attrs="{'invisible': [('status', 'in', ['completed', 'cancelled', 'archived'])]}"/>
                        <field name="status" widget="statusbar" statusbar_visible="draft,published,open_for_applications,applications_closed,in_execution,completed,cancelled"/>
                    </header>
                    <sheet>
                        <div class="oe_title">
                            <label for="name" class="oe_edit_only"/>
                            <h1><field name="name" placeholder="Campaign Name"/></h1>
                        </div>
                        <group>
                            <group string="Campaign Details">
                                <field name="brand_client"/>
                                <field name="start_date"/>
                                <field name="end_date"/>
                                <field name="submission_deadline"/>
                            </group>
                            <group string="Financials & Compensation">
                                <field name="budget"/>
                                <field name="currency_id" options="{'no_create': True}"/>
                                <field name="compensation_model"/>
                            </group>
                        </group>
                        <notebook>
                            <page string="Description & Goals">
                                <group>
                                    <field name="description" nolabel="1" placeholder="Detailed campaign description..."/>
                                    <field name="goals" nolabel="1" placeholder="Campaign goals and KPIs..."/>
                                </group>
                            </page>
                            <page string="Targeting & Content">
                                <group string="Target Influencer Criteria">
                                    <field name="target_criteria_json" widget="ace" options="{'mode': 'json'}" nolabel="1" placeholder='{"audience_niche": "gaming", "min_followers": 10000, "location": "US"}'/>
                                </group>
                                <group string="Content Requirements">
                                    <field name="content_requirements" nolabel="1" placeholder="Specific requirements for content creation (e.g., mention brand, use hashtag #xyz)..."/>
                                </group>
                                <group string="Usage Rights">
                                    <field name="usage_rights" nolabel="1" placeholder="Details on usage rights for submitted content..."/>
                                </group>
                            </page>
                            <page string="Applications">
                                <field name="campaign_application_ids" nolabel="1" context="{'default_campaign_id': active_id}">
                                    <tree>
                                        <field name="influencer_profile_id"/>
                                        <field name="submitted_at"/>
                                        <field name="status"/>
                                        <button name="action_approve_application" string="Approve" type="object" icon="fa-check" attrs="{'invisible': [('status', '!=', 'submitted')]}"/>
                                        <button name="action_reject_application" string="Reject" type="object" icon="fa-times" attrs="{'invisible': [('status', '!=', 'submitted')]}"/>
                                    </tree>
                                    <form>
                                        <sheet>
                                            <group>
                                                <field name="campaign_id" readonly="1"/>
                                                <field name="influencer_profile_id" readonly="1"/>
                                                <field name="status"/>
                                                <field name="submitted_at" readonly="1"/>
                                                <field name="reviewed_at" readonly="1"/>
                                                <field name="reviewer_id" readonly="1"/>
                                            </group>
                                            <group string="Proposal">
                                                <field name="proposal" nolabel="1"/>
                                            </group>
                                             <group string="Rejection Reason" attrs="{'invisible': [('status', '!=', 'rejected')]}">
                                                <field name="rejection_reason" nolabel="1"/>
                                            </group>
                                        </sheet>
                                    </form>
                                </field>
                            </page>
                            <page string="Content Submissions">
                                <!-- This could be a related field from applications or a direct one2many if model structure allows -->
                                <!-- Assuming content_submission_ids is a related field on campaign through campaign_application_ids -->
                                 <field name="content_submission_ids" nolabel="1" context="{'default_campaign_id': active_id}">
                                     <tree>
                                         <field name="campaign_application_id" column_invisible="1"/>
                                         <field name="influencer_profile_id" related="campaign_application_id.influencer_profile_id"/>
                                         <field name="submission_date"/>
                                         <field name="content_url" widget="url"/>
                                         <field name="review_status"/>
                                         <field name="version"/>
                                         <button name="action_approve_content" string="Approve" type="object" icon="fa-check" attrs="{'invisible': [('review_status', '!=', 'pending_review')]}"/>
                                         <button name="action_request_revision" string="Request Revision" type="object" icon="fa-pencil" attrs="{'invisible': [('review_status', '!=', 'pending_review')]}"/>
                                         <button name="action_reject_content" string="Reject" type="object" icon="fa-times" attrs="{'invisible': [('review_status', '!=', 'pending_review')]}"/>
                                     </tree>
                                     <form>
                                         <sheet>
                                             <group>
                                                <field name="campaign_application_id" options="{'no_open': True}"/>
                                                <field name="influencer_profile_id" related="campaign_application_id.influencer_profile_id" string="Influencer"/>
                                                <field name="submission_date"/>
                                                <field name="content_url" widget="url"/>
                                                <field name="file_type"/>
                                                <field name="review_status"/>
                                                <field name="reviewed_by_user_id"/>
                                                <field name="reviewed_at"/>
                                                <field name="version"/>
                                             </group>
                                             <group string="Feedback">
                                                 <field name="feedback" nolabel="1"/>
                                             </group>
                                         </sheet>
                                     </form>
                                 </field>
                            </page>
                             <page string="Performance">
                                 <group>
                                     <field name="actual_performance_metrics_json" widget="ace" options="{'mode': 'json'}" nolabel="1" placeholder='{"total_reach": 50000, "engagement_rate": "2.5%"}'/>
                                 </group>
                             </page>
                        </notebook>
                    </sheet>
                    <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <!-- Campaign Kanban View -->
        <record id="view_influence_gen_campaign_kanban_admin" model="ir.ui.view">
            <field name="name">influence.gen.campaign.kanban.admin</field>
            <field name="model">influence_gen.campaign</field>
            <field name="arch" type="xml">
                <kanban default_group_by="status">
                    <field name="name"/>
                    <field name="brand_client"/>
                    <field name="end_date"/>
                    <field name="status"/>
                    <field name="budget"/>
                    <field name="currency_id"/>
                    <templates>
                        <t t-name="kanban-box">
                            <div t-attf-class="oe_kanban_global_click">
                                <div class="o_kanban_record_top">
                                    <div class="o_kanban_record_headings">
                                        <strong class="o_kanban_record_title"><field name="name"/></strong>
                                    </div>
                                    <small><field name="brand_client"/></small>
                                </div>
                                <ul>
                                    <li>End Date: <field name="end_date"/></li>
                                    <li>Budget: <field name="budget"/> <field name="currency_id"/></li>
                                </ul>
                                <div class="oe_kanban_bottom_right">
                                    <field name="status" widget="badge" decoration-success="status in ['completed', 'in_execution']" decoration-info="status in ['published', 'open_for_applications']" decoration-warning="status == 'applications_closed'" decoration-danger="status == 'cancelled'" decoration-muted="status == 'draft'"/>
                                </div>
                            </div>
                        </t>
                    </templates>
                </kanban>
            </field>
        </record>

        <!-- Campaign Search View -->
        <record id="view_influence_gen_campaign_search_admin" model="ir.ui.view">
            <field name="name">influence.gen.campaign.search.admin</field>
            <field name="model">influence_gen.campaign</field>
            <field name="arch" type="xml">
                <search string="Search Campaigns">
                    <field name="name"/>
                    <field name="brand_client"/>
                    <field name="status"/>
                    <filter string="Draft" name="filter_draft" domain="[('status', '=', 'draft')]"/>
                    <filter string="Published" name="filter_published" domain="[('status', '=', 'published')]"/>
                    <filter string="Open for Applications" name="filter_open_for_applications" domain="[('status', '=', 'open_for_applications')]"/>
                    <filter string="In Execution" name="filter_in_execution" domain="[('status', '=', 'in_execution')]"/>
                    <filter string="Completed" name="filter_completed" domain="[('status', '=', 'completed')]"/>
                    <filter string="Archived" name="filter_archived" domain="[('active', '=', False)]"/>
                    <group expand="0" string="Group By">
                        <filter string="Status" name="group_by_status" context="{'group_by': 'status'}"/>
                        <filter string="Brand/Client" name="group_by_brand" context="{'group_by': 'brand_client'}"/>
                    </group>
                </search>
            </field>
        </record>

        <!-- Campaign Action Window -->
        <record id="action_influence_gen_campaign_admin" model="ir.actions.act_window">
            <field name="name">Campaigns</field>
            <field name="res_model">influence_gen.campaign</field>
            <field name="view_mode">kanban,tree,form</field>
            <field name="search_view_id" ref="view_influence_gen_campaign_search_admin"/>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Create a new Campaign.
                </p>
            </field>
        </record>

        <!-- Content Submission Action Window (for direct menu if needed, typically accessed via Campaign) -->
         <record id="action_influence_gen_content_submission_admin" model="ir.actions.act_window">
            <field name="name">Content Submissions</field>
            <field name="res_model">influence_gen.content_submission</field>
            <field name="view_mode">tree,form</field>
            <!-- Add search view if a dedicated one is created -->
            <field name="context">{'search_default_pending_review': 1}</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    No content submissions found.
                </p><p>
                    Content submissions are typically managed through their respective campaigns.
                </p>
            </field>
        </record>
    </data>
</odoo>