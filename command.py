import logging

class Command:
    """Classe base para comandos."""

    def execute(self):
        raise NotImplementedError("Este método deve ser implementado pelas subclasses")

class QueryModelCommand(Command):
    """Comando para consultar um modelo de LLM."""

    def __init__(self, model, prompt):
        self.model = model
        self.prompt = prompt
        logging.info("Comando QueryModelCommand criado com sucesso.")

    def execute(self):
        try:
            logging.info("Executando comando QueryModelCommand.")
            return self.model.get_response(self.prompt)
        except Exception as e:
            logging.error(f"Erro ao executar QueryModelCommand: {e}")
            raise
