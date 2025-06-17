# Software Design Specification for InfluenceGen.Odoo.Shared.UIComponents

## 1. Introduction

### 1.1 Purpose
This document outlines the software design specification for the `InfluenceGen.Odoo.Shared.UIComponents` Odoo module. This module serves as a centralized library of custom, reusable User Interface (UI) components built with Odoo's Web Library (OWL) and QWeb. These components are intended for use across various InfluenceGen frontend modules, including the Influencer Portal (`InfluenceGen.Odoo.Portal.Endpoints`) and the Administrator Backend (`InfluenceGen.Odoo.Admin.Backend`), to ensure UI consistency, reduce code duplication, and streamline frontend development.

### 1.2 Scope
This SDS covers the design and implementation details for:
*   Shared SCSS styling infrastructure (variables, mixins, global styles).
*   Shared JavaScript utility functions.
*   A collection of reusable OWL components, including:
    *   `CampaignCard`: Displays campaign summary.
    *   `MetricTile`: Displays a single key metric.
    *   `DataChartWrapper`: A wrapper for rendering charts.
    *   `LoadingIndicator`: Visual feedback for loading states.
    *   `StatusBadge`: Displays status information with appropriate styling.
    *   `ProfileSnippet`: Displays a compact influencer profile summary.
*   Odoo module definition and asset management.

### 1.3 Intended Audience
This document is intended for software developers involved in the implementation of the InfluenceGen platform, particularly those working on frontend Odoo modules.

### 1.4 Acronyms and Abbreviations
*   **AI:** Artificial Intelligence
*   **CSS:** Cascading Style Sheets
*   **FAQ:** Frequently Asked Questions
*   **HTML:** HyperText Markup Language
*   **JS:** JavaScript
*   **JSON:** JavaScript Object Notation
*   **OWL:** Odoo Web Library
*   **QWeb:** Odoo's primary templating engine
*   **REQ:** Requirement
*   **SCSS:** Sassy Cascading Style Sheets
*   **SDS:** Software Design Specification
*   **UI:** User Interface
*   **UX:** User Experience
*   **XML:** Extensible Markup Language

## 2. General Design Principles

The shared UI components will adhere to the following principles:

*   **Consistency (REQ-UIUX-001):** Components will strictly follow Odoo 18's UI/UX design language and standards. Shared SCSS variables and mixins will be used to enforce visual consistency.
*   **Reusability:** Components will be designed to be generic and configurable through properties (props) to maximize their applicability across different parts of the InfluenceGen platform.
*   **Modularity:** Each component will be self-contained with its own JS, XML (QWeb template), and SCSS files.
*   **Performance (REQ-UIUX-007):** Components will be optimized for efficient rendering and minimal impact on page load times. Event handling and state management will be designed thoughtfully.
*   **Maintainability:** Code will be well-documented, following Odoo and JavaScript/SCSS best practices.
*   **Accessibility:** While specific WCAG compliance is primarily targeted at the portal, general accessibility principles (e.g., semantic HTML, keyboard considerations where applicable within component scope) will be considered.

## 3. Module Structure and Asset Management

### 3.1 Odoo Module Definition
The module will be named `influence_gen_shared_ui`.

#### 3.1.1 `__init__.py`
*   **Path:** `influence_gen_shared_ui/__init__.py`
*   **Purpose:** Standard Python package initializer. Marks the directory as an Odoo module.
*   **Content:**
    python
    # -*- coding: utf-8 -*-
    # Part of Odoo. See LICENSE file for full copyright and licensing details.
    
    *Note: This file will be mostly empty as this module primarily contains static assets and OWL components, not extensive Python backend logic.*

#### 3.1.2 `__manifest__.py`
*   **Path:** `influence_gen_shared_ui/__manifest__.py`
*   **Purpose:** Declares the module metadata, dependencies, and asset bundles to Odoo.
*   **Content Structure:**
    python
    # -*- coding: utf-8 -*-
    {
        'name': 'InfluenceGen Shared UI Components',
        'version': '18.0.1.0.0',
        'summary': 'Centralized library of reusable UI components for the InfluenceGen platform.',
        'description': """
    This module provides a collection of custom, reusable User Interface (UI) components
    built using Odoo's Web Library (OWL) and QWeb templates. These components are
    intended for use across different InfluenceGen Odoo frontend modules to promote
    UI consistency, reduce code duplication, and accelerate frontend development.
        """,
        'author': 'SSS-AI',
        'website': 'https://www.example.com', # Replace with actual website
        'category': 'InfluenceGen/User Interface',
        'license': 'OEEL-1', # Or appropriate Odoo license
        'depends': [
            'web', # Core Odoo web framework dependency
        ],
        'data': [
            # No XML views to load directly in 'data' for this type of module typically
        ],
        'assets': {
            'web.assets_common': [
                # Shared SCSS (compiled by Odoo's asset pipeline)
                'influence_gen_shared_ui/static/src/scss/shared_variables.scss',
                'influence_gen_shared_ui/static/src/scss/shared_mixins.scss',
                'influence_gen_shared_ui/static/src/scss/shared_global.scss',
                'influence_gen_shared_ui/static/src/scss/components.scss',
                # Shared JS Utilities
                'influence_gen_shared_ui/static/src/js/utils/ui_helpers.js',
            ],
            'web.assets_backend': [
                # OWL Components for Backend
                'influence_gen_shared_ui/static/src/components/**/*.js',
                'influence_gen_shared_ui/static/src/components/**/*.xml',
                # Note: component-specific SCSS is imported via components.scss listed in web.assets_common
            ],
            'web.assets_frontend': [
                # OWL Components for Frontend/Portal
                'influence_gen_shared_ui/static/src/components/**/*.js',
                'influence_gen_shared_ui/static/src/components/**/*.xml',
                # Note: component-specific SCSS is imported via components.scss listed in web.assets_common
            ],
        },
        'installable': True,
        'application': False,
        'auto_install': False,
    }
    
    *   **Note:** The `assets` section is crucial. It tells Odoo where to find the JS, XML (QWeb), and SCSS files. The `web.assets_common` bundle is loaded in both frontend and backend. Specific components might be selectively bundled for frontend or backend if needed, but for a shared library, common availability is often preferred. Component-specific SCSS will be imported into `components.scss`.

## 4. Styling Strategy (SCSS)

SCSS will be used for styling to leverage variables, mixins, and nesting for more maintainable and organized CSS.

#### 4.1 `static/src/scss/shared_variables.scss`
*   **Purpose:** Defines global SCSS variables for consistent theming.
*   **Key Variables (Examples):**
    *   Colors: `$ig-primary-color`, `$ig-secondary-color`, `$ig-success-color`, `$ig-warning-color`, `$ig-danger-color`, `$ig-info-color`, `$ig-text-color`, `$ig-border-color`.
    *   Typography: `$ig-font-family-base`, `$ig-font-size-base`, `$ig-font-size-sm`, `$ig-font-size-lg`, `$ig-line-height-base`.
    *   Spacing: `$ig-spacing-unit` (e.g., 8px), `$ig-padding-base`, `$ig-margin-base`.
    *   Borders: `$ig-border-radius`, `$ig-border-width`.
    *   Breakpoints: `$ig-breakpoint-sm`, `$ig-breakpoint-md`, `$ig-breakpoint-lg` for responsive design.

#### 4.2 `static/src/scss/shared_mixins.scss`
*   **Purpose:** Provides reusable SCSS mixins for common styling patterns.
*   **Key Mixins (Examples):**
    *   `ig-flex-center()`: Applies flex properties for centering content.
    *   `ig-media-breakpoint-up($name)`: Media query helper using defined breakpoints.
    *   `ig-button-variant($background, $color, $border)`: Generates button styles.
    *   `ig-truncate-text()`: Applies styles for text truncation with ellipsis.

#### 4.3 `static/src/scss/shared_global.scss`
*   **Purpose:** Contains base styles applicable across multiple components or global utility classes.
*   **Content:**
    *   Imports `shared_variables.scss` and `shared_mixins.scss`.
    *   May include light resets or very basic styling for common HTML elements if not sufficiently covered by Odoo core styles.
    *   Utility classes (e.g., `.ig-text-muted`, `.ig-mb-1` (margin-bottom utility based on `$ig-spacing-unit`)).

#### 4.4 `static/src/scss/components.scss`
*   **Purpose:** Acts as a main manifest file for importing all individual component SCSS files.
*   **Content:**
    scss
    // Import shared foundations
    @import 'shared_variables';
    @import 'shared_mixins';
    @import 'shared_global';

    // Import individual component styles
    @import '../components/campaign_card/campaign_card.scss';
    @import '../components/metric_tile/metric_tile.scss';
    @import '../components/data_chart_wrapper/data_chart_wrapper.scss';
    @import '../components/loading_indicator/loading_indicator.scss';
    @import '../components/status_badge/status_badge.scss';
    @import '../components/profile_snippet/profile_snippet.scss';
    // Add other component SCSS imports here
    

## 5. Shared JavaScript Utilities

#### 5.1 `static/src/js/utils/ui_helpers.js`
*   **Purpose:** Provides common JavaScript utility functions for UI components.
*   **Namespace:** `InfluenceGen.Odoo.Shared.UI.Utils` (conceptually, actual export/import will use ES modules).
*   **Functions:**
    *   `formatCurrency(amount, currencyCode, locale = 'en-US')`: Formats a number as currency.
        *   **Parameters:** `amount` (Number), `currencyCode` (String, e.g., 'USD'), `locale` (String, optional).
        *   **Returns:** `String` (formatted currency string).
        *   **Logic:** Uses `Intl.NumberFormat`.
    *   `formatDate(dateStringOrObject, options = { year: 'numeric', month: 'short', day: 'numeric' }, locale = 'en-US')`: Formats a date.
        *   **Parameters:** `dateStringOrObject` (String or Date object), `options` (Object, Intl.DateTimeFormat options), `locale` (String, optional).
        *   **Returns:** `String` (formatted date string).
        *   **Logic:** Uses `Intl.DateTimeFormat`.
    *   `debounce(func, delay)`: Returns a debounced version of the passed function.
        *   **Parameters:** `func` (Function), `delay` (Number, milliseconds).
        *   **Returns:** `Function` (debounced function).
        *   **Logic:** Standard debounce implementation using `setTimeout` and `clearTimeout`.
    *   `truncateText(text, maxLength, ellipsis = '...')`: Truncates text to a maximum length.
        *   **Parameters:** `text` (String), `maxLength` (Number), `ellipsis` (String, optional).
        *   **Returns:** `String` (truncated text).
    *   `getInitials(name, count = 2)`: Generates initials from a name string.
        *   **Parameters:** `name` (String), `count` (Number, optional, number of initials).
        *   **Returns:** `String` (initials).
    *   `slugify(text)`: Converts a string to a slug (lowercase, dashes for spaces, remove special chars).
        *   **Parameters:** `text` (String).
        *   **Returns:** `String` (slugified text).
*   **Implementation Detail:** All functions should be exported using `export const`.

## 6. Component Specifications

All OWL components will be structured with a `.js` file for logic, an `.xml` file for the QWeb template, and a `.scss` file for styles.

### 6.1 CampaignCard Component
*   **Purpose:** Displays a summary of a campaign in a card format. (REQ-UIUX-001)
*   **Files:**
    *   `static/src/components/campaign_card/CampaignCard.js`
    *   `static/src/components/campaign_card/CampaignCard.xml`
    *   `static/src/components/campaign_card/campaign_card.scss`
*   **JavaScript (`CampaignCard.js`):**
    *   **Namespace:** `InfluenceGen.Odoo.Shared.UI.Components.CampaignCard`
    *   **Class:** `CampaignCard extends Component`
    *   **Props:**
        *   `campaign`: (Object, required) Containing campaign details:
            *   `id`: (Number | String) Campaign identifier.
            *   `name`: (String) Campaign name.
            *   `status`: (String) Campaign status (e.g., 'Published', 'Ongoing', 'Completed').
            *   `statusType`: (String, optional) Type for `StatusBadge` (e.g., 'success', 'info').
            *   `startDate`: (String | Date) Campaign start date.
            *   `endDate`: (String | Date) Campaign end date.
            *   `descriptionShort`: (String, optional) A brief description or excerpt.
            *   `budgetFormatted`: (String, optional) Formatted budget.
            *   `compensationModelText`: (String, optional) Text describing compensation.
            *   `imageUrl`: (String, optional) URL for a campaign image.
            *   `brandName`: (String, optional) Name of the brand.
            *   `targetAudienceSummary`: (String, optional) Brief summary of target audience.
    *   **State:** (Potentially none for a simple display card, or `isHovered` for hover effects if complex).
    *   **Methods:**
        *   `setup()`: Initialize any component-specific logic or computed properties.
            *   Use `formatDate` from `ui_helpers.js` for dates if not pre-formatted.
        *   `onViewDetailsClick()`: Emits an event `view-details` with `this.props.campaign.id`.
    *   **Template:** `InfluenceGen.Odoo.Shared.UI.Components.CampaignCard`
*   **QWeb Template (`CampaignCard.xml`):**
    *   **`t-name="InfluenceGen.Odoo.Shared.UI.Components.CampaignCard"`**
    *   **Structure:**
        *   Root `div` with class `o_campaign_card`.
        *   Optional image section (`t-if="props.campaign.imageUrl"`) with `img.o_campaign_card_image`.
        *   Content section:
            *   Title (`h3.o_campaign_card_title`): `props.campaign.name`.
            *   Status: Use `StatusBadge` component: `<StatusBadge statusText="props.campaign.status" statusType="props.campaign.statusType || 'default'"/>`.
            *   Dates (`div.o_campaign_card_dates`): Formatted start and end dates.
            *   Brand Name (`div.o_campaign_card_brand`): `t-if="props.campaign.brandName"`.
            *   Short Description (`p.o_campaign_card_description`): `t-if="props.campaign.descriptionShort"`.
            *   Budget/Compensation (`div.o_campaign_card_finance_info`): `t-if="props.campaign.budgetFormatted || props.campaign.compensationModelText"`.
            *   Target Audience (`div.o_campaign_card_audience`): `t-if="props.campaign.targetAudienceSummary"`.
            *   'View Details' button (`button.btn.btn-primary.o_campaign_card_details_btn`): Triggers `onViewDetailsClick`.
*   **SCSS (`campaign_card.scss`):**
    *   Styles for `.o_campaign_card` (e.g., `border`, `border-radius`, `box-shadow`, `padding`, `background-color`).
    *   Styles for internal elements like `.o_campaign_card_image`, `.o_campaign_card_title`, `.o_campaign_card_dates`, `.o_campaign_card_description`.
    *   Uses variables from `shared_variables.scss`.

### 6.2 MetricTile Component
*   **Purpose:** Displays a single key metric, often used in dashboards. (REQ-UIUX-019, REQ-UIUX-001)
*   **Files:**
    *   `static/src/components/metric_tile/MetricTile.js`
    *   `static/src/components/metric_tile/MetricTile.xml`
    *   `static/src/components/metric_tile/metric_tile.scss`
*   **JavaScript (`MetricTile.js`):**
    *   **Namespace:** `InfluenceGen.Odoo.Shared.UI.Components.MetricTile`
    *   **Class:** `MetricTile extends Component`
    *   **Props:**
        *   `label`: (String, required) The label for the metric.
        *   `value`: (String | Number, required) The value of the metric.
        *   `unit`: (String, optional) Unit for the value (e.g., '%', 'USD').
        *   `trend`: (String, optional) Trend indicator ('up', 'down', 'neutral').
        *   `trendValue`: (String | Number, optional) Value associated with the trend (e.g., "+5%").
        *   `iconClass`: (String, optional) CSS class for an icon to display (e.g., Font Awesome class).
        *   `infoText`: (String, optional) Additional contextual information or comparison text.
    *   **Methods:**
        *   `setup()`: Basic setup.
        *   `get trendIconClass()`: Computed property to return CSS class for trend arrow based on `props.trend`.
*   **QWeb Template (`MetricTile.xml`):**
    *   **`t-name="InfluenceGen.Odoo.Shared.UI.Components.MetricTile"`**
    *   **Structure:**
        *   Root `div` with class `o_metric_tile`.
        *   Optional icon (`i` tag with `t-att-class="props.iconClass"` if `props.iconClass`).
        *   Value display (`div.o_metric_tile_value`): `props.value`.
        *   Optional unit (`span.o_metric_tile_unit`): `t-if="props.unit"`, displays `props.unit`.
        *   Label (`div.o_metric_tile_label`): `props.label`.
        *   Optional trend indicator (`div.o_metric_tile_trend`):
            *   Icon (`i` tag with `t-att-class="trendIconClass"`) `t-if="props.trend"`.
            *   Trend value (`span.o_metric_tile_trend_value`): `t-if="props.trendValue"`, displays `props.trendValue`.
        *   Optional info text (`div.o_metric_tile_info`): `t-if="props.infoText"`.
*   **SCSS (`metric_tile.scss`):**
    *   Styles for `.o_metric_tile` (padding, background, border, alignment).
    *   Typography for `.o_metric_tile_label`, `.o_metric_tile_value`, `.o_metric_tile_unit`.
    *   Styling for trend indicators (colors for up/down, icon styling).
    *   Uses shared variables.

### 6.3 DataChartWrapper Component
*   **Purpose:** Provides a reusable wrapper for rendering charts using a library like Chart.js or Odoo's built-in charting capabilities (if suitable). (REQ-UIUX-019, REQ-UIUX-001)
*   **Files:**
    *   `static/src/components/data_chart_wrapper/DataChartWrapper.js`
    *   `static/src/components/data_chart_wrapper/DataChartWrapper.xml`
    *   `static/src/components/data_chart_wrapper/data_chart_wrapper.scss`
*   **JavaScript (`DataChartWrapper.js`):**
    *   **Namespace:** `InfluenceGen.Odoo.Shared.UI.Components.DataChartWrapper`
    *   **Class:** `DataChartWrapper extends Component`
    *   **Dependencies:** Requires a charting library (e.g., Chart.js) to be available in Odoo's assets if not using purely Odoo internal graph views. For this SDS, assume Chart.js integration.
    *   **Props:**
        *   `chartId`: (String, required) Unique ID for the chart canvas element.
        *   `chartType`: (String, required) Type of chart (e.g., 'bar', 'line', 'pie', 'doughnut').
        *   `chartData`: (Object, required) Data object compatible with the charting library (e.g., Chart.js `data` object).
        *   `chartOptions`: (Object, optional) Options object for the charting library (e.g., Chart.js `options` object).
    *   **State:**
        *   `chartInstance`: (Object) Holds the instance of the created chart.
    *   **Hooks:**
        *   `onMounted()`:
            *   Get the canvas element using `t-ref`.
            *   Initialize the chart instance (e.g., `new Chart(ctx, { type: props.chartType, data: props.chartData, options: props.chartOptions })`).
            *   Store the instance in `this.state.chartInstance`.
        *   `onWillUpdateProps(nextProps)`:
            *   If `chartData` or `chartOptions` have changed:
                *   Update the chart: `this.state.chartInstance.data = nextProps.chartData; this.state.chartInstance.options = nextProps.chartOptions || {}; this.state.chartInstance.update();`
        *   `onWillUnmount()`:
            *   Destroy the chart instance: `if (this.state.chartInstance) { this.state.chartInstance.destroy(); }` to prevent memory leaks.
    *   **Methods:**
        *   `setup()`: Initialize state `this.state = useState({ chartInstance: null });` and use `useRef` for the canvas.
*   **QWeb Template (`DataChartWrapper.xml`):**
    *   **`t-name="InfluenceGen.Odoo.Shared.UI.Components.DataChartWrapper"`**
    *   **Structure:**
        *   Root `div` with class `o_data_chart_wrapper`.
        *   `canvas` element with `t-att-id="props.chartId"` and `t-ref="'chartCanvas'"`.
*   **SCSS (`data_chart_wrapper.scss`):**
    *   Styles for `.o_data_chart_wrapper` to control container size, aspect ratio, and responsiveness.
    *   Specific chart element styling (axes, tooltips, legends) is generally handled through `chartOptions` prop fed to the charting library.

### 6.4 LoadingIndicator Component
*   **Purpose:** Displays a visual loading indicator (e.g., spinner). (REQ-UIUX-007, REQ-UIUX-001)
*   **Files:**
    *   `static/src/components/loading_indicator/LoadingIndicator.js`
    *   `static/src/components/loading_indicator/LoadingIndicator.xml`
    *   `static/src/components/loading_indicator/loading_indicator.scss`
*   **JavaScript (`LoadingIndicator.js`):**
    *   **Namespace:** `InfluenceGen.Odoo.Shared.UI.Components.LoadingIndicator`
    *   **Class:** `LoadingIndicator extends Component`
    *   **Props:**
        *   `size`: (String, optional, default: 'md') Size of the indicator ('sm', 'md', 'lg').
        *   `message`: (String, optional) Text message to display below the spinner.
        *   `isFullScreen`: (Boolean, optional, default: `false`) If true, the indicator covers the full parent relatively positioned element.
    *   **Methods:**
        *   `setup()`: Basic setup.
        *   `get indicatorClass()`: Computed property to return CSS classes based on `props.size` and `props.isFullScreen`.
*   **QWeb Template (`LoadingIndicator.xml`):**
    *   **`t-name="InfluenceGen.Odoo.Shared.UI.Components.LoadingIndicator"`**
    *   **Structure:**
        *   Root `div` with class `o_loading_indicator` and dynamic classes from `indicatorClass`.
        *   Spinner element (`div.o_loading_spinner`).
        *   Optional message (`div.o_loading_message`): `t-if="props.message"`, displays `props.message`.
*   **SCSS (`loading_indicator.scss`):**
    *   Styles for `.o_loading_indicator` (positioning for full screen).
    *   Styles for `.o_loading_spinner` (CSS animation for spinner).
        *   Include different sizes based on modifier classes (e.g., `.o_loading_indicator--sm`).
    *   Styles for `.o_loading_message`.
    *   Uses shared variables.

### 6.5 StatusBadge Component
*   **Purpose:** Displays a status with configurable text and type-based styling. (REQ-UIUX-001)
*   **Files:**
    *   `static/src/components/status_badge/StatusBadge.js`
    *   `static/src/components/status_badge/StatusBadge.xml`
    *   `static/src/components/status_badge/status_badge.scss`
*   **JavaScript (`StatusBadge.js`):**
    *   **Namespace:** `InfluenceGen.Odoo.Shared.UI.Components.StatusBadge`
    *   **Class:** `StatusBadge extends Component`
    *   **Props:**
        *   `statusText`: (String, required) The text to display in the badge.
        *   `statusType`: (String, optional, default: 'default') Type of status, influencing color ('info', 'success', 'warning', 'danger', 'neutral', 'primary', 'secondary', 'default').
        *   `isPill`: (Boolean, optional, default: `false`) If true, renders as a pill-shaped badge.
    *   **Methods:**
        *   `setup()`: Basic setup.
        *   `get badgeClass()`: Computed property returning CSS classes: `'o_status_badge'`, `o_status_badge--${this.props.statusType.toLowerCase()}`, and `'o_status_badge--pill'` if `props.isPill` is true.
*   **QWeb Template (`StatusBadge.xml`):**
    *   **`t-name="InfluenceGen.Odoo.Shared.UI.Components.StatusBadge"`**
    *   **Structure:**
        *   `span` element with `t-att-class="badgeClass"` and displays `props.statusText`.
*   **SCSS (`status_badge.scss`):**
    *   Base styles for `.o_status_badge` (padding, font-size, border-radius).
    *   Modifier classes for different types (e.g., `.o_status_badge--success`, `.o_status_badge--warning`) setting `background-color` and `color` using shared color variables.
    *   Style for `.o_status_badge--pill` to make it pill-shaped (`border-radius: 50rem;`).

### 6.6 ProfileSnippet Component
*   **Purpose:** Displays a compact summary of an influencer's profile. (REQ-UIUX-001)
*   **Files:**
    *   `static/src/components/profile_snippet/ProfileSnippet.js`
    *   `static/src/components/profile_snippet/ProfileSnippet.xml`
    *   `static/src/components/profile_snippet/profile_snippet.scss`
*   **JavaScript (`ProfileSnippet.js`):**
    *   **Namespace:** `InfluenceGen.Odoo.Shared.UI.Components.ProfileSnippet`
    *   **Class:** `ProfileSnippet extends Component`
    *   **Props:**
        *   `influencer`: (Object, required) Containing influencer details:
            *   `name`: (String) Full name.
            *   `avatarUrl`: (String, optional) URL for the avatar image.
            *   `mainNiche`: (String, optional) Primary area of influence.
            *   `profileUrl`: (String, optional) URL to the full influencer profile.
    *   **Methods:**
        *   `setup()`: Basic setup.
        *   `get initials()`: Computed property to generate initials from `props.influencer.name` if `avatarUrl` is not provided, using `getInitials` helper.
*   **QWeb Template (`ProfileSnippet.xml`):**
    *   **`t-name="InfluenceGen.Odoo.Shared.UI.Components.ProfileSnippet"`**
    *   **Structure:**
        *   Root `div` (or `a` if `props.influencer.profileUrl` exists) with class `o_profile_snippet`.
        *   Avatar section (`div.o_profile_snippet_avatar`):
            *   `img` tag: `t-if="props.influencer.avatarUrl"` `t-att-src="props.influencer.avatarUrl"`.
            *   Fallback to initials: `div.o_profile_snippet_initials` `t-if="!props.influencer.avatarUrl"`, displays `initials`.
        *   Info section (`div.o_profile_snippet_info`):
            *   Name (`div.o_profile_snippet_name`): `props.influencer.name`.
            *   Niche (`div.o_profile_snippet_niche`): `t-if="props.influencer.mainNiche"`, displays `props.influencer.mainNiche`.
*   **SCSS (`profile_snippet.scss`):**
    *   Styles for `.o_profile_snippet` (flex layout, alignment).
    *   Styles for `.o_profile_snippet_avatar` and `.o_profile_snippet_initials` (size, border-radius, background for initials).
    *   Typography for `.o_profile_snippet_name` and `.o_profile_snippet_niche`.

## 7. Testing Strategy

*   **Unit Tests:** Each OWL component should have unit tests verifying its props handling, state changes, event emissions, and correct rendering of its QWeb template based on different prop combinations. Odoo's QUnit test runner for JS tests will be used.
*   **Visual Regression Tests:** If tooling permits, visual regression tests can help catch unintended UI changes.
*   **Manual Testing:** Components will be manually tested in different contexts (portal, backend) to ensure they integrate and function as expected.

## 8. Documentation Strategy

*   **Component Documentation:** Each component's `.js` file will include JSDoc-style comments for the class, props, methods, and events.
*   **Usage Examples:** Where appropriate, example usage snippets will be provided in comments or a separate developer guide if the library grows complex.
*   **SCSS Variables/Mixins:** Comments in `shared_variables.scss` and `shared_mixins.scss` will explain their purpose and usage.
*   **JS Utilities:** JSDoc comments for functions in `ui_helpers.js`.

This SDS provides a foundation for building a robust and consistent set of shared UI components for the InfluenceGen platform within Odoo 18. Developers should refer to Odoo's official documentation for OWL, QWeb, and asset management best practices.