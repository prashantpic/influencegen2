# Repository Specification

# 1. Name
InfluenceGen.Odoo.Admin.Backend


---

# 2. Description
Provides all backend User Interface (UI) functionalities for Platform Administrators managing the InfluenceGen system within Odoo. This includes interfaces for: user management (influencers, roles, permissions), campaign creation and lifecycle management (reviewing applications, approving content, setting criteria), KYC submission review and approval/rejection, content moderation, system configuration (e.g., AI model parameters, quotas, email templates, business rule parameters), payment oversight, viewing audit logs, and accessing system health dashboards and reports. These interfaces are built using Odoo's backend view system (forms, lists, kanbans, etc.) and actions. It serves as the primary control panel for administrators to operate and maintain the InfluenceGen platform, ensuring they have the tools for comprehensive oversight and management. This repository interacts heavily with 'InfluenceGen.Odoo.Business.Services' (REPO-IGBS-003) for data and business logic, and may consume components from 'InfluenceGen.Odoo.Shared.UIComponents' (REPO-IGSUC-006) for consistent UI elements if applicable to backend views.


---

# 3. Type
WebFrontend


---

# 4. Namespace
InfluenceGen.Odoo.Admin


---

# 5. Output Path
odoo_modules/influence_gen_admin


---

# 6. Framework
Odoo 18


---

# 7. Language
Python, XML


---

# 8. Technology
HTTP, Odoo Backend Views, Odoo Actions


---

# 9. Thirdparty Libraries



---

# 10. Dependencies

- REPO-IGBS-003
- REPO-IGSUC-006
- REPO-IGSCU-007


---

# 11. Layer Ids

- influencegen-odoo-ui-layer


---

# 12. Requirements

- **Requirement Id:** REQ-IOKYC-011  
- **Requirement Id:** REQ-PAC-001  
- **Requirement Id:** REQ-PAC-002  
- **Requirement Id:** REQ-PAC-003  
- **Requirement Id:** REQ-PAC-004  
- **Requirement Id:** REQ-PAC-005  
- **Requirement Id:** REQ-PAC-006  
- **Requirement Id:** REQ-PAC-007  
- **Requirement Id:** REQ-PAC-008  
- **Requirement Id:** REQ-PAC-009  
- **Requirement Id:** REQ-PAC-010  
- **Requirement Id:** REQ-PAC-011  
- **Requirement Id:** REQ-PAC-012  
- **Requirement Id:** REQ-PAC-013  
- **Requirement Id:** REQ-PAC-014  
- **Requirement Id:** REQ-PAC-015  
- **Requirement Id:** REQ-PAC-016  
- **Requirement Id:** REQ-PAC-017  
- **Requirement Id:** REQ-2-001  
- **Requirement Id:** REQ-2-002  
- **Requirement Id:** REQ-2-003  
- **Requirement Id:** REQ-2-007  
- **Requirement Id:** REQ-2-010  
- **Requirement Id:** REQ-2-012  
- **Requirement Id:** REQ-2-014  
- **Requirement Id:** REQ-2-015  
- **Requirement Id:** REQ-AIGS-002  
- **Requirement Id:** REQ-AIGS-004  
- **Requirement Id:** REQ-AIGS-007  
- **Requirement Id:** REQ-IPF-003  
- **Requirement Id:** REQ-IPF-004  
- **Requirement Id:** REQ-IPF-005  
- **Requirement Id:** REQ-IPF-007  
- **Requirement Id:** REQ-IPF-008  
- **Requirement Id:** REQ-UIUX-003  
- **Requirement Id:** REQ-UIUX-015  
- **Requirement Id:** REQ-UIUX-016  
- **Requirement Id:** REQ-ATEL-003  
- **Requirement Id:** REQ-ATEL-008  
- **Requirement Id:** REQ-ATEL-011  
- **Requirement Id:** REQ-DRH-001  
- **Requirement Id:** REQ-DRH-003  
- **Requirement Id:** REQ-DRH-004  
- **Requirement Id:** REQ-DRH-005  
- **Requirement Id:** REQ-DRH-006  
- **Requirement Id:** REQ-DRH-007  
- **Requirement Id:** REQ-DRH-008  
- **Requirement Id:** REQ-DRH-009  
- **Requirement Id:** REQ-12-007  
- **Requirement Id:** REQ-16-012  


---

# 13. Generate Tests
True


---

# 14. Generate Documentation
True


---

# 15. Architecture Style
LayeredArchitecture


---

# 16. Id
REPO-IGAA-002


---

# 17. Architecture_Map

- influencegen-odoo-ui-layer


---

# 18. Components_Map

- influencegen-odoo-ui-layer


---

# 19. Requirements_Map

- REQ-IOKYC-011
- REQ-PAC-001
- REQ-2-001
- REQ-AIGS-002
- REQ-UIUX-003
- REQ-ATEL-008


---

