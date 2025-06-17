<odoo>
    <data>
        <record id="view_influence_gen_broadcast_notification_wizard_form" model="ir.ui.view">
            <field name="name">influence.gen.broadcast.notification.wizard.form</field>
            <field name="model">influence_gen.broadcast_notification_wizard</field>
            <field name="arch" type="xml">
                <form string="Broadcast Notification">
                    <sheet>
                        <group>
                            <field name="message_subject"/>
                        </group>
                        <group string="Message Body">
                            <field name="message_body" widget="html" nolabel="1"/>
                        </group>
                        <group string="Target Audience">
                            <field name="target_user_group_ids" widget="many2many_tags" options="{'no_create_edit': True}" placeholder="All active users if empty"/>
                            <field name="target_influencer_ids" widget="many2many_tags" options="{'no_create_edit': True}" placeholder="Specific influencers (optional)"/>
                        </group>
                        <group string="Delivery Options">
                            <field name="send_email"/>
                            <field name="show_in_app_banner_duration_hours" attrs="{'invisible': [('send_email', '=', True)]}"/> <!-- Example: show only if not email or always visible -->
                        </group>
                    </sheet>
                    <footer>
                        <button name="action_send_notification" string="Send Notification" type="object" class="btn-primary"/>
                        <button string="Cancel" class="btn-secondary" special="cancel"/>
                    </footer>
                </form>
            </field>
        </record>

        <record id="action_influence_gen_broadcast_notification_wizard" model="ir.actions.act_window">
            <field name="name">Broadcast Notification</field>
            <field name="res_model">influence_gen.broadcast_notification_wizard</field>
            <field name="view_mode">form</field>
            <field name="target">new</field>
        </record>
    </data>
</odoo>