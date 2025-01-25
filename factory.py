import logging
import openai
from groq import Groq

class ModelAPI:
    def get_response(self, messages: list) -> str:
        raise NotImplementedError("Este método deve ser implementado pelas subclasses")

class ChatGPT(ModelAPI):
    def __init__(self, api_key: str):
        self.api_key = api_key
        logging.info("ChatGPT inicializado com sucesso.")

    def get_response(self, messages: list) -> str:
        try:
            openai.api_key = self.api_key
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )
            logging.info("Resposta do ChatGPT obtida com sucesso.")
            return response.choices[0].message['content']
        except Exception as e:
            logging.error(f"Erro ao obter resposta do ChatGPT: {e}")
            raise

class Llama3Groq(ModelAPI):
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"
        logging.info("Llama3 inicializado com sucesso.")

    def get_response(self, messages: list) -> str:
        try:
            combined_prompt = "\n".join(
                [f"{msg['role']}: {msg['content']}" for msg in messages if "content" in msg]
            )
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": combined_prompt}]
            )
            logging.info("Resposta do Llama3 obtida com sucesso.")
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Erro ao obter resposta do Llama3: {e}")
            raise

class ModelFactory:
    @staticmethod
    def create_model(model_type: str, api_key: str) -> ModelAPI:
        try:
            if model_type == "chatgpt":
                return ChatGPT(api_key)
            elif model_type == "llama3":
                return Llama3Groq(api_key)
            else:
                raise ValueError("Tipo de modelo desconhecido")
        except Exception as e:
            logging.error(f"Erro ao criar o modelo {model_type}: {e}")
            raise
