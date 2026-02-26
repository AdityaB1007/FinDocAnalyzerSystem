# FinDocAnalyzerSystem
Wingify GenAI Eng Intern Task

A high-performance, privacy-focused financial analysis pipeline that uses **Multi-Agent Orchestration** to extract insights from PDF documents. This system runs entirely on local hardware using **Ollama**, ensuring sensitive financial data is never transmitted to third-party APIs.


## Architecture

The system is built on a **FastAPI** backend and orchestrated by **CrewAI**. It follows a **RAG (Retrieval-Augmented Generation)** architecture to handle large documents efficiently.

* **Financial Document Verifier:** Ensures the file is a legitimate financial report (10-K, 10-Q, etc.).
* **Senior Financial Analyst:** Extracts key metrics (Revenue, Net Income, Cash Flow) using semantic search.
* **Risk Assessment Specialist:** Evaluates potential red flags and liabilities.
* **Investment Advisor:** Synthesizes all findings with real-time market context (via Serper) to provide a final recommendation.

## Setup & Installation

### 1. Prerequisites
* **Python 3.10+**
* **Ollama** (Download at [ollama.com](https://ollama.com))

### 2. Local Model Preparation
You must pull the required models to your local machine:
```
# LLM for reasoning
ollama pull llama3.1:8b

# Embedding model for PDF search
ollama pull nomic-embed-text
```
### 3. Installation
Clone the repository and install dependencies using **requirements.txt**:

## Usage Instructions

### Running the API
Start the FastAPI server:
```
python main.py
```

### Sending a Document for Analysis
Use curl or any API client (like Postman) to upload a PDF:
```
curl.exe -X POST "http://localhost:8000/analyze" `
  -F "file=@path/to/your/document.pdf" `
  -F "query=Extract key financial metrics and assess risk"
```

### Checking Status
The analysis runs in the background. Poll the status endpoint using the job_id returned from the initial request:
```
GET http://localhost:8000/status/{job_id}
```

## API Documentation
```
Endpoint        Method        Description
/               GET           Health check for the API.
/analyze        POST          Accepts a PDF and a query. Starts the multi-agent pipeline.
/status/{id}    GET           Returns the current status (processing, completed, or failed).
```

## Local LLM Optimization (Technical Notes)
Running agents on 8B parameter models requires specific configuration to prevent parsing errors:

1. ReAct Loop Stabilization: Small models often struggle with complex JSON tool inputs. This system uses Dynamic Tool Injection to hardcode file paths into tools,    reducing the agent's input requirement to a single string.
2. Stop Sequences: To prevent "hallucinated" thoughts, the LLM is configured with stop=["Observation:"].
3. Memory Management: Sequential processing (Process.sequential) is utilized to ensure that the heavy embedding process is completed before the next agent begins     its reasoning.
4. Error Handling: All agents are configured with handle_parsing_errors=True to allow them to recover if the model formatting slightly deviates from the expected     Markdown schema.

## Known Limitations & Future Tweaks

1. Context Window: Local 8B models can become "distracted" by very large chunks of text. Future versions will implement more aggressive text cleaning.
2. Inference Speed: Performance is highly dependent on GPU/CPU speed.
3. Formatting: If the model returns a "Failed to Parse" error, adjusting the backstory to be more concise often resolves the issue.

