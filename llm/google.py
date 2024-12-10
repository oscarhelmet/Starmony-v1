from vertexai.generative_models import GenerativeModel, SafetySetting
import os
import uuid
from google.cloud import texttospeech 


class Google:
    def __init__(self):
        self.model = self.model_get()
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'cred.json'
        
    def model_get(self, model='others'):
        metadata = {'others':'gemini-1.5-pro-002'}
        
        return metadata.get(model, metadata.get('others'))
    
    def generate(self,template, 
                 top_p=None, 
                 top_k=20, 
                 temperature=0.6, 
                 system_instructions=None, 
                 max_output_tokens=512) -> str:
        """
        A standardized function to call the gemini model from vertexai class
        This should allow better model serving and switching for future developments
        """
        
        model = GenerativeModel(          
            self.model,
            system_instruction = system_instructions, 
            generation_config = {
               'temperature': temperature,
               'top_p': top_p,
               'top_k': top_k,
               'max_output_tokens': max_output_tokens
            },
            safety_settings = [
                            SafetySetting(
                                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                                threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE
                            ),
                            SafetySetting(
                                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                                threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE
                            ),
                            SafetySetting(
                                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                                threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE
                            ),
                            SafetySetting(
                                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                                threshold=SafetySetting.HarmBlockThreshold.BLOCK_NONE
                            ),
                        ])
        
        res = model.generate_content(template).text.strip()

        return res 
        
        
def t2s(ssml, speaking_rate=0.8):


    print("transcripts:\n", ssml)
    
    """Converts SSML text to speech using Google Cloud Text-to-Speech API.
    
    Args:
        ssml (str): The SSML text to convert to speech
        
    Returns:
        bytes: The audio content as bytes
    """
    client = texttospeech.TextToSpeechClient()
    
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=speaking_rate
    )
    
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    session = str(uuid.uuid4())
    path = f'static/audios/{session}.mp3'
    with open(path, 'wb') as f:
        f.write(response.audio_content)
    
    return f"{session}.mp3"
