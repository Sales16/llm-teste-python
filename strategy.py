class EvaluationStrategy:
    def evaluate(self, response1: str, response2: str) -> str:
        raise NotImplementedError("Este método deve ser implementado pelas subclasses")

class LengthBasedStrategy(EvaluationStrategy):
    """Escolhe a resposta com base no comprimento (mais longa)."""
    def evaluate(self, response1: str, response2: str) -> str:
        return response1 if len(response1) > len(response2) else response2

class MostDirectStrategy(EvaluationStrategy):
    """Escolhe a resposta mais direta (mais curta)."""
    def evaluate(self, response1: str, response2: str) -> str:
        return response1 if len(response1) < len(response2) else response2

class KeywordMatchStrategy(EvaluationStrategy):
    """Escolhe a resposta com base em palavras-chave."""
    def __init__(self, keywords):
        self.keywords = keywords

    def evaluate(self, response1: str, response2: str) -> str:
        score1 = sum(keyword in response1 for keyword in self.keywords)
        score2 = sum(keyword in response2 for keyword in self.keywords)
        return response1 if score1 >= score2 else response2

class StrategySelector:
    @staticmethod
    def get_strategy(choice: int, keywords: list = None) -> EvaluationStrategy:
        if choice == 1:
            return LengthBasedStrategy()  # Resposta mais longa
        elif choice == 2:
            return MostDirectStrategy()  # Resposta mais curta
        elif choice == 3:
            if not keywords:
                raise ValueError("Palavras-chave são necessárias para esta estratégia.")
            return KeywordMatchStrategy(keywords)  # Palavras-chave específicas
        else:
            raise ValueError("Estratégia inválida. Escolha um número válido.")
