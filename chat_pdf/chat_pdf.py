import os
import tempfile
from dotenv import load_dotenv
from langchain.vectorstores import Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.chains import ConversationalRetrievalChain
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
import openai
import pinecone
import requests

load_dotenv(dotenv_path=".env.template")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Load and split the file
def load_and_split_the_file(url: str):
    print("Loading and spliting the file...")

    # Initialize Pinecone DB
    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment="us-central1-gcp"  # next to api key in console
    )

    # Send a GET request to retrieve the PDF file
    response = requests.get(url)

    # Save the content of the response to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(response.content)
        tempfile_path = tmp_file.name

    print(tempfile_path)
    # Create a document from the pdf file
    loader = PyPDFLoader(tempfile_path)

    # Split the document into chunks
    docs = loader.load_and_split()

    return docs, tempfile_path

# Load and vectorize the file
def load_and_vectorize_file(url: str):

    # Get namespace Name
    name_space = url.split("/")[-1].split("?")[0]

    # Set the index name
    index_name = "study-genius"

    # OpenAI embeddings
    embeddings = OpenAIEmbeddings()

    # Get the loaded Document
    docs = load_and_split_the_file(url)

    # Get info from db
    index = pinecone.Index(index_name)
    index_stats_response = index.describe_index_stats()
    namespaces = index_stats_response['namespaces']
    namespaces_list = list(namespaces.keys())

    # Verifies if the namespace exits
    if name_space in namespaces_list:
        print('Namespace already exists')
        
    else:
        print("Loading the file on the vector db...")

        # Store the embeddings in the database
        Pinecone.from_documents(
            docs[0], embeddings, index_name=index_name, namespace=name_space)

# Chat with PDF
def chat_with_pdf(query: str, url: str, chat_history: list | None):
    print("Chating the the pdf...")
  # Initialize Pinecone DB
    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment="us-central1-gcp"  # next to api key in console
    )

    # Set the index name
    index_name = "study-genius"
    index = pinecone.Index(index_name)

    # Get name space name
    name_space = url.split("/")[-1].split("?")[0]
    # Get the vectorstore
    vectorstore = Pinecone(index, OpenAIEmbeddings().embed_query,
                           "text", namespace=name_space)

    # Talk to the LLM
    qa = ConversationalRetrievalChain.from_llm(llm=OpenAI(
        temperature=0), retriever=vectorstore.as_retriever(),)

    # Run the query
    result = qa({"question": query, "chat_history": chat_history})
    print(result['answer'])
    # return the anwser
    return result

# Generate Quiz from PDF
def generate_quiz_from_pdf(url: str):

    print("Generating Quiz Questions....")

    # Set up pinecone db
    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment="us-central1-gcp"  # next to api key in console
    )

    # Set the index name
    index_name = "study-genius"
    index = pinecone.Index(index_name)

    # Get name space name
    name_space = url.split("/")[-1].split("?")[0]

    # Get the vectorstore
    vectorstore = Pinecone(index, OpenAIEmbeddings().embed_query,
                           "text", namespace=name_space)

    # Perform similarity check
    docs = vectorstore.similarity_search(
        "Give me a summary of the file", namespace=name_space)
    anwser_context = docs[0].page_content

    # The GPT Prompt
    gptPrompt = f"I want you to generate 10 quiz and 04 possible options questions and the anwser number. Use the data from this thext : {anwser_context}. Output your response in json format like this one" + ''' "questions":[
      {
         "question":"What is the scientific name of a butterfly?",
         "answers":[
            "Apis",
            "Coleoptera",
            "Formicidae",
            "Rhopalocera"
         ],
         "correctIndex":3
      },
      {
         "question":"How hot is the surface of the sun?",
         "answers":[
            "1,233 K",
            "5,778 K",
            "12,130 K",
            "101,300 K"
         ],
         "correctIndex":1
      },
      {
         "question":"Who are the actors in The Internship?",
         "answers":[
            "Ben Stiller, Jonah Hill",
            "Courteney Cox, Matt LeBlanc",
            "Kaley Cuoco, Jim Parsons",
            "Vince Vaughn, Owen Wilson"
         ],
         "correctIndex":3
      }
   ]
     '''

    # Method for GPT3 (You can use it if you have access to the GPT4 API)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": gptPrompt}
        ]
    )

    print(response.choices[0]["message"]["content"])

    # Return the response
    return response.choices[0]["message"]["content"]

# Generate FlashCard
def generate_flash_cards_from_pdf(url: str):

    pinecone.init(
        api_key=PINECONE_API_KEY,  # find at app.pinecone.io
        environment="us-central1-gcp"  # next to api key in console
    )

    # Set the index name
    index_name = "study-genius"
    index = pinecone.Index(index_name)
    print("Generating Flash Cards....")
    name_space = url.split("/")[-1].split("?")[0]

    vectorstore = Pinecone(index, OpenAIEmbeddings().embed_query,
                           "text", namespace=name_space)
    # Perform similarity check
    docs = vectorstore.similarity_search(
        "Give me a summary of the file", namespace=name_space)
    anwser_context = docs[0].page_content

    # The GPT Prompt
    gptPrompt = f"I want you to generate 10 quiz and the anwser. Only Use the data from this thext : {anwser_context} and utput your response in json format like this one " + ''' "questions":[
    question:[  {
         "question":"What is Archtecture ?",
         "answer": "Architecture, the art and technique of designing and building, as distinguished from the skills associated with construction."
    {
         "question":"What is the Photosynthesis ?",
         "answer": "Photosynthesis is the process used by plants, algae and some bacteria to turn sunlight into energy"
      },
   ]
     '''

    # Method for GPT3 (You can use it if you have access to the GPT4 API)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": gptPrompt}
        ]
    )

    print(response.choices[0]["message"]["content"])

    # Return the response
    return response.choices[0]["message"]["content"]

# Summerize the PDF
def summerize_pdf(tempfile_path: str):

    # Load the documents
    loader = PyPDFLoader(tempfile_path)
    docs = loader.load_and_split()

    llm = OpenAI(temperature=0)

    print('Summarizing the file...')
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run(docs)
    print(summary + '\n')

    os.remove(tempfile_path)
    return summary

# Chat with PDF
def chat_with_ai_genius(query: str, chat_history: list | None):
    print("Chating the the AI Genius...")

    # Talk to the LLM
    qa = ConversationalRetrievalChain.from_llm(llm=OpenAI(
        temperature=0))

    # Run the query
    result = qa({"question": query, "chat_history": chat_history})
    print(result['answer'])
    # return the anwser
    return result
