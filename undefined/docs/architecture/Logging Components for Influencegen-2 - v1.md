# Specification

# 1. Logging And Observability Analysis

- **System Overview:**
  
  - **Analysis Date:** 2024-07-26
  - **Technology Stack:**
    
    - Odoo 18 (Python, OWL, XML)
    - N8N
    - PostgreSQL
    - AI Service (Flux LoRA models via REST API)
    
  - **Monitoring Requirements:**
    
    - REQ-ATEL-001: Comprehensive logging across Odoo modules, N8N, integrations, AI interactions.
    - REQ-ATEL-002: Structured logging (JSON), UTC timestamps, context (user, request, correlation IDs), severity.
    - REQ-ATEL-003: Configurable log levels per component/environment.
    - REQ-ATEL-004: Log search, filter, analysis capabilities.
    - REQ-ATEL-005: Audit trail for significant events and user actions.
    - REQ-ATEL-006: Secure, tamper-evident audit logs with detailed entries.
    - REQ-ATEL-007: Log retention policies for operational and audit logs.
    - REQ-ATEL-009: Correlation ID for cross-component tracing.
    - REQ-12-001: Centralized logging for aggregation, search, analysis, alerting.
    - REQ-IL-013: Monitoring API error rates, latencies, N8N workflow status.
    
  - **System Architecture:** Layered architecture with Odoo 18 as the core platform. InfluenceGen modules extend Odoo. N8N is used for workflow automation, primarily for AI image generation, acting as an orchestration layer between Odoo and external AI services. Communication for AI generation is asynchronous via Odoo webhooks to N8N, and N8N callbacks to Odoo REST APIs. PostgreSQL is the database. Potential integrations with third-party KYC/Payment services.
  - **Environment:** production
  
- **Log Level And Category Strategy:**
  
  - **Default Log Level:** INFO
  - **Environment Specific Levels:**
    
    - **Environment:** development  
**Log Level:** DEBUG  
**Justification:** Detailed logging for development and troubleshooting.  
    - **Environment:** staging  
**Log Level:** DEBUG  
**Justification:** Detailed logging for UAT and pre-production validation.  
    - **Environment:** production  
**Log Level:** INFO  
**Justification:** Standard operational logging, errors, and critical events. REQ-ATEL-003 allows for dynamic adjustment if needed.  
    
  - **Component Categories:**
    
    - **Component:** Odoo.InfluenceGen.OnboardingModule  
**Category:** Onboarding  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Track influencer registration, KYC, social media/bank verification steps and errors.  
    - **Component:** Odoo.InfluenceGen.CampaignModule  
**Category:** CampaignManagement  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Track campaign creation, applications, content submissions, approvals, and errors.  
    - **Component:** Odoo.InfluenceGen.AIIntegrationModule  
**Category:** AIImageGeneration.Odoo  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Track AI image requests initiated from Odoo, callback handling, image storage, and related errors.  
    - **Component:** Odoo.InfluenceGen.PaymentModule  
**Category:** PaymentProcessing  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Track payment calculations, batch generation, and integration with Odoo accounting.  
    - **Component:** Odoo.InfluenceGen.N8NWebhookGateway  
**Category:** Integration.OdooToN8N  
**Log Level:** INFO  
**Verbose Logging:** True  
**Justification:** Detailed logging of webhook calls to N8N and callback receptions from N8N, including payload summaries (excluding PII) and status. Critical for REQ-IL-013.  
    - **Component:** N8N.AIImageGenerationWorkflow  
**Category:** AIImageGeneration.N8N  
**Log Level:** INFO  
**Verbose Logging:** True  
**Justification:** Detailed logging of workflow execution steps, parameters, calls to AI service, response handling, and calls to Odoo callback. Critical for REQ-IL-013 and REQ-ATEL-010.  
    - **Component:** Odoo.InfluenceGen.ThirdPartyGateways  
**Category:** Integration.ExternalServices  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Track requests and responses to/from external KYC, payment services.  
    - **Component:** Odoo.Core.Security  
**Category:** Security.Audit  
**Log Level:** INFO  
**Verbose Logging:** False  
**Justification:** Covers audit log events as per REQ-ATEL-005. Actual log entries are audit events, not just operational logs.  
    
  - **Sampling Strategies:**
    
    
  - **Logging Approach:**
    
    - **Structured:** True
    - **Format:** JSON
    - **Standard Fields:**
      
      - timestamp_utc
      - level
      - message
      - correlation_id
      - request_id
      - user_id
      - component_name
      - category
      - source_ip
      - error_code
      - error_details
      - stack_trace
      
    - **Custom Fields:**
      
      - odoo_model
      - odoo_record_id
      - n8n_workflow_id
      - n8n_execution_id
      - target_service
      - action_performed
      - affected_entity_id
      
    
  
- **Log Aggregation Architecture:**
  
  - **Collection Mechanism:**
    
    - **Type:** agent
    - **Technology:** Filebeat | Fluentd | CloudWatch Agent | Azure Monitor Agent (Depends on chosen centralized logging solution)
    - **Configuration:**
      
      - **Paths:**
        
        - /var/log/odoo/*.log
        - /var/log/n8n/workflow_executions.log
        - stdout/stderr from containerized N8N & Odoo
        
      - **Multiline_Pattern:** ^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}
      - **Json_Parsing:** True
      
    - **Justification:** Collects logs from Odoo (configured to output structured JSON) and N8N (configured for JSON output or console output captured by agent).
    
  - **Strategy:**
    
    - **Approach:** centralized
    - **Reasoning:** REQ-12-001 mandates a centralized logging solution for aggregation, search, analysis, and alerting.
    - **Local Retention:** 24-72 hours (or until successfully shipped)
    
  - **Shipping Methods:**
    
    - **Protocol:** HTTPS | TCP (Secure)  
**Destination:** Centralized Logging Service Endpoint (e.g., Logstash, Elasticsearch, Cloud Provider Ingestion API)  
**Reliability:** at-least-once  
**Compression:** True  
    
  - **Buffering And Batching:**
    
    - **Buffer Size:** 50MB
    - **Batch Size:** 1000
    - **Flush Interval:** 5s
    - **Backpressure Handling:** Disk-based spooling by agent
    
  - **Transformation And Enrichment:**
    
    - **Transformation:** Add standard metadata (e.g., host, environment)  
**Purpose:** Contextualization  
**Stage:** collection | transport (by agent or aggregator)  
    - **Transformation:** Parse JSON logs if not natively handled  
**Purpose:** Structured data access  
**Stage:** transport | storage (by aggregator or logging backend)  
    - **Transformation:** GeoIP lookup for source_ip (if applicable)  
**Purpose:** Security analysis  
**Stage:** transport | storage  
    
  - **High Availability:**
    
    - **Required:** True
    - **Redundancy:** Clustered log shippers/aggregators, redundant logging backend nodes.
    - **Failover Strategy:** Automatic failover for collection agents and backend.
    
  
- **Retention Policy Design:**
  
  - **Retention Periods:**
    
    - **Log Type:** OperationalLogs.Odoo  
**Retention Period:** 90 days  
**Justification:** SRS 7.3 for system logs, sufficient for troubleshooting recent issues.  
    - **Log Type:** OperationalLogs.N8N  
**Retention Period:** 90 days  
**Justification:** SRS 7.3 for N8N logs, sufficient for troubleshooting recent workflow executions.  
    - **Log Type:** AuditLogs.Security  
**Retention Period:** 1-7 years (configurable, default 3 years)  
**Justification:** REQ-ATEL-007, SRS 7.3 for audit logs, regulatory compliance and security investigation needs.  
    - **Log Type:** AuditLogs.DataChanges  
**Retention Period:** 1-7 years (configurable, default 3 years)  
**Justification:** REQ-ATEL-007, SRS 7.3 for audit logs, compliance for data lifecycle management.  
    
  - **Compliance Requirements:**
    
    - **Regulation:** GDPR  
**Applicable Log Types:**
    
    - AuditLogs.Security
    - AuditLogs.DataChanges
    - OperationalLogs with PII traces (must be minimized)
    
**Minimum Retention:** As per organizational policy, balancing investigation needs with data minimization.  
**Special Handling:** PII in operational logs should be avoided or masked. Audit logs PII access strictly controlled.  
    
  - **Volume Impact Analysis:**
    
    - **Estimated Daily Volume:** To be determined during testing (expect medium to high volume from N8N and verbose Odoo modules)
    - **Storage Cost Projection:** Dependent on chosen solution and volume. To be calculated.
    - **Compression Ratio:** Expected 5:1 to 10:1 with standard compression.
    
  - **Storage Tiering:**
    
    - **Hot Storage:**
      
      - **Duration:** 30 days (for operational), 90 days (for audit)
      - **Accessibility:** immediate
      - **Cost:** high
      
    - **Warm Storage:**
      
      - **Duration:** Up to 90 days (for operational), up to 1 year (for audit)
      - **Accessibility:** seconds to minutes
      - **Cost:** medium
      
    - **Cold Storage:**
      
      - **Duration:** Beyond warm storage up to full retention period (primarily for audit logs)
      - **Accessibility:** minutes to hours
      - **Cost:** low
      
    
  - **Compression Strategy:**
    
    - **Algorithm:** LZ4 | Zstd (Tool dependent)
    - **Compression Level:** Default
    - **Expected Ratio:** 5:1 to 10:1
    
  - **Anonymization Requirements:**
    
    - **Data Type:** PII in operational logs (e.g. user inputs in debug logs)  
**Method:** Masking | Redaction at source or during ingestion pipeline  
**Timeline:** Real-time or near real-time  
**Compliance:** GDPR  
    
  
- **Search Capability Requirements:**
  
  - **Essential Capabilities:**
    
    - **Capability:** Full-text search on 'message' field  
**Performance Requirement:** < 5 seconds for typical queries  
**Justification:** REQ-ATEL-004: Basic troubleshooting.  
    - **Capability:** Filtering by standard fields (timestamp_utc, level, component_name, correlation_id, user_id)  
**Performance Requirement:** < 3 seconds for typical queries  
**Justification:** REQ-ATEL-004, REQ-12-002: Targeted log analysis.  
    - **Capability:** Saved searches and dashboards for common issues / audit reviews  
**Performance Requirement:** Dashboards load < 10 seconds  
**Justification:** REQ-12-004, REQ-ATEL-008: Efficient operational oversight and compliance.  
    
  - **Performance Characteristics:**
    
    - **Search Latency:** Average < 5 seconds for common queries
    - **Concurrent Users:** 5
    - **Query Complexity:** simple|complex
    - **Indexing Strategy:** Default full-text indexing for message, keyword indexing for standard/custom fields.
    
  - **Indexed Fields:**
    
    - **Field:** timestamp_utc  
**Index Type:** date  
**Search Pattern:** range  
**Frequency:** high  
    - **Field:** level  
**Index Type:** keyword  
**Search Pattern:** exact_match  
**Frequency:** high  
    - **Field:** correlation_id  
**Index Type:** keyword  
**Search Pattern:** exact_match  
**Frequency:** high  
    - **Field:** user_id  
**Index Type:** keyword  
**Search Pattern:** exact_match  
**Frequency:** medium  
    - **Field:** component_name  
**Index Type:** keyword  
**Search Pattern:** exact_match  
**Frequency:** high  
    - **Field:** category  
**Index Type:** keyword  
**Search Pattern:** exact_match  
**Frequency:** high  
    - **Field:** message  
**Index Type:** text  
**Search Pattern:** full_text  
**Frequency:** high  
    - **Field:** error_code  
**Index Type:** keyword  
**Search Pattern:** exact_match  
**Frequency:** low  
    - **Field:** action_performed (audit)  
**Index Type:** keyword  
**Search Pattern:** exact_match  
**Frequency:** medium  
    - **Field:** affected_entity_id (audit)  
**Index Type:** keyword  
**Search Pattern:** exact_match  
**Frequency:** medium  
    
  - **Full Text Search:**
    
    - **Required:** True
    - **Fields:**
      
      - message
      - error_details
      - stack_trace
      
    - **Search Engine:** Elasticsearch | OpenSearch (part of chosen centralized solution)
    - **Relevance Scoring:** True
    
  - **Correlation And Tracing:**
    
    - **Correlation Ids:**
      
      - correlation_id
      - request_id
      
    - **Trace Id Propagation:** Via HTTP headers (e.g., X-Correlation-ID) and within log messages. REQ-ATEL-009.
    - **Span Correlation:** True
    - **Cross Service Tracing:** True
    
  - **Dashboard Requirements:**
    
    - **Dashboard:** Operational Health Summary  
**Purpose:** At-a-glance view of error rates, critical logs by component.  
**Refresh Interval:** 1 minute  
**Audience:** Platform Administrators, Operations Team  
    - **Dashboard:** AI Image Generation Workflow Monitoring  
**Purpose:** Track request volume, success/failure rates, latencies for Odoo-N8N-AI flow.  
**Refresh Interval:** 5 minutes  
**Audience:** Platform Administrators, N8N Admins  
    - **Dashboard:** Security Audit Log Review  
**Purpose:** Review key security events (logins, permission changes, PII access). REQ-ATEL-008.  
**Refresh Interval:** On demand / Daily  
**Audience:** Platform Administrators, Security Team  
    
  
- **Storage Solution Selection:**
  
  - **Selected Technology:**
    
    - **Primary:** Elasticsearch | OpenSearch | Cloud Provider Specific Log Storage (e.g., AWS CloudWatch Logs Insights, Azure Monitor Log Analytics)
    - **Reasoning:** REQ-12-002 requires centralized solution. These technologies provide robust search, scalability, and integration with visualization tools. Choice depends on existing infrastructure and expertise.
    - **Alternatives:**
      
      - Splunk
      - Graylog
      
    
  - **Scalability Requirements:**
    
    - **Expected Growth Rate:** Estimate 20-50% annually based on user/campaign growth.
    - **Peak Load Handling:** System should handle peak registration and AI generation loads without log loss.
    - **Horizontal Scaling:** True
    
  - **Cost Performance Analysis:**
    
    - **Solution:** Managed Cloud Service (e.g., AWS OpenSearch Service)  
**Cost Per Gb:** Varies by provider/region/retention  
**Query Performance:** High  
**Operational Complexity:** low  
    - **Solution:** Self-hosted ELK/OpenSearch  
**Cost Per Gb:** Infrastructure + Personnel cost  
**Query Performance:** High (if well-managed)  
**Operational Complexity:** high  
    
  - **Backup And Recovery:**
    
    - **Backup Frequency:** Daily snapshots (for logging backend configuration and recent hot data)
    - **Recovery Time Objective:** 4 hours (for logging platform)
    - **Recovery Point Objective:** 1 hour (for recent logs)
    - **Testing Frequency:** Annually
    
  - **Geo Distribution:**
    
    - **Required:** False
    - **Regions:**
      
      
    - **Replication Strategy:** 
    
  - **Data Sovereignty:**
    
    - **Region:** As per organizational data residency requirements (e.g., EU for GDPR)  
**Requirements:**
    
    - Store logs containing PII within designated regions.
    
**Compliance Framework:** GDPR  
    
  
- **Access Control And Compliance:**
  
  - **Access Control Requirements:**
    
    - **Role:** Platform Administrator  
**Permissions:**
    
    - read_all_logs
    - manage_log_configs
    - create_dashboards
    
**Log Types:**
    
    - OperationalLogs.*
    - AuditLogs.*
    
**Justification:** REQ-ATEL-008: Full operational oversight and audit review.  
    - **Role:** Developer (Non-Prod)  
**Permissions:**
    
    - read_component_logs
    
**Log Types:**
    
    - OperationalLogs.* (for assigned components in non-prod)
    
**Justification:** Troubleshooting and development in non-production environments.  
    - **Role:** Security Analyst  
**Permissions:**
    
    - read_audit_logs
    - read_security_relevant_operational_logs
    
**Log Types:**
    
    - AuditLogs.Security
    - OperationalLogs with security implications
    
**Justification:** Security incident investigation and compliance monitoring.  
    
  - **Sensitive Data Handling:**
    
    - **Data Type:** PII (e.g., names, emails, KYC data fragments)  
**Handling Strategy:** mask|exclude|tokenize  
**Fields:**
    
    - message (if debug includes user input)
    - custom_fields with PII
    
**Compliance Requirement:** GDPR. Minimize PII in operational logs. Strict access control for logs containing unavoidable PII.  
    - **Data Type:** API Keys, Passwords in logs (accidental)  
**Handling Strategy:** exclude|redact  
**Fields:**
    
    - message
    - payload_dumps
    
**Compliance Requirement:** Security best practices. Prevent credential leakage.  
    
  - **Encryption Requirements:**
    
    - **In Transit:**
      
      - **Required:** True
      - **Protocol:** TLS 1.2+ (TLS 1.3 preferred)
      - **Certificate Management:** Standard PKI, automated renewal.
      
    - **At Rest:**
      
      - **Required:** True
      - **Algorithm:** AES-256
      - **Key Management:** KMS (e.g., HashiCorp Vault, Cloud Provider KMS)
      
    
  - **Audit Trail:**
    
    - **Log Access:** True
    - **Retention Period:** As per AuditLog retention (1-7 years)
    - **Audit Log Location:** Within the centralized logging solution, or a dedicated security audit log store.
    - **Compliance Reporting:** True
    
  - **Regulatory Compliance:**
    
    - **Regulation:** GDPR  
**Applicable Components:**
    
    - Odoo (all modules handling PII)
    - N8N (if processing PII)
    - Centralized Logging Solution
    
**Specific Requirements:**
    
    - Data minimization in logs
    - Right to access/erasure considerations for PII in logs (subject to legal hold/retention needs)
    - Secure storage and access control for logs with PII.
    
**Evidence Collection:** Audit logs of PII access, log configuration change history.  
    
  - **Data Protection Measures:**
    
    - **Measure:** PII Masking/Redaction in Operational Logs  
**Implementation:** Log filtering rules at source or ingestion pipeline.  
**Monitoring Required:** True  
    - **Measure:** Role-Based Access Control to Logs  
**Implementation:** Configuration within centralized logging solution.  
**Monitoring Required:** True  
    
  
- **Project Specific Logging Config:**
  
  - **Logging Config:**
    
    - **Level:** INFO (Production)
    - **Retention:** Operational: 90 days, Audit: 1-7 years
    - **Aggregation:** Centralized (e.g., ELK/OpenSearch/Cloud Service)
    - **Storage:** Tiered (Hot/Warm/Cold)
    - **Configuration:**
      
      - **Odoo_Log_Format:** json_structured_with_correlation_id_and_context
      - **N8N_Log_Output:** stdout_json_format_for_container_capture
      
    
  - **Component Configurations:**
    
    - **Component:** Odoo.InfluenceGen.Modules  
**Log Level:** INFO  
**Output Format:** JSON  
**Destinations:**
    
    - stdout (for agent capture)
    - /var/log/odoo/influencegen.log
    
**Sampling:**
    
    - **Enabled:** False
    - **Rate:** 
    
**Custom Fields:**
    
    - correlation_id
    - user_id
    - request_id
    - odoo_model
    - odoo_record_id
    
    - **Component:** N8N.AIImageGenerationWorkflow  
**Log Level:** INFO  
**Output Format:** JSON (via N8N's logging capabilities or custom Function nodes)  
**Destinations:**
    
    - stdout (for agent capture)
    - N8N internal execution log
    
**Sampling:**
    
    - **Enabled:** False
    - **Rate:** 
    
**Custom Fields:**
    
    - correlation_id
    - request_id
    - n8n_workflow_id
    - n8n_execution_id
    - step_name
    - status
    
    
  - **Metrics:**
    
    - **Custom Metrics:**
      
      
    
  - **Alert Rules:**
    
    - **Name:** CriticalOdooErrorRate  
**Condition:** count(level:ERROR AND component_name:Odoo.*) > 10 in 5m  
**Severity:** Critical  
**Actions:**
    
    - **Type:** email  
**Target:** platform-admins@example.com  
**Configuration:**
    
    
    
**Suppression Rules:**
    
    
**Escalation Path:**
    
    - PagerDutyIntegrationForAdmins
    
    - **Name:** N8NWorkflowFailureRate  
**Condition:** count(status:failed AND component_name:N8N.AIImageGenerationWorkflow) / count(component_name:N8N.AIImageGenerationWorkflow) > 0.1 in 15m  
**Severity:** High  
**Actions:**
    
    - **Type:** slack  
**Target:** #ops-alerts  
**Configuration:**
    
    
    
**Suppression Rules:**
    
    
**Escalation Path:**
    
    
    - **Name:** AuditLogTamperingAttempt  
**Condition:** event_type:AuditLogModificationAttempt  
**Severity:** Critical  
**Actions:**
    
    - **Type:** email  
**Target:** security-team@example.com  
**Configuration:**
    
    
    
**Suppression Rules:**
    
    
**Escalation Path:**
    
    - PagerDutyIntegrationForSecurity
    
    
  
- **Implementation Priority:**
  
  - **Component:** Centralized Logging Backend Setup (e.g., ELK)  
**Priority:** high  
**Dependencies:**
    
    
**Estimated Effort:** Medium-High  
**Risk Level:** medium  
  - **Component:** Odoo Structured JSON Logging Configuration & Agent Setup  
**Priority:** high  
**Dependencies:**
    
    - Centralized Logging Backend Setup
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** N8N Logging Configuration & Agent Setup  
**Priority:** high  
**Dependencies:**
    
    - Centralized Logging Backend Setup
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** Correlation ID Implementation (Odoo & N8N)  
**Priority:** high  
**Dependencies:**
    
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  - **Component:** Basic Operational Dashboards & Alerting Rules  
**Priority:** medium  
**Dependencies:**
    
    - Centralized Logging Backend Setup
    - Odoo Logging
    - N8N Logging
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** Audit Log Configuration and Review Dashboards  
**Priority:** medium  
**Dependencies:**
    
    - Centralized Logging Backend Setup
    - Odoo Logging
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  
- **Risk Assessment:**
  
  - **Risk:** Incomplete or inconsistent logging across components.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Standardized logging libraries/wrappers, code reviews, testing.  
**Contingency Plan:** Post-deployment analysis and iterative improvements to logging.  
  - **Risk:** Log volume overwhelming storage or processing capacity.  
**Impact:** high  
**Probability:** low  
**Mitigation:** Proper capacity planning, log level management, efficient log queries, scalable logging infrastructure.  
**Contingency Plan:** Temporary log level reduction, scaling up logging infrastructure, optimizing expensive queries.  
  - **Risk:** Sensitive data leakage in logs.  
**Impact:** high  
**Probability:** medium  
**Mitigation:** PII masking/redaction, developer training, strict PR reviews for logging PII, security testing.  
**Contingency Plan:** Immediate log rotation/purging of affected logs, incident response, vulnerability patching.  
  - **Risk:** Failure of log shipping or aggregation pipeline.  
**Impact:** medium  
**Probability:** low  
**Mitigation:** Monitoring of the logging pipeline itself, resilient agent configuration, HA for aggregators.  
**Contingency Plan:** Investigate and fix pipeline issue, re-ship logs from local buffers if available.  
  
- **Recommendations:**
  
  - **Category:** Logging Practices  
**Recommendation:** Implement a shared logging library or utility within Odoo custom modules to enforce structured logging, context propagation (correlation IDs, user context), and consistent log levels.  
**Justification:** Ensures consistency, reduces boilerplate code, and makes it easier to adhere to logging standards (REQ-ATEL-002, REQ-ATEL-009).  
**Priority:** high  
**Implementation Notes:** This library should wrap Python's standard `logging` module and integrate with Odoo's request context.  
  - **Category:** N8N Logging  
**Recommendation:** Utilize N8N's built-in execution logging and, where necessary, use Function nodes to emit custom structured logs (e.g., to console for agent capture) including correlation IDs and key workflow parameters.  
**Justification:** Provides detailed insight into N8N workflow execution for troubleshooting and monitoring (REQ-ATEL-010).  
**Priority:** high  
**Implementation Notes:** Ensure N8N is configured to output logs in a way that can be easily ingested by the chosen log agent (e.g., JSON to stdout).  
  - **Category:** Audit Logging  
**Recommendation:** Clearly distinguish between operational logs (for debugging/monitoring) and audit logs (for security/compliance). Store and manage them with appropriate retention and access controls as per REQ-ATEL-006 & REQ-ATEL-007.  
**Justification:** Ensures audit logs meet their specific non-repudiation and integrity requirements, separate from potentially voluminous operational logs.  
**Priority:** high  
**Implementation Notes:** Audit logs should be written to a specific category/index in the centralized solution, or use Odoo's built-in audit trail mechanisms if they meet tamper-evidence requirements.  
  - **Category:** Log Review & Monitoring  
**Recommendation:** Establish regular processes for reviewing key operational dashboards and critical alerts. Periodically review audit logs for anomalies or compliance checks.  
**Justification:** Proactive monitoring helps in early detection of issues and ensures the logging system provides value (REQ-12-004, REQ-ATEL-008).  
**Priority:** medium  
**Implementation Notes:** Schedule weekly operational reviews and monthly/quarterly audit log spot-checks.  
  


---

