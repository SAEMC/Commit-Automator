# Commit Automator

This is a Commit Automator checks number of commits needed, and then commits & pushes it into your Github automatically. Also this displays how your art will look in the GitHub contribution count.

---

## Prerequisites

### Requirements

- Git and Github account
- Python with Conda environment
- Cron

### Set directories

```shell
# Assume that you are in $HOME like '/home/you/'
# So you run these commands, then you will be in '/home/you/Automator/'
mkdir Automator && cd Automator/


# Clone this repository
git clone https://github.com/SAEMC/Commit-Automator.git


# Create a directory for new repository
# Notice that you had to create new remote repository in Github first (Enter your Github username below)
mkdir Auto-Commit && cd Auto-Commit/ && \
echo "# Auto-Commit" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/YourGithubUsername/Auto-Commit.git
git push -u origin main


# You must be in '/home/you/Automator/'
cd ..
```

```
# Now structure is like:
Automator <- You are here
├── Auto-Commit
│   └── README.md
└── Commit-Automator
    ├── LICENSE.txt
    ├── README.md
    ├── art.json.example
    ├── commit-automator
    │   ├── __init__.py
    │   ├── __main__.py
    │   ├── __version__.py
    │   ├── actions.py
    │   ├── calculator.py
    │   ├── committer.py
    │   ├── dataloader.py
    │   ├── logger.py
    │   ├── main.py
    │   └── painter.py
    └── requirements.txt
```

### Create a Conda environment

```shell
# Create and activate a Conda env
conda create -n automator python=3.9 -y
conda activate automator


# You can check the path of Python runtime
# The path shown after run this command is important when use Cron
(automator) which python
```

### Install Python dependencies

```shell
(automator) pip install -r Commit-Automator/requirements.txt
```

<br/>

## Usages

### Handle `art.json`

```shel
# Copy or move 'Commit-Automator/art.json.example' to 'Commit-Automator/art.json'
cp Commit-Automator/art.json.exmaple Commit-Automator/art.json
```

```
# Now you can change the values:
# 1. 'user_name' must be your Github username
# 2. 'art_name' is name of art
#    I've set 'snoopy' for example
# 3. 'start_date' must start from Sunday
# 4. 'duration' is a cycle of painting your art
#    'duration' and length of 'pixels_level' must be same
# 5. 'pixels_level' is color depth from 0 to 4
#    You can see contirbution count color in Github profile page
#    I've set 'snoppy' for example

{
  "user_name": "Username",
  "art_name": "snoopy",
  "start_date": "2022-12-11",
  "duration": 12,
  "pixels_level": [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 4, 4, 1],
    [1, 1, 1, 3, 2, 2, 3],
    [1, 1, 3, 2, 2, 2, 2],
    [1, 1, 3, 2, 2, 2, 2],
    [1, 3, 2, 2, 2, 2, 2],
    [3, 2, 4, 4, 2, 2, 2],
    [3, 2, 2, 2, 2, 2, 2],
    [3, 2, 2, 2, 2, 2, 2],
    [1, 3, 2, 3, 3, 3, 3],
    [1, 1, 3, 3, 2, 2, 3],
    [1, 1, 1, 3, 3, 3, 1]
  ]
}
```

### Use Commit-Automator

```shell
# This is default command
python Commit-Automator/commit-automator -f FilenameOfArt [-x {commit,display}] [-l]


# This is same
python Commit-Automator/commit-automator --file=FilenameOfArt [--execute={commit,display}] [--save-log]


# You'd better check helps
python Commit-Automator/commit-automator -h
```

#### commit

##### 1. Manually

```shell
# 'githubAccessToken' must be already set in environment variables
(automator) export githubAccessToken="YourGithubAccessToken"


# You must be in new repository
(automator) cd Auto-Commit/


# Filename of art is 'art.json' here, but you can change it
(automator) python ../Commit-Automator/commit-automator -f art.json
```

##### 2. Automatically

```
# In the Crontab editor (via '$ crontab -e')


...


# 'githubAccessToken' must be already set in environment variables
githubAccessToken="YourGithubAccessToken"


# You have to change these in the following line:
# 1. Schedule
# 2. Directory of new repository
# 3. Path of Python runtime
# 4. Path of commit-automator package
# 5. Filename of art is 'art.json' here, but you can change it
* * * * * cd /home/you/Automator/Auto-Commit/ ; /the/path/shown/after/run/which/python /home/you/Automator/Commit-Automator/commit-automator -f art.json -l
```

```shell
# And then run this command
service cron restart


# Additionally, you can check the status of Cron
service cron status
```

#### display

```shell
# The feature displaying art cannot save in the log file, this just shows in the shell

# Assume that you are in '/home/you/Automator/'
# Filename of art is 'art.json' here, but you can change it
python Commit-Automator/commit-automator -f art.json -x display


# Also you can do like this:
python Commit-Automator/commit-automator --file=art.json --execute=display
```
