import os
import sys

if 'site-packages' not in sys.path:
  sys.path.append(os.path.join(os.path.dirname(__file__), "site-packages"))

from flask import Flask

app = Flask('last-years')

import views
