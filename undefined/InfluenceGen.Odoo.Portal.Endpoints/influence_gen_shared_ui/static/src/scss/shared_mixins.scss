// Shared SCSS Mixins for InfluenceGen UI Components
// Purpose: Provides reusable SCSS mixins for common styling patterns.
// All InfluenceGen specific mixins should start with 'ig-' prefix.

// Import shared variables to use them within mixins
@import 'shared_variables';

// -----------------------------------------------------------------------------
// Flexbox Utilities
// -----------------------------------------------------------------------------

/**
 * Applies flex properties for centering content both horizontally and vertically.
 * @param {string} $direction - Flex direction (default: row).
 */
@mixin ig-flex-center($direction: row) {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: $direction;
}

/**
 * Applies flex properties for aligning items to the start.
 * @param {string} $direction - Flex direction (default: row).
 */
@mixin ig-flex-start($direction: row) {
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  flex-direction: $direction;
}

/**
 * Applies flex properties for space-between distribution.
 * @param {string} $direction - Flex direction (default: row).
 */
@mixin ig-flex-space-between($direction: row) {
  display: flex;
  align-items: center; // Common default, can be overridden
  justify-content: space-between;
  flex-direction: $direction;
}

// -----------------------------------------------------------------------------
// Responsive Design Utilities
// -----------------------------------------------------------------------------

/**
 * Media query helper for min-width (breakpoint up).
 * @param {string} $name - Breakpoint name (e.g., 'sm', 'md', 'lg').
 *                         Must be a key in $ig-grid-breakpoints map.
 */
@mixin ig-media-breakpoint-up($name) {
  $min: map-get($ig-grid-breakpoints, $name);
  @if $min {
    @media (min-width: $min) {
      @content;
    }
  } @else {
    @warn "Breakpoint `#{$name}` not found in $ig-grid-breakpoints.";
  }
}

/**
 * Media query helper for max-width (breakpoint down).
 * @param {string} $name - Breakpoint name (e.g., 'sm', 'md', 'lg').
 *                         Must be a key in $ig-grid-breakpoints map.
 */
@mixin ig-media-breakpoint-down($name) {
  $max: map-get($ig-grid-breakpoints, $name);
  @if $max and $max > 0 { // max must be > 0 for a meaningful max-width
    @media (max-width: $max - 0.02px) { // Subtract a tiny value to avoid overlap with min-width
      @content;
    }
  } @else if $max == 0 {
    // No down for xs (0)
  }
  @else {
    @warn "Breakpoint `#{$name}` not found in $ig-grid-breakpoints.";
  }
}

/**
 * Media query helper for a specific breakpoint range.
 * @param {string} $lowerName - Lower breakpoint name.
 * @param {string} $upperName - Upper breakpoint name.
 */
@mixin ig-media-breakpoint-between($lowerName, $upperName) {
  $lower: map-get($ig-grid-breakpoints, $lowerName);
  $upper: map-get($ig-grid-breakpoints, $upperName);

  @if $lower and $upper and $upper > $lower {
    @media (min-width: $lower) and (max-width: $upper - 0.02px) {
      @content;
    }
  } @else {
    @warn "Invalid breakpoint range: `#{$lowerName}` to `#{$upperName}`.";
  }
}

// -----------------------------------------------------------------------------
// UI Element Styling
// -----------------------------------------------------------------------------

/**
 * Generates button styles.
 * @param {color} $background - Background color of the button.
 * @param {color} $color - Text color of the button.
 * @param {color} $border - Border color of the button (optional, defaults to $background).
 * @param {color} $hover-background - Background color on hover (optional, defaults to darker $background).
 * @param {color} $hover-color - Text color on hover (optional, defaults to $color).
 * @param {color} $hover-border - Border color on hover (optional, defaults to darker $border).
 */
@mixin ig-button-variant(
  $background,
  $color,
  $border: $background,
  $hover-background: darken($background, 10%),
  $hover-color: $color,
  $hover-border: darken($border, 12%)
) {
  color: $color;
  background-color: $background;
  border-color: $border;

  &:hover {
    color: $hover-color;
    background-color: $hover-background;
    border-color: $hover-border;
  }

  &:focus, &.focus {
    // Add focus styles, e.g., box-shadow
    box-shadow: 0 0 0 0.2rem rgba($background, .5);
  }

  &:disabled, &.disabled {
    color: $color;
    background-color: $background;
    border-color: $border;
    opacity: 0.65; // Standard disabled opacity
  }

  &:not(:disabled):not(.disabled):active,
  &:not(:disabled):not(.disabled).active,
  .show > &.dropdown-toggle {
    color: $hover-color; // Or a specific active color
    background-color: darken($background, 12%);
    border-color: darken($border, 15%);
  }
}

/**
 * Applies styles for text truncation with ellipsis.
 * Ensure the element is a block or inline-block element with a defined width.
 */
@mixin ig-truncate-text() {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// -----------------------------------------------------------------------------
// Clearfix
// -----------------------------------------------------------------------------
// Standard clearfix to contain floats.
@mixin ig-clearfix() {
  &::after {
    display: block;
    content: "";
    clear: both;
  }
}

// -----------------------------------------------------------------------------
// Sizing
// -----------------------------------------------------------------------------
// Creates a square element.
@mixin ig-square($size) {
  width: $size;
  height: $size;
}

// -----------------------------------------------------------------------------
// Appearance
// -----------------------------------------------------------------------------
// Resets appearance for form elements.
@mixin ig-appearance($value: none) {
  -webkit-appearance: $value;
  -moz-appearance: $value;
  appearance: $value;
}

// Add more mixins as needed for specific UI requirements (e.g., form styling, alerts, cards).