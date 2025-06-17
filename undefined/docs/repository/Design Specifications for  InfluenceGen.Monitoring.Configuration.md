markdown
# Software Design Specification: InfluenceGen.Monitoring.Configuration

## 1. Introduction

This document outlines the software design specification for the `InfluenceGen.Monitoring.Configuration` repository. This repository is responsible for storing and managing all configuration files for the monitoring, logging, and alerting systems used by the InfluenceGen platform. Its primary purpose is to centralize operational visibility setup, ensuring that all logging, monitoring, and observability requirements are met through version-controlled configurations.

The key technologies involved are Prometheus (for metrics collection and alerting), Alertmanager (for alert routing), Grafana (for dashboarding and visualization), and the ELK Stack (Elasticsearch, Logstash, Kibana) for centralized logging and log analysis. Integration configurations for tools like PagerDuty are also included.

## 2. System Overview

The `InfluenceGen.Monitoring.Configuration` repository acts as a single source of truth for how the InfluenceGen platform's various components (Odoo, N8N, AI Services) are monitored, how their logs are processed, and how alerts are triggered and routed.

**Key components configured by this repository:**

*   **Prometheus:** Scrapes metrics from various targets, evaluates alerting rules.
*   **Alertmanager:** Receives alerts from Prometheus and routes them to appropriate notification channels.
*   **Grafana:** Connects to Prometheus (and potentially Elasticsearch) to display dashboards visualizing system health and performance.
*   **Logstash:** Ingests logs from different sources, parses, transforms, and forwards them to Elasticsearch.
*   **Elasticsearch:** Stores and indexes log data for searching and analysis.
*   **Kibana:** Provides a UI for querying, visualizing, and managing data in Elasticsearch, including logs and audit trails.

This repository does not contain executable code but rather configuration files that define the behavior of these external monitoring and logging tools.

## 3. Requirements Mapping

This repository directly supports the following high-level requirements:

*   **REQ-12-001 to REQ-12-009 (System Operations, Monitoring & Alerting Infrastructure):** Configurations for logging, metrics collection, dashboards, alerting, and audit log infrastructure.
*   **REQ-16-008 to REQ-16-012 (System Notification Management - for Alerts):** Configuration of alert conditions, routing, and notification channels.
*   **REQ-ATEL-001 to REQ-ATEL-011 (Audit Trail & Event Logging System):** Configurations for log processing, audit log indexing, retention, and review interfaces (via Kibana/Grafana dashboards).

## 4. Design Considerations

*   **Version Control:** All configuration files are to be strictly version-controlled using Git, following defined branching strategies and commit guidelines (REQ-DDSI-002).
*   **Environment Specificity:** Configurations should be structured to allow for environment-specific overrides (e.g., different scrape targets or alert thresholds for dev, staging, prod). This might involve separate files per environment or templating mechanisms if supported by deployment tools. For this SDS, we will assume a base configuration with placeholders or comments indicating where environment-specific values would be injected.
*   **Secrets Management:** Sensitive information (API keys, passwords) **MUST NOT** be stored directly in these configuration files. Placeholders or references to environment variables/secrets management systems should be used.
*   **Modularity:** Configurations are broken down into logical files (e.g., per service for Prometheus rules, per pipeline for Logstash) for better organization and maintainability.
*   **Idempotency:** Where possible, configurations should be designed such that applying them multiple times results in the same state.
*   **Validation:** While not part of this repository, the deployment process for these configurations should include validation steps (e.g., `promtool check rules`, `logstash -t`).

## 5. File Structure and Specifications

The file structure provided in the repository definition will be adhered to. Detailed specifications for each configuration file are as follows:

### 5.1. Prometheus (`prometheus/`)

#### 5.1.1. `prometheus/prometheus.yml`

*   **Purpose:** Main Prometheus server configuration.
*   **LogicDescription:**
    *   `global`:
        *   `scrape_interval`: e.g., `15s` (REQ-12-003)
        *   `evaluation_interval`: e.g., `15s`
    *   `rule_files`:
        *   `- /etc/prometheus/rules/odoo_rules.yml`
        *   `- /etc/prometheus/rules/n8n_rules.yml`
        *   `- /etc/prometheus/rules/ai_service_rules.yml`
        *   `- /etc/prometheus/rules/system_rules.yml`
        *   `- /etc/prometheus/rules/audit_log_rules.yml`
    *   `scrape_configs`:
        *   **Job: `odoo-apps`** (REQ-12-003, REQ-ATEL-001)
            *   `job_name: 'odoo'`
            *   `metrics_path: /metrics` (assuming Odoo exposes metrics here, may need custom exporter)
            *   `file_sd_configs`:
                *   `files: ['/etc/prometheus/targets/odoo_targets.json']`
        *   **Job: `n8n-instances`** (REQ-12-003, REQ-ATEL-001, REQ-ATEL-010)
            *   `job_name: 'n8n'`
            *   `metrics_path: /metrics` (N8N exposes Prometheus metrics by default)
            *   `file_sd_configs`:
                *   `files: ['/etc/prometheus/targets/n8n_targets.json']`
        *   **Job: `ai-service`** (REQ-12-003, REQ-ATEL-001)
            *   `job_name: 'ai-service'`
            *   `metrics_path: /metrics` (assuming AI service or its proxy exposes metrics)
            *   `file_sd_configs`:
                *   `files: ['/etc/prometheus/targets/ai_service_targets.json']`
        *   **Job: `node-exporter`** (REQ-12-003)
            *   `job_name: 'node'`
            *   `static_configs` or `file_sd_configs` to scrape node_exporter instances on Odoo, N8N, AI hosts.
        *   **Job: `database-exporter`** (REQ-12-003)
            *   `job_name: 'database'`
            *   `static_configs` or `file_sd_configs` to scrape PostgreSQL (or other DB) exporters.
        *   **Job: `prometheus`**
            *   `job_name: 'prometheus'`
            *   `static_configs`:
                *   `targets: ['localhost:9090']`
    *   `alerting`:
        *   `alertmanagers`:
            *   `static_configs`:
                *   `targets: ['alertmanager:9093']` (Alertmanager service name and port)

#### 5.1.2. Prometheus Rules (`prometheus/rules/`)

General structure for all `.yml` rule files:

yaml
groups:
  - name: <GroupName> # e.g., OdooHighErrorRate
    rules:
      - alert: <AlertName> # e.g., OdooHttpErrorRateTooHigh
        expr: <PromQL_Expression> # e.g., sum(rate(odoo_http_requests_total{status=~"5.."}[5m])) / sum(rate(odoo_http_requests_total[5m])) * 100 > 5
        for: <Duration> # e.g., 5m
        labels:
          severity: <critical|warning|info|P1|P2|P3> # (REQ-12-009, REQ-16-010)
          component: <odoo|n8n|ai_service|system|audit>
          service: <specific_service_name_if_applicable>
        annotations:
          summary: "High HTTP error rate on Odoo instance {{ $labels.instance }}"
          description: "Odoo instance {{ $labels.instance }} is experiencing an error rate of {{ $value | printf \"%.2f\" }}% for the last 5 minutes. (REQ-12-008, REQ-16-009)"
          runbook_url: "http://internal.wiki/runbooks/odoo-high-error-rate" # Optional


*   **`prometheus/rules/odoo_rules.yml`** (REQ-12-003, REQ-12-008, REQ-16-009)
    *   **Alerts:**
        *   `OdooRequestLatencyHigh`: High request latency (e.g., `histogram_quantile(0.95, sum(rate(odoo_http_request_duration_seconds_bucket[5m])) by (le, instance)) > 1`).
        *   `OdooHttpErrorRateHigh`: High HTTP 5xx error rate.
        *   `OdooWorkerSaturation`: Odoo worker processes nearing saturation.
        *   `OdooDatabaseConnectionErrors`: Errors connecting to the database.
        *   `InfluenceGenCampaignProcessingError`: (If specific business metrics are exported) Errors in critical InfluenceGen campaign processing tasks.
        *   `InfluenceGenKYCQueueHigh`: (If specific business metrics are exported) High number of pending KYC reviews.
*   **`prometheus/rules/n8n_rules.yml`** (REQ-12-003, REQ-12-008, REQ-16-009, REQ-ATEL-010)
    *   **Alerts:**
        *   `N8NWorkflowExecutionFailureRateHigh`: High failure rate for specific critical N8N workflows.
        *   `N8NWorkflowExecutionDurationHigh`: N8N workflows taking too long to execute.
        *   `N8NQueueDepthHigh`: N8N execution queue depth is too high.
        *   `N8NInstanceDown`: N8N instance unresponsive.
        *   `N8NOdooCallbackFailureHigh`: High rate of failures when N8N calls back to Odoo (requires N8N to expose such metrics or derive from N8N logs). (REQ-16-009, REQ-16-011)
*   **`prometheus/rules/ai_service_rules.yml`** (REQ-12-003, REQ-12-008, REQ-16-009)
    *   **Alerts:**
        *   `AIServiceRequestLatencyHigh`: High latency for AI image generation requests.
        *   `AIServiceErrorRateHigh`: High error rate from the AI service API.
        *   `AIServiceUnavailable`: AI service endpoint unresponsive.
        *   `AIGenerationSuccessRateLow`: Low success rate for AI image generation.
        *   `AIServiceQuotaApproaching`: (If metrics available) AI service usage approaching quota limits.
*   **`prometheus/rules/system_rules.yml`** (REQ-12-003, REQ-12-008, REQ-16-009)
    *   **Alerts:**
        *   `HostHighCpuLoad`: High CPU load on critical hosts.
        *   `HostHighMemoryUsage`: High memory usage.
        *   `HostDiskSpaceLow`: Low disk space.
        *   `HostNetworkSaturation`: High network traffic/saturation.
        *   `HostDown`: Host instance unresponsive (e.g., `up == 0`).
        *   `DatabaseDown`: Database server unresponsive.
        *   `DatabaseReplicationLagHigh`: High database replication lag (if applicable). (REQ-16-009)
        *   `SSLCertificateExpiresSoon`: SSL certificates nearing expiry (e.g., `probe_ssl_earliest_cert_expiry - time() < 14 * 24 * 3600`). (REQ-16-009)
        *   `BackupJobFailed`: Critical backup job failure (requires metrics from backup system). (REQ-16-009)
*   **`prometheus/rules/audit_log_rules.yml`** (REQ-12-008, REQ-16-009, REQ-ATEL-005)
    *   **Note:** These rules depend on metrics being exported from the ELK stack or a custom audit log metrics exporter.
    *   **Alerts:**
        *   `HighRateOfFailedLogins`: Excessive failed login attempts for a user or globally.
        *   `SuspiciousAdminActivity`: Potentially suspicious administrative actions (e.g., rapid permission changes).
        *   `SensitiveDataExportDetected`: High volume of sensitive data export events.
        *   `MultipleKYCRejectionsForUser`: Multiple KYC rejections for the same user in a short period.
        *   `AuditLogIngestionLagHigh`: Significant delay in audit logs appearing in Elasticsearch (if this metric is available).

#### 5.1.3. Prometheus Targets (`prometheus/targets/`)

These JSON files define static targets for Prometheus scraping. In a dynamic environment, these could be managed by a service discovery mechanism (e.g., Consul, Kubernetes SD) or generated by configuration management tools.

*   **`prometheus/targets/odoo_targets.json`**
    json
    [
      {
        "targets": ["odoo-prod-instance1:8069", "odoo-prod-instance2:8069"], // Placeholder, actual host:port for Odoo metrics
        "labels": {
          "env": "production",
          "app": "odoo",
          "service": "influencegen_app"
        }
      },
      {
        "targets": ["odoo-staging-instance1:8069"],
        "labels": {
          "env": "staging",
          "app": "odoo",
          "service": "influencegen_app"
        }
      }
    ]
    
*   **`prometheus/targets/n8n_targets.json`**
    json
    [
      {
        "targets": ["n8n-prod-instance1:5678"], // Placeholder, actual host:port for N8N metrics
        "labels": {
          "env": "production",
          "app": "n8n"
        }
      }
    ]
    
*   **`prometheus/targets/ai_service_targets.json`**
    json
    [
      {
        "targets": ["ai-service-metrics-proxy:9100"], // Placeholder, host:port for AI service metrics (or its exporter)
        "labels": {
          "env": "production",
          "app": "ai_service"
        }
      }
    ]
    
    *(Similar files for `node_exporter_targets.json`, `db_exporter_targets.json` if using file_sd for them)*

### 5.2. Alertmanager (`alertmanager/`)

#### 5.2.1. `alertmanager/alertmanager.yml`

*   **Purpose:** Main Alertmanager configuration.
*   **LogicDescription:** (REQ-12-008, REQ-12-009, REQ-16-008, REQ-16-010)
    yaml
    global:
      resolve_timeout: 5m
      # smtp_smarthost, smtp_from, etc. for email, if not defined per receiver
      # slack_api_url, pagerduty_url - actual secrets via env vars or secrets manager
      # Example:
      # smtp_smarthost: 'smtp.example.com:587'
      # smtp_from: 'alertmanager@influencegen.com'
      # smtp_auth_username: 'alertmanager_user'
      # smtp_auth_password: ${SMTP_PASSWORD} # Injected from environment

    route:
      group_by: ['alertname', 'component', 'service']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 1h
      receiver: 'default-receiver' # Catch-all
      routes:
        - receiver: 'critical-pagerduty-receiver'
          matchers:
            - severity =~ "critical|P1"
          continue: true # Allows multiple receivers for critical alerts if needed
        - receiver: 'warning-slack-receiver'
          matchers:
            - severity =~ "warning|P2"
        - receiver: 'info-email-receiver'
          matchers:
            - severity =~ "info|P3"
        # Specific component routing if needed
        - receiver: 'odoo-team-email'
          matchers:
            - component == "odoo"
            - severity =~ "warning|critical"
          # Add more specific routes as needed

    receivers:
      - name: 'default-receiver'
        email_configs:
          - to: 'ops-catchall@influencegen.com'
            send_resolved: true
            html: '{{ template "default_template.tmpl" . }}'
            headers:
              Subject: '[InfluenceGen ALERT] {{ .CommonLabels.alertname }} ({{ .Status }})'

      - name: 'critical-pagerduty-receiver' # (REQ-16-010)
        pagerduty_configs:
          - service_key: ${PAGERDUTY_SERVICE_KEY_CRITICAL} # Injected
            send_resolved: true
            client: 'InfluenceGen Alertmanager'
            client_url: '{{ .ExternalURL }}'
            description: '{{ template "pagerduty.default.description" . }}' # Uses Alertmanager's default or custom
            severity: '{{ if .CommonLabels.severity }}{{ .CommonLabels.severity | toLower }}{{ else }}critical{{ end }}'
            details:
              firing: '{{ template "default_template.tmpl" . }}'

      - name: 'warning-slack-receiver' # (REQ-16-010)
        slack_configs:
          - api_url: ${SLACK_WEBHOOK_URL_WARNINGS} # Injected
            channel: '#influencegen-alerts-warning'
            send_resolved: true
            title: '[{{ .Status | toUpper }}] {{ .CommonLabels.alertname }} for {{ .CommonLabels.component }}'
            text: '{{ template "slack.default.text" . }}' # Uses Alertmanager's default or custom

      - name: 'info-email-receiver'
        email_configs:
          - to: 'ops-info@influencegen.com'
            send_resolved: true
            html: '{{ template "default_template.tmpl" . }}'
            headers:
              Subject: '[InfluenceGen INFO] {{ .CommonLabels.alertname }} ({{ .Status }})'
      
      - name: 'odoo-team-email'
        email_configs:
          - to: 'odoo-dev-alerts@influencegen.com'
            send_resolved: true
            html: '{{ template "default_template.tmpl" . }}'
            headers:
              Subject: '[Odoo ALERT] {{ .CommonLabels.alertname }} ({{ .Status }})'

    templates:
      - '/etc/alertmanager/templates/*.tmpl'

    # inhibit_rules:
    # - target_matchers:
    #     severity: 'warning'
    #   source_matchers:
    #     severity: 'critical'
    #   equal: ['alertname', 'instance']
    

#### 5.2.2. Alertmanager Templates (`alertmanager/templates/`)

*   **`alertmanager/templates/default_template.tmpl`** (REQ-12-009, REQ-16-010)
    *   **Purpose:** Formats alert notifications.
    *   **LogicDescription:**
        html
        {{ define "default_template.tmpl" }}
        {{ range .Alerts }}
        <b>Alert:</b> {{ .Labels.alertname }} ({{ .Status }})<br>
        <b>Severity:</b> {{ .Labels.severity | default "N/A" }}<br>
        <b>Component:</b> {{ .Labels.component | default "N/A" }}<br>
        {{ if .Labels.service }}<b>Service:</b> {{ .Labels.service }}<br>{{ end }}
        {{ if .Labels.instance }}<b>Instance:</b> {{ .Labels.instance }}<br>{{ end }}
        <b>Summary:</b> {{ .Annotations.summary }}<br>
        <b>Description:</b> {{ .Annotations.description }}<br>
        <b>Starts At:</b> {{ .StartsAt.Format "2006-01-02 15:04:05 MST" }}<br>
        {{ if .EndsAt.IsZero | not }}<b>Ends At:</b> {{ .EndsAt.Format "2006-01-02 15:04:05 MST" }}<br>{{ end }}
        <hr>
        {{ end }}
        {{ end }}

        {{ define "slack.default.text" }}
        {{ range .Alerts }}
        *Summary:* {{ .Annotations.summary }}
        *Description:* {{ .Annotations.description }}
        {{ end }}
        {{ end }}

        {{ define "pagerduty.default.description" }}
        {{ range .Alerts }}
        {{ .Annotations.summary }} - {{ .Annotations.description }}
        {{ end }}
        {{ end }}
        

#### 5.2.3. Alertmanager Integrations (`alertmanager/integrations/`)

*   **`alertmanager/integrations/pagerduty_config.json`** (REQ-12-009, REQ-16-010)
    *   **Purpose:** Placeholder for non-sensitive PagerDuty settings.
    *   **LogicDescription:**
        json
        {
          "default_escalation_policy_id": "PXXXXXX", // Example, if needed for some custom logic
          "notes": "Actual PagerDuty service/routing keys are injected via environment variables (e.g., PAGERDUTY_SERVICE_KEY_CRITICAL) and used in alertmanager.yml"
        }
        
        **Note:** This file is largely illustrative, as primary PagerDuty config (service keys) is in `alertmanager.yml` and sourced from secrets.

### 5.3. Grafana (`grafana/`)

#### 5.3.1. Grafana Datasources (`grafana/datasources/`)

*   **`grafana/datasources/prometheus_datasource.json`** (REQ-12-004)
    json
    {
        "apiVersion": 1,
        "datasources": [
            {
                "name": "InfluenceGen Prometheus",
                "type": "prometheus",
                "url": "http://prometheus:9090", // Prometheus service name and port
                "access": "server",
                "isDefault": true,
                "jsonData": {
                    "timeInterval": "15s"
                },
                "readOnly": false
            },
            {
                "name": "InfluenceGen Elasticsearch Logs",
                "type": "elasticsearch",
                "url": "http://elasticsearch:9200", // Elasticsearch service name and port
                "access": "server",
                "jsonData": {
                    "timeField": "@timestamp",
                    "esVersion": "8.0.0", // Adjust to match ES version
                    "logMessageField": "message",
                    "logLevelField": "log.level"
                },
                "database": "[influencegen-*-logs-*]YYYY.MM.DD", // Example index pattern for operational logs
                "readOnly": false
            },
            {
                "name": "InfluenceGen Audit Logs",
                "type": "elasticsearch",
                "url": "http://elasticsearch:9200",
                "access": "server",
                "jsonData": {
                    "timeField": "timestamp", // As per AuditLog table
                    "esVersion": "8.0.0"
                },
                "database": "[influencegen-audit-logs-*]YYYY.MM.DD", // Example index pattern for audit logs
                "readOnly": false
            }
        ]
    }
    

#### 5.3.2. Grafana Dashboards (`grafana/dashboards/`)

All dashboard JSON files are Grafana Dashboard JSON Models. They will contain `panels`, `templating` (for variables), `timepicker` settings, etc. The `expr` in panels will use PromQL for Prometheus datasources or Lucene/KQL for Elasticsearch datasources.

*   **`grafana/dashboards/odoo_overview_dashboard.json`** (REQ-12-004, REQ-12-007)
    *   **Key Panels:**
        *   Request Rate (per instance, total)
        *   Error Rate (HTTP 5xx, 4xx)
        *   Average Request Latency (p95, p99)
        *   Active User Sessions
        *   Odoo Worker Utilization
        *   Database Query Performance (if Odoo exporter provides)
        *   Specific InfluenceGen business metrics (e.g., new registrations, campaign applications)
*   **`grafana/dashboards/n8n_workflow_dashboard.json`** (REQ-12-004, REQ-12-007, REQ-ATEL-010)
    *   **Key Panels:**
        *   Workflow Execution Count (total, per workflow)
        *   Workflow Success/Error Rate (per workflow)
        *   Average Workflow Execution Duration (per workflow)
        *   N8N Worker Queue Status
        *   Odoo Callback Success/Failure Rate (if available as metric)
*   **`grafana/dashboards/ai_service_performance_dashboard.json`** (REQ-12-004, REQ-12-007)
    *   **Key Panels:**
        *   AI Image Generation Request Volume
        *   Average AI Request Latency (end-to-end)
        *   AI Service API Error Rate
        *   Image Generation Success vs. Failure Rate
        *   Breakdown by AI Model Used (if applicable)
*   **`grafana/dashboards/system_health_dashboard.json`** (REQ-12-004, REQ-12-007)
    *   **Key Panels (per host/service type):**
        *   CPU Utilization (%)
        *   Memory Utilization (%)
        *   Disk Space Used/Free (%)
        *   Disk I/O Operations
        *   Network Traffic (In/Out)
        *   Database Connections, Replication Lag
*   **`grafana/dashboards/audit_log_review_dashboard.json`** (REQ-12-004, REQ-12-007, REQ-ATEL-008)
    *   **Datasource:** InfluenceGen Audit Logs (Elasticsearch)
    *   **Key Panels:**
        *   Timeline of Audit Events
        *   Top Event Types
        *   Top Users Performing Actions
        *   Failed Login Attempts
        *   Admin Actions Overview
        *   Table view of recent audit logs with filtering capabilities (User ID, Event Type, Target Entity, Date Range).
*   **`grafana/dashboards/influencegen_platform_overview_dashboard.json`** (REQ-12-004, REQ-12-007)
    *   **Key Panels:** Aggregated health status indicators from Odoo, N8N, AI Service, and System dashboards.
        *   Overall Odoo App Health (e.g., green/yellow/red based on key metrics)
        *   Overall N8N Workflow Health
        *   Overall AI Service Health
        *   Critical System Resource Alerts Summary
        *   Recent High-Severity Alerts

#### 5.3.3. Grafana Provisioning (`grafana/provisioning/`)

*   **`grafana/provisioning/dashboards.yml`** (REQ-12-004)
    yaml
    apiVersion: 1

    providers:
      - name: 'InfluenceGenDashboards'
        orgId: 1
        folder: 'InfluenceGen Platform'
        type: file
        disableDeletion: false
        editable: true
        options:
          path: /etc/grafana/provisioning/dashboards/influencegen # This path inside Grafana container maps to grafana/dashboards/
    
*   **`grafana/provisioning/datasources.yml`** (REQ-12-004)
    yaml
    apiVersion: 1

    datasources:
      - name: 'InfluenceGen Prometheus' # Must match name in prometheus_datasource.json
        type: prometheus
        url: http://prometheus:9090
        access: server
        isDefault: true
        jsonData:
          timeInterval: "15s"
        editable: true # Allow UI edits if needed, or set to false for fully IaC
      - name: 'InfluenceGen Elasticsearch Logs' # Must match name in prometheus_datasource.json
        type: elasticsearch
        url: http://elasticsearch:9200
        access: server
        jsonData:
          timeField: "@timestamp"
          esVersion: "8.0.0"
          logMessageField: "message"
          logLevelField: "log.level"
        database: "[influencegen-*-logs-*]YYYY.MM.DD"
        editable: true
      - name: 'InfluenceGen Audit Logs' # Must match name in prometheus_datasource.json
        type: elasticsearch
        url: http://elasticsearch:9200
        access: server
        jsonData:
          timeField: "timestamp"
          esVersion: "8.0.0"
        database: "[influencegen-audit-logs-*]YYYY.MM.DD"
        editable: true

    # If you want to load from files placed in grafana/datasources, structure would be:
    # deleteDatasources:
    #   - name: Prometheus # Old datasource to delete
    #     orgId: 1
    # providers:
    # - name: 'default'
    #   orgId: 1
    #   folder: ''
    #   type: file
    #   disableDeletion: false
    #   editable: true
    #   options:
    #     path: /etc/grafana/provisioning/datasources # Maps to grafana/datasources/
    
    *Note on Grafana Datasource Provisioning: The `datasources.yml` above directly defines datasources. Alternatively, it can point to a directory of JSON files like `grafana/datasources/prometheus_datasource.json`. The direct definition is often simpler for a few datasources.*


### 5.4. ELK Stack (`elk/`)

#### 5.4.1. Logstash Pipelines (`elk/logstash/pipelines/`)

General structure for Logstash `.conf` files:

logstash
input {
  # Input plugin configuration (e.g., beats, tcp, udp, syslog, file)
}

filter {
  # Filter plugin configurations (grok, mutate, date, geoip, json, kv)
  # Ensure UTC timestamping and correlation ID handling (REQ-12-001, REQ-ATEL-002)
  # Example:
  # if [correlation_id] {
  #   mutate { add_field => { "trace.id" => "%{[correlation_id]}" } } # If using OpenTelemetry trace IDs
  # }
  # date { match => ["timestamp_field", "ISO8601"] target => "@timestamp" }
}

output {
  elasticsearch {
    hosts => ["http://elasticsearch:9200"] // Elasticsearch service name and port
    index => "influencegen-%{[app_name]}-logs-%{+YYYY.MM.dd}" // Dynamic index name
    user => "${ES_USER}" // Injected
    password => "${ES_PASSWORD}" // Injected
    # manage_template => false # If templates are managed externally via API/Kibana Dev Tools
    # template => "/usr/share/logstash/config/index_templates/my_template.json" # Path to ES template if Logstash manages it
    # template_name => "my_template_name"
    # template_overwrite => true
  }
  # stdout { codec => rubydebug } # For debugging
}


*   **`elk/logstash/pipelines/odoo_pipeline.conf`** (REQ-12-001, REQ-12-002, REQ-ATEL-001, REQ-ATEL-002, REQ-ATEL-004)
    *   **Input:** Beats input from Filebeat on Odoo hosts, or direct TCP/UDP if Odoo logs there.
    *   **Filter:**
        *   Grok to parse Odoo's specific log format (multiline for tracebacks). Reference `influencegen_patterns`.
        *   Mutate to rename/add fields (e.g., `app_name: "odoo"`).
        *   Date filter to parse Odoo's timestamp and set `@timestamp` in UTC.
        *   Extract `correlation_id` if present in Odoo logs.
    *   **Output:** Elasticsearch, index `influencegen-odoo-logs-%{+YYYY.MM.dd}`.
*   **`elk/logstash/pipelines/n8n_pipeline.conf`** (REQ-12-001, REQ-12-002, REQ-ATEL-001, REQ-ATEL-002, REQ-ATEL-004, REQ-ATEL-010)
    *   **Input:** Beats input from Filebeat on N8N hosts, or direct TCP/UDP if N8N logs there. N8N often logs in JSON.
    *   **Filter:**
        *   JSON filter if logs are in JSON format.
        *   Mutate to add `app_name: "n8n"`.
        *   Date filter to parse N8N's timestamp and set `@timestamp` in UTC.
        *   Extract N8N `workflowId`, `executionId`, `nodeName`, `correlation_id`.
    *   **Output:** Elasticsearch, index `influencegen-n8n-logs-%{+YYYY.MM.dd}`.
*   **`elk/logstash/pipelines/system_pipeline.conf`** (REQ-12-001, REQ-12-002, REQ-ATEL-001, REQ-ATEL-002, REQ-ATEL-004)
    *   **Input:** Syslog input or Beats from various system hosts.
    *   **Filter:**
        *   Grok for common syslog formats.
        *   Mutate to add `app_name: "system"`, extract hostname.
        *   Date filter.
    *   **Output:** Elasticsearch, index `influencegen-system-logs-%{+YYYY.MM.dd}`.
*   **`elk/logstash/pipelines/audit_log_pipeline.conf`** (REQ-12-001, REQ-12-002, REQ-12-006, REQ-ATEL-001, REQ-ATEL-002, REQ-ATEL-004, REQ-ATEL-005, REQ-ATEL-006)
    *   **Input:** Beats input from where Odoo writes structured audit logs (e.g., a specific file or DB poller output). Assume audit logs are JSON.
    *   **Filter:**
        *   JSON filter.
        *   Mutate to add `app_name: "audit"`.
        *   Date filter for `timestamp` field, target `@timestamp`.
        *   Ensure all fields from REQ-ATEL-006 (`eventType`, `actorUserId`, `targetEntity`, `targetId`, `action`, `details`, `ipAddress`) are correctly mapped.
    *   **Output:** Elasticsearch, index `influencegen-audit-logs-%{+YYYY.MM.dd}`.

#### 5.4.2. Logstash Patterns (`elk/logstash/patterns/`)

*   **`elk/logstash/patterns/influencegen_patterns`** (REQ-12-001, REQ-ATEL-002)
    *   Contains custom Grok patterns for Odoo or other non-standard log formats.
    *   Example for Odoo:
        grok
        ODOO_LOG_LINE %{TIMESTAMP_ISO8601:odoo_timestamp} %{NUMBER:pid} %{LOGLEVEL:loglevel} %{DATA:dbname} %{GREEDYDATA:message}
        # Add more complex multiline patterns if needed for tracebacks
        

#### 5.4.3. `elk/logstash/logstash.yml`

*   **Purpose:** Main Logstash configuration.
*   **LogicDescription:**
    yaml
    http.host: "0.0.0.0"
    # path.config: /usr/share/logstash/pipeline # Points to directory containing .conf files
    # pipeline.workers: # Number of CPU cores
    # queue.type: persisted
    # Add other relevant global settings
    
    **Note:** Pipeline configurations are typically managed via `pipelines.yml` in modern Logstash, or by placing `.conf` files in the `path.config` directory if using a single pipeline. For multiple pipelines as defined, `pipelines.yml` is preferred:
    yaml
    # pipelines.yml example
    - pipeline.id: odoo
      path.config: "/usr/share/logstash/pipelines/odoo_pipeline.conf"
    - pipeline.id: n8n
      path.config: "/usr/share/logstash/pipelines/n8n_pipeline.conf"
    - pipeline.id: system
      path.config: "/usr/share/logstash/pipelines/system_pipeline.conf"
    - pipeline.id: audit
      path.config: "/usr/share/logstash/pipelines/audit_log_pipeline.conf"
    

#### 5.4.4. Elasticsearch Index Templates (`elk/elasticsearch/index_templates/`)

General structure for index template JSON:

json
{
  "index_patterns": ["influencegen-<log_type>-logs-*"], // e.g., influencegen-odoo-logs-*
  "template": {
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "index.lifecycle.name": "<ilm_policy_name>", // e.g., operational_log_policy
      "index.lifecycle.rollover_alias": "influencegen-<log_type>-logs" // For rollover
    },
    "mappings": {
      "_source": { "enabled": true },
      "properties": {
        "@timestamp": { "type": "date" },
        "message": { "type": "text" },
        "log.level": { "type": "keyword" },
        "app_name": { "type": "keyword" },
        "host.name": { "type": "keyword" },
        "trace.id": { "type": "keyword" }, // For correlation ID
        // ... other common fields
        // ... specific fields for this log_type
      }
    },
    "aliases": {
      "influencegen-<log_type>-logs-read": {} // Example read alias
    }
  }
}


*   **`elk/elasticsearch/index_templates/odoo_logs_template.json`** (REQ-12-001, REQ-12-002, REQ-ATEL-004)
    *   `index_patterns`: `["influencegen-odoo-logs-*"]`
    *   `settings.index.lifecycle.name`: `operational_log_policy`
    *   `mappings`: Specific fields for Odoo logs (e.g., `odoo_timestamp`, `pid`, `dbname`, parsed fields from message).
*   **`elk/elasticsearch/index_templates/n8n_logs_template.json`** (REQ-12-001, REQ-12-002, REQ-ATEL-004, REQ-ATEL-010)
    *   `index_patterns`: `["influencegen-n8n-logs-*"]`
    *   `settings.index.lifecycle.name`: `operational_log_policy`
    *   `mappings`: Specific fields for N8N logs (e.g., `workflowName`, `workflowId`, `executionId`, `nodeName`, `status`).
*   **`elk/elasticsearch/index_templates/system_logs_template.json`** (REQ-12-001, REQ-12-002, REQ-ATEL-004)
    *   `index_patterns`: `["influencegen-system-logs-*"]`
    *   `settings.index.lifecycle.name`: `operational_log_policy`
    *   `mappings`: Common syslog fields.
*   **`elk/elasticsearch/index_templates/audit_logs_template.json`** (REQ-12-001, REQ-12-002, REQ-12-006, REQ-ATEL-004, REQ-ATEL-005, REQ-ATEL-006)
    *   `index_patterns`: `["influencegen-audit-logs-*"]`
    *   `settings.index.lifecycle.name`: `audit_log_retention_policy`
    *   `mappings`:
        *   `timestamp`: `{ "type": "date" }` (ensure this matches the field name from audit log source)
        *   `eventType`: `{ "type": "keyword" }`
        *   `actorUserId`: `{ "type": "keyword" }`
        *   `targetEntity`: `{ "type": "keyword" }`
        *   `targetId`: `{ "type": "keyword" }`
        *   `action`: `{ "type": "keyword" }`
        *   `details`: `{ "type": "object", "dynamic": true, "enabled": true }` (or flattened if structure is known and simpler)
        *   `ipAddress`: `{ "type": "ip" }`
        *   `outcome`: `{ "type": "keyword" }`

#### 5.4.5. Elasticsearch ILM Policies (`elk/elasticsearch/ilm_policies/`)

*   **`elk/elasticsearch/ilm_policies/hot_warm_cold_delete_policy.json`** (REQ-12-001, REQ-ATEL-004)
    *   Name: `operational_log_policy`
    *   **Phases:**
        *   `hot`:
            *   `actions`: `{ "rollover": { "max_size": "50gb", "max_age": "7d" } }`
        *   `warm`:
            *   `min_age`: `30d`
            *   `actions`: `{ "forcemerge": { "max_num_segments": 1 }, "shrink": { "number_of_shards": 1 }, "allocate": { "require": { "box_type": "warm" } } }` (if node roles are used)
        *   `cold`:
            *   `min_age`: `90d`
            *   `actions`: `{ "freeze": {}, "allocate": { "require": { "box_type": "cold" } } }`
        *   `delete`:
            *   `min_age`: `180d` (Adjust per SRS 7.3 for operational logs)
            *   `actions`: `{ "delete": {} }`
*   **`elk/elasticsearch/ilm_policies/audit_log_retention_policy.json`** (REQ-12-006, REQ-ATEL-007)
    *   Name: `audit_log_retention_policy`
    *   **Phases:**
        *   `hot`:
            *   `actions`: `{ "rollover": { "max_size": "20gb", "max_age": "30d" } }`
        *   `delete`:
            *   `min_age`: `365d` (Example: 1 year. Adjust to 1-7 years or specific policy from SRS 7.3 / REQ-ATEL-007)
            *   `actions`: `{ "delete": {} }`
        *   Consider `cold` phase with search snapshots for very long retention if direct deletion is not desired after hot phase.

#### 5.4.6. `elk/elasticsearch/elasticsearch.yml`

*   **Purpose:** Core Elasticsearch configuration.
*   **LogicDescription:**
    yaml
    cluster.name: "influencegen-elk-cluster"
    node.name: ${NODE_NAME} # Injected per node
    # node.roles: [ data_hot, data_warm, data_cold, ingest, ml, master ] # Example node roles
    network.host: 0.0.0.0
    http.port: 9200
    discovery.seed_hosts: ["es-node1:9300", "es-node2:9300"] # Placeholder
    # cluster.initial_master_nodes: ["es-node1"] # Placeholder
    path.data: /usr/share/elasticsearch/data
    path.logs: /usr/share/elasticsearch/logs
    xpack.security.enabled: true # Recommended for production
    xpack.security.enrollment.enabled: true # For initial setup
    # xpack.security.http.ssl.enabled: true
    # xpack.security.transport.ssl.enabled: true
    # ILM related settings if needed globally
    # action.destructive_requires_name: true
    

#### 5.4.7. Kibana Saved Objects (`elk/kibana/saved_objects/`)

These files are JSON exports of Kibana dashboards, visualizations, or saved searches. They allow for versioning and programmatic deployment of Kibana assets.

*   **`elk/kibana/saved_objects/odoo_logs_dashboard.json`** (REQ-12-002, REQ-12-007)
    *   Contains visualizations like:
        *   Log count over time (Odoo)
        *   Distribution of log levels (Odoo)
        *   Top error messages (Odoo)
        *   Log entries table, filterable by level, message content, Odoo module.
*   **`elk/kibana/saved_objects/n8n_logs_dashboard.json`** (REQ-12-002, REQ-12-007, REQ-ATEL-010)
    *   Contains visualizations like:
        *   N8N workflow execution counts (success/failure)
        *   Log entries by workflow ID/name
        *   Errors in N8N nodes
        *   Table of N8N log entries.
*   **`elk/kibana/saved_objects/audit_log_search.json`** (REQ-12-007, REQ-ATEL-008)
    *   A saved search or dashboard focused on audit logs.
    *   Visualizations:
        *   Timeline of audit events.
        *   Breakdown by `eventType`, `actorUserId`, `targetEntity`.
        *   Table view with columns: `timestamp`, `actorUserId`, `eventType`, `action`, `targetEntity`, `targetId`, `ipAddress`, `outcome`, `details`.
        *   Pre-built filters for common queries (e.g., failed logins, permission changes).

#### 5.4.8. `elk/kibana/kibana.yml`

*   **Purpose:** Core Kibana configuration.
*   **LogicDescription:**
    yaml
    server.port: 5601
    server.host: "0.0.0.0"
    elasticsearch.hosts: ["http://elasticsearch:9200"] // Elasticsearch service name and port
    # elasticsearch.username: "kibana_system" // If ES security is enabled
    # elasticsearch.password: "${KIBANA_SYSTEM_PASSWORD}" // Injected
    # logging.dest: stdout
    # server.publicBaseUrl: "https://kibana.influencegen.com" // If externally exposed
    

### 5.5. Common (`common/`)

#### 5.5.1. `common/global_settings.yml`

*   **Purpose:** Centralized common configuration values. (REQ-12-009, REQ-16-010)
*   **LogicDescription:**
    yaml
    # Environment Specifics (can be overridden by deployment process)
    environment_name: "production" # or "staging", "development"
    platform_domain: "influencegen.com"

    # Default Alerting Contacts (can be overridden in Alertmanager routes)
    default_ops_email: "ops-alerts@influencegen.com"
    default_security_email: "security-alerts@influencegen.com"
    default_pagerduty_routing_key: "${PAGERDUTY_DEFAULT_ROUTING_KEY}" # Placeholder for env var
    default_slack_channel: "#general-alerts"

    # Severity Labels for Alerts
    severity_critical: "P1"
    severity_warning: "P2"
    severity_info: "P3"

    # Common Labels for Prometheus/Alertmanager
    common_labels:
      platform: "InfluenceGen"
      # region: "us-east-1" # If multi-region

    # Log Retention Periods (examples, actual values from SRS 7.3)
    operational_logs_retention_days: 180
    audit_logs_retention_days: 1095 # 3 years

    # Other global settings as needed
    
    **Note:** These global settings are primarily for documentation and to guide the setup of tools. Actual injection into tool configurations will depend on the deployment automation (e.g., Ansible, Terraform, Helm charts templating these values).

## 6. Data Flow and Interactions

*   **Metrics Flow:** Odoo, N8N, AI Services, System Hosts -> Prometheus (scrape) -> Alertmanager (alerts) -> Notification Channels (Email, Slack, PagerDuty). Prometheus also -> Grafana (visualization).
*   **Logs Flow:** Odoo, N8N, System Hosts, Audit Log Sources -> Filebeat/Syslog -> Logstash (parse, transform) -> Elasticsearch (store, index) -> Kibana (visualization, search) / Grafana (visualization) / Prometheus (alerts based on log metrics, if exported).
*   **Configuration Flow:** This repository (Git) -> CI/CD Pipeline -> Deployment Tool (e.g., Ansible, Helm) -> Target Monitoring/Logging Systems.

## 7. Security Considerations

*   **Access Control:** Access to monitoring tools (Prometheus, Grafana, Kibana, Alertmanager UIs) must be restricted to authorized personnel.
*   **Secrets Management:** All API keys, passwords, and sensitive credentials used by these tools (e.g., SMTP passwords, Slack tokens, PagerDuty keys, Elasticsearch credentials) MUST be managed through a secure secrets management system or environment variables, not committed to this repository.
*   **Network Security:** Communication between components (e.g., Prometheus scraping targets, Logstash sending to Elasticsearch, Alertmanager to notification endpoints) should be secured, using HTTPS/TLS where possible and network policies/firewalls to restrict access.
*   **Data in Logs:** Care must be taken to avoid logging sensitive PII in operational logs. Audit logs, by nature, will contain sensitive information and must be secured accordingly (REQ-12-006, REQ-ATEL-006).

## 8. Future Considerations

*   **Templating Engine:** For more complex environment-specific configurations, a templating engine (e.g., Jinja2 with Ansible, Helm for Kubernetes) could be used to generate final configuration files from these base templates and environment-specific variable files.
*   **Configuration Validation Tools:** Integrate automated validation of configuration files (e.g., `promtool check config`, `logstash --config.test_and_exit`) into the CI/CD pipeline.
*   **Dynamic Service Discovery:** For highly dynamic environments, expand the use of Prometheus service discovery mechanisms beyond simple file-based SD.

This SDS provides the blueprint for the configuration files within the `InfluenceGen.Monitoring.Configuration` repository, ensuring a robust and comprehensive monitoring, logging, and alerting infrastructure for the InfluenceGen platform.
