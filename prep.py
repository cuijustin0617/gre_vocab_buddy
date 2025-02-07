from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

def generate_word_data(word):
    prompt = f'''Generate for the word '{word}':
    1. A concise dictionary-style definition
    2. A short, easier-to-understand definition
    3. 3 example sentences (varying difficulty, academic context)
    4. 3 synonyms
    Format as JSON with keys: def_dict, def_simple, examples, synonyms
    e.g.
    {{
        "word": "word",
        "def_dict": "definition",
        "def_simple": "simple definition",
        "examples": ["example1", "example2", "example3"],
        "synonyms": ["synonym1", "synonym2", "synonym3"]
    }}
    return the JSON itself, nothing else.
    '''
    
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Debug print to see raw response
    print(f"Raw response content: {response.choices[0].message.content}")
    
    max_retries = 4
    for attempt in range(max_retries):
        try:
            # Parse the content attribute of the message, which contains the JSON string
            data = json.loads(response.choices[0].message.content.strip('```json\n').strip('```'))
            return {
                "word": word,
                "def_dict": data["def_dict"], 
                "def_simple": data["def_simple"],
                "examples": data["examples"],
                "synonyms": data["synonyms"]
            }
        except:
            if attempt < max_retries - 1:
                print(f"Error processing {word}, retrying attempt {attempt + 2}/{max_retries}")
                continue
            else:
                print(f"Failed to process {word} after {max_retries} attempts")
                return None

def run_prep():
    # Load existing word data if available
    word_data = {}
    if os.path.exists("data/word_data.json"):
        try:
            with open("data/word_data.json", "r") as f:
                content = f.read().strip()
                if content:  # Check if file is not empty
                    word_data = json.load(f)
        except json.JSONDecodeError:
            print("Warning: word_data.json was corrupted or empty. Starting fresh.")
            word_data = {}
    
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Load words from input file
    with open("data/words.txt") as f:
        words = [w.strip() for w in f.readlines()]
    
    # Process only new words
    for word in words:
        if word not in word_data:
            print(f"Processing new word: {word}")
            data = generate_word_data(word)
            if data:
                word_data[word] = data
                # Checkpoint: save after each word
                with open("data/word_data.json", "w") as f:
                    json.dump(word_data, f, indent=2)
        else:
            print(f"Skipping existing word: {word}")
    
    print("Word processing complete!")

if __name__ == "__main__":
    run_prep()