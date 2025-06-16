odoo.define('influence_gen_portal.utils.accessibility', function (require) {
'use strict';

/**
 * Manages focus by attempting to set focus to the specified element.
 * @param {string} elementSelector - CSS selector for the target element.
 */
function manageFocus(elementSelector) {
    try {
        const el = document.querySelector(elementSelector);
        if (el && typeof el.focus === 'function') {
            el.focus();
        }
    } catch (e) {
        console.error(`Error trying to focus on element with selector: ${elementSelector}`, e);
    }
}

/**
 * Announces a message to screen readers using an ARIA live region.
 * Creates or reuses a live region element.
 * @param {string} message - The message to be announced.
 * @param {string} [politeness='assertive'] - The politeness level ('assertive' or 'polite').
 */
function announceToScreenReader(message, politeness = 'assertive') {
    let liveRegion = document.getElementById('ig-sr-live-region');
    if (!liveRegion) {
        liveRegion = document.createElement('div');
        liveRegion.id = 'ig-sr-live-region';
        liveRegion.className = 'sr-only'; // Visually hidden
        liveRegion.setAttribute('aria-live', politeness);
        liveRegion.setAttribute('aria-atomic', 'true');
        document.body.appendChild(liveRegion);
    }

    // Set politeness level before changing content
    liveRegion.setAttribute('aria-live', politeness);

    // Clear previous message before setting new one to ensure it's announced
    liveRegion.textContent = '';
    // Use a timeout to ensure the clear is processed before the new message
    setTimeout(() => {
        liveRegion.textContent = message;
    }, 100); // Small delay might be needed for some screen readers
}

/**
 * Calculates the contrast ratio between two colors.
 * Useful for development to check if color combinations meet WCAG AA/AAA.
 * Not typically used at runtime for dynamic content adjustment in this context.
 * @param {string} fgColor - Foreground color (e.g., '#RRGGBB' or 'rgb(r,g,b)').
 * @param {string} bgColor - Background color (e.g., '#RRGGBB' or 'rgb(r,g,b)').
 * @returns {number} The contrast ratio.
 */
function checkColorContrast(fgColor, bgColor) {
    // Helper to parse color string to RGB array
    function parseColor(colorStr) {
        if (colorStr.startsWith('#')) {
            const hex = colorStr.substring(1);
            const r = parseInt(hex.length === 3 ? hex[0] + hex[0] : hex.substring(0, 2), 16);
            const g = parseInt(hex.length === 3 ? hex[1] + hex[1] : hex.substring(2, 4), 16);
            const b = parseInt(hex.length === 3 ? hex[2] + hex[2] : hex.substring(4, 6), 16);
            return [r, g, b];
        } else if (colorStr.startsWith('rgb')) {
            const match = colorStr.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/);
            if (match) {
                return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
            }
        }
        console.warn('Invalid color format for contrast check:', colorStr);
        return [0, 0, 0]; // Default to black on error
    }

    // Helper to calculate luminance
    function getLuminance(rgb) {
        const [r, g, b] = rgb.map(val => {
            const srgb = val / 255;
            return (srgb <= 0.03928) ? srgb / 12.92 : Math.pow((srgb + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }

    const fgLuminance = getLuminance(parseColor(fgColor));
    const bgLuminance = getLuminance(parseColor(bgColor));

    const ratio = (Math.max(fgLuminance, bgLuminance) + 0.05) / (Math.min(fgLuminance, bgLuminance) + 0.05);
    return parseFloat(ratio.toFixed(2));
}


return {
    manageFocus: manageFocus,
    announceToScreenReader: announceToScreenReader,
    checkColorContrast: checkColorContrast,
};

});