
from django_thermostat.mappings import get_mappings
from pypelib.RuleTable import RuleTable
from django_thermostat.mappings import get_mappings
from django_thermostat.utils import gen_comparing_time
from django_thermostat.models import Rule


def evaluate():

    mappings = get_mappings()
    table = RuleTable(
        "Calecfaccion Invierno laborables",
        mappings,
        "RegexParser",
        #rawfile,
        "RAWFile",
        None)

    start_time = gen_comparing_time(10, 0, 0)

    end_time = gen_comparing_time(13, 0, 0)
    print " ############################## estar time: %s" % start_time
    print " ############################## end time: %s " % end_time
    print " ############################## current time: %s " % mappings["current_time"]()
    print " ############################## current day of week: %s" % mappings["current_day_of_week"]()
    print " ############################## current temp %s" % mappings["current_internal_temperature"]()
    print " ############################## economic %s" % mappings["economic_temperature"]()
    print " ############################## confort %s" % mappings["confort_temperature"]()
    print " ############################## tuned %s" % mappings["tuned_temperature"]()
    print " ############################## flame %s" % mappings["flame_on"]()
    print " ############################## heat on %s" % mappings["heater_on"]()
    table.setPolicy(True)

    table.addRule("if heater_manual = 1  then accept do tune_to_confort")
#    table.addRule("if (heater_manual = 0 ) && (0 = is_weekend) && ((current_time > %f) && (current_time < %f)) then accept" % (start_time, end_time))

    for rule in Rule.objects.filter(active=True).order_by("pk"):
        table.addRule(rule.to_pypelib())

 #   print "DUMP *******************************"
 #   table.dump()
 #   print "END DUMP *******************************"

    metaObj = {}

    #Create the metaObj

    table.evaluate(metaObj)

    table1 = RuleTable(
        "Calecfaccion",
        mappings,
        "RegexParser",
        #rawfile,
        "RAWFile",
        None)
    table1.addRule("if heater_on = 0 then deny")
    table1.addRule("if current_internal_temperature < tuned_temperature then accept")

    print "DUMP *******************************"
    table1.dump()
    print "END DUM **********************************"

    try:
        table1.evaluate(metaObj)
        try:
            mappings["start_flame"]()
        except Exception, ex:
            print "ERROR: Cant start flame: %s" % ex
    except Exception as e:
        try:
            mappings["stop_flame"]()
        except Exception, ex:
            print "ERROR: Cant stop flame: %s" % ex

