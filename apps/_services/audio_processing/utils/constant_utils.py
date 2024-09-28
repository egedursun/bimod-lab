class AudioProcessingExecutorActionsNames:
    TTS = "tts"
    STT = "stt"

    @staticmethod
    def as_list():
        return [AudioProcessingExecutorActionsNames.TTS, AudioProcessingExecutorActionsNames.STT]
