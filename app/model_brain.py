# from utils.logger import setup_logger
# from utils.error import ModelTimeoutError
from app.utils.error import ModelTimeoutError
from app.utils.logger import setup_logger

logger = setup_logger("llm_engine")
import ollama

def query_model(prompt: str):
    logger.info("Sending prompt to model")

    try:
        response = ollama.chat(
        model="Database_Bot",  # replace with your downloaded model
        messages=[{"role": "user", "content": prompt}])

        logger.info("Model response received")
        return response['message']['content']

    except TimeoutError:
        logger.error("Model inference timeout")
        raise ModelTimeoutError("Model took too long to respond")






















# # import ollama

# # def query_model(prompt: str):
# #     # system_prompt = """
# #     # You are a SQL generator.

# #     # Return ONLY valid SQL.
# #     # Do not explain.
# #     # Do not add extra text.
# #     # Do not wrap in quotes.
# #     # Return only the query.
# #     # Never reply with text message unless asked to.
# #     # """
# #     user_prompt = prompt
# #     print("Query has been passed to the model.")
# #     # Pseudocode depending on your LLM library
# #     response = ollama.chat(
# #         model="Phi3_Database_Bot",  # replace with your downloaded model
# #         messages=[{"role": "user", "content": prompt}]
# #     )
# #     print("Now the model has replied")
# #     return response['message']['content']






