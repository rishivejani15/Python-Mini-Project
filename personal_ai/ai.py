from dotenv import load_dotenv
load_dotenv()
import pathlib
import textwrap
import os
import google.generativeai as genai
from IPython.display import display
from IPython.display import Markdown

def ask_ques():
  ques=input('\nHey, how can I assist you ? \n')
  return ques

def classify_question(ques):
  goahead_with_web_search=False
  device_lst=['alarm','reminder','call','message']
  personal_ques_lst=['who are you','who created you','what is your name']
  device=False
  for i in device_lst:
    if i in ques:
      device=True

  if device:
    print('Sorry, but cannnt perform device related tasks.')

  personal_question=False
  for i in personal_ques_lst:
    if i in ques.lower():
      personal_question=True

  if personal_question:
      print('I am Jarvis, created by CodeMonks')

  if device:
    goahead_with_web_search=False
  elif personal_question:
    goahead_with_web_search=False
  else:
    goahead_with_web_search=True
  return goahead_with_web_search

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

def ask_gemini(ques):
  modified_prompt='Hey give me answer to this question '+ques+' in maximum of 50 words'
  response = model.generate_content(modified_prompt)
  to_markdown(response.text)
  return response.text

have_any_other_ques='yes'
while have_any_other_ques=='yes':
  q=ask_ques()
  go_ahead=classify_question(q)
  answer=''

  if go_ahead==True:
    answer= ask_gemini(q)
    print(answer)

  have_any_other_ques=input('Do you have any other questions (yes/no) ?')