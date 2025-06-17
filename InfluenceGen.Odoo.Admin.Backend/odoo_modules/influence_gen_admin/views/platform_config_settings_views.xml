<odoo>
    <data>
        <record id="influence_gen_config_settings_view_form" model="ir.ui.view">
            <field name="name">influence.gen.config.settings.view.form</field>
            <field name="model">res.config.settings</field>
            <field name="inherit_id" ref="base_setup.res_config_settings_view_form"/>
            <field name="arch" type="xml">
                <xpath expr="//div[hasclass('settings')]" position="inside">
                    <div class="app_settings_block" data-string="InfluenceGen Platform" string="InfluenceGen Platform" data-key="influence_gen_admin" groups="influence_gen_admin.group_influence_gen_platform_admin">
                        <!-- Security Policies -->
                        <h2>Security Policies</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane">
                                    <field name="influence_gen_mfa_admin_mandatory"/>
                                </div>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_mfa_admin_mandatory"/>
                                    <div class="text-muted">
                                        Enforce Multi-Factor Authentication for Platform Administrators.
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_password_min_length"/>
                                    <div class="text-muted">
                                        <field name="influence_gen_password_min_length" class="oe_inline"/> Minimum length for user passwords.
                                    </div>
                                    <label for="influence_gen_password_complexity_regex"/>
                                    <div class="text-muted">
                                        <field name="influence_gen_password_complexity_regex" class="oe_inline" placeholder="e.g., ^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$"/> Regex for password complexity.
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- AI Services Configuration -->
                        <h2>AI Services Configuration</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_ai_quota_default_images_per_month"/>
                                    <div class="text-muted">
                                        <field name="influence_gen_ai_quota_default_images_per_month" class="oe_inline"/> Default AI images an influencer can generate per month.
                                    </div>
                                    <label for="influence_gen_ai_default_resolution"/>
                                    <div class="text-muted">
                                        <field name="influence_gen_ai_default_resolution" class="oe_inline" placeholder="e.g., 1024x1024"/> Default AI Image Resolution.
                                    </div>
                                     <label for="influence_gen_ai_default_aspect_ratio"/>
                                    <div class="text-muted">
                                        <field name="influence_gen_ai_default_aspect_ratio" class="oe_inline" placeholder="e.g., 16:9"/> Default AI Aspect Ratio.
                                    </div>
                                </div>
                            </div>
                             <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_ai_default_cfg_scale"/>
                                    <div class="text-muted">
                                        <field name="influence_gen_ai_default_cfg_scale" class="oe_inline"/> Default AI CFG Scale.
                                    </div>
                                     <label for="influence_gen_ai_default_inference_steps"/>
                                    <div class="text-muted">
                                        <field name="influence_gen_ai_default_inference_steps" class="oe_inline"/> Default AI Inference Steps.
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- KYC Configuration -->
                        <h2>KYC Configuration</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_kyc_accepted_doc_types"/>
                                    <div class="text-muted">
                                        <field name="influence_gen_kyc_accepted_doc_types" placeholder="Passport,Driver's License"/> Comma-separated list of accepted ID document types.
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 o_setting_box">
                                 <div class="o_setting_left_pane">
                                    <field name="influence_gen_kyc_social_verify_method"/>
                                </div>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_kyc_social_verify_method"/>
                                    <div class="text-muted">
                                        Method used for verifying social media account ownership.
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Data Retention -->
                        <h2>Data Retention Policies (Days)</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_retention_pii_days"/>
                                    <div><field name="influence_gen_retention_pii_days" class="oe_inline"/> <span class="text-muted">PII Retention for inactive influencers.</span></div>
                                    <label for="influence_gen_retention_kyc_docs_days"/>
                                    <div><field name="influence_gen_retention_kyc_docs_days" class="oe_inline"/> <span class="text-muted">KYC Docs Retention.</span></div>
                                    <label for="influence_gen_retention_campaign_data_days"/>
                                    <div><field name="influence_gen_retention_campaign_data_days" class="oe_inline"/> <span class="text-muted">Campaign Data Retention.</span></div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_retention_generated_images_personal_days"/>
                                    <div><field name="influence_gen_retention_generated_images_personal_days" class="oe_inline"/> <span class="text-muted">Personal AI Images Retention.</span></div>
                                    <label for="influence_gen_retention_audit_logs_days"/>
                                    <div><field name="influence_gen_retention_audit_logs_days" class="oe_inline"/> <span class="text-muted">Audit Logs Retention.</span></div>
                                    <label for="influence_gen_retention_operational_logs_days"/>
                                    <div><field name="influence_gen_retention_operational_logs_days" class="oe_inline"/> <span class="text-muted">Operational Logs Retention.</span></div>
                                </div>
                            </div>
                        </div>

                        <!-- Content Moderation -->
                        <h2>Content Moderation</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_content_moderation_ai_prompt_denylist"/>
                                    <div class="text-muted">
                                        <field name="influence_gen_content_moderation_ai_prompt_denylist" placeholder="keyword1,phrase two,..."/> Comma-separated keywords/phrases for AI prompt denylist.
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_content_moderation_api_key"/>
                                    <div><field name="influence_gen_content_moderation_api_key" class="oe_inline" password="True"/> <span class="text-muted">API Key for third-party content moderation.</span></div>
                                    <label for="influence_gen_content_moderation_api_endpoint"/>
                                    <div><field name="influence_gen_content_moderation_api_endpoint" class="oe_inline" placeholder="https://api.moderationservice.com/v1/moderate"/> <span class="text-muted">API Endpoint for content moderation.</span></div>
                                </div>
                            </div>
                        </div>

                        <!-- Email Configuration -->
                        <h2>Email Configuration</h2>
                        <div class="row mt16 o_settings_container">
                             <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <div class="content-group">
                                        <div class="text-muted">
                                            Odoo manages SMTP servers via global settings or specific mail servers. These fields reflect the current company's outgoing mail server. Configure under General Settings / Discuss or Technical / Email / Outgoing Mail Servers.
                                        </div>
                                         <button string="Configure Outgoing Email Servers" name="%(mail.action_ir_mail_server_list)d" type="action" class="oe_link"/>
                                    </div>
                                    <label for="influence_gen_smtp_host" string="Host"/>
                                    <div><field name="influence_gen_smtp_host"/></div>
                                    <label for="influence_gen_smtp_port" string="Port"/>
                                    <div><field name="influence_gen_smtp_port"/></div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_smtp_user" string="Username"/>
                                    <div><field name="influence_gen_smtp_user"/></div>
                                    <label for="influence_gen_smtp_password" string="Password"/>
                                    <div><field name="influence_gen_smtp_password" password="True"/></div>
                                    <label for="influence_gen_smtp_encryption" string="Encryption"/>
                                    <div><field name="influence_gen_smtp_encryption"/></div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Logging & Monitoring -->
                        <h2>Logging & Monitoring</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_log_level_odoo_default"/>
                                    <div><field name="influence_gen_log_level_odoo_default"/> <span class="text-muted">Default Odoo Log Level for InfluenceGen modules.</span></div>
                                    <label for="influence_gen_log_level_n8n_default"/>
                                    <div><field name="influence_gen_log_level_n8n_default"/> <span class="text-muted">Default N8N Log Level (if controllable via API).</span></div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_alert_critical_email_to"/>
                                    <div><field name="influence_gen_alert_critical_email_to" placeholder="admin1@example.com,admin2@example.com"/> <span class="text-muted">Email recipient(s) for critical system alerts.</span></div>
                                </div>
                            </div>
                        </div>

                        <!-- API Configuration -->
                        <h2>API Configuration</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_api_rate_limit_callback"/>
                                    <div><field name="influence_gen_api_rate_limit_callback" placeholder="e.g., 100/minute"/> <span class="text-muted">Rate limit for callback APIs from external services.</span></div>
                                </div>
                            </div>
                        </div>

                        <!-- Payment Configuration -->
                        <h2>Payment Configuration</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_payment_default_journal_id"/>
                                    <div><field name="influence_gen_payment_default_journal_id" domain="[('type', 'in', ('bank', 'cash'))]"/> <span class="text-muted">Default Payment Journal for payouts.</span></div>
                                </div>
                            </div>
                             <div class="col-12 col-lg-6 o_setting_box">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_payment_default_expense_account_id"/>
                                    <div><field name="influence_gen_payment_default_expense_account_id" domain="[('account_type', '=', 'expense')]"/> <span class="text-muted">Default Expense Account for payouts.</span></div>
                                </div>
                            </div>
                        </div>

                        <!-- Secrets Management -->
                        <h2>Secrets Management</h2>
                        <div class="row mt16 o_settings_container">
                            <div class="col-12 col-lg-6 o_setting_box">
                                 <div class="o_setting_left_pane">
                                     <field name="influence_gen_secrets_management_type"/>
                                 </div>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_secrets_management_type"/>
                                    <div class="text-muted">
                                        Method for managing sensitive secrets like API keys.
                                    </div>
                                </div>
                            </div>
                            <div class="col-12 col-lg-6 o_setting_box" attrs="{'invisible': [('influence_gen_secrets_management_type', '!=', 'vault')]}">
                                <div class="o_setting_left_pane"/>
                                <div class="o_setting_right_pane">
                                    <label for="influence_gen_secrets_vault_url"/>
                                    <div><field name="influence_gen_secrets_vault_url" placeholder="https://vault.example.com:8200"/> <span class="text-muted">URL for External Vault (e.g., HashiCorp Vault).</span></div>
                                    <label for="influence_gen_secrets_vault_token_path"/>
                                    <div><field name="influence_gen_secrets_vault_token_path" placeholder="e.g., /path/to/token or auth/approle/login"/> <span class="text-muted">Path for Vault Token or Auth method.</span></div>
                                </div>
                            </div>
                        </div>

                    </div>
                </xpath>
            </field>
        </record>

        <record id="influence_gen_config_action" model="ir.actions.act_window">
            <field name="name">InfluenceGen Settings</field>
            <field name="res_model">res.config.settings</field>
            <field name="view_mode">form</field>
            <field name="target">inline</field>
            <field name="context">{'module' : 'influence_gen_admin', 'bin_size': False}</field>
        </record>
    </data>
</odoo>