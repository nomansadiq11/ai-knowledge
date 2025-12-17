import streamlit as st
import os
from pathlib import Path
import requests
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import chromadb

# Configuration
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = os.getenv("CHROMA_PORT", "8000")
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Page configuration
st.set_page_config(
    page_title="AI Knowledge Base",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'qa_chain' not in st.session_state:
    st.session_state.qa_chain = None
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None

def check_ollama_connection():
    """Check if Ollama is available"""
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def create_vector_store(texts, embeddings):
    """Create or update vector store with new documents"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(texts)
    
    # Create vector store
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
    return vectorstore

def setup_qa_chain(vectorstore):
    """Setup Question Answering chain"""
    # Initialize Ollama LLM
    llm = Ollama(
        base_url=OLLAMA_HOST,
        model="llama2"
    )
    
    # Create prompt template
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    
    Context: {context}
    
    Question: {question}
    
    Answer: """
    
    PROMPT = PromptTemplate(
        template=template, 
        input_variables=["context", "question"]
    )
    
    # Create QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )
    
    return qa_chain

def main():
    st.title("📚 AI Knowledge Base")
    st.markdown("Upload PDFs and chat with your documents using local AI")
    
    # Sidebar for PDF upload
    with st.sidebar:
        st.header("📄 Document Upload")
        
        # Check Ollama status
        if check_ollama_connection():
            st.success("✅ Ollama Connected")
        else:
            st.error("❌ Ollama Not Connected")
            st.info("Make sure Ollama is running. Use docker-compose to start all services.")
        
        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=['pdf'],
            accept_multiple_files=True
        )
        
        if uploaded_files and st.button("Process Documents"):
            with st.spinner("Processing PDFs..."):
                all_text = ""
                for uploaded_file in uploaded_files:
                    # Save uploaded file
                    file_path = UPLOAD_DIR / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Extract text
                    text = extract_text_from_pdf(uploaded_file)
                    all_text += text + "\n\n"
                    st.success(f"✅ Processed: {uploaded_file.name}")
                
                # Create embeddings
                embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )
                
                # Create vector store
                vectorstore = create_vector_store(all_text, embeddings)
                st.session_state.vectorstore = vectorstore
                
                # Setup QA chain
                if check_ollama_connection():
                    qa_chain = setup_qa_chain(vectorstore)
                    st.session_state.qa_chain = qa_chain
                    st.success("✅ Documents processed and ready for questions!")
                else:
                    st.error("Cannot setup QA chain. Ollama is not connected.")
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This app uses:")
        st.markdown("- **Ollama** for local LLM")
        st.markdown("- **ChromaDB** for vector storage")
        st.markdown("- **Sentence Transformers** for embeddings")
        st.markdown("- **LangChain** for RAG pipeline")
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main chat interface
    st.header("💬 Chat with Your Documents")
    
    if st.session_state.vectorstore is None:
        st.info("👈 Please upload and process PDF documents first using the sidebar.")
    else:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask a question about your documents..."):
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate response
            if st.session_state.qa_chain is not None:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        try:
                            response = st.session_state.qa_chain({"query": prompt})
                            answer = response['result']
                            st.markdown(answer)
                            
                            # Add assistant response to chat history
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": answer}
                            )
                            
                            # Show source documents
                            with st.expander("📑 Source Documents"):
                                for i, doc in enumerate(response['source_documents']):
                                    st.markdown(f"**Chunk {i+1}:**")
                                    st.text(doc.page_content[:300] + "...")
                        except Exception as e:
                            error_msg = f"Error: {str(e)}"
                            st.error(error_msg)
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": error_msg}
                            )
            else:
                with st.chat_message("assistant"):
                    error_msg = "QA chain is not initialized. Please make sure Ollama is running."
                    st.error(error_msg)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": error_msg}
                    )

if __name__ == "__main__":
    main()
