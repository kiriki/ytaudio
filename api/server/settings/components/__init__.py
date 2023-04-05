import os
from pathlib import Path

from decouple import AutoConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).parent.parent.parent.parent
os.environ.setdefault('BASE_DIRECTORY', BASE_DIR.as_posix())

# Loading `.env` files
# See docs: https://gitlab.com/mkleehammer/autoconfig
config = AutoConfig(search_path=BASE_DIR.joinpath('config'))
