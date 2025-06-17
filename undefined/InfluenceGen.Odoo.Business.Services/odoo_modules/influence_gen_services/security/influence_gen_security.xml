<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">

        <!-- Security Categories -->
        <record model="ir.module.category" id="module_category_influence_gen">
            <field name="name">InfluenceGen</field>
            <field name="description">Manages access rights for the InfluenceGen platform.</field>
            <field name="sequence">20</field>
        </record>

        <!-- Security Groups -->
        <record id="group_influence_gen_influencer" model="res.groups">
            <field name="name">InfluenceGen / Influencer</field>
            <field name="category_id" ref="module_category_influence_gen"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user')), (4, ref('base.group_portal'))]"/>
            <field name="comment">The user is an influencer on the platform.</field>
        </record>

        <record id="group_influence_gen_admin" model="res.groups">
            <field name="name">InfluenceGen / Platform Administrator</field>
            <field name="category_id" ref="module_category_influence_gen"/>
            <field name="implied_ids" eval="[(4, ref('base.group_system'))]"/> <!-- System admin implies user -->
            <field name="comment">The user is an administrator of the InfluenceGen platform.</field>
        </record>

        <!-- Record Rules -->

        <!-- Influencer Profile: Own Records Only for Influencers -->
        <record id="influencer_profile_self_rule_influencer" model="ir.rule">
            <field name="name">Influencer Profile: Own Record Access for Influencer</field>
            <field name="model_id" ref="model_influence_gen_influencer_profile"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/> <!-- Assuming influencers can initiate their profile -->
            <field name="perm_unlink" eval="False"/> <!-- Influencers cannot delete their own profile -->
            <field name="domain_force">[('user_id','=',user.id)]</field>
        </record>
        <!-- Influencer Profile: Admin All Access -->
        <record id="influencer_profile_admin_all_rule" model="ir.rule">
            <field name="name">Influencer Profile: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_influencer_profile"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="True"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- Social Media Profile: Own Records for Influencers -->
        <record id="social_media_profile_self_rule_influencer" model="ir.rule">
            <field name="name">Social Media Profile: Own Record Access</field>
            <field name="model_id" ref="model_influence_gen_social_media_profile"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="True"/> <!-- Influencers can manage their social profiles -->
            <field name="domain_force">[('influencer_profile_id.user_id','=',user.id)]</field>
        </record>
        <record id="social_media_profile_admin_all_rule" model="ir.rule">
            <field name="name">Social Media Profile: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_social_media_profile"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- KYC Data: Own Records for Influencers (Read/Create only, Write by Admin for status) -->
        <record id="kyc_data_self_rule_influencer" model="ir.rule">
            <field name="name">KYC Data: Own Record Access</field>
            <field name="model_id" ref="model_influence_gen_kyc_data"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/> <!-- Status updated by admin/system -->
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="False"/>
            <field name="domain_force">[('influencer_profile_id.user_id','=',user.id)]</field>
        </record>
        <record id="kyc_data_admin_all_rule" model="ir.rule">
            <field name="name">KYC Data: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_kyc_data"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- Bank Account: Own Records for Influencers -->
        <record id="bank_account_self_rule_influencer" model="ir.rule">
            <field name="name">Bank Account: Own Record Access</field>
            <field name="model_id" ref="model_influence_gen_bank_account"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="False"/> <!-- Prevent accidental deletion, admin can manage -->
            <field name="domain_force">[('influencer_profile_id.user_id','=',user.id)]</field>
        </record>
        <record id="bank_account_admin_all_rule" model="ir.rule">
            <field name="name">Bank Account: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_bank_account"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- Terms Consent: Own Records for Influencers (Read/Create) -->
        <record id="terms_consent_self_rule_influencer" model="ir.rule">
            <field name="name">Terms Consent: Own Record Access</field>
            <field name="model_id" ref="model_influence_gen_terms_consent"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="False"/>
            <field name="domain_force">[('influencer_profile_id.user_id','=',user.id)]</field>
        </record>
        <record id="terms_consent_admin_all_rule" model="ir.rule">
            <field name="name">Terms Consent: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_terms_consent"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- Campaign: Influencer Read, Admin Full -->
        <record id="campaign_influencer_read_rule" model="ir.rule">
            <field name="name">Campaign: Influencer Read Access</field>
            <field name="model_id" ref="model_influence_gen_campaign"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
            <field name="domain_force">[('status','in',['published','open','in_progress','completed'])]</field> <!-- Influencers see active/past campaigns -->
        </record>
         <record id="campaign_admin_all_rule" model="ir.rule">
            <field name="name">Campaign: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_campaign"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- Campaign Application: Own for Influencer -->
        <record id="campaign_application_self_rule_influencer" model="ir.rule">
            <field name="name">Campaign Application: Own Record Access</field>
            <field name="model_id" ref="model_influence_gen_campaign_application"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/> <!-- Can update own proposal or withdraw -->
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="False"/> <!-- Cannot delete, can withdraw -->
            <field name="domain_force">[('influencer_profile_id.user_id','=',user.id)]</field>
        </record>
        <record id="campaign_application_admin_all_rule" model="ir.rule">
            <field name="name">Campaign Application: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_campaign_application"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- Content Submission: Own for Influencer -->
        <record id="content_submission_self_rule_influencer" model="ir.rule">
            <field name="name">Content Submission: Own Record Access</field>
            <field name="model_id" ref="model_influence_gen_content_submission"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/>
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="False"/>
            <field name="domain_force">[('influencer_profile_id.user_id','=',user.id)]</field>
        </record>
         <record id="content_submission_admin_all_rule" model="ir.rule">
            <field name="name">Content Submission: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_content_submission"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- AI Image Generation Request: Own for Influencer -->
        <record id="ai_image_request_self_rule_influencer" model="ir.rule">
            <field name="name">AI Image Request: Own Record Access</field>
            <field name="model_id" ref="model_influence_gen_ai_image_generation_request"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="True"/> <!-- Can cancel own pending requests -->
            <field name="perm_create" eval="True"/>
            <field name="perm_unlink" eval="False"/>
            <field name="domain_force">[('user_id','=',user.id)]</field>
        </record>
        <record id="ai_image_request_admin_all_rule" model="ir.rule">
            <field name="name">AI Image Request: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_ai_image_generation_request"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- Generated Image: Own for Influencer (via request) -->
        <record id="generated_image_self_rule_influencer" model="ir.rule">
            <field name="name">Generated Image: Own Record Access</field>
            <field name="model_id" ref="model_influence_gen_generated_image"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/> <!-- Meta-data mostly system set -->
            <field name="perm_create" eval="False"/> <!-- System created -->
            <field name="perm_unlink" eval="False"/> <!-- System managed via retention -->
            <field name="domain_force">[('request_id.user_id','=',user.id)]</field>
        </record>
        <record id="generated_image_admin_all_rule" model="ir.rule">
            <field name="name">Generated Image: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_generated_image"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- Payment Record: Own for Influencer (Read-only) -->
        <record id="payment_record_self_rule_influencer" model="ir.rule">
            <field name="name">Payment Record: Own Record Read Access</field>
            <field name="model_id" ref="model_influence_gen_payment_record"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_influencer'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
            <field name="domain_force">[('influencer_profile_id.user_id','=',user.id)]</field>
        </record>
         <record id="payment_record_admin_all_rule" model="ir.rule">
            <field name="name">Payment Record: Admin All Access</field>
            <field name="model_id" ref="model_influence_gen_payment_record"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

        <!-- Audit Log: Admin Read-Only -->
        <record id="audit_log_admin_read_rule" model="ir.rule">
            <field name="name">Audit Log: Admin Read-Only Access</field>
            <field name="model_id" ref="model_influence_gen_audit_log"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>
        
        <!-- Platform Setting: Admin Full -->
        <record id="platform_setting_admin_rule" model="ir.rule">
            <field name="name">Platform Setting: Admin Full Access</field>
            <field name="model_id" ref="model_influence_gen_platform_setting"/>
            <field name="groups" eval="[(4, ref('group_influence_gen_admin'))]"/>
            <field name="domain_force">[(1,'=',1)]</field>
        </record>

    </data>
</odoo>