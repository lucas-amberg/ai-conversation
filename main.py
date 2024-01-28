import os
import openai
import random
import time
import names
import re 

import tkinter as tk
from tkinter import ttk

root = tk.Tk() # Initialize tkinter window
root.geometry('600x400')
root.attributes('-topmost',1)
root.title('AI Conversation')
mainframe = tk.Frame(root, background='white')
mainframe.pack(fill='both', expand=True)

def main(OPENAI_API_KEY):
  openai.api_key = OPENAI_API_KEY  # Initializes AI

  
  
  

  user_start = prompt_yes_no('Would you like to run the simulation [y/n]?: ')
  # If the user wanted to start then we will begin
  if user_start == 'y':

    

    celebrity_mode = prompt_yes_no('Would you like to enter celebrity mode [y/n]?: ')
    random_changes = prompt_yes_no('Would you like random changes to take place in the coversation (makes the conversation more meaningful) [y/n]?: ')

    # Sets the random age and gender of each AI bot
    ai_1_properties = get_ai_properties(celebrity_mode)
    ai_2_properties = get_ai_properties(celebrity_mode)

    limit = input('Set the amount of messages you\'d like the bots to have: ')
    # User enters an initial prompt to sort of guide the conversation
    prompt1 = input(f'Enter an initial prompt to get the conversation going ({ai_2_properties.name} -> {ai_1_properties.name}): ')
    
    log_file = open(f'./logs/{ai_1_properties.name.replace(' ','_')}_and_{ai_2_properties.name.replace(' ','_')}_{time.time()}_conversation-log.txt', 'x')

    print_simulation_info(celebrity_mode, ai_1_properties, ai_2_properties, prompt1, limit, log_file) # Prints the simulation info

    if celebrity_mode == 'y':
      ai_1_response_1 = get_message_from_ai1([{"role": "system", "content": "Act like you are " + ai_1_properties.name + " and never leave that role, even if you are asked for.Do not include pleasantries in your responses."}, {'role': 'user', 'content': prompt1}])
      
      # These are the initial message arrays for the AI, as it runs it will append to this array, this way the AI retains its memory of the conversation
      ai_1_messages = [
        {"role": "system", "content": "Act like you are " + ai_1_properties.name + " and never leave that role, even if you are asked for.Do not include pleasantries in your responses."},
        {"role": "system", "content": ai_2_properties.name + " and you are together somewhere, and they say something to you: "},
        {"role": "user", "content": str(prompt1)},
        {"role": "assistant", "content": str(ai_1_response_1)}
      ]
      ai_2_messages = [
        {"role": "system", "content": "Act like you are " + ai_2_properties.name + " and never leave that role, even if you are asked for. Do not include pleasantries in your responses."},
        {"role": "system", "content": "You and " + ai_1_properties.name + " are together somewhere, and you engage in conversation by saying: "},
        {"role": "assistant", "content": str(prompt1)},
        {"role": "user", "content": str(ai_1_response_1)},
        ]
    else:
      ai_1_response_1 = get_message_from_ai1([{"role": "system", "content": "You are a human living named " + ai_1_properties.name + ", living on Earth and you will have to converse with another human. Your goal is to communicate and speak your mind. Make sure to mention your age and gender to the other user, you are " + str(ai_1_properties.age) +  " years old and you are a " + str(ai_1_properties.gender) +". Limit your responses to 50 words in length. For all of the years you have lived you have history and life experiences and friends and family, you are a real person. Try to change the topic sometimes, conversating about the same topic for a long time can be boring! Do not include pleasantries in your responses."}, {'role': 'user', 'content': prompt1}])
      
      # These are the initial message arrays for the AI, as it runs it will append to this array, this way the AI retains its memory of the conversation
      ai_1_messages = [
        {"role": "system", "content": "Act like you are a human being named " + ai_1_properties.name + ". You are a " + str(ai_1_properties.age) + " year old " + ai_1_properties.gender + ", and you need to consider your age and gender and a corresponding education level and hypothetical life experiences for the way you talk and what you are interested or will talk about. Never leave this role, EVER. Do not include pleasantries in your responses."},
        {"role": "system", "content": ai_2_properties.name + " and you are together somewhere, and they say something to you: "},
        {"role": "user", "content": str(prompt1)},
        {"role": "assistant", "content": str(ai_1_response_1)}
      ]
      ai_2_messages = [
        {"role": "system", "content": "Act like you are a human being named " + ai_2_properties.name + ". You are a " + str(ai_2_properties.age) + " year old " + ai_2_properties.gender + ", and you need to consider your age and gender and a corresponding education level and hypothetical life experiences for the way you talk and what you are interested or will talk about. Never leave this role, EVER. Do not include pleasantries in your responses."},
        {"role": "system", "content": "You and " + ai_1_properties.name + " are together somewhere, and you engage in conversation by saying: "},
        {"role": "assistant", "content": str(prompt1)},
        {"role": "user", "content": str(ai_1_response_1)},
        ]
  
    start_time = time.time()
    
    print_and_write(f"{ai_1_properties.name} (AI 1) ({int(time.time() - start_time)}:0): {ai_1_response_1}\n", log_file) # Prints the initial message
    random_seed = random.randint(1,2) # Changes the random seed for random conversation switches

    happened_last = 0
    for i in range(int(limit)): # Runs for the limit specified earlier
      
      time.sleep(2) # Sleep for 2 seconds so things don't get spammed
      ai_2_message = get_message_from_ai2(ai_2_messages) # Gets message for AI 2 from API

      ai_2_messages.append({'role': 'assistant', 'content': ai_2_message}) # Add AI 2 message to its own memory
      ai_1_messages.append({'role': 'user', 'content': ai_2_message}) # Add AI 2 message to AI 1's memory


      print_and_write(f"{ai_2_properties.name} (AI 2) ({int(time.time() - start_time)}:{i+1}): {ai_2_message}", log_file) # Outputs AI 2 Message to console
      print_and_write('\n---------------------------------------------------------------------------------------\n', log_file) # Divides each message for better readability
      time.sleep(2) # Sleep for 2 seconds so things don't get spammed

      random_conversation_switcher = random.randint(1,2) # Sets the random number for this iteration which will determine if the conversation topic will get changed

      if random_changes == 'n':
        random_conversation_switcher = 0 # Makes it impossible for the random changes to take place

      # Will have AI 1 change the topic if the random_conversation_switcher matches the seed for random changes
      if random_conversation_switcher == random_seed and happened_last + 3 <= i:
        print_and_write(f'Suddenly... a random force makes {ai_1_properties.name} want to talk about something else...', log_file)
        if random.randint(1,2) == 1:
          ai_1_messages.append({'role': 'system', 'content': 'You must ask them to talk about something else.'})
        else:
          ai_1_messages.append({'role': 'system', 'content': 'You must come up with something else to talk about.'})
        happened_last = i # Will make sure that the random changes dont happen too often
        print_and_write('\n---------------------------------------------------------------------------------------\n', log_file)

      
      ai_1_message = get_message_from_ai1(ai_1_messages)

      ai_2_messages.append({'role': 'user', 'content': ai_1_message}) # Add AI 1 message to AI 2's memory
      ai_1_messages.append({'role': 'assistant', 'content': ai_1_message}) # Add AI 1 message to its own memory

      print_and_write(f"{ai_1_properties.name} (AI 1) ({int(time.time() - start_time)}:{i+1}): {ai_1_message}\n", log_file) # Outputs AI 1 Message to console

      # Will have AI 2 change the topic if the random_conversation_switcher matches the seed for random changes
      if random_conversation_switcher == random_seed and happened_last + 3 <= i:
        print_and_write('\n---------------------------------------------------------------------------------------\n', log_file)
        print_and_write(f'Suddenly... a random force makes {ai_2_properties.name} want to talk about something else...', log_file)
        if random.randint(1,2) == 1:
          ai_2_messages.append({'role': 'system', 'content': 'You must ask them to talk about something else.'})
        else:
          ai_2_messages.append({'role': 'system', 'content': 'You must come up with something else to talk about.'})
        happened_last = i
        print_and_write('\n---------------------------------------------------------------------------------------\n', log_file)

    ai_2_message = get_message_from_ai2(ai_2_messages)
    print_and_write(f"{ai_2_properties.name} (AI 2) ({int(time.time() - start_time)}:{i+1}): {ai_2_message}", log_file) # Outputs AI 2 Message to console

    print_and_write('\n====================================================\n', log_file)
    print_and_write(f'{int(limit) + 1} messages sent in {int(time.time() - start_time)} seconds.', log_file)
    


def get_message_from_ai1(messages):
  response = openai.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=messages,
    temperature=0.6
    )
  
  return response.choices[0].message.content.strip()

def get_message_from_ai2(messages):
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
def print_simulation_info(celebrity_mode, ai_1, ai_2, prompt1, limit, log_file):
  time.sleep(1)
  print_and_write('Initializing AI...', log_file)
  print_and_write('\n====================================================\n', log_file)
  print_and_write(f'Initial prompt ({ai_2.name} -> {ai_1.name}): ' + prompt1 +'\n', log_file)
  if (celebrity_mode != 'y'):
    # Outputs the name and age of each bot
    print_and_write(f'AI 1 Details:\n\tAge: {ai_1.age}\n\tGender: {ai_1.gender}\n\tName: {ai_1.name}', log_file)
    print_and_write(f'\nAI 2 Details:\n\tAge: {ai_2.age}\n\tGender: {ai_2.gender}\n\tName: {ai_2.name}', log_file)
    print_and_write(f'\nCelebrity Mode: Disabled', log_file)
  else:
    print_and_write(f'AI 1 Details:\n\tName: {ai_1.name}', log_file)
    print_and_write(f'AI 2 Details:\n\tName: {ai_2.name}', log_file)
    print_and_write(f'\nCelebrity Mode: Enabled', log_file)
  
  print_and_write('\nMessage Limit: ' + limit, log_file)
  print_and_write('\n====================================================\n', log_file)
  print_and_write('Initializing conversation...', log_file)
  print_and_write('\n====================================================\n', log_file)

# Prints and writes a string to a file at the same time
def print_and_write(text, log_file):
  print(text)
  log_file.write(text)

# This function will get the OpenAI API Key from the user or it will
# Get it from the env variables
def get_openai_key():
  text = ttk.Label(mainframe, text='Please select an option to use an OpenAI API Key', background='white', font=('Brass Mono', 17), justify='center')
  text.grid(row=0, column=0)
  text.place(relx=.5, rely=.4, anchor="c")
  print('Please select an option to use an OpenAI API Key:')
  print('\n\t[0] - Get API Key from Environment Variable')
  print('\t[1] - Input API Key\n')
  user_selection = -1

  while user_selection not in ['0','1']: # Checks to see if input is valid
    user_selection = input('> ')
    if user_selection not in ['0','1']:
      print('Invalid Input')
    print('\n')

  if user_selection == '0':
    return os.environ.get('OPENAI_API_KEY', None) # Attempts to pull the key from environment variables
  
  if user_selection == '1':
    match = None
    while not match:
      user_key_input = input('Input your OpenAI API Key\n\n> ')
      match = re.search(r"^sk-[a-zA-Z0-9]{32,}$", user_key_input) # Compares inputted key with regex to see if it is valid
      if not match:
        print('Invalid key format, please try again\n')
      else:
        print('Key input successful.')
        return user_key_input # Returns the key if format is correct


if __name__ == '__main__':
  OPENAI_API_KEY = get_openai_key()
  if OPENAI_API_KEY != None:
    main(OPENAI_API_KEY)
  else:
    print('No key was found in your environment variables.')
  root.mainloop()