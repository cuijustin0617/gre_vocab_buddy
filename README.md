# GRE Vocabulary Study Assistant

A comprehensive study tool to help prepare for the GRE vocabulary section using spaced repetition and AI-powered learning.

## Features

### Data Preparation
- Import word lists from simple `.txt` files
- Uses AI/LLM to automatically generate:
  - Dictionary definitions
  - Simplified definitions
  - Example sentences
  - Synonyms
- Converts raw word lists into structured JSON data format

### Study Mode
- Interactive study sessions with customizable number of words
- Smart word selection algorithm that prioritizes:
  - Less frequently reviewed words (75% of selection)
  - Random selection for variety (25% of selection)
- For each word, displays:
  - Dictionary definition
  - Simplified "plain English" definition  
  - Multiple example sentences
- Saves study history with timestamps
- Tracks review counts per word

### Quiz Mode
- Test your knowledge with interactive quizzes
- Tracks accuracy statistics:
  - Total quiz attempts
  - Correct answers
- Uses spaced repetition principles

### Memory System
- Maintains persistent progress tracking
- Records for each word:
  - Number of reviews
  - Quiz performance
  - Total attempts
- Automatically initializes tracking for new words
- Uses JSON for data storage

## Usage

### Study Mode (study.py)
The study mode implements an intelligent word selection algorithm to optimize learning:

- **Selection Algorithm**:
  - 75% of words are chosen based on least-reviewed status
  - 25% are randomly selected to maintain variety
  - Words not seen in the last 24 hours are prioritized

- **Study Session Flow**:
  1. Choose number of words to study (default: 10)
  2. For each word:
     - View dictionary and simplified definitions
     - See multiple example sentences
     - Mark word as reviewed
  3. Session progress is automatically saved

### Quiz Mode (quiz.py)
The quiz system uses spaced repetition principles to reinforce learning:

- **Quiz Types**:
  - Definition matching
  - Synonym selection
  - Context-based word usage

- **Spaced Repetition**:
  - Words are scheduled for review based on performance
  - Correct answers increase interval before next review
  - Incorrect answers decrease interval
  - Uses a modified SuperMemo-2 algorithm

- **Performance Tracking**:
  - Accuracy rate per word
  - Overall quiz statistics
  - Learning progress visualization


