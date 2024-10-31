import xml.etree.ElementTree as ET
import requests


def parse_question_xml(xml):
    """Parse the XML question data and return a list of questions."""
    root = ET.fromstring(xml)
    questions = []
    for question_node in root.findall('q'):
        question_text = question_node.text.strip() if question_node.text else ""
        blanks = []
        
        for elem in question_node:
            if elem.tag == 'blank':
                blanks.append({
                    'id': elem.get('id'),
                    'text': elem.text.strip() if elem.text else ""
                })
                question_text += elem.text.strip() if elem.text else ""
            
            if elem.tail:
                question_text += elem.tail.strip() if elem.text else ""
        
        question = {
            'id': question_node.get('id'),
            'text': question_text,
            'blanks': blanks
        }
        questions.append(question)
    return questions

def render_questions(questions):
    """Render the questions on the page."""
    html = '<div class="container">\n'
    for question in questions:
        html += f"""
        <div class="question">
            <p>{question['id']}. {question['text']}</p>
            <input type="text" placeholder="{question['blanks'][0]['text']}">
        </div>
        """
    html += '</div>'
    return html



def render_dashboard(dashboard_xml):
    """Render the dashboard based on the provided XML data."""
    root = ET.fromstring(dashboard_xml)

    html = """
    <main>
     <div class="row justify-content-center" style="min-height: calc(100vh - 50px - 76.78px - 96px) !important;
    align-items: center;">
        <div class="col-md-8">
        <div class="card">
            <div class="card-header text-center py-3">
                <h2 class="mb-0">Student Performance Dashboard</h2>
            </div>
            <div class="card-body p-4">
            <div class="dashboard">
    """

    # Accuracy section
    accuracy_section = root.find('accuracy')
    html += """
        <div class="accuracy-section">
            <h2>Accuracy</h2>
            <div class="bar-chart">
    """
    for part in accuracy_section.findall('part'):
        html += f"""
                <div class="bar-item">
                    <div class="bar-label">{part.find('title').text}</div>
                    <div class="bar-container">
                        <div class="bar" style="width: {part.find('value').text}%;">{part.find('value').text}%</div>
                    </div>
                </div>
        """
    html += """
            </div>
        </div>
    """

    # Strength section
    strength_section = root.find('strength')
    html += """
        <div class="analysis-section">
            <h2>Strengths</h2>
            <ul>
    """
    for p in strength_section.findall('p'):
        html += f"                <li>{p.text}</li>\n"
    html += """
            </ul>
        </div>
    """

    # Weakness section
    weakness_section = root.find('weakness')
    html += """
        <div class="analysis-section">
            <h2>Weaknesses</h2>
            <ul>
    """
    for p in weakness_section.findall('p'):
        html += f"                <li>{p.text}</li>\n"
    html += """
            </ul>
        </div>
    """

    # Recommendation section
    recommendation_section = root.find('recommendation')
    html += """
        <div class="analysis-section">
            <h2>Recommendations</h2>
            <ul>
    """
    for p in recommendation_section.findall('p'):
        html += f"                <li>{p.text}</li>\n"
    html += """
            </ul>
        </div>
    """

    html += """
            </div>
            </div>
            </div>
            </div>
        </div>
    </main>
    """

    return html