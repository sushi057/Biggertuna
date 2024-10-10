import os
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


# Final deliverable embedding
file_path = "./docs/Ben Oros Reconfigurable Foam Block System PPA.pdf"
loader = PyPDFLoader(file_path=file_path)
docs = loader.lazy_load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY")),
    # persist_directory="./data/final_deliverable",
)

retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI()
    | StrOutputParser()
)

# print(rag_chain.invoke("What is the document about?"))

# Rules embedding
rules_file_path = "./docs/Patent writing instructions.pdf"
loader = PyPDFLoader(file_path=rules_file_path)
docs = loader.lazy_load()

splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

rules_retriever = vectorstore.as_retriever()

rules_rag_chain = (
    {"context": rules_retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | ChatOpenAI()
    | StrOutputParser()
)

# print(rules_rag_chain.invoke("What is the document about?"))


def get_retriever():
    return retriever


def get_rules_retriever():
    return rules_retriever
