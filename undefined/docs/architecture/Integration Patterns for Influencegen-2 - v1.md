# Architecture Design Specification

# 1. Patterns

## 1.1. Asynchronous Request-Response
### 1.1.2. Type
Messaging

### 1.1.3. Implementation
Odoo initiates requests to N8N by triggering a designated N8N webhook (HTTP POST). N8N processes the request asynchronously and, upon completion, calls back a dedicated Odoo REST API endpoint (HTTP POST) with the results.

### 1.1.4. Applicability
Essential for the AI Image Generation workflow (REQ-AIGS-001, REQ-IL-002, REQ-IL-003). This decouples Odoo from N8N's potentially long-running AI processing, improving Odoo's responsiveness and overall system resilience.

## 1.2. Request-Reply (Synchronous)
### 1.2.2. Type
Invocation

### 1.2.3. Implementation
N8N makes direct synchronous HTTP/REST API calls to external AI image generation services. Odoo or N8N may also make synchronous HTTP/REST calls to third-party KYC or payment gateway APIs if such integrations are implemented.

### 1.2.4. Applicability
Required for N8N's interaction with AI Image Generation services (REQ-IL-005) and any direct integrations Odoo/N8N might have with KYC (REQ-IL-011) or Payment services (REQ-IL-012) where an immediate response is expected to continue processing.

## 1.3. Orchestration
### 1.3.2. Type
Orchestration

### 1.3.3. Implementation
N8N workflows act as the central orchestrator, managing the sequence of operations for AI image generation. This includes receiving the request from Odoo, calling the AI service, handling its response, and invoking the callback to Odoo.

### 1.3.4. Applicability
Core to the AI Image Generation process (REQ-IL-001, REQ-AIGS-001), and potentially for other future complex integrations involving multiple steps and external services. Ensures logical flow and error management for these processes.

## 1.4. Retry
### 1.4.2. Type
Reliability

### 1.4.3. Implementation
N8N workflows implement configurable retry logic with backoff strategies for calls to external AI services and for callbacks to Odoo's API endpoint. Odoo should also implement retries for its webhook calls to N8N if initial attempts fail.

### 1.4.4. Applicability
Essential for all critical integration points (Odoo to N8N, N8N to AI service, N8N to Odoo callback) to handle transient failures and improve overall system resilience against temporary network issues or service unavailability (REQ-IL-009).

## 1.5. Timeout
### 1.5.2. Type
Reliability

### 1.5.3. Implementation
Configurable timeouts are applied to all synchronous outbound HTTP requests made by N8N (to AI services) and by Odoo (for webhook calls to N8N). Odoo's callback endpoint must also process requests efficiently to avoid timeouts on N8N's side.

### 1.5.4. Applicability
Necessary for all synchronous external service calls to prevent indefinite blocking of resources and to ensure timely failure detection if a service is unresponsive (REQ-IL-009, REQ-AIGS-008).

## 1.6. Dead Letter Channel
### 1.6.2. Type
Messaging

### 1.6.3. Implementation
N8N workflows are designed to route requests that fail persistently (after exhausting retries) to a designated error handling mechanism. This could involve logging detailed error information and triggering alerts for manual investigation.

### 1.6.4. Applicability
Crucial for asynchronous integration processes, particularly AI image generation, to ensure that critical failures are captured, not lost, and can be investigated and potentially reprocessed (REQ-IL-009).

## 1.7. Idempotent Receiver
### 1.7.2. Type
Reliability

### 1.7.3. Implementation
Odoo's REST API callback endpoint (e.g., for receiving AI image generation results from N8N) is designed to safely handle potential duplicate messages or requests (e.g., due to N8N retries) without causing unintended side effects like creating duplicate image records.

### 1.7.4. Applicability
Essential for Odoo's callback endpoints (REQ-IL-003) to ensure data integrity and consistency when receiving asynchronous responses, especially when the calling system (N8N) implements retries.

## 1.8. Rate Limiting
### 1.8.2. Type
Control

### 1.8.3. Implementation
Odoo's publicly exposed API endpoints involved in integrations (e.g., the callback URL for N8N) have configurable rate limits. N8N workflows are designed to respect and handle rate limits imposed by external services they call (e.g., AI, KYC, Payment APIs).

### 1.8.4. Applicability
Required to protect Odoo's API endpoints from potential overload (e.g., from N8N) and to ensure N8N behaves as a good citizen respecting external service usage policies, thus preventing service disruption and ensuring fair usage (REQ-PAC-013, REQ-IL-015).



---

