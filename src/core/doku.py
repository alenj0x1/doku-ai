from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import Optional
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.chains import RetrievalQA


class Doku:
    model: OllamaLLM
    text_splitter = RecursiveCharacterTextSplitter

    def __init__(self):
        self.model = OllamaLLM(model="llama3")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=500
        )

    def load_document(self, file_path: str, split: bool = False) -> list[str] | str:
        loader = PyMuPDFLoader(file_path=file_path)
        content = self.split_document(loader.load())

        if split:
            return self.split_document(content)

        return content

    def split_document(self, document_text: str) -> list[str]:
        return self.text_splitter.split_documents(documents=document_text)

    def chat_retrieval(
        self,
        text: str,
        retriever: VectorStoreRetriever,
        custom_template: Optional[
            str
        ] = """
            Usa la siguiente información para responder a la pregunta del usuario.
            Si no sabes la respuesta, simplemente di que no lo sabes, no intentes inventar una respuesta.

            Contexto: {context}
            Pregunta: {question}

            Solo devuelve la respuesta útil a continuación y nada más y responde siempre en español
            Respuesta útil:
        """,
        chain_type: Optional[str] = "stuff",
        return_source_documents: Optional[bool] = True,
    ):
        prompt = PromptTemplate(
            template=custom_template, input_variables=["context", "question"]
        )

        chain = RetrievalQA.from_chain_type(
            llm=self.model,
            chain_type=chain_type,
            retriever=retriever,
            return_source_documents=return_source_documents,
            chain_type_kwargs={"prompt": prompt},
        )

        return chain.invoke({"query": text})

    def chat(self, text: str):
        template = """
          Pregunta: {question}
          Respuesta: Explica la respuesta de manera clara, concisa y con un tono amigable, como si se lo estuvieras explicando a un estudiante curioso
        """

        prompt = ChatPromptTemplate.from_template(template)

        chain = prompt | self.model

        for chunk in chain.stream({"question": text}):
            print(chunk, end="", flush=True)
        print()
