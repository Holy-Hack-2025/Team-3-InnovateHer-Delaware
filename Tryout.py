import matplotlib.pyplot as plt

import requests 
from dotenv import load_dotenv 
import os 
load_dotenv()

api_key = os.getenv("OPENAI_API_key")

url = "URL "
headers = ... 
data = 

## Add Errors because otherwise the user dont know: keep all the exceptions of errors in the application

try: 
    response = requests.post(url, json = data, ....)
    print(response.json)
except requests.exeptions.RequestExceptions as e: 
    print("API request failed")

# sometimes applications fail due to exceptions, try to catch 
# what should we add to this code to try to filter out exceptions which are needed or not? 
#   ignore (but then you are not retrying again), retry logic (eg network failure: you are throwing this to the user )
retry_strategy = Retry()
# you need to use some libraries which can be used 
# makes it resilient: caching, baching

# another option: SDK = software development kit --> everything you need to integrate that platform into your application 
from openai import Open AI 
... 
load_dataenv() 
personal_api_key = os.getenv("")
client = OpenAI(api°key=personal_api_key)

response = client.chat.completions.create(model="gpt...")
messages[]

#Disadvantages: if you go really customed --> not the best choice. but a lot easier 
# API VS SDK 





# Anticipation is key to succes: flowchat for work, but there are a lot of things that can happen (error, how to use feedbackt to the customers, ...)
# Turn your api from a technical asset into a standout product 

# Logging: request comes in --> 1st you log the request, but you need a second log point --> 4 log points --> "4 ogen principe": you need to know where to log someting and at which points 
# who has accessed what data for which purpose and when? --> measure formats of the API 
# how many logs should you keep --> usually 3 months of logs --> very expensive databasis 
# Zalando APIs can help 
# working load: if you use an api during working hours eberything can go down. Your current user base's traffic patterns and frequency determine when and how heavility they load the system/ An upredictable or rapidly growng uer base can cause sudden spikes in API traffic. 