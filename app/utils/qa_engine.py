import os
import requests
import logging

logger = logging.getLogger(__name__)

class QAEngine:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("GROQ_API_KEY environment variable is not set!")
        else:
            logger.info(f"GROQ_API_KEY loaded in QAEngine: {self.api_key[:10]}...")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model  = "meta-llama/llama-4-maverick-17b-128e-instruct"

    def ask_about_celebrity(self,name,question):
        headers = {
            "Authorization" : f"Bearer {self.api_key}",
            "Content-Type" : "application/json"
        }

        prompt = f"""
                    You are a AI Assistant that knows a lot about celebrities. You have to answer questions about {name} concisely and accurately.
                    Question : {question}
                    """
        
        payload  = {
            "model" : self.model,
            "messages" : [{"role" : "user" , "content" : prompt}],
            "temperature" :  0.5,
            "max_tokens" : 512
        }

        try:
            response = requests.post(self.api_url , headers=headers , json=payload)
            logger.info(f"QA API response status: {response.status_code}")

            if response.status_code==200:
                answer = response.json()['choices'][0]['message']['content']
                logger.info(f"QA answer: {answer[:100]}...")
                return answer
            else:
                logger.error(f"QA API error: {response.status_code} - {response.text}")
                return f"API Error: {response.status_code}"
        except Exception as e:
            logger.error(f"Exception in QA: {str(e)}")
            return f"Error: {str(e)}"