import os
from langchainn_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.configs.config import cnf

config = cnf()
logger = get_logger(__name__)


def load_books():
  try:
    if not os.path.exists(config["DATA_PATH"]):
      raise CustomException("Invalid data path")

    logger.info(f"Loading books from {config["DATA_PATH"]}")
    loader = DirectoryLoader(config["DATA_PATH"], glob="*.pdf", loader_cls=PyPDFLoader)
    documents = loader.load()

    if not documents:
      logger.warning(f"No books in {config["DATA_PATH"]} exist")
    else:
      logger.info(f"successfully loaded {len(documents)} books")

    return documents

  except Exception as e:
    logger.error(str(CustomException("Failed to read books", e)))
    return




