# Specification

# 1. Alerting And Incident Response Analysis

- **System Overview:**
  
  - **Analysis Date:** 2024-07-26
  - **Technology Stack:**
    
    - Odoo 18
    - N8N
    - Python
    - PostgreSQL
    - Flux LoRA AI Models
    - REST APIs
    
  - **Metrics Configuration:**
    
    - SRS Section 6.1 Performance Requirements
    - SRS Section 6.4 Reliability Requirements
    - SRS Section 9.1 Logging, Monitoring, and Observability
    - SRS Section 9.2 Alerting
    
  - **Monitoring Needs:**
    
    - API Performance (Odoo-N8N, N8N-AI, N8N-Odoo Callback, External KYC/Payment)
    - AI Image Generation Pipeline (Success/Failure, Latency, Queue Depth)
    - System Resource Utilization (Odoo, N8N, AI Serving Instances - CPU, Memory, Disk, GPU)
    - Database Performance (Query Latency, Connections, Replication Lag)
    - KYC & Payment Processing Success/Failure Rates & Service Availability
    - Critical Workflow Failures (N8N, Odoo Callbacks)
    - Security Events (Failed Logins, Unauthorized Access Attempts)
    - Backup Job Status
    - SSL Certificate Health
    
  - **Environment:** production
  
- **Alert Condition And Threshold Design:**
  
  - **Critical Metrics Alerts:**
    
    - **Metric:** Odoo_N8N_API_Error_Rate  
**Condition:** Error rate > 5% over 5 minutes  
**Threshold Type:** static  
**Value:** 5%  
**Justification:** SRS 9.2: High API error rates. Ensures core integration stability.  
**Business Impact:** High - Prevents AI image generation requests.  
    - **Metric:** Odoo_N8N_API_P95_Latency  
**Condition:** P95 Latency > 1 second over 5 minutes  
**Threshold Type:** static  
**Value:** 1s  
**Justification:** SRS 9.2: Sustained latency increases. Impacts user experience for initiating AI gen.  
**Business Impact:** Medium - Slows down AI image generation initiation.  
    - **Metric:** N8N_AI_Service_API_Error_Rate  
**Condition:** Error rate > 10% over 10 minutes  
**Threshold Type:** static  
**Value:** 10%  
**Justification:** SRS 9.2: AI image generation service unavailability or persistent failures. Critical for AI feature.  
**Business Impact:** Critical - Prevents AI image generation.  
    - **Metric:** N8N_AI_Service_API_P95_Latency  
**Condition:** P95 Latency > 15 seconds over 10 minutes (excluding AI processing time, just API call latency)  
**Threshold Type:** static  
**Value:** 15s  
**Justification:** SRS 9.2: Sustained latency increases for AI service calls. Degrades AI gen performance.  
**Business Impact:** High - Significantly slows down AI image generation.  
    - **Metric:** N8N_Odoo_Callback_Error_Rate  
**Condition:** Error rate > 5% over 5 minutes  
**Threshold Type:** static  
**Value:** 5%  
**Justification:** SRS 9.2: N8N callback delivery failures to Odoo. Prevents results from reaching users.  
**Business Impact:** Critical - AI generation results lost or delayed.  
    - **Metric:** AI_Image_Generation_Failure_Rate  
**Condition:** Overall failure rate (Odoo to AI result) > 15% over 30 minutes  
**Threshold Type:** static  
**Value:** 15%  
**Justification:** SRS 9.1, 9.2: AI image generation success/failure rates. High failure rate indicates systemic issue.  
**Business Impact:** Critical - Core AI feature unusable for many users.  
    - **Metric:** AI_Image_Generation_P95_Total_Latency  
**Condition:** P95 End-to-end Latency (Odoo request to image available in Odoo) > 45 seconds over 15 minutes  
**Threshold Type:** static  
**Value:** 45s  
**Justification:** SRS 6.1, 9.2: AI image generation processing times. Exceeding target significantly impacts UX.  
**Business Impact:** High - Poor user experience for AI image generation.  
    - **Metric:** N8N_Workflow_Queue_Length  
**Condition:** Queue length > 100 pending AI generation requests for > 10 minutes  
**Threshold Type:** static  
**Value:** 100  
**Justification:** SRS 9.1: Queue lengths for asynchronous tasks. Indicates N8N processing bottleneck.  
**Business Impact:** Medium - Delays in AI image generation for users.  
    - **Metric:** Odoo_Server_CPU_Utilization  
**Condition:** CPU Utilization > 85% for > 15 minutes  
**Threshold Type:** static  
**Value:** 85%  
**Justification:** SRS 9.2: Critical resource thresholds breached. Indicates Odoo server overload.  
**Business Impact:** High - Platform slowdown or unavailability.  
    - **Metric:** Odoo_Server_Memory_Utilization  
**Condition:** Memory Utilization > 90% for > 15 minutes  
**Threshold Type:** static  
**Value:** 90%  
**Justification:** SRS 9.2: Critical resource thresholds breached. Risk of OOM errors.  
**Business Impact:** High - Platform instability or crashes.  
    - **Metric:** Odoo_Server_Disk_Space_Free  
**Condition:** Free Disk Space < 10% on critical volumes  
**Threshold Type:** static  
**Value:** 10%  
**Justification:** SRS 9.2: Low disk space. Can lead to data loss or service outage.  
**Business Impact:** Critical - Potential data loss or service unavailability.  
    - **Metric:** N8N_Server_CPU_Utilization  
**Condition:** CPU Utilization > 85% for > 15 minutes  
**Threshold Type:** static  
**Value:** 85%  
**Justification:** SRS 9.2: Critical resource thresholds breached. N8N overload affecting AI gen.  
**Business Impact:** High - AI generation pipeline slowdown or failure.  
    - **Metric:** AI_Serving_GPU_Utilization_Error  
**Condition:** GPU Utilization == 0% for > 5 minutes AND N8N AI queue length > 0  
**Threshold Type:** compound  
**Value:** 0% AND queue > 0  
**Justification:** SRS 9.1: GPU utilization. Indicates AI model serving is not processing requests.  
**Business Impact:** Critical - AI image generation completely stalled.  
    - **Metric:** PostgreSQL_Slow_Queries_Count  
**Condition:** Number of queries > 5 seconds in last 5 minutes > 10  
**Threshold Type:** static  
**Value:** >10  
**Justification:** SRS 9.1: Database performance metrics. Indicates DB performance issues.  
**Business Impact:** Medium - Platform slowdown for DB-intensive operations.  
    - **Metric:** PostgreSQL_Connections_Max_Reached  
**Condition:** Active connections > 90% of max_connections for > 5 minutes  
**Threshold Type:** static  
**Value:** 90%  
**Justification:** SRS 9.1, 9.2: Database connection issues. Risk of DB unavailability.  
**Business Impact:** High - Platform features may fail due to DB connection exhaustion.  
    - **Metric:** KYC_Service_Error_Rate  
**Condition:** Error rate for external KYC service calls > 20% over 15 minutes  
**Threshold Type:** static  
**Value:** 20%  
**Justification:** SRS 9.2: KYC verification service outages or high failure rates. Blocks influencer onboarding.  
**Business Impact:** High - Prevents new influencer onboarding.  
    - **Metric:** Payment_Processing_Failure_Rate  
**Condition:** Failure rate for payment processing > 10% over 1 hour  
**Threshold Type:** static  
**Value:** 10%  
**Justification:** SRS 9.2: Payment processing failures. Impacts influencer payouts.  
**Business Impact:** Critical - Influencers not paid, legal/reputational risk.  
    - **Metric:** N8N_Critical_Workflow_Failure_Count  
**Condition:** Execution failure count for critical workflow 'X' > 3 in 1 hour  
**Threshold Type:** static  
**Value:** 3  
**Justification:** SRS 9.2: N8N workflow execution failures for critical processes. Impacts specific business logic.  
**Business Impact:** Varies (Medium to High) - Depends on workflow, e.g., campaign status updates.  
    - **Metric:** Odoo_Backup_Job_Failure  
**Condition:** Last backup job status == FAILED  
**Threshold Type:** static  
**Value:** FAILED  
**Justification:** SRS 9.2: Backup job failures. Risk of data loss (violates RPO).  
**Business Impact:** Critical - Increased risk of data loss in disaster.  
    - **Metric:** SSL_Certificate_Expiry_Warning  
**Condition:** Certificate for critical endpoint expires in < 14 days  
**Threshold Type:** static  
**Value:** <14d  
**Justification:** SRS 9.2: SSL certificate expiry warnings. Prevents service disruption.  
**Business Impact:** High (if expires) - Service becomes inaccessible or insecure.  
    - **Metric:** Admin_Failed_Login_Attempts  
**Condition:** Number of failed login attempts for any admin account > 5 in 15 minutes from same IP  
**Threshold Type:** static  
**Value:** 5  
**Justification:** SRS 9.2: Multiple failed login attempts for admin accounts. Potential brute-force attack.  
**Business Impact:** Critical - Potential security breach.  
    
  - **Threshold Strategies:**
    
    - **Strategy:** static  
**Applicable Metrics:**
    
    - Most defined above, based on NFRs or operational stability targets
    
**Implementation:** Fixed values defined in monitoring configuration.  
**Advantages:**
    
    - Simple to implement
    - Clear pass/fail criteria
    
    - **Strategy:** baseline-deviation  
**Applicable Metrics:**
    
    - Odoo_UI_Page_Load_Time_P95
    - User_Registration_Rate
    - Campaign_Application_Rate
    
**Implementation:** Monitor collects data for a period (e.g., 7 days) to establish a baseline, then alerts if current values deviate significantly (e.g., > 3 std deviations or > 50% from hourly/daily baseline).  
**Advantages:**
    
    - Adapts to normal fluctuations
    - Catches unusual changes not covered by static thresholds
    
    
  - **Baseline Deviation Alerts:**
    
    - **Metric:** Odoo_UI_Page_Load_Time_P95_Baseline_Deviation  
**Baseline Period:** 7 days (rolling, excluding maintenance windows)  
**Deviation Percentage:** 50% increase from hourly baseline, sustained for 10 mins  
**Minimum Samples:** 100  
**Seasonal Adjustment:** True  
    
  - **Predictive Alerts:**
    
    - **Metric:** Odoo_Server_Disk_Space_Free_Predictive  
**Prediction Window:** 7 days  
**Confidence Threshold:** 90%  
**Algorithm:** Linear Regression or Time Series Forecasting  
**Training Period:** 30 days  
    
  - **Compound Conditions:**
    
    - **Name:** AI_Service_Stalled  
**Conditions:**
    
    - AI_Serving_GPU_Utilization_Error (GPU Util 0%)
    - N8N_Workflow_Queue_Length (>0)
    
**Logic:** AND  
**Time Window:** 5 minutes  
**Justification:** If GPU is idle but there are jobs queued, AI processing is stuck.  
    - **Name:** Admin_Account_Brute_Force_Suspected  
**Conditions:**
    
    - Admin_Failed_Login_Attempts (>5 from same IP for one admin)
    - Multiple_Admin_Failed_Logins_Different_Accounts_Same_IP (>3 distinct admin accounts from same IP in 15 mins)
    
**Logic:** OR  
**Time Window:** 15 minutes  
**Justification:** Detects targeted attack on one admin or broader attempt across multiple admins from one source.  
    
  
- **Severity Level Classification:**
  
  - **Severity Definitions:**
    
    - **Level:** Critical  
**Criteria:** System-wide outage, critical feature unavailability (e.g., AI Gen, Payments, Onboarding), significant data loss/corruption risk, security breach in progress or imminent.  
**Business Impact:** Major financial loss, severe reputational damage, legal/compliance failure, loss of user trust.  
**Customer Impact:** Majority of users unable to use core platform features. Data at risk.  
**Response Time:** Immediate (within 5-15 minutes acknowledgment, start investigation)  
**Escalation Required:** True  
    - **Level:** High  
**Criteria:** Significant feature degradation, partial service interruption, important NFR violation (e.g., performance targets consistently missed), potential security vulnerability.  
**Business Impact:** Moderate financial loss, reputational damage, user dissatisfaction.  
**Customer Impact:** Significant portion of users impacted, key workflows are slow or error-prone.  
**Response Time:** Within 30-60 minutes acknowledgment  
**Escalation Required:** True  
    - **Level:** Medium  
**Criteria:** Minor feature impairment, non-critical NFR deviation, isolated errors, early warning of potential issues.  
**Business Impact:** Minor financial impact, minor user inconvenience.  
**Customer Impact:** Some users experience minor issues or slowness with non-critical features.  
**Response Time:** Within 2-4 hours acknowledgment  
**Escalation Required:** False  
    - **Level:** Low  
**Criteria:** Informational, minor deviations, non-impacting errors, resource usage nearing warning thresholds.  
**Business Impact:** Negligible.  
**Customer Impact:** No direct customer impact, or very isolated minor inconvenience.  
**Response Time:** Within 1 business day  
**Escalation Required:** False  
    
  - **Business Impact Matrix:**
    
    - **Impact Type:** revenue  
**Severity Mapping:** Direct loss of revenue (e.g. payment failure) -> Critical; Impeded campaign creation -> High  
**Time To Detection:** <15 min (Critical), <1hr (High)  
**Time To Resolution:** RTO (4 hours) or less for Critical; <8 hrs for High  
    - **Impact Type:** customer  
**Severity Mapping:** Platform Unavailability -> Critical; AI Gen Failure -> Critical; KYC Failure -> High; Slow UI -> Medium  
**Time To Detection:** <15 min (Critical), <1hr (High)  
**Time To Resolution:** RTO for Critical; SLA dependent for others  
    - **Impact Type:** reputation  
**Severity Mapping:** Data Breach -> Critical; Major Outage -> Critical; Payment Issues -> High  
**Time To Detection:** Immediate  
**Time To Resolution:** ASAP, ongoing communication  
    - **Impact Type:** compliance  
**Severity Mapping:** GDPR Violation -> Critical; Audit Log Failure -> High  
**Time To Detection:** Immediate  
**Time To Resolution:** ASAP, legal involvement  
    
  - **Customer Impact Criteria:**
    
    - **Impact Level:** severe  
**User Percentage:** >50% or all admin users  
**Functionality Affected:**
    
    - Core platform access
    - AI Image Generation
    - Payment Processing
    - Onboarding
    
**Severity Level:** Critical  
    - **Impact Level:** significant  
**User Percentage:** 10-50%  
**Functionality Affected:**
    
    - Campaign Management
    - Content Submission
    - Performance Tracking
    
**Severity Level:** High  
    - **Impact Level:** moderate  
**User Percentage:** <10% or non-critical features  
**Functionality Affected:**
    
    - Profile Management (non-critical fields)
    - System Administration (non-critical settings)
    
**Severity Level:** Medium  
    
  - **Sla Violation Severity:**
    
    - **Sla Type:** availability  
**Threshold Breach:** Uptime < 99.9% (calculated monthly)  
**Severity Level:** High (if approaching SLA limit), Critical (if breached for extended period)  
**Escalation Trigger:** Projection indicates SLA miss OR actual breach.  
    - **Sla Type:** performance  
**Threshold Breach:** AI Gen P95 Latency > 45s sustained  
**Severity Level:** High  
**Escalation Trigger:** Sustained breach for >1 hour.  
    - **Sla Type:** RPO  
**Threshold Breach:** Last successful backup older than 1 hour AND backup failure alert  
**Severity Level:** Critical  
**Escalation Trigger:** Backup failure alert.  
    - **Sla Type:** RTO  
**Threshold Breach:** System recovery estimated or actual time > 4 hours during an incident  
**Severity Level:** Critical  
**Escalation Trigger:** During DRP execution if projected RTO will be missed.  
    
  - **System Health Severity:**
    
    - **Health Indicator:** Odoo Application Server Cluster Health  
**Degradation Level:** One or more nodes unresponsive / high error rate  
**Severity Mapping:** High/Critical depending on redundancy and impact  
**Automated Response:** Attempt auto-restart of failed node (if configured)  
    - **Health Indicator:** N8N Service Health  
**Degradation Level:** Unresponsive or consistently failing workflows  
**Severity Mapping:** Critical (if AI gen impacted)  
**Automated Response:** Attempt N8N service restart (if configured)  
    - **Health Indicator:** AI Model Serving Infrastructure Health  
**Degradation Level:** High error rate from AI models or service unresponsive  
**Severity Mapping:** Critical  
**Automated Response:** Attempt AI service/model reload (if configured)  
    
  
- **Notification Channel Strategy:**
  
  - **Channel Configuration:**
    
    - **Channel:** email  
**Purpose:** General alerting, non-urgent notifications, daily summaries.  
**Applicable Severities:**
    
    - Low
    - Medium
    - High
    - Critical
    
**Time Constraints:** 24/7  
**Configuration:**
    
    - **Smtp Server:** org_smtp.example.com
    - **Default Recipient List:** devops@example.com, support@example.com
    
    - **Channel:** sms  
**Purpose:** Urgent notifications for on-call personnel for Critical alerts.  
**Applicable Severities:**
    
    - Critical
    
**Time Constraints:** 24/7  
**Configuration:**
    
    - **Gateway Provider:** Twilio/Vonage
    - **On Call Rotation Integration:** True
    
    - **Channel:** slack  
**Purpose:** Real-time alerting for teams, collaborative incident response.  
**Applicable Severities:**
    
    - Medium
    - High
    - Critical
    
**Time Constraints:** Business Hours (for Medium), 24/7 (for High/Critical)  
**Configuration:**
    
    - **Webhook Url:** slack_webhook_url
    - **Default Channel:** #alerts-influencegen
    
    - **Channel:** pagerduty  
**Purpose:** Primary on-call notification and escalation management for Critical and High alerts.  
**Applicable Severities:**
    
    - High
    - Critical
    
**Time Constraints:** 24/7  
**Configuration:**
    
    - **Integration Key:** pagerduty_integration_key
    - **Service Name:** InfluenceGen Platform
    
    
  - **Routing Rules:**
    
    - **Condition:** Severity == Critical  
**Severity:** Critical  
**Alert Type:** Any  
**Channels:**
    
    - pagerduty
    - sms
    - slack
    - email
    
**Priority:** 1  
    - **Condition:** Severity == High  
**Severity:** High  
**Alert Type:** Any  
**Channels:**
    
    - pagerduty
    - slack
    - email
    
**Priority:** 2  
    - **Condition:** Severity == Medium  
**Severity:** Medium  
**Alert Type:** Any  
**Channels:**
    
    - slack
    - email
    
**Priority:** 3  
    - **Condition:** Severity == Low  
**Severity:** Low  
**Alert Type:** Any  
**Channels:**
    
    - email
    
**Priority:** 4  
    - **Condition:** AlertSource == SecurityMonitoring && Severity IN (High, Critical)  
**Severity:** High/Critical  
**Alert Type:** Security  
**Channels:**
    
    - pagerduty_security_team
    - slack_security_channel
    - email_security_dl
    
**Priority:** 0  
    
  - **Time Based Routing:**
    
    - **Time Window:** Non-Business Hours (e.g., 18:00-08:00 Local Time, Weekends)  
**Timezone:** Configurable (e.g., UTC, local to support team)  
**Channels:**
    
    - pagerduty
    - sms
    
**Fallback Channels:**
    
    - email
    
    
  - **Ticketing Integration:**
    
    - **System:** Jira Service Management (or Odoo Helpdesk)  
**Trigger Conditions:**
    
    - Severity IN (Critical, High, Medium) AND IsNewIncident
    
**Ticket Priority:** Matches Alert Severity  
**Auto Assignment:** True  
    
  - **Emergency Notifications:**
    
    - **Trigger:** Manual trigger by Incident Commander for Major Incidents (e.g., DRP activation)  
**Channels:**
    
    - sms
    - voice_call_system
    - email_all_stakeholders
    
**Recipients:**
    
    - CrisisManagementTeam
    - ExecutiveLeadership
    - AllEmployees (if broad impact)
    
**Escalation Path:**
    
    - Defined in BCP/DRP
    
    
  - **Chat Platform Integration:**
    
    - **Platform:** slack  
**Channels:**
    
    - #alerts-influencegen-critical
    - #alerts-influencegen-high
    - #alerts-influencegen-medium
    
**Bot Integration:** True  
**Thread Management:** Create new thread for each distinct incident, post updates in thread.  
    
  
- **Alert Correlation Implementation:**
  
  - **Grouping Requirements:**
    
    - **Grouping Criteria:** Same source component (e.g., Odoo Server X) AND similar error type occurring within short time window.  
**Time Window:** 5 minutes  
**Max Group Size:** 10  
**Suppression Strategy:** Group into single incident, increment count.  
    - **Grouping Criteria:** Alerts related to a single distributed trace (via Correlation ID).  
**Time Window:** 15 minutes (trace lifetime)  
**Max Group Size:** 0  
**Suppression Strategy:** Correlate under a parent incident representing the user-facing impact.  
    
  - **Parent Child Relationships:**
    
    - **Parent Condition:** AI_Service_Unresponsive (High error rate from N8N_AI_Service_API_Error_Rate)  
**Child Conditions:**
    
    - AI_Image_Generation_Failure_Rate (High)
    - N8N_Workflow_Queue_Length (Increasing)
    
**Suppression Duration:** While parent alert is active  
**Propagation Rules:** Child alerts are linked to parent incident, notifications for children might be suppressed if parent is acknowledged.  
    
  - **Topology Based Correlation:**
    
    - **Component:** PostgreSQL Primary DB Server  
**Dependencies:**
    
    - Odoo Application Servers
    - N8N (if it uses Odoo DB directly for some state)
    
**Correlation Rules:**
    
    - If DB server is down, suppress 'Odoo App Server Cannot Connect to DB' alerts and correlate under 'DB Down' incident.
    
**Impact Analysis:** High (DB down impacts entire platform)  
    
  - **Time Window Correlation:**
    
    - **Correlation Window:** 2 minutes  
**Similarity Threshold:** High (e.g., same error message pattern from multiple app servers)  
**Deduplication Strategy:** Consolidate into one alert, update count/affected hosts.  
    
  - **Causal Relationship Detection:**
    
    - **Cause Metric:** Low_Disk_Space_Free (on DB Server)  
**Effect Metrics:**
    
    - PostgreSQL_Slow_Queries_Count (High)
    - PostgreSQL_Replication_Lag (High)
    
**Detection Window:** 10 minutes  
**Confidence Threshold:** 80%  
    
  - **Maintenance Window Suppression:**
    
    - **Maintenance Type:** Scheduled System Maintenance (Odoo, N8N, DB, AI Service)  
**Suppression Scope:**
    
    - Affected components/services defined in maintenance plan
    
**Automatic Detection:** True  
**Manual Override:** True  
    
  
- **False Positive Mitigation:**
  
  - **Noise Reduction Strategies:**
    
    - **Strategy:** Alert Tuning  
**Implementation:** Regular review of alert thresholds and conditions based on historical performance and incident data.  
**Applicable Alerts:**
    
    - All
    
**Effectiveness:** High  
    - **Strategy:** Dependency Checking  
**Implementation:** Before firing an alert for an application error, check health of its critical dependencies (e.g., database, external service). If dependency is down, suppress app error or link to dependency issue.  
**Applicable Alerts:**
    
    - API_Error_Rate
    - Workflow_Failure_Count
    
**Effectiveness:** Medium  
    
  - **Confirmation Counts:**
    
    - **Alert Type:** Resource_Utilization_Spike (e.g. CPU momentary spike)  
**Confirmation Threshold:** 3  
**Confirmation Window:** 5 minutes  
**Reset Condition:** Metric returns below threshold for 1 polling cycle.  
    
  - **Dampening And Flapping:**
    
    - **Metric:** Network_Interface_Flapping (Up/Down repeatedly)  
**Dampening Period:** 10 minutes (suppress further alerts if flapping detected)  
**Flapping Threshold:** 5  
**Suppression Duration:** 30 minutes (or until stable)  
    
  - **Alert Validation:**
    
    - **Validation Type:** health-probe  
**Validation Logic:** For 'Service Unresponsive' alerts, monitoring system performs an independent health check (e.g., synthetic transaction) before escalating.  
**Timeout Duration:** 30 seconds  
**Fallback Action:** If probe also fails, escalate alert. If probe succeeds, log potential transient issue but do not escalate.  
    
  - **Smart Filtering:**
    
    - **Filter Type:** anomaly-detection (for metrics without clear static thresholds)  
**Implementation:** ML-based anomaly detection service integrated with monitoring.  
**Learning Period:** 14-30 days  
**Accuracy:** Target >85% precision  
    
  - **Quorum Based Alerting:**
    
    - **Alert Type:** Odoo_Cluster_Node_Unhealthy  
**Quorum Size:** 3  
**Agreement Threshold:** 2 out of 3  
**Participant Sources:**
    
    - Different monitoring agents in different AZs
    
    
  
- **On Call Management Integration:**
  
  - **Escalation Paths:**
    
    - **Severity:** Critical  
**Escalation Levels:**
    
    - **Level:** 0  
**Recipients:**
    
    - Primary On-Call (PagerDuty Schedule - L1/L2)
    
**Escalation Time:** 0 minutes (Immediate)  
**Requires Acknowledgment:** True  
    - **Level:** 1  
**Recipients:**
    
    - Secondary On-Call (PagerDuty Schedule - L2/L3)
    
**Escalation Time:** 15 minutes (if unacked)  
**Requires Acknowledgment:** True  
    - **Level:** 2  
**Recipients:**
    
    - Support Manager/Team Lead
    
**Escalation Time:** 30 minutes (if unacked)  
**Requires Acknowledgment:** True  
    
**Ultimate Escalation:** Head of Engineering / CTO  
    - **Severity:** High  
**Escalation Levels:**
    
    - **Level:** 0  
**Recipients:**
    
    - Primary On-Call (PagerDuty Schedule - L1/L2)
    
**Escalation Time:** 0 minutes (Immediate)  
**Requires Acknowledgment:** True  
    - **Level:** 1  
**Recipients:**
    
    - Secondary On-Call (PagerDuty Schedule - L2/L3)
    
**Escalation Time:** 30 minutes (if unacked)  
**Requires Acknowledgment:** True  
    
**Ultimate Escalation:** Support Manager/Team Lead  
    
  - **Escalation Timeframes:**
    
    - **Severity:** Critical  
**Initial Response:** 5-15 minutes (acknowledge)  
**Escalation Interval:** 15 minutes per level  
**Max Escalations:** 3  
    - **Severity:** High  
**Initial Response:** 30-60 minutes (acknowledge)  
**Escalation Interval:** 30 minutes per level  
**Max Escalations:** 2  
    
  - **On Call Rotation:**
    
    - **Team:** Platform Operations (L1/L2)  
**Rotation Type:** weekly  
**Handoff Time:** Monday 09:00 Local Time  
**Backup Escalation:** Secondary on-call from same team, then L3/Dev team.  
    - **Team:** Development (L3)  
**Rotation Type:** weekly (for specific critical services)  
**Handoff Time:** Monday 09:00 Local Time  
**Backup Escalation:** Development Team Lead  
    
  - **Acknowledgment Requirements:**
    
    - **Severity:** Critical  
**Acknowledgment Timeout:** 15 minutes  
**Auto Escalation:** True  
**Requires Comment:** True  
    - **Severity:** High  
**Acknowledgment Timeout:** 30 minutes  
**Auto Escalation:** True  
**Requires Comment:** False  
    
  - **Incident Ownership:**
    
    - **Assignment Criteria:** Based on service affected and on-call schedule (auto-assigned by PagerDuty).  
**Ownership Transfer:** Formal handoff procedure if primary assignee changes shift or escalates.  
**Tracking Mechanism:** Incident Management System (Jira/PagerDuty)  
    
  - **Follow The Sun Support:**
    
    - **Region:** APAC, EMEA, AMER (Illustrative)  
**Coverage Hours:** Respective regional business hours, with global on-call for out-of-hours Critical/High.  
**Handoff Procedure:** Daily handoff meetings, shared incident tracking system.  
**Escalation Override:** Global Incident Manager can override regional escalation.  
    
  
- **Project Specific Alerts Config:**
  
  - **Alerts:**
    
    - **Name:** High_Odoo_N8N_API_Error_Rate  
**Description:** Error rate for Odoo to N8N API calls is above 5% for 5 minutes.  
**Condition:** avg(rate(odoo_n8n_api_errors[5m])) > 0.05  
**Threshold:** 5%  
**Severity:** High  
**Channels:**
    
    - pagerduty
    - slack
    - email
    
**Correlation:**
    
    - **Group Id:** odoo_n8n_integration
    - **Suppression Rules:**
      
      - During N8N_Maintenance_Window
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 30m
    - **Escalation Path:**
      
      - High Severity Path
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** True
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 2
    - **Confirmation Window:** 2m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** runbooks/odoo_n8n_api_errors.md
    - **Troubleshooting Steps:**
      
      - Check N8N service status.
      - Review Odoo logs for request details.
      - Review N8N logs for error messages.
      
    
    - **Name:** High_N8N_AI_Service_API_Error_Rate  
**Description:** Error rate for N8N to AI Service API calls is above 10% for 10 minutes.  
**Condition:** avg(rate(n8n_ai_api_errors[10m])) > 0.10  
**Threshold:** 10%  
**Severity:** Critical  
**Channels:**
    
    - pagerduty
    - sms
    - slack
    - email
    
**Correlation:**
    
    - **Group Id:** n8n_ai_integration
    - **Suppression Rules:**
      
      - During AI_Service_Maintenance_Window
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - Critical Severity Path
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** True
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 3
    - **Confirmation Window:** 5m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** runbooks/n8n_ai_api_errors.md
    - **Troubleshooting Steps:**
      
      - Check AI Service status page.
      - Review N8N logs for AI service error details.
      - Verify API keys and quotas for AI service.
      
    
    - **Name:** High_N8N_Odoo_Callback_Error_Rate  
**Description:** Error rate for N8N to Odoo Callback API calls is above 5% for 5 minutes.  
**Condition:** avg(rate(n8n_odoo_callback_errors[5m])) > 0.05  
**Threshold:** 5%  
**Severity:** Critical  
**Channels:**
    
    - pagerduty
    - sms
    - slack
    - email
    
**Correlation:**
    
    - **Group Id:** n8n_odoo_integration
    - **Suppression Rules:**
      
      - During Odoo_Maintenance_Window
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - Critical Severity Path
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** True
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 2
    - **Confirmation Window:** 2m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** runbooks/n8n_odoo_callback_errors.md
    - **Troubleshooting Steps:**
      
      - Check Odoo service status.
      - Review N8N logs for callback error details.
      - Review Odoo logs for callback processing errors.
      
    
    - **Name:** High_AI_Image_Generation_P95_Latency  
**Description:** P95 end-to-end latency for AI image generation exceeds 45 seconds over 15 minutes.  
**Condition:** percentile_95(ai_image_gen_latency[15m]) > 45s  
**Threshold:** 45s  
**Severity:** High  
**Channels:**
    
    - pagerduty
    - slack
    - email
    
**Correlation:**
    
    - **Group Id:** ai_performance
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 30m
    - **Escalation Path:**
      
      - High Severity Path
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 3
    - **Confirmation Window:** 5m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** runbooks/ai_gen_latency.md
    - **Troubleshooting Steps:**
      
      - Analyze latency breakdown: Odoo->N8N, N8N processing, AI service, N8N->Odoo callback.
      - Check resource utilization on all components.
      
    
    - **Name:** Odoo_Server_High_CPU  
**Description:** Odoo server CPU utilization is above 85% for 15 minutes.  
**Condition:** avg(odoo_cpu_util[15m]) > 85  
**Threshold:** 85%  
**Severity:** High  
**Channels:**
    
    - pagerduty
    - slack
    - email
    
**Correlation:**
    
    - **Group Id:** odoo_resources
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 30m
    - **Escalation Path:**
      
      - High Severity Path
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 0m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** runbooks/odoo_high_cpu.md
    - **Troubleshooting Steps:**
      
      - Identify top CPU consuming Odoo processes.
      - Check for long-running queries or inefficient code.
      - Consider scaling Odoo resources if persistent.
      
    
    - **Name:** Odoo_Server_Low_Disk_Space  
**Description:** Free disk space on Odoo server critical volume is less than 10%.  
**Condition:** odoo_disk_free_percent < 10  
**Threshold:** 10%  
**Severity:** Critical  
**Channels:**
    
    - pagerduty
    - sms
    - slack
    - email
    
**Correlation:**
    
    - **Group Id:** odoo_resources
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - Critical Severity Path
      
    
**Suppression:**
    
    - **Maintenance Window:** False
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 0m
    
**Remediation:**
    
    - **Automated Actions:**
      
      - Attempt automated cleanup of old logs/temp files (if safe script exists)
      
    - **Runbook Url:** runbooks/odoo_low_disk.md
    - **Troubleshooting Steps:**
      
      - Identify large files/directories.
      - Archive or delete unnecessary data.
      - Increase disk capacity.
      
    
    - **Name:** PostgreSQL_High_Connection_Usage  
**Description:** PostgreSQL active connections are above 90% of max_connections for 5 minutes.  
**Condition:** avg(pgsql_connections_percent[5m]) > 90  
**Threshold:** 90%  
**Severity:** High  
**Channels:**
    
    - pagerduty
    - slack
    - email
    
**Correlation:**
    
    - **Group Id:** db_performance
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 30m
    - **Escalation Path:**
      
      - High Severity Path
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 0m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** runbooks/pgsql_high_connections.md
    - **Troubleshooting Steps:**
      
      - Identify sources of high connections (application, long queries).
      - Optimize connection pooling in Odoo.
      - Consider increasing max_connections if appropriate.
      
    
    - **Name:** Odoo_Backup_Failure  
**Description:** The last Odoo database backup job failed.  
**Condition:** odoo_backup_status == FAILED  
**Threshold:** FAILED  
**Severity:** Critical  
**Channels:**
    
    - pagerduty
    - sms
    - slack
    - email
    
**Correlation:**
    
    - **Group Id:** backup_status
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 15m
    - **Escalation Path:**
      
      - Critical Severity Path
      
    
**Suppression:**
    
    - **Maintenance Window:** False
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 0m
    
**Remediation:**
    
    - **Automated Actions:**
      
      - Attempt automated re-run of backup job (1 attempt)
      
    - **Runbook Url:** runbooks/odoo_backup_failure.md
    - **Troubleshooting Steps:**
      
      - Review backup logs for error details.
      - Ensure backup destination is available and has space.
      - Manually trigger backup after resolving issue.
      
    
    - **Name:** KYC_Service_Outage  
**Description:** Error rate for external KYC service calls is above 20% for 15 minutes.  
**Condition:** avg(rate(kyc_service_errors[15m])) > 0.20  
**Threshold:** 20%  
**Severity:** High  
**Channels:**
    
    - pagerduty
    - slack
    - email
    
**Correlation:**
    
    - **Group Id:** external_services
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 30m
    - **Escalation Path:**
      
      - High Severity Path
      
    
**Suppression:**
    
    - **Maintenance Window:** True
    - **Dependency Failure:** False
    - **Manual Override:** True
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 0m
    
**Remediation:**
    
    - **Automated Actions:**
      
      
    - **Runbook Url:** runbooks/kyc_service_outage.md
    - **Troubleshooting Steps:**
      
      - Check KYC provider status page.
      - Verify API credentials and connectivity.
      - Notify stakeholders about onboarding impact.
      
    
    - **Name:** Admin_Account_Multiple_Failed_Logins  
**Description:** More than 5 failed login attempts for an admin account from the same IP in 15 minutes.  
**Condition:** count(admin_failed_logins_same_ip[15m]) > 5  
**Threshold:** 5 attempts  
**Severity:** Critical  
**Channels:**
    
    - pagerduty_security_team
    - slack_security_channel
    - email_security_dl
    
**Correlation:**
    
    - **Group Id:** security_incidents
    - **Suppression Rules:**
      
      
    
**Escalation:**
    
    - **Enabled:** True
    - **Escalation Time:** 5m
    - **Escalation Path:**
      
      - Security Critical Path
      
    
**Suppression:**
    
    - **Maintenance Window:** False
    - **Dependency Failure:** False
    - **Manual Override:** False
    
**Validation:**
    
    - **Confirmation Count:** 1
    - **Confirmation Window:** 0m
    
**Remediation:**
    
    - **Automated Actions:**
      
      - Temporarily block IP at firewall if feasible and pattern is clear (requires careful implementation)
      
    - **Runbook Url:** runbooks/security_admin_failed_logins.md
    - **Troubleshooting Steps:**
      
      - Investigate source IP reputation.
      - Review audit logs for affected admin account.
      - Contact admin user if known activity.
      - Consider enforcing MFA for admins if not already.
      
    
    
  - **Alert Groups:**
    
    - **Group Id:** odoo_n8n_integration  
**Name:** Odoo-N8N Core Integration  
**Alerts:**
    
    - High_Odoo_N8N_API_Error_Rate
    - High_N8N_Odoo_Callback_Error_Rate
    
**Suppression Strategy:** If Odoo_Maintenance_Window OR N8N_Maintenance_Window  
**Escalation Override:** Default  
    - **Group Id:** n8n_ai_integration  
**Name:** N8N-AI Service Integration  
**Alerts:**
    
    - High_N8N_AI_Service_API_Error_Rate
    
**Suppression Strategy:** If AI_Service_Maintenance_Window  
**Escalation Override:** Default  
    - **Group Id:** odoo_resources  
**Name:** Odoo Server Resources  
**Alerts:**
    
    - Odoo_Server_High_CPU
    - Odoo_Server_Low_Disk_Space
    
**Suppression Strategy:** If Odoo_Maintenance_Window  
**Escalation Override:** Default  
    - **Group Id:** db_performance  
**Name:** Database Performance  
**Alerts:**
    
    - PostgreSQL_High_Connection_Usage
    
**Suppression Strategy:** If DB_Maintenance_Window  
**Escalation Override:** Default  
    - **Group Id:** security_incidents  
**Name:** Security Incidents  
**Alerts:**
    
    - Admin_Account_Multiple_Failed_Logins
    
**Suppression Strategy:** None  
**Escalation Override:** Security_Escalation_Path  
    
  - **Notification Templates:**
    
    - **Template Id:** default_critical_email  
**Channel:** email  
**Format:** Subject: CRITICAL Alert: {{AlertName}} on {{Host/Service}}

Severity: CRITICAL
Alert: {{AlertName}}
Description: {{AlertDescription}}
Condition: {{AlertCondition}}
Timestamp: {{TimestampUTC}}

Runbook: {{RunbookURL}}

Please acknowledge and investigate immediately via PagerDuty: {{PagerDutyLink}}  
**Variables:**
    
    - AlertName
    - Host/Service
    - AlertDescription
    - AlertCondition
    - TimestampUTC
    - RunbookURL
    - PagerDutyLink
    
    - **Template Id:** default_slack_critical  
**Channel:** slack  
**Format:** :rotating_light: *CRITICAL Alert: {{AlertName}}* :rotating_light:
*Service/Host:* `{{Host/Service}}`
*Description:* {{AlertDescription}}
*Condition Met:* `{{AlertCondition}}`
*Runbook:* <{{RunbookURL}}|View Runbook>
*PagerDuty:* <{{PagerDutyLink}}|Acknowledge/View Incident>  
**Variables:**
    
    - AlertName
    - Host/Service
    - AlertDescription
    - AlertCondition
    - RunbookURL
    - PagerDutyLink
    
    - **Template Id:** default_sms_critical  
**Channel:** sms  
**Format:** CRITICAL: {{AlertName}} on {{Host/Service}}. Ack in PagerDuty: {{PagerDutyShortLink}}  
**Variables:**
    
    - AlertName
    - Host/Service
    - PagerDutyShortLink
    
    
  
- **Implementation Priority:**
  
  - **Component:** Critical API Endpoint Monitoring (Odoo-N8N, N8N-AI, N8N-Odoo)  
**Priority:** high  
**Dependencies:**
    
    - Centralized Logging
    - Monitoring System Setup
    
**Estimated Effort:** 5 days  
**Risk Level:** low  
  - **Component:** AI Generation Pipeline Health (Success/Failure, Latency)  
**Priority:** high  
**Dependencies:**
    
    - Centralized Logging
    - Monitoring System Setup
    
**Estimated Effort:** 5 days  
**Risk Level:** medium  
  - **Component:** Core System Resource Monitoring (Odoo, N8N, DB, AI Serving)  
**Priority:** high  
**Dependencies:**
    
    - Monitoring System Setup
    
**Estimated Effort:** 3 days  
**Risk Level:** low  
  - **Component:** Backup Failure Alerting  
**Priority:** high  
**Dependencies:**
    
    - Backup System Integration with Monitoring
    
**Estimated Effort:** 2 days  
**Risk Level:** low  
  - **Component:** Security Alerting (Admin Failed Logins)  
**Priority:** high  
**Dependencies:**
    
    - Audit Log Analysis Capability
    
**Estimated Effort:** 3 days  
**Risk Level:** medium  
  - **Component:** PagerDuty Integration & Escalation Path Setup  
**Priority:** high  
**Dependencies:**
    
    - Alerting System Chosen
    
**Estimated Effort:** 3 days  
**Risk Level:** low  
  - **Component:** Maintenance Window Suppression Logic  
**Priority:** medium  
**Dependencies:**
    
    - Alerting System
    - Change Management Process/Tool
    
**Estimated Effort:** 4 days  
**Risk Level:** medium  
  
- **Risk Assessment:**
  
  - **Risk:** Alert Fatigue due to excessive or poorly tuned alerts.  
**Impact:** high  
**Probability:** high  
**Mitigation:** Strict criteria for new alerts, regular tuning, tiered severity, effective correlation and suppression, actionable alerts only.  
**Contingency Plan:** Dedicated alert review meetings, implement 'quiet hours' for non-critical alerts, progressively disable noisy alerts.  
  - **Risk:** Monitoring/Alerting system failure.  
**Impact:** critical  
**Probability:** low  
**Mitigation:** Monitor the monitor (e.g., dead man's snitch), redundant monitoring components if feasible, regular health checks of monitoring system.  
**Contingency Plan:** Fallback to manual checks of key system health indicators, expedited repair of monitoring system.  
  - **Risk:** False positives leading to wasted effort.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Thorough testing of alert conditions, use of confirmation counts, alert validation mechanisms, feedback loop from on-call to tune alerts.  
**Contingency Plan:** Document common false positive scenarios and their resolution, refine alert logic.  
  - **Risk:** False negatives (missed critical incidents).  
**Impact:** critical  
**Probability:** medium  
**Mitigation:** Comprehensive metric coverage based on SRS, regular review of incident root causes for missed alerting opportunities, defense-in-depth monitoring.  
**Contingency Plan:** Post-incident review to identify gaps and add/improve alerts.  
  - **Risk:** Incorrect escalation or notification routing.  
**Impact:** high  
**Probability:** low  
**Mitigation:** Clear documentation of on-call schedules and escalation paths, regular testing of notification channels and PagerDuty rules.  
**Contingency Plan:** Manual escalation by incident commander or first responder if automated routing fails.  
  
- **Recommendations:**
  
  - **Category:** Alert Design  
**Recommendation:** Ensure every alert is actionable and linked to a documented runbook or troubleshooting guide (as per SRS 10.5.3).  
**Justification:** Reduces mean time to resolution (MTTR) and empowers on-call personnel.  
**Priority:** high  
**Implementation Notes:** Runbooks should be version-controlled and easily accessible from alert notifications.  
  - **Category:** Alert Management Process  
**Recommendation:** Establish a regular (e.g., bi-weekly or monthly) alert review process involving operations and development teams.  
**Justification:** To continuously tune alerts, remove noise, identify gaps, and ensure alerts remain relevant as the system evolves.  
**Priority:** high  
**Implementation Notes:** Track alert metrics (number of alerts, acknowledgments, resolution times, false positives) to inform reviews.  
  - **Category:** Automation  
**Recommendation:** Explore automated remediation actions for common, well-understood, low-risk alerts (e.g., restarting a stateless service worker).  
**Justification:** Can reduce MTTR for simple issues and free up on-call personnel.  
**Priority:** medium  
**Implementation Notes:** Start with very simple, safe actions. Implement with circuit breakers to prevent repeated failed automation.  
  - **Category:** User Experience (UX) for Monitoring  
**Recommendation:** Develop key dashboards in the monitoring system that provide an at-a-glance overview of system health, specifically for Odoo, N8N, and AI pipeline (SRS 9.1, 9.3.1).  
**Justification:** Facilitates quick assessment by administrators and operations, supplements direct alerting.  
**Priority:** high  
**Implementation Notes:** Dashboards should align with key business processes and NFRs.  
  - **Category:** Training  
**Recommendation:** Provide training to on-call personnel on the monitoring tools, alert interpretation, runbook usage, and incident management processes (SRS 3.3).  
**Justification:** Ensures effective response to incidents.  
**Priority:** high  
**Implementation Notes:** Include simulated incident response exercises.  
  


---

