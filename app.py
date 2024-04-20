from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from Extraction_FinalCode import convert_any_to_string
import openai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
openai.api_key = "api-key"

# Create the uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_text = None
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']
        if file:
            # Save the file to the uploads folder
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Convert the uploaded document to a string
            document_text = convert_any_to_string(file_path)
            
            # Use the document text to generate responses from the AI model
            prompt = request.form['prompt']
            response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=f"Document text: {document_text}\n\nQuestion: {prompt}",
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            generated_text = response.choices[0].text.strip()
            
            # Remove the uploaded file
            os.remove(file_path)
    
    return render_template('index.html', generated_text=generated_text)

if __name__ == '__main__':
    app.run(debug=True)