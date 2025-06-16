/**
 * @namespace InfluenceGen.N8N.Utils.Logging
 * Provides standardized JavaScript helper functions for structured logging within N8N Function nodes.
 */
const InfluenceGenN8NUtilsLogging = {
  /**
   * Formats a log entry into a structured JSON object.
   * @param {string} level - Log level (e.g., "INFO", "ERROR", "DEBUG").
   * @param {string} message - The main log message.
   * @param {object} context - An object containing additional contextual information.
   *   Expected to include:
   *   - workflowInstance (object): N8N execution data (e.g., $execution).
   *   - nodeName (string): The name of the N8N node.
   *   - correlationId (string): The correlation ID for distributed tracing.
   *   - data (object, optional): Custom data payload for the log entry.
   *   - payload (object, optional): Alternative to 'data' for custom data.
   * @returns {object} - A structured log entry.
   */
  formatLogEntry: function(level, message, context) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      level: level,
      message: message,
      n8n: {},
      app: {
        correlationId: context.correlationId || null,
        nodeName: context.nodeName || null,
      },
      payload: context.data || context.payload || {},
    };

    if (context.workflowInstance) {
      logEntry.n8n.executionId = context.workflowInstance.id || null;
      logEntry.n8n.workflowId = context.workflowInstance.workflowId || null;
      // In N8N versions < 1.0, workflowId might be under context.workflowInstance.workflow.id
      if (!logEntry.n8n.workflowId && context.workflowInstance.workflow && context.workflowInstance.workflow.id) {
          logEntry.n8n.workflowId = context.workflowInstance.workflow.id;
      }
    }
    
    // Merge any other properties directly from context if they don't conflict
    // and are not already handled (like workflowInstance, nodeName, correlationId, data, payload)
    const reservedContextKeys = ['workflowInstance', 'nodeName', 'correlationId', 'data', 'payload'];
    for (const key in context) {
        if (context.hasOwnProperty(key) && !reservedContextKeys.includes(key) && typeof logEntry.payload[key] === 'undefined') {
            logEntry.payload[key] = context[key];
        }
    }
    // If context.data or context.payload was an array or primitive, ensure payload is an object
    if (typeof logEntry.payload !== 'object' || logEntry.payload === null) {
        logEntry.payload = { value: logEntry.payload };
    }


    return logEntry;
  },

  /**
   * Logs an informational message.
   * @param {object} workflowInstance - The N8N workflow execution instance data (e.g., from $execution).
   * @param {string} nodeName - The name of the N8N node generating the log.
   * @param {string} correlationId - The correlation ID for distributed tracing.
   * @param {string} message - The informational message.
   * @param {object} [data={}] - Additional data to include in the log context.
   * @returns {void}
   */
  logInfo: function(workflowInstance, nodeName, correlationId, message, data = {}) {
    const context = {
      workflowInstance: workflowInstance,
      nodeName: nodeName,
      correlationId: correlationId,
      data: data,
    };
    const logEntry = this.formatLogEntry("INFO", message, context);
    console.log(JSON.stringify(logEntry));
  },

  /**
   * Logs an error message.
   * @param {object} workflowInstance - The N8N workflow execution instance data.
   * @param {string} nodeName - The name of the N8N node generating the log.
   * @param {string} correlationId - The correlation ID.
   * @param {string} errorMessage - The primary error message.
   * @param {object} [errorDetails={}] - Additional details about the error (e.g., stack trace, error code).
   * @returns {void}
   */
  logError: function(workflowInstance, nodeName, correlationId, errorMessage, errorDetails = {}) {
    const context = {
      workflowInstance: workflowInstance,
      nodeName: nodeName,
      correlationId: correlationId,
      data: errorDetails, // errorDetails are treated as the payload for error logs
    };
    const logEntry = this.formatLogEntry("ERROR", errorMessage, context);
    console.log(JSON.stringify(logEntry));
  }
};

// For direct use in N8N Function nodes, you might copy the object or its methods.
// e.g., const logging = InfluenceGenN8NUtilsLogging;
// logging.logInfo(...);
// Or if embedding:
// const formatLogEntry = function(...) { ... };
// const logInfo = function(...) { ... };
// const logError = function(...) { ... };