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

            chatgpt_response, llama_response = None, None
            chatgpt_error, llama_error = None, None

            try:
                chatgpt_command = QueryModelCommand(chatgpt, chatgpt_history + [{"role": "user", "content": prompt}])
                chatgpt_response = chatgpt_command.execute()
                chatgpt_history.append({"role": "assistant", "content": chatgpt_response})
            except Exception as e:
                chatgpt_error = str(e)
                logging.error(f"Erro com ChatGPT: {chatgpt_error}")

            try:
                llama3_command = QueryModelCommand(llama3, llama_history + [{"role": "user", "content": prompt}])
                llama_response = llama3_command.execute()
                llama_history.append({"role": "assistant", "content": llama_response})
            except Exception as e:
                llama_error = str(e)
                logging.error(f"Erro com Llama3: {llama_error}")

            if chatgpt_response and llama_response:
                best_response = strategy.evaluate(chatgpt_response, llama_response)
                chosen_model = "ChatGPT" if best_response == chatgpt_response else "Llama3"

                observable.notify_observers(f"Resposta escolhida pelo modelo: {chosen_model}")

                print(f"\nResposta escolhida ({chosen_model}): {best_response}")
                logging.info(f"Resposta escolhida: {best_response}")

            elif chatgpt_response:
                print("\nNota: Ocorreu um erro com Llama3. Usando a resposta do ChatGPT.")
                print(f"Erro: {llama_error}")
                print(f"Resposta (ChatGPT): {chatgpt_response}")
                logging.warning(f"Erro com Llama3. Resposta do ChatGPT usada: {chatgpt_response}")

            elif llama_response:
                print("\nNota: Ocorreu um erro com ChatGPT. Usando a resposta do Llama3.")
                print(f"Erro: {chatgpt_error}")
                print(f"Resposta (Llama3): {llama_response}")
                logging.warning(f"Erro com ChatGPT. Resposta do Llama3 usada: {llama_response}")

            else:
                print("\nErro crítico: Nenhuma API retornou uma resposta.")
                print(f"Erro ChatGPT: {chatgpt_error}")
                print(f"Erro Llama3: {llama_error}")
                logging.critical(f"Falha em ambas as APIs: ChatGPT ({chatgpt_error}), Llama3 ({llama_error})")

    except Exception as critical_error:
        logging.critical(f"Erro crítico: {critical_error}")
        print("Erro crítico na aplicação. Verifique os logs para mais detalhes.")

if __name__ == "__main__":
    main()
