import os
import shutil
from moviepy.editor import VideoFileClip

# Set the base directory where your videos are located
base_dir = 'videos/'

# Step 1: Rename files that contain '#' to use '_'
for root, dirs, files in os.walk(base_dir):
    for filename in files:
        if '#' in filename:
            new_filename = filename.replace('#', '_')
            old_file = os.path.join(root, filename)
            new_file = os.path.join(root, new_filename)
            os.rename(old_file, new_file)
            print(f'Renamed: {old_file} -> {new_file}')

# Step 2: Define paths for video management
paths = [
    'videos/visualization_train_ours',
    'videos/visualization_train_s2g',
    'videos/visualization_train_angie',
    'videos/visualization_eval_ours',
    'videos/visualization_eval_s2g',
    'videos/visualization_eval_angie'
]

# Step 3: Process videos
for path in paths:
    for video in os.listdir(path):
        video_path = os.path.join(path, video)
        
        # Remove videos that do not contain 'audio'
        if 'audio' not in video:
            os.remove(video_path)
            print(f'Removed: {video_path}')

# Step 3: Process videos
for path in paths:
    for video in os.listdir(path):
        video_path = os.path.join(path, video)
        
        # Remove videos that do not contain 'audio'
        if 'audio' not in video:
            os.remove(video_path)
            print(f'Removed: {video_path}')
        
        # Rename videos in 'visualization_ours_train'
        if path == 'videos/visualization_train_ours' or path == 'videos/visualization_eval_ours':
            # Change name format
            new_video = '_'.join(video.split('_')[:2]) + '_audio.mp4'
            new_video_path = os.path.join(path, new_video)
            os.rename(video_path, new_video_path)
            print(f'Renamed: {video_path} -> {new_video_path}')

# Step 2: Define paths for video management
train_path = ['videos/visualization_train_ours', 'videos/visualization_eval_ours']
gt_paths = ['videos/sample_output_videos', 'videos/sample_output_videos2']

# Step 3: Collect training video names
train_videos = {}
for path in train_path:
    for video in os.listdir(path):
        if 'audio' in video:  # Assuming we are interested in audio videos
            train_videos[video] = os.path.join(path, video)

# Step 4: Process GT videos
for gt_path in gt_paths:
    for gt_video in os.listdir(gt_path):
        gt_video_path = os.path.join(gt_path, gt_video)
        
        # Check for a matching training video
        for train_video in train_videos:
            if train_video.replace('_audio', '') in gt_video:  # Match base name
                # Load the GT video and the training audio
                gt_clip = VideoFileClip(gt_video_path)
                train_audio_path = train_videos[train_video]
                train_audio_clip = VideoFileClip(train_audio_path).audio

                # Set the audio to the GT video
                gt_clip = gt_clip.set_audio(train_audio_clip)

                # Clip the GT video to match the length of the training video
                train_clip = VideoFileClip(train_audio_path)
                duration = min(gt_clip.duration, train_clip.duration)
                gt_clip = gt_clip.subclip(0, duration)

                # Save the modified GT video
                new_gt_video_path = os.path.join(gt_path, f"modified_{gt_video}")
                gt_clip.write_videofile(new_gt_video_path, codec='libx264', audio_codec='aac')
                
                print(f'Processed: {gt_video_path} -> {new_gt_video_path}')

                # Close the clips
                gt_clip.close()
                train_audio_clip.close()
                break

# move the modified GT videos to the new GT folder, and rename them to match the training videos
new_gt_path1 = 'videos/new_sample_output_videos'
new_gt_path2 = 'videos/new_sample_output_videos2'
os.makedirs(new_gt_path1, exist_ok=True)
os.makedirs(new_gt_path2, exist_ok=True)

for gt_path in gt_paths:
    new_gt_path = new_gt_path1 if gt_path == gt_paths[0] else new_gt_path2
    for gt_video in os.listdir(gt_path):
        gt_video_path = os.path.join(gt_path, gt_video)
        if gt_video.startswith('modified_'):
            new_gt_video_path = os.path.join(new_gt_path, gt_video.replace('modified_', ''))
            shutil.move(gt_video_path, new_gt_video_path)
            print(f'Moved: {gt_video_path} -> {new_gt_video_path}')
