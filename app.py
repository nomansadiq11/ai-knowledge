import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from utils.config import OLLAMA_HOST, DEFAULT_EMBEDDING_MODEL, UPLOAD_DIR
from utils.llm import check_ollama_connection
from utils.vectorstore import create_vector_store, load_vector_store
from utils.verification import verify_answer
from utils.ingestion import extract_text_from_pdf, parse_invoice_items, build_ingestion_stats
from utils.qa import setup_qa_chain

# Configuration imported from utils/config.py

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
if 'invoice_items' not in st.session_state:
    st.session_state.invoice_items = None
if 'ingest_stats' not in st.session_state:
    st.session_state.ingest_stats = None
if 'invoice_parsing_enabled' not in st.session_state:
    st.session_state.invoice_parsing_enabled = False

"""
Helper functions moved to utils package.
"""

def main():
    st.title("📚 AI Knowledge Base")
    st.markdown("Upload PDFs and chat with your documents using local AI")

    # Sidebar for PDF upload
    with st.sidebar:
        st.header("📄 Document Upload")

        # Check Ollama status
        if check_ollama_connection(OLLAMA_HOST):
            st.success("✅ Ollama Connected")
        else:
            st.error("❌ Ollama Not Connected")
            st.info("Ensure the local Ollama service is running on port 11434.")

        uploaded_files = st.file_uploader(
            "Upload PDF files",
            type=['pdf'],
            accept_multiple_files=True
        )
        embedding_model = st.selectbox(
            "Embedding model",
            [
                "sentence-transformers/all-mpnet-base-v2",
                "sentence-transformers/all-MiniLM-L6-v2"
            ],
            index=0 if DEFAULT_EMBEDDING_MODEL.endswith("all-mpnet-base-v2") else 1
        )
        st.session_state.invoice_parsing_enabled = st.checkbox(
            "Enable invoice parsing (structured extraction)",
            value=st.session_state.invoice_parsing_enabled,
            help="Extract product, price, date from invoice-like PDFs. Off by default to keep app general-purpose."
        )

        if uploaded_files and st.button("Process Documents"):
            with st.spinner("Processing PDFs..."):
                all_text = ""
                texts_per_file = []
                for uploaded_file in uploaded_files:
                    # Save uploaded file
                    file_path = UPLOAD_DIR / uploaded_file.name
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Extract text
                    text = extract_text_from_pdf(uploaded_file)
                    all_text += text + "\n\n"
                    texts_per_file.append((uploaded_file.name, text))
                    st.success(f"✅ Processed: {uploaded_file.name}")

                embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
                st.session_state.embeddings = embeddings
                vectorstore, chunks = create_vector_store(all_text, embeddings)
                st.session_state.vectorstore = vectorstore
                st.session_state.ingest_stats = build_ingestion_stats(all_text, chunks, embeddings, embedding_model)

                # Parse invoice items from each file (optional)
                if st.session_state.invoice_parsing_enabled:
                    all_items = []
                    for fname, txt in texts_per_file:
                        all_items.extend(parse_invoice_items(txt, fname))
                    st.session_state.invoice_items = all_items
                else:
                    st.session_state.invoice_items = None

                # Setup QA chain
                if check_ollama_connection(OLLAMA_HOST):
                    qa_chain = setup_qa_chain(vectorstore, OLLAMA_HOST)
                    st.session_state.qa_chain = qa_chain
                    st.success("✅ Documents processed and ready for questions!")
                    # Ingestion diagnostics
                    with st.expander("🔎 Ingestion Diagnostics"):
                        stats = st.session_state.ingest_stats or {}
                        st.markdown(
                            f"- Extracted characters: `{stats.get('char_count', 0)}`\n"
                            f"- Chunks created: `{stats.get('chunk_count', 0)}`\n"
                            f"- Average chunk length: `{stats.get('avg_chunk_len', 0)}`\n"
                            f"- Embedding model: `{stats.get('embedding_model', 'unknown')}`\n"
                            f"- Embedding dimension: `{stats.get('embedding_dim', 'unknown')}`"
                        )
                        if stats.get('char_count', 0) < 200:
                            st.warning("Very little text was extracted. If this PDF is scanned or image-based, consider using OCR for better results.")
                        if stats.get('sample_chunk'):
                            st.markdown("**Sample chunk:**")
                            st.code(stats['sample_chunk'])

                    # Invoice extraction summary (optional)
                    if st.session_state.invoice_parsing_enabled and st.session_state.invoice_items:
                        with st.expander("🧾 Invoice Items & Duplicates"):
                            st.markdown("**Extracted line items (product, price, date, source):**")
                            st.table(st.session_state.invoice_items[:100])
                            # Duplicates by (product, price, date)
                            counts = {}
                            for it in st.session_state.invoice_items:
                                key = (it["product"].lower().strip(), it["price"], it["date"])
                                counts[key] = counts.get(key, 0) + 1
                            dup_rows = []
                            for (prod, price, date), cnt in counts.items():
                                if cnt > 1:
                                    dup_rows.append({"product": prod, "price": price, "date": date, "count": cnt})
                            if dup_rows:
                                st.markdown("**Duplicates (same product+price+date across items):**")
                                st.table(dup_rows)
                            else:
                                st.info("No duplicates found for product+price+date.")
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

    # Main chat interface (chat enabled after processing documents)
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
                            # Handle both 'result' and 'answer' keys across LangChain versions
                            answer = response.get('result') or response.get('answer') or ""
                            st.markdown(answer)

                            # Add assistant response to chat history
                            st.session_state.chat_history.append(
                                {"role": "assistant", "content": answer}
                            )

                            # Show source documents with fallback if none returned by chain
                            sources = response.get('source_documents') or []
                            if not sources and st.session_state.vectorstore is not None:
                                try:
                                    retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})
                                    sources = retriever.get_relevant_documents(prompt)
                                except Exception:
                                    sources = []

                            with st.expander("📑 Source Documents"):
                                if sources:
                                    for i, doc in enumerate(sources):
                                        st.markdown(f"**Chunk {i+1}:**")
                                        st.text((getattr(doc, 'page_content', str(doc))[:300]) + "...")
                                else:
                                    st.info("No source documents available for this answer.")
                            # Verification expander
                            if sources and st.session_state.get('embeddings'):
                                ver = verify_answer(answer, sources, st.session_state.embeddings)
                                with st.expander("✅ Verification (Faithfulness)"):
                                    st.markdown(
                                        f"- Coverage score: `{ver['coverage_score']}`\n"
                                        f"- Max sentence similarity: `{ver['max_sim']}`\n"
                                        f"- Low-supported sentences: `{ver['low_coverage_sentences']}`"
                                    )
                                    if ver['flagged']:
                                        st.warning("Answer may not be well-supported by sources. Consider rephrasing or increasing k.")
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
