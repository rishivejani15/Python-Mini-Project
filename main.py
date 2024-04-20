from flask import Flask, request, render_template, redirect, jsonify, session, render_template_string
import random
import string
import requests
import pyperclip
import urllib
from urllib.parse import unquote
from flask_cors import CORS
from flask import session
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = b'5#y2L"F4Q8z\n\xec]/'
all_users = {}
question_data = None
score = 0
random_code =  0
music_thread=None


my_email = "15rishivejani@gmail.com"
app_password = "wzmpddvkfhhmwhhj"

def generate_random_code(length):
    characters = string.ascii_letters + string.digits
    random_code = ''.join(random.choice(characters) for _ in range(length))
    return random_code

random_code = generate_random_code(5)


@app.route('/copy_code', methods=['POST'])
def copy_code():
    pyperclip.copy(random_code)
    return '', 204  # Return an empty response with status code 204 (No Content)

@app.route('/', methods=["GET", "POST"])
def r():
    # Start playing music when the server starts
    # global music_thread
    # music_thread = threading.Thread(target=play_music)
    # music_thread.daemon = True
    # music_thread.start()
    return render_template('room.html')

@app.route('/check_answer', methods=["POST"])
def check_answer():
    data = request.json
    question_index = int(data.get('questionIndex'))
    selected_answer = data.get('answer')

    # Retrieve the user's score from the session or initialize it to 0
    score = session.get('score', 0)

    # Check if the selected answer is correct
    is_correct = False
    if question_data and 0 <= question_index < len(question_data):
        correct_answer = question_data[question_index]['correct_answer']
        is_correct = selected_answer == correct_answer

    # Update score if the answer is correct
    if is_correct:  
        # Increment the user's score
        score += 1
        session['score'] = score

    # Return response indicating whether the answer is correct
    return jsonify({'is_correct': is_correct, 'score': score})

@app.route('/data_question', methods=["GET"])
def data_question():
    if question_data:
        return jsonify(question_data)
    else:
        return jsonify({'error': 'Question data not available'})

@app.route('/register', methods=["GET", "POST"])
def reg():
    if request.method == "POST":
        name = request.form["userName"]
        # if 'username' in session:
        #     session.pop('username',None)
        #     session.pop('score',None)
        session['username'] = name  # Initialize the username in the session
        code = request.form["sc"]
        if code == random_code:
            all_users[name] = {'score': 0}
            return redirect("/questions")
        else:
            return render_template('register.html')
    return render_template('register.html')


@app.route('/gg', methods=["GET", "POST"])
def gg():
    return redirect("/generate_quiz")

@app.route('/generate_quiz', methods=["GET", "POST"])
def gg1():
    global question_data
    if request.method == "POST":
        amount = request.form["amount"]
        category = request.form["category"]
        difficulty = request.form["difficulty"]
        q_type = request.form["type"]

        parameters = {
            "amount": amount,
            "category": category,
            "difficulty": difficulty,
            "type": q_type,
            "encode": "url3986"
        }

        response = requests.get("https://opentdb.com/api.php", params=parameters)
        data = response.json()
        question_data = data.get("results", [])

        return redirect("/questions")

    return render_template("quiz_generator.html")

@app.route('/admin', methods=["GET", "POST"])
def a():
    global random_code
    if request.method == "POST":
        name = request.form["userName"]
        all_users[name] = {'score': 0}
        return redirect("/admin")
    return render_template('admin.html', all_users=all_users, code=random_code)

questions = []
corr_answers = []
filename = 'quiz_results.txt'

def save_questions_to_file():
    with open(filename, 'w',encoding='utf-8') as file:
        # Iterate through the questions and answers
        for i in range(len(questions)):
            question = questions[i]
            correct_answer = corr_answers[i]
            # Format the question and answers as a single line
            line = f"Question: {question}\nCorrect Answer: {correct_answer}\n\n"
            # Write the line to the file
            file.write(line)

@app.route('/questions', methods=["GET", "POST"])
def ques():
    global score
    if question_data:
        decoded_questions = []
        for question in question_data:
            decoded_question = {}
            decoded_question["question"] = unquote(question["question"])
            questions.append(decoded_question["question"])
            decoded_question["correct_answer"] = unquote(question["correct_answer"])
            corr_answers.append(decoded_question["correct_answer"])
            decoded_question["incorrect_answers"] = [unquote(answer) for answer in question["incorrect_answers"]]
            decoded_question["type"] = unquote(question["type"])
            decoded_question["difficulty"] = unquote(question["difficulty"])
            decoded_question["category"] = unquote(question["category"])
            answers = [decoded_question["correct_answer"]] + decoded_question["incorrect_answers"]
            random.shuffle(answers)
            decoded_question["shuffled_answers"] = answers
            decoded_questions.append(decoded_question)

        return render_template('display_questions.html', questions=decoded_questions, score=score)
    else:
        return render_template('waiting.html')

@app.route('/share_on_whatsapp', methods=['POST'])
def share_on_whatsapp():
    code = request.form.get('code')
    l1 = ["Check out this code:"]
    l2 = ["Here is the link to join the room: https://1rlsn44x-5000.inc1.devtunnels.ms/"]
    message = f"{l1[0]} {code}\n{l2[0]}"
    encoded_message = urllib.parse.quote(message)
    url = f'https://api.whatsapp.com/send?text={encoded_message}'
    return redirect(url)

def send_email_with_attachment(email, subject, body, file_path):
    # Create a multipart email message
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = email
    msg['Subject'] = subject
    
    # Attach the body text to the message
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the file to the message
    with open(file_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), Name=file_path)
    # Add the attachment to the message
    attachment.add_header('Content-Disposition', f'attachment; filename="{file_path}"')
    msg.attach(attachment)
    
    # Connect to the SMTP server and send the email
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=app_password)
            connection.sendmail(from_addr=my_email, to_addrs=email, msg=msg.as_string())
            print(f"Email with attachment sent successfully to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
    
    # stop_music()

@app.route('/leaderboard', methods=['GET','POST'])
def leaderboard():
    save_questions_to_file()
    if request.method == "POST":
        email = request.form["mail"]
        file_path = "quiz_results.txt"  # Specify the file path you want to attach
        subject = "Quizify"
        body = "Here is the correct answers of the quiz!"
        send_email_with_attachment(email, subject, body, file_path)
    sorted_users = sorted(all_users.items(), key=lambda x: x[1]['score'], reverse=True)
    print("Sorted Users:", sorted_users)  # Print sorted users to console
    return render_template('leaderboard.html', users=sorted_users)

@app.route('/byebye', methods=['POST'])
def byebye():
    if request.method == "POST":
        data = request.json
        username = session.get('username')
        final_score = data.get('final_score')
        if username:
            # Update the user's score if the username exists in the session
            all_users.setdefault(username, {'score': 0})['score'] = final_score
            # Print the final score
            print("Final score for", username, ":", final_score)
            # Print all users' names and final scores
            print("All users and their scores:")
            for user, info in all_users.items():
                print(user, ":", info['score'])
            # Handle any other actions you need to perform
            return jsonify({'success': True}), 200
        else:
            # Handle case where username is not found in session
            return jsonify({'success': False, 'error': 'Username not found in session'}), 404
    return jsonify({'success': False}), 405

def clear_all_users():
    """Clear all users from the dictionary and remove user session data."""
    global all_users
    all_users.clear()  # Clear all users from the dictionary
    session.pop('username', None)  # Remove 'username' key from session
    session.pop('score', None)  # Remove 'score' key from session

def restart_game():
    """Restart the game by resetting game state variables."""
    global question_data, random_code
    
    # Reset question data to None (or whatever initial state you prefer)
    question_data = None
    
    # Generate a new random code for the next game
    random_code = generate_random_code(5)
    
    # Clear all users and their session data
    clear_all_users()

    # Add any other necessary game reset logic here (e.g. resetting scores)

    # Optionally, you may want to stop and restart music if using any
    # if music_thread:
    #     music_thread.stop()  # Stop music thread if applicable
    #     music_thread = threading.Thread(target=play_music)
    #     music_thread.daemon = True
    #     music_thread.start()


@app.route('/restart-game', methods=['POST'])
def restart_game_endpoint():
    # Call the function to clear all users
    clear_all_users()
    
    # Call the function to restart the game
    restart_game()
    
    # Return a success response
    return jsonify({'statu  s': 'success'}), 200

if __name__ == "__main__":
    app.run(debug=True)