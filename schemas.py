from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    prompt: str = Field(
        ..., description="The prompt to generate a response for", min_length=1, max_length=8192
    )  # Adjust max length later


class GenerateResponse(BaseModel):
    response: str
