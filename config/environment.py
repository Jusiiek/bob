import os

from dotenv import load_dotenv


load_dotenv()

HERE = os.getcwd()
COGS_FOLDER = os.path.join(HERE, 'cogs')
SERVERS_DIR = os.path.join(HERE, 'servers')

TOKEN = os.getenv('TOKEN')
SERVER_ID = os.getenv('SERVER_ID')
