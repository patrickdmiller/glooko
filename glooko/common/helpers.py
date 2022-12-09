import logging
import pytz
import re
from datetime import datetime
from glooko.common import config
def glooko_pump_ts_to_UTC(ts, tz = config.TIMEZONE):
  local = pytz.timezone(config.TIMEZONE)
  ts = re.sub(r'\.\d{3}?Z','',ts)
  date_obj =  datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")
  local_dt = local.localize(date_obj, is_dst=True)
  utc_dt = local_dt.astimezone(pytz.utc)
  logging.debug(f'converting time from {date_obj} to utc {utc_dt}')
  return utc_dt