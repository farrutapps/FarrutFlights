import json

class request:
    def __init__(self, slices, sale_country, max_price="", passengers = 1, num_responses = 5):
        self.num_responses = num_responses
        self.slices = slices
        self.sale_country = sale_country
        self.max_price = max_price
        self.passengers = passengers

    @classmethod
    def from_dict(cls, dict_):
        slices = []

        for item in dict_['slice']:
            slices.append(slice.from_dict(item))
        
        return cls(slices, dict_['saleCountry'],dict_['maxPrice'],dict_['passengers']['adultCount'],dict_['solutions'])
    

    def to_dict(self):
        slices_dict = []
        for my_slice in self.slices:
            slices_dict.append(my_slice.to_dict())
            
        result = {
          "request" : {
            "passengers": {
            "kind": "qpxexpress#passengerCounts",
            "adultCount": self.passengers
            },
            "slice": slices_dict,
            "maxPrice": self.max_price,
            "saleCountry": self.sale_country,
            "solutions": self.num_responses
          }
        }
        return result
        
    def to_json(self):
        return json.dumps(self.to_dict())    
        

class slice:
    def __init__(self,origin, destination, date, min_time = "", max_time = ""):
        self.origin = origin
        self.destination = destination
        self.date = date
        self.min_time = min_time
        self.max_time = max_time
        self.to_json()
      
    @classmethod
    def from_dict(cls,dict_):
        return cls(dict_['origin'],dict_['destination'],dict_['date'],dict_['permittedDepartureTime']['earliestTime'],dict_['permittedDepartureTime']['latestTime'])

    def to_dict(self):
        result = {        
            "kind": "qpxexpress#sliceInput",
            "origin": self.origin,
            "destination": self.destination,
            "date": self.date.to_API(),
            "maxStops": 0,
            "permittedDepartureTime": {
                "kind": "qpxexpress#timeOfDayRange",
                "earliestTime": self.min_time,
              "latestTime": self.max_time
            }
        }
        return result
        
    def to_json(self):
        return json.dumps(self.to_dict())
        
#Represents a date. Used to convert between API style and standard European, point separated style.
class date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_API(cls,date_time):
        date = date_time.split('T')[0]
        splits = date.split('-')
        return cls(splits[2],splits[1], splits[0])

    @classmethod
    def from_std(cls,date):
        splits = date.split('.')
        return cls(splits[0], splits[1], splits[2])
       
    def to_std(self):
        return ".".join((self.day,self.month,self.year))

    def to_API(self):
        return "-".join((self.year,self.month,self.day))
        
