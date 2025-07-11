import time

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse

from dependencies import get_llm_service
from logger import jsonl_logger
from schemas import GenerateRequest, GenerateResponse
from services import LLMService

app = FastAPI()


@app.post("/generate")
async def generate(
    body: GenerateRequest,
    llm_service: LLMService = Depends(get_llm_service),
) -> GenerateResponse:
    started_at = time.time()
    llm_response = await llm_service.generate(body.prompt)
    finished_at = time.time()
    jsonl_logger.log(
        {
            "endpoint": "/generate",
            "prompt": body.prompt,
            "response": llm_response,
            "llm_type": llm_service.get_type().value,
            "started_at": started_at,
            "finished_at": finished_at,
            "duration_ms": (finished_at - started_at) * 1000,
        }
    )
    return GenerateResponse(response=llm_response)


@app.post("/stream")
async def stream(
    body: GenerateRequest,
    llm_service: LLMService = Depends(get_llm_service),
) -> StreamingResponse:
    async def stream_generator():
        # NOTE: Here is a tradeoff between logging and latency.
        #       1. Logging the full response after the stream is complete would add latency and use
        #          more memory because we need to keep the chunks in memory.
        #       2. Logging the each chunk would add logging overhead and later we would need
        #          to aggregate the chunks.
        started_at = time.time()
        full_response: list[str] = []
        async for chunk in await llm_service.stream(body.prompt):
            yield chunk
            full_response.append(chunk)

        finished_at = time.time()
        jsonl_logger.log(
            {
                "endpoint": "/stream",
                "prompt": body.prompt,
                "response": "".join(full_response),
                "llm_type": llm_service.get_type().value,
                "started_at": started_at,
                "finished_at": finished_at,
                "duration_ms": (finished_at - started_at) * 1000,
            }
        )

    return StreamingResponse(stream_generator(), media_type="text/plain")
