import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/opt/WAFX')

from app import app as application