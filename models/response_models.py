from pydantic import BaseModel

class ImageAnalysisResponse(BaseModel):
    analysis_text: str

class TextResponse(BaseModel):
    response: str