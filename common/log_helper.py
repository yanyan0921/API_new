import logging


class Logger:
    def __init__(self, runner_id):
        logger = logging.getLogger("main")
        logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler(runner_id + ".txt")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)

        logger.addHandler(handler)
        logger.addHandler(console)
