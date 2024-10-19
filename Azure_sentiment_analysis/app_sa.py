import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

AI_SERVICE_KEY = os.getenv("AI_SERVICE_KEY")
AI_SERVICE_ENDPOINT = os.getenv("AI_SERVICE_ENDPOINT")
credential = AzureKeyCredential(AI_SERVICE_KEY)
ai_client = TextAnalyticsClient(endpoint=AI_SERVICE_ENDPOINT, credential=credential)

#OPENAI_API_ENDPOINT = "https://aiservicesdemo3232.cognitiveservices.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview"  # Replace with your actual OpenAI API key
OPENAI_API_ENDPOINT = "https://aiservicesdemo3232.openai.azure.com/"
# OpenAI API setup
client = AzureOpenAI(
    azure_endpoint= OPENAI_API_ENDPOINT, 
    api_key=AI_SERVICE_KEY,  
    api_version="2024-02-01"  # As per documentation
)


def user_input(sentiment,user_question):
    # Create the prompt
    prompt_template = f'Analyze the sentiment of the following text: "{user_input}". Can you provide a brief analysis and explain the reasoning behind the identified sentiment?{sentiment}'
    chain = prompt_template
    llm = AzureChatOpenAI(
        azure_deployment= "gpt-35-turbo",
        api_version= "2024-02-01",
        api_key=AI_SERVICE_KEY,
        azure_endpoint = AI_SERVICE_ENDPOINT
    )
    prompt = chain.format(context= sentiment, question= user_question)  #line no 98 #lineno 119
    response = llm.invoke(prompt)  #prompttemplate + embedding respone + the user question
    
    return response.content
    #print(response.content) #cmd
    #st.write(response.content)  #getting response in ui


# Streamlit app
def main():
    st.set_page_config(page_title="Chat with PDF")
    # Streamlit app
    st.title("Sentiment Analysis with OpenAI")
    
    #Text Input 
    user_question = st.text_area("Enter text for sentiment analysis:")
    if st.button("Analyze Sentiment"):
            if user_question:
                # Analyze sentiment with Azure
                sentiment_analysis = ai_client.analyze_sentiment(documents=[user_question])[0]
                sentiment = sentiment_analysis.sentiment
                st.write(f"Sentiment: **{sentiment}**")
                sentiment = str(sentiment)
                # Get the analysis from OpenAI
                response_content = user_input(sentiment, user_question)
                st.write("OpenAI Response:")
                st.write(response_content)
            else:
                st.error("Please enter some text.")     

if __name__ == "__main__":
    main()

# import streamlit as st
# from azure.core.credentials import AzureKeyCredential
# from azure.ai.textanalytics import TextAnalyticsClient

# # Initialize Azure Text Analytics client
# AI_SERVICE_ENDPOINT = "https://aiservicesdemo3232.cognitiveservices.azure.com/"
# AI_SERVICE_KEY = "dad9815a11fb41adb8983c5a7f42a145"

# ai_endpoint = AI_SERVICE_ENDPOINT
# ai_key = AI_SERVICE_KEY
# credential = AzureKeyCredential(ai_key)
# ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

# # Streamlit app
# st.title("Sentiment Analysis")

# # Text input
# user_input = st.text_area("Enter text for sentiment analysis:")

# if st.button("Analyze Sentiment"):
#     if user_input:
#         # Analyze sentiment
#         sentiment_analysis = ai_client.analyze_sentiment(documents=[user_input])[0]
#         sentiment = sentiment_analysis.sentiment
#         st.write(f"Sentiment: **{sentiment}**")
#     else:
#         st.error("Please enter some text.")
