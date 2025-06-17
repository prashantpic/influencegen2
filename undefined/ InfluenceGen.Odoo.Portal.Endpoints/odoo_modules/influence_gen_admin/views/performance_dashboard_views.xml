<odoo>
    <data>
        <!-- Performance Dashboard View -->
        <record id="influence_gen_performance_dashboard_view" model="ir.ui.view">
            <field name="name">influence.gen.performance.dashboard</field>
            <field name="model">ir.actions.act_window</field> <!-- Placeholder model, dashboards often don't have a direct model -->
            <field name="type">ir.actions.client</field>
            <field name="tag">influence_gen_dashboard</field> <!-- Custom client action tag -->
            <!-- Or use Odoo's built-in dashboard view if preferred -->
            <!-- 
            <field name="model">influence_gen.campaign</field> 
            <field name="arch" type="xml">
                <dashboard>
                    <view type="graph" ref="view_campaign_performance_graph"/>
                    <view type="pivot" ref="view_campaign_performance_pivot"/>
                    <group>
                        <group>
                            <aggregate name="total_budget" field="budget" widget="monetary" string="Total Budget"/>
                            <aggregate name="active_campaigns" field="id" measure="__count__" domain="[('status', 'in', ['published', 'open_for_applications', 'in_execution'])]" string="Active Campaigns"/>
                        </group>
                        <group>
                            <formula name="avg_budget_per_campaign" value="total_budget / (active_campaigns or 1)" string="Avg. Budget/Active Campaign" widget="monetary"/>
                        </group>
                    </group>
                    <view type="list" ref="view_influence_gen_campaign_tree_admin">
                         <field name="name"/>
                         <field name="status"/>
                         <field name="budget"/>
                    </view>
                </dashboard>
            </field>
            -->
        </record>

         <!-- Example Graph View for Dashboard (if using Odoo dashboard tag) -->
        <record id="view_campaign_performance_graph" model="ir.ui.view">
            <field name="name">campaign.performance.graph</field>
            <field name="model">influence_gen.campaign</field> <!-- Or CampaignPerformanceMV -->
            <field name="arch" type="xml">
                <graph string="Campaign Performance">
                    <field name="status" type="col"/>
                    <field name="budget" type="measure"/>
                </graph>
            </field>
        </record>

        <!-- Example Pivot View for Dashboard (if using Odoo dashboard tag) -->
        <record id="view_campaign_performance_pivot" model="ir.ui.view">
            <field name="name">campaign.performance.pivot</field>
            <field name="model">influence_gen.campaign</field> <!-- Or CampaignPerformanceMV -->
            <field name="arch" type="xml">
                <pivot string="Campaign Performance">
                    <field name="brand_client" type="row"/>
                    <field name="status" type="col"/>
                    <field name="budget" type="measure"/>
                </pivot>
            </field>
        </record>

        <!-- Performance Dashboard Action Window -->
        <record id="action_influence_gen_performance_dashboard" model="ir.actions.act_window">
            <field name="name">Performance Dashboard</field>
            <field name="res_model">influence_gen.campaign</field> <!-- Placeholder, change if using client action or different model -->
            <!-- If using client action:
            <field name="res_model">ir.actions.client</field>
            <field name="tag">influence_gen_dashboard_client_action</field>
            -->
            <!-- If using Odoo dashboard view type for a model: -->
            <field name="view_mode">dashboard,graph,pivot,tree,form</field>
            <field name="view_id" ref="influence_gen_performance_dashboard_view"/> <!-- Point to the <dashboard> view if defined -->
            <field name="help" type="html">
                <p class="o_view_nocontent_smiling_face">
                    Performance Dashboard
                </p><p>
                    This dashboard provides an overview of campaign performance and key metrics.
                    (Further configuration or custom client action might be needed for full functionality)
                </p>
            </field>
        </record>

        <!-- Placeholder for Client Action JS (if 'ir.actions.client' is used for a custom dashboard) -->
        <!-- This would typically be in a static/src/js file and added to assets -->
        <!--
        <template id="assets_backend_performance_dashboard" name="performance_dashboard_assets" inherit_id="web.assets_backend">
            <xpath expr="." position="inside">
                <script type="text/javascript" src="/influence_gen_admin/static/src/js/performance_dashboard_action.js"/>
            </xpath>
        </template>
        -->
    </data>
</odoo>