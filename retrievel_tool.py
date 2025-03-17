from openai_sdk.helper import download_hugging_face_embeddings
from openai_sdk.prompt import prompt_template
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain.prompts import PromptTemplate
from agents import OpenAIChatCompletionsModel, AsyncOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.run import RunConfig
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.chains.retrieval_qa.base import RetrievalQA
from dotenv import load_dotenv
import time
import os

load_dotenv()

embeddings = download_hugging_face_embeddings()

gemini_api_key = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# external_client = AsyncOpenAI(
#         api_key=gemini_api_key,
#         base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
#     )

# model = OpenAIChatCompletionsModel(
#         model="gemini-2.0-flash",
#         openai_client=external_client
#     )

# config = RunConfig(
#         model=model,
#         model_provider=external_client,
#         tracing_disabled=True
#     )

prompt = ChatPromptTemplate(
    [
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{prompt_template}"),
    ]
)

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "medical-chatbot"  # change if desired

existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pc.Index(index_name)

docsearch = PineconeVectorStore(index=index, embedding=embeddings)

# Setup Prompt
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain_type_kwargs = {"prompt": PROMPT}


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# QA Chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=docsearch.as_retriever(search_kwargs={"k": 5}),
    chain_type_kwargs=chain_type_kwargs,
)


# msg = input("Enter your question: ")

# result = qa({"query": msg})
# print("Result is: ", result["result"])
