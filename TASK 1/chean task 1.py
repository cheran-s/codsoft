import re
import datetime
import random
import sqlite3

# Connect to or create the database
conn = sqlite3.connect('chatbot_memory.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    birth_year INTEGER
)
''')
conn.commit()

# Fetch user name from database (if exists)
def get_stored_name():
    cursor.execute("SELECT name FROM user_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    return row[0] if row else "Friend"

def save_name(name):
    cursor.execute("INSERT INTO user_data (name) VALUES (?)", (name,))
    conn.commit()

def save_birth_year(year):
    cursor.execute("UPDATE user_data SET birth_year = ? WHERE id = (SELECT MAX(id) FROM user_data)", (year,))
    conn.commit()

def get_age():
    cursor.execute("SELECT birth_year FROM user_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    if row and row[0]:
        return datetime.datetime.now().year - int(row[0])
    return None

# Initial name fetch
user_name = get_stored_name()

def chatbot():
    global user_name
    print("Chatbot: Hello! I'm your ChatBot. Type 'bye' to end our conversation.")

    while True:
        user_input = input(f"{user_name}: ").lower().strip()

        if user_input in ['bye', 'exit', 'quit']:
            print("Chatbot: Bye! Take care.")
            break

        elif re.search(r'\bhi\b|\bhello\b|\bhey\b', user_input):
            print("Chatbot: Hello there!")

        elif "your name" in user_input:
            print("Chatbot: I'm your chatbot. What's your name?")

        elif re.search(r"my name is (.*)", user_input):
            user_name = re.search(r"my name is (.*)", user_input).group(1).capitalize()
            save_name(user_name)
            print(f"Chatbot: Nice to meet you, {user_name}!")

        elif "how are you" in user_input:
            print("Chatbot: I'm doing well. How about you?")

        elif "date" in user_input:
            today = datetime.date.today()
            print(f"Chatbot: Today's date is {today.strftime('%A, %B %d, %Y')}")

        elif "time" in user_input:
            now = datetime.datetime.now()
            print(f"Chatbot: Current time is {now.strftime('%I:%M %p')}")

        elif "joke" in user_input:
            jokes = [
                "Why don't programmers like nature? It has too many bugs.",
                "Why do Java developers wear glasses? Because they don't C#.",
                "What do you call a fake noodle? An impasta."
            ]
            print("Chatbot: " + random.choice(jokes))

        elif "thank" in user_input:
            print("Chatbot: You're welcome!")

        elif "help" in user_input:
            print("Chatbot: I can talk, tell jokes, share facts, quotes, show date, time, and calculate simple math.")

        elif re.search(r'\d+ [\+\-\*/] \d+', user_input):
            try:
                print("Chatbot: The result is", eval(user_input))
            except:
                print("Chatbot: Sorry, something went wrong with the calculation.")

        elif "weather" in user_input:
            print("Chatbot: I can't fetch real weather data, but I hope it's a good day for you.")

        elif "quote" in user_input:
            quotes = [
                "Believe in yourself and all that you are.",
                "Success is not final, failure is not fatal: It is the courage to continue that counts.",
                "The best way to get started is to quit talking and begin doing."
            ]
            print("Chatbot: " + random.choice(quotes))

        elif "age" in user_input:
            age = get_age()
            if age:
                print(f"Chatbot: You are around {age} years old.")
            else:
                yob = input("Chatbot: What year were you born? ")
                if yob.isdigit():
                    save_birth_year(int(yob))
                    print(f"Chatbot: Got it! You're around {datetime.datetime.now().year - int(yob)} years old.")
                else:
                    print("Chatbot: Please enter a valid year.")

        elif "color" in user_input:
            print("Chatbot: That's a nice color.")

        elif "food" in user_input:
            print("Chatbot: That sounds tasty.")

        elif "i am sad" in user_input or "feeling sad" in user_input:
            print("Chatbot: I'm here for you. Things will get better.")

        elif "compliment" in user_input:
            compliments = ["You're doing great!", "You are very intelligent!", "You have a wonderful personality."]
            print("Chatbot: " + random.choice(compliments))

        elif "i am bored" in user_input:
            suggestions = ["Read a book", "Try learning a new skill", "Watch a movie"]
            print("Chatbot: You could try this - " + random.choice(suggestions))

        elif "i love you" in user_input:
            print("Chatbot: Thank you. I appreciate that.")

        elif "convert" in user_input and "celsius" in user_input:
            c = float(input("Enter temperature in Celsius: "))
            f = (c * 9/5) + 32
            print(f"Chatbot: That's {f:.1f}°F")

        elif "convert" in user_input and "fahrenheit" in user_input:
            f = float(input("Enter temperature in Fahrenheit: "))
            c = (f - 32) * 5/9
            print(f"Chatbot: That's {c:.1f}°C")

        elif "fact" in user_input:
            facts = [
                "Octopuses have three hearts.",
                "Bananas are berries, but strawberries are not.",
                "Honey never spoils."
            ]
            print("Chatbot: " + random.choice(facts))

        else:
            print("Chatbot: I didn't understand that. Could you rephrase?")

# Start chatbot
chatbot()

# Close the database connection when done
conn.close()
