#! /usr/bin/env python
from datetime import datetime, timedelta

hour = timedelta(hours=1)
minute = timedelta(minutes=1)

now = datetime.now()
later = now+(5*minute)

print(later.strftime("%H:%M"))


