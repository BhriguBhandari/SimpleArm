import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/bbhanda/scoutbot_ws/src/scoutbot_description/install/scoutbot_description'
