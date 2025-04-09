# _*_ coding: UTF-8 _*_
"""
@Project  : tk_Flask
@File     : test.py
@Author   :wangmaosheng
@Date     : 2025/3/24 22:40
@Desc:    :
"""


from moviepy.editor import VideoFileClip, concatenate_videoclips
import whisper

# 1. 加载视频并提取音频
video = VideoFileClip("movie.mp4")
audio = video.audio
audio.write_audiofile("movie_audio.mp3")

# 2. 语音转字幕（Whisper）
model = whisper.load_model("base")
result = model.transcribe("movie_audio.mp3")

# 3. 计算字幕与 DeepSeek 文案相似度（GPT 处理）
deepseek_script = ["英雄终于打败了反派", "主角迎来了结局", "爆炸场面十分震撼"]
selected_clips = []
for i, segment in enumerate(result["segments"]):
    text = segment["text"]
    if any(kw in text for kw in deepseek_script):
        start, end = segment["start"], segment["end"]
        selected_clips.append(video.subclip(start, end))

# 4. 拼接高光片段
final_clip = concatenate_videoclips(selected_clips)
final_clip.write_videofile("highlight.mp4")