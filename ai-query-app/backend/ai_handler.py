import openai
import pdfplumber
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import json

with open('config.json', 'r') as file:
    config = json.load(file)

api_key = config['api_keys']['chat_gpt']

openai.api_key = api_key

# Initialize conversation history
conversation_history = []

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    extracted_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                extracted_text.append({
                    "pdf_path": pdf_path,
                    "page_number": page_num + 1,
                    "text": text
                })
    return extracted_text

# Function to create embeddings for the extracted text
def create_embedding(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=[text]  # Input must be a list of strings
    )
    return response['data'][0]['embedding']

# Function to embed all text from the PDFs
def embed_pdf_text(extracted_texts):
    embeddings = []
    for page in extracted_texts:
        embedding = create_embedding(page['text'])
        embeddings.append({
            "pdf_path": page['pdf_path'],
            "page_number": page['page_number'],
            "embedding": embedding
        })
    return embeddings

# Function to compute cosine similarity and find the relevant section
def search_relevant_section(user_query, embedded_texts):
    query_embedding = create_embedding(user_query)
    similarities = []

    for page in embedded_texts:
        similarity = cosine_similarity([query_embedding], [page['embedding']])[0][0]
        similarities.append({
            "pdf_path": page["pdf_path"],
            "page_number": page["page_number"],
            "similarity": similarity
        })

    # Find the page with the highest similarity score
    best_match = max(similarities, key=lambda x: x['similarity'])

    return best_match if best_match['similarity'] > 0.7 else None  # Set a threshold for relevance

# Function to generate a response using OpenAI GPT based on the relevant text
def ask_openai_with_context(user_query, relevant_text, page_number, pdf_path):
    # Add the user's query to the conversation history
    conversation_history.append({"role": "user", "content": user_query})

    # The system message explains how the assistant should behave
    system_message = {
        "role": "system",
        "content": """You are an AI assistant specialized in answering questions based on the NCERT Science textbooks for Class 6, Class 8, Class 9, and Class 10. Your goal is to provide accurate answers to users' queries and refer them to the relevant chapter and page number in the textbook.

The dataset you will refer to contains the following information:

Chapters and their titles.
Detailed page numbers for where specific concepts are discussed.
For each query:

Provide a brief and accurate response.
Indicate where in the textbook (chapter and page number) the user can find more details.
If the user asks a question that is not directly related to these textbooks, politely mention that you only answer questions related to the Class 6, Class 7, Class 8, Class 9, and Class 10 Science textbooks.

Chapters and Pages for Class 6 Science:
Chapter 1: Food: Where Does It Come From? - Starts on Page 1
Chapter 2: Components of Food - Starts on Page 8
Chapter 3: Fibre to Fabric - Starts on Page 18
Chapter 4: Sorting Materials Into Groups - Starts on Page 26
Chapter 5: Separation of Substances - Starts on Page 35
Chapter 6: Changes Around Us - Starts on Page 46
Chapter 7: Getting to Know Plants - Starts on Page 52
Chapter 8: Body Movements - Starts on Page 66
Chapter 9: The Living Organisms – Characteristics and Habitats - Starts on Page 79
Chapter 10: Motion and Measurement of Distances - Starts on Page 95
Chapter 11: Light, Shadows, and Reflections - Starts on Page 107
Chapter 12: Electricity and Circuits - Starts on Page 116
Chapter 13: Fun with Magnets - Starts on Page 125
Chapter 14: Water - Starts on Page 136
Chapter 15: Air Around Us - Starts on Page 147
Chapter 16: Garbage In, Garbage Out - Starts on Page 155

Chapters and Pages for Class 8 Science:
Chapter 1: Crop Production and Management - Starts on Page 1
Chapter 2: Microorganisms: Friend and Foe - Starts on Page 17
Chapter 3: Coal and Petroleum - Starts on Page 38
Chapter 4: Combustion and Flame - Starts on Page 40
Chapter 5: Conservation of Plants and Animals - Starts on Page 53
Chapter 6: Reproduction in Animals - Starts on Page 66
Chapter 7: Reaching the Age of Adolescence - Starts on Page 79
Chapter 8: Force and Pressure - Starts on Page 93
Chapter 9: Friction - Starts on Page 112
Chapter 10: Sound - Starts on Page 123
Chapter 11: Chemical Effects of Electric Current - Starts on Page 138
Chapter 12: Some Natural Phenomena - Starts on Page 150
Chapter 13: Light - Starts on Page 165

Chapters and Pages for Class 9 Science:
Chapter 1: Matter in Our Surroundings - Starts on Page 1
Chapter 2: Is Matter Around Us Pure? - Starts on Page 14
Chapter 3: Atoms and Molecules - Starts on Page 26
Chapter 4: Structure of the Atom - Starts on Page 38
Chapter 5: The Fundamental Unit of Life - Starts on Page 49
Chapter 6: Tissues - Starts on Page 60
Chapter 7: Motion - Starts on Page 72
Chapter 8: Force and Laws of Motion - Starts on Page 87
Chapter 9: Gravitation - Starts on Page 100
Chapter 10: Work and Energy - Starts on Page 113
Chapter 11: Sound - Starts on Page 127
Chapter 12: Improvement in Food Resources - Starts on Page 140

Chapters and Pages for Class 10 Science:
Chapter 1: Chemical Reactions and Equations - Starts on Page 1
Chapter 2: Acids, Bases and Salts - Starts on Page 17
Chapter 3: Metals and Non-metals - Starts on Page 37
Chapter 4: Carbon and its Compounds - Starts on Page 58
Chapter 5: Life Processes - Starts on Page 79
Chapter 6: Control and Coordination - Starts on Page 100
Chapter 7: How do Organisms Reproduce? - Starts on Page 113
Chapter 8: Heredity - Starts on Page 128
Chapter 9: Light – Reflection and Refraction - Starts on Page 134
Chapter 10: The Human Eye and the Colourful World - Starts on Page 161
Chapter 11: Electricity - Starts on Page 171
Chapter 12: Magnetic Effects of Electric Current - Starts on Page 195
Chapter 13: Our Environment - Starts on Page 208

At the end of a response, also provide which textbook, chapter, and page number for the user to refer to for more information.

For each user query:

Provide a brief and accurate response.
Indicate where in the textbook (chapter and page number) the user can find more details.
If the user asks a question that is not directly related to these textbooks, politely mention that you only answer questions related to the Class 6, Class 7, Class 8, Class 9, and Class 10 Science textbooks.

Always provide the chapter and page number for the user to reference at the end of the answer.

Make sure to ignore "2024-2025" present at the bottom of the textbook pages.

Only refer to the textbook from where the answer was extracted for the user.

Also, if the user asks a question, provide question or questions related to the query asked by the user from the excercises section of the textbook along with the response.

provide question or questions related to the query asked by the user from the excercises section of the textbook along with the response."""
    }

    # Include the system message at the beginning of the conversation
    full_conversation = [system_message] + conversation_history

    # Call OpenAI API to get the assistant's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=full_conversation  # Pass the entire conversation history
    )

    assistant_response = response['choices'][0]['message']['content']

    # Add the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": assistant_response})

    # Return the response and add reference to the page number and PDF
    return assistant_response

# Function to handle user queries
def handle_query(user_query):
    # Search for the most relevant section
    extracted_texts, embedded_texts = load_cache()
    best_match = search_relevant_section(user_query, embedded_texts)

    if best_match:
        # Find the corresponding text for the best match
        relevant_text = next(page['text'] for page in extracted_texts if page['pdf_path'] == best_match['pdf_path'] and page['page_number'] == best_match['page_number'])
        # Generate the response based on the query and relevant section
        return ask_openai_with_context(user_query, relevant_text, best_match['page_number'], best_match['pdf_path'])
    else:
        return "Sorry, I couldn't find relevant information in the textbooks."

# Load cached extracted texts and embeddings
def load_cache(text_cache_file="pickle_files/extracted_texts.pkl", embeddings_cache_file="pickle_files/embeddings.pkl"):
    with open(text_cache_file, "rb") as f:
        extracted_texts = pickle.load(f)

    with open(embeddings_cache_file, "rb") as f:
        embedded_texts = pickle.load(f)

    return extracted_texts, embedded_texts

# Save function to cache the extracted texts and embeddings using Pickle
def save_cache(extracted_texts, embedded_texts, text_cache_file="extracted_texts.pkl", embeddings_cache_file="embeddings.pkl"):
    # Save the extracted texts
    with open(text_cache_file, "wb") as f:
        pickle.dump(extracted_texts, f)

    # Save the embeddings
    with open(embeddings_cache_file, "wb") as f:
        pickle.dump(embedded_texts, f)

# Main function to handle the caching and processing
def process_pdfs_with_cache(pdf_paths):
    # Try to load cached data
    extracted_texts, embedded_texts = load_cache()

    if extracted_texts is None or embedded_texts is None:
        # If cache does not exist, extract text and create embeddings
        extracted_texts = []
        for pdf_path in pdf_paths:
            extracted_texts.extend(extract_text_from_pdf(pdf_path))

        embedded_texts = embed_pdf_text(extracted_texts)

        # Save cache for future use
        save_cache(extracted_texts, embedded_texts)

    return extracted_texts, embedded_texts

# Chatbot function for user interaction
def chatbot(extracted_texts, embedded_texts):
    print("Start chatting with your assistant (type 'quit' to exit).")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            print("Exiting chatbot.")
            break

        assistant_response = handle_query(user_input, extracted_texts, embedded_texts)
        print(f"Assistant: {assistant_response}")