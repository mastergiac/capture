import logging
import socket
import os
import sys
import datetime
import urllib

logger = None

CAMERA_IP_ADDRESS = "http://10.0.1.11"
CAMERA_PICTURE_LARGE = "%s/snapshot/view0.jpg" % CAMERA_IP_ADDRESS
CAMERA_PICTURE_SMALL = "%s/snapshot/view4.jpg" % CAMERA_IP_ADDRESS
IP_ADDRESS = (socket.gethostbyname(socket.gethostname())).replace(".","_")

PICUTRE_BASE_DIRECTORY="/var/tmp/%s" % IP_ADDRESS
fmt = '%Y_%m_%d-%H_%M'

def initialize():
	global logger
	# create logger
	logger = logging.getLogger('%s' % IP_ADDRESS)
	logger.setLevel(logging.DEBUG)
	# create file handler which logs even debug messages
	fh = logging.FileHandler('/var/tmp/%s_capture.log' % IP_ADDRESS)
	fh.setLevel(logging.DEBUG)
	# create console handler with a higher log level
	ch = logging.StreamHandler()
	ch.setLevel(logging.ERROR)
	# create formatter and add it to the handlers
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh.setFormatter(formatter)
	ch.setFormatter(formatter)
	# add the handlers to the logger
	logger.addHandler(fh)
	logger.addHandler(ch)
	
	if os.path.exists(PICUTRE_BASE_DIRECTORY) == False:
		logger.info("Creating directory '%s'" % PICUTRE_BASE_DIRECTORY)
		try:
			os.makedirs(PICUTRE_BASE_DIRECTORY)
		except Exception as e:
			logger.error("Creating directory '%s'" % PICUTRE_BASE_DIRECTORY)
			logger.error(e)
			sys.exit(-1)


def capture_picture(output_directory=None):
	logger.info("Start capture_picture method")
	imageFile = "%s/%s.jpg" % (output_directory,  datetime.datetime.now().strftime(fmt))
	try:
		urllib.urlretrieve(CAMERA_PICTURE_SMALL, imageFile)
	except Exception as e:
		logger.error("capture_picture '%s'" % imageFile)
		logger.error(e)
		sys.exit(-1)


def main():
	initialize()
	logger.info("Start main method")
	capture_picture(PICUTRE_BASE_DIRECTORY)



if __name__ == "__main__":
	main()