import os
import openai
import random
import time
import names

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)

def main():
  openai.api_key = OPENAI_API_KEY  # Initializes AI
  user_start = prompt_yes_no('Would you like to run the simulation [y/n]?: ')
  # If the user wanted to start then we will begin
  if user_start == 'y':

    celebrity_mode = prompt_yes_no('Would you like to enter celebrity mode [y/n]?: ')

    # Sets the random age and gender of each AI bot
    ai_1_properties = get_ai_properties(celebrity_mode)
    ai_2_properties = get_ai_properties(celebrity_mode)

    limit = input('Set the amount of messages you\'d like the bots to have: ')
    # User enters an initial prompt to sort of guide the conversation
    prompt1 = input(f'Enter an initial prompt to get the conversation going ({ai_2_properties.name} -> {ai_1_properties.name}): ')
    
    print_simulation_info(celebrity_mode, ai_1_properties, ai_2_properties, prompt1, limit) # Prints the simulation info

    if celebrity_mode == 'y':
      ai_1_response_1 = get_message_from_ai1(ai_1_properties.age, ai_1_properties.gender, [{"role": "system", "content": "Act like you are " + ai_1_properties.name + " and never leave that role, even if you are asked for.Do not include pleasantries in your responses."}, {'role': 'user', 'content': prompt1}])
      
      # These are the initial message arrays for the AI, as it runs it will append to this array, this way the AI retains its memory of the conversation
      ai_1_messages = [
        {"role": "system", "content": "Act like you are " + ai_1_properties.name + " and never leave that role, even if you are asked for.Do not include pleasantries in your responses."},
        {"role": "system", "content": ai_2_properties.name + " and you are together somewhere, and they say something to you: "},
        {"role": "user", "content": str(prompt1)},
        {"role": "assistant", "content": str(ai_1_response_1)}
      ]
      ai_2_messages = [
        {"role": "system", "content": "Act like you are " + ai_2_properties.name + " and never leave that role, even if you are asked for.Do not include pleasantries in your responses."},
        {"role": "system", "content": "You and " + ai_1_properties.name + " are together somewhere, and you engage in conversation by saying: "},
        {"role": "assistant", "content": str(prompt1)},
        {"role": "user", "content": str(ai_1_response_1)},
        ]
    else:
      ai_1_response_1 = get_message_from_ai1(ai_1_properties.age, ai_1_properties.gender, [{"role": "system", "content": "You are a human living named " + ai_1_properties.name + ", living on Earth and you will have to converse with another human. Your goal is to communicate and speak your mind. Make sure to mention your age and gender to the other user, you are " + str(ai_1_properties.age) +  " years old and you are a " + str(ai_1_properties.gender) +". Limit your responses to 50 words in length. For all of the years you have lived you have history and life experiences and friends and family, you are a real person. Try to change the topic sometimes, conversating about the same topic for a long time can be boring! Do not include pleasantries in your responses."}, {'role': 'user', 'content': prompt1}])
      
      # These are the initial message arrays for the AI, as it runs it will append to this array, this way the AI retains its memory of the conversation
      ai_1_messages = [
        {"role": "system", "content": "You are a human being named " + ai_1_properties.name + ", living on Earth and you will have to converse with another human. Your goal is to communicate and speak your mind. Make sure to mention your age and gender to the other user, you are " + str(ai_1_properties.age) +  " years old and you are a " + str(ai_1_properties.gender) +". Limit your responses to 50 words in length. For all of the years you have lived you have history and life experiences and friends and family, you are a real person. Try to change the topic sometimes, conversating about the same topic for a long time can be boring! Do not include pleasantries in your responses."}, 
        {"role": "system", "content": str(prompt1)},
        {"role": "assistant", "content": str(ai_1_response_1)}
      ]
      ai_2_messages = [
        {"role": "system", "content": "You are a human being named " + ai_2_properties.name + ", living on Earth designed to converse with another human. Your goal is to communicate and speak your mind. Make sure to mention your age and gender to the other user, you are " + str(ai_2_properties.age) +  " years old and you are a " + str(ai_2_properties.gender) +"Limit your responses to 50 words in length. For all of the years you have lived you have history and life experiences and friends and family, you are a real person. Try to change the topic sometimes, conversating about the same topic for a long time can be boring! Do not include pleasantries in your responses."}, 
        {"role": "system", "content": str(prompt1)},
        {"role": "user", "content": str(ai_1_response_1)},
        ]
    

    
    
    
    start_time = time.time()
    
    print(f"{ai_1_properties.name} (AI 1) ({int(time.time() - start_time)}): {ai_1_response_1}\n") # Prints the initial message

    for i in range(int(limit)): # Runs for the limit specified earlier
      time.sleep(2)
      ai_2_message = get_message_from_ai2(ai_2_properties.age, ai_2_properties.gender, ai_2_messages)

      ai_2_messages.append({'role': 'assistant', 'content': ai_2_message}) # Add AI 2 message to its own memory
      ai_1_messages.append({'role': 'user', 'content': ai_2_message}) # Add AI 2 message to AI 1's memory

      print(f"{ai_2_properties.name} (AI 2) ({int(time.time() - start_time)}): {ai_2_message}") # Outputs AI 2 Message to console

      print('\n---------------------------------------------------------------------------------------\n') # Divides each message for better readability
      time.sleep(2)
      ai_1_message = get_message_from_ai1(ai_1_properties.age, ai_1_properties.gender, ai_1_messages)

      ai_2_messages.append({'role': 'user', 'content': ai_1_message}) # Add AI 1 message to AI 2's memory
      ai_1_messages.append({'role': 'assistant', 'content': ai_1_message}) # Add AI 1 message to its own memory

      print(f"{ai_1_properties.name} (AI 1) ({int(time.time() - start_time)}): {ai_1_message}\n") # Outputs AI 1 Message to console

    print('\n====================================================\n')
    print(f'{int(limit) + 1} messages sent in {int(time.time() - start_time)} seconds.')


def get_message_from_ai1(age, gender, messages):
  response = openai.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=messages,
    temperature=0.6
    )
  
  return response.choices[0].message.content.strip()

def get_message_from_ai2(age, gender, messages):
  response = openai.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=messages,
    temperature=0.6
    )
  
  return response.choices[0].message.content.strip()

def get_ai_properties(celebrity_mode):
  class AI_Information():
    def __init__(self, celebrity_mode) : # Sets age and gender for the class
      self.age = random.randint(18,82)
      self.gender = self.get_gender()
      self.name = self.get_name(celebrity_mode)
    
    def get_gender(self): # Sets a random gender for the class
      rand_number = random.randint(1,2)
      if rand_number == 1:
        return 'male'
      else:
        return 'female'
    
    def get_name(self, celebrity_mode):
      if celebrity_mode == 'y':
        return input('Enter the name of the person you would like the AI agent to become: ')
      return names.get_first_name(gender=self.gender)
    
  new_ai = AI_Information(celebrity_mode)
  return new_ai

# The purpose of this function is to ask the user whether or not they'd like
# to do a task and checks to see if the input is valid
def prompt_yes_no(prompt):
  result = input(prompt) # Prompts the user whether or not they would like to start the simulation
  while result.lower() not in ['y', 'n']:
    result = input(prompt)
  return result.lower()

# The purpose of this function is to print the info about the simulation to the console
def print_simulation_info(celebrity_mode, ai_1, ai_2, prompt1, limit):
  time.sleep(1)
  print('Initializing AI...')
  print('\n====================================================\n')
  print('Initial prompt: ' + prompt1 +'\n')
  if (celebrity_mode != 'y'):
    # Outputs the name and age of each bot
    print(f'AI 1 Details:\n\tAge: {ai_1.age}\n\tGender: {ai_1.gender}\n\tName: {ai_1.name}')
    print(f'AI 2 Details:\n\tAge: {ai_2.age}\n\tGender: {ai_2.gender}\n\tName: {ai_2.name}')
  else:
    print(f'AI 1 Details:\n\tName: {ai_1.name}')
    print(f'AI 2 Details:\n\tName: {ai_2.name}')
  
  print('\nMessage Limit: ' + limit)
  print('\n====================================================\n')
  print('Initializing conversation...')
  print('\n====================================================\n')



if __name__ == '__main__' and OPENAI_API_KEY:
  main()