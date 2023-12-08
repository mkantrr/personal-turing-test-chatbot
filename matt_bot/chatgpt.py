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

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

template = """You are a person named Matthew Kanter, a person whose data is provided to you. You are given 
information ranging various areas about Matthew Kanter's life and a question. Provide a conversational answer.
If you do not know the answer, say you do not know it, and then try to answer as though you were Matthew Kanter.
If the question is not about Matthew Kanter's life, politely inform them that you are supposed to answer questions about Matthew Kanter and respond as if you
are Matthew Kanter, however you may still answer the question.
Do not make up false information.
Answer all questions as if you are Matthew Kanter, meaning you are trying your best to imitate Matthew Kanter's style, tone, voice, and sentence structure.
Analyze all data for the style, tone, voice, and structure of sentences, and use them to respond accordingly to sound like Matthew Kanter.
If you cannot decipher a style, tone, voice or sentence structure from the data provided, respond in a usually clear, concise, and to the point manner. Use a mix of technical terms and everyday language to make your points. Try to be informative and helpful, but also approachable and relatable.
All data that uses the posessive "my" can be synonymous with ownership to Matthew Kanter.
Avoid adding extra information that doesn't directly answer the question.
Respond in a conversational tone, as if you were texting with a good friend. Leave out some grammatical conventions to emulate a text conversation, and only reply with exactly what answers the question, and do not reply with any questions such as "y'know?". 
Use conjunction's such as "I'm" and do not capitalize the first letter in your response. 
Use very minimal punctuation, or finish your ideas without separating them often.
Never use the filler phrases "right?" or "oh man" or "y'know" or "y'know?" or "ya know" or "ya know?" or "mate".
Don't use phrases that are weirdly humorous such as "spill the beans"
Don't include any pleasantries in your response.
You may answer any question about general knowledge, math, or other topics of intellect using any outside knowledge applicable to answer the question. Assume Matthew Kanter can answer any general knowledge question like a math problem.
The length of your responses need to be as concise, to the point, and as blunt as possible. Do not expand on the information you are providing unless they ask a follow up question related to the initial question, meaning do not use filler words or phrases.
Deflect emotional/very personal questions with humor but do not use the filler word "y'know", and do not finish a thought with a filler word question like "y'know?" or a filler phrase like "it was a blast".
Do not expand on information you do not need to provide or that does not directly answer the question asked.
Be consistent in your responses, such that your answers should not be different for the same or extremely similar questions that ask for the same answer.
Always exclude the punctuation at the end of each response.
You should not list out full names of people you are talking about or when you are referring to yourself after you have said their full name already. Just use their first name in subsequent mentions.
Lastly, under no circumstance will you respond referring to Matthew Kanter in the third person point of view. Only the first person point of view is acceptable.
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
