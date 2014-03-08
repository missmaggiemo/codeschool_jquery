#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2

import json
import random
import string
import logging
import hashlib
import datetime
import time

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)
# autoescape escapes html from user text automatically

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))



class Vacation(db.Model):
      confirm = db.StringProperty(required=True, indexed=True)
      depart = db.StringProperty(required=True, default="San Francisco, CA")
      arrive = db.StringProperty(required=True, indexed=True)
      date = db.DateProperty(required=True)
      nights = db.IntegerProperty(required=True, default=7)
      num_people = db.IntegerProperty(required=True, default=2)
      price = db.FloatProperty(required=True)
      name = db.StringProperty(required=True)
      flights = db.StringListProperty()



class Flight(db.Model):
      name = db.StringProperty(required=True, choices=set(["outgoing", "returning", "layover"]))
      depart = db.StringProperty(required=True, default="San Francisco, CA")
      arrive = db.StringProperty(required=True)
      date = db.DateProperty(required=True)
      time = db.TimeProperty(required=True)
      flight_number = db.StringProperty(required=True, indexed=True)
      confirm = db.StringProperty(required=True, indexed=True)
      boarding_pass = db.TextProperty(required=False)
      # parent = vacation
      # confirm from vacation

# global variables

tours = {"london": datetime.date(11,1,1),
        "tokyo": datetime.date(6,1,1),
        "barcelona": datetime.date(5,1,1)}

destinations = {"rome": "Rome, Italy",
                "rio": "Rio De Janiero, Brazil",
                "paris": "Paris, France",
                "london": "London, England",
                "tokyo": "Tokyo, Japan",
                "barcelona": "Barcelona, Spain"}

weather =  {"rome": "70 &deg; F, Sunny",
            "rio": "70 &deg; F, Sunny",
            "paris": "70 &deg; F, Sunny",
            "london": "50 &deg; F, Rainy",
            "tokyo": "70 &deg; F, Sunny",
            "barcelona": "70 &deg; F, Sunny"}

price_per_person =  {"rome": 1200,
          "rio": 1000,
          "paris": 1500,
          "london": 2500,
          "tokyo": 3000,
          "barcelona": 2000}

# utility methods

def log_record(text):
    return logging.error(text.upper())

def sleep(n):
    return time.sleep(abs(float(n)))


# vacation methods

def get_vacation(confirmation):
    return Vacation.all().filter("confirm =", confirmation).get()

def generate_confirmation():
    confirmation = ''.join(random.choice(string.hexdigits.upper()) for x in xrange(6))
    while get_vacation(confirmation):
        confirmation = ''.join(random.choice(string.hexdigits.upper()) for x in xrange(6))
    return confirmation

def generate_new_vacation_and_flights(depart=None, arrive=None, date=None, nights=None, num_people=None, price=None, name=None):
    new_vacation = Vacation(confirm=generate_confirmation(), depart=depart, arrive=arrive, date=date, nights=nights, num_people=num_people, price=price, name=name)
    new_vacation.put()
    sleep(0.5)
    flights = generate_flights(new_vacation.confirm)
    sleep(0.5)

    for flight in flights:
      flight.boarding_pass = generate_ticket_html(flight.flight_number)
      flight.put()

    sleep(0.5)
    return new_vacation




# flight methods

def get_flight(flight_number):
    return Flight.all().filter("flight_number =", flight_number).get()

def generate_flight_number():
    flight_number = ''.join(random.choice(string.letters.upper()) for x in xrange(2)) + ''.join(random.choice(string.digits) for x in xrange(6))
    while get_flight(flight_number):
        flight_number = ''.join(random.choice(string.letters.upper()) for x in xrange(2)) + ''.join(random.choice(string.digits) for x in xrange(6))
    return flight_number

def random_time(after_time=False):
    if after_time:
      minutes = random.choice(range(480,660))
      dt = datetime.datetime.combine(datetime.date.today(), after_time) + datetime.timedelta(minutes=minutes)
      return dt.time()
    else:
      return datetime.time(random.choice(range(0,12)), random.choice(range(60)), random.choice(range(60)))

def return_date(date, nights=7):
    return date + datetime.timedelta(days=nights)

def generate_layover():
    return random.choice(['Seattle, WA', 'Dallas, TX', 'Portland, OR', 'Los Angeles, CA', 'St. Louis, MO', 'Cedar Rapids, IA', 'Fargo, ND', 'New Orleans, LA', 'Cleveland, OH'])


def generate_flights(confirmation):

    vacation = get_vacation(confirmation)
    layover_dest = generate_layover()

    departing = Flight(parent=vacation,
                name="outgoing",
                depart=vacation.depart,
                arrive=layover_dest,
                date=vacation.date,
                time=random_time(),
                flight_number=generate_flight_number(),
                confirm=vacation.confirm)
    departing.put()

    returning = Flight(parent=vacation,
                name="returning",
                depart=vacation.arrive,
                arrive=vacation.depart,
                date=return_date(vacation.date, vacation.nights),
                time=random_time(),
                flight_number=generate_flight_number(),
                confirm=vacation.confirm)
    returning.put()

    layover = Flight(parent=vacation,
                name="layover",
                depart=layover_dest,
                arrive=vacation.arrive,
                date=vacation.date,
                time=random_time(departing.time),
                flight_number=generate_flight_number(),
                confirm=vacation.confirm)
    layover.put()

    vacation.flights = [departing.flight_number, layover.flight_number, returning.flight_number]
    vacation.put()

    return [departing, layover, returning]


def generate_ticket_html(flight_number):
    flight = get_flight(flight_number)
    html = "<div class='ticket'><p><span>Flight Number: %s</span><span>Confirmation Number: %s</span></p><img src='images/jquery_QR.png' alt='QR_Code' /></div>" % (flight.flight_number, flight.confirm)
    return html


def get_flights_from_confirmation(confirmation):
  vacation = get_vacation(confirmation)
  if vacation:
      log_record(str(vacation))
      flights = vacation.flights
      if flights:
          flights = map(get_flight, flights)
          return flights



# class methods

def parse_date(unicode_date):
    date_list = unicode_date.split("-")
    date_list = map(int, date_list)
    return datetime.date(date_list[0], date_list[1], date_list[2])













class HomeHandler(Handler):
    def get(self):
        self.render("home.html")



class FlightsHandler(Handler):
    def get(self):
        confirmation = self.request.get('confirmation')
        flights = get_flights_from_confirmation(confirmation)
        self.render("flights.html", confirmation=confirmation, flights=flights)



class DestinationHandler(Handler):
    def get(self):
      dest = self.request.get("dest")
      if dest:
        self.render("destination.html", destination=destinations[dest], dest=dest, price=price_per_person[dest])
      else:
        self.render('destination.html')

    def post(self):
      dest = self.request.get("arrive")
      first_name = self.request.get("first-name")
      last_name = self.request.get("last-name")
      depart = self.request.get("depart")
      arrive = destinations[dest]
      num_people = self.request.get("num-people")
      date = self.request.get("date")
      nights = self.request.get("nights")
      price = self.request.get("price")

      for item in [dest, first_name, last_name, depart, arrive, num_people, str(parse_date(date)), nights, price]:
          log_record(item)

      if dest and first_name and last_name and depart and arrive and num_people and date and nights and price:
          name = first_name + " " + last_name
          date = parse_date(date)
          nights = int(nights)
          price = float(price)
          num_people = int(num_people)

          vacation = generate_new_vacation_and_flights(depart=depart, arrive=arrive, date=date, nights=nights, num_people=num_people, price=price, name=name)

          self.redirect("/flights?confirmation="+vacation.confirm)
      else:
          self.render('tour.html', destination=destinations[dest], dest=dest, error="One of the boxes isn't filled in!")




class TourHandler(Handler):
    def get(self):
      dest = self.request.get("dest")
      if dest:
        self.render('tour.html', destination=destinations[dest], dest=dest, price=price_per_person[dest])
      else:
        self.render('tour.html')

    def post(self):
        dest = self.request.get("arrive")
        log_record(dest)
        first_name = self.request.get("first-name")
        last_name = self.request.get("last-name")
        depart = self.request.get("depart")
        arrive = destinations[dest]
        num_people = self.request.get("num_people")
        price = self.request.get("price")

        for item in [dest, first_name, last_name, depart, arrive, num_people, price]:
          log_record(item)

        if first_name and last_name and depart and arrive and num_people:
          name = first_name + " " + last_name
          date = tours[dest]
          nights = 7
          price = float(price)
          num_people = int(num_people)

          vacation = generate_new_vacation_and_flights(depart=depart, arrive=arrive, date=date, nights=nights, num_people=num_people, price=price, name=name)

          self.redirect("/flights?confirmation="+vacation.confirm)

        else:
            self.render('tour.html', destination=destinations[dest], dest=dest, error="One of the boxes isn't filled in!")




class ConfirmationHandler(Handler):
    def get(self):
      self.render("check_confirm.html")




class CheckFlightsHandler(Handler):
    def post(self):
      confirmation = self.request.get('confirmation')
      flights = get_flights_from_confirmation(confirmation)
      if flights:
          self.render("check_flights.html", confirmation=confirmation, flights=flights)
      else:
          self.render("check_flights.html", error=True, confirmation=confirmation)




app = webapp2.WSGIApplication([
    ('/', HomeHandler),
    ('/flights', FlightsHandler),
    ('/destination', DestinationHandler),
    ('/tour', TourHandler),
    ('/confirmation', ConfirmationHandler),
    ('/check-flights', CheckFlightsHandler)
], debug=True)
