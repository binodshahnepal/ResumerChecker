import os


def ensure_directories(paths: list[str]) -> None:
    for path in paths:
        os.makedirs(path, exist_ok=True)
