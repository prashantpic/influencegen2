<odoo>
    <data>
        <!-- Payment Record List View -->
        <record id="view_influence_gen_payment_record_tree_admin" model="ir.ui.view">
            <field name="name">influence.gen.payment.record.tree.admin</field>
            <field name="model">influence_gen.payment_record</field>
            <field name="arch" type="xml">
                <tree string="Payment Records" decoration-info="status=='pending'" decoration-warning="status=='in_progress'" decoration-success="status=='paid'" decoration-danger="status=='failed'">
                    <field name="influencer_profile_id"/>
                    <field name="campaign_id" optional="show"/>
                    <field name="amount"/>
                    <field name="currency_id"/>
                    <field name="status"/>
                    <field name="due_date"/>
                    <field name="paid_date" optional="hide"/>
                    <field name="transaction_id" optional="show"/>
                    <field name="payment_method" optional="show"/>
                </tree>
            </field>
        </record>

        <!-- Payment Record Form View -->
        <record id="view_influence_gen_payment_record_form_admin" model="ir.ui.view">
            <field name="name">influence.gen.payment.record.form.admin</field>
            <field name="model">influence_gen.payment_record</field>
            <field name="arch" type="xml">
                <form string="Payment Record">
                    <header>
                        <!-- Add buttons for actions like "Mark as Paid", "Generate Vendor Bill" if applicable -->
                        <button name="action_mark_as_paid" string="Mark as Paid" type="object" class="oe_highlight"
                                attrs="{'invisible': [('status', 'not in', ['pending', 'in_progress'])]}"/>
                        <button name="action_generate_vendor_bill" string="Generate Vendor Bill" type="object"
                                attrs="{'invisible': [('status', '!=', 'pending')]}"/> <!-- Condition depends on accounting integration -->
                        <field name="status" widget="statusbar" statusbar_visible="pending,in_progress,paid,failed"/>
                    </header>
                    <sheet>
                        <group>
                            <group>
                                <field name="influencer_profile_id" options="{'no_create': True}"/>
                                <field name="campaign_id" options="{'no_create': True}"/>
                                <field name="content_submission_id" options="{'no_create': True}"/>
                                <field name="payment_method"/>
                            </group>
                            <group>
                                <field name="amount"/>
                                <field name="currency_id" options="{'no_create': True}"/>
                                <field name="due_date"/>
                                <field name="paid_date"/>
                                <field name="transaction_id"/>
                            </group>
                        </group>
                        <group string="Odoo Accounting Link" name="odoo_accounting_link">
                             <field name="odoo_payment_id" readonly="1" string="Odoo Payment"/> <!-- Assuming odoo_payment_id is a M2O to account.payment -->
                             <field name="odoo_vendor_bill_id" readonly="1" string="Odoo Vendor Bill"/> <!-- Assuming odoo_vendor_bill_id is a M2O to account.move -->
                        </group>
                        <group string="Notes">
                            <field name="notes" nolabel="1"/>
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

        <!-- Payment Record Search View -->
        <record id="view_influence_gen_payment_record_search_admin" model="ir.ui.view">
            <field name="name">influence.gen.payment.record.search.admin</field>
            <field name="model">influence_gen.payment_record</field>
            <field name="arch" type="xml">
                <search string="Search Payment Records">
                    <field name="influencer_profile_id"/>
                    <field name="campaign_id"/>
                    <field name="status"/>
                    <field name="payment_method"/>
                    <filter string="Pending" name="filter_pending" domain="[('status', '=', 'pending')]"/>
                    <filter string="In Progress" name="filter_in_progress" domain="[('status', '=', 'in_progress')]"/>
                    <filter string="Paid" name="filter_paid" domain="[('status', '=', 'paid')]"/>
                    <filter string="Failed" name="filter_failed" domain="[('status', '=', 'failed')]"/>
                    <filter string="Due This Month" name="filter_due_this_month"
                            domain="[('due_date', '&gt;=', context_today().strftime('%Y-%m-01')), ('due_date', '&lt;=', (context_today() + relativedelta(months=1, day=1, days=-1)).strftime('%Y-%m-%d'))]"/>
                    <group expand="0" string="Group By">
                        <filter string="Status" name="group_by_status" context="{'group_by': 'status'}"/>
                        <filter string="Influencer" name="group_by_influencer" context="{'group_by': 'influencer_profile_id'}"/>
                        <filter string="Campaign" name="group_by_campaign" context="{'group_by': 'campaign_id'}"/>
                        <filter string="Payment Method" name="group_by_payment_method" context="{'group_by': 'payment_method'}"/>
                    </group>
                </search>
            </field>
        </record>

        <!-- Payment Record Action Window -->
        <record id="action_influence_gen_payment_record_admin" model="ir.actions.act_window">
            <field name="name">Payment Records</field>
            <field name="res_model">influence_gen.payment_record</field>
            <field name="view_mode">tree,form</field>
            <field name="search_view_id" ref="view_influence_gen_payment_record_search_admin"/>
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    No payment records found.
                </p><p>
                    Manage influencer payments, track statuses, and integrate with accounting.
                </p>
            </field>
        </record>
    </data>
</odoo>