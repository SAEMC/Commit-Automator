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
# Now structure looks like:
Automator <- You are here
├── Auto-Commit
│   └── README.md
└── Commit-Automator
    ├── LICENSE.txt
    ├── README.md
    ├── assets
    │   ├── Snoopy.png
    │   └── Whale.png
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
    ├── examples
    │   ├── art.json.example
    │   └── cron4commit.sh.example
    └── requirements.txt
```

### Create a Conda environment

```shell
# Create and activate a Conda env
conda create -n automator python=3.9 -y && \
conda activate automator


# You can check the path of Python runtime
# The path shown after run this command is important when you use Cron
(automator) which python
```

### Install Python dependencies

```shell
# Install Python dependencies which will be saved in the Conda env
(automator) pip install -r Commit-Automator/requirements.txt
```

<br/>

## Usages

### Handle `art.json`

```shell
# Copy or move 'Commit-Automator/examples/art.json.example' to 'Commit-Automator/art.json'
cp Commit-Automator/examples/art.json.exmaple Commit-Automator/art.json
```

```
# In 'art.json'

# Now you can change the values:
# 1. 'user_name' must be your Github username
# 2. 'art_name' is name of art
#    I've set 'Snoopy' for example
# 3. 'start_date' must start from Sunday
# 4. 'duration' is a cycle of painting your art
#    'duration' and length of 'pixels_level' must be same
# 5. 'pixels_level' is color depth from 0 to 4
#    You can see contirbution count color in Github profile page
#    I've set 'Snoppy' for example

{
  "user_name": "Username",
  "art_name": "Snoopy",
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

# This 'art.json' shows Snoopy like below,
# and in my case, it shows Whale:
```

<p align="center">
  <img src="./assets/Snoopy.png" alt="Snoopy" width="400" height="180">
  <img src="./assets/Whale.png" alt="Whale" width="400" height="180">
</p>

### Use Commit-Automator

```shell
# This is default command
python Commit-Automator/commit-automator -f FilenameOfArt [-x {commit,display}] [-l]


# This is same
python Commit-Automator/commit-automator --file=FilenameOfArt [--execute={commit,display}] [--save-log]


# You'd better check helps
python Commit-Automator/commit-automator -h
```

### Use Commit-Automator with `commit`

#### 1. Manually

```shell
# 'githubAccessToken' must be already set in environment variables
(automator) export githubAccessToken="YourGithubAccessToken"


# You must be in new repository
(automator) cd Auto-Commit/


# Filename of art is 'art.json' here, but you can change it
# Saving log file is 'True' here, but you can change it
(automator) python ../Commit-Automator/commit-automator -f art.json -l
```

#### 2. Automatically

```shell
# Copy or move 'Commit-Automator/examples/cron4commit.sh.example' to 'Commit-Automator/cron4commit.sh'
cp Commit-Automator/examples/cron4commit.sh.exmaple Commit-Automator/cron4commit.sh
```

```shell
# In 'cron4commit.sh'

# Whenever the paths are changed,
# you just modify this script without running Cron restart command


...


# You have to change these in the following lines:
# 1. Directory of new repository
# 2. Path of Python runtime
# 3. Path of commit-automator package
# 4. Filename of art is 'art.json' here, but you can change it
# 5. Saving log file is 'True' here, but you can change it

cd /home/you/Automator/Auto-Commit/ && \                   # 1
  /the/path/shown/after/run/which/python \                 # 2
  /home/you/Automator/Commit-Automator/commit-automator \  # 3
  -f art.json -l                                           # 4, 5
```

```
# In the Crontab editor (via '$ crontab -e')

# When you get the schedule and path of 'cron4commit.sh' fixed once,
# you might be never worry about the paths of
# the directory of new repository, Python runtime, etc.
# So I love this way

...


# 'githubAccessToken' must be already set in environment variables
githubAccessToken="YourGithubAccessToken"


# You have to change schedule
# For example, '* * * * *' -> '45 23 * * *'
# And have to change the path of 'cron4commit.sh'
* * * * * /home/you/Automator/Commit-Automator/cron4commit.sh
```

```shell
# And then run this command
service cron restart


# Additionally, you can check the status of Cron
service cron status
```

### Use Commit-Automator with `display`

```shell
# Assume that you are in '/home/you/Automator/'
# Filename of art is 'art.json' here, but you can change it
python Commit-Automator/commit-automator -f art.json -x display


# Also you can do like this:
python Commit-Automator/commit-automator --file=art.json --execute=display
```
