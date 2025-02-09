# quiz.py
import json
import random
from study import load_memory, save_memory

def generate_question(word_data, memory):
    word = word_data["word"]
    correct = word_data["def_dict"]  # Using the dictionary definition
    
    # Get 3 random wrong definitions
    with open("data/word_data.json") as f:
        all_words = json.load(f).values()
        wrongs = [w["def_dict"] for w in all_words 
                 if w["word"] != word]
        wrongs = random.sample(wrongs, 3)
    
    options = [correct] + wrongs
    random.shuffle(options)
    answer = options.index(correct) + 1
    
    return {
        "question": f"What's the definition of '{word}'?",
        "options": options,
        "answer": answer
    }

def get_quiz_words(word_data, memory, num_questions):
    # Get only studied words
    studied_words = [w for w in word_data if memory[w]["review_count"] > 0]
    
    if not studied_words:
        raise ValueError("No studied words available for quiz. Please study some words first.")
    
    # Calculate weights based on performance and quiz frequency
    weights = []
    for word in studied_words:
        mem = memory[word]
        if mem["total_quiz"] == 0:
            weight = 2.0  # Higher weight for never-quizzed words
        else:
            correct_ratio = mem["correct"] / mem["total_quiz"]
            weight = 1.0 + (1.0 - correct_ratio)  # Higher weight for more wrong answers
        weights.append(weight)
    
    # Normalize weights
    total = sum(weights)
    weights = [w/total for w in weights]
    
    # Select words based on weights
    return random.choices(studied_words, weights=weights, k=min(num_questions, len(studied_words)))

def run_quiz():
    with open("data/word_data.json") as f:
        word_data = json.load(f)
    
    memory = load_memory()
    
    try:
        num_q = int(input("How many questions? "))
        quiz_words = get_quiz_words(word_data, memory, num_q)
        wrongs = []
        
        for word in quiz_words:
            data = word_data[word]
            q = generate_question(data, memory)
            
            print(f"\n{q['question']}")
            for i, opt in enumerate(q["options"], 1):
                print(f"{i}. {opt}")
            
            while True:
                try:
                    choice = int(input("Your answer (1-4): "))
                    if 1 <= choice <= 4:
                        break
                    print("Please enter a number between 1 and 4.")
                except ValueError:
                    print("Please enter a valid number.")
            
            memory[word]["total_quiz"] += 1
            if choice == q["answer"]:
                print("Correct!")
                memory[word]["correct"] += 1
            else:
                print(f"Wrong! The correct answer was {q['answer']}:")
                print(f"'{data['def_dict']}'")
                wrongs.append({
                    "word": word,
                    "question": q,
                    "your_choice": choice
                })
        
        save_memory(memory)
        
        if wrongs:
            with open("data/wrong_answers.json", "w") as f:
                json.dump(wrongs, f, indent=2)
            print(f"\nSaved {len(wrongs)} wrong answers to review!")
            
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_quiz()