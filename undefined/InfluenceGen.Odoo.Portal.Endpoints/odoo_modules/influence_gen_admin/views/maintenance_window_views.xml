<odoo>
    <data>
        <!-- Maintenance Window List View -->
        <record id="view_influence_gen_maintenance_window_tree" model="ir.ui.view">
            <field name="name">influence.gen.maintenance.window.tree</field>
            <field name="model">influence_gen.maintenance_window</field>
            <field name="arch" type="xml">
                <tree string="Maintenance Windows" decoration-info="status=='planned'" decoration-warning="status=='in_progress'" decoration-success="status=='completed'" decoration-muted="status=='cancelled'">
                    <field name="name"/>
                    <field name="start_datetime"/>
                    <field name="end_datetime"/>
                    <field name="status"/>
                    <field name="notify_users"/>
                </tree>
            </field>
        </record>

        <!-- Maintenance Window Form View -->
        <record id="view_influence_gen_maintenance_window_form" model="ir.ui.view">
            <field name="name">influence.gen.maintenance.window.form</field>
            <field name="model">influence_gen.maintenance_window</field>
            <field name="arch" type="xml">
                <form string="Maintenance Window">
                    <header>
                        <button name="action_send_notification" string="Send Notification" type="object"
                                class="oe_highlight" attrs="{'invisible': [('status', '!=', 'planned')]}"/>
                        <button name="action_start_maintenance" string="Start Maintenance" type="object"
                                class="oe_highlight" attrs="{'invisible': [('status', '!=', 'planned')]}"/>
                        <button name="action_complete_maintenance" string="Complete Maintenance" type="object"
                                class="oe_highlight" attrs="{'invisible': [('status', '!=', 'in_progress')]}"/>
                        <button name="action_cancel_maintenance" string="Cancel Maintenance" type="object"
                                attrs="{'invisible': [('status', 'in', ['completed', 'cancelled'])]}"/>
                        <field name="status" widget="statusbar" statusbar_visible="planned,in_progress,completed,cancelled"/>
                    </header>
                    <sheet>
                        <div class="oe_title">
                            <label for="name" class="oe_edit_only"/>
                            <h1><field name="name" placeholder="e.g. Server Upgrade"/></h1>
                        </div>
                        <group>
                            <group>
                                <field name="start_datetime"/>
                                <field name="end_datetime"/>
                            </group>
                            <group>
                                <field name="notify_users"/>
                            </group>
                        </group>
                        <group string="Description/Impact">
                            <field name="description" nolabel="1" placeholder="Details about the maintenance and expected impact..."/>
                        </group>
                        <group string="Notification Message (if notify users is checked)">
                            <field name="notification_message" nolabel="1" placeholder="Custom message for users. If empty, a default message will be used."
                                   attrs="{'invisible': [('notify_users', '=', False)]}"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- Maintenance Window Calendar View -->
        <record id="view_influence_gen_maintenance_window_calendar" model="ir.ui.view">
            <field name="name">influence.gen.maintenance.window.calendar</field>
            <field name="model">influence_gen.maintenance_window</field>
            <field name="arch" type="xml">
                <calendar string="Maintenance Windows" date_start="start_datetime" date_stop="end_datetime" display="name" color="status">
                    <field name="name"/>
                    <field name="status"/>
                </calendar>
            </field>
        </record>

        <!-- Maintenance Window Action Window -->
        <record id="action_influence_gen_maintenance_window" model="ir.actions.act_window">
            <field name="name">Maintenance Windows</field>
            <field name="res_model">influence_gen.maintenance_window</field>
            <field name="view_mode">tree,form,calendar</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Schedule a new Maintenance Window.
                </p><p>
                    Manage planned system downtimes and notify users.
                </p>
            </field>
        </record>
    </data>
</odoo>