import os
from pytubefix import YouTube
from pydub import AudioSegment, effects
import librosa
import soundfile as sf
import tempfile

def adjust_bpm(youtube_url: str, current_bpm: float, desired_bpm: float):
    """
    Download a YouTube video and adjust its speed to match the desired BPM.
    
    Args:
        youtube_url (str): URL of the YouTube video
        current_bpm (float): Current BPM of the song
        desired_bpm (float): Desired BPM of the song
        
    Returns:
        str: Path to the output file
    """
    # Calculate the speed ratio
    speed_ratio = desired_bpm / current_bpm

    # Temp directory for storing unedited audio
    temp_dir = tempfile.mkdtemp()
    temp_wav_path = os.path.join(temp_dir, "temp_audio.wav")
    
    # Create video stream
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    original_download_path = audio_stream.download(output_path=temp_dir)

    sound = AudioSegment.from_file(original_download_path)
    sound.export(temp_wav_path, format="wav")


    y, sr = librosa.load(temp_wav_path)

    y_fast = librosa.effects.time_stretch(y, rate = speed_ratio)

    # Export path
    output_path = os.path.join(os.getcwd(), f"{yt.title}.mp3")

    sf.write(output_path, y_fast, sr)

    # sound = AudioSegment.from_file(download_path)

    # speedup_audio = effects.speedup(sound, playback_speed=speed_ratio, chunk_size=80, crossfade= 100)
    

    # nightcore?

    # new_frame_rate = int(sound.frame_rate * speed_ratio)

    # adjusted_sound = sound._spawn(speedup_effect, overrides={
    #         "frame_rate": new_frame_rate
    #     })
    # adjusted_sound = adjusted_sound.set_frame_rate(sound.frame_rate)

    # adjusted_sound.export(output_path, format="mp3")
    # export
    # speedup_audio.export(output_path, format="mp3")

    # Delete temp directory
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)


if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ")
    current_bpm = float(input("Enter current BPM: "))
    desired_bpm = float(input("Enter desired BPM: "))
    adjust_bpm(youtube_url, current_bpm, desired_bpm)