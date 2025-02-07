# quiz.py
import json
import random
from study import load_memory, save_memory

def generate_question(word_data, memory):
    word = word_data["word"]
    correct = word_data["definition"]
    
    # Get 3 random wrong definitions
    with open("data/word_data.json") as f:
        all_words = json.load(f).values()
        wrongs = [w["definition"] for w in all_words 
                 if w["word"] != word][:3]
    
    options = [correct] + wrongs
    random.shuffle(options)
    answer = options.index(correct) + 1
    
    return {
        "question": f"What's the definition of '{word}'?",
        "options": options,
        "answer": answer
    }

def run_quiz():
    with open("data/word_data.json") as f:
        word_data = json.load(f)
    
    memory = load_memory()
    studied_words = [w for w in word_data if memory[w]["review_count"] > 0]
    
    num_q = int(input("How many questions? "))
    quiz_words = random.sample(studied_words, num_q)
    wrongs = []
    
    for word in quiz_words:
        data = word_data[word]
        q = generate_question(data, memory)
        
        print(f"\n{q['question']}")
        for i, opt in enumerate(q["options"], 1):
            print(f"{i}. {opt}")
        
        choice = int(input("Your answer: "))
        memory[word]["total_quiz"] += 1
        if choice == q["answer"]:
            print("Correct!")
            memory[word]["correct"] += 1
        else:
            print(f"Wrong! Correct was {q['answer']}")
            wrongs.append({
                "word": word,
                "question": q,
                "your_choice": choice
            })
    
    save_memory(memory)
    
    # Save wrong answers
    if wrongs:
        with open("data/wrong_answers.json", "w") as f:
            json.dump(wrongs, f, indent=2)
        print(f"\nSaved {len(wrongs)} wrong answers to review!")

if __name__ == "__main__":
    run_quiz()