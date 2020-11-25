# Learning Social Circles in Networks
Data Science Final Project, 2020 FALL

## Usage

Clone this repository
```
git clone https://github.com/Jennifer-Shiau/DS-Final-Project.git
cd DS-Final-Project
```

Parse data and output a friend-list
```
python3 parse.py
```
- Output `list/friend_list.txt`

Perform feature evaluation
```
python3 feature_evaluation.py
```
- Step 1
    - Process `data/features.txt` into `feature_dict`, which stores the feature values of all users
- Step 2
    - Count the number of values of each feature (`feat_count`)
- Step 3
    - Process `list/friend_list.txt` and evaluate features of each user and his/her friends (`feat_value`)
    - Output `list/feature_value.txt`

## Notes

Data Descriptions
- `data/egonets/*.egonets` : A list of the user's friends
    - userid: friend1 friend2 friend3 ...
- `data/features.txt` : User profiles
    - userid feature1 feature2 feature3 ...
- `data/featureList.txt` : Descriptions of features
    - birthday, education, work, ...

Output File Descriptions
- `list/friend_list.txt` : Friend-lists of all users
    - userid friend1 friend2 friend3 ...
- `list/feature_value.txt` : Values of all features
    - feature value
