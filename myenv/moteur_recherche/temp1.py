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
from rdflib import Graph, Namespace, RDF

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
       
def query_disease_info(file_path, disease_name):
    # Créer un objet Graph pour charger le fichier RDF
    g = Graph()

    # Charger les données RDF depuis le fichier
    g.parse(file_path, format="xml")

    # Définir les namespaces utilisés dans le fichier RDF
    ex = Namespace("http://www.example.com/")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    # Construire la requête SPARQL pour récupérer les informations sur la maladie spécifique
    query = f"""
        PREFIX ex: <{ex}>
        SELECT ?label ?comment ?symptom
        WHERE {{
            ?disease rdf:type ex:Disease ;
                     rdfs:label ?label ;
                     rdfs:comment ?comment .
            OPTIONAL {{ ?disease ex:hasSymptom ?symptom . }}
            FILTER (str(?label) = "{disease_name}")
        }}
    """

    # Exécuter la requête SPARQL
    results = g.query(query)

# Store the results in a dictionary
    disease_info = {}
    for row in results:
        disease_info['Label'] = row.label
        disease_info['Comment'] = row.comment
        if row.symptom:
            disease_info['Symptom'] = row.symptom

    return disease_info


def disease_info_view(request):
    if request.method == 'POST':
        form_data = request.POST
        disease_name = form_data['disease_name']

        file_path = "static/liste_maladie.rdf"
        disease_info = query_disease_info(file_path, disease_name)

        context = {
            'disease_info': disease_info,
            'disease_name': disease_name
        }
        print(context)

        return render(request, 'testin.html', context)

    return render(request, 'testin.html')