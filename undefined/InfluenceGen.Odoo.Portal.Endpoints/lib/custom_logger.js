```javascript
/**
 * lib/custom_logger.js
 * Helper JavaScript module for custom, structured logging within N8N Function nodes.
 * Assumes this code is "prepended" to N8N Function nodes, making the
 * logEvent and getCorrelationId functions globally available.
 */

// This function needs to be available globally in the Function node scope.
function getCorrelationId(contextData) {
    let correlationId = 'N/A_CORRELATION_ID';

    // 1. Try from explicit contextData (if caller includes 'requestId')
    if (contextData && contextData.requestId) {
        return contextData.requestId;
    }
    
    // 2. Try from n8nExecutionData (if contextData is the $execution object)
    if (contextData && contextData.id && typeof $execution !== 'undefined' && contextData.id === $execution.id) {
         // This means contextData itself might be $execution, so use $execution.id
         // but we prefer a business requestId.
    }

    // 3. Try to access from the initial webhook node's output if this is a subsequent node.
    // This relies on N8N's context allowing access to other nodes' data ($('nodeName').item.json).
    // This is a common pattern but can be fragile if node names change.
    try {
        if (typeof $ !== 'undefined' && $('receiveOdooRequest') && $('receiveOdooRequest').item && $('receiveOdooRequest').item.json && $('receiveOdooRequest').item.json.request_id) {
            correlationId = $('receiveOdooRequest').item.json.request_id;
            return correlationId;
        }
    } catch (e) {
        // console.warn('[Custom Logger] Could not get request_id from receiveOdooRequest node:', e.message);
    }
    
    // 4. Try from $vars if set (less common for correlation ID unless explicitly managed)
    try {
        if (typeof $vars !== 'undefined' && $vars.initialOdooRequestId) {
            correlationId = $vars.initialOdooRequestId;
            return correlationId;
        }
    } catch(e) { /* ignore */ }


    // 5. Fallback to N8N's execution ID if available
    try {
        if (typeof $execution !== 'undefined' && $execution.id) {
            correlationId = `EXEC_${$execution.id}`; // Prefix to distinguish from business request_id
            return correlationId;
        }
    } catch (e) {
        // console.warn('[Custom Logger] Could not get N8N execution ID:', e.message);
    }
    
    return correlationId; // Returns 'N/A_CORRELATION_ID' if all attempts fail
}


// This function needs to be available globally in the Function node scope.
function logEvent(level, message, contextData = {}) {
    const logLevelOrder = {
        'DEBUG': 10,
        'INFO': 20,
        'WARN': 30,
        'ERROR': 40,
        'CRITICAL': 50
    };

    const configuredLogLevelEnv = (typeof process !== 'undefined' && process.env) ? process.env.LOG_LEVEL : 'INFO';
    const configuredLogLevel = configuredLogLevelEnv ? configuredLogLevelEnv.toUpperCase() : 'INFO';
    const minimumLogLevel = logLevelOrder[configuredLogLevel] || logLevelOrder['INFO'];
    const currentLogLevelValue = logLevelOrder[level.toUpperCase()] || logLevelOrder['INFO']; // Default to INFO if level is unknown

    if (currentLogLevelValue < minimumLogLevel) {
        return; // Skip logging if current level is below configured minimum
    }

    let correlationId;
    // If requestId is directly in contextData, use it. Otherwise, try getCorrelationId.
    if (contextData && contextData.requestId) {
        correlationId = contextData.requestId;
    } else {
        // Pass contextData to getCorrelationId in case it needs to look for requestId within it,
        // or pass $execution if available.
        let correlationContext = contextData;
        if (typeof $execution !== 'undefined') {
            correlationContext = $execution; // Prefer $execution as context for getCorrelationId if requestId not in contextData
        }
        correlationId = getCorrelationId(correlationContext);
    }
    
    const workflowInfo = {
        name: 'N/A_WF_NAME',
        id: 'N/A_WF_ID'
    };
    if (typeof $workflow !== 'undefined') {
        workflowInfo.name = $workflow.name;
        workflowInfo.id = $workflow.id;
    }
    
    const executionInfo = {
        id: 'N/A_EXEC_ID',
        mode: 'N/A_EXEC_MODE'
    };
    if (typeof $execution !== 'undefined') {
        executionInfo.id = $execution.id;
        executionInfo.mode = $execution.mode;
    }
    
    const nodeInfo = {
        name: 'N/A_NODE_NAME',
        type: 'N/A_NODE_TYPE'
    };
    if (typeof $node !== 'undefined') {
        nodeInfo.name = $node.name;
        nodeInfo.type = $node.type;
    }
    
    const logObject = {
        timestamp: new Date().toISOString(),
        level: level.toUpperCase(),
        message: message,
        correlationId: correlationId,
        workflow: workflowInfo,
        execution: executionInfo,
        node: nodeInfo,
        ...contextData // Spread additional context provided by the caller
    };

    // Remove potentially large or sensitive default N8N context objects if they were spread
    // For example, if contextData included the full 'items' array.
    // The caller should provide specific, sanitized context.
    // This is just a safeguard; ideally contextData is already curated.
    delete logObject.items; 
    delete logObject.json;
    delete logObject.binary;


    // Output JSON string to console, which N8N captures
    // In N8N, console.log, console.warn, console.error are typically routed to execution logs.
    const logString = JSON.stringify(logObject);
    switch (level.toUpperCase()) {
        case 'DEBUG':
        case 'INFO':
            console.log(logString);
            break;
        case 'WARN':
            console.warn(logString);
            break;
        case 'ERROR':
        case 'CRITICAL':
            console.error(logString);
            break;
        default:
            console.log(logString);
            break;
    }
}
```