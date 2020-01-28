activate_this = '/var/www/html/flask/env/bin/activate_this.py'

with open(activate_this) as f:
 exec(f.read(), dict(__file__=activate_this))

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/html/flask")

from control import app as application