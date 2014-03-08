# scraps.py



# original methods

def get_vacation(confirmation):
    return Vacation.all().filter("confirm =", confirmation).get()


def generate_time():
    return str(random.choice(range(1,13))) + ":" + str(random.choice(range(7))) + str(random.choice(range(10))) + random.choice(["am", "pm"])

def generate_date(nights=0):
    if nights != 0:
        nights += 1
    flight_date = datetime.datetime.now() + datetime.timedelta(days=(21 + nights))
    return flight_date.strftime("%m/%d/%y")

def generate_layover():
    return random.choice(['Seattle, WA', 'Dallas, TX', 'Portland, OR', 'Los Angeles, CA', 'St. Louis, MO', 'Cedar Rapids, IA', 'Fargo, ND', 'New Orleans, LA', 'Cleveland, OH'])

def make_flights(confirmation):
    vacation = get_vacation(confirmation)
    layover_dest = generate_layover()

    departing = {'name': 'Departing', 'depart': vacation.depart, 'arrive': layover_dest, 'date': generate_date()}
    returning = {'name': 'Arriving', 'depart': vacation.arrive, 'arrive': vacation.depart, 'date': generate_date(vacation.nights)}
    layover = {'name': 'Layover', 'depart': layover_dest, 'arrive': vacation.arrive, 'date': generate_date()}
    flights_list = [departing, layover, returning]

    for flight in flights_list:
        flight['time'] = generate_time()

    return flights_list















class FlightReservationHandler(Handler):
    def get(self):
        confirmation = self.request.get('confirmation')
        vac = get_vacation(confirmation)
        self.render("flight_booking.html", arrive=vac.arrive, nights=vac.nights, price="{0:.2f}".format(vac.price), confirm=vac.confirm)

    def post(self):
        confirmation = self.request.get('confirmation')
        first = self.request.get("first-name")
        last = self.request.get("last-name")
        vac = get_vacation(confirmation)

        if first and last:
            name = "%s %s" % (first, last)
            vac.name = name
            vac.put()
            self.render("thank-you.html", first=first, confirmation=confirmation)
        else:
            error="Sorry, we need both a first and last name!"
            self.render("flight_booking.html", arrive=vac.arrive, nights=vac.nights, price="{0:.2f}".format(vac.price), confirm=vac.confirm, error=error)




class BookHandler(Handler):
    def post(self):
        destination = self.request.get('destination')
        totalPrice = float(self.request.get('totalPrice'))
        nights = int(self.request.get('nights'))

        confirmation = ''.join(random.choice(string.hexdigits) for x in xrange(6))
        while get_vacation(confirmation):
            confirmation = ''.join(random.choice(string.hexdigits) for x in xrange(6))

        new_vacation = Vacation(confirm=confirmation, arrive=destination, price=totalPrice, nights=nights)
        new_vacation.put()

        link = "/reservation?confirmation=" + confirmation
        self.write(json.dumps({'destination': destination, 'totalPrice': totalPrice, 'nights': nights, 'confirmation': confirmation, 'link': link}))





















class DestinationHandler(Handler):
    def get(self):
      dest = self.request.get("dest")
      if dest:
        destinations = {"rome": "Rome, Italy",
                        "rio": "Rio De Janiero, Brazil",
                        "paris": "Paris, France",
                        "london": "London, England",
                        "tokyo": "Tokyo, Japan",
                        "barcelona": "Barcelona, Spain"}

        self.render("destination.html", destination=destinations[dest])
      else:
        self.render('destination.html')

    def post(self):
      first = self.request.get("first")
      last = self.request.get("last")
      depart = self.request.get("depart")
      arrive = self.request.get("arrive")
      num_people = self.request.get("num_people")
      date = self.request.get("date")
      nights = self.request.get("nights")

      if first and last and depart and arrive and num_people:
        name = first + " " + last
        tours = {"london": datetime.date.today(),
        "tokyo": datetime.date.today(),
        "barcelona": datetime.date.today()}
        new_vacation = Vacation(confirm=generate_confirmation, depart=deprat, arrive=arrive, date=date, nights, num_people, price=price, name=name)

      self.render("flights.html")






class TourHandler(Handler):
    def get(self):
      dest = self.request.get("dest")
      if dest:
        destinations = {"rome": "Rome, Italy",
                        "rio": "Rio De Janiero, Brazil",
                        "paris": "Paris, France",
                        "london": "London, England",
                        "tokyo": "Tokyo, Japan",
                        "barcelona": "Barcelona, Spain"}
        self.render('tour.html', destination=destinations[dest], dest=dest)
      else:
        self.render('tour.html')

    def post(self):
        first = self.request.get("first")
        last = self.request.get("last")
        depart = self.request.get("depart")
        arrive = self.request.get("arrive")
        num_people = self.request.get("num_people")

        if first and last and depart and arrive and num_people:
          name = first + " " + last
          tours = {"london": datetime.date.today(),
          "tokyo": datetime.date.today(),
          "barcelona": datetime.date.today()}
          new_vacation = Vacation(confirm=generate_confirmation, depart=deprat, arrive=arrive, date=date, nights, num_people, price=price, name=name)

        self.render("flights.html")






















first = self.request.get("first")
last = self.request.get("last")
depart = self.request.get("depart")
arrive = self.request.get("arrive")
num_people = self.request.get("num_people")
dest = self.request.get("dest")




class Vacation(db.Model):
    confirm = db.StringProperty(required=True, indexed=True)
    depart = db.StringProperty(required=True, default="San Francisco, CA")
    arrive = db.StringProperty(required=True, indexed=True)
    date = db.DateProperty(required=True)
    nights = db.IntegerProperty(required=True, default=7)
    num_people = db.IntegerProperty(required=True, default=2)
    price = db.FloatProperty(required=True)
    name = db.StringProperty(required=False)


class Flight(db.Model):
  # parent = vacation
  name = db.StringProperty(required=True, choices=["outgoing", "returning", "layover"])
  depart = db.StringProperty(required=True, default="San Francisco, CA")
  arrive = db.StringProperty(required=True)
  date = db.DateProperty(required=True)
  time = db.TimeProperty(require=True)
  flight_number = db.StringProperty(required=True, indexed=True)
  confirmation = db.StringProperty(required=True, indexed=True)
  # confirmation from vacation


# vacation methods

def get_vacation(confirmation):
    return Vacation.all().filter("confirm =", confirmation).get()

def generate_confirmation():
    confirmation = ''.join(random.choice(string.hexdigits) for x in xrange(6))
    while get_vacation(confirmation):
        confirmation = ''.join(random.choice(string.hexdigits) for x in xrange(6))
    return confirmation


# flight methods

def get_flight(flight_number):
    return Flight.all().filter("flight_number =", flight_number).get()

def generate_flight_number():
    flight_number = ''.join(random.choice(string.letters) for x in xrange(2)) + ''.join(random.choice(string.numbers) for x in xrange(6))
    while get_flight(flight_number):
        flight_number = ''.join(random.choice(string.letters) for x in xrange(2)) + ''.join(random.choice(string.numbers) for x in xrange(6))
    return flight_number

def random_time(after_time=False):
    if after_time:
      minutes = random.choice(range(120,720))
      dt = datetime.combine(datetime.date.today(), after_time) + datetime.timedelta(minutes=minutes)
      return dt.time()
    else:
      return datetime.time(random.choice(range(0,24)), random.choice(range(60)), random.choice(range(60)))

def return_date(date, nights=0):
    return date + date.timedelta(days=nights)

def generate_layover():
    return random.choice(['Seattle, WA', 'Dallas, TX', 'Portland, OR', 'Los Angeles, CA', 'St. Louis, MO', 'Cedar Rapids, IA', 'Fargo, ND', 'New Orleans, LA', 'Cleveland, OH'])




# original:

def random_time():
    return str(random.choice(range(1,13))) + ":" + str(random.choice(range(7))) + str(random.choice(range(10))) + random.choice(["am", "pm"])

def generate_date(nights=0):
    if nights != 0:
        nights += 1
    flight_date = datetime.datetime.now() + datetime.timedelta(days=(21 + nights))
    return flight_date.strftime("%m/%d/%y")

def generate_layover():
    return random.choice(['Seattle, WA', 'Dallas, TX', 'Portland, OR', 'Los Angeles, CA', 'St. Louis, MO', 'Cedar Rapids, IA', 'Fargo, ND', 'New Orleans, LA', 'Cleveland, OH'])

def generate_flights(confirmation):
    vacation = get_vacation(confirmation)
    layover_dest = generate_layover()

    departing = {'name': 'Departing', 'depart': vacation.depart, 'arrive': layover_dest, 'date': generate_date()}
    returning = {'name': 'Arriving', 'depart': vacation.arrive, 'arrive': vacation.depart, 'date': generate_date(vacation.nights)}
    layover = {'name': 'Layover', 'depart': layover_dest, 'arrive': vacation.arrive, 'date': generate_date()}
    flights_list = [departing, layover, returning]

    for flight in flights_list:
        flight['time'] = generate_time()

    return flights_list
