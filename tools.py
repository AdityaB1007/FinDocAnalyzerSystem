## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool, PDFSearchTool
from crewai.tools import tool
from langchain_community.document_loaders import PyPDFLoader

## Creating search tool
search_tool = SerperDevTool()
pdf_search_tool = PDFSearchTool()

## Creating custom pdf reader tool
@tool("Document Readr")
def read_data_tool(path: str) -> str:
    """Tool to read data from a pdf file from a path

    Args:
        path (str): Path to the financial document pdf file
    Returns:
        str: Full Financial Document file
    """
    try:
         
        docs = PyPDFLoader(file_path=path).load()

        full_report = ""
        for data in docs:
            content = data.page_content
            clean_content = " ".join(content.split())
            full_report += clean_content + "\n"
        return full_report
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

## Creating Investment Analysis Tool
@tool("Investment Analyzer")
def analyze_investment_tool(financial_document_data: str) -> str:
    """
    Analyzes financial document data for investment opportunities. 
    Expects a string of financial text and returns a summary of key metrics.
    """
    # 1. Clean data (your original logic, optimized)
    clean_data = " ".join(financial_document_data.split())
    
    # 2. Example Analysis Logic (Replace with your actual math/logic)
    # In a real tool, you might use regex to find numbers or send this to a sub-LLM
    if "revenue" in clean_data.lower():
        return f"Analysis Complete: Found revenue mentions. Data quality: {len(clean_data)} chars."
    
    return "Analysis Complete: No standard investment markers found in the text."

## Creating Risk Assessment Tool
@tool("Risk Assessment Tool")
def create_risk_assessment_tool(financial_document_data: str) -> str:
    """
    Evaluates potential risks based on provided financial data.
    Returns a risk level (Low/Medium/High) and a brief justification.
    """
    # Placeholder for actual risk logic (e.g., debt-to-equity checks)
    data_lower = financial_document_data.lower()
    
    if "debt" in data_lower or "liability" in data_lower:
        return "Risk Assessment: MEDIUM. Document mentions liabilities that require further audit."
    
    return "Risk Assessment: LOW. No immediate red flags detected in the provided text."