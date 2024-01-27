import os
import openai
import random
import time
import names

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)

def main():
  openai.api_key = OPENAI_API_KEY  # Initializes AI
  user_start = input('Would you like to run the simulation [y/n]?: ') # Prompts the user whether or not they would like to start the simulation
  while user_start.lower() not in ['y', 'n']:
    user_start = input('Would you like to run the simulation [y/n]?: ')

  # If the user wanted to start then we will begin
  if user_start.lower() == 'y':
    # User enters an initial prompt to sort of guide the conversation
    prompt1 = input('Enter an initial prompt to get the conversation going: ')
    limit = input('Set the amount of messages you\'d like the bots to have: ')

    # Sets the random age and gender of each AI bot
    ai_1_properties = get_ai_properties()
    ai_2_properties = get_ai_properties()

    # Outputs the name and age of each bot
    time.sleep(1)
    print('Initializing AI...')
    print('\n====================================================\n')
    print('Initial prompt: ' + prompt1+'\n')
    print(f'AI 1 Details:\n\tAge: {ai_1_properties.age}\n\tGender: {ai_1_properties.gender}')
    print(f'AI 2 Details:\n\tAge: {ai_2_properties.age}\n\tGender: {ai_2_properties.gender}')
    print('Message Limit: ' + limit)
    print('\n====================================================\n')
    print('Initializing conversation...')
    print('\n====================================================\n')

    ai_1_response_1 = get_message_from_ai1(ai_1_properties.age, ai_1_properties.gender, [{'role': 'user', 'content': prompt1}])

    # These are the initial message arrays for the AI, as it runs it will append to this array, this way the AI retains its memory of the conversation
    ai_1_messages = [
      {"role": "system", "content": "You are a human living on Earth and you will have to converse with another human. Your goal is to communicate and speak your mind. Make sure to mention your age and gender to the other user, you are " + str(ai_1_properties.age) +  " years old and you are a " + str(ai_1_properties.gender) +". Limit your responses to 50 words in length. For all of the years you have lived you have history and life experiences and friends and family, you are a real person."}, 
      {"role": "user", "content": str(prompt1)},
      ]
    ai_2_messages = [
      {"role": "system", "content": "You are a human living on Earth designed to converse with another human. Your goal is to communicate and speak your mind. Make sure to mention your age and gender to the other user, you are " + str(ai_2_properties.age) +  " years old and you are a " + str(ai_2_properties.gender) +"Limit your responses to 50 words in length. For all of the years you have lived you have history and life experiences and friends and family, you are a real person."}, 
      {"role": "user", "content": str(ai_1_response_1)},
      ]
    
    start_time = time.time()
    
    print(f"\tAI 1 {time.time() - start_time}: {ai_1_response_1}\n")
    time.sleep(2)
    for i in range(int(limit)): # Runs for the limit specified earlier
      ai_2_message = get_message_from_ai2(ai_2_properties.age, ai_2_properties.gender, ai_2_messages)
      ai_1_messages.append({'role': 'user', 'content': ai_2_message})
      print(f"\tAI 2 {time.time() - start_time}: {ai_2_message}\n")
      time.sleep(2)
      ai_1_message = get_message_from_ai1(ai_2_properties.age, ai_2_properties.gender, ai_1_messages)
      ai_2_messages.append({'role': 'user', 'content': ai_1_message})
      print(f"\tAI 1{time.time() - start_time}: {ai_1_message}\n")

    print('\n====================================================\n')
    print(f'{int(limit) + 1} messages sent in {time.time() - start_time} seconds.')


def get_message_from_ai1(age, gender, messages):
  response = openai.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=messages
    )
  
  return response.choices[0].message.content.strip()

def get_message_from_ai2(age, gender, messages):
  response = openai.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=messages
    )
  
  return response.choices[0].message.content.strip()

def get_ai_properties():
  class AI_Information():
    def __init__(self) : # Sets age and gender for the class
      self.age = random.randint(18,82)
      self.gender = self.get_gender()
    
    def get_gender(self): # Sets a random gender for the class
      rand_number = random.randint(1,2)
      if rand_number == 1:
        return 'Male'
      else:
        return 'Female'
    
  new_ai = AI_Information()
  return new_ai

if __name__ == '__main__' and OPENAI_API_KEY:
  main()