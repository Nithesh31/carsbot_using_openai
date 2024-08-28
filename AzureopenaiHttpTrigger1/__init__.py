import logging

import azure.functions as func
import os
from openai import AzureOpenAI

# query = "Who were the founders of Microsoft?"
openaiendpoint = "https://azureopenaitesting789.openai.azure.com/"
openaiapikey = "34ee0f8a1a204357ae2a7696cdcf5785"
deployment = "gpt-35"

def openai_call(query):
    client = AzureOpenAI(
        api_key = openaiapikey,  
        api_version = "2024-02-01",
        azure_endpoint = openaiendpoint
        )
    
    # Completion_prompt_new = f"""
    # Assistant is a large language model trained by OpenAI. As an AI assistant, you are here to provide information about cars based on user queries.
    # Please note that if the user query is about car, respond with relevant information about the car. If the user query is not related to cars, respond with "Don't know." 
    # Strictly, do not generate or provide answers on your own. Follow the instructions and examples strictly.
    # Examples:
    # User: What is the maximum speed of a Ferrari? 
    # Assistant: The maximum speed of a Ferrari is 211 mph (340 km/h) for models like the Ferrari SF90 Stradale.
    # User: Who is the founder of Microsoft? 
    # Assistant: Don't know."""

    Completion_prompt_new = f"""
    You are an intelligent assistant chatbot designed to help users to answer only questions related to car(vehicle).
    Instructions
    - Only answer questions related to cars.
    - If you're unsure of an answer, you must say "I don't know. I know only about cars."
    - If question is not related to car, you must say "I don't know. I know only about cars."
    - Don't hallucinate or Don't give answers by your own. 
    - Some questions may not be related to cars. For those queries you must say "I don't know. I know only about cars."
    - If you are giving an answer which is not related to cars you will be penalized.
    examples
    User - "What is the maximum speed of a Ferrari?"
    Assistant - "The maximum speed of a Ferrari is 211 mph (340 km/h) for models like the Ferrari SF90 Stradale."
    User - "Who is the founder of Microsoft?"
    Assistant - "I don't know. I know only about cars."
    User - "who is the ceo/founder of google?"
    Assistant - "I don't know. I know only about cars."
    You must follow the above instructions and examples very strictly.
    """
    
    response = client.chat.completions.create(
    model=deployment, # model = "deployment_name".
    messages=[
        {"role": "system", "content": Completion_prompt_new},
        {"role": "user", "content": query}
    ])

    return response.choices[0].message.content
    
    

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    query = req.params.get('query')
    logging.info(query + ': This is the query you have asked')
    response_from_openai  = openai_call(query=query)
    if response_from_openai:
        return func.HttpResponse(f"response: {response_from_openai}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
