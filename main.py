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
root.title('AI Conversation by Lucas Amberg')
root.resizable(False, False)
mainframe = tk.Frame(root, background='white')
mainframe.pack(fill='both', expand=True)

API_KEY = None

def main():
  openai.api_key = API_KEY  # Initializes AI
  print('ran main')

  # celebrity_mode = prompt_yes_no('Would you like to enter celebrity mode [y/n]?: ')
  celebrity_mode = prompt_yes_no('Would you like to enter celebrity mode?', 17)
  print('celeb mode main ', celebrity_mode)

  random_changes = prompt_yes_no('Would you like random changes to take place in the coversation?', 14)
  print('random main ', random_changes)

  # Sets the random age and gender of each AI bot
  ai_1_properties = get_ai_properties(celebrity_mode)
  ai_2_properties = get_ai_properties(celebrity_mode)

  print('ai1 ', ai_1_properties.name)
  print('ai2 ', ai_2_properties.name)

  limit = get_text('Set the amount of messages you\'d like the bots to have', 14)
  while not limit.isdigit():
    limit = get_text('Set the amount of messages you\'d like the bots to have', 14)
  
  # User enters an initial prompt to sort of guide the conversation
  prompt1 = get_text(f'Enter an initial prompt to get the conversation going ({ai_2_properties.name} -> {ai_1_properties.name})', 13)

  
  log_file = open(f'./logs/{ai_1_properties.name.replace(' ','_')}_and_{ai_2_properties.name.replace(' ','_')}_{time.time()}_conversation-log.txt', 'x')
  print('log made')
  clear_mainframe()

  root.title(f'{ai_1_properties.name} and {ai_2_properties.name} are having a conversation | AI Conversation by Lucas Amberg')

  brief_text_popup('Starting Conversation... Please wait for result...', f'{ai_1_properties.name} and {ai_2_properties.name} are currently having a conversation. This may take a moment.', 500)

  global canvas
  canvas = tk.Canvas(mainframe, width=560, height=400)
  canvas.pack(fill='both', side='left', expand=1)

  scrollbar = ttk.Scrollbar(mainframe, orient='vertical', command=canvas.yview)
  scrollbar.pack(side='right', fill='y')

  canvas.config(yscrollcommand=scrollbar.set)
  canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

  global secondframe
  secondframe = tk.Frame(canvas)

  canvas.create_window((0,0), window=secondframe, anchor='nw')


  

  print_simulation_info(celebrity_mode, ai_1_properties, ai_2_properties, prompt1, limit, log_file) # Prints the simulation info

  if celebrity_mode == 'y':
    ai_1_response_1 = get_message_from_ai1([{"role": "system", "content": "Act like you are " + ai_1_properties.name + " and never leave that role, even if you are asked for.Do not include pleasantries in your responses."}, {'role': 'user', 'content': prompt1}])
    print('message got')
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
    print('message got')
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
  print('clock started')
  add_to_gui_and_log(f"{ai_1_properties.name} (AI 1) ({int(time.time() - start_time)}:0): {ai_1_response_1}\n", log_file) # Prints the initial message
  random_seed = random.randint(1,2) # Changes the random seed for random conversation switches

  happened_last = 0
  for i in range(int(limit)): # Runs for the limit specified earlier
    
    root.after(2000) # Sleep for 2 seconds so things don't get spammed
    ai_2_message = get_message_from_ai2(ai_2_messages) # Gets message for AI 2 from API

    ai_2_messages.append({'role': 'assistant', 'content': ai_2_message}) # Add AI 2 message to its own memory
    ai_1_messages.append({'role': 'user', 'content': ai_2_message}) # Add AI 2 message to AI 1's memory


    add_to_gui_and_log(f"{ai_2_properties.name} (AI 2) ({int(time.time() - start_time)}:{i+1}): {ai_2_message}", log_file) # Outputs AI 2 Message to console
    add_to_gui_and_log('\n---------------------------------------------------------------------------------------\n', log_file) # Divides each message for better readability
    root.after(2000) # Sleep for 2 seconds so things don't get spammed

    random_conversation_switcher = random.randint(1,2) # Sets the random number for this iteration which will determine if the conversation topic will get changed

    if random_changes == 'n':
      random_conversation_switcher = 0 # Makes it impossible for the random changes to take place

    # Will have AI 1 change the topic if the random_conversation_switcher matches the seed for random changes
    if random_conversation_switcher == random_seed and happened_last + 3 <= i:
      add_to_gui_and_log(f'Suddenly... a random force makes {ai_1_properties.name} want to talk about something else...', log_file)
      if random.randint(1,2) == 1:
        ai_1_messages.append({'role': 'system', 'content': 'You must ask them to talk about something else.'})
      else:
        ai_1_messages.append({'role': 'system', 'content': 'You must come up with something else to talk about.'})
      happened_last = i # Will make sure that the random changes dont happen too often
      add_to_gui_and_log('\n---------------------------------------------------------------------------------------\n', log_file)

    
    ai_1_message = get_message_from_ai1(ai_1_messages)

    ai_2_messages.append({'role': 'user', 'content': ai_1_message}) # Add AI 1 message to AI 2's memory
    ai_1_messages.append({'role': 'assistant', 'content': ai_1_message}) # Add AI 1 message to its own memory

    add_to_gui_and_log(f"{ai_1_properties.name} (AI 1) ({int(time.time() - start_time)}:{i+1}): {ai_1_message}\n", log_file) # Outputs AI 1 Message to console

    # Will have AI 2 change the topic if the random_conversation_switcher matches the seed for random changes
    if random_conversation_switcher == random_seed and happened_last + 3 <= i:
      add_to_gui_and_log('\n---------------------------------------------------------------------------------------\n', log_file)
      add_to_gui_and_log(f'Suddenly... a random force makes {ai_2_properties.name} want to talk about something else...', log_file)
      if random.randint(1,2) == 1:
        ai_2_messages.append({'role': 'system', 'content': 'You must ask them to talk about something else.'})
      else:
        ai_2_messages.append({'role': 'system', 'content': 'You must come up with something else to talk about.'})
      happened_last = i
      add_to_gui_and_log('\n---------------------------------------------------------------------------------------\n', log_file)

  ai_2_message = get_message_from_ai2(ai_2_messages)
  add_to_gui_and_log(f"{ai_2_properties.name} (AI 2) ({int(time.time() - start_time)}:{i+1}): {ai_2_message}", log_file) # Outputs AI 2 Message to console

  add_to_gui_and_log('\n====================================================\n', log_file)
  add_to_gui_and_log(f'{int(limit) + 1} messages sent in {int(time.time() - start_time)} seconds.', log_file)
  root.title(f'{ai_1_properties.name} and {ai_2_properties.name} had a conversation | AI Conversation by Lucas Amberg')
  

# Asks the user if they want to use Celebrity Mode
def prompt_yes_no(prompt, font_size):
  text = ttk.Label(mainframe, text=prompt, wraplength=550, background='white', font=('Brass Mono', font_size), justify='center')
  text.place(relx=.5, rely=.4, anchor="c")
  answer = tk.StringVar(value='y')
  answer_button_clicked = tk.StringVar()
  radio_button_yes = ttk.Radiobutton(mainframe, text='Yes', variable=answer, value='y')
  radio_button_no = ttk.Radiobutton(mainframe, text='No', variable=answer, value='n')
  radio_button_yes.place(relx=.4, rely=.55, anchor="c")
  radio_button_no.place(relx=.6, rely=.55, anchor="c")
  submit_yes_no = ttk.Button(mainframe, text='Submit Choice', command=lambda: answer_button_clicked.set('clicked'))
  submit_yes_no.place(relx=.5, rely=.7, anchor="c")
  submit_yes_no.wait_variable(answer_button_clicked)
  clear_mainframe()
  return answer.get()

def get_text(prompt, font_size):
  text = ttk.Label(mainframe, text=prompt, wraplength=550, background='white', font=('Brass Mono', font_size), justify='center')
  text.place(relx=.5, rely=.4, anchor="c")
  answer_button_clicked = tk.StringVar()
  text_input = ttk.Entry(mainframe, width=70)
  text_input.place(relx=.5, rely=.6, anchor="c")
  submit_input = ttk.Button(mainframe, text='Submit Choice', command=lambda: answer_button_clicked.set('clicked'))
  submit_input.place(relx=.5, rely=.7, anchor="c")
  submit_input.wait_variable(answer_button_clicked)
  result = text_input.get()
  clear_mainframe()
  return result

def add_to_gui_and_log(text, log_file):
  text_gui = ttk.Label(secondframe, text=text, background='white', font=('Brass Mono', 12), justify='left', padding=4, width=600, wraplength=560)
  text_gui.pack()
  log_file.write(text)

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

def brief_text_popup(main_text, sub_text, popup_time):
  starting_var = tk.StringVar()
  starting_text = ttk.Label(mainframe, wraplength=550, text=main_text, background='white', font=('Brass Mono', 14), justify='center')
  starting_subtext = ttk.Label(mainframe, wraplength=550, text=sub_text, background='white', font=('Brass Mono', 10), justify='center')
  starting_text.place(relx=0.5, rely=0.4, anchor='c')
  starting_subtext.place(relx=0.5, rely=0.6, anchor='c')

  root.after(popup_time, func=lambda: starting_var.set('starting'))
  starting_text.wait_variable(starting_var)
  clear_mainframe()

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
        return get_text('Enter the name of the person you would like the AI agent to become: ', 13)
      return names.get_first_name(gender=self.gender)
    
  new_ai = AI_Information(celebrity_mode)
  return new_ai

# # The purpose of this function is to ask the user whether or not they'd like
# # to do a task and checks to see if the input is valid
# def prompt_yes_no(prompt):
#   result = input(prompt) # Prompts the user whether or not they would like to start the simulation
#   while result.lower() not in ['y', 'n']:
#     result = input(prompt)
#   return result.lower()

# The purpose of this function is to print the info about the simulation to the console
def print_simulation_info(celebrity_mode, ai_1, ai_2, prompt1, limit, log_file):
  root.after(1000)
  add_to_gui_and_log('Initializing AI...', log_file)
  add_to_gui_and_log('\n====================================================\n', log_file)
  add_to_gui_and_log(f'Initial prompt ({ai_2.name} -> {ai_1.name}): ' + prompt1 +'\n', log_file)
  if (celebrity_mode != 'y'):
    # Outputs the name and age of each bot
    add_to_gui_and_log(f'AI 1 Details:\n\tAge: {ai_1.age}\n\tGender: {ai_1.gender}\n\tName: {ai_1.name}', log_file)
    add_to_gui_and_log(f'\nAI 2 Details:\n\tAge: {ai_2.age}\n\tGender: {ai_2.gender}\n\tName: {ai_2.name}', log_file)
    add_to_gui_and_log(f'\nCelebrity Mode: Disabled', log_file)
  else:
    add_to_gui_and_log(f'AI 1 Details:\n\tName: {ai_1.name}', log_file)
    add_to_gui_and_log(f'AI 2 Details:\n\tName: {ai_2.name}', log_file)
    add_to_gui_and_log(f'\nCelebrity Mode: Enabled', log_file)
  
  add_to_gui_and_log('\nMessage Limit: ' + limit, log_file)
  add_to_gui_and_log('\n====================================================\n', log_file)
  add_to_gui_and_log('Initializing conversation...', log_file)
  add_to_gui_and_log('\n====================================================\n', log_file)

# Prints and writes a string to a file at the same time
# def add_to_gui_and_log(text, log_file):
#   print(text)
#   log_file.write(text)

# This function will get the OpenAI API Key from the user or it will
# Get it from the env variables
def get_openai_key():
  r = tk.StringVar()
  text = ttk.Label(mainframe, text='Please select an option to use an OpenAI API Key', background='white', font=('Brass Mono', 17), justify='center')
  text.grid(row=0, column=0)
  text.place(relx=.5, rely=.4, anchor="c")
  env_button = ttk.Button(mainframe, text='Get From Environment Variable', padding=20, width=20, command=lambda: get_from_env(r))
  input_button = ttk.Button(mainframe, text='Input Key', padding=20, width=20, command=lambda: get_from_input(r))
  env_button.place(relx=.3, rely=.6, anchor='c')
  input_button.place(relx=.7, rely=.6, anchor='c')
  input_button.wait_variable(r)

# Gets the environment variable
def get_from_env(r):
  global API_KEY
  clear_mainframe()
  API_KEY = os.environ.get('OPENAI_API_KEY', None)
  r.set('pressed')

# Gets the API key from input
def get_from_input(r):
  clear_mainframe()
  text = ttk.Label(mainframe, text='Please input your OpenAI API Key', background='white', font=('Brass Mono', 17), justify='center')
  text.grid(row=0, column=0)
  text.place(relx=.5, rely=.4, anchor="c")
  input_box = ttk.Entry(mainframe, width=70)
  input_box.place(relx=.5, rely=.5, anchor='c')
  input_button = ttk.Button(mainframe, width=20, padding=20, text='Submit Key', command=lambda: validate_key(input_box, r))
  input_button.place(relx=.5, rely=.65, anchor='c')

def validate_key(input_box, r):
  global API_KEY
  key_from_box = input_box.get()
  match = re.search(r"^sk-[a-zA-Z0-9]{32,}$", key_from_box)
  invalid_input = ttk.Label(mainframe, text='Your Input Was Invalid, Please Try Again', background='white', foreground='red', font=('Brass Mono', 12), justify='center')
  invalid_input.place(relx=.5, rely=.8, anchor='c')
  invalid_input.grid_remove()
  if not match:
    invalid_input.pack()
  else:
    API_KEY = key_from_box
    clear_mainframe()
    r.set('pressed')

  
# Clears the mainframe
def clear_mainframe():
  for widget in mainframe.winfo_children():
    widget.destroy() # Clears the frame

if __name__ == '__main__':
  brief_text_popup('Welcome to AI Conversation', 'By Lucas Amberg', 2000)
  brief_text_popup('Using OpenAI API', '(A Conversation Will Cost Typically $0.01-$0.10)', 2000)
  get_openai_key()
  if API_KEY != None:
    main()
  else:
    text=ttk.Label(mainframe, text='No API Key Was Found In Your ENV Variables', background='white', foreground='red', font=('Brass Mono', 12), justify='center')
  root.mainloop()