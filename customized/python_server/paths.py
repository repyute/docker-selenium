import os

# Maven local repo
from pathlib import Path

home = str(Path.home())

rootPath = os.path.abspath(
    os.path.dirname(os.path.abspath(__file__))
)

# Env file path
envPath = os.path.abspath(
    os.path.join(rootPath, '.env')
)

logPath = os.path.abspath(
    os.path.join(rootPath, 'out.log')
)

outputPath = os.path.abspath(
    os.path.join(rootPath, 'output')
)
