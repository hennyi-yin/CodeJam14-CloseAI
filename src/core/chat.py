from .assistant import setup_assistant
from .stt import real_time_speech_to_text

assistant = setup_assistant()

def get_bot_response(user_message=None):
    if user_message is None:
        user_message = real_time_speech_to_text()
        
    response = assistant.get_completion(user_message)
    
    return user_message, response