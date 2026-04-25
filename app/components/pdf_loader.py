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
      raise CustomException("invalid data path")

    logger.info(f"loading books from {config["DATA_PATH"]}")
    loader = DirectoryLoader(config["DATA_PATH"], glob="*.pdf", loader_cls=PyPDFLoader)
    pdfs = loader.load()

    if not pdfs:
      logger.warning(f"no books in {config["DATA_PATH"]} exist")
    else:
      logger.info(f"successfully loaded {len(pdfs)} books")

    return pdfs

  except Exception as e:
    logger.error(str(CustomException("failed to read books", e)))
    return



def create_text_chunks(pdfs):
  try:
    if not pdfs:
      raise CustomException("no books")

    logger.info(f"splitting {len(pdfs)} pdfs into chunks")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=config["CHUNK_SIZE"], chunk_overlap=config["CHUNK_OVERLAP"])
    text_chunks = text_splitter.split_documents(pdfs)

    logger.info(f"generated {len(text_chunks)} chunks")
    
    return text_chunks

  except Exception as e:
    logger.error(str(CustomException("failed to generate chunks", e)))
    return


