import os
import json
import random
from copy import deepcopy

path_group1 = ['videos/mmm']
path_group2 = ['videos/momask']
path_group3 = ['videos/stmc']
path_group4 = ['videos/ours']
# path_group5 = ['videos/real']


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
    for path in path_group1:
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

    # cur_group_videos = []
    # for path in path_group5:
    #     # randomly sample 25 videos
    #     for video in os.listdir(path):
    #         video_path = os.path.join(path, video)
    #         cur_group_videos.append(video_path)

    # sampled_videos = random.sample(cur_group_videos, 4)
    # all_sampled_paths.extend(sampled_videos)



    # Shuffle the complete list of sampled videos
    random.shuffle(all_sampled_paths)

    participant_sets[i] = all_sampled_paths

json_path = 'jsons'
if not os.path.exists(json_path):
    os.makedirs(json_path)

# Step 3: Write the participant sets to a JSON file
json_base = {
    "title": "Subjective Evaluation of Human Motion Videos",

    "instructions": "Please watch each video and rate the videos based on Three evaluation metrics,\n \
        1. Realness: How human-like the motion in the video looks\n \
        2. Alignment: How close the motion represents to its text description\n \
        3. Overall: Overall quality of the video\n \
    Please rate each video on a scale of 1 to 5, where 1 is the lowest and 5 is the highest\n",

    "groups":[]
}

for i, participant_set in participant_sets.items():
    # do deep copy, do not modify the original json_base
    cur_json = deepcopy(json_base)
    for video_path in participant_set:
        id_name = None
        if 'mmm' in video_path:
            id_name = 'mmm'
        elif 'momask' in video_path:
            id_name = 'momask'
        elif 'stmc' in video_path:
            id_name = 'stmc'
        elif 'ours' in video_path:
            id_name = 'ours'
        elif 'real' in video_path:
            id_name = 'real'

        video_path = '../' + video_path
        group = {
            "sample_id": id_name,
            # the video path
            "video": video_path,
            "captions": [ 
                # realness
                "1. Terrible, Completely Unnatural movements\n\
                2. Poor, with many errors and unnatural\n\
                3. Fair, hard to judge\n\
                4. Good, better, it looks real\n\
                5. Excellent, it is what a natural human motion\n",
                # alignment
                "1. Terrible, it is not what the text describes at all\n\
                2. Poor, poorly aligned with the text description\n\
                3. Fair, it is hard to judge\n\
                4. Good, almost aligns with text, with small error\n\
                5. Excellent, it is exactly what the text describes\n",
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
    

