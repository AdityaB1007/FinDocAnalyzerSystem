from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
import os
import uuid
from typing import Dict
from crewai import Crew, Process
from crewai_tools import PDFSearchTool
from tools import analyze_investment_tool, create_risk_assessment_tool
from agents import financial_analyst, verifier, risk_assessor, investment_advisor
from task import analyze_financial_document, risk_assessment, investment_analysis, verification

app = FastAPI(title="Financial Document Analyzer")

job_results: Dict[str, dict] = {}

def run_crew(job_id: str, query: str, file_path: str):
    """To run the whole crew"""
    
    job_results[job_id] = {"status": "processing", "result": None}

    safe_path = file_path.replace("\\", "/")

    dynamic_pdf_tool = PDFSearchTool(
            pdf=safe_path, 
            config=dict(
                llm=dict(provider="ollama", config=dict(model="llama3.1:8b", base_url="http://localhost:11434")),
                embedder=dict(provider="ollama", config=dict(model="nomic-embed-text"))
            )
        )

    verifier.tools = [dynamic_pdf_tool]
        # Analyst gets BOTH the PDF tool and the investment tool
    financial_analyst.tools = [dynamic_pdf_tool, analyze_investment_tool]
        # Risk Assessor gets BOTH the PDF tool and the risk tool
    risk_assessor.tools = [dynamic_pdf_tool, create_risk_assessment_tool]

    try:
        
        financial_crew = Crew(
            agents=[verifier, financial_analyst, risk_assessor, investment_advisor],
            tasks=[verification, analyze_financial_document, risk_assessment, investment_analysis],
            process=Process.sequential,
            verbose=True
        )
    
        result = financial_crew.kickoff({'query': query, 'file_path': safe_path})
        job_results[job_id] = {"status": "completed", "result": str(result)}

    except Exception as e:

        job_results[job_id] = {"status": "failed", "error": str(e)}
        
    finally:

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def process_document_endpoint(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    job_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{job_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        if not query or query.strip() == "":
            query = "Analyze this financial document for investment insights"
            
        # Run the full pipeline
        background_tasks.add_task(run_crew, job_id, query.strip(), file_path)
        
        return {
            "message": "Document received and processing started",
            "status_url": f"/status/{job_id}",
            "query": query,
            "job_id": job_id,
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


@app.get("/status/{job_id}")
async def check_status(job_id: str):
    """Check the status of a processing job"""
    if job_id not in job_results:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    return job_results[job_id]

if __name__ == "__main__":
    import uvicorn
    # Fixed the reload argument requirement
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)