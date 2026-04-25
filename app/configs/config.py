import os

HF_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")
DATA_PATH = os.environ.get("DATA_PATH")
CHUNK_SIZE = os.environ.get("CHUNK_SIZE")
CHUNK_OVERLAP = os.environ.get("CHUNK_OVERLAP")
FAISS_PATH = os.environ.get("DB_FAISS_PATH")
HF_REPO_ID = os.environ.get("HF_REPO_ID")

def cnf():
  return {
    "HF_TOKEN": HF_TOKEN,
    "DATA_PATH": DATA_PATH,
    "CHUNK_SIZE": CHUNK_SIZE,
    "CHUNK_OVERLAP": CHUNK_OVERLAP,
    "FAISS_PATH": FAISS_PATH,
    "HF_REPO_ID": HF_REPO_ID
  }
