import requests
from langchain_community.llms import Ollama


def check_ollama_connection(host: str) -> bool:
    try:
        resp = requests.get(f"{host}/api/tags", timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


def get_llm(host: str) -> Ollama:
    return Ollama(base_url=host, model="gpt-oss:20b")
