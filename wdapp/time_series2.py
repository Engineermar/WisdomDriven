@@ -0,0 +1,195 @@
from django.db import models
import datetime
 class TimeSeries(models.Model):
    """
    Abstract Base class for aggregating time series.
     Requires a related time_series class.
    """
    @property
    def first(self):
        try:
            return self.time_series.order_by('nodefile__date')[0]
        except:
            pass
     @property
    def canonical(self):
        """
        Returns the canonical node from the time series
        which is determined by the is_canonical boolean if
        it exists, and defaults to the first object in the
        series if it does not.
        
        Raises a MultipleCanonicalError if multiple objects
        have is_canonical = True
         TODO use get instead and standard get execptions.
        """
	try:
            return self.time_series.get(is_canonical=True)
        except ObjectDoesNotExist:
            print "WARNING: %s has no canonical time point." % self.first
        except MultipleObjectsReturned:
            raise self.MultipleCanonicalError
     @property
    def last(self):
        try:
            return self.time_series.order_by('-nodefile__date')[0]
        except:
            pass
     def start_date(self):
        try:
            self.first.date
        except:
            pass
     def end_date(self):
        try:
            return self.last.date
        except:
            pass
     def date_range_qs(self, start_date=None, end_date=None):
        """
        Returns a queryset of state_change objects for given
        date range takes an optional start_date and end_date
        Assumes they are passed as datetime.date objects.
        """
        try:
            qs = self.time_series.all()
            if start_date:
                qs = qs.filter(nodefile__date__gt=start_date)
            if end_date:
                qs = qs.filter(nodefile__date__lt=end_date)
            return qs
        except:
            pass
     def __unicode__(self):
        try:
            return self.canonical
        except:
            return 'id: %d' % self.id
     def MultipleCanonicalError(Exception):
        pass
     class Meta:
        abstract = True
 class TimePoint(models.Model):
 class GenericNodeTimePoint(models.Model):
    is_canonical = models.BooleanField(default=False)
     raw_data = models.CharField(max_length=500)
    nodefile = models.ForeignKey("NodeFile",
                                 related_name="time_series_set")
     name = models.CharField(max_length=200, blank=True)
    sysop = models.ForeignKey("Sysop", blank=True, null=True)
     number = models.PositiveIntegerField()
     coordinates = models.PointField(null=True, blank=True)
    phone_numbers = models.ManyToManyField("PhoneNumber",
         related_name="node_time_points", blank=True, null=True)
    phone_number_text = models.CharField(max_length = 40, blank=True)
     #region information
    # NB: State can be a country or US state or province
    region = models.CharField(max_length=100, blank=True) 
    city = models.CharField(max_length=100, blank=True)
     speeds = models.ManyToManyField("NodeSpeed", blank=True, null=True)
    flags = models.ManyToManyField("NodeFlag", blank=True, null=True)
    flags_text = models.CharField(max_length=1000, blank=True)
     connections = models.ManyToManyField("NodeTimePoint",
            blank=True, null=True)
     objects = models.GeoManager()
     @classmethod
    def is_net(cls):
        return cls is NetTimePoint
     @classmethod
    def is_zone(cls):
        return cls is ZoneTimePoint
     @classmethod
    def is_node(cls):
        return cls is NodeTimePoint
     @property
    def parent(self):
        if self.is_zone():
            return None
        elif self.is_node():
            return self.net
        else:
            if not self.parent_net:
                return self.zone
            else:
                return self.parent_net
     def hours(self):
        """
        Will eventually parse the state_text field to
        calculate the hours active per unit time.
        """
        pass
     @property
    def date(self):
        """
        Returns date from related NodeFile.
        """
        return self.nodefile.date
     @property
    def year(self):
        """
        Returns year from related NodeFile.
        """
        return self.date.year
     @property
    def day(self):
        """
        Returns the day of the related nodefile.
        """
        return self.nodefile.day
     def check_coordinates(self):
        """
        Returns true if the phone number may yield a valid coordinate
        pair.
         FIX
        """
        if self.phone_number:
            if self.zone:
                if self.zone == Zone.objects.get(number=1):
                    return True
                else:
                    return False
            return True
     def has_coordinates(self):
        if self.coordinates: return True
        else: return False
     def __unicode__(self):
        return "%s on day %s, %s" % \
                (self.name, self.day, self.year)
     class Meta:
        ordering = ['nodefile__date', 'number']
 
23  tests.py
@@ -0,0 +1,23 @@
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".
 Replace these with more appropriate tests for your application.
"""
 from django.test import TestCase
 class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)
 __test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.
 >>> 1 + 1 == 2
True
"""}
django time series analysis

This message was moved to the Junk Email folder because you only trust email from senders in your Safe Senders list. It's not spam
Augustine Masikonde <amasikonde@gmail.com>
Wed 12/5/2018, 11:05 PM
https://github.com/eamonnmag/chronoglyph/commit/36502d6cc4dae00d4ef84bfeaa584e17a105cd1c

V/R

Augustine Masikonde
IT Business Analyst
703-953-6700
amasikonde@gmail.com 

In God we trust, everyone else must show Data.