import os
from pytubefix import YouTube
from pydub import AudioSegment
import pyrubberband as pyrb
import sox
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


    tf = sox.Transformer()
    tf.tempo(speed_ratio)
    

    # Export path
    output_path = os.path.join(os.getcwd(), f"{yt.title}.mp3")

    tf.build(temp_wav_path, output_path)

    # Delete temp directory
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)


if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ")
    current_bpm = float(input("Enter current BPM: "))
    desired_bpm = float(input("Enter desired BPM: "))
    adjust_bpm(youtube_url, current_bpm, desired_bpm)