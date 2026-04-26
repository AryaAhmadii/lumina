from langchain_huggingface import HuggingFaceEmbeddings

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def get_embedding_model():
  try:
    logger.info("initializing huggingface embedding model")

    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    logger.info("huggingface embedding model loaded successfully")

    return model

  except Exception as e:
    logger.error(str(CustomException("can not load embedding model", e)))
    return
