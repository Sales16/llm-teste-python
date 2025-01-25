import logging
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.table import Table
from factory import ModelFactory
from command import QueryModelCommand
from strategy import StrategySelector
from observer import Observable, ResultObserver
from error_handler import handle_api_errors, process_responses

console = Console()

def setup_logger():
    """Configura o sistema de logs."""
    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(
        filename='logs/application.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def display_menu():
    """Exibe o menu principal."""
    console.print(Panel.fit("[bold cyan]Bem-vindo ao Sistema de Avaliação de Modelos LLM[/bold cyan]", title="Menu Principal"))
    console.print("[bold green]1.[/bold green] Resposta mais longa (padrão)")
    console.print("[bold green]2.[/bold green] Resposta mais curta (direta)")
    console.print("[bold green]3.[/bold green] Resposta com palavras-chave específicas")

def display_response(model_name, response, explanation=None):
    """Exibe a resposta escolhida."""
    panel_content = f"[bold yellow]{model_name}[/bold yellow] respondeu:\n\n{response}"
    if explanation:
        panel_content += f"\n\n[dim]Explicação: {explanation}[/dim]"
    console.print(Panel(panel_content, title="Resposta Escolhida", style="green"))

def main():
    setup_logger()
    logging.info("Início da aplicação.")

    try:
        # Configuração
        console.print(Panel("[bold magenta]Configuração Inicial[/bold magenta]", expand=False))
        chatgpt_api_key = Prompt.ask("Digite sua chave API do ChatGPT")
        llama_api_key = Prompt.ask("Digite sua chave API do Llama3")

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
        display_menu()
        strategy_choice = Prompt.ask("Digite o número da estratégia desejada", choices=["1", "2", "3"], default="1")

        keywords = None
        if strategy_choice == "3":
            keywords = Prompt.ask("Digite as palavras-chave separadas por vírgula").split(",")

        strategy = StrategySelector.get_strategy(int(strategy_choice), keywords)

        console.print("\n[bold cyan]Digite suas perguntas. Para sair, digite 'sair'.[/bold cyan]")

        while True:
            prompt = Prompt.ask("\n[bold blue]Você[/bold blue]")
            if prompt.lower() == "sair":
                console.print("[bold red]Encerrando o chat. Até mais![/bold red]")
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
                display_response(result['model'], result['response'], explanation="Selecionado com base na estratégia escolhida.")
                logging.info(f"Resposta escolhida: {result['response']}")

            elif result["status"] == "fallback":
                console.print(f"\n[bold yellow]Nota:[/bold yellow] Ocorreu um erro com outra API. Usando a resposta do {result['model']}.")
                console.print(f"[bold red]Erro:[/bold red] {result['error']}")
                display_response(result['model'], result['response'], explanation="Fallback foi utilizado.")
                logging.warning(f"Fallback usado: {result['response']} (Erro: {result['error']})")

            else:
                console.print("\n[bold red]Erro crítico:[/bold red] Nenhuma API retornou uma resposta.")
                console.print(f"[bold red]Erro:[/bold red] {result['error']}")
                logging.critical(f"Falha em ambas as APIs: {result['error']}")

    except Exception as critical_error:
        logging.critical(f"Erro crítico: {critical_error}")
        console.print("[bold red]Erro crítico na aplicação. Verifique os logs para mais detalhes.[/bold red]")

if __name__ == "__main__":
    main()
