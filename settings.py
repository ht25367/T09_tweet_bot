import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), 'setting.env')
load_dotenv(dotenv_path)

# 使用例
USN = os.environ.get("USER_NAME")

# プロジェクト用、環境変数の設定
API_KEY = os.environ.get("API_key")
API_SECRET = os.environ.get("API_secret")
BEARER_TOKEN = os.environ.get("Bearer_token")
ACCESS_TOKEN = os.environ.get("Access_token")
ACCESS_SECRET = os.environ.get("Access_secret")
