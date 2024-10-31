from llm.google import Google 
from llm.utils import remove_code_blocks

def generate_question(grade, subject, chapter, language, noq):


    grade_descriptions = {
        0 : 'Easy and entry level for students who just starts to learn, assume they just know very easy words',
        1 : 'Easy to intermediate level for students who are growing, but still have limited knowledge, easier wording',
        2 : 'Intermediate level for students who are studying in junior schools, having sufficient knowledge and words to understand the world',
        3 : 'Pre-college level for students who are studing in high school, having most of the high school knowledge.'
    }

    print(grade, subject, chapter, language, noq)

    system_instruction = f"""
    You are an Excercise publisher for Hong Kong students.
    Your task is to write questions regarding the related topic 
    You will be received a topic to create the worksheet.
    Organise it and write it question by question, with subquestions if needed.
    You should make {noq} questions per request in following format:

    <question>
        <q id="1">
            Question <blank id="1">_____</blank> is cool.
        </q>
    </question>
    
    <blank> is the expected user input field. Show "______" only when the answer is inline. 


    Example:
    <question>
        <q id="1">
           What is 1+1? <blank id="1"></blank>
        </q>
        <q id="2">
            Inline <blank id="1">_____</blank>(look) like this.
        </q>

    Answer in the xml only, other comments should omit, since this will be embedded in an app.
    Delete all md code block formats, element like ``` should be banned.
    If it is an math equation, use $example_math$ to bound it, avoid  $2 and a banana costs $3, if it is dollar sign use $\$5$.
    """


    template = f"""Make a set of questions for {chapter} in {subject} Subject with the style of {grade_descriptions[int(grade)]}. The questions should be in the language of {language}"""

    return remove_code_blocks(Google()\
            .generate(template = template,
                system_instructions = system_instruction,
                top_p = 0.95,
                temperature = 1,
                top_k = None,
                max_output_tokens = None))
    
