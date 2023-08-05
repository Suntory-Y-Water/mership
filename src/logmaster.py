import os
import sys
from logging import getLogger, DEBUG, Formatter, FileHandler, StreamHandler

class WriteLogger(object):
    def __init__(self):

        folder_name = "../log"
        file_name = "log.txt"

        self.create_log_files(folder_name, file_name)
        self.configure_loggers(folder_name, file_name)

    def create_log_files(self, folder_name, file_name):
        file_path = os.path.join(folder_name, file_name)
        if not os.path.exists(file_path):
            os.makedirs(folder_name, exist_ok=True)
            with open(file_path, "w") as file:
                pass

    def configure_loggers(self, folder_name:str, file_name:str):
        formatter = Formatter('%(asctime)s - %(message)s')

        self.logger = self.create_logger("logger", folder_name, file_name, formatter, DEBUG)

    def create_logger(self, name:str, folder_name:str, file_name:str, formatter:str, level:str):
        logger = getLogger(name)
        logger.setLevel(level)

        for h in logger.handlers[:]:
            logger.removeHandler(h)
            h.close()

        # ファイルハンドラーを追加
        file_handler = FileHandler(os.path.join(folder_name, file_name), encoding="UTF-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # ストリームハンドラー（ターミナル出力）を追加
        stream_handler = StreamHandler(sys.stdout)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger