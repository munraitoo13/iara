Iara (Sim, um trocadilho com "IA") é uma assistente de recepção virtual para coletar informações de visitantes e agendar consultas médicas de forma eficiente.

## Funcionalidades

- Coleta de informações do visitante, como nome, endereço e motivo da visita.

## Funcionalidades Futuras (TBD)

- Agendamento de consultas médicas.
- Integração com calendários para evitar conflitos de horários.
- Envio de lembretes de consultas via e-mail ou SMS.

## Nota

É UM PROJETO EXPERIMENTAL! O uso de tokens é alto intencionalmente para testes e desenvolvimento. Não é recomendado para uso em produção.

## Tecnologias Utilizadas

- Python 3.13
- Pydantic
- Google GenAI SDK

## Instalação

Siga os passos abaixo para configurar e instalar o projeto localmente:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/your-username/iara.git
    cd iara
    ```

2.  **Crie e ative o ambiente virtual:**

    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    uv pip install -r requirements.txt
    # ou se estiver usando uv.lock
    uv pip install -r uv.lock
    ```

    _Nota: O arquivo `requirements.txt` pode precisar ser gerado a partir do `uv.lock` ou `pyproject.toml`._

4.  **Configure as variáveis de ambiente:**

    Copie o arquivo `.env.example` para `.env` e preencha com suas credenciais, especialmente a chave da API do Google GenAI.

    ```bash
    cp .env.example .env
    ```

## Como Rodar

Para executar o projeto, certifique-se de que o ambiente virtual está ativado e execute o arquivo `main.py`:

```bash
source .venv/bin/activate
python iara/main.py
```
