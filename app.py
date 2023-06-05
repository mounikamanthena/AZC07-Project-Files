# NOTE: Moved all the previous and WIP code to reference_code.py
# OpenAI API integration code https://www.youtube.com/watch?v=pGOyw_M1mNE
# Flask code from CS50 project and DigitalOcean
import flask
import openai
from download_route import download_route
from reset_route import reset_route

# Check for OpenAI API key from text file: 'api_key.txt' https://platform.openai.com/account/api-keys. Still not very secure but better than having the API key hardcoded.
# NOTE: Remember to delete or clear the api_key.txt file if code is to be shared or made public
try:
    with open("api_key.txt", "r") as file:
        api_key = file.read().strip()

    if not api_key:
        raise ValueError("API key not found in the file.")

    openai.api_key = api_key
except FileNotFoundError:
    print("File 'api_key.txt' not found. Please create an 'api_key.txt' file and add your OpenAI API key.")
except ValueError as e:
    print("Invalid API key: " + str(e))

# Configure application
app = flask.Flask(__name__)
app.secret_key = 'very_secret_key'

# Ensure templates are auto-reloaded when modified
app.config["TEMPLATES_AUTO_RELOAD"] = True

# NOTE: Enter prompt details below
# Initialised separate variables for prompts so it can be easily called by other functions, and so if changes need to be made to the prompts, they can just be changed here.
interview_prompt = "Assume that the user input is a job title and based on that job title give them five interview questions based on the job title"
keyword_prompt = "Could you please summarise the user input in just a few important keywords"

# Init variables to store message history, each a list of dictionaries. Each dictionary is a message with two key value pairs - 'role' and 'content'
# Currently using different variables for each app, but in the future should look into other methods like flask sessions to store data instead
interview_msg = [{"role": "system", "content": interview_prompt}]
keyword_msg = [{"role": "system", "content": keyword_prompt}]


# Homepage: Explanation of the project
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return flask.render_template('home.html')


# Interview route
@app.route("/interviewquestions", methods=['GET', 'POST'])
def interview():
    if flask.request.method == 'POST':
        message = flask.request.form['message']
        interview_msg.append({"role": "user", "content": message})

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=interview_msg)
        reply = response["choices"][0]["message"]["content"]

        interview_msg.append({"role": "assistant", "content": reply})
        return flask.render_template('interviewquestions.html', message=message, reply=reply)
    else:
        return flask.render_template('interviewquestions.html')


# Keyword route
@app.route('/keywords', methods=['GET', 'POST'])
def keyword():
    if flask.request.method == 'POST':
        message = flask.request.form['message']
        keyword_msg.append({"role": "user", "content": message})

        # Make a chat completion request to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=keyword_msg,
            max_tokens=50
        )
        output = response.choices[0].message.content

        keyword_msg.append({"role": "assistant", "content": output})
        return flask.render_template('keyword.html', message=message, output=output)
    else:
        return flask.render_template('keyword.html')


# Routes to write the conversation into text files and provide to user as download
@app.route('/download/interview')
def download_interview():
    download_route(interview_msg, "interview_msg.txt")
    path = "interview_msg.txt"
    return flask.send_file(path, as_attachment=True)

@app.route('/download/keyword')
def download_keywords():
    download_route(keyword_msg, "keyword_msg.txt")
    path = "keyword_msg.txt"
    return flask.send_file(path, as_attachment=True)


# Routes to reset variables to default prompts so conversation history is cleared
@app.route('/reset/interview')
def reset_interview():
    global interview_msg
    interview_msg = reset_route("interview_msg")
    return flask.redirect('/interviewquestions')

@app.route('/reset/keyword')
def reset_keyword():
    global keyword_msg
    keyword_msg = reset_route("keyword_msg")
    return flask.redirect('/keywords')


if __name__ == '__main__':
    app.run(debug=True)
