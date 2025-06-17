# Specification

# 1. Files

- **Path:** prometheus/prometheus.yml  
**Description:** Main Prometheus server configuration. Defines global settings, scrape configurations for Odoo, N8N, AI services, and system metrics exporters. Specifies scrape intervals, timeouts, rule file paths, and service discovery mechanisms.  
**Template:** YAML Configuration Template  
**Dependancy Level:** 1  
**Name:** prometheus  
**Type:** ConfigurationFile  
**Relative Path:** prometheus/prometheus.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Metric Collection Configuration
    - Service Discovery Configuration
    - Alerting Rule File Integration
    
**Requirement Ids:**
    
    - REQ-12-003
    - REQ-12-008
    - REQ-16-009
    
**Purpose:** Configures the Prometheus monitoring server, defining what targets to scrape for metrics and where to find alerting rules.  
**Logic Description:** Contains sections for 'global' settings, 'rule_files' to load alerting rules, 'scrape_configs' for various jobs (Odoo, N8N, AI Service, node exporters, etc.), and 'alerting' to specify Alertmanager endpoints. Scrape jobs will use static configs or service discovery methods (e.g., file_sd_configs pointing to files in prometheus/targets/).  
**Documentation:**
    
    - **Summary:** Core configuration file for Prometheus. Inputs: paths to rule files, target definitions. Outputs: active scrape configurations and alerting setup for Prometheus.
    
**Namespace:** InfluenceGen.Monitoring.Prometheus  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/rules/odoo_rules.yml  
**Description:** Prometheus alerting rules specific to Odoo application metrics. Defines alerts for Odoo performance issues, error rates, and business-specific KPIs.  
**Template:** YAML Configuration Template (PromQL)  
**Dependancy Level:** 0  
**Name:** odoo_rules  
**Type:** ConfigurationFile  
**Relative Path:** prometheus/rules/odoo_rules.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Application Alerting
    
**Requirement Ids:**
    
    - REQ-12-003
    - REQ-12-008
    - REQ-16-009
    
**Purpose:** Defines specific alerting conditions based on metrics scraped from Odoo instances.  
**Logic Description:** Contains a 'groups' list, each group having a 'name' and a list of 'rules'. Each rule specifies an 'alert' name, an 'expr' (PromQL query for the alert condition), a 'for' duration, 'labels' (severity, component), and 'annotations' (summary, description). Alerts for Odoo could include high request latency, high error rates, specific business process failures if instrumented.  
**Documentation:**
    
    - **Summary:** Defines alerting rules for Odoo. Inputs: Odoo metrics. Outputs: Alerts sent to Alertmanager if conditions are met.
    
**Namespace:** InfluenceGen.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** AlertingConfiguration
    
- **Path:** prometheus/rules/n8n_rules.yml  
**Description:** Prometheus alerting rules for N8N workflow execution metrics, queue lengths, and error rates.  
**Template:** YAML Configuration Template (PromQL)  
**Dependancy Level:** 0  
**Name:** n8n_rules  
**Type:** ConfigurationFile  
**Relative Path:** prometheus/rules/n8n_rules.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N Workflow Alerting
    
**Requirement Ids:**
    
    - REQ-12-003
    - REQ-12-008
    - REQ-16-009
    - REQ-ATEL-010
    
**Purpose:** Defines alerting conditions for N8N instances, focusing on workflow health and performance.  
**Logic Description:** Similar structure to odoo_rules.yml. Rules for N8N could include high workflow error rates, long execution times, Odoo callback delivery failures (if N8N metrics expose this), or high queue depths for N8N workers.  
**Documentation:**
    
    - **Summary:** Defines alerting rules for N8N. Inputs: N8N metrics. Outputs: Alerts sent to Alertmanager.
    
**Namespace:** InfluenceGen.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** AlertingConfiguration
    
- **Path:** prometheus/rules/ai_service_rules.yml  
**Description:** Prometheus alerting rules for AI image generation service metrics, such as API latency, error rates, and success/failure rates.  
**Template:** YAML Configuration Template (PromQL)  
**Dependancy Level:** 0  
**Name:** ai_service_rules  
**Type:** ConfigurationFile  
**Relative Path:** prometheus/rules/ai_service_rules.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Service Alerting
    
**Requirement Ids:**
    
    - REQ-12-003
    - REQ-12-008
    - REQ-16-009
    
**Purpose:** Defines alerting conditions related to the AI image generation service's performance and availability.  
**Logic Description:** Similar structure. Rules could include high AI service API error rates, high latency for generation requests, high failure rate for image generation, or unavailability of the AI service endpoint.  
**Documentation:**
    
    - **Summary:** Defines alerting rules for the AI service. Inputs: AI service metrics. Outputs: Alerts.
    
**Namespace:** InfluenceGen.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** AlertingConfiguration
    
- **Path:** prometheus/rules/system_rules.yml  
**Description:** General system and infrastructure alerting rules, such as CPU utilization, memory usage, disk space, and network issues for Odoo, N8N, and AI service hosts.  
**Template:** YAML Configuration Template (PromQL)  
**Dependancy Level:** 0  
**Name:** system_rules  
**Type:** ConfigurationFile  
**Relative Path:** prometheus/rules/system_rules.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Infrastructure Alerting
    
**Requirement Ids:**
    
    - REQ-12-003
    - REQ-12-008
    - REQ-16-009
    
**Purpose:** Defines alerts for underlying system resource health.  
**Logic Description:** Similar structure. Rules for high CPU/memory/disk utilization, network latency, host down, database connectivity issues, imminent SSL certificate expiry, critical backup job failures.  
**Documentation:**
    
    - **Summary:** Defines system-level alerting rules. Inputs: Node exporter metrics, database metrics. Outputs: Alerts.
    
**Namespace:** InfluenceGen.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** AlertingConfiguration
    
- **Path:** prometheus/rules/audit_log_rules.yml  
**Description:** Prometheus alerting rules based on metrics derived from audit log analysis (e.g., frequent login failures, sensitive data access attempts). This might require custom exporters or metrics derived from ELK.  
**Template:** YAML Configuration Template (PromQL)  
**Dependancy Level:** 0  
**Name:** audit_log_rules  
**Type:** ConfigurationFile  
**Relative Path:** prometheus/rules/audit_log_rules.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Security Alerting from Audit Logs
    
**Requirement Ids:**
    
    - REQ-12-008
    - REQ-16-009
    - REQ-ATEL-005
    
**Purpose:** Defines security-related alerts based on patterns or thresholds in audit log data.  
**Logic Description:** Rules might target metrics like 'rate_of_failed_logins_per_user' or 'count_of_sensitive_data_access_events'. Requires a mechanism to expose audit log insights as Prometheus metrics (e.g., a custom exporter querying Elasticsearch, or Logstash metrics).  
**Documentation:**
    
    - **Summary:** Defines alerting rules based on audit log metrics. Inputs: Audit log derived metrics. Outputs: Security alerts.
    
**Namespace:** InfluenceGen.Monitoring.Prometheus.Rules  
**Metadata:**
    
    - **Category:** AlertingConfiguration
    
- **Path:** prometheus/targets/odoo_targets.json  
**Description:** Service discovery file for Prometheus, defining Odoo instances to be scraped. Could be static or dynamically generated.  
**Template:** JSON Configuration Template  
**Dependancy Level:** 0  
**Name:** odoo_targets  
**Type:** ConfigurationFile  
**Relative Path:** prometheus/targets/odoo_targets.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Service Discovery for Prometheus
    
**Requirement Ids:**
    
    - REQ-12-003
    
**Purpose:** Lists Odoo application targets for Prometheus metric scraping.  
**Logic Description:** JSON array of target objects, each with a 'targets' list (host:port) and 'labels' (e.g., environment, job_name). Example: `[{"targets": ["odoo-prod-1:8069", "odoo-prod-2:8069"], "labels": {"env": "production", "app": "odoo"}}]`  
**Documentation:**
    
    - **Summary:** Defines Odoo scrape targets for Prometheus. Inputs: Odoo instance endpoints. Outputs: Scraped metrics.
    
**Namespace:** InfluenceGen.Monitoring.Prometheus.Targets  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/targets/n8n_targets.json  
**Description:** Service discovery file for Prometheus, defining N8N instances to be scraped.  
**Template:** JSON Configuration Template  
**Dependancy Level:** 0  
**Name:** n8n_targets  
**Type:** ConfigurationFile  
**Relative Path:** prometheus/targets/n8n_targets.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N Service Discovery for Prometheus
    
**Requirement Ids:**
    
    - REQ-12-003
    
**Purpose:** Lists N8N application targets for Prometheus metric scraping.  
**Logic Description:** Similar JSON structure to odoo_targets.json, specifying N8N instance endpoints and relevant labels.  
**Documentation:**
    
    - **Summary:** Defines N8N scrape targets for Prometheus. Inputs: N8N instance endpoints. Outputs: Scraped metrics.
    
**Namespace:** InfluenceGen.Monitoring.Prometheus.Targets  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** prometheus/targets/ai_service_targets.json  
**Description:** Service discovery file for Prometheus, defining AI service endpoints or related metric exporters to be scraped.  
**Template:** JSON Configuration Template  
**Dependancy Level:** 0  
**Name:** ai_service_targets  
**Type:** ConfigurationFile  
**Relative Path:** prometheus/targets/ai_service_targets.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Service Discovery for Prometheus
    
**Requirement Ids:**
    
    - REQ-12-003
    
**Purpose:** Lists AI service (or its metric proxy) targets for Prometheus metric scraping.  
**Logic Description:** Similar JSON structure, specifying AI service metric endpoints. If the AI service is external and doesn't expose Prometheus metrics directly, this might target a custom exporter.  
**Documentation:**
    
    - **Summary:** Defines AI service scrape targets. Inputs: AI service metric endpoints. Outputs: Scraped metrics.
    
**Namespace:** InfluenceGen.Monitoring.Prometheus.Targets  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    
- **Path:** alertmanager/alertmanager.yml  
**Description:** Main Alertmanager configuration. Defines routing rules for alerts, receivers (email, Slack, PagerDuty, etc.), inhibition rules, and notification templating.  
**Template:** YAML Configuration Template  
**Dependancy Level:** 0  
**Name:** alertmanager  
**Type:** ConfigurationFile  
**Relative Path:** alertmanager/alertmanager.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Alert Routing
    - Notification Channel Configuration
    - Alert Grouping and Inhibition
    
**Requirement Ids:**
    
    - REQ-12-008
    - REQ-12-009
    - REQ-16-008
    - REQ-16-009
    - REQ-16-010
    - REQ-16-011
    
**Purpose:** Configures how alerts generated by Prometheus are processed, grouped, and routed to various notification channels.  
**Logic Description:** Contains 'global' settings, 'route' block defining the main routing tree (based on labels like severity, component), 'receivers' defining notification channels (email_configs, slack_configs, pagerduty_configs), and 'inhibit_rules'. Also references notification 'templates'.  
**Documentation:**
    
    - **Summary:** Core configuration for Alertmanager. Inputs: Alerts from Prometheus. Outputs: Notifications to configured channels.
    
**Namespace:** InfluenceGen.Monitoring.Alertmanager  
**Metadata:**
    
    - **Category:** AlertingConfiguration
    
- **Path:** alertmanager/templates/default_template.tmpl  
**Description:** Default Go template for formatting alert notifications sent by Alertmanager. Can be customized for different receivers.  
**Template:** Go Template File  
**Dependancy Level:** 0  
**Name:** default_template  
**Type:** ConfigurationFile  
**Relative Path:** alertmanager/templates/default_template.tmpl  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Alert Notification Formatting
    
**Requirement Ids:**
    
    - REQ-12-009
    - REQ-16-010
    
**Purpose:** Defines the structure and content of alert notifications.  
**Logic Description:** Uses Go templating language to iterate over alerts, access their labels and annotations, and format them into a human-readable message for emails, Slack, etc. Includes information like alert name, summary, description, severity, and affected entities.  
**Documentation:**
    
    - **Summary:** Notification template for Alertmanager. Inputs: Alert data. Outputs: Formatted notification message.
    
**Namespace:** InfluenceGen.Monitoring.Alertmanager.Templates  
**Metadata:**
    
    - **Category:** AlertingConfiguration
    
- **Path:** alertmanager/integrations/pagerduty_config.json  
**Description:** Placeholder for PagerDuty integration specific settings, if PagerDuty is used as a notification channel. Actual secrets should be managed via a secrets manager.  
**Template:** JSON Configuration Template  
**Dependancy Level:** 0  
**Name:** pagerduty_config  
**Type:** ConfigurationFile  
**Relative Path:** alertmanager/integrations/pagerduty_config.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - PagerDuty Integration Settings
    
**Requirement Ids:**
    
    - REQ-12-009
    - REQ-16-010
    
**Purpose:** Stores non-sensitive configuration parameters for PagerDuty integration. Sensitive keys managed separately.  
**Logic Description:** May contain PagerDuty service keys or routing keys. IMPORTANT: Actual sensitive API keys should be injected via environment variables or a secure secrets management system, not stored in this file directly. This file might define mappings or default severities if the PagerDuty receiver in alertmanager.yml needs them.  
**Documentation:**
    
    - **Summary:** Configuration parameters for PagerDuty integration (non-sensitive parts).
    
**Namespace:** InfluenceGen.Monitoring.Alertmanager.Integrations  
**Metadata:**
    
    - **Category:** AlertingConfiguration
    
- **Path:** grafana/datasources/prometheus_datasource.json  
**Description:** Grafana datasource definition for connecting to the Prometheus server. This is typically provisioned.  
**Template:** JSON Configuration Template (Grafana Datasource)  
**Dependancy Level:** 0  
**Name:** prometheus_datasource  
**Type:** ConfigurationFile  
**Relative Path:** grafana/datasources/prometheus_datasource.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Grafana Datasource Configuration
    
**Requirement Ids:**
    
    - REQ-12-004
    
**Purpose:** Defines how Grafana connects to Prometheus to query metrics.  
**Logic Description:** JSON object specifying 'name', 'type' (prometheus), 'url' of the Prometheus server, 'access' mode (server/proxy), and other datasource-specific settings like scrape interval if needed.  
**Documentation:**
    
    - **Summary:** Configures Prometheus as a datasource in Grafana.
    
**Namespace:** InfluenceGen.Monitoring.Grafana.Datasources  
**Metadata:**
    
    - **Category:** DashboardingConfiguration
    
- **Path:** grafana/dashboards/odoo_overview_dashboard.json  
**Description:** Grafana dashboard definition (JSON model) for visualizing Odoo application performance metrics.  
**Template:** JSON Configuration Template (Grafana Dashboard)  
**Dependancy Level:** 0  
**Name:** odoo_overview_dashboard  
**Type:** ConfigurationFile  
**Relative Path:** grafana/dashboards/odoo_overview_dashboard.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Performance Dashboard
    
**Requirement Ids:**
    
    - REQ-12-004
    - REQ-12-007
    
**Purpose:** Provides a visual overview of Odoo application health and key performance indicators.  
**Logic Description:** Grafana dashboard JSON model. Contains panels with PromQL queries to visualize metrics like request rates, error rates, latencies, active user sessions, resource usage of Odoo instances. Uses variables for filtering by environment or instance.  
**Documentation:**
    
    - **Summary:** JSON definition for Odoo overview dashboard in Grafana.
    
**Namespace:** InfluenceGen.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** DashboardingConfiguration
    
- **Path:** grafana/dashboards/n8n_workflow_dashboard.json  
**Description:** Grafana dashboard definition for N8N workflow metrics: execution counts, success/error rates, durations, queue status.  
**Template:** JSON Configuration Template (Grafana Dashboard)  
**Dependancy Level:** 0  
**Name:** n8n_workflow_dashboard  
**Type:** ConfigurationFile  
**Relative Path:** grafana/dashboards/n8n_workflow_dashboard.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N Workflow Performance Dashboard
    
**Requirement Ids:**
    
    - REQ-12-004
    - REQ-12-007
    - REQ-ATEL-010
    
**Purpose:** Visualizes N8N workflow performance and health.  
**Logic Description:** Grafana dashboard JSON model. Panels show N8N workflow execution statistics, error rates per workflow, average execution times, and N8N worker queue lengths. Uses PromQL queries against N8N metrics.  
**Documentation:**
    
    - **Summary:** JSON definition for N8N workflow dashboard in Grafana.
    
**Namespace:** InfluenceGen.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** DashboardingConfiguration
    
- **Path:** grafana/dashboards/ai_service_performance_dashboard.json  
**Description:** Grafana dashboard for AI image generation service metrics: request volume, latency, success/failure rates, model usage.  
**Template:** JSON Configuration Template (Grafana Dashboard)  
**Dependancy Level:** 0  
**Name:** ai_service_performance_dashboard  
**Type:** ConfigurationFile  
**Relative Path:** grafana/dashboards/ai_service_performance_dashboard.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - AI Service Performance Dashboard
    
**Requirement Ids:**
    
    - REQ-12-004
    - REQ-12-007
    
**Purpose:** Visualizes the performance and utilization of the AI image generation service.  
**Logic Description:** Grafana dashboard JSON model. Panels display metrics like number of AI generation requests, average processing time, error rates from the AI service, and potentially breakdowns by AI model used. Uses PromQL queries against AI service metrics or metrics from N8N related to AI calls.  
**Documentation:**
    
    - **Summary:** JSON definition for AI service performance dashboard in Grafana.
    
**Namespace:** InfluenceGen.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** DashboardingConfiguration
    
- **Path:** grafana/dashboards/system_health_dashboard.json  
**Description:** Grafana dashboard for overall system infrastructure health: CPU, memory, disk, network for key servers.  
**Template:** JSON Configuration Template (Grafana Dashboard)  
**Dependancy Level:** 0  
**Name:** system_health_dashboard  
**Type:** ConfigurationFile  
**Relative Path:** grafana/dashboards/system_health_dashboard.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - System Infrastructure Health Dashboard
    
**Requirement Ids:**
    
    - REQ-12-004
    - REQ-12-007
    
**Purpose:** Provides an overview of the health of the underlying infrastructure hosting the platform components.  
**Logic Description:** Grafana dashboard JSON model. Visualizes metrics from node exporters or cloud provider monitoring, such as CPU load, memory utilization, disk I/O, network traffic, and free disk space for critical servers (Odoo, N8N, AI service hosts, database servers).  
**Documentation:**
    
    - **Summary:** JSON definition for system health dashboard in Grafana.
    
**Namespace:** InfluenceGen.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** DashboardingConfiguration
    
- **Path:** grafana/dashboards/audit_log_review_dashboard.json  
**Description:** Grafana dashboard for visualizing key metrics and trends from audit logs (e.g., login attempts, admin actions). Requires Elasticsearch as a datasource if logs are there.  
**Template:** JSON Configuration Template (Grafana Dashboard)  
**Dependancy Level:** 0  
**Name:** audit_log_review_dashboard  
**Type:** ConfigurationFile  
**Relative Path:** grafana/dashboards/audit_log_review_dashboard.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Visualization Dashboard
    
**Requirement Ids:**
    
    - REQ-12-004
    - REQ-12-007
    - REQ-ATEL-008
    
**Purpose:** Provides a visual interface for reviewing and analyzing audit log data patterns and anomalies.  
**Logic Description:** Grafana dashboard JSON model. Panels display visualizations of audit log data, such as counts of login attempts (successful vs. failed), distribution of administrative actions, KYC status changes over time. This dashboard would typically use Elasticsearch as a datasource, querying the audit log indices.  
**Documentation:**
    
    - **Summary:** JSON definition for audit log review dashboard in Grafana.
    
**Namespace:** InfluenceGen.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** DashboardingConfiguration
    
- **Path:** grafana/dashboards/influencegen_platform_overview_dashboard.json  
**Description:** A high-level Grafana dashboard combining key metrics from Odoo, N8N, AI services, and system health for an overall platform status.  
**Template:** JSON Configuration Template (Grafana Dashboard)  
**Dependancy Level:** 0  
**Name:** influencegen_platform_overview_dashboard  
**Type:** ConfigurationFile  
**Relative Path:** grafana/dashboards/influencegen_platform_overview_dashboard.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Overall Platform Health Dashboard
    
**Requirement Ids:**
    
    - REQ-12-004
    - REQ-12-007
    
**Purpose:** Offers a consolidated view of the entire InfluenceGen platform's operational status.  
**Logic Description:** Grafana dashboard JSON model. Aggregates top-level health indicators and critical metrics from various specialized dashboards (Odoo, N8N, AI, System) into a single view for quick assessment of overall platform health.  
**Documentation:**
    
    - **Summary:** JSON definition for the main InfluenceGen platform overview dashboard in Grafana.
    
**Namespace:** InfluenceGen.Monitoring.Grafana.Dashboards  
**Metadata:**
    
    - **Category:** DashboardingConfiguration
    
- **Path:** grafana/provisioning/dashboards.yml  
**Description:** Grafana configuration for automatically provisioning dashboards defined in the grafana/dashboards/ directory.  
**Template:** YAML Configuration Template (Grafana Provisioning)  
**Dependancy Level:** 1  
**Name:** dashboards_provisioning  
**Type:** ConfigurationFile  
**Relative Path:** grafana/provisioning/dashboards.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Grafana Dashboard Provisioning
    
**Requirement Ids:**
    
    - REQ-12-004
    
**Purpose:** Automates the loading of Grafana dashboards on startup or configuration reload.  
**Logic Description:** YAML file specifying providers. Each provider points to a directory on the Grafana server's filesystem (e.g., `/etc/grafana/provisioning/dashboards` which would be mapped to `grafana/dashboards/` in this repo) containing dashboard JSON files. Defines organization ID, folder, and update interval.  
**Documentation:**
    
    - **Summary:** Configures Grafana to automatically load dashboard definitions.
    
**Namespace:** InfluenceGen.Monitoring.Grafana.Provisioning  
**Metadata:**
    
    - **Category:** DashboardingConfiguration
    
- **Path:** grafana/provisioning/datasources.yml  
**Description:** Grafana configuration for automatically provisioning datasources defined in the grafana/datasources/ directory.  
**Template:** YAML Configuration Template (Grafana Provisioning)  
**Dependancy Level:** 1  
**Name:** datasources_provisioning  
**Type:** ConfigurationFile  
**Relative Path:** grafana/provisioning/datasources.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Grafana Datasource Provisioning
    
**Requirement Ids:**
    
    - REQ-12-004
    
**Purpose:** Automates the setup of Grafana datasources.  
**Logic Description:** YAML file specifying datasource providers. Each provider points to a directory (e.g., `/etc/grafana/provisioning/datasources`) containing datasource definition files (like prometheus_datasource.json).  
**Documentation:**
    
    - **Summary:** Configures Grafana to automatically load datasource definitions.
    
**Namespace:** InfluenceGen.Monitoring.Grafana.Provisioning  
**Metadata:**
    
    - **Category:** DashboardingConfiguration
    
- **Path:** elk/logstash/pipelines/odoo_pipeline.conf  
**Description:** Logstash pipeline configuration for processing, parsing, and enriching logs originating from Odoo applications.  
**Template:** Logstash Configuration File  
**Dependancy Level:** 0  
**Name:** odoo_pipeline  
**Type:** ConfigurationFile  
**Relative Path:** elk/logstash/pipelines/odoo_pipeline.conf  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    - ETLForLogs
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Log Processing
    - Log Enrichment
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-12-002
    - REQ-ATEL-001
    - REQ-ATEL-002
    - REQ-ATEL-004
    
**Purpose:** Defines how Odoo logs are ingested, transformed, and sent to Elasticsearch.  
**Logic Description:** Logstash configuration file with `input` (e.g., Beats, syslog, file), `filter` (e.g., grok for parsing Odoo's log format, mutate for field modifications, geoip for IP enrichment, date for timestamp parsing), and `output` (Elasticsearch) sections. Ensures logs are structured and indexed correctly. Uses UTC timestamps and correlation IDs.  
**Documentation:**
    
    - **Summary:** Logstash pipeline for Odoo logs. Inputs: Raw Odoo logs. Outputs: Structured JSON logs to Elasticsearch.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Logstash  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/logstash/pipelines/n8n_pipeline.conf  
**Description:** Logstash pipeline for processing logs from N8N workflows and the N8N application itself.  
**Template:** Logstash Configuration File  
**Dependancy Level:** 0  
**Name:** n8n_pipeline  
**Type:** ConfigurationFile  
**Relative Path:** elk/logstash/pipelines/n8n_pipeline.conf  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    - ETLForLogs
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N Log Processing
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-12-002
    - REQ-ATEL-001
    - REQ-ATEL-002
    - REQ-ATEL-004
    - REQ-ATEL-010
    
**Purpose:** Defines how N8N logs are ingested, transformed, and indexed.  
**Logic Description:** Similar to odoo_pipeline.conf, but tailored for N8N's log format (often JSON). Filters parse workflow IDs, execution status, error messages, and other relevant N8N context. Includes correlation IDs.  
**Documentation:**
    
    - **Summary:** Logstash pipeline for N8N logs. Inputs: Raw N8N logs. Outputs: Structured JSON logs to Elasticsearch.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Logstash  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/logstash/pipelines/system_pipeline.conf  
**Description:** Logstash pipeline for processing generic system logs (e.g., syslog, auth.log, kernel logs) from various hosts.  
**Template:** Logstash Configuration File  
**Dependancy Level:** 0  
**Name:** system_pipeline  
**Type:** ConfigurationFile  
**Relative Path:** elk/logstash/pipelines/system_pipeline.conf  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    - ETLForLogs
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - System Log Processing
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-12-002
    - REQ-ATEL-001
    - REQ-ATEL-002
    - REQ-ATEL-004
    
**Purpose:** Centralizes processing for various system-level logs.  
**Logic Description:** Logstash configuration using appropriate input plugins (e.g., syslog, Beats) and filters (grok for common syslog formats, kv for key-value logs) to parse diverse system logs. Standardizes fields and sends to Elasticsearch.  
**Documentation:**
    
    - **Summary:** Logstash pipeline for system logs. Inputs: Various system logs. Outputs: Structured logs to Elasticsearch.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Logstash  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/logstash/pipelines/audit_log_pipeline.conf  
**Description:** Logstash pipeline specifically for processing InfluenceGen audit trail logs, ensuring all required fields are correctly parsed and indexed.  
**Template:** Logstash Configuration File  
**Dependancy Level:** 0  
**Name:** audit_log_pipeline  
**Type:** ConfigurationFile  
**Relative Path:** elk/logstash/pipelines/audit_log_pipeline.conf  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    - ETLForLogs
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Processing and Structuring
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-12-002
    - REQ-12-006
    - REQ-ATEL-001
    - REQ-ATEL-002
    - REQ-ATEL-004
    - REQ-ATEL-005
    - REQ-ATEL-006
    
**Purpose:** Ensures audit logs are accurately ingested and prepared for secure storage and review.  
**Logic Description:** Logstash pipeline with input from where audit logs are shipped (e.g., a specific file beat, kafka topic, or database poller). Filters meticulously parse structured audit log fields (timestamp, user ID, action, entity, IP, outcome, details JSON). Ensures sensitive information within 'details' is handled appropriately (e.g., not over-indexed if too verbose). Outputs to a dedicated Elasticsearch index for audit logs.  
**Documentation:**
    
    - **Summary:** Logstash pipeline for InfluenceGen audit logs. Inputs: Raw audit logs. Outputs: Structured audit logs to Elasticsearch.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Logstash  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/logstash/patterns/influencegen_patterns  
**Description:** Custom Grok patterns used in Logstash pipelines for parsing specific log formats from InfluenceGen components if standard patterns are insufficient.  
**Template:** Grok Patterns File  
**Dependancy Level:** 0  
**Name:** influencegen_patterns  
**Type:** ConfigurationFile  
**Relative Path:** elk/logstash/patterns/influencegen_patterns  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Custom Log Parsing Rules
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-ATEL-002
    
**Purpose:** Defines reusable custom patterns for log parsing in Logstash.  
**Logic Description:** A plain text file where each line defines a Grok pattern. For example: `INFLUENCEGEN_ODOLOG %{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:loglevel} ...`. These patterns are then referenced in the `grok` filter of Logstash pipelines.  
**Documentation:**
    
    - **Summary:** Custom Grok patterns for Logstash. Used by Logstash pipelines.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Logstash.Patterns  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/logstash/logstash.yml  
**Description:** Main Logstash configuration file, defining global settings, pipeline workers, and queue settings.  
**Template:** YAML Configuration Template  
**Dependancy Level:** 1  
**Name:** logstash_config  
**Type:** ConfigurationFile  
**Relative Path:** elk/logstash/logstash.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Logstash Core Configuration
    
**Requirement Ids:**
    
    - REQ-12-002
    
**Purpose:** Configures the Logstash instance itself.  
**Logic Description:** YAML file specifying settings like `path.config` (pointing to pipeline directory), `pipeline.workers`, `queue.type`, `http.host`, `http.port` for monitoring Logstash itself.  
**Documentation:**
    
    - **Summary:** Global Logstash settings.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Logstash  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/elasticsearch/index_templates/odoo_logs_template.json  
**Description:** Elasticsearch index template for Odoo logs, defining mappings, settings, and aliases for indices storing Odoo application logs.  
**Template:** JSON Configuration Template (Elasticsearch Index Template)  
**Dependancy Level:** 0  
**Name:** odoo_logs_template  
**Type:** ConfigurationFile  
**Relative Path:** elk/elasticsearch/index_templates/odoo_logs_template.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Log Index Schema
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-12-002
    - REQ-ATEL-004
    
**Purpose:** Defines the structure and settings for Elasticsearch indices that store Odoo logs.  
**Logic Description:** JSON object specifying `index_patterns` (e.g., `influencegen-odoo-logs-*`), `settings` (number of shards, replicas), and `mappings` (field data types like keyword, text, date, integer, geo_point for IP addresses). This ensures consistent indexing and searchability.  
**Documentation:**
    
    - **Summary:** Elasticsearch index template for Odoo logs.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Elasticsearch  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/elasticsearch/index_templates/n8n_logs_template.json  
**Description:** Elasticsearch index template for N8N logs.  
**Template:** JSON Configuration Template (Elasticsearch Index Template)  
**Dependancy Level:** 0  
**Name:** n8n_logs_template  
**Type:** ConfigurationFile  
**Relative Path:** elk/elasticsearch/index_templates/n8n_logs_template.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N Log Index Schema
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-12-002
    - REQ-ATEL-004
    - REQ-ATEL-010
    
**Purpose:** Defines structure for N8N log indices in Elasticsearch.  
**Logic Description:** Similar to odoo_logs_template.json, but with mappings tailored for N8N log fields (e.g., workflowName, executionId, nodeName, status).  
**Documentation:**
    
    - **Summary:** Elasticsearch index template for N8N logs.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Elasticsearch  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/elasticsearch/index_templates/system_logs_template.json  
**Description:** Elasticsearch index template for generic system logs.  
**Template:** JSON Configuration Template (Elasticsearch Index Template)  
**Dependancy Level:** 0  
**Name:** system_logs_template  
**Type:** ConfigurationFile  
**Relative Path:** elk/elasticsearch/index_templates/system_logs_template.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - System Log Index Schema
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-12-002
    - REQ-ATEL-004
    
**Purpose:** Defines structure for system log indices in Elasticsearch.  
**Logic Description:** Provides mappings for common system log fields like hostname, process, pid, severity, message.  
**Documentation:**
    
    - **Summary:** Elasticsearch index template for system logs.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Elasticsearch  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/elasticsearch/index_templates/audit_logs_template.json  
**Description:** Elasticsearch index template specifically for InfluenceGen audit logs, ensuring proper mapping for search and security analysis.  
**Template:** JSON Configuration Template (Elasticsearch Index Template)  
**Dependancy Level:** 0  
**Name:** audit_logs_template  
**Type:** ConfigurationFile  
**Relative Path:** elk/elasticsearch/index_templates/audit_logs_template.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Index Schema
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-12-002
    - REQ-12-006
    - REQ-ATEL-004
    - REQ-ATEL-005
    - REQ-ATEL-006
    
**Purpose:** Defines structure for InfluenceGen audit log indices.  
**Logic Description:** Mappings for audit log fields: timestamp (date), eventType (keyword), actorUserId (keyword), targetEntity (keyword), targetId (keyword), action (keyword), details (nested or flattened object), ipAddress (ip). Emphasizes keyword types for exact matching and aggregation.  
**Documentation:**
    
    - **Summary:** Elasticsearch index template for audit logs.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Elasticsearch  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/elasticsearch/ilm_policies/hot_warm_cold_delete_policy.json  
**Description:** Elasticsearch Index Lifecycle Management (ILM) policy for operational logs (Odoo, N8N, system). Defines phases for hot, warm, cold, and delete.  
**Template:** JSON Configuration Template (Elasticsearch ILM Policy)  
**Dependancy Level:** 0  
**Name:** hot_warm_cold_delete_policy  
**Type:** ConfigurationFile  
**Relative Path:** elk/elasticsearch/ilm_policies/hot_warm_cold_delete_policy.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Operational Log Retention Policy
    
**Requirement Ids:**
    
    - REQ-12-001
    - REQ-ATEL-004
    
**Purpose:** Manages the lifecycle of operational log indices to optimize storage and performance.  
**Logic Description:** JSON defining ILM policy with phases: `hot` (active indexing, e.g., 7 days, rollover), `warm` (less frequent access, shrink, forcemerge, e.g., after 30 days), `cold` (infrequent access, freeze, e.g., after 90 days), `delete` (e.g., after 180 days). Durations are examples and configurable based on SRS 7.3.  
**Documentation:**
    
    - **Summary:** ILM policy for operational logs in Elasticsearch.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Elasticsearch.ILM  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/elasticsearch/ilm_policies/audit_log_retention_policy.json  
**Description:** Elasticsearch ILM policy specifically for audit logs, potentially with longer retention periods and different lifecycle phases.  
**Template:** JSON Configuration Template (Elasticsearch ILM Policy)  
**Dependancy Level:** 0  
**Name:** audit_log_retention_policy  
**Type:** ConfigurationFile  
**Relative Path:** elk/elasticsearch/ilm_policies/audit_log_retention_policy.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Retention Policy
    
**Requirement Ids:**
    
    - REQ-12-006
    - REQ-ATEL-007
    
**Purpose:** Manages the lifecycle of audit log indices, ensuring compliance with longer retention needs.  
**Logic Description:** JSON defining ILM policy for audit logs. May have fewer phases (e.g., hot, delete) or different transition times. Delete phase configured for 1-7 years or as specified in SRS 7.3 and REQ-ATEL-007. Emphasis on ensuring data is not prematurely deleted.  
**Documentation:**
    
    - **Summary:** ILM policy for audit logs in Elasticsearch.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Elasticsearch.ILM  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/elasticsearch/elasticsearch.yml  
**Description:** Main Elasticsearch configuration file. Defines cluster settings, node roles, network settings, and paths. Typically managed per node, but this can store common settings or templates.  
**Template:** YAML Configuration Template  
**Dependancy Level:** 0  
**Name:** elasticsearch_config  
**Type:** ConfigurationFile  
**Relative Path:** elk/elasticsearch/elasticsearch.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Elasticsearch Cluster Configuration
    
**Requirement Ids:**
    
    - REQ-12-002
    
**Purpose:** Configures the Elasticsearch cluster behavior.  
**Logic Description:** YAML file with settings like `cluster.name`, `node.name`, `network.host`, `discovery.seed_hosts`, `path.data`, `path.logs`. Some settings are node-specific and managed by deployment automation.  
**Documentation:**
    
    - **Summary:** Core Elasticsearch configuration settings.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Elasticsearch  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/kibana/saved_objects/odoo_logs_dashboard.json  
**Description:** Exported Kibana dashboard definition for visualizing Odoo application logs.  
**Template:** JSON Configuration Template (Kibana Saved Object)  
**Dependancy Level:** 0  
**Name:** odoo_logs_dashboard_kibana  
**Type:** ConfigurationFile  
**Relative Path:** elk/kibana/saved_objects/odoo_logs_dashboard.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Log Dashboard for Kibana
    
**Requirement Ids:**
    
    - REQ-12-002
    - REQ-12-007
    
**Purpose:** Provides a pre-built dashboard in Kibana for analyzing Odoo logs.  
**Logic Description:** JSON export of a Kibana dashboard. Contains definitions for visualizations (e.g., log entry counts, error rates over time, top error messages) and their layout on the dashboard, targeting Odoo log indices.  
**Documentation:**
    
    - **Summary:** Kibana dashboard definition for Odoo logs.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Kibana  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/kibana/saved_objects/n8n_logs_dashboard.json  
**Description:** Exported Kibana dashboard definition for N8N workflow logs.  
**Template:** JSON Configuration Template (Kibana Saved Object)  
**Dependancy Level:** 0  
**Name:** n8n_logs_dashboard_kibana  
**Type:** ConfigurationFile  
**Relative Path:** elk/kibana/saved_objects/n8n_logs_dashboard.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - N8N Log Dashboard for Kibana
    
**Requirement Ids:**
    
    - REQ-12-002
    - REQ-12-007
    - REQ-ATEL-010
    
**Purpose:** Provides a Kibana dashboard for analyzing N8N logs.  
**Logic Description:** JSON export of a Kibana dashboard for N8N logs, visualizing workflow execution details, errors, and performance based on N8N log indices.  
**Documentation:**
    
    - **Summary:** Kibana dashboard definition for N8N logs.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Kibana  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/kibana/saved_objects/audit_log_search.json  
**Description:** Exported Kibana saved search or dashboard definition tailored for reviewing InfluenceGen audit logs.  
**Template:** JSON Configuration Template (Kibana Saved Object)  
**Dependancy Level:** 0  
**Name:** audit_log_search_kibana  
**Type:** ConfigurationFile  
**Relative Path:** elk/kibana/saved_objects/audit_log_search.json  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Audit Log Review Interface in Kibana
    
**Requirement Ids:**
    
    - REQ-12-007
    - REQ-ATEL-008
    
**Purpose:** Provides pre-configured views/searches in Kibana for efficient audit log review.  
**Logic Description:** JSON export of a Kibana saved search or dashboard. Includes relevant columns, default time range, and potentially pre-defined filters for common audit review tasks (e.g., filtering by user, event type, or target entity). Targets the audit log index.  
**Documentation:**
    
    - **Summary:** Kibana saved search/dashboard for audit logs.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Kibana  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** elk/kibana/kibana.yml  
**Description:** Main Kibana configuration file. Defines settings like Elasticsearch host, server port, and default index patterns.  
**Template:** YAML Configuration Template  
**Dependancy Level:** 0  
**Name:** kibana_config  
**Type:** ConfigurationFile  
**Relative Path:** elk/kibana/kibana.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Kibana Core Configuration
    
**Requirement Ids:**
    
    - REQ-12-002
    
**Purpose:** Configures the Kibana instance.  
**Logic Description:** YAML file specifying settings like `server.port`, `server.host`, `elasticsearch.hosts`, `kibana.index` (for Kibana's own metadata), and potentially `elasticsearch.username` and `elasticsearch.password` if security is enabled.  
**Documentation:**
    
    - **Summary:** Core Kibana configuration settings.
    
**Namespace:** InfluenceGen.Monitoring.ELK.Kibana  
**Metadata:**
    
    - **Category:** LoggingConfiguration
    
- **Path:** common/global_settings.yml  
**Description:** Shared global settings or variables that might be referenced by multiple monitoring tool configurations (e.g., environment name, common labels, default notification email).  
**Template:** YAML Configuration Template  
**Dependancy Level:** 0  
**Name:** global_settings  
**Type:** ConfigurationFile  
**Relative Path:** common/global_settings.yml  
**Repository Id:** REPO-IGMON-009  
**Pattern Ids:**
    
    - ConfigurationManagement
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Centralized Common Configuration Values
    
**Requirement Ids:**
    
    - REQ-12-009
    - REQ-16-010
    
**Purpose:** Provides a single source for common variables used across monitoring configurations.  
**Logic Description:** YAML file containing key-value pairs for global settings. For example: `environment: production`, `default_alert_email: ops@example.com`, `critical_severity_label: P1`. These can be templated into other configuration files during deployment or by the tools themselves if supported.  
**Documentation:**
    
    - **Summary:** Global variables for monitoring configurations.
    
**Namespace:** InfluenceGen.Monitoring.Common  
**Metadata:**
    
    - **Category:** MonitoringConfiguration
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enable_odoo_application_alerts
  - enable_n8n_workflow_failure_alerts
  - enable_ai_service_latency_alerts
  - enable_system_resource_critical_alerts
  - enable_audit_log_security_event_alerts
  - enable_pagerduty_notifications_for_p1
  - enable_slack_notifications_for_p2
  
- **Database Configs:**
  
  - prometheus_server_address
  - elasticsearch_connection_url_for_grafana_datasource
  - elasticsearch_output_url_for_logstash
  - alertmanager_api_url
  


---

