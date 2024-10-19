#text analytics
# speech to text analystics
#sentiment analysis for text
#sentiment analysis for speeech

import streamlit as st
import speech_recognition as sr
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from openai import AzureOpenAI
from langchain_openai import AzureChatOpenAI
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI

# Azure Text Analytics client
AI_SERVICE_ENDPOINT = "https://aiservicesdemo3232.cognitiveservices.azure.com/"
AI_SERVICE_KEY = "dad9815a11fb41adb8983c5a7f42a145"  # Replace with your actual key
credential = AzureKeyCredential(AI_SERVICE_KEY)
ai_client = TextAnalyticsClient(endpoint=AI_SERVICE_ENDPOINT, credential=credential)

#OPENAI_API_ENDPOINT = "https://aiservicesdemo3232.cognitiveservices.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2024-08-01-preview"  # Replace with your actual OpenAI API key
OPENAI_API_ENDPOINT = "https://aiservicesdemo3232.openai.azure.com/"



AZURE_SPEECH_REGION ="eastus"
AZURE_SPEECH_KEY = "dad9815a11fb41adb8983c5a7f42a145"

DEPLOYMENT_NAME = "gpt-35-turbo"
OPENAI_API_VERSION = "2024-02-01"


# Azure Text Analytics client
AI_SERVICE_ENDPOINT = "https://aiservicesdemo3232.cognitiveservices.azure.com/"
AI_SERVICE_KEY = "dad9815a11fb41adb8983c5a7f42a145"  # Replace with your actual key



# OpenAI API setup
client = AzureOpenAI(
    azure_endpoint= OPENAI_API_ENDPOINT, 
    api_key=AI_SERVICE_KEY,  
    api_version="2024-02-01"  # As per documentation
)


def user_input(sentiment,user_question):
    # Create the prompt
    prompt_template = f'Analyze the sentiment of the following text: "{user_question}". Can you provide a brief analysis and explain the reasoning behind the identified sentiment?{sentiment}'
    
    chain = prompt_template
    llm = AzureChatOpenAI(
        azure_deployment= "gpt-35-turbo",
        api_version= "2024-02-01",
        api_key=AI_SERVICE_KEY,
        azure_endpoint = AI_SERVICE_ENDPOINT
    )
    prompt = chain.format(context= sentiment, question= user_question)  #line no 98 #lineno 119
    response = llm.invoke(prompt)  #prompttemplate + embedding respone + the userquestion
    
    return response.content
    #print(response.content) #cmd
    #st.write(response.content)  #getting response in ui



def speech_recognition_result():
    speech_config = speechsdk.SpeechConfig(subscription = AZURE_SPEECH_KEY, region = AZURE_SPEECH_REGION)
    speech_config.speech_recognition_language = "en-us"
    
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    #speech recog both speech and audio as input
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("You can speak now, I'm listening")
    
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(speech_recognition_result.text)
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized.")
    else:
            print(f"Speech Recognition canceled: {speech_recognition_result.cancellation_details.reason}")
        
        
    output = speech_recognition_result.text
    #print(output)
    st.write("*You said:* " + output + "**")
    azure_openai = AzureChatOpenAI(
        azure_deployment=DEPLOYMENT_NAME,  # Your Azure OpenAI deployment name
        api_version=OPENAI_API_VERSION,     # Your API version
        api_key=AI_SERVICE_KEY,
        azure_endpoint = AI_SERVICE_ENDPOINT
    )

    # Prepare the prompt
    #prompt = output  # Assuming 'output' is defined elsewhere in your code

    prompt = f"""
    Sentiment Detection Prompt

    Please analyze the text output detect from speech recognition and determine the overall sentiment as either Positive, Negative, or Mixed. Provide a brief explanation for your classification.
    you are provided with following examples as reference to detect the text 
    Examples:

    Text: "I absolutely loved the concert! The energy was incredible and the band played all my favorite songs."
    Sentiment: Positive
    Explanation: The sentiment is positive due to expressions of enjoyment and excitement.

    Text: "I had a terrible experience at the restaurant. The service was slow and the food was cold."
    Sentiment: Negative
    Explanation: The sentiment is negative because of dissatisfaction and complaints.

    Text: "The movie had stunning visuals, but the plot was confusing and hard to follow."
    Sentiment: Mixed
    Explanation: The sentiment is mixed as there are both positive and negative elements present.
    Now, please analyze the following text: {output}.


    """
    # Create the response
    response = azure_openai.invoke(prompt)

    # Extract the output text
    output_text = response.content  # Use .content to get the text in the response
    
    return output_text



def main():
        

    # Set the title of the app
    st.header("Sentiment Analysis using Azure")

    # Add a subtitle
    st.write("Choose your input method")

    # Create a sidebar for better navigation
    st.sidebar.header("Options")
    input_option = st.sidebar.radio("Select Input Method", ("Text Input", "Voice Input"))

    # Function for text input
    def text_input():
        st.subheader("Enter your text")
        user_question = st.text_area("Enter text for sentiment analysis:",  height=150)
        
        if st.button("Analyze Text"):
                if user_question:
                    # Analyze sentiment with Azure
                    st.success("Text has been submitted!")
                    sentiment_analysis = ai_client.analyze_sentiment(documents=[user_question])[0]
                    sentiment = sentiment_analysis.sentiment
                    st.write(f"Sentiment: **{sentiment}**")
                    sentiment = str(sentiment)
                    # Get the analysis from OpenAI
                    response_content = user_input(sentiment, user_question)
                    st.write("OpenAI Response:")
                    st.write(response_content)
                else:
                    st.error("Please enter some text before clicking the button.")    

    # Function for voice input (placeholder for functionality)
    def voice_input():
        st.header("Record your voice")
        st.write("Click the button below to start recording your speech.")
        
        text = ""
        # Button to start recording
        if st.button("Record Speech"): 
            # Create a recognizer instance
            recognizer = sr.Recognizer()
            # Use the microphone as source
            with sr.Microphone() as source:
                st.write("Listening...")
            # Capture the audio
                
                # Try to recognize the speech
                try:
                    st.write("Recognizing...")
                    text = speech_recognition_result()
                    st.markdown("<h3 style='font-size: 30px;>{text}</h3>", unsafe_allow_html=True) 
                    st.markdown("**The Sentiment Analysis is :**")
                    text = text.split("\n")
                    with st.success("Show Result"):
                        for e in text:
                            st.markdown(f"**{e}**")
                except sr.UnknownValueError:
                    st.error("Sorry, I could not understand the audio.")
                except sr.RequestError as e:
                    st.error(f"Could not request results from the speech recognition service; {e}")
                    

    # Render the appropriate input method based on user selection
    if input_option == "Text Input":
        text_input()
    else:
        voice_input()

    # Footer
    st.markdown("---")
    

 
if __name__ == "__main__":
    main()