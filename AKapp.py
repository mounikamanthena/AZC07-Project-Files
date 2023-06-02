# NOTE: Moved all the previous and WIP code to reference_code.py
# OpenAI API integration code https://www.youtube.com/watch?v=pGOyw_M1mNE
# Flask code from CS50 project and DigitalOcean
import flask
import openai

from download_route import download_route

# API key 
openai.api_key = "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"

# Configure application
app = flask.Flask(__name__)
app.secret_key = 'very_secret_key'

# Ensure templates are auto-reloaded when modified
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Initialised messages variable, which is a list of dictionaries. Each dictionary is a message with two key value pairs - 'role' and 'content'
# Currently using different variables for each app, but in the future should look into other methods like flask sessions to store data instead
# TODO: Update prompts
keyword_msg = [{"role": "system", "content": "Could you please summarise the user input in just a few important keywords"}]

interview_msg = [{"role": "system", "content": "Assume that the user input is a job title and based on that job title give them five interview questions based on the job title"}]


# Homepage: Explanation of the project
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return flask.render_template('home.html')


# For the Interview Page.
@app.route("/interview", methods=['GET', 'POST'])
def summary():

    if request.method == 'POST':
        message = request.form['input']
        interview_msg.append({"role": "user", "content": message})
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=interview_msg)
        reply = response["choices"][0]["message"]["content"]
        interview_msg.append({"role": "assistant", "content": reply})
        return render_template('interview.html', reply=reply)
    else:
        return render_template('interview.html')


# TODO: Example keyword route
@app.route('/keywords', methods=['GET', 'POST'])
def keyword():
    if flask.request.method == 'POST':
        message = flask.request.form['message']

        # Define chat conversation using system, user, and message input
        conversation = [
            {'role': 'system', 'content': 'Could you please summarise the user input in just a few important keywords'},
            {'role': 'user', 'content': message}
        ]

        # Make a chat completion request to OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation,
            max_tokens=50
        )

        output = response.choices[0].message.content

        return flask.render_template('keyword.html', message=message, output=output)
    else:
        return flask.render_template('keyword.html')


# Route to write the conversation into messages.txt and provide to user as download
# Rewrote so it calls the download_route function and passes it the relevant variable depending on the app TODO: HTML will need to be edited to reflect routing
@app.route('/download/interview')
def download_summary():
    return download_route(summariser_msg)


@app.route('/download/keyword')
def download_keywords():
    return download_route(keyword_msg)


if __name__ == '__main__':
    app.run(debug=True)
