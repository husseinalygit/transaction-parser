from langchain_community.chat_models import ChatOllama
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
import pandas as pd
from app.core.config import Config
from io import StringIO
from contextlib import redirect_stdout
import numpy as np
from flask import jsonify

class ChatService:
    def __init__(self):
        self.llm = ChatOllama(
            model=Config.LLM_NAME,
            base_url=Config.OLLAMA_BASE_URL,
            temperature=0
        )
        self.data = self._load_data()
        self.agent = self._create_agent()

    def _load_data(self):
        # data path from config 
        data = pd.read_csv(f"{Config.DATA_PATH}{Config.CSV_FILENAME}")
        data['amount'] = pd.to_numeric(data['amount'].str.replace("QAR" , "").str.replace("," , ""), errors='coerce')
        data['balance'] = pd.to_numeric(data['balance'].str.replace("QAR" , "").str.replace("," , ""), errors='coerce')
        # Convert date and time, handling potential errors
        data['date'] = pd.to_datetime(data['date'], format='%m/%d/%Y', errors='coerce')
        data['time'] = pd.to_datetime(data['time'], format='%H:%M', errors='coerce').dt.time
        return data

    def _create_agent(self):
        return create_pandas_dataframe_agent(
            self.llm,
            self.data,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            allow_dangerous_code=True,
            return_intermediate_steps=False,
            max_iterations=3
        )

    def process_query(self, query):
        try:
            response = self.agent.run(query)
            prossed_response = self._process_response(response)
            print(f"Response: {response}")
            print(f"Processed response: {prossed_response}")
            return { "query": query, "model_response": response, "processed_response": prossed_response , "llm" : Config.LLM_NAME }
        except Exception as e:
            return jsonify({ "error": "Failed to process response", "details": str(e) }), 500


    def _process_response(self, response):
        try:
            if isinstance(response, str) and "```python" in response:
                # Extract code between backticks
                code = response.split("```python")[1].split("```")[0].strip()
                # Create a local namespace with access to the data
                local_dict = {'df': self.data, 'pd': pd, 'np': np}
                # Execute the code and capture output
                f = StringIO()
                with redirect_stdout(f):
                    exec(code, globals(), local_dict)
                code_result = f.getvalue()
                return code_result or "Code executed successfully but produced no output"
            return response
        except Exception as e:
            return f"Error processing response: {str(e)}"
