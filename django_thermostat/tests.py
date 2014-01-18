#This file mainly exists to allow python setup.py test to work.
import unittest, os, subprocess
from django_thermostat.models import *
from django_thermostat.mappings.weather import log_flame_stats
from django_thermostat import settings
from time import sleep


class TestMappings(unittest.TestCase):
    def test_is_at_night(self, ):
        from mappings.timings import is_at_night
        self.assertTrue(is_at_night() == 1,
            "Not properly calculating is_at_night")


class TestFlameStatsParser(unittest.TestCase):
    
    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_regular(self):
        os.remove(settings.FLAME_STATS_PATH)
        log_flame_stats(True)
        sleep(5)
        log_flame_stats(False)
        out = subprocess.check_output(["python", "manage.py", "parse_flame_stats", "1"])
        #self.assertRegexpMatches(text, expected_regexp, msg)
        self.assertRegexpMatches(
            out,
            "5\n$",
            "not properly parsing regular example of flame stats: %s" % out)
        
    def test_without_final_off(self):
        os.remove(settings.FLAME_STATS_PATH)
        log_flame_stats(True)
        sleep(5)
        out = subprocess.check_output(["python", "manage.py", "parse_flame_stats", "1"])
        self.assertRegexpMatches(
            out,
            "5\n$",
            "not properly parsing without final_off: %s" % out)
    
    def test_starts_before_time_range(self):
        os.remove(settings.FLAME_STATS_PATH)
        log_flame_stats(True)
        sleep(61)
        out = subprocess.check_output(["python", "manage.py", "parse_flame_stats", "1"])
        self.assertRegexpMatches(
            out,
            "60\n$",
            "not properly parsing without final_off: %s" % out)
        
    

class TestRules(unittest.TestCase):
    def setup(self, ):
        Day(name="Mon", value="Mon").save()
        Day(name="Tue", value="Tue").save()
        Day(name="Wed", value="Wed").save()
        Day(name="Thu", value="Thu").save()
        Day(name="Fri", value="Fri").save()

    def test_to_pyplib(self, ):
        self.setup()
        d = Day.objects.get(name="Mon")

        tr = TimeRange(start="6:00:00", end="7:00:00")
        tr.save()
        r = Rule()

        r.active = True
        r.action = "confort_temperature"
        r.save()
        r.days.add(d)
        r.ranges.add(tr)

        self.assertEquals(
            r.to_pypelib(),

            "if ( (current_day_of_week = Mon)  ) && ( (1385528400.0 > current_time && current_time < 1385532000.0) )  then do confort_temperature",
            "Not properly trasnsforming to pypelib, got: %s" % r.to_pypelib()
        )

        r.days.add(Day.objects.get(name="Tue"))

        self.assertEquals(
            r.to_pypelib(),
            "if ( (current_day_of_week = Mon) ||  (current_day_of_week = Tue)  ) && ( (1385528400.0 > current_time && current_time < 1385532000.0) )  then do confort_temperature",
            "Not properly trasnsforming to pypelib, got: %s" % r.to_pypelib()
        )

        r.days.add(Day.objects.get(name="Fri"))

        self.assertEquals(
            r.to_pypelib(),
            "if ( (current_day_of_week = Mon) ||  (current_day_of_week = Tue) ||  (current_day_of_week = Fri)  ) && ( (1385528400.0 > current_time && current_time < 1385532000.0) )  then do confort_temperature",
            "Not properly trasnsforming to pypelib, got: %s" % r.to_pypelib()
        )

        r.days.all().delete()

        self.assertEquals(
            r.to_pypelib(),
            "if ( (1385528400.0 > current_time && current_time < 1385532000.0) )  then do confort_temperature",
            "Not properly trasnsforming to pypelib, got: %s" % r.to_pypelib()
        )

        r.ranges.all().delete()

        self.assertEquals(
            r.to_pypelib(),
            "if 1 = 1  then do confort_temperature",
            "Not properly trasnsforming to pypelib, got: %s" % r.to_pypelib()
        )



def main():
    unittest.main()

if __name__ == "__main__":
    unittest.main()
