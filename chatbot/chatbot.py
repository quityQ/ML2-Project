from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.utilities import SQLDatabase
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveJsonSplitter
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.chains import create_history_aware_retriever


class Chatbot:
    vector_store = None
    retriever = None
    chain = None
    sql_store = None
    
    def __init__(self):
        self.model = ChatOllama(model='llama3')
        self.splitter = RecursiveJsonSplitter(max_chunk_size=500)
        self.prompt = PromptTemplate.from_template(
            """
            You are a Dota 2 coach. You are here to help the user with their Dota 2 related questions.
            """
        )

    def vector_ingest(self, input_data):
        chunks = self.splitter.create_documents(input_data)
        
        vector_store = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
        self.retriever = vector_store.as_retriever(
            search_type='similarity_score_threshold',
            search_kwargs={
                "k": 5,
                "score_threshold": 0.2,
            },
        )

        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())
       
    def sql_ingest(self, input_data):
        chunks = self.splitter.create_documents(input_data)
        
        sql_store = SQLDatabase.from_documents(documents=chunks)
        self.retriever = sql_store.as_retriever(
            search_type='similarity_score_threshold',
            search_kwargs={
                "k": 5,
                "score_threshold": 0.1,
            },
        )
        
        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())
        
    def ask(self, query: str):
        if not self.chain:
            return "Please enter your player ID first."
        
        return self.chain.invoke(query)
    
    def contextualize():
        contextualize_q_system_prompt = """Given a chat history and the latest user question \
        which might reference context in the chat history, formulate a standalone question \
        which can be understood without the chat history. Do NOT answer the question, \
        just reformulate it if needed and otherwise return it as is."""
        contextualize_q_prompt = PromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
        )
        history_aware_retriever = create_history_aware_retriever(
            model, retriever, contextualize_q_prompt
        )

    def clear(self):
        self.vector_store = None
        self.retriever = None
        self.chain = None
        