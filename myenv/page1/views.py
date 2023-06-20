from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from google.oauth2 import service_account
from google.cloud import dialogflow_v2 as dialogflow
import os
import json
from google.oauth2 import service_account
from google.cloud.dialogflow_v2.types import TextInput, QueryInput
from google.cloud.dialogflow_v2 import SessionsClient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.templatetags.static import static

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
# It is  request -> response file
# It is a request handler

def gotoindex(request):
    if request.method == 'POST':
        input_value = request.POST.get('input_value')
        return render(request, 'index.html', {'input_value': input_value})
    
    else:
         form = forms.Form()
         return render(request, 'index.html', {'form': form})

def my_view(request):
       if request.method == 'POST':
           input_value = request.POST.get('input_value')
           return render(request, 'testin.html', {'input_value': input_value})
       else:
           form = forms.Form()
           return render(request, 'testin.html', {'form': form})
       

def dialog_flow_Prompt(request):
       if request.method == 'POST':
           file_path  = os.path.join(BASE_DIR, 'static/api1.json')
           # Retrieve user input from form
           prompt = request.POST.get('input_value')
           # Set up credentials and API client
           credentials = service_account.Credentials.from_service_account_file(file_path)
           project_id = 'tuto1-avex'
           session_client = dialogflow.SessionsClient(credentials=credentials)
           session_id = '102933083679047031424'
           language_code = 'en'
           print(credentials)

           # Set up session path
           session_path = session_client.session_path(project_id, session_id)

           # Set up query input
           text_input = dialogflow.types.TextInput(text=prompt, language_code=language_code)
           query_input = dialogflow.types.QueryInput(text=text_input)

           # Send the query
           response = session_client.detect_intent(session=session_path, query_input=query_input)

           # Get fulfillment text from response
           fulfillment_text = response.query_result.fulfillment_text

           # Pass fulfillment text to template
           return render(request, 'index.html', {'fulfillment_text': fulfillment_text, 'input_value': prompt})
       else:
           # Render form template for GET requests
           return render(request, 'index.html')
