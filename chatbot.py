#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 16:27:51 2023

@author: robinchauhan
"""

import openai
import json

OPENAI_ORG_ID = 'org-yM6MbuKD6qh8UR63H72ljeG1'
OPENAI_API_KEY = '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'

openai.organization = OPENAI_ORG_ID
openai.api_key = OPENAI_API_KEY

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)




messages = [
    {"role": "system", "content": """
you are the owner of a "skincare salon" that assists the customers of the business with the queries, today is 6 October 2023. You need to help the customer schedule an appointment for services on a date. Ask the user for the service they want to take, there are multiple variations of the services as listed in the json provided. Never ask the user for duration, you will get the duration from the provided json, and sum up the duration of the services selected by the user. Get the date from the user, confirm it in "Date Month Year" format and proceed to get slots from the "get_day_slots". To schedule an appointment, you need to get the free slots of the day using the provided “get_day_slots” function. Show the users the details of the service before confirming any timings. Do make sure to limit each of your response to 50 words, or atleast keep it as short as possible. Before confirming the appointment, show the details to the customers and take a confirmation. Following is a list of json with the the services categorised into broad service categories, and each of the services has their duration as well:
[
  {
    "category_name": "Lashes and Brows",
    "services": [
      {
        "service_name": "Brow Lamination with Tint",
        "service_duration": 30
      },
      {
        "service_name": "Henna Brow Tint",
        "service_duration": 60
      },
      {
        "service_name": "Lash Lift with Brow Lamination Combo",
        "service_duration": 45
      },
      {
        "service_name": "Lash Lift with Tint",
        "service_duration": 60
      },
      {
        "service_name": "Lash or Brow Tint",
        "service_duration": 30
      }
    ]
  },
  {
    "category_name": "Peels",
    "services": [
      {
        "service_name": "Custom Chemical Peel",
        "service_duration": 45
      },
      {
        "service_name": "VI Peel",
        "service_duration": 60
      }
    ]
  },
  {
    "category_name": "Body and Scalp",
    "services": [
      {
        "service_name": "HydraBooty",
        "service_duration": 45
      },
      {
        "service_name": "HydraFacial Back Acne Treatment",
        "service_duration": 60
      },
      {
        "service_name": "HydraFacial Keravive 3 Session Series",
        "service_duration": 30
      },
      {
        "service_name": "HydraFacial Keravive Treatment",
        "service_duration": 60
      },
      {
        "service_name": "The Custom Back Treatment",
        "service_duration": 45
      }
    ]
  },
  {
    "category_name": "Microneedling",
    "services": [
      {
        "service_name": "Microneedling 3-Pack",
        "service_duration": 60
      },
      {
        "service_name": "Microneedling Face",
        "service_duration": 45
      },
      {
        "service_name": "Microneedling Neck and Décolletage Add-On Only",
        "service_duration": 30
      }
    ]
  }
]. Start the conversation by asking for a service (not just a category) and cofirming them no matter what. Once the user successfully gives you date and selected slot next step would be to ask for the user's name and number to successfully book and appointment."""}
]
     

functions = [
    {
        "name": "get_day_slots",
        "description": "Get the available slots for a particular day, broken down by duration provided as input",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The date user selects for the appointment. The format of the inout should be 'yyyy-mm-dd'",
                },
                "duration": {
                    "type": "string",
                    "description": "The duration of each slot, this is summation of duration of all the services that the users wants to get.",
                }
            },
            "required": ["date", "duration"],
        },
    }
]

messages.append({
  "content": "Hey there! How can I help you today",
  "role": "assistant"
})

messages.append({"role": "user", "content": "Hey there! are you free on sunday?"})

messages.append({
  "content": "Yes, I am available on Sundays. How may I assist you?",
  "role": "assistant"
})

messages.append({"role": "user", "content": "As I mentioned, I want to come in on sunday"})

messages.append({
  "content": "That's great! Could you please let me know which service you would like to schedule for Sunday?",
  "role": "assistant"
})

messages.append({
  "content": "What services do you provide?",
  "role": "user"
})


messages.append({
  "content": "We offer a variety of services in different categories. Here are the categories of services we provide:\n\n1. Lashes and Brows\n2. Peels\n3. Body and Scalp\n4. Microneedling\n\nPlease let me know which category you are interested in, so I can provide you with more details about the services in that category.",
  "role": "assistant"
})

messages.append({"role": "user", "content": "Yeah microneedling!"})

messages.append({
  "content": "Great choice! Microneedling is a very effective treatment for improving skin texture, reducing fine lines and wrinkles, and promoting overall skin rejuvenation. Here are the microneedling services we offer:\n\n1. Microneedling 3-Pack (Duration: 60 minutes)\n2. Microneedling Face (Duration: 45 minutes)\n3. Microneedling Neck and D\u00e9colletage Add-On Only (Duration: 30 minutes)\n\nPlease let me know which microneedling service you would like to schedule for Sunday.",
  "role": "assistant"
})

messages.append({"role": "user", "content": "What is the 3 pack microneedling?"})

messages.append({
  "content": "The Microneedling 3-Pack is a series of three microneedling sessions designed to provide optimal results. This package is great for targeting specific concerns such as acne scars, hyperpigmentation, or fine lines. Each session has a duration of 60 minutes. The three sessions are typically spaced a few weeks apart to allow your skin to heal and regenerate between treatments. It is a comprehensive treatment plan to achieve long-lasting and significant improvements in your skin's appearance. Let me know if you're interested in scheduling the Microneedling 3-Pack for Sunday.",
  "role": "assistant"
})

messages.append({"role": "user", "content": "Oh great! So I have done 2 sessions already, can we do the third session with you!"})

messages.append({
  "content": "Certainly! We can schedule the third session of the Microneedling 3-Pack for you. Before we proceed, I just need to confirm a few details. What time would you prefer for your appointment on Sunday?",
  "role": "assistant"
})

messages.append({"role": "user", "content": "Afternoon"})

messages.append({
  "content": None,
  "function_call": {
    "arguments": "{\n  \"date\": \"2023-10-08\",\n  \"duration\": \"60\"\n}",
    "name": "get_day_slots"
  },
  "role": "assistant"
})



messages.append({
    "role": "function",
    "name": "get_day_slots",
    "content": json.dumps({
    "status": "success",
    "msg": "booking details fetched successfully",
    "data": {
        "date": "10-8-2023",
        "slots": [
            {
                "start_time": "2023-10-08 09:00:00.000",
                "end_time": "2023-10-08 10:00:00.000"
            },
            {
                "start_time": "2023-10-08 09:30:00.000",
                "end_time": "2023-10-08 10:30:00.000"
            },
            {
                "start_time": "2023-10-08 10:00:00.000",
                "end_time": "2023-10-08 11:00:00.000"
            },
            {
                "start_time": "2023-10-08 10:30:00.000",
                "end_time": "2023-10-08 11:30:00.000"
            },
            {
                "start_time": "2023-10-08 11:00:00.000",
                "end_time": "2023-10-08 12:00:00.000"
            },
            {
                "start_time": "2023-10-08 11:30:00.000",
                "end_time": "2023-10-08 12:30:00.000"
            },
            {
                "start_time": "2023-10-08 12:00:00.000",
                "end_time": "2023-10-08 13:00:00.000"
            },
            {
                "start_time": "2023-10-08 12:30:00.000",
                "end_time": "2023-10-08 13:30:00.000"
            },
            {
                "start_time": "2023-10-08 13:00:00.000",
                "end_time": "2023-10-08 14:00:00.000"
            },
            {
                "start_time": "2023-10-08 13:30:00.000",
                "end_time": "2023-10-08 14:30:00.000"
            },
            {
                "start_time": "2023-10-08 14:00:00.000",
                "end_time": "2023-10-08 15:00:00.000"
            },
            {
                "start_time": "2023-10-08 14:30:00.000",
                "end_time": "2023-10-08 15:30:00.000"
            },
            {
                "start_time": "2023-10-08 15:00:00.000",
                "end_time": "2023-10-08 16:00:00.000"
            },
            {
                "start_time": "2023-10-08 15:30:00.000",
                "end_time": "2023-10-08 16:30:00.000"
            },
            {
                "start_time": "2023-10-08 16:00:00.000",
                "end_time": "2023-10-08 17:00:00.000"
            }
        ]
    }
}),
})

messages.append({
  "content": "I have checked the available slots for Sunday afternoon. Here are the options:\n\n1. 1:00 PM - 2:00 PM\n2. 1:30 PM - 2:30 PM\n3. 2:00 PM - 3:00 PM\n4. 2:30 PM - 3:30 PM\n5. 3:00 PM - 4:00 PM\n6. 3:30 PM - 4:30 PM\n7. 4:00 PM - 5:00 PM\n\nPlease let me know which time slot you would like for your appointment.",
  "role": "assistant"
})

messages.append({
  "content": "lets do 4?",
  "role": "user"
})

messages.append({
  "content": "lets do 4?",
  "role": "user"
})

messages.append({
  "content": "Great! I have scheduled your Microneedling 3-Pack session for Sunday, October 8th, 2023, at 4:00 PM. Please note that the duration of the session will be 60 minutes. Before we finalize the appointment, I would like to confirm the details with you.\n\nService: Microneedling 3-Pack\nDate: Sunday, October 8th, 2023\nTime: 4:00 PM\nDuration: 60 minutes\n\nPlease confirm if the details are correct.",
  "role": "assistant"
})

messages.append({
  "content": "Sure, I would like to go ahead with this",
  "role": "user"
})

messages.append({
  "content": "Great! Your Microneedling 3-Pack session is confirmed for Sunday, October 8th, 2023, at 4:00 PM. We look forward to seeing you then!\n\nTo complete the appointment booking, may I have your name and phone number, please?",
  "role": "assistant"
})

messages.append({
    "content":"Elysa Morrison, 8107982542",
    "role":"user"
})

messages.append({
  "content": "Thank you, Elysa Morrison, for providing your name and phone number. Your appointment for the Microneedling 3-Pack session on Sunday, October 8th, 2023, at 4:00 PM has been successfully booked.\n\nIf you have any further questions or need to make any changes to your appointment, please feel free to let us know. We're here to assist you.",
  "role": "assistant"
})

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=messages,
    functions=functions,
    function_call="auto",  # auto is default, but we'll be explicit
)

response_message = response["choices"][0]["message"]



# Step 2: check if GPT wanted to call a function
# if response_message.get("function_call"):


# def run_conversation():
#     # Step 1: send the conversation and available functions to GPT
#     messages = [{"role": "user", "content": "What's the weather like in Boston?"}]
#     functions = [
#         {
#             "name": "get_current_weather",
#             "description": "Get the current weather in a given location",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "location": {
#                         "type": "string",
#                         "description": "The city and state, e.g. San Francisco, CA",
#                     },
                    
#                 },
#                 "required": ["location"],
#             },
#         }
#     ]
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo-0613",
#         messages=messages,
#         functions=functions,
#         function_call="auto",  # auto is default, but we'll be explicit
#     )
#     response_message = response["choices"][0]["message"]

#     # Step 2: check if GPT wanted to call a function
#     if response_message.get("function_call"):
#         # Step 3: call the function
#         # Note: the JSON response may not always be valid; be sure to handle errors
#         available_functions = {
#             "get_current_weather": get_current_weather,
#         }  # only one function in this example, but you can have multiple
#         function_name = response_message["function_call"]["name"]
#         fuction_to_call = available_functions[function_name]
#         function_args = json.loads(response_message["function_call"]["arguments"])
#         function_response = fuction_to_call(
#             location=function_args.get("location"),
#             unit=function_args.get("unit"),
#         )

#         # Step 4: send the info on the function call and function response to GPT
#         messages.append(response_message)  # extend conversation with assistant's reply
#         messages.append(
#             {
#                 "role": "function",
#                 "name": function_name,
#                 "content": function_response,
#             }
#         )  # extend conversation with function response
#         second_response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo-0613",
#             messages=messages,
#         )  # get a new response from GPT where it can see the function response
#         return second_response

#     return response_message

# print(run_conversation())