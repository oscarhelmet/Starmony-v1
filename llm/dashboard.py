from llm.google import Google 
from llm.utils import remove_code_blocks


def dashboard(qs, ans, language = 'English'):

    system_instruction = """
    You are an Excercise publisher for Hong Kong students.
    Your task is to check answers for a set of questions 
    You will received a set of questions and they are answered in <answer>.
    Check if the questions are correct.   

    Give Dashboard to analyse (accuracy of each part with bar visualisation), strength, weakness and recommendations and find the root problem of the student’s performance, 
    make it in the following format:
    Example:
    <dashboard>
        <accuracy>
            <part id='a'>
                <title>Multiplication</title>
                <value>75</value>
            </part>
        </accuracy>

        <strength>
            <p> XXXX </p>
            <p> XXXX </p>
        </strength>
        
        <weakness>
            <p> XXXX </p>
            <p> XXXX </p>
        </weakness>

        <recommendation>
            <p> XXXX </p>
            <p> XXXX </p>
        </recommendation>
    </dashboard> 

    Answer in the xml only, other comments should omit, since this will be embedded in an app.
    Delete all md code block formats, element like ``` should be banned.
    """


    template = f"""questions set:{qs}
                    
                    answer respond:{ans}
                    
                    Return the report in the following language: {language}
    """
    
    return remove_code_blocks(Google()\
            .generate(template = template,
                system_instructions = system_instruction,
                top_p = 0.95,
                temperature = 1,
                top_k = None,
                max_output_tokens = None))
        

if __name__ == "__main__":
    res = dashboard(open('/home/lemon/AI/EduTech/Starmony/example/questions.xml'),open('/home/lemon/AI/EduTech/Starmony/example/answer.xml'))
    print(res)