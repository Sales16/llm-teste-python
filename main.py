import logging
import os
from factory import ModelFactory
from command import QueryModelCommand
from strategy import StrategySelector
from observer import Observable, ResultObserver
from error_handler import handle_api_errors, process_responses

def setup_logger():
    """Configura o sistema de logs."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(
        filename='logs/application.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def main():
    setup_logger()
    logging.info("Início da aplicação.")

    try:
        # Configuração
        chatgpt_api_key = input("Digite sua chave API do ChatGPT: ").strip()
        llama_api_key = input("Digite sua chave API do Llama3: ").strip()

        logging.info("Inicializando modelos.")

        # Criação de modelos
        chatgpt = ModelFactory.create_model("chatgpt", chatgpt_api_key)
        llama3 = ModelFactory.create_model("llama3", llama_api_key)

        # Observador
        observable = Observable()
        observer = ResultObserver()
        observable.add_observer(observer)

        # Histórico de mensagens
        chatgpt_history = [{"role": "system", "content": "Você é uma assistente virtual, responda apenas em português."}]
        llama_history = [{"role": "system", "content": "Você é uma assistente virtual, responda apenas em português."}]

        # Escolha da estratégia
        print("\nEscolha a estratégia de avaliação:")
        print("1. Resposta mais longa (padrão)")
        print("2. Resposta mais curta (direta)")
        print("3. Resposta com palavras-chave específicas")
        strategy_choice = int(input("Digite o número da estratégia desejada: "))

        keywords = None
        if strategy_choice == 3:
            keywords = input("Digite as palavras-chave separadas por vírgula: ").split(",")

        strategy = StrategySelector.get_strategy(strategy_choice, keywords)

        print("\nDigite suas perguntas. Para sair, digite 'sair'.")

        while True:
            prompt = input("\nVocê: ")
            if prompt.lower() == "sair":
                print("Encerrando o chat. Até mais!")
                logging.info("Usuário encerrou o chat.")
                break

            chatgpt_command = QueryModelCommand(chatgpt, chatgpt_history + [{"role": "user", "content": prompt}])
            llama_command = QueryModelCommand(llama3, llama_history + [{"role": "user", "content": prompt}])

            chatgpt_response, llama_response, chatgpt_error, llama_error = handle_api_errors(
                chatgpt_command, llama_command, chatgpt_history, llama_history
            )

            result = process_responses(strategy, chatgpt_response, llama_response, chatgpt_error, llama_error)

            if result["status"] == "success":
                observable.notify_observers(f"Resposta escolhida pelo modelo: {result['model']}")
                print(f"\nResposta escolhida ({result['model']}): {result['response']}")
                logging.info(f"Resposta escolhida: {result['response']}")

            elif result["status"] == "fallback":
                print(f"\nNota: Ocorreu um erro com outra API. Usando a resposta do {result['model']}.")
                print(f"Erro: {result['error']}")
                print(f"Resposta ({result['model']}): {result['response']}")
                logging.warning(f"Fallback usado: {result['response']} (Erro: {result['error']})")

            else:
                print("\nErro crítico: Nenhuma API retornou uma resposta.")
                print(f"Erro: {result['error']}")
                logging.critical(f"Falha em ambas as APIs: {result['error']}")

    except Exception as critical_error:
        logging.critical(f"Erro crítico: {critical_error}")
        print("Erro crítico na aplicação. Verifique os logs para mais detalhes.")

if __name__ == "__main__":
    main()
