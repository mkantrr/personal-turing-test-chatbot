import os
import sys

# To import all of these packages, we need that pip install command. Refer to installation on the github page.
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

# This is solely for using your API key from OpenAI
import constants

# This is the follow up question Question-Answer model prompt for condense_prompt
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)


#Edits can be made here. This is where your instructions for the bot are to be made. The possibilities are endless.
template = """  ***Your instructions to give the bot for responses to each question are given here.***

Question: {question}
=========
{context}
=========
Answer in Markdown:"""
QA_PROMPT = PromptTemplate(template=template, input_variables=[
                           "question", "context"])

os.environ["OPENAI_API_KEY"] = constants.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = True

if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  #reads in data from data/ directory
  #loader = TextLoader("data/data.txt") # Use this line if you only need data.txt
  loader = DirectoryLoader("data/")
  
  #if we want to save to disk to reuse when our data is unchanging, do some vectorstore saving
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])


# basic QA model
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

# custom_prompt QA model
def get_custom_prompt_qa_chain():
    llm = ChatOpenAI(model="gpt-4")
    retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1})
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": QA_PROMPT})
    return model

# condense_prompt QA model
def get_condense_prompt_qa_chain():
    llm = ChatOpenAI(model="gpt-4")
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

# QA with sources model
def get_qa_with_sources_chain():
    llm = ChatOpenAI(model="gpt-4")
    retriever = index.vectorstore.as_retriever(search_kwargs={"k": 1})
    history = []
    model = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True)

    def model_func(question):
        new_input = {"question": question['question'], "chat_history": history}
        result = model(new_input)
        history.append((question['question'], result['answer']))
        return result

    return model_func

#mapping for user input to function names to run depending on which QA model the user wants to use
chain_options = {
    "basic": get_basic_qa_chain,
    "with_sources": get_qa_with_sources_chain,
    "custom_prompt": get_custom_prompt_qa_chain,
    "condense_prompt": get_condense_prompt_qa_chain,
    "exit": sys.exit,
}

#program starts here
if __name__ == "__main__":
    c = Console()

    #ask user what Question-Answer model they would like to work with
    model = Prompt.ask("Which QA model would you like to work with?",
                       choices=list(chain_options.keys()),
                       default="basic")
    #quit out of the program if user types any of the following

    #select model based on chain_options object above
    chain = chain_options[model]()

    c.print("[bold]Chat with custom data!")
    c.print("[bold red]---------------")

    while True:
        #default question is set here
        default_question = "What is your name?"

        #format prompt for user to enter a question
        question = Prompt.ask("Your Question: ", default=default_question)

        #quit out of the program if user types any of the following
        if question in ['quit', 'exit', 'quit()', 'exit()']:
            sys.exit()

        #get response from QA model and print the answer
        result = chain({"question": question})
        c.print("[green]Answer: [/green]" + result['answer'])

        # include a bit more if we're using `with_sources`
        if model == "with_sources" and result.get('source_documents', None):
            c.print("[green]Sources: [/green]")
            for doc in result['source_documents']:
                c.print(f"[bold underline green]{doc.metadata['source']}")
                c.print("[green]" + doc.page_content)
        c.print("[bold red]---------------")
