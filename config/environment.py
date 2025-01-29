from enum import Enum


class Environment(str, Enum):
    DEV = 'DEV'
    STABLE = 'STABLE'
    LOAD_TESTING = 'LOAD_TESTING'
