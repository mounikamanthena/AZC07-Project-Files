import os

# Function should delete the text file of the same name and reset return the default prompt as a variable
def reset_route(messages):
    # Store name of text file before the messages var is overwritten in the next step
    filename = messages + ".txt"
    print(filename)

    # Reset to default
    if messages == "interview_msg":
        messages = [{"role": "system", "content": "Assume that the user input is a job title and based on that job title give them five interview questions based on the job title"}]
    elif messages == "keyword_msg":
        messages = [{"role": "system", "content": "Could you please summarise the user input in just a few important keywords"}]

    # Delete messages.txt, flash confirmation then return
    if os.path.exists(filename):
        os.remove(filename)   
        # Commented out as flask message code not implemented in HTML - will throw error
        # flask.flash('History cleared', 'success')
    # else:
        # flask.flash('History already cleared', 'error')

    return messages