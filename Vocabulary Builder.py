import csv
import random

# Function to load words from CSV file
def load_words(file_path):
    words = []
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            words.append({
                'word': row[0],
                'definition': row[1],
                'topic': row[2],
                'difficulty': int(row[3])
            })
    return words

# Function for user registration
def register_user(username, password):
    with open('users.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, 0, 0])  # Initialize scores

# Function for user login
def login_user(username, password):
    with open('users.csv', 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                return True, int(row[2]), int(row[3])  # Return scores if user found
        return False, 0, 0

# Function to update user scores
def update_scores(username, game_type, score):
    with open('users.csv', 'r+', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        rows = list(reader)
        for i in range(len(rows)):
            if rows[i][0] == username:
                if game_type == 'guessing':
                    rows[i][2] = str(int(rows[i][2]) + score)
                elif game_type == 'matching':
                    rows[i][3] = str(int(rows[i][3]) + score)
                break
        file.seek(0)
        writer = csv.writer(file)
        writer.writerows(rows)

# Function to filter words based on difficulty level and topic
def filter_words(words, difficulty, topic):
    filtered_words = [word for word in words if word['difficulty'] == difficulty and word['topic'] == topic]
    return filtered_words

# Function for word guessing game
def play_guessing_game(words):
    word = random.choice(words)['word']
    word = word.lower()  # Convert word to lowercase
    word_length = len(word)
    print("Guess the word! It has {} letters.".format(word_length))
    guessed_word = ['_'] * word_length
    attempts = 0
    max_attempts = 6
    while attempts < max_attempts and '_' in guessed_word:
        print("Current word:", ' '.join(guessed_word))
        letter = input("Enter a letter: ").lower()  # Convert input letter to lowercase
        if len(letter) == 1 and letter.isalpha():
            if letter in word:
                for i in range(word_length):
                    if word[i] == letter:
                        guessed_word[i] = letter
                print("Correct guess!")
            else:
                attempts += 1
                print("Incorrect guess. Attempts left:", max_attempts - attempts)
        else:
            print("Invalid input. Please enter a single letter.")
    if '_' not in guessed_word:
        print("Congratulations! You guessed the word '{}'.".format(word))
        return True
    else:
        print("Sorry, you didn't guess the word. The word was '{}'.".format(word))
        return False

# Function for definition matching game
def play_matching_game(words):
    word = random.choice(words)
    print("Match the definition with the word!")
    print("Definition: " + word['definition'])
    guessed_word = input("Enter your guess: ").lower()
    if guessed_word.strip() == word['word'].lower():  # Compare ignoring case and leading/trailing spaces
        print("Correct!")
        return True
    else:
        print("Incorrect. The correct word was '{}'.".format(word['word']))
        return False

# Main function
def main():
    words = load_words('CSWords.csv')
    print("Welcome to Vocabulary Builder!")

    while True:
        # User authentication menu
        print("\nLogin or Register:")
        print("1. Login")
        print("2. Register")
        auth_choice = input("Enter the number corresponding to your choice: ")
        if auth_choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            logged_in, guessing_score, matching_score = login_user(username, password)
            if logged_in:
                print("Login successful!")
            else:
                print("Invalid username or password.")
                continue
        elif auth_choice == '2':
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            register_user(username, password)
            print("Registration successful! You can now login.")
            continue
        else:
            print("Invalid choice. Please choose again.")
            continue

        # Menu to choose difficulty level and topic
        print("\nChoose Difficulty Level:")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")
        print("4. Very Hard")
        difficulty_choice = int(input("Enter the number corresponding to the desired difficulty level: "))
        difficulty_map = {1: 'Easy', 2: 'Medium', 3: 'Hard', 4: 'Very Hard'}
        selected_difficulty = difficulty_map.get(difficulty_choice)

        print("\nChoose Topic:")
        topics = set(word['topic'] for word in words)
        for i, topic in enumerate(topics, start=1):
            print(f"{i}. {topic}")
        topic_choice = int(input("Enter the number corresponding to the desired topic: "))
        selected_topic = list(topics)[topic_choice - 1]

        filtered_words = filter_words(words, difficulty_choice, selected_topic)

        # Menu to choose game
        while True:
            print("\nMenu:")
            print("1. Word Guessing Game")
            print("2. Definition Matching Game")
            print("3. Choose Different Topic and Difficulty")
            print("4. Exit")
            game_choice = input("Choose a game (1-4): ")
            if game_choice == '1':
                game_type = 'guessing'
                if play_guessing_game(filtered_words):
                    update_scores(username, game_type, 1)
                else:
                    update_scores(username, game_type, 0)
            elif game_choice == '2':
                game_type = 'matching'
                if play_matching_game(filtered_words):
                    update_scores(username, game_type, 1)
                else:
                    update_scores(username, game_type, 0)
            elif game_choice == '3':
                break  # Return to topic and difficulty selection
            elif game_choice == '4':
                print("Thank you for playing!")
                return
            else:
                print("Invalid choice")

if __name__ == "__main__":
    main()
