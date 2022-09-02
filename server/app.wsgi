import sys
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
sys.path.insert(0, '/var/www/lge_backend')
sys.path.insert(0, '/var/www/lge_backend/venv/lib/python3.10/site-packages')
from lge_backend.app import app