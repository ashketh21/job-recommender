## Main Flask Application that integrates all components and renders the web interface

from flask import Flask, request, render_template, flash
from werkzeug.utils import secure_filename
import os
import traceback
from resume_parser import extract_text_from_pdf
from job_scraper import scrape_indeed_jobs
from matcher import match_resume_to_jobs

app = Flask(__name__)
app.secret_key = 'dev_key_for_flash_messages'  # Required for flash messages
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    matches = []
    if request.method == "POST":
        try:
            # Check if the post request has the file part
            if 'resume' not in request.files:
                flash('No file part')
                return render_template("index.html", error="No file selected")
            
            file = request.files['resume']
            
            # If user does not select file
            if file.filename == '':
                flash('No selected file')
                return render_template("index.html", error="No file selected")
            
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            print(f"File saved to {filepath}")
            
            #Go through the resume parsing, job scraping, and matching process; return errors if any step fails
            print("Starting resume parsing...")
            
            try:
                resume_text = extract_text_from_pdf(filepath)
                print(f"Resume text extracted: {resume_text[:100]}...")  # Print first 100 chars
            except Exception as e:
                print(f"Error extracting resume text: {str(e)}")
                return render_template("index.html", error=f"Error parsing resume: {str(e)}")
                
            try:
                job_descriptions = scrape_indeed_jobs("software developer")
                print(f"Jobs scraped: {len(job_descriptions)} jobs found")
            except Exception as e:
                print(f"Error scraping jobs: {str(e)}")
                return render_template("index.html", error=f"Error scraping jobs: {str(e)}")
                
            try:
                matches = match_resume_to_jobs(resume_text, job_descriptions)
                print(f"Matches found: {len(matches)}")
            except Exception as e:
                print(f"Error matching resume to jobs: {str(e)}")
                return render_template("index.html", error=f"Error matching resume to jobs: {str(e)}")
                
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            traceback.print_exc()
            return render_template("index.html", error=f"An unexpected error occurred: {str(e)}")

    return render_template("index.html", matches=matches)

if __name__ == "__main__":
    app.run(debug=True)