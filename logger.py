import logging
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
_ch = logging.StreamHandler()
_ch.setLevel(logging.INFO)
# _ch_formatter = logging.Formatter('[{}][{}]%(name)s,%(funcName)s:%(message)s'.format(_logfile, _filename))
_fh = logging.FileHandler(f"./log/{_filename}.log")

_fh.setLevel(logging.INFO)
_fh_formatter = logging.Formatter(
    "%(asctime)s, %(levelname)s, %(filename)s, %(message)s"
)
_ch.setFormatter(_fh_formatter)
_fh.setFormatter(_fh_formatter)
logger.addHandler(_fh)
# logger.addHandler(_ch)
# logger.info(f">{_filename}.log")
