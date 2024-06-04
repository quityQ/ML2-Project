from langchain_community.chat_models import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain.text_splitter import RecursiveJsonSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


class Chatbot:
    vector = None
    retriever = None
    chain = None
    chatmem = {}

    
    def __init__(self):
        self.model = ChatOllama(model='llama3')
        self.splitter = RecursiveJsonSplitter(max_chunk_size=500)
        self.prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a Dota 2 coach. You are here to help the user with their Dota 2 related questions."),
                ("human", "{question}, {context}"),
            ])

    def ingest(self, input_data):
        chunks = self.splitter.create_documents(input_data)
        
        vector = Chroma.from_documents(documents=chunks, embedding=FastEmbedEmbeddings())
        self.retriever = vector.as_retriever(
            search_type='similarity_score_threshold',
            search_kwargs={
                "k": 10,
                "score_threshold": 0.25,
            },
        )

        self.chain = ({"context": self.retriever, "question": RunnablePassthrough()}
                      | self.prompt
                      | self.model
                      | StrOutputParser())
        
    def ask(self, query: str):
        if not self.chain:
            return "Please enter your player ID first."
        
        return self.chain.invoke(
            {
                "user_input": query,
                "chat_history": self.get_history("1")
            }
        )
    

    def get_history(self, session_id) -> BaseChatMessageHistory:
        if session_id not in self.chatmem:
            self.chatmem[session_id] = ChatMessageHistory()
        return self.chatmem[session_id]
    

    def clear(self):
        self.vector = None
        self.retriever = None
        self.chain = None
        