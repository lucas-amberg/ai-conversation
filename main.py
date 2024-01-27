import os
import openai

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)

def main():
  user_start = input('Would you like to run the simulation [y/n]?: ')
  while user_start.lower() not in ['y', 'n']:
    user_start = input('Would you like to run the simulation [y/n]?: ')
  if user_start.lower() == 'y':
    pass

if __name__ == '__main__' and OPENAI_API_KEY:
  main()