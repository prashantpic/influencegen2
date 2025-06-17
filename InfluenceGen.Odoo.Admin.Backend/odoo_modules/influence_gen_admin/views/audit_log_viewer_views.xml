<odoo>
    <data>
        <!-- Audit Log List View -->
        <record id="view_influence_gen_audit_log_tree_admin" model="ir.ui.view">
            <field name="name">influence.gen.audit.log.tree.admin</field>
            <field name="model">influence_gen.audit_log</field>
            <field name="arch" type="xml">
                <tree string="Audit Logs" default_order="timestamp desc">
                    <field name="timestamp"/>
                    <field name="actor_user_id"/>
                    <field name="event_type"/>
                    <field name="action"/>
                    <field name="target_entity"/>
                    <field name="target_record_display_name" string="Target Record"/> <!-- Assuming target_record_display_name is a related field for display -->
                    <field name="target_id" column_invisible="True"/>
                    <field name="ip_address" optional="show"/>
                </tree>
            </field>
        </record>

        <!-- Audit Log Form View (Read-only) -->
        <record id="view_influence_gen_audit_log_form_admin" model="ir.ui.view">
            <field name="name">influence.gen.audit.log.form.admin</field>
            <field name="model">influence_gen.audit_log</field>
            <field name="arch" type="xml">
                <form string="Audit Log Entry" create="false" edit="false" delete="false">
                    <sheet>
                        <group>
                            <group>
                                <field name="timestamp"/>
                                <field name="actor_user_id"/>
                                <field name="event_type"/>
                                <field name="action"/>
                            </group>
                            <group>
                                <field name="target_entity"/>
                                <field name="target_id"/>
                                <field name="target_record_display_name" string="Target Record Name"/>
                                <field name="ip_address"/>
                            </group>
                        </group>
                        <group string="Details (JSON)">
                            <field name="details_json" widget="ace" options="{'mode': 'json', 'readonly': True}" nolabel="1"/>
                        </group>
                    </sheet>
                </form>
            </field>
        </record>

        <!-- Audit Log Search View -->
        <record id="view_influence_gen_audit_log_search_admin" model="ir.ui.view">
            <field name="name">influence.gen.audit.log.search.admin</field>
            <field name="model">influence_gen.audit_log</field>
            <field name="arch" type="xml">
                <search string="Search Audit Logs">
                    <field name="actor_user_id"/>
                    <field name="event_type"/>
                    <field name="action"/>
                    <field name="target_entity"/>
                    <field name="target_id"/>
                    <field name="ip_address"/>
                    <field name="details_json" string="Details (JSON contains)"/>
                    <filter string="Timestamp" name="filter_timestamp" date="timestamp"/>
                    <filter string="Today" name="filter_today" domain="[('timestamp', '&gt;=', context_today().strftime('%Y-%m-%d 00:00:00')), ('timestamp', '&lt;=', context_today().strftime('%Y-%m-%d 23:59:59'))]"/>
                    <filter string="This Week" name="filter_this_week"
                            domain="[('timestamp', '&gt;=', (context_today() - relativedelta(weeks=1, weekday=0)).strftime('%Y-%m-%d 00:00:00')),
                                     ('timestamp', '&lt;=', (context_today() + relativedelta(weekday=6)).strftime('%Y-%m-%d 23:59:59'))]"/>
                    <filter string="This Month" name="filter_this_month" domain="[('timestamp', '&gt;=', context_today().strftime('%Y-%m-01 00:00:00'))]"/>

                    <group expand="0" string="Group By">
                        <filter string="Actor User" name="group_by_actor_user_id" context="{'group_by': 'actor_user_id'}"/>
                        <filter string="Event Type" name="group_by_event_type" context="{'group_by': 'event_type'}"/>
                        <filter string="Action" name="group_by_action" context="{'group_by': 'action'}"/>
                        <filter string="Target Entity" name="group_by_target_entity" context="{'group_by': 'target_entity'}"/>
                        <filter string="Date (Day)" name="group_by_date" context="{'group_by': 'timestamp:day'}"/>
                    </group>
                </search>
            </field>
        </record>

        <!-- Audit Log Viewer Action Window -->
        <record id="action_influence_gen_audit_log_viewer" model="ir.actions.act_window">
            <field name="name">Audit Logs</field>
            <field name="res_model">influence_gen.audit_log</field>
            <field name="view_mode">tree,form</field>
            <field name="search_view_id" ref="view_influence_gen_audit_log_search_admin"/>
            <field name="context">{'search_default_order_by_timestamp_desc': 1}</field>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    No audit logs found.
                </p><p>
                    Audit logs track important events and changes within the system.
                </p>
            </field>
        </record>
    </data>
</odoo>