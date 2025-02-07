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

- **Study Session Flow**:
  1. Choose number of words to study 
  2. For each word:
     - View dictionary and simplified definitions
     - See multiple example sentences
     - Mark word as reviewed
  3. Session progress is automatically saved

### Quiz Mode (quiz.py)
The quiz system uses spaced repetition principles to reinforce learning:



