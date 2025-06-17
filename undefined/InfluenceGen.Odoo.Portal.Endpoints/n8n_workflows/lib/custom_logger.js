/**
 * lib/custom_logger.js
 * Helper JavaScript module for custom, structured logging within N8N Function nodes.
 */

// Define log level priorities
const LOG_LEVELS = {
    'DEBUG': 10,
    'INFO': 20,
    'WARN': 30,
    'ERROR': 40,
    'CRITICAL': 50,
};
const DEFAULT_LOG_LEVEL = 'INFO';

/**
 * Retrieves the correlation ID for logging purposes.
 * It prioritizes an explicitly passed `requestId` in contextData,
 * then tries to get `request_id` from the initial webhook node's output,
 * and finally falls back to N8N's execution ID.
 * @param {object} [contextData={}] - Contextual data, may contain `requestId`.
 * @param {object} [n8nGlobals={}] - Object containing N8N globals like $execution, $, $node, $workflow.
 * @returns {string} The correlation ID.
 */
function getCorrelationId(contextData = {}, n8nGlobals = {}) {
    let correlationId = 'N/A'; // Default

    // 1. Explicitly passed requestId in contextData
    if (contextData && contextData.requestId) {
        return contextData.requestId;
    }
    
    // 2. Try to get request_id from initial webhook node if $ is available
    if (n8nGlobals.$ && typeof n8nGlobals.$ === 'function') {
        try {
            // Attempt to access data from the 'receiveOdooRequest' node.
            // This relies on the node name being fixed and accessible.
            const webhookNodeOutput = n8nGlobals.$('receiveOdooRequest').item.json;
            if (webhookNodeOutput && webhookNodeOutput.request_id) {
                correlationId = webhookNodeOutput.request_id;
                // Store it in workflow variables for easier access in error handlers if possible
                // if (n8nGlobals.$vars && typeof n8nGlobals.$vars.set === 'function' && !n8nGlobals.$vars.initialOdooRequestId) {
                // n8nGlobals.$vars.set('initialOdooRequestId', correlationId);
                // }
                return correlationId;
            }
        } catch (e) {
            // console.warn(`[Logger] Could not retrieve request_id from 'receiveOdooRequest' node: ${e.message}`);
        }
    }

    // 3. Fallback to N8N execution ID if available
    if (n8nGlobals.$execution && n8nGlobals.$execution.id) {
        correlationId = n8nGlobals.$execution.id;
        return correlationId;
    }
    
    // 4. If $vars.initialOdooRequestId was set previously
    // if (n8nGlobals.$vars && n8nGlobals.$vars.initialOdooRequestId) {
    // return n8nGlobals.$vars.initialOdooRequestId;
    // }


    return correlationId; // Returns 'N/A' if no ID could be determined
}


/**
 * Logs a structured event to the console (which N8N captures).
 * @param {string} level - Log level (e.g., 'INFO', 'ERROR', 'DEBUG', 'WARN', 'CRITICAL').
 * @param {string} message - The log message.
 * @param {object} [contextData={}] - Additional contextual data (e.g., `requestId`, `payload`, `stepName`).
 *                                  N8N globals ($execution, $, $node, $workflow) should be passed in contextData.n8nGlobals if needed by getCorrelationId.
 */
function logEvent(level, message, contextData = {}) {
    const n8nGlobals = contextData.n8nGlobals || {
        $workflow: typeof $workflow !== 'undefined' ? $workflow : undefined,
        $execution: typeof $execution !== 'undefined' ? $execution : undefined,
        $node: typeof $node !== 'undefined' ? $node : undefined,
        $: typeof $ !== 'undefined' ? $ : undefined,
        // $vars: typeof $vars !== 'undefined' ? $vars : undefined, // If using $vars for correlationId
    };
    delete contextData.n8nGlobals; // Remove from final log object if it was passed

    const configuredLogLevelName = (process.env.LOG_LEVEL || DEFAULT_LOG_LEVEL).toUpperCase();
    const minimumLogLevelPriority = LOG_LEVELS[configuredLogLevelName] || LOG_LEVELS[DEFAULT_LOG_LEVEL];
    const currentEventLogLevelPriority = LOG_LEVELS[level.toUpperCase()] || 0; // Log unknown levels by default if not filtered

    if (currentEventLogLevelPriority < minimumLogLevelPriority) {
        return; // Skip logging if below configured level
    }

    const logObject = {
        timestamp: new Date().toISOString(),
        level: level.toUpperCase(),
        message: message,
        correlationId: getCorrelationId(contextData, n8nGlobals),
        workflowName: n8nGlobals.$workflow ? n8nGlobals.$workflow.name : 'N/A',
        executionId: n8nGlobals.$execution ? n8nGlobals.$execution.id : 'N/A',
        nodeName: n8nGlobals.$node ? n8nGlobals.$node.name : 'N/A',
        ...contextData // Spread additional context provided by the caller
    };

    // Clean up potentially large or sensitive items from contextData if they were not meant for logging
    // For example, if 'payload' is too big or contains sensitive info.
    // This should be handled by the caller by not putting such data in contextData.

    console.log(JSON.stringify(logObject));
}

// Example usage within a Function Node:
// logEvent('INFO', 'Processing started.', { 
//     someKey: 'someValue', 
//     payloadSummary: { field1: items[0].json.field1 },
//     n8nGlobals: { $workflow, $execution, $node, $ } // Pass N8N globals
// });
// logEvent('ERROR', 'An error occurred.', { 
//     errorDetails: err.message, 
//     stack: err.stack,
//     n8nGlobals: { $workflow, $execution, $node, $ }
// });

// Note: When embedding this script in N8N Function nodes,
// ensure `LOG_LEVELS` and `DEFAULT_LOG_LEVEL` constants are also included,
// or that `logEvent` is self-contained or relies on `process.env.LOG_LEVEL` check directly.
// The provided functions `getCorrelationId` and `logEvent` are designed to be used together.