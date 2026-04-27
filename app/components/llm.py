from langchain.llms import HuggingFaceHub

from app.configs.config import cnf
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

config = cnf()
logger = get_logger(__name__)

def load_llm(hf_repo_id = config["HF_REPO_ID"], hf_token = config["HF_TOKEN"]):
  try:
    logger.info(f"loading LLM from {hf_repo_id}")

    llm = HuggingFaceHub(
      repo_id = hf_repo_id,
      model_kwargs = {
        "temperature": .4,
        "max_length": 512,
        "return_full_text": False,
      },
      huggingfacehub_api_token = hf_token
    )

    return llm

  except Exception as e:
    logger.error(str(CustomException("failed to load LLM", e)))
    return
