# Architecture Design Specification

# 1. Style
LayeredArchitecture


---

# 2. Patterns

## 2.1. Model-View-Controller (MVC) / Model-Template-View (MTV)
Odoo's architecture inherently follows an MTV (similar to MVC) pattern. Models represent data and business logic, Views (XML/QWeb) and OWL Components handle presentation, and Controllers (Python) manage request handling and routing.

### 2.1.3. Benefits

- Separation of concerns between data, logic, and presentation.
- Leverages Odoo's established framework for rapid development.
- Maintainability and testability of individual components.

### 2.1.4. Applicability

- **Scenarios:**
  
  - All UI interactions within the Odoo platform for both influencer portal and admin backend.
  

## 2.2. Service Layer
Business logic that doesn't naturally fit into a single Odoo model or spans multiple models can be encapsulated in service classes/methods. These services are then invoked by models or controllers.

### 2.2.3. Benefits

- Better organization of complex business logic.
- Improved reusability of business operations.
- Easier unit testing of business logic.

### 2.2.4. Applicability

- **Scenarios:**
  
  - Orchestrating multi-step onboarding processes.
  - Complex payment calculation logic.
  - Coordinating interactions between different InfluenceGen modules.
  

## 2.3. Repository Pattern (via Odoo ORM)
Odoo's Object-Relational Mapper (ORM) abstracts database interactions. Odoo models effectively act as repositories, providing methods to query and manipulate data without writing direct SQL.

### 2.3.3. Benefits

- Database independence (to some extent).
- Simplified data access logic.
- Object-oriented way of interacting with data.

### 2.3.4. Applicability

- **Scenarios:**
  
  - All data creation, retrieval, update, and deletion operations for InfluenceGen entities.
  

## 2.4. Webhook Integration
Odoo initiates asynchronous tasks by calling N8N webhooks. N8N, upon task completion, calls back a dedicated Odoo REST API endpoint.

### 2.4.3. Benefits

- Decouples Odoo from the direct execution of long-running or external tasks.
- Enables asynchronous processing, improving Odoo's responsiveness.
- Leverages N8N's strengths in workflow automation and external service integration.

### 2.4.4. Applicability

- **Scenarios:**
  
  - Initiating AI image generation requests to N8N (REQ-AIGS-001, REQ-IL-002).
  - Receiving AI image generation results from N8N (REQ-AIGS-001, REQ-IL-003).
  

## 2.5. Asynchronous Task Processing
Long-running operations like AI image generation are handled asynchronously by N8N, preventing blocking of Odoo's main processes.

### 2.5.3. Benefits

- Improved user experience by not freezing the UI.
- Better resource utilization in Odoo.
- Scalability for handling multiple concurrent long tasks.

### 2.5.4. Applicability

- **Scenarios:**
  
  - AI image generation (REQ-AIGS-001, REQ-AIGS-008).
  

## 2.6. Modular Design (Odoo Modules)
The entire InfluenceGen system is built as a collection of custom Odoo modules, each responsible for a specific feature group (e.g., Onboarding, Campaigns, AI Services).

### 2.6.3. Benefits

- Encapsulation of functionality.
- Independent development and deployment of features (within Odoo's module system).
- Better maintainability and organization of a large system.
- Extensibility by adding new modules.

### 2.6.4. Applicability

- **Scenarios:**
  
  - The overall structure of the InfluenceGen platform within Odoo (REQ-DDSI-001).
  

## 2.7. Configuration Management
Platform-wide settings, business rules, and integration parameters are managed through Odoo's configuration mechanisms (e.g., `ir.config_parameter`, custom models for settings).

### 2.7.3. Benefits

- Centralized management of system behavior.
- Ability to adapt the system without code changes.
- Separation of configuration from code.

### 2.7.4. Applicability

- **Scenarios:**
  
  - Configuring KYC rules (REQ-PAC-007), AI model parameters (REQ-PAC-005), email templates (REQ-PAC-010), data retention policies (REQ-PAC-008).
  

## 2.8. Audit Logging
Significant system events and user actions are recorded in a dedicated audit trail for security, compliance, and troubleshooting.

### 2.8.3. Benefits

- Traceability of actions.
- Support for security investigations and compliance reporting.
- Deterrent against misuse.

### 2.8.4. Applicability

- **Scenarios:**
  
  - Tracking KYC changes (REQ-IOKYC-016), campaign management actions (REQ-2-018), AI generation requests (REQ-AIGS-015), payment activities (REQ-IPF-009).
  



---

# 3. Layers

## 3.1. InfluenceGen Odoo UI Layer
Handles all user interface aspects for the InfluenceGen addon, leveraging Odoo's presentation framework. This includes the influencer portal and administrative interfaces.

### 3.1.4. Technologystack
Odoo 18 (XML Views, QWeb Templates, Odoo Web Library (OWL) for JavaScript components, CSS/SCSS), Python Controllers

### 3.1.5. Language
Python, JavaScript, XML, CSS

### 3.1.6. Type
Presentation

### 3.1.7. Responsibilities

- Rendering influencer registration forms, KYC document upload interfaces, campaign discovery pages, content submission forms, AI image generation UIs (REQ-IOKYC-001, REQ-IOKYC-004, REQ-2-004, REQ-2-009, REQ-AIGS-005).
- Displaying influencer dashboards and profile management sections (REQ-IPDPM-002, REQ-IPDPM-003).
- Providing administrative interfaces for managing KYC, campaigns, users, AI settings, payments, and system configurations (REQ-IOKYC-011, REQ-2-007, REQ-PAC-014, REQ-UIUX-015).
- Implementing client-side validation and interactivity (REQ-IOKYC-014, REQ-DMG-013).
- Ensuring UI responsiveness and adherence to Odoo UI/UX standards (REQ-UIUX-001, REQ-UIUX-002).
- Meeting WCAG 2.1 Level AA accessibility standards for influencer-facing portal interfaces (REQ-IPDPM-010, REQ-14-001).

### 3.1.8. Components

- Odoo Views (`ir.ui.view`) for forms, lists, kanbans, dashboards.
- QWeb Templates for dynamic content rendering.
- OWL Components for interactive UI elements (e.g., AI image generator, file uploaders, dynamic filters).
- Odoo HTTP Controllers for portal page routing and specific AJAX endpoints.

### 3.1.9. Interfaces


### 3.1.10. Dependencies

- **Layer Id:** influencegen-odoo-business-logic-layer  
**Type:** Required  

## 3.2. InfluenceGen Odoo Business Logic Layer
Contains the core business logic, domain models, and application services for the InfluenceGen addon. Implemented primarily as Odoo Models and associated methods.

### 3.2.4. Technologystack
Odoo 18 (Python, Odoo ORM)

### 3.2.5. Language
Python

### 3.2.6. Type
BusinessLogic

### 3.2.7. Responsibilities

- Defining and managing InfluenceGen data models (InfluencerProfile, Campaign, KYCData, AIImageGenerationRequest, etc. as per database design - REQ-DMG-001 to REQ-DMG-009, REQ-DMG-023).
- Implementing business rules for influencer onboarding, KYC verification logic, social media and bank account verification (REQ-IOKYC-002, REQ-IOKYC-005, REQ-IOKYC-006, REQ-IOKYC-008).
- Managing campaign lifecycle, application processing, content review workflows, and performance metric calculation (REQ-2-001 to REQ-2-003, REQ-2-007, REQ-2-010, REQ-2-011, REQ-2-013).
- Handling AI image generation request processing logic (prompt validation, parameter handling, quota enforcement) before passing to N8N (REQ-AIGS-003, REQ-AIGS-004, REQ-AIGS-002).
- Calculating influencer payments and managing compensation models (REQ-IPF-003, REQ-IPF-004).
- Enforcing data validation rules (server-side) and uniqueness constraints (REQ-IOKYC-014, REQ-DMG-014, REQ-DMG-015).
- Managing user roles, permissions, and platform configurations via Odoo's mechanisms (REQ-PAC-001, REQ-PAC-002).
- Implementing data retention and legal hold logic (REQ-DRH-001, REQ-DRH-002, REQ-DRH-009).

### 3.2.8. Components

- Custom Odoo Models (e.g., `influence_gen.influencer_profile`, `influence_gen.campaign`, `influence_gen.kyc_data`, `influence_gen.ai_image_request`, `influence_gen.payment_record`, `influence_gen.audit_log`).
- Python methods within these models containing business logic.
- Odoo Services (if used for cross-model logic or specific functionalities).

### 3.2.9. Interfaces


### 3.2.10. Dependencies

- **Layer Id:** influencegen-odoo-infrastructure-integration-services-layer  
**Type:** Required  

## 3.3. InfluenceGen Odoo Infrastructure & Integration Services Layer
Manages interaction with Odoo's core infrastructure (database via ORM, file store, email, schedulers) and handles communication with external systems like N8N and third-party APIs.

### 3.3.4. Technologystack
Odoo 18 (Python), PostgreSQL (via Odoo ORM), `requests` library

### 3.3.5. Language
Python

### 3.3.6. Type
Infrastructure

### 3.3.7. Responsibilities

- Persisting and retrieving data using Odoo ORM (all REQs involving data storage).
- Securely handling file uploads (KYC documents, campaign content, AI images) using Odoo filestore or configured cloud storage (REQ-IOKYC-004, REQ-2-009, REQ-AIGS-006).
- Initiating N8N workflows via webhooks for AI image generation (REQ-IL-002).
- Providing a secure Odoo REST API callback endpoint for N8N to return AI image results (REQ-IL-003, REQ-IL-016).
- Integrating with third-party identity verification services (REQ-IOKYC-005, REQ-IL-011).
- Integrating with third-party bank account verification services (REQ-IOKYC-008, REQ-IPF-002).
- Integrating with Odoo Version 18 accounting module for payment processing (REQ-IPF-006, REQ-2-014).
- Sending email notifications using Odoo's mail system and templates (REQ-IOKYC-010, REQ-2-008, REQ-16-001 to REQ-16-005, REQ-16-015).
- Writing to the audit trail (all REQs mentioning audit logs like REQ-ATEL-005).
- Executing scheduled tasks (Odoo cron jobs) for data retention enforcement, report generation, etc. (REQ-DRH-002).

### 3.3.8. Components

- Odoo ORM API.
- Custom Python services/utility classes for calling N8N and other third-party APIs.
- Odoo HTTP Controllers acting as REST API endpoints for callbacks.
- Odoo `mail.template` and `mail.mail` for notifications.
- Odoo `ir.attachment` for file handling.
- Odoo `ir.cron` for scheduled tasks.

### 3.3.9. Interfaces


### 3.3.10. Dependencies


## 3.4. N8N Orchestration Layer
An external N8N instance and its configured workflows responsible for orchestrating asynchronous tasks, primarily AI image generation, and integrating with the AI backend service.

### 3.4.4. Technologystack
N8N (latest stable version)

### 3.4.5. Language
N/A (N8N visual workflow definition, JavaScript for custom functions)

### 3.4.6. Type
Integration

### 3.4.7. Responsibilities

- Receiving AI image generation requests from Odoo via webhooks (REQ-IL-002).
- Orchestrating the image generation process by integrating with AI backend services supporting 'Flux LoRA models' (REQ-AIGS-001, REQ-IL-005).
- Passing prompts and parameters from Odoo to the AI service.
- Handling responses, including generated images or temporary links, from the AI service.
- Returning generated images (or links) to Odoo's callback endpoint (REQ-IL-003, REQ-IL-010).
- Implementing error handling and retry logic for AI service calls (REQ-IL-009).
- Ensuring secure communication with Odoo and AI services (REQ-IL-007).
- Logging N8N workflow execution details (REQ-ATEL-010).

### 3.4.8. Components

- N8N Workflows specific to InfluenceGen (e.g., AI Image Generation Workflow).
- N8N Nodes (Webhook, HTTP Request, Function, Error Trigger, etc.).
- N8N Credentials management for AI service APIs.

### 3.4.9. Interfaces

### 3.4.9.1. Odoo to N8N Webhook Interface
#### 3.4.9.1.2. Type
Webhook (HTTP POST)

#### 3.4.9.1.3. Operations

- InitiateAIImageGeneration

#### 3.4.9.1.4. Visibility
Internal

### 3.4.9.2. N8N to Odoo Callback API Interface
#### 3.4.9.2.2. Type
REST API (HTTP POST)

#### 3.4.9.2.3. Operations

- ReceiveAIImageResult

#### 3.4.9.2.4. Visibility
Internal

### 3.4.9.3. N8N to AI Service API Interface
#### 3.4.9.3.2. Type
REST API

#### 3.4.9.3.3. Operations

- GenerateImageViaAIModel

#### 3.4.9.3.4. Visibility
Internal


### 3.4.10. Dependencies




---

# 4. Quality Attributes

- **Performance:**
  
  - **Description:** System responsiveness for user interactions and processing times for backend tasks.
  - **Tactics:**
    
    - Asynchronous processing for AI image generation via N8N (REQ-AIGS-001, REQ-AIGS-008).
    - Efficient Odoo ORM queries and database indexing (as per DB design notes).
    - Optimized OWL components and client-side logic for Odoo portal (REQ-UIUX-007).
    - Scalable AI model serving infrastructure (REQ-AIGS-009).
    - Caching strategies for frequently accessed, rarely changing data (e.g., campaign discovery, AI model list).
    
  
- **Scalability:**
  
  - **Description:** Ability of the system to handle increasing numbers of influencers, campaigns, AI generation requests, and data.
  - **Tactics:**
    
    - Odoo's inherent scalability features (multi-process, worker configuration).
    - Scalable N8N deployment.
    - Horizontally/vertically scalable AI model serving infrastructure (REQ-AIGS-009).
    - Scalable storage for KYC documents and generated images (Odoo filestore or cloud storage like S3 - REQ-AIGS-006).
    - Database partitioning for very large tables (e.g., AuditLog, GeneratedImage as per DB design notes).
    
  
- **Security:**
  
  - **Description:** Protection of sensitive data (PII, KYC, financial) and system integrity.
  - **Tactics:**
    
    - Odoo's role-based access control (RBAC) and security groups (REQ-PAC-001).
    - Encryption of PII, KYC, and financial data at rest (AES-256) and in transit (TLS 1.2+) (REQ-IOKYC-013, REQ-IPF-011, REQ-IL-007).
    - Secure API key and credentials management (REQ-IL-008, REQ-PAC-017).
    - Input validation (client-side and server-side) to prevent common vulnerabilities (REQ-IOKYC-014, REQ-DMG-013).
    - Content moderation for AI prompts (REQ-AIGS-003).
    - Comprehensive audit trails (REQ-IOKYC-016, REQ-ATEL-005).
    - Secure social media account verification methods (no password storage - REQ-IOKYC-006).
    - Rate limiting for critical APIs (REQ-PAC-013, REQ-IL-015).
    
  
- **Reliability:**
  
  - **Description:** System availability and fault tolerance, especially for critical integrations.
  - **Tactics:**
    
    - Robust error handling and retry mechanisms in N8N workflows and Odoo integration points (REQ-IL-009).
    - Transactional integrity provided by Odoo ORM.
    - Backup and recovery procedures for Odoo database and file store (REQ-12-016).
    - Monitoring and alerting for system failures and critical errors (REQ-16-008, REQ-16-009).
    - Disaster Recovery Plan (DRP) (REQ-12-016).
    
  
- **Maintainability:**
  
  - **Description:** Ease of modifying, updating, and troubleshooting the system.
  - **Tactics:**
    
    - Modular design using Odoo modules (REQ-DDSI-001).
    - Layered architecture within modules.
    - Adherence to Odoo development best practices and coding standards (REQ-DDSI-003).
    - Comprehensive documentation (technical, user, operational - REQ-DTS-005 to REQ-DTS-009).
    - Centralized logging and monitoring (REQ-ATEL-004, REQ-12-002).
    - Version control for all artifacts (REQ-DDSI-002).
    
  
- **Extensibility:**
  
  - **Description:** Ability to add new features or modify existing ones with minimal impact.
  - **Tactics:**
    
    - Odoo's modular architecture allowing addition of new modules.
    - Adaptable N8N workflow design (REQ-IL-006).
    - Extensible data models to accommodate future KYC steps or payment integrations (REQ-IOKYC-017, REQ-IPF-012).
    - Use of Odoo's inheritance and extension mechanisms.
    
  
- **Usability:**
  
  - **Description:** Ease of use for both influencers and platform administrators.
  - **Tactics:**
    
    - Adherence to Odoo UI/UX design language and standards (REQ-UIUX-001).
    - Intuitive navigation and clear information presentation (REQ-IPDPM-001, REQ-IPDPM-009).
    - Responsive design for various devices (REQ-UIUX-002).
    - Clear error messages and user feedback (REQ-UIUX-009, REQ-16-013).
    - In-app guidance and comprehensive user documentation (REQ-UIUX-011, REQ-DTS-006, REQ-DTS-007).
    
  
- **Accessibility:**
  
  - **Description:** Ensuring the influencer portal is usable by people with disabilities.
  - **Tactics:**
    
    - Strict adherence to WCAG 2.1 Level AA for influencer-facing interfaces (REQ-14-001 to REQ-14-005, REQ-UIUX-020).
    - Keyboard navigability, screen reader compatibility, sufficient color contrast, alt text for images.
    - Accessibility testing as part of QA (REQ-14-006).
    
  


---

