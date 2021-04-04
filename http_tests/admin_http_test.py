import pytest
import requests
import json
from src.config import url
from src.error import AccessError, InputError
from src.admin import user_remove_v1, userpermission_change_v1
from src.other import clear_v1
from jwt import encode


