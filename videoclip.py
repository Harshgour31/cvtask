import librosa
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

def get_beats(audio_path):
    y, sr = librosa.load(audio_path)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    return beat_times


def create_video_from_clips(video_path, beat_times):
    video_clip = VideoFileClip(video_path)
    clips = []

    for i, beat_time in enumerate(beat_times[:-1]):
        start_time = beat_time
        end_time = beat_times[i + 1]
        clip = video_clip.subclip(start_time, end_time)
        clips.append(clip)

    final_clip = concatenate_videoclips(clips)
    return final_clip

def combine_audio_video(audio_path, video_clip, output_path):
    audio_clip = AudioFileClip(audio_path)
    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')



beat_times = get_beats("resource\song.mp3")
final_clip = create_video_from_clips("resource\\vi.mp4", beat_times)
combine_audio_video("resource\song.mp3", final_clip,"resource\out1.mp4")