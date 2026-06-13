from enum import Enum

class Retry(int,Enum):
    max_tries= 3