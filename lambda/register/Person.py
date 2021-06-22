from logging import lastResort


class Person:

    def __init__(self, firstname, lastname, amount):
        self.firstname = firstname
        self.lastname = lastname
        self.amount = amount        

    def presentation(self):
      print("Je m\'appelle {} {}".format(self.firstname,self.lastname))

    def getAmount(self):
        return self.amount

    def getFistname(self):
      return self.firstname
    
    def getLastname(self):
      return self.lastname

    def getUid(self):
      return self.uid

