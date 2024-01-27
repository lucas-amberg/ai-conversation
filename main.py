import os
import openai

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)

def main():
  openai.api_key = OPENAI_API_KEY  # Initializes AI
  user_start = input('Would you like to run the simulation [y/n]?: ') # Prompts the user whether or not they would like to start the simulation
  while user_start.lower() not in ['y', 'n']:
    user_start = input('Would you like to run the simulation [y/n]?: ')
  if user_start.lower() == 'y':
    prompt1 = input('Enter an initial prompt to get the conversation going')

def get_message_from_ai1(prompt):
  response = openai.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=[{"role": "system", "content": "You are human being designed to converse with another human. Your goal is to communicate and speak your mind."},
              {'role': 'user', 'content': prompt}]
    )
  
  return response.choices[0].message.content.strip()

def get_message_from_ai2(prompt):
  response = openai.chat.completions.create(
    model = 'gpt-3.5-turbo',
    messages=[{"role": "system", "content": "You are human being designed to converse with another human. Your goal is to communicate and speak your mind."},
              {'role': 'user', 'content': prompt}]
    )
  
  return response.choices[0].message.content.strip()

if __name__ == '__main__' and OPENAI_API_KEY:
  main()