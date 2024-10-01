import os
import json
import random

paths_group1 = ['videos/mm-diffusion']
path_group2 = ['videos/new_sample_output_videos2', 'videos/new_sample_output_videos']
path_group3 = ['videos/visualization_train_ours', 'videos/visualization_eval_ours']
path_group4 = ['videos/visualization_train_s2g', 'videos/visualization_eval_s2g']
path_group5 = ['videos/visualization_train_angie', 'videos/visualization_eval_angie']


# 25 videos from each group, in total 125 videos, if we recruit 20 participants, 
# each watch 20 videos, in total 400 videos, so sample 4 from each group
# there should not be any repeated videos

# Step 2: Distribute videos into sets for participants
num_participants = 20

# Create a list of lists for each participant
participant_sets = {}

# Fill each participant's set
for i in range(num_participants):
    all_sampled_paths = []

    cur_group_videos = []
    for path in paths_group1:
        # randomly sample 25 videos
        for video in os.listdir(path):
            video_path = os.path.join(path, video)
            cur_group_videos.append(video_path)

    sampled_videos = random.sample(cur_group_videos, 4)
    all_sampled_paths.extend(sampled_videos)

    cur_group_videos = []
    for path in path_group2:
        # randomly sample 25 videos
        for video in os.listdir(path):
            video_path = os.path.join(path, video)
            cur_group_videos.append(video_path)

    sampled_videos = random.sample(cur_group_videos, 4)
    all_sampled_paths.extend(sampled_videos)

    cur_group_videos = []
    for path in path_group3:
        # randomly sample 25 videos
        for video in os.listdir(path):
            video_path = os.path.join(path, video)
            cur_group_videos.append(video_path)

    sampled_videos = random.sample(cur_group_videos, 4)
    all_sampled_paths.extend(sampled_videos)

    cur_group_videos = []
    for path in path_group4:
        # randomly sample 25 videos
        for video in os.listdir(path):
            video_path = os.path.join(path, video)
            cur_group_videos.append(video_path)

    sampled_videos = random.sample(cur_group_videos, 4)
    all_sampled_paths.extend(sampled_videos)

    cur_group_videos = []
    for path in path_group5:
        # randomly sample 25 videos
        for video in os.listdir(path):
            video_path = os.path.join(path, video)
            cur_group_videos.append(video_path)

    sampled_videos = random.sample(cur_group_videos, 4)
    all_sampled_paths.extend(sampled_videos)



    # Shuffle the complete list of sampled videos
    random.shuffle(all_sampled_paths)

    participant_sets[i] = all_sampled_paths

json_path = 'jsons'
if not os.path.exists(json_path):
    os.makedirs(json_path)

# Step 3: Write the participant sets to a JSON file
json_base = {
    "title": "Subjective Evaluation of Gesture Videos",

    "instructions": "Please watch each video and rate the videos based on Four evaluation metrics,\n \
        1. Realness: How realistic the video looks\n \
        2. Diversity: How diverse does the gesture pattern presen\n \
        3. Naturalness: Are speech and gesture synchronized in this video\n \
        4. Overall: Overall quality of the video\n \
    Please rate each video on a scale of 1 to 5, where 1 is the lowest and 5 is the highest\n",

    "groups":[]
}

for i, participant_set in participant_sets.items():
    
    cur_json = json_base.copy()
    for video_path in participant_set:
        id_name = None
        if 'mm-diffusion' in video_path:
            id_name = 'mm-diffusion'
        elif 'new_sample_output_videos2' in video_path:
            id_name = 'gt'
        elif 'new_sample_output_videos' in video_path:
            id_name = 'gt'
        elif 'visualization_train_ours' in video_path:
            id_name = 'ours'
        elif 'visulization_eval_ours' in video_path:
            id_name = 'ours'
        elif 'visualization_train_s2g' in video_path:
            id_name = 's2g'
        elif 'visulization_eval_s2g' in video_path:
            id_name = 's2g'
        elif 'visualization_train_angie' in video_path:
            id_name = 'angie'
        elif 'visulization_eval_angie' in video_path:
            id_name = 'angie'

        video_path = '../' + video_path
        group = {
            "sample_id": id_name,
            # the video path
            "video": video_path,
            "captions": [ # realness
                "1. Terrible, can't recognized as human gestures\n\
                2. Poor, it is not real\n\
                3. Fair, hard to judge\n\
                4. Good, better, it looks real\n\
                5. Excellent, it is what a human would do\n",
                # diversity
                "1. Terrible, it is not diverse at all\n\
                2. Poor, it is not diverse\n\
                3. Fair, it is hard to judge\n\
                4. Good, it various but a little bit limited\n\
                5. Excellent, it is what a human would do\n",
                # synchrony
                "1. Terrible, it is not synchronized at all\n\
                2. Poor, it is not synchronized\n\
                3. Fair, it is hard to judge\n\
                4. Good, it is synchronized but not perfect\n\
                5. Excellent, it is perfectly synchronized\n",
                # overall
                "1. Terrible, it is not good at all\n\
                2. Poor, it is not good\n\
                3. Fair, it is hard to judge\n\
                4. Good, it is good\n\
                5. Excellent, it is perfect\n",
                ],
            }
        cur_json["groups"].append(group)
    
    # save the json file
    with open(f'{json_path}/participant_{i+1}.json', 'w') as f:
        json.dump(cur_json, f, indent=4)
        print(f'Participant {i+1} JSON file saved')
    

