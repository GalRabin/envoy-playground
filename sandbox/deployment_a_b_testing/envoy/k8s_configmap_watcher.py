import hashlib
import logging
import os
import signal
import sys
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

ENVOY_CONFIGMAP_NAME = "envoy-config"
ENVOY_NAMESPACE = "sandbox"
ENVOY_CONFIG_PATH = os.getenv("ENVOY_CONF_PATH")
LOG_PATH = "/logs/k8s_configmap_watcher.log"
PPPID = int(sys.argv[1])
LAST_FILES_HASH = None

logger = logging.getLogger(__name__)


def calculate_dir_files_cache(path: str) -> str:
    files_content = b""
    logger.debug("Calculating new conf files hash")
    for child_path in Path(path).iterdir():
        if (
            child_path.is_file()
            and child_path.name.endswith(".yaml")
            or child_path.name.endswith(".yml")
        ):
            logger.debug(f"Adding file {child_path} to hash")
            files_content += child_path.read_bytes()

    return hashlib.shake_128(files_content).hexdigest(10)


def init_logger(path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    logger.setLevel(logging.DEBUG)
    file_handler = RotatingFileHandler(path, maxBytes=10000, backupCount=5)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)


def wait_until_directory_conf_change(path: str):
    logger.info("Start envoy configuration watcher")
    while True:
        time.sleep(5)
        current_files_hash = calculate_dir_files_cache(path)
        logger.debug(f"Last known file hashes - {LAST_FILES_HASH}")
        logger.debug(f"Current known file hashes - {current_files_hash}")

        if current_files_hash != LAST_FILES_HASH:
            logger.info("Envoy configuration file changed")
            trigger_envoy_hot_restart()
            break


def trigger_envoy_hot_restart():
    logger.info("Triggering envoy hot restart")
    if PPPID:
        logger.info(f"Sending SIGHUP signal to process {PPPID}")
        os.kill(PPPID, signal.SIGHUP)
    else:
        logger.info("Skipping SIGHUP sending, Argument PPPID is missing")


if __name__ == "__main__":
    init_logger(LOG_PATH)
    LAST_FILES_HASH = calculate_dir_files_cache(ENVOY_CONFIG_PATH)
    wait_until_directory_conf_change(ENVOY_CONFIG_PATH)
