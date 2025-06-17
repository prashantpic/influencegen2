<odoo>
    <data>
        <!-- Legal Hold List View -->
        <record id="view_influence_gen_legal_hold_tree" model="ir.ui.view">
            <field name="name">influence.gen.legal.hold.tree</field>
            <field name="model">influence_gen.legal_hold</field>
            <field name="arch" type="xml">
                <tree string="Legal Holds" decoration-danger="status=='active'" decoration-success="status=='lifted'">
                    <field name="name"/>
                    <field name="status"/>
                    <field name="target_model_id" optional="show"/>
                    <field name="target_record_id" string="Target Record"/>
                    <field name="target_influencer_id" optional="show"/>
                    <field name="target_campaign_id" optional="show"/>
                    <field name="effective_date"/>
                    <field name="lifted_date" optional="hide"/>
                    <field name="created_by_id" optional="show"/>
                </tree>
            </field>
        </record>

        <!-- Legal Hold Form View -->
        <record id="view_influence_gen_legal_hold_form" model="ir.ui.view">
            <field name="name">influence.gen.legal.hold.form</field>
            <field name="model">influence_gen.legal_hold</field>
            <field name="arch" type="xml">
                <form string="Legal Hold">
                    <header>
                        <button name="action_lift_hold" string="Lift Hold" type="object"
                                class="oe_highlight" attrs="{'invisible': [('status', '!=', 'active')]}"/>
                        <field name="status" widget="statusbar" statusbar_visible="active,lifted"/>
                    </header>
                    <sheet>
                        <div class="oe_title">
                            <label for="name" class="oe_edit_only"/>
                            <h1><field name="name" placeholder="e.g. Case #123 - Influencer Data Hold"/></h1>
                        </div>
                        <group>
                            <group string="Hold Details">
                                <field name="effective_date"/>
                                <field name="created_by_id" readonly="1"/>
                            </group>
                            <group string="Lift Details" attrs="{'invisible': [('status', '!=', 'lifted')]}">
                                <field name="lifted_date" readonly="1"/>
                                <field name="lifted_by_id" readonly="1"/>
                            </group>
                        </group>
                        <group string="Target">
                             <field name="target_model_id" options="{'no_create': True}"/>
                             <field name="target_record_id"
                                   context="{'active_model': target_model_id and env['ir.model'].browse(target_model_id).model or False}"
                                   domain="target_model_id and [('model', '=', env['ir.model'].browse(target_model_id).model)] or []"
                                   placeholder="Select a record after choosing a model"/>
                             <field name="target_influencer_id" options="{'no_create': True}"/>
                             <field name="target_campaign_id" options="{'no_create': True}"/>
                        </group>
                        <group string="Reason for Hold">
                            <field name="description" nolabel="1" placeholder="Detailed reason for placing this legal hold..."/>
                        </group>
                    </sheet>
                     <div class="oe_chatter">
                        <field name="message_follower_ids"/>
                        <field name="activity_ids"/>
                        <field name="message_ids"/>
                    </div>
                </form>
            </field>
        </record>

        <!-- Legal Hold Search View -->
        <record id="view_influence_gen_legal_hold_search" model="ir.ui.view">
            <field name="name">influence.gen.legal.hold.search</field>
            <field name="model">influence_gen.legal_hold</field>
            <field name="arch" type="xml">
                <search string="Search Legal Holds">
                    <field name="name" string="Hold Name/Case ID"/>
                    <field name="status"/>
                    <field name="target_model_id"/>
                    <field name="target_influencer_id"/>
                    <field name="target_campaign_id"/>
                    <field name="description" string="Reason contains"/>
                    <filter string="Active" name="filter_active" domain="[('status', '=', 'active')]"/>
                    <filter string="Lifted" name="filter_lifted" domain="[('status', '=', 'lifted')]"/>
                    <group expand="0" string="Group By">
                        <filter string="Status" name="group_by_status" context="{'group_by': 'status'}"/>
                        <filter string="Target Model" name="group_by_target_model" context="{'group_by': 'target_model_id'}"/>
                        <filter string="Effective Date (Month)" name="group_by_effective_date" context="{'group_by': 'effective_date:month'}"/>
                    </group>
                </search>
            </field>
        </record>

        <!-- Legal Hold Action Window -->
        <record id="action_influence_gen_legal_hold" model="ir.actions.act_window">
            <field name="name">Legal Holds</field>
            <field name="res_model">influence_gen.legal_hold</field>
            <field name="view_mode">tree,form</field>
            <field name="search_view_id" ref="view_influence_gen_legal_hold_search"/>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Create a new Legal Hold.
                </p><p>
                    Manage legal holds on platform data to prevent modification or deletion.
                </p>
            </field>
        </record>
    </data>
</odoo>