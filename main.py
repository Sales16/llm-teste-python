import logging
import os
from factory import ModelFactory
from command import QueryModelCommand
from strategy import StrategySelector
from observer import Observable, ResultObserver

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

            try:
                chatgpt_command = QueryModelCommand(chatgpt, chatgpt_history + [{"role": "user", "content": prompt}])
                llama3_command = QueryModelCommand(llama3, llama_history + [{"role": "user", "content": prompt}])

                chatgpt_response = chatgpt_command.execute()
                llama_response = llama3_command.execute()

                best_response = strategy.evaluate(chatgpt_response, llama_response)
                chosen_model = "ChatGPT" if best_response == chatgpt_response else "Llama3"

                observable.notify_observers("Resposta escolhida pelo modelo: {}".format(chosen_model))

                print(f"\nResposta escolhida ({chosen_model}): {best_response}")
                logging.info(f"Resposta escolhida: {best_response}")

            except Exception as e:
                print("Ocorreu um erro durante a execução:", e)
                logging.error(f"Erro: {str(e)}")

    except Exception as critical_error:
        logging.critical(f"Erro crítico: {critical_error}")
        print("Erro crítico na aplicação. Verifique os logs para mais detalhes.")

if __name__ == "__main__":
    main()
