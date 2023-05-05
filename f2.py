'''
Created on May 1, 2023

@author: yanyo
'''
class Dog:
    # Class property
    species = 'Canis familiaris'

    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.breed = None
        self.color = None

    def set_breed(self, breed):
        self.breed = breed

    def set_color(self, color):
        self.color = color

    def bark(self):
        print(f"{self.name} says woof!")

    # Getter method for the species property
    @classmethod
    def get_species(self):
        return self.species

    # Setter method for the species property
    @classmethod
    def set_species(self, species):
        self.species = species

    # Getter method for the age property
    @property
    def age_in_human_years(self):
        return self.age * 7

    # Setter method for the age property
    @age_in_human_years.setter
    def age_in_human_years(self, age):
        self.age = age // 7

# Create an object of the class Dog
my_dog = Dog("Fido", 3)

# Set the breed and color using the access functions
my_dog.set_breed("Labrador Retriever")
my_dog.set_color("Golden")

# Access the attributes of the object
print(my_dog.name)              # Output: Fido
print(my_dog.age)               # Output: 3
print(my_dog.breed)             # Output: Labrador Retriever
print(my_dog.color)             # Output: Golden
print(my_dog.age_in_human_years) # Output: 21

# Call a method of the object
my_dog.bark()                   # Output: Fido says woof!

# Access the class property
print(Dog.get_species())         # Output: Canis familiaris

# Set the class property
Dog.set_species('Canis lupus')
print(Dog.get_species())         # Output: Canis lupus

# Modify the age property using the setter method
#my_dog.age_in_human_years = 35
my_dog.age_in_human_years= 35
print(my_dog.age)               # Output: 5