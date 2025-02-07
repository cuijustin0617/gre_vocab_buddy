# study.py (Daily Study)
import json
import random
from datetime import datetime
import os

def load_memory():
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    try:
        with open("data/memory.json") as f:
            content = f.read()
            return json.loads(content) if content else {}
    except (FileNotFoundError, json.JSONDecodeError):
        # Return empty dict if file doesn't exist or is invalid
        return {}

def save_memory(memory):
    with open("data/memory.json", "w") as f:
        json.dump(memory, f, indent=2)

def get_study_set(num_words):
    with open("data/word_data.json") as f:
        word_data = json.load(f)
    
    memory = load_memory()
    words = list(word_data.keys())
    
    # Initialize memory for new words
    for word in words:
        if word not in memory:
            memory[word] = {
                "review_count": 0,
                "correct": 0,
                "total_quiz": 0
            }
    
    # Sort by review count and accuracy
    sorted_words = sorted(words, key=lambda x: (
        memory[x]["review_count"],
        -memory[x]["total_quiz"]
    ))
    
    # Select 75% least reviewed, 25% random
    split = int(0.75 * num_words)
    study_words = sorted_words[:split] 
    if len(study_words) < num_words:
        study_words += random.sample(sorted_words[split:], num_words - split)
    
    save_memory(memory)
    return study_words

def run_study():
    num_words = int(input("How many words to study today? "))
    study_words = get_study_set(num_words)
    memory = load_memory()
    
    with open("data/word_data.json") as f:
        word_data = json.load(f)
    
    # Create output file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("study_history", exist_ok=True)
    output_file = f"study_history/study_list_{timestamp}.txt"
    
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"Study List Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for word in study_words:
                data = word_data[word]
                # Write to console
                print(f"\nWord: {word}")
                print(f"Definition: {data['def_dict']}")
                print(f"Definition Simple: {data['def_simple']}")
                print("Examples:")
                for ex in data["examples"]:
                    print(f"- {ex}")
                
                # Write to file
                f.write(f"Word: {word}\n")
                f.write(f"Definition: {data['def_dict']}\n")
                f.write(f"Definition Simple: {data['def_simple']}\n")
                f.write("Examples:\n")
                for ex in data["examples"]:
                    f.write(f"- {ex}\n")
                f.write("\n")
                
                input("\nPress Enter to continue...")
            
            # Only update review counts if entire list was completed
            for word in study_words:
                memory[word]["review_count"] += 1
            save_memory(memory)
            
            print(f"\nStudy list saved to: {output_file}")
            
    except KeyboardInterrupt:
        print("\nStudy session interrupted. Progress not counted towards review totals.")
        print(f"Partial study list saved to: {output_file}")

if __name__ == "__main__":
    run_study()