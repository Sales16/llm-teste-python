# Aplicação Python para Comparação de LLMs

## Descrição
A aplicação desse projeto foi desenvolvido como parte de um teste prático para implementar uma solução que conecta duas APIs de Modelos de Linguagem Natural (LLMs): ChatGPT e Llama3 (via Groq). A solução utiliza padrões de projeto (Factory, Command, Strategy e Observer) para garantir flexibilidade, modularidade e clareza no código.

A aplicação permite que o usuário:
- Envie perguntas a ambos os modelos.
- Compare as respostas usando diferentes estratégias de avaliação.
- Veja qual modelo gerou a resposta escolhida e o motivo da escolha.
- Continue interagindo até que decida encerrar o chat.

## Configuração
1. Obtenha suas chaves de API para o ChatGPT e Groq.
   
2. Instale as dependências:
   ```bash
   pip install openai groq rich
    ```

## Uso
1. Execute a aplicação:
   ```bash
   python main.py
   ```

2. Siga as instruções no console para inserir suas chaves de API e escolher a estratégia de avaliação.
   
3. Envie suas perguntas. Para sair, digite sair.

### Estratégias de Avaliação
- **1. Resposta mais longa (padrão)**: Escolhe a resposta mais longa entre as fornecidas pelos modelos.
- **2. Resposta mais curta (direta)**: Escolhe a resposta mais curta entre as fornecidas pelos modelos.
- **3. Resposta com palavras-chave específicas**: Escolhe a resposta que contém mais palavras-chave fornecidas pelo usuário.

