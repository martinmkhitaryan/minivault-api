"""
Minimal test script for minivault-api service.
Run after 'docker compose up' or 'fastapi dev app.py'.
"""

import asyncio

import httpx

BASE_URL = "http://localhost:8000"


async def wait_for_service():
    for _ in range(20):
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                r = await client.get(f"{BASE_URL}/docs")
                if r.status_code == 200:
                    print("Service is up!")
                    return True
        except Exception:
            pass
        await asyncio.sleep(1)
    print("Service did not start in time.")
    return False


async def test_generate():
    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(f"{BASE_URL}/generate", json={"prompt": "Hello, world!"})
        print("/generate status:", r.status_code)
        print("/generate response:", r.text)


async def test_stream():
    async with httpx.AsyncClient(timeout=10.0) as client:
        async with client.stream("POST", f"{BASE_URL}/stream", json={"prompt": "Stream test."}) as r:
            print("/stream status:", r.status_code)
            print("/stream response:")
            async for chunk in r.aiter_text():
                print(chunk, end="", flush=True)
            print()


async def main():
    if not await wait_for_service():
        return
    await test_generate()
    await test_stream()


if __name__ == "__main__":
    asyncio.run(main())
