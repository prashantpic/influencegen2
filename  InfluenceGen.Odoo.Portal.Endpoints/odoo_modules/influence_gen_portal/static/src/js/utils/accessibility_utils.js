/** @odoo-module */

import { _t } from "@web/core/l10n/translation";

/**
 * Utility functions for common accessibility tasks.
 */
export const accessibilityUtils = {

    /**
     * Safely attempts to set keyboard focus to a specific element.
     * Useful for managing focus after dynamic content changes or opening modals.
     * @param {string|HTMLElement} element - CSS selector string or the actual HTMLElement.
     */
    manageFocus: function(element) {
        let el;
        if (typeof element === 'string') {
            el = document.querySelector(element);
        } else if (element instanceof HTMLElement) {
            el = element;
        }

        if (el && typeof el.focus === 'function') {
            try {
                 // Use requestAnimationFrame to ensure the element is visible and rendered
                 requestAnimationFrame(() => {
                     el.focus({ preventScroll: true }); // preventScroll is a good option
                     // Optional: add an outline or highlight for a moment for visual confirmation
                     // el.style.outline = '2px solid blue'; setTimeout(() => el.style.outline = '', 500);
                 });
            } catch (e) {
                console.error("Failed to set focus:", e);
            }
        } else {
            console.warn("manageFocus: Element not found or not focusable.", element);
        }
    },

    /**
     * Announces a message to screen readers using an ARIA live region.
     * Create a live region element in your layout if one doesn't exist.
     * Example HTML: <div id="live-region" aria-live="polite" class="visually-hidden"></div>
     * @param {string} message - The message to announce.
     * @param {'polite'|'assertive'} [priority='polite'] - The urgency of the message. 'polite' waits for user inactivity, 'assertive' interrupts immediately.
     */
    announceToScreenReader: function(message, priority = 'polite') {
        let liveRegion = document.getElementById('o_live_region'); // Standard Odoo ID for live region
        if (!liveRegion) {
            // Create a visually hidden live region if it doesn't exist
            liveRegion = document.createElement('div');
            liveRegion.setAttribute('id', 'o_live_region');
            liveRegion.classList.add('visually-hidden'); // Use Odoo's/Bootstrap's hidden class
            liveRegion.setAttribute('role', 'status'); // More specific role
            document.body.appendChild(liveRegion);
        }
         liveRegion.setAttribute('aria-live', priority);
        // Using innerHTML to ensure screen readers pick up changes consistently
        liveRegion.innerHTML = ''; // Clear previous message
        const messageNode = document.createTextNode(message);
        liveRegion.appendChild(messageNode);

         // Optionally clear after a longer delay, but typically screen readers handle this.
         // setTimeout(() => {
         //      if (liveRegion.contains(messageNode)) {
         //          liveRegion.removeChild(messageNode);
         //      }
         // }, 5000); // Adjust delay as needed, or remove clearing logic
    },

     /**
      * Placeholder for color contrast check (usually done in design/CSS, but can be useful programmatically)
      * This is complex and typically relies on browser APIs or dedicated libraries.
      * Not implemented here, but serves as a note.
      * @param {string} fgColor - Foreground color (e.g., #RRGGBB or rgba()).
      * @param {string} bgColor - Background color.
      * @returns {number} - Contrast ratio.
      */
     checkColorContrast: function(fgColor, bgColor) {
         console.warn("checkColorContrast utility is a placeholder. Contrast should be checked during design and QA using browser developer tools or specialized accessibility checkers.");
         // Implementation would involve converting colors to RGB, calculating luminance, and then contrast ratio.
         return 0; // Placeholder
     },

     // Add other utilities like managing ARIA attributes for dynamic elements if needed.
};

// Register as an Odoo JS module if needed
// odoo.define('influence_gen_portal.utils.accessibility', function (require) {
//     'use strict';
//     return accessibilityUtils;
// });