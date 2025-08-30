# Specification

# 1. Files

- **Path:** influence_gen_shared_ui/__init__.py  
**Description:** Python package initializer for the Odoo module. Imports subdirectories or modules if any Python logic were present, but primarily serves to mark the directory as a package. For a UI component library, this is often minimal.  
**Template:** Python Package Init  
**Dependancy Level:** 0  
**Name:** __init__  
**Type:** Python Module  
**Relative Path:** __init__.py  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Odoo Module Initialization
    
**Requirement Ids:**
    
    
**Purpose:** Initializes the 'influence_gen_shared_ui' Odoo module as a Python package.  
**Logic Description:** Contains standard Odoo module imports if necessary, typically empty or imports Python files from within the module if they exist.  
**Documentation:**
    
    - **Summary:** Standard Odoo Python package initializer.
    
**Namespace:** odoo.addons.influence_gen_shared_ui  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** influence_gen_shared_ui/__manifest__.py  
**Description:** Odoo module manifest file. Defines module metadata, dependencies, and asset bundles. Specifies JS, XML (QWeb), and SCSS files for shared UI components to be loaded by Odoo's asset management system for backend and frontend.  
**Template:** Odoo Manifest  
**Dependancy Level:** 0  
**Name:** __manifest__  
**Type:** Odoo Module Manifest  
**Relative Path:** __manifest__.py  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Module Definition
    - Asset Management Declaration
    - Dependency Declaration
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Declares the 'influence_gen_shared_ui' module to Odoo, listing its properties, dependencies, and assets like JavaScript components, QWeb templates, and SCSS stylesheets.  
**Logic Description:** A Python dictionary containing keys like 'name', 'version', 'summary', 'author', 'depends', 'data', 'assets'. The 'assets' key will list paths to all JS, XML, and SCSS files for the shared UI components, categorizing them for 'web.assets_common', 'web.assets_backend', and 'web.assets_frontend' as appropriate. For example, 'web.assets_common' would include 'influence_gen_shared_ui/static/src/scss/shared_*.scss' and 'influence_gen_shared_ui/static/src/js/utils/*.js'. 'web.assets_frontend' and 'web.assets_backend' would include 'influence_gen_shared_ui/static/src/components/**/*.js' and 'influence_gen_shared_ui/static/src/components/**/*.xml', and 'influence_gen_shared_ui/static/src/scss/components.scss'.  
**Documentation:**
    
    - **Summary:** Defines the metadata and resources for the InfluenceGen Shared UI Components Odoo module.
    
**Namespace:** odoo.addons.influence_gen_shared_ui  
**Metadata:**
    
    - **Category:** ModuleDefinition
    
- **Path:** influence_gen_shared_ui/static/src/scss/shared_variables.scss  
**Description:** SCSS file defining shared variables for colors, typography, spacing, breakpoints, etc., to ensure UI consistency across InfluenceGen components. These variables can be overridden for theming.  
**Template:** SCSS Stylesheet  
**Dependancy Level:** 0  
**Name:** shared_variables  
**Type:** Stylesheet  
**Relative Path:** static/src/scss/shared_variables.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Shared Styling Variables
    - Theming Foundation
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Centralizes common SASS variables (e.g., primary colors, font sizes, spacing units) used by shared UI components to maintain a consistent visual style.  
**Logic Description:** Contains SCSS variable definitions. Example: $ig-primary-color: #HEXCODE; $ig-font-family-base: 'Arial', sans-serif; $ig-spacing-unit: 8px;  
**Documentation:**
    
    - **Summary:** Defines global SCSS variables for the InfluenceGen UI component library.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** influence_gen_shared_ui/static/src/scss/shared_mixins.scss  
**Description:** SCSS file defining shared mixins for reusable style patterns (e.g., flexbox centering, media query helpers, button states) used across InfluenceGen components.  
**Template:** SCSS Stylesheet  
**Dependancy Level:** 0  
**Name:** shared_mixins  
**Type:** Stylesheet  
**Relative Path:** static/src/scss/shared_mixins.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Reusable SCSS Mixins
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Provides a collection of reusable SCSS mixins to encapsulate common style patterns and reduce code duplication in component stylesheets.  
**Logic Description:** Contains SCSS mixin definitions. Example: @mixin ig-flex-center { display: flex; align-items: center; justify-content: center; }  
**Documentation:**
    
    - **Summary:** Defines global SCSS mixins for the InfluenceGen UI component library.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** influence_gen_shared_ui/static/src/scss/shared_global.scss  
**Description:** SCSS file for global styles or utility classes that apply across multiple InfluenceGen shared components. May include light resets or base styling for common HTML elements used within components, if not covered by Odoo's core styles.  
**Template:** SCSS Stylesheet  
**Dependancy Level:** 1  
**Name:** shared_global  
**Type:** Stylesheet  
**Relative Path:** static/src/scss/shared_global.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Global Utility Styles
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Contains base styles and global utility classes for InfluenceGen components, ensuring consistency. Imports shared_variables.scss and shared_mixins.scss.  
**Logic Description:** @import 'shared_variables.scss'; @import 'shared_mixins.scss'; Defines base component styles or utility classes like .ig-text-truncate, .ig-visually-hidden.  
**Documentation:**
    
    - **Summary:** Provides global utility styles and base styling for InfluenceGen components.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** influence_gen_shared_ui/static/src/scss/components.scss  
**Description:** Main SCSS file that imports all individual component SCSS files. This file is typically included in the Odoo assets bundle.  
**Template:** SCSS Stylesheet  
**Dependancy Level:** 1  
**Name:** components  
**Type:** Stylesheet  
**Relative Path:** static/src/scss/components.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Component Style Aggregation
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Aggregates styles from all individual shared UI components by importing their respective SCSS files. This is used for bundling component styles.  
**Logic Description:** Contains @import statements for each component's SCSS file. Example: @import '../components/campaign_card/campaign_card.scss'; @import '../components/metric_tile/metric_tile.scss';  
**Documentation:**
    
    - **Summary:** Main SCSS file for importing all shared component styles.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** influence_gen_shared_ui/static/src/js/utils/ui_helpers.js  
**Description:** JavaScript module containing shared utility functions for InfluenceGen UI components. Examples: data formatting functions, event handling helpers, DOM manipulation utilities not provided by OWL.  
**Template:** JavaScript Module  
**Dependancy Level:** 0  
**Name:** ui_helpers  
**Type:** Utility  
**Relative Path:** static/src/js/utils/ui_helpers.js  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** formatCurrency  
**Parameters:**
    
    - amount
    - currencyCode
    
**Return Type:** string  
**Attributes:** export const  
    - **Name:** formatDate  
**Parameters:**
    
    - dateString
    - format
    
**Return Type:** string  
**Attributes:** export const  
    - **Name:** debounce  
**Parameters:**
    
    - func
    - delay
    
**Return Type:** function  
**Attributes:** export const  
    
**Implemented Features:**
    
    - UI Utility Functions
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    - REQ-UIUX-007
    
**Purpose:** Provides reusable JavaScript helper functions for common UI tasks across shared components, promoting code reuse and consistency.  
**Logic Description:** Contains exported JavaScript functions for tasks like formatting dates, numbers, currencies, debouncing user input, or other common UI logic.  
**Documentation:**
    
    - **Summary:** Shared JavaScript utility functions for InfluenceGen UI components.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Utils  
**Metadata:**
    
    - **Category:** Utility
    
- **Path:** influence_gen_shared_ui/static/src/components/campaign_card/CampaignCard.js  
**Description:** OWL component for displaying a summary of campaign information in a card format. Props: campaignData (object).  
**Template:** Odoo OWL Component JS  
**Dependancy Level:** 2  
**Name:** CampaignCard  
**Type:** Component  
**Relative Path:** static/src/components/campaign_card/CampaignCard.js  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    - Reusable Component
    
**Members:**
    
    - **Name:** campaign  
**Type:** Object  
**Attributes:** prop  
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** onViewDetailsClick  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Campaign Information Display
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Defines the JavaScript logic for the CampaignCard OWL component, handling props, state, and event handlers for displaying campaign summaries.  
**Logic Description:** Imports Component, useState from OWL. Defines props (e.g., campaign object with name, description, status, dates). Setup method initializes state. Event handlers for actions like 'view details'.  
**Documentation:**
    
    - **Summary:** OWL component to render a campaign summary card. Expects 'campaign' prop with campaign details.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.CampaignCard  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/campaign_card/CampaignCard.xml  
**Description:** QWeb template for the CampaignCard OWL component. Defines the HTML structure for displaying campaign name, status, dates, and a brief description.  
**Template:** Odoo OWL Component QWeb Template  
**Dependancy Level:** 2  
**Name:** CampaignCard  
**Type:** ComponentTemplate  
**Relative Path:** static/src/components/campaign_card/CampaignCard.xml  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign Card UI Structure
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Provides the HTML structure for the CampaignCard component, using QWeb directives to render dynamic data from the component's state and props.  
**Logic Description:** Uses t-name, t-props, t-esc, t-if, t-foreach directives. Structure includes elements for campaign title, status badge (potentially another shared component), key dates, and a summary. May include a 'View Details' button.  
**Documentation:**
    
    - **Summary:** QWeb template for the CampaignCard component.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.CampaignCard  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/campaign_card/campaign_card.scss  
**Description:** SCSS styles specific to the CampaignCard component. Ensures the card is visually appealing and consistent with the InfluenceGen theme.  
**Template:** Odoo Component SCSS  
**Dependancy Level:** 2  
**Name:** campaign_card.scss  
**Type:** Stylesheet  
**Relative Path:** static/src/components/campaign_card/campaign_card.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Campaign Card Styling
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Contains SCSS rules to style the CampaignCard component, including layout, typography, colors, and spacing. May import shared variables/mixins.  
**Logic Description:** Defines styles for .o_campaign_card container, .o_campaign_card_title, .o_campaign_card_status, .o_campaign_card_description etc. Uses variables from shared_variables.scss.  
**Documentation:**
    
    - **Summary:** SCSS styles for the CampaignCard component.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** influence_gen_shared_ui/static/src/components/metric_tile/MetricTile.js  
**Description:** OWL component for displaying a single key metric, often used in dashboards. Props: label (string), value (string|number), unit (string, optional), trend (string, optional: 'up', 'down', 'neutral'), iconClass (string, optional).  
**Template:** Odoo OWL Component JS  
**Dependancy Level:** 2  
**Name:** MetricTile  
**Type:** Component  
**Relative Path:** static/src/components/metric_tile/MetricTile.js  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    - Reusable Component
    
**Members:**
    
    - **Name:** label  
**Type:** String  
**Attributes:** prop  
    - **Name:** value  
**Type:** String | Number  
**Attributes:** prop  
    - **Name:** unit  
**Type:** String  
**Attributes:** prop  
    - **Name:** trend  
**Type:** String  
**Attributes:** prop  
    - **Name:** iconClass  
**Type:** String  
**Attributes:** prop  
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Metric Display Tile
    
**Requirement Ids:**
    
    - REQ-UIUX-019
    - REQ-UIUX-001
    
**Purpose:** Defines the JavaScript logic for the MetricTile OWL component, used for displaying key performance indicators or other metrics in dashboards.  
**Logic Description:** Imports Component from OWL. Defines props for label, value, unit, trend indication (up/down/neutral), and optional icon. Setup method handles prop processing.  
**Documentation:**
    
    - **Summary:** OWL component to render a metric tile. Expects 'label' and 'value' props, with optional 'unit', 'trend', and 'iconClass'.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.MetricTile  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/metric_tile/MetricTile.xml  
**Description:** QWeb template for the MetricTile OWL component. Structures the display of the metric label, value, unit, and trend indicator/icon.  
**Template:** Odoo OWL Component QWeb Template  
**Dependancy Level:** 2  
**Name:** MetricTile  
**Type:** ComponentTemplate  
**Relative Path:** static/src/components/metric_tile/MetricTile.xml  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Metric Tile UI Structure
    
**Requirement Ids:**
    
    - REQ-UIUX-019
    - REQ-UIUX-001
    
**Purpose:** Provides the HTML structure for the MetricTile component, rendering the label, value, unit, and an optional trend icon based on props.  
**Logic Description:** Uses t-name, t-props. Structure includes elements for the metric label, the main value, an optional unit, and an icon representing trend (e.g., arrow up/down) if the 'trend' prop is provided.  
**Documentation:**
    
    - **Summary:** QWeb template for the MetricTile component.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.MetricTile  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/metric_tile/metric_tile.scss  
**Description:** SCSS styles for the MetricTile component, ensuring it's visually clear and suitable for dashboard displays.  
**Template:** Odoo Component SCSS  
**Dependancy Level:** 2  
**Name:** metric_tile.scss  
**Type:** Stylesheet  
**Relative Path:** static/src/components/metric_tile/metric_tile.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Metric Tile Styling
    
**Requirement Ids:**
    
    - REQ-UIUX-019
    - REQ-UIUX-001
    
**Purpose:** Contains SCSS rules for styling the MetricTile component, including its layout, typography for label and value, and trend indicator styles.  
**Logic Description:** Defines styles for .o_metric_tile container, .o_metric_tile_label, .o_metric_tile_value, .o_metric_tile_trend_icon. Uses shared variables.  
**Documentation:**
    
    - **Summary:** SCSS styles for the MetricTile component.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** influence_gen_shared_ui/static/src/components/data_chart_wrapper/DataChartWrapper.js  
**Description:** OWL component that acts as a wrapper for a third-party charting library (e.g., Chart.js, D3.js if integrated, or Odoo's native charting capabilities). Props: chartType (string), chartData (object), chartOptions (object).  
**Template:** Odoo OWL Component JS  
**Dependancy Level:** 2  
**Name:** DataChartWrapper  
**Type:** Component  
**Relative Path:** static/src/components/data_chart_wrapper/DataChartWrapper.js  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    - Reusable Component
    - Wrapper
    
**Members:**
    
    - **Name:** chartType  
**Type:** String  
**Attributes:** prop  
    - **Name:** chartData  
**Type:** Object  
**Attributes:** prop  
    - **Name:** chartOptions  
**Type:** Object  
**Attributes:** prop  
    - **Name:** chartInstance  
**Type:** Object  
**Attributes:** state  
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** onMounted  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** onWillUpdateProps  
**Parameters:**
    
    - nextProps
    
**Return Type:** void  
**Attributes:**   
    - **Name:** onWillUnmount  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Chart Display Wrapper
    
**Requirement Ids:**
    
    - REQ-UIUX-019
    - REQ-UIUX-001
    
**Purpose:** Provides a consistent way to render charts within the InfluenceGen platform by wrapping a charting library or Odoo's chart rendering logic.  
**Logic Description:** Imports Component, onMounted, onWillUpdateProps, onWillUnmount from OWL. Takes chartType, chartData, and chartOptions as props. In onMounted, initializes the chart instance. In onWillUpdateProps, updates the chart if data/options change. In onWillUnmount, destroys the chart instance to prevent memory leaks. This component needs to interact with a chosen charting library (e.g. Chart.js, or Odoo's graph view helpers if applicable).  
**Documentation:**
    
    - **Summary:** OWL component wrapper for displaying charts. Takes chart type, data, and options as props.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.DataChartWrapper  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/data_chart_wrapper/DataChartWrapper.xml  
**Description:** QWeb template for the DataChartWrapper. Typically a single container element (e.g., a canvas or div) where the chart will be rendered by JavaScript.  
**Template:** Odoo OWL Component QWeb Template  
**Dependancy Level:** 2  
**Name:** DataChartWrapper  
**Type:** ComponentTemplate  
**Relative Path:** static/src/components/data_chart_wrapper/DataChartWrapper.xml  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Chart Container UI
    
**Requirement Ids:**
    
    - REQ-UIUX-019
    - REQ-UIUX-001
    
**Purpose:** Provides the HTML container (e.g., a canvas element or a div) for the JavaScript-rendered chart.  
**Logic Description:** Uses t-name. Contains a single div or canvas element with a unique t-ref attribute that the JavaScript component logic will use to mount the chart.  
**Documentation:**
    
    - **Summary:** QWeb template for the DataChartWrapper component.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.DataChartWrapper  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/data_chart_wrapper/data_chart_wrapper.scss  
**Description:** SCSS styles for the DataChartWrapper, primarily for sizing and container styling. Specific chart styling is usually handled by chart library options.  
**Template:** Odoo Component SCSS  
**Dependancy Level:** 2  
**Name:** data_chart_wrapper.scss  
**Type:** Stylesheet  
**Relative Path:** static/src/components/data_chart_wrapper/data_chart_wrapper.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Chart Wrapper Styling
    
**Requirement Ids:**
    
    - REQ-UIUX-019
    - REQ-UIUX-001
    
**Purpose:** Styles the container of the chart, ensuring proper sizing and responsiveness.  
**Logic Description:** Defines styles for .o_data_chart_wrapper, potentially setting width, height, aspect-ratio, or responsive behavior for the chart container.  
**Documentation:**
    
    - **Summary:** SCSS styles for the DataChartWrapper component.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** influence_gen_shared_ui/static/src/components/loading_indicator/LoadingIndicator.js  
**Description:** OWL component for a reusable loading indicator (e.g., spinner). Props: size (string, optional: 'sm', 'md', 'lg'), message (string, optional).  
**Template:** Odoo OWL Component JS  
**Dependancy Level:** 2  
**Name:** LoadingIndicator  
**Type:** Component  
**Relative Path:** static/src/components/loading_indicator/LoadingIndicator.js  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    - Reusable Component
    
**Members:**
    
    - **Name:** size  
**Type:** String  
**Attributes:** prop  
    - **Name:** message  
**Type:** String  
**Attributes:** prop  
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Loading State Indication
    
**Requirement Ids:**
    
    - REQ-UIUX-007
    - REQ-UIUX-001
    
**Purpose:** Defines the JavaScript logic for a reusable loading indicator OWL component. Used to provide feedback during data fetching or processing.  
**Logic Description:** Imports Component from OWL. Defines props for size ('sm', 'md', 'lg', default 'md') and an optional loading message. Computed properties might determine CSS classes based on size.  
**Documentation:**
    
    - **Summary:** OWL component for a visual loading indicator. Props: size, message.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.LoadingIndicator  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/loading_indicator/LoadingIndicator.xml  
**Description:** QWeb template for the LoadingIndicator. Displays a spinner (CSS or SVG) and an optional message.  
**Template:** Odoo OWL Component QWeb Template  
**Dependancy Level:** 2  
**Name:** LoadingIndicator  
**Type:** ComponentTemplate  
**Relative Path:** static/src/components/loading_indicator/LoadingIndicator.xml  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Loading Indicator UI
    
**Requirement Ids:**
    
    - REQ-UIUX-007
    - REQ-UIUX-001
    
**Purpose:** Provides the HTML structure for the loading indicator, typically a spinner animation and an optional text message.  
**Logic Description:** Uses t-name. Contains markup for a spinner element (could be an SVG or CSS-animated divs) and a conditional (t-if) paragraph for the loading message.  
**Documentation:**
    
    - **Summary:** QWeb template for the LoadingIndicator component.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.LoadingIndicator  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/loading_indicator/loading_indicator.scss  
**Description:** SCSS styles for the LoadingIndicator, including spinner animation and layout.  
**Template:** Odoo Component SCSS  
**Dependancy Level:** 2  
**Name:** loading_indicator.scss  
**Type:** Stylesheet  
**Relative Path:** static/src/components/loading_indicator/loading_indicator.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Loading Indicator Styling
    
**Requirement Ids:**
    
    - REQ-UIUX-007
    - REQ-UIUX-001
    
**Purpose:** Styles the loading indicator, including any spinner animations, sizing, and message typography.  
**Logic Description:** Defines styles for .o_loading_indicator and its child elements. Includes CSS keyframe animations for spinners if not using an SVG/image.  
**Documentation:**
    
    - **Summary:** SCSS styles for the LoadingIndicator component.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** influence_gen_shared_ui/static/src/components/status_badge/StatusBadge.js  
**Description:** OWL component for displaying a status badge with configurable text and color based on status type. Props: status (string), type (string: 'info', 'success', 'warning', 'danger', 'default').  
**Template:** Odoo OWL Component JS  
**Dependancy Level:** 2  
**Name:** StatusBadge  
**Type:** Component  
**Relative Path:** static/src/components/status_badge/StatusBadge.js  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    - Reusable Component
    
**Members:**
    
    - **Name:** statusText  
**Type:** String  
**Attributes:** prop  
    - **Name:** statusType  
**Type:** String  
**Attributes:** prop  
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    - **Name:** badgeClass  
**Type:** String  
**Attributes:** get  
    
**Implemented Features:**
    
    - Status Display Badge
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Defines the JavaScript logic for a reusable status badge component. It determines the badge's appearance based on the 'type' prop.  
**Logic Description:** Imports Component from OWL. Props for 'statusText' (the text to display) and 'statusType' ('info', 'success', 'warning', 'danger', 'neutral', default 'default'). A computed property 'badgeClass' returns the appropriate CSS class based on 'statusType'.  
**Documentation:**
    
    - **Summary:** OWL component for a status badge. Props: statusText, statusType.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.StatusBadge  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/status_badge/StatusBadge.xml  
**Description:** QWeb template for the StatusBadge component. A simple span or div with dynamic classes for styling.  
**Template:** Odoo OWL Component QWeb Template  
**Dependancy Level:** 2  
**Name:** StatusBadge  
**Type:** ComponentTemplate  
**Relative Path:** static/src/components/status_badge/StatusBadge.xml  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Status Badge UI
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Provides the HTML structure for the status badge, typically a span element that displays the status text and applies dynamic styling.  
**Logic Description:** Uses t-name. A span element with a base class '.o_status_badge' and a dynamic class bound to `badgeClass` from the component. Displays `props.statusText`.  
**Documentation:**
    
    - **Summary:** QWeb template for the StatusBadge component.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.StatusBadge  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/status_badge/status_badge.scss  
**Description:** SCSS styles for the StatusBadge component, defining different appearances (colors, backgrounds) for various status types.  
**Template:** Odoo Component SCSS  
**Dependancy Level:** 2  
**Name:** status_badge.scss  
**Type:** Stylesheet  
**Relative Path:** static/src/components/status_badge/status_badge.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Status Badge Styling
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Styles the status badge, providing distinct visual cues for different status types (e.g., green for success, red for danger) using shared color variables.  
**Logic Description:** Defines base styles for .o_status_badge. Defines modifier classes like .o_status_badge--success, .o_status_badge--warning, etc., each setting appropriate background-color and color using variables from shared_variables.scss.  
**Documentation:**
    
    - **Summary:** SCSS styles for the StatusBadge component.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    
- **Path:** influence_gen_shared_ui/static/src/components/profile_snippet/ProfileSnippet.js  
**Description:** OWL component for displaying a small snippet of an influencer's profile (e.g., avatar, name, main niche). Props: influencer (object).  
**Template:** Odoo OWL Component JS  
**Dependancy Level:** 2  
**Name:** ProfileSnippet  
**Type:** Component  
**Relative Path:** static/src/components/profile_snippet/ProfileSnippet.js  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    - Reusable Component
    
**Members:**
    
    - **Name:** influencer  
**Type:** Object  
**Attributes:** prop  
    
**Methods:**
    
    - **Name:** setup  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:**   
    
**Implemented Features:**
    
    - Influencer Profile Snippet Display
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Defines the JavaScript logic for an OWL component that displays a compact summary of an influencer's profile.  
**Logic Description:** Imports Component from OWL. Props: 'influencer' object containing at least avatar URL, full name, and primary niche/area of influence.  
**Documentation:**
    
    - **Summary:** OWL component for a brief influencer profile snippet. Props: influencer.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.ProfileSnippet  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/profile_snippet/ProfileSnippet.xml  
**Description:** QWeb template for the ProfileSnippet OWL component. Displays an avatar, name, and primary niche.  
**Template:** Odoo OWL Component QWeb Template  
**Dependancy Level:** 2  
**Name:** ProfileSnippet  
**Type:** ComponentTemplate  
**Relative Path:** static/src/components/profile_snippet/ProfileSnippet.xml  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Profile Snippet UI Structure
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Provides the HTML structure for the influencer profile snippet, showing an avatar image, name, and key detail.  
**Logic Description:** Uses t-name. Includes an img tag for the avatar, a span/div for the influencer's name, and another for their primary niche or a short bio snippet.  
**Documentation:**
    
    - **Summary:** QWeb template for the ProfileSnippet component.
    
**Namespace:** InfluenceGen.Odoo.Shared.UI.Components.ProfileSnippet  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** influence_gen_shared_ui/static/src/components/profile_snippet/profile_snippet.scss  
**Description:** SCSS styles for the ProfileSnippet component, focusing on layout and typography for a compact display.  
**Template:** Odoo Component SCSS  
**Dependancy Level:** 2  
**Name:** profile_snippet.scss  
**Type:** Stylesheet  
**Relative Path:** static/src/components/profile_snippet/profile_snippet.scss  
**Repository Id:** REPO-IGSUC-006  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Profile Snippet Styling
    
**Requirement Ids:**
    
    - REQ-UIUX-001
    
**Purpose:** Styles the influencer profile snippet for a clean and compact presentation, suitable for lists or headers.  
**Logic Description:** Defines styles for .o_profile_snippet container, .o_profile_snippet_avatar, .o_profile_snippet_name, .o_profile_snippet_detail. Ensures proper alignment and spacing.  
**Documentation:**
    
    - **Summary:** SCSS styles for the ProfileSnippet component.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Styling
    


---

# 2. Configuration

- **Feature Toggles:**
  
  
- **Database Configs:**
  
  


---

