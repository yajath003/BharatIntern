from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"response": "No message received."})
    response = get_bot_response(user_input)
    return jsonify({"response": response})


def get_bot_response(user_input):
    user_input = user_input.lower()
    words = user_input.split()

    if 'hello' in words or 'hi' in words:
        return 'Hi, how can I assist you?!'
    elif 'how' in words and 'you' in words:
        return 'I am good, thank you!'
    elif 'what' in words and 'are' in words and 'you' in words:
        return """I am chatbot, an artificial intelligence language model. 
        My purpose is to assist with answering questions, providing information, and engaging in conversations on a wide range of topics. 
        How can I help you today?"""
    elif 'joke' in words:
        return """Sure! Here's one for you:
        Why don't scientists trust atoms?
        Because they make up everything!"""
    else:
        return 'Sorry, can you specify that?'


if __name__ == '__main__':
    app.run(debug=True)
