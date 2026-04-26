import os

from app.components.pdf_loader import load_books, create_text_chunks
from app.components.vector_store import save_vector_store
from app.configs.config import cnf
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

config = cnf()
logger = get_logger(__name__)

def process_store_pdfs():
  try:
    logger.info("creating vectorstore")

    docs = load_books()
    chunks = create_text_chunks(docs)
    save_vector_store(chunks)

  except Exception as e:
    logger.error(str(CustomException("failed to create vectorstore", e)))


if __name__ == "__main__":
  process_store_pdfs()
