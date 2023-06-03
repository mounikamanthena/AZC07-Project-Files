from flask import send_file

# Create text file named after variable to store conversation history
def download_route(messages, filename):
   with open(filename, 'w') as f:
       for message in messages:
           f.write(f"{message['role']}: {message['content']}\n")
           f.write("---\n")
   path = filename
   return send_file(path, as_attachment=True)