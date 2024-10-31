from flask import Flask, render_template, request, redirect, url_for
from questions.questions import parse_question_xml, render_questions, render_dashboard
from llm.generate_question import generate_question
from llm.dashboard import dashboard
import uuid 

app = Flask(__name__)

session = uuid.uuid4()

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/generate', methods=['GET','POST'])
def generate_questions():
    if request.method == 'POST':
        grade = request.form['grade']
        subject = request.form['subject']
        chapter = request.form['chapter']
        language = request.form['language']
        noq = request.form['noq']

        # Generate the questions XML using the provided parameters
        questions_xml = generate_question(grade, subject, chapter, language,noq)
        f = open(f"questions_set/{session}.xml", "w")
        f.write(questions_xml)
        f.close()

        # Load and render the questions
        questions = parse_question_xml(questions_xml)

        question_html = render_questions(questions)
        print(questions)

        return render_template('answer.html', questions=questions)

    # Render the index.html template with the form
    return render_template('generate.html')

@app.route('/answer', methods=['POST'])
def answer():
    # Retrieve the user's answers from the request
    answers = request.form.to_dict()
    language = request.form['language']

    f = open(f"questions_set/{session}.xml", "r")
    res = dashboard(f.read(),answers,language)
    print(res)

    dashboard_data = render_dashboard(res)
    print(dashboard)

    return render_template('dashboard.html', dashboard=dashboard_data)

if __name__ == '__main__':
    app.run(debug=True, port=3618)