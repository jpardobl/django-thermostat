from django.core.management.base import BaseCommand, CommandError
from pypelib.RuleTable import RuleTable
from django_thermostat.mappings import get_mappings
from django_thermostat.mappings.timings import gen_comparing_time


class Command(BaseCommand):
    args = ''
    help = 'Evaluate rules realted to heater status. The result will start or stop the heater'

    def handle(self, *args, **options):
        mappings = get_mappings()
        table = RuleTable(
            "Calecfaccion Invierno laborables",
            mappings,
            "RegexParser",
            #rawfile,
            "RAWFile",
            None)

        start_time = gen_comparing_time(00, 00, 00)

        end_time = gen_comparing_time(22, 00, 00)
        print " ############################## estar time: %s" % start_time
        print " ############################## end time: %s " % end_time
        print " ############################## current day of week: %s" % mappings["current_day_of_week"]()
        print " ############################## current temp %s" % mappings["current_internal_temperature"]()
        print " ############################## economic %s" % mappings["economic_temperature"]()
        print " ############################## confort %s" % mappings["confort_temperature"]()
        print " ############################## flame %s" % mappings["flame_on"]()
        table.setPolicy(False)

        table.addRule("if heater_on = 0 then deny")
        table.addRule("if (heater_manual = 1 ) && ( current_internal_temperature < confort_temperature) then accept")
        table.addRule("if (heater_manual = 0 ) && (1 = is_weekend) && ((current_hour > %f) && (current_hour < %f)) && (current_internal_temperature < confort_temperature) then accept" % (start_time, end_time))
        table.addRule("if current_internal_temperature < economic_temperature then accept")

        print "DUMP *******************************"
        table.dump()

        print "END DUMP *******************************"

        metaObj = {}

        #Create the metaObj

        try:

            table.evaluate(metaObj)
            mappings["start_flame"]()
        except Exception as e:
            mappings["stop_flame"]()
