# Disease Search Engine

This project is a disease search engine designed to operate through a chatbot interface, enabling users to receive immediate and accurate health information. Users can input symptoms, and the search engine leverages advanced technology to diagnose and provide detailed information about the corresponding disease.

## Implementation Methods

1. **Dialogflow Integration**: We utilized Dialogflow, a Google-owned platform that supports the creation of conversational interfaces using natural language processing (NLP). This integration allows our chatbot to understand and respond to user queries effectively, simulating a real conversation. This ensures that users receive a seamless and interactive experience as they seek health advice.

2. **Custom RDF (Resource Description Framework) Document**: We developed a custom RDF document, which is a standard model for data interchange on the web. RDF has features that facilitate data merging even if the underlying schemas differ, and it specifically supports the evolution of schemas over time without requiring all the data consumers to be changed. This RDF document acts as a robust knowledge base for our chatbot, enabling it to accurately interpret user symptoms and provide reliable diagnoses.

## Tech Stack
1. Django
2. Bootstrap
3. DialogFlow
4. RDF
