import os
from google.cloud import texttospeech
from dotenv import dotenv_values

# Load config
input_path = 'input/google_text_to_speech/'
config = dotenv_values(f'{input_path}google_text_to_speech.env')
supported_languages = config.get('supported_languages')
language = dict()
for supported_language in supported_languages.split(','):
    language[supported_language] = {
        'language_code': config.get(f'{supported_language}_language_code'),
        'name': config.get(f'{supported_language}_name')
    }
print(f'Supported languages: {language}')

# Instantiates a client
client = texttospeech.TextToSpeechClient.from_service_account_json(f'{input_path}service_account_key.json')


def run(data: dict):

    result = dict()

    for key, value in data.items():

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=value)

        # Build the voice request
        for supported_language in supported_languages.split(','):
            if supported_language in key:
                curr_language = language[supported_language]
        voice = texttospeech.VoiceSelectionParams(
            language_code=curr_language.get('language_code'),
            name=curr_language.get('name'),
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Create folder if not exist
        output_folder_path = 'output/google-text-to-speech/'
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)

        # The response's audio_content is binary.
        filename = f'{output_folder_path}{key}.mp3'
        with open(filename, 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print(f'Audio content written to file {filename}')

        result[key] = filename
    
    print(f'Processed: {result}')
    return result
