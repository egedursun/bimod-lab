# NOTE: Implement this test
#   ========================
#   - Long audio files (more than 25MBs) are not supported to directly get transcribed, so they need to be split
#     into chunks
#   ========================

"""
    from pydub import AudioSegment

    song = AudioSegment.from_mp3("good_morning.mp3")

    # PyDub handles time in milliseconds
    ten_minutes = 10 * 60 * 1000

    first_10_minutes = song[:ten_minutes]

    first_10_minutes.export("good_morning_10.mp3", format="mp3")
"""
