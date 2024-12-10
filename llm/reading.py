from llm.google import Google 
from llm.utils import remove_code_blocks

def gen_reading(grade, chapter=None):

    if chapter == None:
        seed = random.randint(0,10000000) 
        chapter=f"random topic,  seed = {seed}"


    grade_descriptions = {
        0 : 'Easy and entry level for students who just starts to learn, assume they just know very easy words',
        1 : 'Easy to intermediate level for students who are growing, but still have limited knowledge, easier wording',
        2 : 'Intermediate level for students who are studying in junior schools, having sufficient knowledge and words to understand the world',
        3 : 'Pre-college level for students who are studing in high school, having most of the high school knowledge.'
    }

    print(grade, chapter)

    system_instruction = """
-Make 3 code blocks to show 3 different things
-1: A reading passage (include a title)
-2: a set of questions (Multiple-choice, Fill in the blanks, summary cloze, long questions[reply in complete sentence])
-3: answers for the questions 

- Difficulties: IETLS level 2-5 [equivalent: Hong Kong Secondary 1-3]
- Questions limits less than 30

- for quesions, use the following xml format:
    <question>
        <q id="1">
            Question <blank id="1">_____</blank> is cool.
        </q>
    </question>
    
    <blank> is the expected user input field. Show "______" only when the answer is inline. 


    Example:
    ```
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
    
    for summary cloze, mark as <q>

-for answers, use the following format:
    ```
    1. 2
    2. blank
    ```
-for all output code blocks, just use 
```(NO TYPE SPECIFICATION)
content 
``` is fine for the parser, other wise will be ignored.
    """


    template = f"""Make a set of questions for {chapter} with the style of {grade_descriptions[int(grade)]}."""


    res = Google()\
            .generate(template = template,
                system_instructions = system_instruction,
                top_p = 0.95,
                temperature = 1,
                top_k = None,
                max_output_tokens = None)

    print(res)
    return res


def seperate_reading(input):
    """Separates the LLM output into passage, questions and answers from markdown code blocks.
    
    Args:
        input (str): The raw LLM output containing markdown code blocks for passage, questions and answers
        
    Returns:
        tuple: (passage, questions, answers) strings
    """
    # Split by markdown code blocks
    parts = input.split("```")
    
    # Remove empty strings and whitespace
    parts = [p.strip() for p in parts if p.strip()]
    
    if len(parts) != 3:  # We expect 3 code blocks with content
        return None, None, None
        
    # Get the content from each code block
    passage = parts[0]
    questions = parts[1] 
    answers = parts[2]
    
    return passage, questions, answers


