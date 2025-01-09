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

    - for quesions, use the following xml format:
    <question>
        <!-- Fill in the blank question -->
        <q id="1">
            What is 1+1? <blank id="1"></blank>
        </q>
        
        <!-- Fill in the blank with inline display, multiple blanks -->
        <q id="2">
            Inline <blank id="1">_____</blank>(look) like this. And I would <blank id="2">_____</blank>(like) to look like this.
        </q>
        
        <!-- Multiple choice question (radio - single selection) -->
        <multiple_choice id="3">
            <prompt>Which of the following is correct?</prompt>
            <choice id="1">A. First option</choice>
            <choice id="2">B. Second option</choice>
            <choice id="3">C. Third option</choice>
            <choice id="4">D. Fourth option</choice>
        </multiple_choice>
        
        <!-- Multiple choice question (checkbox - multiple selections) -->
        <more_choice id="4">
            <prompt>Select all that apply:</prompt>
            <choice id="1">A. First option</choice>
            <choice id="2">B. Second option</choice>
            <choice id="3">C. Third option</choice>
            <choice id="4">D. Fourth option</choice>
        </more_choice>
    </question>
    ```
    Do not include any other xml elements
    -for answers, use the following format:
        ```
        1. 2
        2. blank
        ```
    -for all output code blocks, just use 
    "```", instead of "```answers" or "```xml"
    content 
    ``` is fine for the parser, other wise will be ignored.
    """

    template = f"""Make a set of questions for {chapter} in {subject} Subject with the style of {grade_descriptions[int(grade)]}. The questions should be in the language of {language}"""

    return Google()\
            .generate(template = template,
                system_instructions = system_instruction,
                top_p = 0.95,
                temperature = 1,
                top_k = None,
                max_output_tokens = None)
    


def seperate_qa(input):
    """Separates the LLM output into SSML, questions and answers from markdown code blocks.
    
    Args:
        input (str): The raw LLM output containing markdown code blocks for SSML, questions and answers
        
    Returns:
        tuple: (ssml, questions, answers) strings
    """
    # Split by markdown code blocks
    parts = input.split("```")
    
    # Remove empty strings and whitespace
    parts = [p.strip() for p in parts if p.strip()]
    
    if len(parts) != 2:  # We expect 3 code blocks with content
        return None, None
        
    # Get the content from each code block
    questions = parts[0] 
    answers = parts[1]
    
    return questions, answers