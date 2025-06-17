<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1"> <!-- noupdate="1" to prevent overwrite on update if manually changed -->

        <!-- REQ-DRH-002: Cron job for applying data retention policies -->
        <record id="ir_cron_apply_retention_policies" model="ir.cron">
            <field name="name">InfluenceGen: Apply Data Retention Policies</field>
            <!--
                The model_id for a service call cron job can be a bit tricky.
                Using 'res.users' as a common model that always exists.
                The service is then accessed via model.env['service.name'].method().
            -->
            <field name="model_id" ref="base.model_res_users"/>
            <field name="state">code</field>
            <field name="code">model.env['influence_gen.services.retention_and_legal_hold'].apply_retention_policies_automated()</field>
            <field name="user_id" ref="base.user_root"/> <!-- Run as superuser for broad access -->
            <field name="interval_number">1</field>
            <field name="interval_type">days</field> <!-- Run daily -->
            <field name="numbercall">-1</field> <!-- Run indefinitely -->
            <field name="doall" eval="False"/> <!-- Process only if server hasn't run it for this period -->
            <field name="active" eval="True"/>
        </record>

        <!-- REQ-AIGS-002: Cron job for resetting monthly AI quotas -->
        <record id="ir_cron_reset_monthly_ai_quotas" model="ir.cron">
            <field name="name">InfluenceGen: Reset Monthly AI Quotas (Conceptual)</field>
            <field name="model_id" ref="base.model_res_users"/> <!-- See comment above -->
            <field name="state">code</field>
            <!-- This method needs to be defined in AiIntegrationService -->
            <field name="code">model.env['influence_gen.services.ai_integration'].reset_monthly_quotas_for_all_users()</field>
            <field name="user_id" ref="base.user_root"/>
            <field name="interval_number">1</field>
            <field name="interval_type">months</field> <!-- Runs monthly -->
            <!-- Run on the 1st of the month at 1 AM server time -->
            <field name="nextcall" eval="(DateTime.now() + relativedelta(months=1, day=1, hour=1, minute=0, second=0)).strftime('%Y-%m-%d %H:%M:%S')" />
            <field name="numbercall">-1</field>
            <field name="doall" eval="False"/>
            <field name="active" eval="True"/>
        </record>

    </data>
</odoo>