import os
from pytube import YouTube
from pydub import AudioSegment
import tempfile

def adjust_bpm(youtube_url, current_bpm, desired_bpm):
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
    
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Download the YouTube video
        print(f"Downloading video from {youtube_url}...")
        yt = YouTube(youtube_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        download_path = audio_stream.download(output_path=temp_dir)
        
        # Convert to wav for processing
        print("Converting to WAV format...")
        sound = AudioSegment.from_file(download_path)
        
        # Adjust the speed without changing pitch
        print(f"Adjusting BPM from {current_bpm} to {desired_bpm} (speed ratio: {speed_ratio:.2f})...")
        adjusted_sound = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed_ratio)
        })
        adjusted_sound = adjusted_sound.set_frame_rate(sound.frame_rate)
        
        # Create output filename
        video_title = yt.title
        safe_title = "".join([c for c in video_title if c.isalnum() or c in " -_"]).strip()
        output_filename = f"{safe_title}_{current_bpm}to{desired_bpm}bpm.mp3"
        output_path = os.path.join(os.getcwd(), output_filename)
        
        # Export the result
        print(f"Exporting to {output_path}...")
        adjusted_sound.export(output_path, format="mp3")
        
        print("Done!")
        return output_path
    
    finally:
        # Clean up temporary files
        for file in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, file))
        os.rmdir(temp_dir)

if __name__ == "__main__":
    youtube_url = input("Enter YouTube URL: ")
    current_bpm = float(input("Enter current BPM: "))
    desired_bpm = float(input("Enter desired BPM: "))
    
    output_file = adjust_bpm(youtube_url, current_bpm, desired_bpm)
    print(f"Adjusted audio saved to: {output_file}")
