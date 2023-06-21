from django.shortcuts import render
from django import forms
from rdflib import Graph, Namespace

from google.oauth2 import service_account
from google.cloud import dialogflow_v2 as dialogflow
from google.cloud.dialogflow_v2.types import TextInput, QueryInput

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the form for the disease name input
class DiseaseForm(forms.Form):
    disease_name = forms.CharField(label='Disease Name', max_length=100)

# Define the function to perform the Dialogflow treatment
def dialog_flow_prompt(session_id, prompt):
    # Set up credentials and API client
    file_path = os.path.join(BASE_DIR, 'static/api1.json')
    credentials = service_account.Credentials.from_service_account_file(file_path)
    project_id = 'tuto1-avex'
    session_client = dialogflow.SessionsClient(credentials=credentials)
    language_code = 'fr'

    # Set up session path
    session_path = session_client.session_path(project_id, session_id)

    # Set up query input
    text_input = TextInput(text=prompt, language_code=language_code)
    query_input = QueryInput(text=text_input)

    # Send the query
    response = session_client.detect_intent(session=session_path, query_input=query_input)

    # Get fulfillment text from response
    fulfillment_text = response.query_result.fulfillment_text

    return fulfillment_text

# Define the function to perform the RDF treatment
def query_disease_info(file_path, disease_name):
    try:
        # Create a Graph object to load the RDF file
        g = Graph()

        # Load RDF data from file
        g.parse(file_path, format="xml")

        # Define the namespaces used in the RDF file
        ex = Namespace("http://www.example.com/")
        rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

        # Build the SPARQL query to retrieve information about the specific disease
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

        # Execute the SPARQL query
        results = g.query(query)

        # Store the results in a dictionary
        disease_info = {}
        for row in results:
            if results is not None:
                disease_info['Label'] = row.label
                disease_info['Comment'] = row.comment
                if row.symptom:
                    disease_info['Symptom'] = row.symptom
            else:
               errorMsg = "No results"

        return disease_info
    except:
        return None

# Define the view function for the disease info page
def disease_info_view(request):
    if request.method == 'POST':
        # Retrieve user input from form
        form = DiseaseForm(request.POST)
        if form.is_valid():
            disease_name = form.cleaned_data['disease_name']

            # Perform the RDF and Dialogflow treatments
            file_path = os.path.join(BASE_DIR, 'static/liste_maladie.rdf')
            disease_info = query_disease_info(file_path, disease_name)

            session_id = '102933083679047031424'
            fulfillment_text = dialog_flow_prompt(session_id, disease_name)

            # Pass the results to the template
            context = {
                'disease_info': disease_info,
                'disease_name': disease_name,
                'fulfillment_text': fulfillment_text
            }

            return render(request, 'index.html', context)

    # Render the form template for GET requests
    form = DiseaseForm()
    context = {'form': form}
    return render(request, 'index.html', context)

def disease_info_viewV2(request):
    if request.method == 'POST':
        # Retrieve user input from form
        form = DiseaseForm(request.POST)
        if form.is_valid():
            disease_name = form.cleaned_data['disease_name']

            # Perform the RDF and Dialogflow treatments
            file_path = os.path.join(BASE_DIR, 'static/liste_maladie.rdf')
            disease_info = query_disease_info(file_path, disease_name)

            session_id = '102933083679047031424'
            fulfillment_text = dialog_flow_prompt(session_id, disease_name)

            # Pass the results to the template
            context = {
                'disease_info': disease_info,
                'disease_name': disease_name,
                'fulfillment_text': fulfillment_text
            }

            return render(request, 'testin.html', context)
        

    # Render the form template for GET requests
    form = DiseaseForm()
    context = {'form': form}
    return render(request, 'testin.html', context)
