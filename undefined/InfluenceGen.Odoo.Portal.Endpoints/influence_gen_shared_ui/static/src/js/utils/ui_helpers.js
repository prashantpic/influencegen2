/** @odoo-module **/

/**
 * InfluenceGen.Odoo.Shared.UI.Utils
 *
 * This module provides common JavaScript utility functions for UI components
 * across the InfluenceGen platform. These helpers aim to standardize common
 * tasks like data formatting, event handling, and text manipulation.
 */

/**
 * Formats a number as currency.
 *
 * @param {number} amount - The number to format.
 * @param {string} currencyCode - The ISO 4217 currency code (e.g., 'USD', 'EUR').
 * @param {string} [locale='en-US'] - The locale string (e.g., 'en-US', 'de-DE').
 * @returns {string} The formatted currency string. Returns an empty string if amount is not a number.
 * @example
 * formatCurrency(1234.56, 'USD'); // "$1,234.56"
 * formatCurrency(500, 'EUR', 'de-DE'); // "500,00 €"
 */
export const formatCurrency = (amount, currencyCode, locale = 'en-US') => {
    if (typeof amount !== 'number' || isNaN(amount)) {
        console.warn('formatCurrency: Invalid amount provided.', amount);
        return '';
    }
    if (typeof currencyCode !== 'string' || currencyCode.length !== 3) {
        console.warn('formatCurrency: Invalid currencyCode provided.', currencyCode);
        // Fallback or throw error? For now, proceed but it might format incorrectly.
    }
    try {
        return new Intl.NumberFormat(locale, {
            style: 'currency',
            currency: currencyCode,
        }).format(amount);
    } catch (error) {
        console.error('Error formatting currency:', error);
        return `${amount} ${currencyCode}`; // Fallback basic format
    }
};

/**
 * Formats a date string or Date object into a more readable format.
 *
 * @param {string|Date} dateStringOrObject - The date string (parsable by `new Date()`) or a Date object.
 * @param {object} [options={ year: 'numeric', month: 'short', day: 'numeric' }] - Intl.DateTimeFormat options.
 * @param {string} [locale='en-US'] - The locale string.
 * @returns {string} The formatted date string. Returns an empty string if date is invalid.
 * @example
 * formatDate('2023-12-25'); // "Dec 25, 2023"
 * formatDate(new Date(), { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
 */
export const formatDate = (dateStringOrObject, options = { year: 'numeric', month: 'short', day: 'numeric' }, locale = 'en-US') => {
    if (!dateStringOrObject) {
        // console.warn('formatDate: No date provided.');
        return '';
    }
    try {
        const date = (dateStringOrObject instanceof Date) ? dateStringOrObject : new Date(dateStringOrObject);
        if (isNaN(date.getTime())) {
            // console.warn('formatDate: Invalid date provided.', dateStringOrObject);
            return '';
        }
        return new Intl.DateTimeFormat(locale, options).format(date);
    } catch (error) {
        console.error('Error formatting date:', error);
        return String(dateStringOrObject); // Fallback to original string
    }
};

/**
 * Returns a debounced version of the passed function.
 * The debounced function will only be executed after it has not been called for `delay` milliseconds.
 *
 * @param {Function} func - The function to debounce.
 * @param {number} delay - The delay in milliseconds.
 * @returns {Function} The debounced function.
 * @example
 * const debouncedSave = debounce(saveInput, 500);
 * inputElement.addEventListener('keyup', debouncedSave);
 */
export const debounce = (func, delay) => {
    let timeoutId;
    return function(...args) {
        const context = this;
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(context, args);
        }, delay);
    };
};

/**
 * Truncates text to a maximum length and appends an ellipsis.
 *
 * @param {string} text - The text to truncate.
 * @param {number} maxLength - The maximum length of the text (excluding ellipsis).
 * @param {string} [ellipsis='...'] - The ellipsis string to append.
 * @returns {string} The truncated text, or the original text if it's shorter than maxLength.
 * @example
 * truncateText("This is a long piece of text.", 10); // "This is a..."
 * truncateText("Short text", 20); // "Short text"
 */
export const truncateText = (text, maxLength, ellipsis = '...') => {
    if (typeof text !== 'string') {
        // console.warn('truncateText: Input text must be a string.');
        return '';
    }
    if (text.length <= maxLength) {
        return text;
    }
    return text.substring(0, maxLength) + ellipsis;
};

/**
 * Generates initials from a name string.
 *
 * @param {string} name - The full name string.
 * @param {number} [count=2] - The number of initials to generate.
 * @returns {string} The generated initials in uppercase. Returns empty string if name is empty or invalid.
 * @example
 * getInitials("John Doe"); // "JD"
 * getInitials("Jane Mary Smith", 3); // "JMS"
 * getInitials("Single", 2); // "S"
 */
export const getInitials = (name, count = 2) => {
    if (typeof name !== 'string' || !name.trim()) {
        return '';
    }
    const words = name.trim().split(/\s+/);
    return words
        .slice(0, count)
        .map(word => word[0] ? word[0].toUpperCase() : '')
        .join('');
};

/**
 * Converts a string to a slug (lowercase, dashes for spaces, remove special characters).
 *
 * @param {string} text - The string to slugify.
 * @returns {string} The slugified string.
 * @example
 * slugify("My Awesome Title!"); // "my-awesome-title"
 * slugify("  Another Example with Spaces  "); // "another-example-with-spaces"
 */
export const slugify = (text) => {
    if (typeof text !== 'string') {
        return '';
    }
    return text
        .toString()
        .normalize('NFKD') // Normalize accented characters
        .toLowerCase()
        .trim()
        .replace(/\s+/g, '-') // Replace spaces with -
        .replace(/[^\w-]+/g, '') // Remove all non-word chars
        .replace(/--+/g, '-'); // Replace multiple - with single -
};

// Example of a more complex utility if needed, e.g., for parsing query params
/**
 * Parses URL query parameters into an object.
 *
 * @param {string} [queryString=window.location.search] - The query string to parse.
 * @returns {object} An object representation of the query parameters.
 * @example
 * // Assuming URL is ?name=John&age=30
 * getQueryParams(); // { name: "John", age: "30" }
 * getQueryParams("?foo=bar&baz=qux"); // { foo: "bar", baz: "qux" }
 */
export const getQueryParams = (queryString = window.location.search) => {
    const params = {};
    const searchParams = new URLSearchParams(queryString);
    for (const [key, value] of searchParams) {
        params[key] = value;
    }
    return params;
};

/**
 * A simple utility to create a DOM element with attributes and children.
 * Not a replacement for OWL/QWeb, but can be useful for very simple, dynamic JS-only DOM manipulations
 * if ever needed outside components (though generally discouraged).
 *
 * @param {string} tagName - The HTML tag name.
 * @param {object} [attributes={}] - An object of attributes to set on the element.
 * @param {Array<Node|string>} [children=[]] - An array of child nodes or strings to append.
 * @returns {HTMLElement} The created HTML element.
 */
export const createElement = (tagName, attributes = {}, children = []) => {
    const element = document.createElement(tagName);
    for (const key in attributes) {
        element.setAttribute(key, attributes[key]);
    }
    children.forEach(child => {
        if (typeof child === 'string') {
            element.appendChild(document.createTextNode(child));
        } else if (child instanceof Node) {
            element.appendChild(child);
        }
    });
    return element;
};

// Add other general-purpose UI helper functions as they become necessary.
// For example:
// - scrollIntoView(element)
// - copyToClipboard(text)
// - etc.