# odoo_modules/influence_gen_integration_adapters/doc/openapi/n8n_callback_v1.yaml
openapi: 3.0.0
info:
  title: InfluenceGen N8N Callback API
  version: v1
  description: API endpoint for N8N to send AI image generation results to Odoo.
servers:
  - url: '{odoo_base_url}' # Variable for Odoo base URL
    variables:
      odoo_base_url:
        default: https://your-odoo-instance.com # To be replaced by actual instance URL
components:
  securitySchemes:
    N8NSharedSecret:
      type: apiKey
      in: header
      name: X-N8N-Signature # Header name for the shared secret/token
  schemas:
    GeneratedImageDataDto:
      type: object
      properties:
        image_url:
          type: string
          format: url
          nullable: true
          description: URL if N8N returns a temporary URL for the image.
        image_data_b64:
          type: string
          format: byte # base64 encoded string
          nullable: true
          description: Base64 encoded image data if N8N returns the image directly.
        filename:
          type: string
          nullable: true
          description: Suggested filename for the image.
        content_type:
          type: string
          nullable: true # e.g., image/png, image/jpeg
          description: MIME type of the image.
        metadata:
          type: object
          additionalProperties: true
          nullable: true
          description: Any extra metadata from the image generation process.
      description: Represents a single generated image's data.

    N8nAiGenerationResult:
      type: object
      required:
        - request_id
        - status
      properties:
        request_id:
          type: string
          description: The Odoo-generated unique ID of the original image generation request.
        status:
          type: string
          enum: [success, failure]
          description: Overall status of the AI image generation task.
        images:
          type: array
          items:
            $ref: '#/components/schemas/GeneratedImageDataDto'
          description: List of generated images (data or URLs). Populated if status is 'success'.
          nullable: true
        error_message:
          type: string
          nullable: true
          description: Detailed error message if the status is 'failure'.
        error_code:
          type: string
          nullable: true
          description: External service error code, if applicable, when status is 'failure'.
        n8n_execution_id:
            type: string
            nullable: true
            description: N8N's internal execution ID for this workflow run, for tracing purposes.
      description: Payload sent from N8N to Odoo with the results of an AI image generation request.

paths:
  /influence_gen/n8n/ai_callback:
    post:
      summary: Receives AI image generation results from N8N.
      description: This endpoint is called by N8N to deliver the outcome (success or failure) of an AI image generation task initiated by Odoo.
      operationId: handleAiImageResult
      security:
        - N8NSharedSecret: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/N8nAiGenerationResult'
      responses:
        '200':
          description: Callback successfully received and accepted for processing.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: success
                    description: Indicates that the callback was accepted.
        '400':
          description: Bad Request - The payload is invalid or malformed.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: Invalid payload format
        '401':
          description: Unauthorized - Authentication failed (e.g., invalid X-N8N-Signature).
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: Authentication failed
        '500':
          description: Internal Server Error - An error occurred on the Odoo side while processing the callback.
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: string
                    example: Error processing callback