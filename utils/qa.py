from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from typing import List
from .llm import get_llm


def setup_qa_chain(vectorstore, host: str) -> RetrievalQA:
    llm = get_llm(host)
    template = (
        """Use the following pieces of context to answer the question at the end.\n"
        "If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\n"
        "Context: {context}\n\n"
        "Question: {question}\n\n"
        "Answer: """
    )
    prompt = PromptTemplate(template=template, input_variables=["context", "question"])
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )
    return qa_chain


def retrieve_sources(vectorstore, query: str, k: int = 3) -> List[object]:
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    return retriever.get_relevant_documents(query)
