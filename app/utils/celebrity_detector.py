import os 
import base64
import requests
import logging

logger = logging.getLogger(__name__)

class CelebrityDetector:

    def __init__(self):
        self.api_key=os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("GROQ_API_KEY environment variable is not set!")
        else:
            logger.info(f"GROQ_API_KEY loaded: {self.api_key[:10]}...")
        self.api_url="https://api.groq.com/openai/v1/chat/completions"
        self.model ="meta-llama/llama-4-maverick-17b-128e-instruct"
    #identify celebrity in the image
    def identify(self, image_bytes):
        #Convert image bytes to base64 string(for API transmission)
        encoded_image= base64.b64encode(image_bytes).decode()

        headers= {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        prompt = {
            "model": self.model,
            "messages": [
                {
                    "role": "user", 
                    "content": [
                        {
                            "type": "text",
                            "text": """You are a celebrity recognition expert AI. 
Identify the person in the image. If known, respond in this format:

- **Full Name**:
- **Profession**:
- **Nationality**:
- **Famous For**:
- **Top Achievements**:

If unknown, return "Unknown".
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.3,    
            "max_tokens": 1024     
        }

    
        
        try:
            response= requests.post(self.api_url, headers=headers, json=prompt)
            logger.info(f"Groq API response status: {response.status_code}")
            
            if response.status_code == 200:
                result=response.json()['choices'][0]['message']['content']
                logger.info(f"Celebrity detected: {result[:100]}...")
                
                name=self.extract_name(result)
                logger.info(f"Extracted name: {name}")

                return result, name
            else:
                logger.error(f"Groq API error: {response.status_code} - {response.text}")
                return f"API Error: {response.status_code}", ""
        except Exception as e:
            logger.error(f"Exception in celebrity detection: {str(e)}")
            return f"Error: {str(e)}", ""
    def extract_name(self, content):
        for line in content.splitlines():
            if line.startswith("- **Full Name**:"):
                return line.split(":")[1].strip()

        return "Unknown"    