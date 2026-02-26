# FinDocAnalyzerSystem
Wingify GenAI Eng Intern Task

A high-performance, privacy-focused financial analysis pipeline that uses **Multi-Agent Orchestration** to extract insights from PDF documents. This system runs entirely on local hardware using **Ollama**, ensuring sensitive financial data is never transmitted to third-party APIs.

## Architecture

The system is built on a **FastAPI** backend and orchestrated by **CrewAI**. It follows a **RAG (Retrieval-Augmented Generation)** architecture to handle large documents efficiently.

* **Financial Document Verifier:** Ensures the file is a legitimate financial report (10-K, 10-Q, etc.).
* **Senior Financial Analyst:** Extracts key metrics (Revenue, Net Income, Cash Flow) using semantic search.
* **Risk Assessment Specialist:** Evaluates potential red flags and liabilities.
* **Investment Advisor:** Synthesizes all findings with real-time market context (via Serper) to provide a final recommendation.

# Bugs and Fixes
```
1. first the requirements list. It had too many clashes with the dependencies.
2. "agents.py", 'tool' should have been 'tools'.
3. "agents.py", Design/Logic Problems:
                
                Irresponsible Agent Configurations: All agents are intentionally designed with problematic behaviors:

                1. Financial Analyst: Makes up advice, ignores compliance, makes assumptions without reading reports
                2. Verifier: Approves everything without actual verification
                3. Investment Advisor: Recommends risky products, ignores SEC compliance, includes fake credentials
                4. Risk Assessor: Promotes reckless "YOLO" investing
                
                Financial Compliance Violations: The entire system openly disregards regulatory requirements (SEC, financial compliance standards)
                Misleading User Guidance: Each agent's backstory and goal explicitly instruct them to be untrustworthy and reckless with financial advice.
                This appears to be a satirical demonstration of what NOT to do in a financial advisor system. If this is meant to be a real production system, it needs fundamental redesign with proper compliance, verification processes, and qualified financial guidance.

    Fixes - 1. Fixed tool= → tools= parameter error 
            2. Financial Analyst - Now focuses on thorough analysis based on actual data with compliance and due diligence
            3. Document Verifier - Now properly validates documents with strict compliance standards instead of approving everything
            4. Investment Advisor - Now provides evidence-based recommendations with transparency and follows SEC/FINRA regulations
            5. Risk Assessor - Now conducts objective risk assessments using established methodologies and promotes responsible diversification

4.  max_iter=1 - Very restrictive. This means each agent gets only ONE iteration/thought cycle. For financial analysis, each agent will often need multiple iterations.
    max_rpm=1 - This is extremely slow. It limits to 1 request per minute, which will make the entire system crawl. This should probably be 10-60+ depending on your OpenAI API rate limits. Setting it too low will cause unnecessary delays.

    Fixes - 1. max_iter=5 - All agents now have reasonable iteration limits
            2. max_rpm=30 - Much better than 1 request per minute

5.  from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model="gpt-4", api_key=os.getenv("OPENAI_API_KEY"))
    (Now changed to ollama 'llama3.1' model)

6. "agents.py", The investment_advisor and risk_assessor agents don't have memory=True set (unlike analyst and verifier). Since investment advisors especially benefit from retaining context about client situations across interactions, considered adding memory=True to those agents as well.

7. "tools.py", from crewai_tools.tools.serper_dev_tool import SerperDevTool
                ImportError: cannot import name 'SerperDevTool' from 'crewai_tools.tools.serper_dev_tool' (unknown location), fix - 'from crewai_tools import tools''from crewai_tools.tools.serper_dev_tool import SerperDevTool' to 'from crewai_tools import SerperDevTool'

8. "tools.py", 'docs = Pdf(file_path=path).load()' to 'docs = PyPDFLoader(file_path=path).load()' using 'from langchain_community.document_loaders import PyPDFLoader'

9. "tools.py",  async def should be def: CrewAI tools should be regular functions, not async. Async will cause issues when crewai tries to use them.


10. "tools.py", tools are functionally unfinished and architecturally incomplete for use within the CrewAI framework.

    1. Missing the @tool Decorator
        CrewAI agents cannot "see" these functions as tools unless they are decorated. The framework uses the decorator to extract the function's name and docstring so the LLM knows when and how to call it.

    2. Logic is Placeholder Only
        The TODO comments are accurate—there is currently no actual analysis happening.
        InvestmentTool: It only performs a basic string cleanup (removing double spaces) and returns a hardcoded string.
        RiskTool: It currently takes data and immediately returns a "to be implemented" string without processing anything.

    3. Argument Type Hinting
        CrewAI tools rely heavily on Python type hints and docstrings. Without a clear docstring, the Agent will likely hallucinate what the tool does or pass the wrong data types to it.

11. "agents.py", 
Agent	            Current Tools	    Problem
Financial Analyst	[read_data_tool]	It has the "Investment Analysis" tool available in imports but not assigned.
Document Verifier	None	            Critical. It is tasked with verifying documents but has no tool to read them. It can't verify what it can't see.
Investment Advisor	None	            It is expected to give recommendations but has no access to the search tool to check current market prices or news.
Risk Assessor	    None	            It has no tools assigned to actually perform the risk calculations or read the data.


12. "task.py", all the instructions were bogus, had to change them. Every single task was assigned to financial_analyst.
13. "task.py", trying to import FinancialDocumentTool and use FinancialDocumentTool.read_data_tool. That class doesn't exist in tools.py now as we only have standalone functions now. If we assign a tool to the Agent, we don't necessarily need to re-assign it to the Task unless you are overriding something.
14. "task.py", No Sequential Context: For a pipeline to work, the Risk Assessor needs to read the Analyst's report. Right now, all four tasks are running blind without passing data to each other.
15. "main.py", 
    1. The Naming Collision (Fatal Error)
        You imported a task named analyze_financial_document, but then you named your FastAPI endpoint async def analyze_financial_document(...).
        The Result: Python reads top-to-bottom. It will overwrite your CrewAI Task object with the FastAPI route function. When run_crew tries to execute the task, it will crash because it's trying to execute a web route instead of a Task.

    2. The "Missing File" Black Hole
        Your API correctly receives the file, saves it, and passes file_path to run_crew(). But inside run_crew(), look at your kickoff:
        result = financial_crew.kickoff({'query': query})
        The Result: You never pass the file_path into the Crew. The agents will execute, but they will have absolutely no idea where the uploaded PDF is stored.

    3. The Abandoned Crew
        You only imported one agent (financial_analyst) and one task. The Verifier, Risk Assessor, and Investment Advisor are entirely missing from this execution.

    4. The Uvicorn Reload Crash
        uvicorn.run(app, reload=True) will throw an error. When hot-reloading is enabled, Uvicorn requires the application to be passed as an import string ("main:app") rather than the direct object.

16. "main.py", Renamed the function to avoid shadowing the imported Task
17. "main.py", Fixed the reload argument requirement
18. "tools.py", changed tool import: 'from crewai.tools import tool'
```

---

# Setup and Usage Instructions

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

## Local LLM Optimization (Technical Notes)
Running agents on 8B parameter models requires specific configuration to prevent parsing errors:

1. ReAct Loop Stabilization: Small models often struggle with complex JSON tool inputs. This system uses Dynamic Tool Injection to hardcode file paths into tools,    reducing the agent's input requirement to a single string.

2. Memory Management: Sequential processing (Process.sequential) is utilized to ensure that the heavy embedding process is completed before the next agent begins     its reasoning.

3. Agentic Memory System:
   To ensure the pipeline is cohesive, we enabled Short-Term Memory across the crew.
   Contextual Awareness: This allows the Investment Advisor to remember the specific risks identified by the Risk Assessor without re-reading the entire document.
   Implementation: The memory system utilizes a local RAG storage to keep track of the "Shared Mental Model" between agents, ensuring that even if an agent    finishes its task, its findings remain available for the next specialist in the chain.

4. Dynamic Tooling (RAG)
   To prevent the LLM from hallucinating file paths, we utilize Dynamic Tool Injection. The PDFSearchTool is instantiated inside the API route with a hardcoded       path, allowing the agent to call it using only a simple query string.

5. ReAct Loop Stability
   Handle Parsing Errors: Agents are configured with handle_parsing_errors=True to allow the framework to catch and correct minor formatting slips.
   Reduced Iterations: max_iter is limited to prevent "infinite loops" where the agent repeatedly queries the same data without progressing.
    Sync Config: We ensure the LLM configuration inside the PDFSearchTool matches the Agent's LLM to maintain consistent output formatting.

6. Error Handling: All agents are configured with handle_parsing_errors=True to allow them to recover if the model formatting slightly deviates from the expected     Markdown schema.

## Known Limitations & Future Tweaks

1. Context Window: Local 8B models can become "distracted" by very large chunks of text. Future versions will implement more aggressive text cleaning.
2. Inference Speed: Performance is highly dependent on GPU/CPU speed.
3. Formatting: If the model returns a "Failed to Parse" error, adjusting the backstory to be more concise often resolves the issue.

# API Documentation
```
Endpoint        Method        Description
/               GET           Health check for the API.
/analyze        POST          Accepts a PDF and a query. Starts the multi-agent pipeline.
/status/{id}    GET           Returns the current status (processing, completed, or failed).
```

