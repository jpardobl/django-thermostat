import requests, logging, re
from django_thermostat import settings
from django.core.management.base import BaseCommand, CommandError
from time import localtime, time, mktime

class Command(BaseCommand):
    args = ''
    help = 'Parse de date stats file to retrieve the statistics aggregation for the last N minutes.'

    def _time_range(self, length):
        current = time()
        return [float(current - length * 60), float(current)]

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.DEBUG)
        
        if len(args) != 1:
            self.stderr.write("Please send argument of how many minutes")
            exit(1)
        with open(settings.FLAME_STATS_PATH) as f:
            contents = f.readlines()
        t_range = self._time_range(int(args[0]))
        logging.debug("Time range %s" % t_range)
        cont = 0
        
        
        data = []
        for line in contents:
            cont = cont + 1
            m = re.search("(\d+\.\d+)\n$", line)
            
            if m is None:
                logging.warn("Format of line %d not correct, cannot find time from epoch at the end" % cont)
                continue
            time = float(m.groups(0)[0])

            if time < t_range[0] or time > t_range[1]:
                logging.debug("Dejamos la linea %d fuera porque se sale del rango pedido" % cont)
                continue
            
            m = re.search("^(ON|OFF)", line)
            if m is None:
                logging.warn("Format of line %d not correct, cannot find ON|OFF action at the beginning" % cont)
                
                continue
            action = m.groups(0)[0]
            data.append([action, time])

        last_start = None
        last_heating_period = None
        total_heating_period = 0
        for action, time in data:
            if action == "ON":
                last_start = time
                last_heating_period = None
            if action == "OFF" and last_start is not None:
                #TODO que pasa si last_start es None
                last_heating_period = time - last_start 
                last_start = None
                
            total_heating_period = total_heating_period + (last_heating_period if last_heating_period is not None else 0)
            logging.debug("action: %s time: %d; %d %d %d" % (
                        action, 
                        time,
                        last_heating_period if last_heating_period is not None else 0,
                        last_start if last_start is not None else 0,
                        total_heating_period))
        
        #if the first action in data is OFF, means the flame was on by the starting of the time range
        #it is needed to add this time
        if len(data) and data[0][0] == "OFF":
            print data[0][1]
            total_heating_period = total_heating_period + (data[0][1] - t_range[0])
        
        #if the last action is ON, need to add the time from the instance of that last action,
        #to the end of the range
        if len(data) and data[len(data)-1][0] == "ON":
            total_heating_period = total_heating_period + (t_range[1] - data[0][1])
            
        print "total_heating_period:%d " % total_heating_period
