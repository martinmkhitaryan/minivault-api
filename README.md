# MiniVault API

A minimal FastAPI-based API for generating and streaming responses from a Language Model (LLM). Supports both a stubbed (mock) LLM and integration with [Ollama](https://ollama.com/) for local LLM inference.

> **Note:** This is a test task project.

## Features
- **/generate**: Generate a full response from an LLM in one request.
- **/stream**: Stream the LLM response chunk by chunk.
- **Pluggable LLM backend**: Use a stubbed LLM for testing or connect to Ollama for real responses.
- **Structured JSONL logging**: All requests and responses are logged to `logs/` in JSONL format.

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd minivault-api
   ```
2. **Create a virtual environment and activate it**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The backend LLM service is controlled by the environment variable `MINIVAULT_LLM_SERVICE`:
- `stubbed` (default): Uses a mock LLM with canned responses.
- `ollama`: Connects to a local Ollama server (default: `http://localhost:11434`, model: `tinyllama`).

Set the variable before running the server:
```bash
export MINIVAULT_LLM_SERVICE=ollama
```

## Running the API

```bash
fastapi dev app.py
```

The API will be available at `http://localhost:8000` by default.

### With Docker Compose

You can run the API and Ollama LLM backend together using Docker Compose:

```bash
docker compose up --build
```

This will start two containers:
- **ollama**: Runs the Ollama LLM server and pulls the `tinyllama` model.
- **minivault-api**: Runs the FastAPI app, configured to use the Ollama backend.

The API will be available at [http://localhost:8000](http://localhost:8000).

## Testing the Service

A minimal test script is provided to verify the API endpoints after startup:

```bash
python test_service.py
```

This script will:
- Wait for the API service to become available
- Test the `/generate` endpoint
- Test the `/stream` endpoint


## Example Usage

**Generate (full response):**
```bash
curl -X POST http://localhost:8000/generate \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Hello, world!"}'
```

**Stream (chunked response):**
```bash
curl --no-buffer -X POST http://localhost:8000/stream \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Hello, world!"}'
```

## Logging
- All requests and responses are logged in JSONL format in the `logs/` directory, one file per day.
- Each log entry includes endpoint, prompt, response, LLM type, timestamps, and duration.

## Development
- Code style: [Black](https://black.readthedocs.io/en/stable/), [flake8](https://flake8.pycqa.org/en/latest/)

---

## Notes on Project Structure and Logging

**Project Structure:**

- The project uses a flat file structure for simplicity, as this is just a test task.
- In a production environment, I would use a more modular and layered structure (e.g., separating routers, services, etc.).

**Logging:**

- Currently, logging to a file is performed in the FastAPI controllers in app.py, and logging is handled in a separate thread to avoid blocking the main request flow. In a production system, it might be more appropriate to move logging to the services themselves, depending on what information should be logged and where the most relevant context is available. For this test task, the current approach is sufficient, but the decision can be adapted based on requirements and context.

## Design Choices & Future Improvements

- This project uses a flat structure and controller-based logging for simplicity, but in production, modularization and separation of API and worker components would be prioritized for scalability and maintainability. 
- Additionally, while a single pod deployment is sufficient for simple or test scenarios, in production it is preferable to deploy the frontend API and backend workers in separate pods. This allows for independent scaling, better resource isolation, and avoids interference between request handling and background processing. 
- For streaming responses, returning token by token might not be optimal due to syscall overhead; buffering could be more profitable, but performance testing would be needed to confirm. FastAPI's StreamingResponse might already have built-in buffering mechanisms.
- Testing: The project should include pytest for unit testing. Unit tests should be added to ensure proper functionality of the LLM services, API endpoints, and data validation. This would include testing both the stubbed and Ollama LLM services, as well as the FastAPI endpoints with proper mocking of dependencies.