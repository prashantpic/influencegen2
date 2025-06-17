# Specification

# 1. Sequence Design Overview

- **Sequence_Diagram:**
  ### . AIImageGenerationFullFlow
  End-to-end flow: user requests AI image in Odoo, N8N orchestrates generation with AI service, Odoo receives and stores the result, and UI updates.

  #### .4. Purpose
  To generate AI-powered images for users within the platform.

  #### .5. Type
  ServiceInteraction

  #### .6. Participant Repository Ids
  
  - UI.InfluencerPortal
  - Service.AI.Odoo
  - Gateway.N8N
  - Orchestrator.N8N.AIWorkflow
  - External.AIService
  - Adapter.FileStorage
  - Platform.OdooCore
  
  #### .7. Key Interactions
  
  - User inputs prompt/params in UI.InfluencerPortal, submits to Service.AI.Odoo.
  - Service.AI.Odoo validates, checks quota, creates AIImageGenerationRequest record.
  - Service.AI.Odoo calls Gateway.N8N to trigger N8N webhook.
  - Gateway.N8N sends HTTP POST to Orchestrator.N8N.AIWorkflow webhook.
  - Orchestrator.N8N.AIWorkflow calls External.AIService.
  - External.AIService returns image data/link to Orchestrator.N8N.AIWorkflow.
  - Orchestrator.N8N.AIWorkflow calls Odoo callback API via Gateway.N8N.
  - Gateway.N8N (Odoo callback) receives image data/link, passes to Service.AI.Odoo.
  - Service.AI.Odoo downloads/stores image via Adapter.FileStorage.
  - Service.AI.Odoo creates GeneratedImage record, updates AIImageGenerationRequest status.
  - UI.InfluencerPortal updates to display generated image.
  
  #### .8. Related Feature Ids
  
  - REQ-AIGS-001
  - REQ-AIGS-005
  - REQ-AIGS-006
  - REQ-AIGS-008
  - REQ-IL-001
  - REQ-IL-002
  - REQ-IL-003
  - REQ-IL-004
  - REQ-IL-005
  - REQ-IL-010
  
  #### .9. Domain
  AI Image Generation

  #### .10. Metadata
  
  - **Complexity:** High
  - **Priority:** Critical
  


---

# 2. Sequence Diagram Details

- **Success:** True
- **Cache_Created:** True
- **Status:** refreshed
- **Cache_Id:** s8x7onlw5ckbufnbwoxnxy6twadb2k01r6h53p1l
- **Cache_Name:** cachedContents/s8x7onlw5ckbufnbwoxnxy6twadb2k01r6h53p1l
- **Cache_Display_Name:** repositories
- **Cache_Status_Verified:** True
- **Model:** models/gemini-2.5-pro-preview-03-25
- **Workflow_Id:** I9v2neJ0O4zJsz8J
- **Execution_Id:** 7486
- **Project_Id:** 14
- **Record_Id:** 19
- **Cache_Type:** repositories


---

