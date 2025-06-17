# odoo_modules/influence_gen_integration_adapters/dtos/n8n_dtos.py
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class N8nAiGenerationRequestDto:
    """
    Data Transfer Object for initiating AI image generation via N8N.
    """
    request_id: str # Odoo-generated unique ID for this request
    prompt: str
    user_id: int # Odoo user ID
    influencer_profile_id: int # Odoo influencer_profile ID
    negative_prompt: Optional[str] = None
    model_id: Optional[str] = None # Identifier for the AI model/LoRA
    resolution: Optional[str] = "1024x1024" # e.g., "widthxheight"
    aspect_ratio: Optional[str] = "1:1"
    seed: Optional[int] = None
    inference_steps: Optional[int] = 20
    cfg_scale: Optional[float] = 7.5
    campaign_id: Optional[int] = None # Odoo campaign ID
    # Add any other parameters required by N8N/AI service
    custom_params: Optional[Dict[str, Any]] = field(default_factory=dict)

@dataclass
class GeneratedImageDataDto:
    """
    Data Transfer Object for individual generated image data from N8N.
    """
    image_url: Optional[str] = None # If N8N returns a temporary URL
    image_data_b64: Optional[str] = None # If N8N returns base64 encoded image data
    filename: Optional[str] = None # Suggested filename
    content_type: Optional[str] = None # e.g., 'image/png'
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict) # Any extra metadata from generation

@dataclass
class N8nAiGenerationResultDto:
    """
    Data Transfer Object for the result of an AI image generation process from N8N.
    """
    request_id: str # Corresponds to the Odoo request_id
    status: str # e.g., "success", "failure"
    images: List[GeneratedImageDataDto] = field(default_factory=list)
    error_message: Optional[str] = None
    error_code: Optional[str] = None # External service error code
    n8n_execution_id: Optional[str] = None # N8N's own execution ID for tracing