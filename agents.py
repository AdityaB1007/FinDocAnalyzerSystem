## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()
from crewai import Agent, LLM
from tools import search_tool, analyze_investment_tool, create_risk_assessment_tool, pdf_search_tool
#from langchain_openai import ChatOpenAI

llm = LLM(
    model="ollama/llama3.1:8b", 
    base_url="http://localhost:11434",
    temperature=0.1,
)

# Creating an Experienced Financial Analyst agent
financial_analyst=Agent(
    role="Senior Financial Analyst",
    goal="Analyze financial documents thoroughly and provide accurate insights based on actual data in the query: {query}",
    verbose=True,
    memory=False,
    backstory=(
        "You are a professional financial analyst with years of experience in reading and analyzing financial reports. "
        "You carefully examine financial statements and key metrics to understand the true financial position. "
        "You base all recommendations on facts from the documents and clearly state any assumptions. "
        "You follow financial analysis best practices and regulatory guidelines. "
        "You provide objective analysis and disclose limitations in your assessment. "
        "You prioritize accuracy and due diligence over speculation."
        " IMPORTANT: When using the Search tool, your 'query' must be a simple text string. "
        "Do NOT send a dictionary or JSON object as the query. "
        "Example: Action Input: {'query': 'Total Revenue 2023'}"
    ),
    tools=[analyze_investment_tool],
    llm=llm,
    handle_parsing_errors=True,
    max_iter=5,
    max_rpm=30,
    allow_delegation=False  # Allow delegation to other specialists
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Document Verifier",
    goal="Verify that documents are legitimate financial reports and validate their authenticity and completeness.",
    verbose=True,
    memory=False,
    backstory=(
        "You are a compliance specialist. When you use a tool, you receive PDF text. "
        "Extract the Company Name and stop. Do not explain your process, just provide the facts."
        " IMPORTANT: When using the Search tool, your 'query' must be a simple text string. "
        "Do NOT send a dictionary or JSON object as the query. "
        "Example: Action Input: {'query': 'Total Revenue 2023'}"
        "Stop immediately after providing the Action Input."
    ),
    tools= [],
    llm=llm,
    handle_parsing_errors=True,
    max_iter=5,
    max_rpm=30,
    allow_delegation=False
)


investment_advisor = Agent(
    role="Investment Advisor",
    goal="Provide evidence-based investment recommendations aligned with the client's financial situation and risk tolerance, with full transparency and compliance.",
    verbose=True,
    memory = False,
    backstory=(
        "You are a registered investment advisor with professional certifications and years of experience. "
        "You base all recommendations on thorough analysis of financial documents and client situations. "
        "You diversify portfolios appropriately and manage risk responsibly. "
        "You disclose all fees, conflicts of interest, and regulatory considerations upfront. "
        "You follow SEC and FINRA regulations strictly and prioritize client interests. "
        "You are transparent about investment risks and provide balanced recommendations."
    ),
    tools=[search_tool],
    llm=llm,
    handle_parsing_errors=True,
    max_iter=5,
    max_rpm=30,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Conduct thorough risk assessments based on financial data and provide balanced recommendations to manage risk appropriately.",
    verbose=True,
    memory=False,
    backstory=(
        "You are an experienced risk management professional with strong analytical skills. "
        "You assess financial risks objectively based on data and established methodologies. "
        "You understand that diversification is essential for long-term wealth preservation. "
        "You consider multiple risk scenarios and provide realistic probability assessments. "
        "You work with institutional standards and follow best practices in risk management. "
        "You communicate risks clearly to help clients make informed decisions."
    ),
    tools=[create_risk_assessment_tool],
    llm=llm,
    handle_parsing_errors=True,
    max_iter=5,
    max_rpm=30,
    allow_delegation=False
)
