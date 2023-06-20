from google.cloud import dialogflow_v2 as dialogflow

# Set up credentials
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'

# Create a session client
session_client = dialogflow.SessionsClient()

# Set up session variables
project_id = 'your-project-id'
session_id = 'your-session-id'
language_code = 'en-US'

# Define the query text
query_text = 'Hello!'

# Set up the session path
session_path = session_client.session_path(project_id, session_id)

# Set up the query input
text_input = dialogflow.TextInput(text=query_text, language_code=language_code)
query_input = dialogflow.QueryInput(text=text_input)

# Send the query
response = session_client.detect_intent(session=session_path, query_input=query_input)

# Print the response
print(response.query_result.fulfillment_text)
