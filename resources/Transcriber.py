from functools import lru_cache
import warnings
import whisper


class SpeechRecognizer:
    
    def __init__(self, model_name="base"):
        self.model_name = model_name
        self.device = "cpu"
        self.model = self.load_model()
        # Set up warnings filter
        warnings.filterwarnings("ignore", category=UserWarning)

    def banner(self, text):
        print(f"# {text} #\n")

    @lru_cache(maxsize=None)
    def load_model(self):
        return whisper.load_model(self.model_name, device=self.device)

    def convert_text(self, audio_file):
        self.banner("Transcribing texts")
        try:
            result = self.model.transcribe(audio_file)
            return result["text"]
        except Exception as e:
            print(f"Error occurred during audio file conversion: {e}")
            return None