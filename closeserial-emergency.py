from libs import  communications
from pyardrone import ARDrone
c=communications.CommunicationManager()
d= ARDrone()
d.emergency()
#c.close_serial_port()