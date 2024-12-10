from llm.google import Google 
from llm.utils import remove_code_blocks
import random

def gen_listening(grade, chapter=None):


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
    You will be given a topic and you need to make a scripts for beginners' listening test in the following ssml (GCP T2S) format.
After one, you will be making a list of 5- 10 questions in a code block (including fill in the blanks, The questions could mostly be a note jotting style (point  form), Multiple choices {dont make all b, evenly distributed}, but without any spelling questions, directly e.g. The colour of banana: ______, instead of how to spell yellow.)  [student version]
Add a Breakline and code blocks the answers.
example:

```
<speak>
  Here are <say-as interpret-as="characters">SSML</say-as> samples.
  I can pause <break time="3s"/>.
  I can play a sound
  <audio src="https://www.example.com/MY_MP3_FILE.mp3">didn't get your MP3 audio file</audio>.
  I can speak in cardinals. Your number is <say-as interpret-as="cardinal">10</say-as>.
  Or I can speak in ordinals. You are <say-as interpret-as="ordinal">10</say-as> in line.
  Or I can even speak in digits. The digits for ten are <say-as interpret-as="characters">10</say-as>.
  I can also substitute phrases, like the <sub alias="World Wide Web Consortium">W3C</sub>.
  Finally, I can speak a paragraph with two sentences.
    <p><s><voice name="en-US-Wavenet-J">Hey everyone, thanks for coming to the meeting today.</voice></s></p>
  <p><s><voice name="en-US-Wavenet-A">Ya.</voice></s></p>
</speak>
```
- The questions should be straight forward
-```example questions
The family is going to __________ on vacation
Leaving Time _____________
Flight Time ________________
``` Ommit using complete sentence to ask 
-the script should use easy words
-try to repeat the information, after the one says,
-if that is a phone number, repeat it, if there is a name, spell it [make a 3ms pause between each letter], Like {E<break time="5ms"/>N<break time="5ms"/>G<break time="5ms"/>L<break time="5ms"/>I<break time="5ms"/>S<break time="5ms"/>H <break time="10ms"/>}. ONLY personal information will be spelt, instead of normal words.
-When introducing the characters, use third person to introduce, like (B:Hey, Andy! A:Hi!)
-For voice types female= {a,c,f}, male = {b,d} (Assign the names to corresponding wavenet), use GB, except others accent specified. If asked to generate in foreign language like japanese accent, use back their own language instead of en-JP (e.g. ja-JP), but in English context, so that it will return strong accent, if it is hong kong use yue-HK-Standard-{}
-If the voice is in foreign language, use the language code of the language, e.g. ja-JP for japanese, en only support [en-US, en-GB, en-AU, en-IN] only.
-Try to add some emotion tag or pitch to make it more natural
-<speak> is like <html> bound the whole speech and </speak> end in the end
-instead of prasody and par, please use <p> and <s> to bound the one sentence
-Before the speech, please add. ``` <voice name="en-GB-Standard-B">The recording is about to begin.</voice>
<audio src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>
<break time="2s"/>``` 

-After the speech, please add. beep``` 
<audio src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>
<voice name="en-GB-Standard-B">That is the end of the recording. You will have 1 minute to tidy up your answers.</voice>
<break time="2s"/>
-beep src <audio src="https://www.soundjay.com/buttons/beep-01a.mp3"></audio>

- for quesions, use the following xml format:
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

    return Google()\
            .generate(template = template,
                system_instructions = system_instruction,
                top_p = 0.95,
                temperature = 1,
                top_k = None,
                max_output_tokens = None)


def seperate_session(input):
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
    
    if len(parts) != 3:  # We expect 3 code blocks with content
        return None, None, None
        
    # Get the content from each code block
    ssml = parts[0]
    questions = parts[1] 
    answers = parts[2]
    
    return ssml, questions, answers


