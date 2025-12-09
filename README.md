# Iara

Iara (a pun on "IA", the Portuguese acronym for AI) is a proof-of-concept for a virtual receptionist assistant. Its primary goal is to streamline the front-desk process by efficiently gathering visitor information, with a long-term vision of handling medical appointment scheduling. This project serves as an experimental platform for developing conversational AI solutions in clinical environments.

## Core Features

- **Visitor Information Gathering:** Collects essential details from visitors, including name, address, and the purpose of their visit.

## Future Roadmap (To Be Developed)

- **Appointment Scheduling:** Allow patients to book medical appointments directly through the assistant.
- **Calendar Integration:** Sync with existing calendar systems to avoid scheduling conflicts.
- **Automated Reminders:** Send appointment reminders to patients via email or SMS.

## Disclaimer

This is an **experimental project**. Token usage is intentionally high for testing and development purposes. It is **not recommended for production use**.

## Tech Stack

- Python 3.13
- Pydantic
- Google GenAI SDK

## Installation

Follow the steps below to set up and install the project locally:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/iara.git
    cd iara
    ```

2.  **Create and activate the virtual environment:**

    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    uv pip install -r requirements.txt
    # or if you are using uv.lock
    uv pip install -r uv.lock
    ```

    _Note: The `requirements.txt` file may need to be generated from `uv.lock` or `pyproject.toml`._

4.  **Configure environment variables:**

    Copy the `.env.example` file to `.env` and fill in your credentials, especially the Google GenAI API key.

    ```bash
    cp .env.example .env
    ```

## How to Run

To run the project, make sure the virtual environment is activated and execute the `main.py` file:

```bash
source .venv/bin/activate
python iara/main.py
```
