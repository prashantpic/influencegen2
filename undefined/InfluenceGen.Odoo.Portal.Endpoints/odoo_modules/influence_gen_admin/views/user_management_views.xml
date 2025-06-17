<odoo>
    <data>
        <!-- Inherit User Form View to Add InfluenceGen Profile Tab -->
        <record id="view_users_form_inherit_influence_gen" model="ir.ui.view">
            <field name="name">res.users.form.inherit.influence.gen</field>
            <field name="model">res.users</field>
            <field name="inherit_id" ref="base.view_users_form"/>
            <field name="arch" type="xml">
                <xpath expr="//notebook" position="inside">
                    <page string="InfluenceGen Profile" name="influence_gen_profile" 
                          attrs="{'invisible': [('is_influencer', '=', False)]}">
                        <group>
                            <field name="is_influencer" invisible="1"/> <!-- Helper field on res.users -->
                            <field name="influencer_profile_id" readonly="1" options="{'no_open': False, 'no_create': True}"/>
                             <!-- Add more read-only fields from influence_gen.influencer_profile if needed -->
                            <group string="KYC Status (Summary)" name="kyc_summary_placeholder" attrs="{'invisible': [('influencer_profile_id', '=', False)]}">
                                <!-- Placeholder: Display KYC status from related influencer_profile_id -->
                                <!-- This might require a related field on res.users or dynamic fetching if complex -->
                                <label for="influencer_profile_id" string="View Full Profile for Details"/>
                            </group>
                        </group>
                    </page>
                </xpath>
                 <xpath expr="//field[@name='partner_id']" position="after">
                     <!-- This field should be defined on res.users model for this to work -->
                     <!-- It is assumed that 'is_influencer' is a computed field on res.users -->
                     <!-- that checks if a related influencer_gen.influencer_profile exists -->
                    <field name="is_influencer" readonly="1" string="Is Influencer?"/>
                </xpath>
            </field>
        </record>

        <!-- Inherit User Tree View to Add InfluenceGen related info if necessary -->
        <record id="view_users_tree_inherit_influence_gen" model="ir.ui.view">
            <field name="name">res.users.tree.inherit.influence.gen</field>
            <field name="model">res.users</field>
            <field name="inherit_id" ref="base.view_users_tree"/>
            <field name="arch" type="xml">
                <xpath expr="//field[@name='login_date']" position="after">
                    <!-- This field should be defined on res.users model for this to work -->
                    <field name="is_influencer" optional="show"/>
                </xpath>
            </field>
        </record>

        <!-- Inherit Group Form View (No specific changes needed per SDS, but can be extended here) -->
        <record id="view_groups_form_inherit_influence_gen" model="ir.ui.view">
            <field name="name">res.groups.form.inherit.influence.gen</field>
            <field name="model">res.groups</field>
            <field name="inherit_id" ref="base.view_groups_form"/>
            <field name="arch" type="xml">
                <!-- Example: Add a comment or field if relevant to InfluenceGen group management -->
                <xpath expr="//field[@name='comment']" position="after">
                    <field name="category_id" attrs="{'readonly': [('category_id', '=', ref('influence_gen_admin.module_category_influence_gen_administration'))]}"/>
                </xpath>
            </field>
        </record>

    </data>
</odoo>