import tomllib
import os

class DefaultConfig:
    PROMPTS = tomllib.load(open(os.path.join(os.path.dirname(__file__), "prompts.toml"), "rb"))
    