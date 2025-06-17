<odoo>
    <data>
        <!-- KYC Data List View -->
        <record id="view_influence_gen_kyc_data_tree_admin" model="ir.ui.view">
            <field name="name">influence.gen.kyc.data.tree.admin</field>
            <field name="model">influence_gen.kyc_data</field>
            <field name="arch" type="xml">
                <tree string="KYC Submissions">
                    <field name="influencer_profile_id"/>
                    <field name="document_type"/>
                    <field name="create_date" string="Submission Date"/>
                    <field name="verification_status"/>
                    <field name="reviewer_id"/>
                    <field name="reviewed_at"/>
                </tree>
            </field>
        </record>

        <!-- KYC Data Form View -->
        <record id="view_influence_gen_kyc_data_form_admin" model="ir.ui.view">
            <field name="name">influence.gen.kyc.data.form.admin</field>
            <field name="model">influence_gen.kyc_data</field>
            <field name="arch" type="xml">
                <form string="KYC Submission">
                    <header>
                        <button name="action_approve" string="Approve" type="object" class="oe_highlight"
                                attrs="{'invisible': [('verification_status', 'not in', ['pending', 'in_review'])]}"/>
                        <button name="action_reject" string="Reject" type="object"
                                attrs="{'invisible': [('verification_status', 'not in', ['pending', 'in_review'])]}"/>
                        <button name="%(action_influence_gen_kyc_request_info_wizard)d" string="Request More Info" type="action"
                                context="{'default_kyc_submission_id': active_id}"
                                attrs="{'invisible': [('verification_status', 'not in', ['pending', 'in_review'])]}"/>
                        <field name="verification_status" widget="statusbar" statusbar_visible="pending,in_review,approved,rejected,needs_more_info"/>
                    </header>
                    <sheet>
                        <group>
                            <group>
                                <field name="influencer_profile_id" options="{'no_open': False, 'no_create': True}"/>
                                <field name="document_type"/>
                                <field name="document_front_url" widget="image" options="{'size': [90, 90]}" attrs="{'readonly': True}"/>
                                <field name="document_back_url" widget="image" options="{'size': [90, 90]}" attrs="{'invisible': [('document_back_url', '=', False)], 'readonly': True}"/>
                            </group>
                            <group>
                                <field name="submission_date" readonly="1"/>
                                <field name="reviewer_id" readonly="1"/>
                                <field name="reviewed_at" readonly="1"/>
                            </group>
                        </group>
                        <notebook>
                            <page string="Review Details">
                                <group>
                                    <field name="notes"/>
                                </group>
                            </page>
                        </notebook>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- KYC Data Kanban View -->
        <record id="view_influence_gen_kyc_data_kanban_admin" model="ir.ui.view">
            <field name="name">influence.gen.kyc.data.kanban.admin</field>
            <field name="model">influence_gen.kyc_data</field>
            <field name="arch" type="xml">
                <kanban default_group_by="verification_status">
                    <field name="influencer_profile_id"/>
                    <field name="document_type"/>
                    <field name="submission_date"/>
                    <field name="verification_status"/>
                    <templates>
                        <t t-name="kanban-box">
                            <div t-attf-class="oe_kanban_global_click">
                                <div class="o_kanban_record_top">
                                    <div class="o_kanban_record_headings">
                                        <strong class="o_kanban_record_title"><field name="influencer_profile_id"/></strong>
                                    </div>
                                </div>
                                <div>
                                    <field name="document_type"/>
                                </div>
                                <div>
                                    <field name="submission_date"/>
                                </div>
                                <div class="oe_kanban_bottom_right">
                                    <field name="verification_status" widget="badge" decoration-success="verification_status == 'approved'" decoration-danger="verification_status == 'rejected'" decoration-warning="verification_status in ['pending', 'in_review', 'needs_more_info']"/>
                                </div>
                            </div>
                        </t>
                    </templates>
                </kanban>
            </field>
        </record>

        <!-- KYC Data Search View -->
        <record id="view_influence_gen_kyc_data_search_admin" model="ir.ui.view">
            <field name="name">influence.gen.kyc.data.search.admin</field>
            <field name="model">influence_gen.kyc_data</field>
            <field name="arch" type="xml">
                <search string="Search KYC Submissions">
                    <field name="influencer_profile_id"/>
                    <field name="document_type"/>
                    <field name="verification_status"/>
                    <filter string="Pending" name="filter_pending" domain="[('verification_status', '=', 'pending')]"/>
                    <filter string="In Review" name="filter_in_review" domain="[('verification_status', '=', 'in_review')]"/>
                    <filter string="Approved" name="filter_approved" domain="[('verification_status', '=', 'approved')]"/>
                    <filter string="Rejected" name="filter_rejected" domain="[('verification_status', '=', 'rejected')]"/>
                    <filter string="Needs More Info" name="filter_needs_more_info" domain="[('verification_status', '=', 'needs_more_info')]"/>
                    <group expand="0" string="Group By">
                        <filter string="Status" name="group_by_status" context="{'group_by': 'verification_status'}"/>
                        <filter string="Document Type" name="group_by_document_type" context="{'group_by': 'document_type'}"/>
                        <filter string="Reviewer" name="group_by_reviewer" context="{'group_by': 'reviewer_id'}"/>
                    </group>
                </search>
            </field>
        </record>

        <!-- KYC Data Action Window -->
        <record id="action_influence_gen_kyc_data_admin" model="ir.actions.act_window">
            <field name="name">KYC Submissions</field>
            <field name="res_model">influence_gen.kyc_data</field>
            <field name="view_mode">kanban,tree,form</field>
            <field name="search_view_id" ref="view_influence_gen_kyc_data_search_admin"/>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    No KYC submissions found.
                </p>
            </field>
        </record>
    </data>
</odoo>