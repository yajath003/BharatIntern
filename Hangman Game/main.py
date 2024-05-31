from flask import Flask, render_template, flash, request, session, redirect
import csv
import os
import random

csv_file_path = os.path.join('static', 'files', 'Book1.csv')
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


def read_csv_file(file_path):
    encodings = ['utf-8', 'latin1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, mode='r', newline='', encoding=encoding) as file:
                reader = csv.reader(file)
                rows = list(reader)
                return rows
        except Exception as e:
            continue
    raise Exception("Unable to read CSV file with available encodings.")


def rand():
    rows = read_csv_file(csv_file_path)
    ran = random.choice(rows)
    session['clue'] = ran[0]
    session['word'] = ran[1].upper()
    session['blank'] = '_ ' * len(session['word'])
    session['correct'] = 0
    session['guessed_letters'] = []
    session['errors'] = 3


@app.route('/')
def index():
    rand()
    session['score'] = 0
    return render_template('index.html')


@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        guess = request.form.get('text').upper()

        if guess in session['guessed_letters']:
            flash('You already guessed that letter!')
        else:
            session['guessed_letters'].append(guess)
            new_blank = list(session['blank'].replace(' ', ''))
            word_list = list(session['word'])
            correct_guesses = session['correct']
            correct_guess = False

            for i, letter in enumerate(word_list):
                if letter == guess:
                    new_blank[i] = letter
                    correct_guesses += 1
                    correct_guess = True

            session['blank'] = ' '.join(new_blank)
            session['correct'] = correct_guesses

            if not correct_guess:
                session['errors'] -= 1

            if correct_guesses == len(session['word']):
                session['score'] += 1
                flash('Congratulations! You guessed the word!')
                rand()

            if session['errors'] == 0:
                flash('Game over! You have used the maximum number of chances.')
                rand()
                return redirect('/')
    return render_template('start.html', clue=session['clue'], blank=session['blank'], len=len(session['word']),
                           score=session['score'], errors=session['errors'])


if __name__ == "__main__":
    app.run(debug=True)
