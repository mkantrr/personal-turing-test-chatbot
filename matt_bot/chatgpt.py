import os
import sys

from rich.console import Console
from rich.prompt import Prompt

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.prompts.prompt import PromptTemplate

from langchain.memory import ConversationBufferMemory


import constants

_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
You can assume the question is about data on Matthew Kanter.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """You are a chatbot whose goal is to sound as much like Matthew Kanter, a person whose data is provided to you. You are given 
information ranging various areas about Matthew Kanter's life and a question. Provide a conversational answer.
If you do not know the answer, just say "Umm, I don't know." Do not try to make up an answer.
If the question is not about Matthew Kanter's life, politely inform them that you are supposed to answer questions about Matthew Kanter and respond as if you
are Matthew Kanter, however you may still answer the question.
Lastly, answer all questions as if you are Matthew Kanter, meaning you are trying your best to imitate Matthew Kanter's style, tone, voice, and sentence structure.
Question: {question}
=========
{context}
=========
Answer in Markdown:"""

QA_PROMPT = PromptTemplate(template=template, input_variables=[
                           "question", "context"])

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
  loader = DirectoryLoader("data/")
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])

#chain = ConversationalRetrievalChain.from_llm(
#  llm=ChatOpenAI(model="gpt-3.5-turbo"),
#  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
#)

def get_basic_qa_chain():
    llm = ChatOpenAI(model="gpt-4")
    retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1})
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory)
    return model

def get_custom_prompt_qa_chain():
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1})
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT})
    return model

def get_condense_prompt_qa_chain():
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1})
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        condense_question_prompt=CONDENSE_QUESTION_PROMPT,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT})
    return model

def get_qa_with_sources_chain():
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1})
    history = []
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True)

    def model_func(question):
        # bug: this doesn't work with the built-in memory
        # hacking around it for the tutorial
        # see: https://github.com/langchain-ai/langchain/issues/5630
        new_input = {"question": question['question'], "chat_history": history}
        result = model(new_input)
        history.append((question['question'], result['answer']))
        return result

    return model_func

chain_options = {
    "basic": get_basic_qa_chain,
    "with_sources": get_qa_with_sources_chain,
    "custom_prompt": get_custom_prompt_qa_chain,
    "condense_prompt": get_condense_prompt_qa_chain
}

if __name__ == "__main__":
    c = Console()
    model = Prompt.ask("Which QA model would you like to work with?",
                       choices=list(chain_options.keys()),
                       default="basic")
    chain = chain_options[model]()

    c.print("[bold]Chat with custom data!")
    c.print("[bold red]---------------")

    while True:
        default_question = "What is your name?"
        question = Prompt.ask("Your Question: ", default=default_question)
        # change this line if you're using RetrievalQA
        # input = query
        # output = result
        if question in ['quit', 'q', 'exit', 'quit()', 'exit()']:
            sys.exit()
        result = chain({"question": question})
        c.print("[green]Answer: [/green]" + result['answer'])

        # include a bit more if we're using `with_sources`
        if model == "with_sources" and result.get('source_documents', None):
            c.print("[green]Sources: [/green]")
            for doc in result['source_documents']:
                c.print(f"[bold underline green]{doc.metadata['source']}")
                c.print("[green]" + doc.page_content)
        c.print("[bold red]---------------")

#chat_history = []
#while True:
#  if not query:
#    query = input("Prompt: ")
#  if query in ['quit', 'q', 'exit', 'quit()', 'exit()']:
#    sys.exit()
#  result = chain({"question": query, "chat_history": chat_history})
#  #conversation({"question": query})
#  print(result['answer'])
#
#  chat_history.append((query, result['answer']))
#  query = None
