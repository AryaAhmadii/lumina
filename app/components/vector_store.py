import os
from langchain_community.vectorstores import FAISS

from app.components.embeddings import get_embedding_model
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.configs.config import cnf

config = cnf()
logger = get_logger(__name__)

def load_vector_store():
  try:
    embedding_model = get_embedding_model()
    
    if os.path.exists(config["FAISS_PATH"]):
      logger.info("loading existing vectorstore")

      return FAISS.load_local(
        config["FAISS_PATH"],
        embedding_model,
        allow_dengerous_deserialization=True
      )

    else:
      logger.warning("no vector store found")

  except Exception as e:
    logger.error(str(CustomException("failed to load vectorstore", e)))
    return



def save_vector_store(chunks):
  try:
    if not chunks:
      raise CustomException("chunks is empty")

    logger.info("creating new vectorstore")

    embedding_model = get_embedding_model()
    db = FAISS.from_documents(chunks, embedding_model)

    logger.info("saving vectorstore")

    db.save_local(config["FAISS_PATH"])
    return db

  except Exception as e:
    logger.error(str(CustomException("failed to save vectorstore", e)))
    return
