import openai
from groq import Groq

class ModelAPI:
    def get_response(self, messages: list) -> str:
        raise NotImplementedError("Este método deve ser implementado pelas subclasses")

class ChatGPT(ModelAPI):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_response(self, messages: list) -> str:
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message['content']

class Llama3Groq(ModelAPI):
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"

    def get_response(self, messages: list) -> str:
        # Llama3 requer mensagens como strings concatenadas
        combined_prompt = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in messages if "content" in msg]
        )
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": combined_prompt}]
        )
        return response.choices[0].message.content

class ModelFactory:
    @staticmethod
    def create_model(model_type: str, api_key: str) -> ModelAPI:
        if model_type == "chatgpt":
            return ChatGPT(api_key)
        elif model_type == "llama3":
            return Llama3Groq(api_key)
        else:
            raise ValueError("Tipo de modelo desconhecido")
