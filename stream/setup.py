from setuptools import setup

def readfile_as_list(path):
    with open(path, 'r') as fh:
        return [l.strip() for l in fh.read().strip().split("\n")]

setup(
    name='TweetStream',
    version='1.0',
    install_requires=readfile_as_list('requirements.txt'),
    py_modules=[
        'application',
        'encoding_fix',
        'tweetstream',
        'twitter_authentication',
    ],
    packages=[
        'tweepy',
        'win_unicode_console',
    ]
)
