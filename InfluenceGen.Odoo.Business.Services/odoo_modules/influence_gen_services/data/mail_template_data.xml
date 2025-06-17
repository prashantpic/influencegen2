<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0"> <!-- noupdate="0" allows templates to be updated on module upgrade -->

        <!-- REQ-16-001: Influencer Registration Confirmation -->
        <record id="email_template_influencer_registration_confirmation" model="mail.template">
            <field name="name">Influencer: Registration Confirmation</field>
            <field name="model_id" ref="model_influence_gen_influencer_profile"/>
            <field name="subject">Welcome to InfluenceGen, ${object.full_name}! Your Registration is Received</field>
            <field name="email_from">"${object.company_id.email_formatted if object.company_id and object.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Dear ${object.full_name},</p>
                    <p>Thank you for registering with InfluenceGen! We have received your application and are excited to have you join our community.</p>
                    <p>Our team will review your information. You will be notified about the status of your KYC verification and account activation shortly. In the meantime, you can explore your portal and complete any pending profile information.</p>
                    <p>If you have any questions, please don't hesitate to contact our support team.</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
            <field name="report_template" eval="False"/>
        </record>

        <!-- REQ-16-002: KYC Status Update -->
        <record id="email_template_kyc_status_update" model="mail.template">
            <field name="name">Influencer: KYC Status Update</field>
            <!-- Assuming template is triggered on kyc_data or influencer_profile -->
            <field name="model_id" ref="model_influence_gen_kyc_data"/>
            <field name="subject">InfluenceGen: KYC Status Update for ${object.influencer_profile_id.full_name}</field>
            <field name="email_from">"${object.influencer_profile_id.company_id.email_formatted if object.influencer_profile_id and object.influencer_profile_id.company_id and object.influencer_profile_id.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.influencer_profile_id.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Dear ${object.influencer_profile_id.full_name},</p>
                    <p>This email is to inform you about an update to your KYC (Know Your Customer) verification status.</p>
                    <p><strong>Your current KYC status is: ${object.influencer_profile_id.get_field_label('kyc_status')}: ${object.influencer_profile_id.kyc_status.capitalize().replace('_', ' ')}</strong></p>
                    <t t-if="ctx.get('decision') == 'approved'">
                        <p>Congratulations! Your KYC information has been successfully verified.</p>
                    </t>
                    <t t-if="ctx.get('decision') == 'rejected'">
                        <p>Unfortunately, your recent KYC submission could not be approved at this time.</p>
                        <t t-if="ctx.get('notes')"><p>Reason: ${ctx.get('notes')}</p></t>
                        <p>Please review the feedback and resubmit the required information through your portal, or contact support if you have questions.</p>
                    </t>
                    <t t-if="ctx.get('decision') == 'requires_more_info'">
                        <p>We require some additional information or clarification to complete your KYC verification.</p>
                        <t t-if="ctx.get('notes')"><p>Details: ${ctx.get('notes')}</p></t>
                        <p>Please log in to your portal to provide the requested information.</p>
                    </t>
                     <t t-if="not ctx.get('decision') and object.influencer_profile_id.kyc_status == 'submitted'">
                        <p>Your KYC documents have been successfully submitted and are now under review. We will notify you once the review is complete.</p>
                    </t>
                    <p>You can check your application status and details by logging into your portal.</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
        </record>
        
        <!-- REQ-16-002 (alternative for KYC submission received if not covered by status update) -->
        <record id="email_template_kyc_submission_received" model="mail.template">
            <field name="name">Influencer: KYC Submission Received</field>
            <field name="model_id" ref="model_influence_gen_influencer_profile"/>
            <field name="subject">InfluenceGen: Your KYC Documents Have Been Received</field>
            <field name="email_from">"${object.company_id.email_formatted if object.company_id and object.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Dear ${object.full_name},</p>
                    <p>We have successfully received your KYC documents. Our team will now review them.</p>
                    <p>You will be notified via email once the review is complete and your KYC status is updated. This typically takes a few business days.</p>
                    <p>Thank you for your cooperation.</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
        </record>

        <!-- REQ-16-003: Account Activation -->
        <record id="email_template_account_activation" model="mail.template">
            <field name="name">Influencer: Account Activated</field>
            <field name="model_id" ref="model_influence_gen_influencer_profile"/>
            <field name="subject">Congratulations! Your InfluenceGen Account is Now Active!</field>
            <field name="email_from">"${object.company_id.email_formatted if object.company_id and object.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Dear ${object.full_name},</p>
                    <p>Great news! Your InfluenceGen account has been successfully verified and activated.</p>
                    <p>You can now log in to your portal to:</p>
                    <ul>
                        <li>Explore and apply for available campaigns.</li>
                        <li>Manage your profile and payment information.</li>
                        <li>Access AI image generation tools (if applicable).</li>
                    </ul>
                    <p>We're thrilled to have you on board and look forward to seeing your impact!</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
        </record>

        <!-- REQ-16-004: Campaign Application Status -->
        <record id="email_template_campaign_app_approved" model="mail.template">
            <field name="name">Influencer: Campaign Application Approved</field>
            <field name="model_id" ref="model_influence_gen_campaign_application"/>
            <field name="subject">Good News! Your Application for "${object.campaign_id.name}" is Approved!</field>
            <field name="email_from">"${object.campaign_id.company_id.email_formatted if object.campaign_id and object.campaign_id.company_id and object.campaign_id.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.influencer_profile_id.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Dear ${object.influencer_profile_id.full_name},</p>
                    <p>We're pleased to inform you that your application to participate in the campaign "<strong>${object.campaign_id.name}</strong>" has been approved!</p>
                    <p>Please log in to your portal for next steps, content submission guidelines, and deadlines related to this campaign.</p>
                    <p>We're excited to collaborate with you on this project!</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
        </record>
        <record id="email_template_campaign_app_rejected" model="mail.template">
            <field name="name">Influencer: Campaign Application Update</field>
            <field name="model_id" ref="model_influence_gen_campaign_application"/>
            <field name="subject">Update on Your Application for "${object.campaign_id.name}"</field>
            <field name="email_from">"${object.campaign_id.company_id.email_formatted if object.campaign_id and object.campaign_id.company_id and object.campaign_id.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.influencer_profile_id.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Dear ${object.influencer_profile_id.full_name},</p>
                    <p>Thank you for your interest in the campaign "<strong>${object.campaign_id.name}</strong>".</p>
                    <p>After careful consideration, we regret to inform you that your application was not selected for this particular campaign at this time.</p>
                    <t t-if="ctx.get('rejection_reason')">
                        <p>Reason: ${ctx.get('rejection_reason')}</p>
                    </t>
                    <p>We receive many applications and selection can be very competitive. We encourage you to continue exploring and applying for other campaigns on our platform that match your profile.</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
        </record>


        <!-- REQ-16-005: Content Submission Feedback -->
        <record id="email_template_content_submission_approved" model="mail.template">
            <field name="name">Influencer: Content Submission Approved</field>
            <field name="model_id" ref="model_influence_gen_content_submission"/>
            <field name="subject">Great Work! Your Content for "${object.campaign_id.name}" is Approved!</field>
            <field name="email_from">"${object.campaign_id.company_id.email_formatted if object.campaign_id and object.campaign_id.company_id and object.campaign_id.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.influencer_profile_id.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Hi ${object.influencer_profile_id.full_name},</p>
                    <p>Excellent news! Your recent content submission (Version ${object.version}) for the campaign "<strong>${object.campaign_id.name}</strong>" has been approved.</p>
                    <p>Thank you for your contribution. Payment processing will be initiated according to the campaign terms.</p>
                    <p>Keep up the fantastic work!</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
        </record>
        <record id="email_template_content_submission_rejected" model="mail.template">
            <field name="name">Influencer: Content Submission Update (Rejected)</field>
            <field name="model_id" ref="model_influence_gen_content_submission"/>
            <field name="subject">Update on Your Content Submission for "${object.campaign_id.name}"</field>
            <field name="email_from">"${object.campaign_id.company_id.email_formatted if object.campaign_id and object.campaign_id.company_id and object.campaign_id.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.influencer_profile_id.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Hi ${object.influencer_profile_id.full_name},</p>
                    <p>This email is regarding your content submission (Version ${object.version}) for the campaign "<strong>${object.campaign_id.name}</strong>".</p>
                    <p>Unfortunately, this submission did not meet the campaign requirements and has been rejected.</p>
                    <t t-if="ctx.get('feedback_text')">
                        <p><strong>Feedback from our team:</strong></p>
                        <p style="border-left: 3px solid #ccc; padding-left: 10px; margin-left: 5px;"><em>${ctx.get('feedback_text')}</em></p>
                    </t>
                    <p>Please review the feedback carefully. Depending on campaign rules, you may be able to submit a revised version or this decision may be final for this submission. Check your portal for details.</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
        </record>
        <record id="email_template_content_submission_revision" model="mail.template">
            <field name="name">Influencer: Content Submission Revision Requested</field>
            <field name="model_id" ref="model_influence_gen_content_submission"/>
            <field name="subject">Revision Requested for Your Content on "${object.campaign_id.name}"</field>
            <field name="email_from">"${object.campaign_id.company_id.email_formatted if object.campaign_id and object.campaign_id.company_id and object.campaign_id.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.influencer_profile_id.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Hi ${object.influencer_profile_id.full_name},</p>
                    <p>We've reviewed your content submission (Version ${object.version}) for the campaign "<strong>${object.campaign_id.name}</strong>" and have requested some revisions.</p>
                    <t t-if="ctx.get('feedback_text')">
                        <p><strong>Feedback and requested changes:</strong></p>
                        <p style="border-left: 3px solid #ccc; padding-left: 10px; margin-left: 5px;"><em>${ctx.get('feedback_text')}</em></p>
                    </t>
                    <p>Please log in to your portal to view the full feedback and submit a revised version by the specified deadline.</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
        </record>
        
        <!-- REQ-16-015: Generic System Notifications (Example: AI Quota Reset) -->
        <record id="email_template_ai_quota_reset" model="mail.template">
            <field name="name">Influencer: AI Image Generation Quota Reset</field>
            <field name="model_id" ref="model_influence_gen_influencer_profile"/>
            <field name="subject">Your InfluenceGen AI Image Generation Quota Has Been Reset</field>
            <field name="email_from">"${object.company_id.email_formatted if object.company_id and object.company_id.email_formatted else user.company_id.email_formatted | safe}"</field>
            <field name="email_to">${object.email | safe}</field>
            <field name="body_html" type="html">
                <div style="font-family: Arial, sans-serif; font-size: 14px; color: #333;">
                    <p>Dear ${object.full_name},</p>
                    <p>Just a friendly reminder that your monthly AI image generation quota on the InfluenceGen platform has been reset for the new period.</p>
                    <p>You can now continue creating amazing visuals for your content!</p>
                    <p>Best regards,<br/>The InfluenceGen Team</p>
                </div>
            </field>
            <field name="user_signature" eval="False"/>
            <field name="auto_delete" eval="True"/>
        </record>

    </data>
</odoo>