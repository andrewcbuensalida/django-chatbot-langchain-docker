from langsmith import traceable  # Automatically looks at .env from os.environ to connect to langsmith
from langsmith.wrappers import wrap_openai
from langchain_core.retrievers import BaseRetriever
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from django.conf import settings
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor



# Turn vector retriever into a tool
index_name = "cancer-wiki"
embeddings = OpenAIEmbeddings()
docsearch = PineconeVectorStore.from_existing_index(index_name, embeddings)
retriever_tool = create_retriever_tool(
    docsearch.as_retriever(    
    search_kwargs={
        "k":2 # how many chunks to return from vector store. If you use the default value of 4, it won't find that Andrew has experience in Python
    }),
    "cancer_search",
    "Search for information about cancer based on wikipedia page. For any questions about cancer, you must use this tool!",
)

# Define another search tool
tavily_search = TavilySearchResults()

# Combine the tools
tools = [tavily_search, retriever_tool]

# Define the LLM
llm = ChatOpenAI(model="gpt-4", temperature=0,api_key=settings.OPENAI_API_KEY)

# Define the prompt
prompt = hub.pull("hwchase17/openai-functions-agent") # Prompt to guide agent

# Initialize agent
agent = create_tool_calling_agent(llm, tools, prompt) # the brains

# Define the agent executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # this repeatedly calls the agent and executes the tools