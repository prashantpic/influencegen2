<odoo>
    <data>
        <!-- Root Menu -->
        <menuitem id="menu_influence_gen_admin_root"
                  name="InfluenceGen Admin"
                  web_icon="influence_gen_admin,static/description/icon.png"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"
                  sequence="10"/>

        <!-- Dashboard Menu (Points to Performance Dashboard for now) -->
        <menuitem id="menu_influence_gen_admin_dashboard"
                  name="Dashboard"
                  parent="menu_influence_gen_admin_root"
                  action="action_influence_gen_performance_dashboard"
                  sequence="10"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <!-- Influencers Menu -->
        <menuitem id="menu_influence_gen_admin_influencers"
                  name="Influencers"
                  parent="menu_influence_gen_admin_root"
                  action="influence_gen_services.action_influence_gen_influencer_profile"
                  sequence="20"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <!-- KYC Management Menu -->
        <menuitem id="menu_influence_gen_admin_kyc"
                  name="KYC Management"
                  parent="menu_influence_gen_admin_root"
                  action="action_influence_gen_kyc_data_admin"
                  sequence="30"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <!-- Campaigns Menu -->
        <menuitem id="menu_influence_gen_admin_campaigns"
                  name="Campaigns"
                  parent="menu_influence_gen_admin_root"
                  action="action_influence_gen_campaign_admin"
                  sequence="40"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>
        
        <!-- Content Submissions Menu -->
        <menuitem id="menu_influence_gen_admin_content_submissions"
                  name="Content Submissions"
                  parent="menu_influence_gen_admin_root"
                  action="action_influence_gen_content_submission_admin"
                  sequence="50"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <!-- AI Services Menu -->
        <menuitem id="menu_influence_gen_admin_ai_services"
                  name="AI Services"
                  parent="menu_influence_gen_admin_root"
                  sequence="60"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_ai_model_config"
                  name="AI Model Configuration"
                  parent="menu_influence_gen_admin_ai_services"
                  action="action_influence_gen_ai_model_config"
                  sequence="10"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_ai_usage_tracking"
                  name="AI Usage Tracking"
                  parent="menu_influence_gen_admin_ai_services"
                  action="action_influence_gen_ai_usage_tracking"
                  sequence="20"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <!-- Financials Menu -->
        <menuitem id="menu_influence_gen_admin_financials"
                  name="Financials"
                  parent="menu_influence_gen_admin_root"
                  sequence="70"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_payments"
                  name="Payments"
                  parent="menu_influence_gen_admin_financials"
                  action="action_influence_gen_payment_record_admin"
                  sequence="10"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <!-- User & Access Menu -->
        <menuitem id="menu_influence_gen_admin_user_access"
                  name="User & Access"
                  parent="menu_influence_gen_admin_root"
                  sequence="80"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_users"
                  name="Users"
                  parent="menu_influence_gen_admin_user_access"
                  action="base.action_res_users"
                  sequence="10"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_groups"
                  name="Groups"
                  parent="menu_influence_gen_admin_user_access"
                  action="base.action_res_groups"
                  sequence="20"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <!-- Legal & Compliance Menu -->
        <menuitem id="menu_influence_gen_admin_legal_compliance"
                  name="Legal & Compliance"
                  parent="menu_influence_gen_admin_root"
                  sequence="90"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_legal_documents"
                  name="Legal Documents"
                  parent="menu_influence_gen_admin_legal_compliance"
                  action="action_influence_gen_legal_document_version"
                  sequence="10"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_legal_holds"
                  name="Legal Holds"
                  parent="menu_influence_gen_admin_legal_compliance"
                  action="action_influence_gen_legal_hold"
                  sequence="20"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>
        
        <!-- System Operations Menu -->
        <menuitem id="menu_influence_gen_admin_system_operations"
                  name="System Operations"
                  parent="menu_influence_gen_admin_root"
                  sequence="100"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_audit_logs"
                  name="Audit Logs"
                  parent="menu_influence_gen_admin_system_operations"
                  action="action_influence_gen_audit_log_viewer"
                  sequence="10"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_maintenance_windows"
                  name="Maintenance Windows"
                  parent="menu_influence_gen_admin_system_operations"
                  action="action_influence_gen_maintenance_window"
                  sequence="20"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_broadcast_notifications"
                  name="Broadcast Notifications"
                  parent="menu_influence_gen_admin_system_operations"
                  action="action_influence_gen_broadcast_notification_wizard"
                  sequence="30"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <menuitem id="menu_influence_gen_admin_system_health"
            name="System Health"
            parent="menu_influence_gen_admin_system_operations"
            action="action_influence_gen_system_health_dashboard"
            sequence="40"
            groups="influence_gen_admin.group_influence_gen_platform_admin"/>

        <!-- Configuration Menu -->
        <menuitem id="menu_influence_gen_admin_configuration"
                  name="Configuration"
                  parent="menu_influence_gen_admin_root"
                  action="influence_gen_config_action"
                  sequence="110"
                  groups="influence_gen_admin.group_influence_gen_platform_admin"/>
    </data>
</odoo>