# Specification

# 1. Telemetry And Metrics Analysis

- **System Overview:**
  
  - **Analysis Date:** 2025-06-13
  - **Technology Stack:**
    
    - Odoo 18 (Python, OWL, XML)
    - N8N
    - PostgreSQL
    - AI Service (Flux LoRA models via REST API)
    
  - **Monitoring Components:**
    
    - Centralized Logging (e.g., ELK Stack, Splunk, CloudWatch Logs)
    - Metrics Monitoring (e.g., Prometheus/Grafana, Datadog, New Relic)
    - Distributed Tracing (e.g., OpenTelemetry-compatible)
    
  - **Requirements:**
    
    - SRS InfluenceGen Odoo 18 Integration Version 2.0 (ID 19)
    
  - **Environment:** production
  
- **Standard System Metrics Selection:**
  
  - **Hardware Utilization Metrics:**
    
    - **Name:** system.cpu.utilization  
**Type:** gauge  
**Unit:** percentage  
**Description:** CPU utilization for Odoo, N8N, AI Model Serving, and PostgreSQL instances.  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** agent
    
**Thresholds:**
    
    - **Warning:** 70%
    - **Critical:** 85%
    
**Justification:** REQ-12-003, REQ-PERF-BASE: Essential for capacity planning and performance troubleshooting.  
    - **Name:** system.memory.utilization  
**Type:** gauge  
**Unit:** percentage  
**Description:** Memory utilization for Odoo, N8N, AI Model Serving, and PostgreSQL instances.  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** agent
    
**Thresholds:**
    
    - **Warning:** 75%
    - **Critical:** 90%
    
**Justification:** REQ-12-003, REQ-PERF-BASE: Essential for stability and performance.  
    - **Name:** system.disk.io.ops  
**Type:** counter  
**Unit:** operations/sec  
**Description:** Disk I/O operations for Odoo (filestore), PostgreSQL, and potentially N8N/AI if disk-intensive.  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** agent
    
**Thresholds:**
    
    - **Warning:** depends_on_disk_spec
    - **Critical:** depends_on_disk_spec_saturation
    
**Justification:** REQ-12-003, REQ-PERF-DB: Critical for database and file storage performance.  
    - **Name:** system.disk.space.used.percentage  
**Type:** gauge  
**Unit:** percentage  
**Description:** Disk space used for Odoo (DB, filestore), N8N (logs, data), PostgreSQL (data, WAL).  
**Collection:**
    
    - **Interval:** 300s
    - **Method:** agent
    
**Thresholds:**
    
    - **Warning:** 80%
    - **Critical:** 90%
    
**Justification:** REQ-12-003, REQ-SCAL-STOR: Prevents service outages due to full disks.  
    - **Name:** system.network.io.bytes  
**Type:** counter  
**Unit:** bytes/sec  
**Description:** Network traffic (in/out) for Odoo, N8N, AI Model Serving instances.  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** agent
    
**Thresholds:**
    
    - **Warning:** depends_on_link_capacity
    - **Critical:** depends_on_link_capacity_saturation
    
**Justification:** REQ-12-003: Monitors network bottlenecks and usage.  
    - **Name:** gpu.utilization  
**Type:** gauge  
**Unit:** percentage  
**Description:** GPU utilization for AI Model Serving instances (REQ-AIGS-013, REQ-DI-AISERV-CONF).  
**Collection:**
    
    - **Interval:** 30s
    - **Method:** agent_nvidia_smi
    
**Thresholds:**
    
    - **Warning:** 70%
    - **Critical:** 90%
    
**Justification:** REQ-12-003: Critical for AI image generation performance.  
    - **Name:** gpu.memory.utilization  
**Type:** gauge  
**Unit:** percentage  
**Description:** GPU memory utilization for AI Model Serving instances (REQ-AIGS-013, REQ-DI-AISERV-CONF).  
**Collection:**
    
    - **Interval:** 30s
    - **Method:** agent_nvidia_smi
    
**Thresholds:**
    
    - **Warning:** 75%
    - **Critical:** 90%
    
**Justification:** REQ-12-003: Prevents out-of-memory errors on GPU.  
    
  - **Runtime Metrics:**
    
    - **Name:** odoo.workers.active_count  
**Type:** gauge  
**Unit:** count  
**Description:** Number of active Odoo workers.  
**Technology:** Odoo  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** odoo_internal_api_or_log
    
**Criticality:** high  
**Justification:** REQ-PERF-BASE: Indicates load and potential bottlenecks.  
    - **Name:** odoo.request_queue.length  
**Type:** gauge  
**Unit:** count  
**Description:** Length of the request queue for Odoo workers (if exposed by Odoo version/config).  
**Technology:** Odoo  
**Collection:**
    
    - **Interval:** 30s
    - **Method:** odoo_internal_api_or_log
    
**Criticality:** high  
**Justification:** REQ-PERF-BASE: Early indicator of system overload.  
    - **Name:** n8n.workflow.active_executions  
**Type:** gauge  
**Unit:** count  
**Description:** Number of currently active N8N workflow executions.  
**Technology:** N8N  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** n8n_api_or_metrics_endpoint
    
**Criticality:** medium  
**Justification:** REQ-12-003: Monitors N8N processing load.  
    - **Name:** n8n.workflow.execution_queue.length  
**Type:** gauge  
**Unit:** count  
**Description:** Length of the N8N workflow execution queue (if N8N exposes this).  
**Technology:** N8N  
**Collection:**
    
    - **Interval:** 30s
    - **Method:** n8n_api_or_metrics_endpoint
    
**Criticality:** medium  
**Justification:** REQ-12-003: Indicates N8N processing backlog.  
    - **Name:** postgresql.connections.active_count  
**Type:** gauge  
**Unit:** count  
**Description:** Number of active connections to PostgreSQL.  
**Technology:** PostgreSQL  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** db_query
    
**Criticality:** high  
**Justification:** REQ-12-003: Monitors database connection pool health.  
    - **Name:** postgresql.query.slow_query_rate  
**Type:** counter  
**Unit:** queries/sec  
**Description:** Rate of slow queries executed on PostgreSQL.  
**Technology:** PostgreSQL  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** db_log_parsing_or_pg_stat_statements
    
**Criticality:** medium  
**Justification:** REQ-12-003: Identifies database performance issues.  
    
  - **Request Response Metrics:**
    
    - **Name:** odoo.ui.page_load_time_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Odoo UI page load times (REQ-UIUX-007).  
**Dimensions:**
    
    - route
    - user_role
    
**Percentiles:**
    
    - p50
    - p90
    - p95
    
**Collection:**
    
    - **Interval:** on_request
    - **Method:** rum_or_server_side_timing
    
    - **Name:** odoo.ui.interaction_latency_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Latency of key Odoo UI interactive elements (REQ-UIUX-007).  
**Dimensions:**
    
    - interaction_name
    - user_role
    
**Percentiles:**
    
    - p50
    - p90
    - p95
    
**Collection:**
    
    - **Interval:** on_request
    - **Method:** rum_or_server_side_timing
    
    
  - **Availability Metrics:**
    
    - **Name:** system.availability.percentage  
**Type:** gauge  
**Unit:** percentage  
**Description:** Overall system availability for core InfluenceGen functionalities (REQ-REL-UPT-001).  
**Calculation:** Calculated from health checks of Odoo, N8N, AI Service endpoints.  
**Sla Target:** 99.9%  
    
  - **Scalability Metrics:**
    
    - **Name:** odoo.concurrent_users.count  
**Type:** gauge  
**Unit:** count  
**Description:** Number of concurrent users active in Odoo (REQ-PERF-THR-001, REQ-SCAL-CONC-001).  
**Capacity Threshold:** configurable (e.g., 200, 500, 1000)  
**Auto Scaling Trigger:** False  
**Justification:** REQ-PERF-THR-001, REQ-SCAL-CONC-001  
    
  
- **Application Specific Metrics Design:**
  
  - **Transaction Metrics:**
    
    - **Name:** influencer.registration.attempts_rate  
**Type:** counter  
**Unit:** registrations/sec  
**Description:** Rate of new influencer registration attempts (REQ-PERF-THR-002, REQ-SCAL-REG-001).  
**Business_Context:** Influencer Onboarding  
**Dimensions:**
    
    
**Collection:**
    
    - **Interval:** 60s
    - **Method:** application_counter_increment
    
**Aggregation:**
    
    - **Functions:**
      
      - rate
      
    - **Window:** 60s
    
    - **Name:** influencer.registration.success_rate  
**Type:** gauge  
**Unit:** percentage  
**Description:** Percentage of successful influencer registrations (initial form submission).  
**Business_Context:** Influencer Onboarding  
**Dimensions:**
    
    
**Collection:**
    
    - **Interval:** 300s
    - **Method:** calculated (successes/attempts)
    
**Aggregation:**
    
    - **Functions:**
      
      - avg
      
    - **Window:** 300s
    
    - **Name:** influencer.kyc.submission_rate  
**Type:** counter  
**Unit:** submissions/sec  
**Description:** Rate of KYC document submissions (REQ-12-003).  
**Business_Context:** Influencer Onboarding  
**Dimensions:**
    
    
**Collection:**
    
    - **Interval:** 60s
    - **Method:** application_counter_increment
    
**Aggregation:**
    
    - **Functions:**
      
      - rate
      
    - **Window:** 60s
    
    - **Name:** influencer.kyc.verification.automated_step_latency_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Latency of automated KYC verification steps (e.g., 3rd party API calls) (REQ-PERF-KYC-001).  
**Business_Context:** Influencer Onboarding  
**Dimensions:**
    
    - verification_service
    - step_name
    
**Collection:**
    
    - **Interval:** on_event
    - **Method:** application_timer
    
**Aggregation:**
    
    - **Functions:**
      
      - avg
      - p95
      
    - **Window:** on_event
    
    - **Name:** influencer.kyc.verification.success_rate  
**Type:** gauge  
**Unit:** percentage  
**Description:** Success rate of KYC verifications (automated or manual steps combined) (REQ-12-003).  
**Business_Context:** Influencer Onboarding  
**Dimensions:**
    
    - verification_type
    
**Collection:**
    
    - **Interval:** 3600s
    - **Method:** calculated
    
**Aggregation:**
    
    - **Functions:**
      
      - avg
      
    - **Window:** 3600s
    
    - **Name:** campaign.application_rate  
**Type:** counter  
**Unit:** applications/sec  
**Description:** Rate of influencers applying to campaigns (REQ-12-003).  
**Business_Context:** Campaign Management  
**Dimensions:**
    
    - campaign_id
    
**Collection:**
    
    - **Interval:** 60s
    - **Method:** application_counter_increment
    
**Aggregation:**
    
    - **Functions:**
      
      - rate
      
    - **Window:** 60s
    
    - **Name:** campaign.content.submission_rate  
**Type:** counter  
**Unit:** submissions/sec  
**Description:** Rate of content submissions by influencers for campaigns (REQ-12-003).  
**Business_Context:** Campaign Management  
**Dimensions:**
    
    - campaign_id
    
**Collection:**
    
    - **Interval:** 60s
    - **Method:** application_counter_increment
    
**Aggregation:**
    
    - **Functions:**
      
      - rate
      
    - **Window:** 60s
    
    - **Name:** payment.processing.attempts_rate  
**Type:** counter  
**Unit:** payments/sec  
**Description:** Rate of payment processing attempts for influencers (REQ-12-003).  
**Business_Context:** Finance  
**Dimensions:**
    
    
**Collection:**
    
    - **Interval:** 60s
    - **Method:** application_counter_increment
    
**Aggregation:**
    
    - **Functions:**
      
      - rate
      
    - **Window:** 60s
    
    - **Name:** payment.processing.success_rate  
**Type:** gauge  
**Unit:** percentage  
**Description:** Success rate of payment processing (REQ-12-003).  
**Business_Context:** Finance  
**Dimensions:**
    
    
**Collection:**
    
    - **Interval:** 3600s
    - **Method:** calculated
    
**Aggregation:**
    
    - **Functions:**
      
      - avg
      
    - **Window:** 3600s
    
    
  - **Cache Performance Metrics:**
    
    - **Name:** odoo.orm.cache.hit_ratio  
**Type:** gauge  
**Unit:** percentage  
**Description:** Odoo ORM cache hit ratio (if exposed).  
**Cache Type:** Odoo ORM Cache  
**Hit Ratio Target:** >80%  
**Justification:** REQ-PERF-BASE: Indicates effectiveness of Odoo's caching.  
    
  - **External Dependency Metrics:**
    
    - **Name:** api.odoo_to_n8n_webhook.latency_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Latency of Odoo's webhook calls to N8N for AI image generation (REQ-IL-013).  
**Dependency:** N8N Webhook Receiver  
**Circuit Breaker Integration:** False  
**Sla:**
    
    - **Response Time:** 0.5s
    - **Availability:** 99.9%
    
    - **Name:** api.odoo_to_n8n_webhook.error_rate  
**Type:** counter  
**Unit:** errors/sec  
**Description:** Error rate of Odoo's webhook calls to N8N (REQ-IL-013, REQ-16-009).  
**Dependency:** N8N Webhook Receiver  
**Circuit Breaker Integration:** False  
**Sla:**
    
    - **Availability:** 99.9%
    
    - **Name:** api.n8n_to_aiservice.latency_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Latency of N8N's calls to the AI Image Generation Service (REQ-IL-013).  
**Dependency:** AI Image Generation Service  
**Circuit Breaker Integration:** True  
**Sla:**
    
    - **Response Time:** varies_by_complexity (avg 5-15s for AI part)
    - **Availability:** 99.5%
    
    - **Name:** api.n8n_to_aiservice.error_rate  
**Type:** counter  
**Unit:** errors/sec  
**Description:** Error rate of N8N's calls to the AI Image Generation Service (REQ-IL-013, REQ-16-009).  
**Dependency:** AI Image Generation Service  
**Circuit Breaker Integration:** True  
**Sla:**
    
    - **Availability:** 99.5%
    
    - **Name:** api.n8n_to_odoo_callback.latency_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Latency of N8N's callback calls to Odoo (REQ-IL-013).  
**Dependency:** Odoo Callback API  
**Circuit Breaker Integration:** False  
**Sla:**
    
    - **Response Time:** 0.5s
    - **Availability:** 99.9%
    
    - **Name:** api.n8n_to_odoo_callback.error_rate  
**Type:** counter  
**Unit:** errors/sec  
**Description:** Error rate of N8N's callback calls to Odoo (REQ-IL-013, REQ-16-009).  
**Dependency:** Odoo Callback API  
**Circuit Breaker Integration:** False  
**Sla:**
    
    - **Availability:** 99.9%
    
    - **Name:** api.external_kyc_service.latency_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Latency of calls to external KYC verification service (if used) (REQ-IL-013).  
**Dependency:** External KYC Service  
**Circuit Breaker Integration:** True  
**Sla:**
    
    - **Response Time:** defined_by_kyc_provider_sla
    - **Availability:** defined_by_kyc_provider_sla
    
    - **Name:** api.external_kyc_service.error_rate  
**Type:** counter  
**Unit:** errors/sec  
**Description:** Error rate of calls to external KYC verification service (REQ-IL-013, REQ-16-009).  
**Dependency:** External KYC Service  
**Circuit Breaker Integration:** True  
**Sla:**
    
    - **Availability:** defined_by_kyc_provider_sla
    
    
  - **Error Metrics:**
    
    - **Name:** odoo.application.error_rate  
**Type:** counter  
**Unit:** errors/sec  
**Description:** Rate of unhandled errors in Odoo application logs.  
**Error Types:**
    
    - python_exception
    - orm_error
    - controller_error
    
**Dimensions:**
    
    - error_class
    - module_name
    
**Alert Threshold:** configurable (e.g., >5 errors/min)  
**Justification:** REQ-12-003, REQ-REL-ERR-001: General application health.  
    - **Name:** n8n.workflow.execution.error_rate  
**Type:** counter  
**Unit:** errors/sec  
**Description:** Rate of N8N workflow execution failures not attributed to external services (REQ-12-003, REQ-16-009).  
**Error Types:**
    
    - node_execution_error
    - workflow_logic_error
    
**Dimensions:**
    
    - workflow_name
    - node_name
    
**Alert Threshold:** configurable (e.g., >2 errors/min for critical workflow)  
**Justification:** REQ-12-003, REQ-REL-ERR-001: N8N operational health.  
    
  - **Throughput And Latency Metrics:**
    
    - **Name:** ai.image_generation.request_rate  
**Type:** counter  
**Unit:** requests/sec  
**Description:** Rate of AI image generation requests initiated from Odoo (REQ-AIGS-009, REQ-12-003).  
**Percentiles:**
    
    
**Buckets:**
    
    
**Sla Targets:**
    
    
    - **Name:** ai.image_generation.success_rate  
**Type:** gauge  
**Unit:** percentage  
**Description:** End-to-end success rate of AI image generation requests (REQ-12-003).  
**Percentiles:**
    
    
**Buckets:**
    
    
**Sla Targets:**
    
    
    - **Name:** ai.image_generation.end_to_end_latency_seconds  
**Type:** histogram  
**Unit:** seconds  
**Description:** Total time from user request in Odoo to image available in Odoo (REQ-AIGS-008, REQ-12-003).  
**Percentiles:**
    
    - p50
    - p90
    - p95
    
**Buckets:**
    
    - 1
    - 5
    - 10
    - 15
    - 20
    - 30
    - 60
    
**Sla Targets:**
    
    - **P90:** 20s
    - **P95:** 30s
    
    
  
- **Business Kpi Identification:**
  
  - **Critical Business Metrics:**
    
    - **Name:** influencer.onboarding.registrations_per_hour  
**Type:** counter  
**Unit:** count/hour  
**Description:** Number of new influencer registrations per hour (REQ-PERF-THR-002).  
**Business Owner:** Platform Operations  
**Calculation:** SUM(registration_attempts) GROUP BY hour  
**Reporting Frequency:** hourly  
**Target:** 50-100  
    - **Name:** ai.image_generation.daily_volume  
**Type:** counter  
**Unit:** count/day  
**Description:** Total AI images generated per day (REQ-AIGS-009).  
**Business Owner:** Platform Operations  
**Calculation:** SUM(ai_image_generation_requests) GROUP BY day  
**Reporting Frequency:** daily  
**Target:** 5000-10000  
    - **Name:** influencer.active_count_total  
**Type:** gauge  
**Unit:** count  
**Description:** Total number of active influencers on the platform (REQ-SCAL-INF-001).  
**Business Owner:** Platform Operations  
**Calculation:** COUNT(DISTINCT influencer_id WHERE status='active')  
**Reporting Frequency:** daily  
**Target:** 10000 (initial), 100000+ (scalable)  
    
  - **User Engagement Metrics:**
    
    - **Name:** user.logins.daily_active_influencers  
**Type:** gauge  
**Unit:** count  
**Description:** Number of unique influencers logging in per day (REQ-12-003).  
**Segmentation:**
    
    - user_role
    
**Cohort Analysis:** False  
    
  - **Conversion Metrics:**
    
    - **Name:** influencer.onboarding.kyc_approval_rate  
**Type:** gauge  
**Unit:** percentage  
**Description:** Percentage of KYC submissions that are approved (REQ-12-003).  
**Funnel Stage:** KYC Verification  
**Conversion Target:** >85%  
    
  - **Operational Efficiency Kpis:**
    
    - **Name:** influencer.onboarding.kyc_manual_review_time_avg_hours  
**Type:** gauge  
**Unit:** hours  
**Description:** Average time taken for manual KYC review by administrators.  
**Calculation:** AVG(kyc_reviewed_at - kyc_submitted_for_manual_review_at)  
**Benchmark Target:** <24 hours  
    - **Name:** system.backup.job_success_rate  
**Type:** gauge  
**Unit:** percentage  
**Description:** Success rate of scheduled database and filestore backup jobs (REQ-REL-BCK-001, REQ-16-009).  
**Calculation:** COUNT(successful_backups) / COUNT(total_backup_jobs)  
**Benchmark Target:** 100%  
    
  - **Revenue And Cost Metrics:**
    
    - **Name:** ai.image_generation.cost_per_image_usd  
**Type:** gauge  
**Unit:** USD  
**Description:** Estimated cost per generated AI image (if using paid AI service or for cloud resource cost allocation).  
**Frequency:** daily  
**Accuracy:** estimated  
    
  - **Customer Satisfaction Indicators:**
    
    
  
- **Collection Interval Optimization:**
  
  - **Sampling Frequencies:**
    
    - **Metric Category:** Critical API Latency/Errors (AI Gen Path)  
**Interval:** 10s  
**Justification:** Rapid detection of integration issues.  
**Resource Impact:** medium  
    - **Metric Category:** System Resource Utilization (CPU, Memory)  
**Interval:** 60s  
**Justification:** Standard interval for OS-level metrics.  
**Resource Impact:** low  
    - **Metric Category:** Business Transaction Rates (Registrations, AI Gen)  
**Interval:** 60s  
**Justification:** Timely tracking of key activities.  
**Resource Impact:** low  
    - **Metric Category:** Database Performance (Connections, Slow Queries)  
**Interval:** 60s  
**Justification:** Key DB health indicators.  
**Resource Impact:** medium  
    - **Metric Category:** UI Performance (Page Loads)  
**Interval:** on_request (RUM) or sampled server-side 60s  
**Justification:** User experience monitoring.  
**Resource Impact:** medium_if_rum_high_if_server_high_freq  
    - **Metric Category:** Batch Job Status (Backups)  
**Interval:** on_completion  
**Justification:** Event-driven for job outcomes.  
**Resource Impact:** low  
    
  - **High Frequency Metrics:**
    
    - **Name:** api.n8n_to_aiservice.latency_seconds  
**Interval:** 10s  
**Criticality:** high  
**Cost Justification:** Essential for AI generation SLA.  
    - **Name:** api.n8n_to_aiservice.error_rate  
**Interval:** 10s  
**Criticality:** high  
**Cost Justification:** Essential for AI generation reliability.  
    
  - **Cardinality Considerations:**
    
    - **Metric Name:** odoo.ui.page_load_time_seconds  
**Estimated Cardinality:** medium (number of routes * roles)  
**Dimension Strategy:** Limit dimensions to critical routes/roles if cardinality becomes an issue.  
**Mitigation Approach:** Aggregation rules, dropping high-cardinality dimensions if necessary.  
    - **Metric Name:** api.*.latency_seconds  
**Estimated Cardinality:** low to medium (per API endpoint/dependency)  
**Dimension Strategy:** Use specific endpoint/dependency as dimension.  
**Mitigation Approach:** N/A  
    
  - **Aggregation Periods:**
    
    - **Metric Type:** Latency Histograms  
**Periods:**
    
    - 1m
    - 5m
    - 15m
    - 1h
    
**Retention Strategy:** Rollup to coarser granularity over time.  
    - **Metric Type:** Error Rates/Counters  
**Periods:**
    
    - 1m
    - 5m
    - 1h
    - 1d
    
**Retention Strategy:** Sum/Rate over increasing windows.  
    
  - **Collection Methods:**
    
    - **Method:** agent  
**Applicable Metrics:**
    
    - system.*
    - gpu.*
    
**Implementation:** OS-level agents (e.g., Prometheus node_exporter, nvidia_dcgm_exporter)  
**Performance:** low_overhead  
    - **Method:** application_instrumentation  
**Applicable Metrics:**
    
    - api.*.latency_seconds
    - api.*.error_rate
    - ai.image_generation.*
    - influencer.*
    - campaign.*
    - payment.*
    - odoo.application.error_rate
    
**Implementation:** Code-level metrics libraries (e.g., Prometheus client libraries for Python/Odoo, N8N internal metrics if exposed)  
**Performance:** medium_overhead_depending_on_granularity  
    - **Method:** log_parsing  
**Applicable Metrics:**
    
    - postgresql.query.slow_query_rate (alternative)
    - odoo.request_queue.length (alternative)
    
**Implementation:** Log shippers (e.g., Filebeat) and parsing in logging backend (e.g., Logstash, Loki)  
**Performance:** medium_overhead_on_logging_system  
    - **Method:** db_query  
**Applicable Metrics:**
    
    - postgresql.connections.active_count
    - influencer.active_count_total
    
**Implementation:** Scheduled queries against PostgreSQL (e.g., pg_stat_activity, custom queries)  
**Performance:** low_to_medium_overhead_on_db  
    
  
- **Aggregation Method Selection:**
  
  - **Statistical Aggregations:**
    
    - **Metric Name:** api.*.latency_seconds  
**Aggregation Functions:**
    
    - avg
    - p50
    - p90
    - p95
    - p99
    - count
    - sum
    - rate(count)
    
**Windows:**
    
    - 1m
    - 5m
    - 15m
    
**Justification:** Comprehensive view of API performance and error rates.  
    - **Metric Name:** system.cpu.utilization  
**Aggregation Functions:**
    
    - avg
    - max
    
**Windows:**
    
    - 1m
    - 5m
    - 15m
    
**Justification:** Understanding typical and peak CPU load.  
    
  - **Histogram Requirements:**
    
    - **Metric Name:** ai.image_generation.end_to_end_latency_seconds  
**Buckets:**
    
    - 1
    - 2.5
    - 5
    - 7.5
    - 10
    - 12.5
    - 15
    - 17.5
    - 20
    - 25
    - 30
    - 45
    - 60
    - +Inf
    
**Percentiles:**
    
    - p50
    - p90
    - p95
    - p99
    
**Accuracy:** high  
    - **Metric Name:** odoo.ui.page_load_time_seconds  
**Buckets:**
    
    - 0.1
    - 0.25
    - 0.5
    - 0.75
    - 1
    - 1.5
    - 2
    - 2.5
    - 3
    - 4
    - 5
    - +Inf
    
**Percentiles:**
    
    - p50
    - p90
    - p95
    
**Accuracy:** high  
    
  - **Percentile Calculations:**
    
    - **Metric Name:** api.*.latency_seconds  
**Percentiles:**
    
    - p50
    - p90
    - p95
    - p99
    
**Algorithm:** hdr_histogram_or_equivalent_prometheus  
**Accuracy:** high  
    - **Metric Name:** ai.image_generation.end_to_end_latency_seconds  
**Percentiles:**
    
    - p50
    - p90
    - p95
    - p99
    
**Algorithm:** hdr_histogram_or_equivalent_prometheus  
**Accuracy:** high  
    
  - **Metric Types:**
    
    - **Name:** api.*.error_rate  
**Implementation:** counter  
**Reasoning:** Monotonically increasing count of errors, rate calculated over time.  
**Resets Handling:** Handled by rate() function in query language.  
    - **Name:** system.cpu.utilization  
**Implementation:** gauge  
**Reasoning:** Represents current value that can go up or down.  
**Resets Handling:** N/A  
    
  - **Dimensional Aggregation:**
    
    - **Metric Name:** api.*.latency_seconds  
**Dimensions:**
    
    - endpoint
    - http_method
    - status_code_class
    
**Aggregation Strategy:** Aggregations (avg, sum, p95) can be performed over any combination of these dimensions.  
**Cardinality Impact:** Medium; manage by limiting distinct endpoint strings or using regex matching in queries.  
    
  - **Derived Metrics:**
    
    - **Name:** system.availability.percentage  
**Calculation:** (uptime_seconds / total_seconds_in_period) * 100 OR (1 - (SUM(outage_event_count_for_critical_services) / total_probes_for_critical_services)) * 100  
**Source Metrics:**
    
    - health_check_status (multiple services)
    
**Update Frequency:** 1m  
    
  
- **Storage Requirements Planning:**
  
  - **Retention Periods:**
    
    - **Metric Type:** High-Granularity (e.g., 10s-1m resolution) API/Performance Metrics  
**Retention Period:** 7-14 days  
**Justification:** Short-term troubleshooting and detailed analysis.  
**Compliance Requirement:** N/A  
    - **Metric Type:** Medium-Granularity (e.g., 5m-15m resolution) Aggregated Metrics  
**Retention Period:** 30-90 days  
**Justification:** Trend analysis, capacity planning.  
**Compliance Requirement:** N/A  
    - **Metric Type:** Low-Granularity (e.g., 1h resolution) Business KPIs & Long-Term Trends  
**Retention Period:** 1-2 years  
**Justification:** Long-term reporting and strategic planning.  
**Compliance Requirement:** May be relevant for some business reporting.  
    
  - **Data Resolution:**
    
    - **Time Range:** 0-7 days  
**Resolution:** 10s-1m  
**Query Performance:** high  
**Storage Optimization:** raw_data  
    - **Time Range:** 7-90 days  
**Resolution:** 5m-15m  
**Query Performance:** medium  
**Storage Optimization:** downsampled_via_aggregation_rules  
    - **Time Range:** >90 days  
**Resolution:** 1h  
**Query Performance:** low  
**Storage Optimization:** heavily_downsampled_long_term_storage  
    
  - **Downsampling Strategies:**
    
    - **Source Resolution:** 10s  
**Target Resolution:** 1m  
**Aggregation Method:** avg for gauges, sum for counters, merge for histograms  
**Trigger Condition:** After 24 hours of 10s data  
    - **Source Resolution:** 1m  
**Target Resolution:** 5m  
**Aggregation Method:** avg for gauges, sum for counters, merge for histograms  
**Trigger Condition:** After 7 days of 1m data  
    
  - **Storage Performance:**
    
    - **Write Latency:** <100ms for high-frequency metrics
    - **Query Latency:** <5s for typical dashboard queries (medium range), <30s for complex analytical queries (long range)
    - **Throughput Requirements:** Handle peak metric ingestion rate (e.g., 1000s of DPM)
    - **Scalability Needs:** Storage system must scale with user growth and feature usage.
    
  - **Query Optimization:**
    
    - **Query Pattern:** Time-series aggregation by dimension (e.g., average API latency per endpoint over last hour)  
**Optimization Strategy:** Proper indexing on time and dimensions in TSDB.  
**Indexing Requirements:**
    
    - timestamp
    - metric_name
    - dimension_tags
    
    
  - **Cost Optimization:**
    
    - **Strategy:** Aggressive downsampling and tiered storage  
**Implementation:** Configure recording rules and retention policies in Prometheus/TSDB. Use cheaper storage for older, aggregated data.  
**Expected Savings:** Significant reduction in long-term storage costs.  
**Tradeoffs:** Loss of raw data granularity for older periods.  
    
  
- **Project Specific Metrics Config:**
  
  - **Standard Metrics:**
    
    - **Name:** system.cpu.utilization  
**Type:** gauge  
**Unit:** percentage  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** agent
    
**Thresholds:**
    
    - **Warning:** 70
    - **Critical:** 85
    
**Dimensions:**
    
    - host
    - service_name
    
    - **Name:** system.memory.utilization  
**Type:** gauge  
**Unit:** percentage  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** agent
    
**Thresholds:**
    
    - **Warning:** 75
    - **Critical:** 90
    
**Dimensions:**
    
    - host
    - service_name
    
    - **Name:** system.disk.space.used.percentage  
**Type:** gauge  
**Unit:** percentage  
**Collection:**
    
    - **Interval:** 300s
    - **Method:** agent
    
**Thresholds:**
    
    - **Warning:** 80
    - **Critical:** 90
    
**Dimensions:**
    
    - host
    - mount_point
    
    - **Name:** postgresql.connections.active_count  
**Type:** gauge  
**Unit:** count  
**Collection:**
    
    - **Interval:** 60s
    - **Method:** db_query
    
**Thresholds:**
    
    - **Warning:** 80%_of_max_connections
    - **Critical:** 95%_of_max_connections
    
**Dimensions:**
    
    - db_instance
    
    
  - **Custom Metrics:**
    
    - **Name:** api.n8n_to_aiservice.error_rate  
**Description:** Error rate of N8N's calls to the AI Image Generation Service.  
**Calculation:** rate(api_n8n_to_aiservice_errors_total[5m])  
**Type:** counter  
**Unit:** errors/sec  
**Business Context:** AI Image Generation Reliability  
**Collection:**
    
    - **Interval:** on_event
    - **Method:** application_instrumentation
    
**Alerting:**
    
    - **Enabled:** True
    - **Conditions:**
      
      - value > 0.1 for 5m
      
    
    - **Name:** ai.image_generation.end_to_end_latency_seconds_p95  
**Description:** 95th percentile of total time from user request in Odoo to image available in Odoo.  
**Calculation:** histogram_quantile(0.95, sum(rate(ai_image_generation_end_to_end_latency_seconds_bucket[5m])) by (le))  
**Type:** histogram  
**Unit:** seconds  
**Business Context:** AI Image Generation Performance  
**Collection:**
    
    - **Interval:** on_event
    - **Method:** application_instrumentation
    
**Alerting:**
    
    - **Enabled:** True
    - **Conditions:**
      
      - value > 30 for 10m
      
    
    - **Name:** influencer.registration.success_rate  
**Description:** Percentage of successful influencer registrations.  
**Calculation:** (sum(rate(influencer_registration_success_total[1h])) / sum(rate(influencer_registration_attempts_total[1h]))) * 100  
**Type:** gauge  
**Unit:** percentage  
**Business Context:** Influencer Onboarding  
**Collection:**
    
    - **Interval:** on_event
    - **Method:** application_instrumentation
    
**Alerting:**
    
    - **Enabled:** True
    - **Conditions:**
      
      - value < 80 for 1h
      
    
    - **Name:** system.backup.job_success_rate  
**Description:** Success rate of scheduled backup jobs.  
**Calculation:** (sum(backup_job_success_total) / sum(backup_job_total)) * 100 over last 24h  
**Type:** gauge  
**Unit:** percentage  
**Business Context:** System Reliability  
**Collection:**
    
    - **Interval:** on_completion
    - **Method:** job_status_reporting
    
**Alerting:**
    
    - **Enabled:** True
    - **Conditions:**
      
      - value < 100
      
    
    
  - **Dashboard Metrics:**
    
    - **Dashboard:** Odoo_System_Health  
**Metrics:**
    
    - system.cpu.utilization (Odoo hosts)
    - system.memory.utilization (Odoo hosts)
    - odoo.workers.active_count
    - odoo.request_queue.length
    - odoo.ui.page_load_time_seconds_p95
    - odoo.application.error_rate
    
**Refresh Interval:** 60s  
**Audience:** Platform Administrators, Operations Team  
    - **Dashboard:** N8N_AI_Integration_Performance  
**Metrics:**
    
    - system.cpu.utilization (N8N host)
    - system.memory.utilization (N8N host)
    - n8n.workflow.active_executions
    - n8n.workflow.execution_queue.length
    - api.odoo_to_n8n_webhook.latency_seconds_p95
    - api.odoo_to_n8n_webhook.error_rate
    - api.n8n_to_aiservice.latency_seconds_p95
    - api.n8n_to_aiservice.error_rate
    - api.n8n_to_odoo_callback.latency_seconds_p95
    - api.n8n_to_odoo_callback.error_rate
    - n8n.workflow.execution.error_rate
    
**Refresh Interval:** 30s  
**Audience:** Platform Administrators, Operations Team, N8N Developers  
    - **Dashboard:** AI_Image_Generation_Service_KPIs  
**Metrics:**
    
    - gpu.utilization (AI hosts)
    - gpu.memory.utilization (AI hosts)
    - ai.image_generation.request_rate
    - ai.image_generation.success_rate
    - ai.image_generation.end_to_end_latency_seconds_p95
    - ai.image_generation.daily_volume
    
**Refresh Interval:** 60s  
**Audience:** Platform Administrators, Business Stakeholders  
    - **Dashboard:** Business_Operations_Overview  
**Metrics:**
    
    - influencer.onboarding.registrations_per_hour
    - influencer.onboarding.kyc_approval_rate
    - influencer.active_count_total
    - campaign.application_rate
    - payment.processing.success_rate
    
**Refresh Interval:** 300s  
**Audience:** Business Stakeholders, Platform Management  
    
  
- **Implementation Priority:**
  
  - **Component:** Basic System Metrics (CPU, Mem, Disk) for Odoo, N8N, DB, AI  
**Priority:** high  
**Dependencies:**
    
    - Monitoring Agent Setup
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** API Metrics for Odoo-N8N-AI Path (Latency, Errors, Rate)  
**Priority:** high  
**Dependencies:**
    
    - Application Instrumentation
    
**Estimated Effort:** High  
**Risk Level:** medium  
  - **Component:** AI Image Generation End-to-End Metrics (Latency, Success Rate)  
**Priority:** high  
**Dependencies:**
    
    - Application Instrumentation in Odoo & N8N
    
**Estimated Effort:** High  
**Risk Level:** medium  
  - **Component:** Influencer Onboarding Funnel Metrics (Registration, KYC)  
**Priority:** medium  
**Dependencies:**
    
    - Application Instrumentation in Odoo
    
**Estimated Effort:** Medium  
**Risk Level:** low  
  - **Component:** Odoo UI Performance Metrics  
**Priority:** medium  
**Dependencies:**
    
    - RUM or Odoo Server-Side Instrumentation
    
**Estimated Effort:** Medium  
**Risk Level:** medium  
  
- **Risk Assessment:**
  
  - **Risk:** Metrics collection impacts system performance.  
**Impact:** medium  
**Probability:** medium  
**Mitigation:** Optimize agent configurations, use efficient instrumentation libraries, sample high-frequency/cardinality metrics.  
**Contingency Plan:** Reduce collection frequency or granularity for problematic metrics.  
  - **Risk:** Inaccurate or misleading metrics.  
**Impact:** high  
**Probability:** low  
**Mitigation:** Thoroughly test metric definitions and collection. Validate against known system behavior. Cross-reference with logs.  
**Contingency Plan:** Correct metric definitions. Recalculate historical data if possible and critical.  
  - **Risk:** Monitoring system outage or data loss.  
**Impact:** high  
**Probability:** low  
**Mitigation:** Deploy redundant monitoring components. Regularly backup monitoring system configuration and data.  
**Contingency Plan:** Restore monitoring system from backup. Rely on basic logging during outage.  
  - **Risk:** Alert fatigue due to poorly tuned thresholds.  
**Impact:** medium  
**Probability:** high  
**Mitigation:** Start with conservative thresholds, iteratively tune based on operational experience. Implement alert grouping and deduplication.  
**Contingency Plan:** Temporarily disable noisy alerts. Conduct an alert review and tuning session.  
  
- **Recommendations:**
  
  - **Category:** Instrumentation  
**Recommendation:** Adopt OpenTelemetry standards for application instrumentation where possible to ensure vendor neutrality and comprehensive tracing capabilities.  
**Justification:** Provides flexibility for future monitoring tool changes and aligns with industry best practices (REQ-12-005).  
**Priority:** high  
**Implementation Notes:** Requires Python and N8N (if custom JS nodes used) to be instrumented with OpenTelemetry SDKs.  
  - **Category:** Dashboarding  
**Recommendation:** Develop persona-based dashboards (Admin, Ops, Business) to provide relevant views into system health and KPIs.  
**Justification:** Ensures stakeholders get actionable information efficiently (REQ-12-004, REQ-12-007).  
**Priority:** high  
**Implementation Notes:** Use Grafana or chosen monitoring tool's dashboarding features.  
  - **Category:** Alerting  
**Recommendation:** Implement automated runbooks or troubleshooting guides linked to critical alerts to expedite incident response.  
**Justification:** Reduces MTTR and provides consistency in handling common issues (REQ-OP-SUP-KB).  
**Priority:** medium  
**Implementation Notes:** Store runbooks in a knowledge base and link them in alert notifications.  
  - **Category:** Review & Iteration  
**Recommendation:** Schedule regular (e.g., quarterly) reviews of metrics, dashboards, and alert configurations to ensure they remain relevant and effective.  
**Justification:** System behavior and business priorities evolve, requiring monitoring adjustments.  
**Priority:** medium  
**Implementation Notes:** Involve operations, development, and business stakeholders in reviews.  
  


---

