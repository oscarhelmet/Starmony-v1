from flask import Flask, render_template, request, redirect, url_for
from questions.questions import parse_question_xml, render_questions, render_dashboard
from llm.generate_question import generate_question, seperate_qa
from llm.dashboard import dashboard
from llm.listening import gen_listening, seperate_session
from llm.reading import gen_reading, seperate_reading
from llm.google import t2s
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
        respond = generate_question(grade, subject, chapter, language,noq)
        print(respond)
        questions_xml, answers = seperate_qa(respond)
        f = open(f"questions_set/{session}.xml", "w")
        f.write(f"questions: {questions_xml}, Modal Answers for checking: {answers}")
        f.close()

        # Load and render the questions
        questions = parse_question_xml(questions_xml)

        question_html = render_questions(questions)
        print(questions)

        return render_template('answer.html', questions=questions)

    # Render the index.html template with the form
    return render_template('generate.html')


@app.route('/listening', methods=['GET','POST'])
def listening():
    if request.method == 'POST':
        grade = request.form['grade']
        chapter = request.form['chapter']
        speed = request.form['speed']
        language = request.form['language']
        
        # Generate the questions using the provided parameters
        respond = gen_listening(grade=grade, chapter=chapter, language=language)
        ssml, questions_xml, answers = seperate_session(respond)
        
        # print  

        # Save questions and answers
        f = open(f"questions_set/{session}.xml", "w")
        f.write(f"questions: {questions_xml}, Modal Answers for checking: {answers}")
        f.close()

        # Convert SSML to audio using text-to-speech
        audio_path = t2s(ssml, speaking_rate=float(speed))  # Assuming t2s() handles the SSML to audio conversion
        
        # Load and render the questions
        questions = parse_question_xml(questions_xml)
        question_html = render_questions(questions)
        
        return render_template('answer.html', 
                             questions=questions, 
                             audio=audio_path)

    return render_template('listening.html')

@app.route('/reading', methods=['GET','POST'])
def reading():
    if request.method == 'POST':
        grade = request.form['grade']
        chapter = request.form['chapter']
        language = request.form['language']

        
        # Generate the questions using the provided parameters
        respond = gen_reading(grade=grade, chapter=chapter, language=language)
        passage, questions_xml, answers = seperate_reading(respond)
        
        print(respond)

        # Save questions and answers
        f = open(f"questions_set/{session}.xml", "w")
        f.write(f"questions: {questions_xml}, Modal Answers for checking: {answers}")
        f.close()

        # Load and render the questions
        questions = parse_question_xml(questions_xml)
        question_html = render_questions(questions)
        
        return render_template('answer.html', 
                             questions=questions, 
                             passage=passage)

    return render_template('reading.html')


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