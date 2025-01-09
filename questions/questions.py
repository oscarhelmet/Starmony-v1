import xml.etree.ElementTree as ET
import requests
import re

def parse_question_xml(xml):
    """Parse the XML question data and return a list of questions."""
    
    # First handle non-XML formats
    if not (xml.startswith("<question>") or xml.startswith("<questions>")):
        lines = xml.strip().split('\n')
        if not lines:
            return ""
        
        start_words = lines[0].strip()
        pattern = rf'{re.escape(start_words)}\s*(.*)'
        match = re.search(pattern, xml, re.DOTALL)
        if match:
            xml = match.group(1).strip()
    
    try:
        root = ET.fromstring(xml)
        questions = []
        
        # Process regular questions with blanks
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
                    question_text += elem.tail.strip()
            
            questions.append({
                'type': 'blank',
                'id': question_node.get('id'),
                'text': question_text,
                'blanks': blanks
            })
        
        # Process multiple choice questions (radio)
        for mc_node in root.findall('multiple_choice'):
            prompt = mc_node.find('prompt').text.strip() if mc_node.find('prompt') is not None else ""
            choices = []
            for choice in mc_node.findall('choice'):
                choices.append({
                    'id': choice.get('id'),
                    'text': choice.text.strip() if choice.text else ""
                })
            
            questions.append({
                'type': 'multiple_choice',
                'id': mc_node.get('id'),
                'prompt': prompt,
                'choices': choices
            })
        
        # Process checkbox questions
        for more_choice_node in root.findall('more_choice'):
            prompt = more_choice_node.find('prompt').text.strip() if more_choice_node.find('prompt') is not None else ""
            choices = []
            for choice in more_choice_node.findall('choice'):
                choices.append({
                    'id': choice.get('id'),
                    'text': choice.text.strip() if choice.text else ""
                })
            
            questions.append({
                'type': 'more_choice',
                'id': more_choice_node.get('id'),
                'prompt': prompt,
                'choices': choices
            })
        
        return questions
    
    except ET.ParseError:
        return []

def render_questions(questions):
    """Render the questions on the page."""
    html = '<div class="container">\n'
    for question in questions:
        if question['type'] == 'blank':
            html += f"""
            <div class="question">
                <p><i class="bi bi-patch-question-fill"></i> {question['id']}. {question['text']}</p>
                <div class="input-group mb-3">
                    <span class="input-group-text" id="basic-addon1">Answers | 答案</span>
                    <input type="text" class="form-control" name="q{question['id']}" 
                           aria-label="" aria-describedby="basic-addon1">
                </div>
            </div>
            """
        elif question['type'] == 'multiple_choice':
            html += f"""
            <div class="question">
                <p><i class="bi bi-patch-question-fill"></i> {question['id']}. {question['prompt']}</p>
                <div class="mb-3">
            """
            for choice in question['choices']:
                html += f"""
                    <div class="form-check">
                        <input class="form-check-input" type="radio" 
                               name="q{question['id']}" 
                               id="q{question['id']}_{choice['id']}" 
                               value="{choice['id']}">
                        <label class="form-check-label" for="q{question['id']}_{choice['id']}">
                            {choice['text']}
                        </label>
                    </div>
                """
            html += """
                </div>
            </div>
            """
        elif question['type'] == 'more_choice':
            html += f"""
            <div class="question">
                <p><i class="bi bi-patch-question-fill"></i> {question['id']}. {question['prompt']}</p>
                <div class="mb-3">
            """
            for choice in question['choices']:
                html += f"""
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" 
                               name="q{question['id']}_{choice['id']}" 
                               id="q{question['id']}_{choice['id']}" 
                               value="{choice['id']}">
                        <label class="form-check-label" for="q{question['id']}_{choice['id']}">
                            {choice['text']}
                        </label>
                    </div>
                """
            html += """
                </div>
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