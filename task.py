## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, risk_assessor, investment_advisor
#from tools import search_tool, FinancialDocumentTool

## Creating a task to help solve user's query

verification = Task(
    description=(
        "Search the PDF for the 'Company Name' and 'Document Title'. "
        "Use the tool with a simple string query. "
        "Confirm if this is a legitimate 10-K, quarterly update, or balance sheet."
    ),
    expected_output="A simple string containing the Company Name and document type.",
    agent=verifier,
    human_input=False,
    max_inter=2,
)

analyze_financial_document = Task(
    description=(
        "Using the document verified in the previous step, perform a strict, factual extraction of key financial metrics. "
        "Focus on actual numbers reported in the text, such as Revenue, Net Income, Margins, or Cash Flow. "
        "Do not make up any numbers. If a metric is not in the document, explicitly state 'Not provided'. "
        "Address any specific requests from the user's query: {query}."
    ),
    expected_output="A bulleted list of actual financial metrics extracted directly from the document with no speculation.",
    agent=financial_analyst,
    context=[verification], # This forces the Analyst to wait for the Verifier
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description=(
        "Review the factual metrics provided by the Financial Analyst. "
        "Use your risk assessment tools to identify any explicit risks mentioned in the text (e.g., 'debt', 'liabilities', 'market headwinds'). "
        "Provide a grounded Risk Level (Low/Medium/High) based strictly on the data."
    ),
    expected_output="A sober risk assessment report highlighting only the risks explicitly found in the financial data.",
    agent=risk_assessor,
    context=[analyze_financial_document], # Waits for the Analyst
    async_execution=False,
)

investment_analysis = Task(
    description=(
        "Review the complete pipeline: the verified document, the extracted metrics, and the risk assessment. "
        "Use your search tool to find 2-3 recent, real-world news headlines about this company to contextualize the data. "
        "Synthesize this into a final, highly professional investment recommendation (Buy/Hold/Sell) that directly answers the user's query: {query}. "
        "Include strict disclaimers that this is AI-generated financial analysis."
    ),
    expected_output="A professional 3-paragraph investment memo combining the PDF data with live market context, including a clear recommendation and disclaimers.",
    agent=investment_advisor,
    context=[verification, analyze_financial_document, risk_assessment], # Needs the full picture
    async_execution=False,
)
