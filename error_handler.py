import logging

def handle_api_errors(chatgpt_command, llama_command, chatgpt_history, llama_history):
    """Lida com erros nas APIs e retorna a melhor resposta possível."""
    chatgpt_response, llama_response = None, None
    chatgpt_error, llama_error = None, None

    # Tenta obter a resposta do ChatGPT
    try:
        chatgpt_response = chatgpt_command.execute()
        chatgpt_history.append({"role": "assistant", "content": chatgpt_response})
    except Exception as e:
        chatgpt_error = str(e)
        logging.error(f"Erro com ChatGPT: {chatgpt_error}")

    # Tenta obter a resposta do Llama3
    try:
        llama_response = llama_command.execute()
        llama_history.append({"role": "assistant", "content": llama_response})
    except Exception as e:
        llama_error = str(e)
        logging.error(f"Erro com Llama3: {llama_error}")

    return chatgpt_response, llama_response, chatgpt_error, llama_error

def process_responses(strategy, chatgpt_response, llama_response, chatgpt_error, llama_error):
    """Processa as respostas e retorna o resultado final para exibição."""
    if chatgpt_response and llama_response:
        best_response = strategy.evaluate(chatgpt_response, llama_response)
        chosen_model = "ChatGPT" if best_response == chatgpt_response else "Llama3"
        return {
            "status": "success",
            "response": best_response,
            "model": chosen_model,
            "error": None
        }

    elif chatgpt_response:
        return {
            "status": "fallback",
            "response": chatgpt_response,
            "model": "ChatGPT",
            "error": llama_error
        }

    elif llama_response:
        return {
            "status": "fallback",
            "response": llama_response,
            "model": "Llama3",
            "error": chatgpt_error
        }

    else:
        return {
            "status": "error",
            "response": None,
            "model": None,
            "error": f"Falha em ambas as APIs: ChatGPT ({chatgpt_error}), Llama3 ({llama_error})"
        }
