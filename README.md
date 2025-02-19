# Multi-LLM Idea Discussion App

## Overview
The **Multi-LLM Idea Discussion App** is a Streamlit-based web application that facilitates interactive discussions on various topics using multiple LLMs (Large Language Models). The app enables role-based discussions between multiple AI models and generates a summarized plan of the conversation.

## Features
- Supports three LLMs for generating discussion: **LLaMA-3.1, LLaMA-3.2, DeepSee-by-qwen,deepseek-by-meta and gemma**.
- Allows users to define characters with names and professions.
- Allows utilization of required members in discussion
- Conducts discussions iteratively between the characters.
- Summarizes discussions into a structured plan using LLaMA-3.3.
- Streamlit-based UI for easy interaction.

## Directory Structure
```
└── multi-llm-idea-discussion-app/
    ├── README.md
    ├── Road_ahead.md
    ├── main.py
    ├── requirements.txt
    ├── models/
    │   ├── dee_see.py
    │   ├── dee_see_meta.py
    │   ├── gemma_model.py
    │   ├── llama_model_1.py
    │   └── middle_llama.py
    └── services/
        └── event_summarizer.py

```

## Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/anuragsinghbhandari/Multi-LLm-Idea-Discussion-App.git
   cd Multi-LLm-Idea-Discussion-App
   ```
2. **Create and activate a virtual environment (optional but recommended)**
   ```sh
   python -m venv venv  #only once while setup
   source venv/bin/activate  # On Windows use `venv\Scripts\activate` #everytime you open the directory
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables**
   GO to https://console.groq.com/keys and create account and create an api key.
   create an .env file in root folder and set GROQ_API_KEY=YOUR_API_KEY
   If the key is not set, the application will prompt you to enter it at runtime.

## Usage
1. **Run the Streamlit app**
   ```sh
   streamlit run main.py
   ```
2. **Enter the required details**
   - Topic of discussion
   - Names and professions of the three participants
3. **Click "Start"** to initiate a structured discussion.
4. **Click "Summarize"** to generate a structured plan of the discussion.

## Models Used
- `llama_model_1.py`: Uses **LLaMA-3.1-8b** for generating responses.
- `middle_llama.py`: Uses **LLaMA-3.2-3b-preview** for responses.
- `dee_see.py`: Uses **DeepSeek-R1-Distill-Qwen-32B** for generating responses.
-  dee_see_meta.py: Uses **DeepSeek-R1-Distill-llama-70b** for generating responses.
- `event_summarizer.py`: Uses **LLaMA-3.3-70b-versatile** to summarize discussions.

## Dependencies
The project requires the following Python packages:
```
langchain-groq
streamlit
python-dotenv
```
Install them using:
```sh
pip install -r requirements.txt
```

## License
This project is licensed under the APACHE License.

## Acknowledgements
- [Meta AI](https://ai.facebook.com/research/) for LLaMA models.
- [DeepSeek](https://www.deepseek.com/) for their language model.
- [LangChain](https://www.langchain.com/) for simplifying LLM interactions.
- [Gemma](https://www.ai.google.dev/) for gemma model.
