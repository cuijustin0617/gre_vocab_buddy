import csv

def process_barron_words(input_file='barron800_words.txt', output_file='barron800_words.csv'):
    # Open both files - input for reading, output for writing
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        # Write CSV header
        outfile.write('word\n')
        
        # Process each line
        for line in infile:
            # Split by tab and take first element (the word)
            word = line.split('\t')[0]
            # Convert to lowercase and write to file with newline
            outfile.write(f"{word.lower()}\n")

# Run the function
process_barron_words()