import logging
from django.conf import settings


class Logger():

	@staticmethod
	def getLogger():
		#Simple wrapper. Ensures logging is always correctly configured (logging.basicConfig is executed)
		logger = logging.getLogger("thermostat.rules")
        logger.setLevel(settings.LOG_LEVEL)
        return logger
