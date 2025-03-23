import os
from dotenv import load_dotenv
from typing import cast, List
import chainlit as cl
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from agents.tool import function_tool
from retrievel_tool import qa
from google_search import client, model_id, google_search_tool
from google.genai.types import GenerateContentConfig




# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

@cl.set_starters  # type: ignore
async def set_starts() -> List[cl.Starter]:
    return [
        cl.Starter(
            label="Greetings",
            message="Hello! What can you help me with today?",
        ),
        cl.Starter(
            label="Cancer Symptoms",
            message="What are the symptoms of Cancer?",
        ),
    ]

@function_tool
@cl.step(type="retrieval")
def retrieval(question: str):
    """
    Retrieve relevant medical information for the given question from the vector database. 
    This tool searches pre-stored medical knowledge and returns the most contextually relevant answer. 
    Input: Medical question as a string.
    Output: Retrieved answer from the vector store to be used in forming the final medical response.

    """
    result = qa.invoke({"query": question})
    return result["result"]

@function_tool
@cl.step(type="search_tool")
def search_tool(content: str):
    
    """
    Search the internet for up-to-date and relevant medical information based on the user's query. 
    This tool is used when additional or current information is required to supplement vector store results. 
    Always use this tool to gather accurate and recent medical data to support the final response. 
    Input: User query as a string.
    Output: Extracted text result from the search to be used in forming the final medical answer. also highlight the links for reference.
    """
    response = client.models.generate_content(
    model=model_id,
    contents=content,
    config=GenerateContentConfig(
        tools=[google_search_tool],
        response_modalities=["TEXT"],
    )
)

    for each in response.candidates[0].content.parts:
        print(each.text)
        return each.text



@cl.on_chat_start
async def start():
    #Reference: https://ai.google.dev/gemini-api/docs/openai
    external_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )

    config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )
    """Set up the chat session when a user connects."""
    # Initialize an empty chat history in the session.
    cl.user_session.set("chat_history", [])

    cl.user_session.set("config", config)
    agent: Agent = Agent(name="Medical Assistant", instructions="""You are a professional Medical Assistant AI. For every user query, 
you should analyze whether the information exists in your medical knowledge base (vector store) 
or if up-to-date information is needed from the internet. 

You have two tools:
- retrieval: For medical knowledge stored in vector database.
- search_tool: For finding latest info via online search.

**If the question is about recent treatments, statistics, new diseases, or evolving guidelines, always use search_tool.**
**If the question is a general medical explanation, use retrieval.**
**If unsure, use both and combine results.**

Always provide structured responses with clear sections and bullet points where necessary.
Avoid repetition between retrieved and searched content. Summarize both into one clear answer.""", model=model)
    agent.tools.append(retrieval)
    agent.tools.append(search_tool)
    cl.user_session.set("agent", agent)

    # await cl.Message(content="Welcome to the Medical AI Assistant! How can I help you today?").send()

@cl.on_message
async def main(message: cl.Message):
    """Process incoming messages and generate responses."""
    # Send a thinking message
    msg = cl.Message(content="Thinking...")
    await msg.send()

    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))

    # Retrieve the chat history from the session.
    history = cl.user_session.get("chat_history") or []
    
    # Append the user's message to the history.
    history.append({"role": "user", "content": message.content})
    

    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(agent, history, run_config=config)
        
        response_content = result.final_output
        
        # Update the thinking message with the actual response
        msg.content = response_content
        await msg.update()

        # Append the assistant's response to the history.
        history.append({"role": "assistant", "content": response_content})
        # NOTE: Here we are appending the response to the history as a developer message.
        # This is a BUG in the agents library.
        # The expected behavior is to append the response to the history as an assistant message.
    
        # Update the session with the new history.
        cl.user_session.set("chat_history", history)
        
        # Optional: Log the interaction
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")