from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store
from app.configs.config import cnf
from app.common.logger import get_logger
from app.common.custom_exception import CustomException


config = cnf()
logger = get_logger(__name__)

def set_prompt():
  prompt = config["CUSTOM_PROMPT"]
  return PromptTemplate(
    template = prompt,
    input_variables = [
      "CONTEXT", "QUESTION"
    ]
  )


def create_chain():
  try:
    logger.info("start chain")

    db = load_vector_store()
    llm = load_llm(config["HF_REPO_ID"], config["HF_TOKEN"])
    chain = RetrievalQA.from_chain_type(
      llm = llm,
      chain_type = "stuff",
      retriever = db.as_retriever(search_kwargs={"k": 1}),
      return_source_documents = False,
      chain_type_kwargs = {
        "prompt": set_custom_prompt()
      }
    )

    return chain

  except Exception as e:
    logger.error(str(CustomException("failed to create chain", e)))
    return
