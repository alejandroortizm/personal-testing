# Python basics test script

# 1. Variables & data types
name = "Alejandro"
age = 30
is_engineer = True
print(f"Name: {name}, Age: {age}, Engineer: {is_engineer}")

# 2. Lists
fruits = ["apple", "banana", "cherry"]
fruits.append("mango")
print(f"Fruits: {fruits}")

# 3. Dictionary
person = {"name": "Alejandro", "team": "Uber", "language": "Python"}
for key, value in person.items():
    print(f"  {key}: {value}")

# 4. Function
def fibonacci(n):
    sequence = [0, 1]
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    return sequence[:n]

print(f"Fibonacci (10): {fibonacci(10)}")

# 5. List comprehension
squares = [x**2 for x in range(1, 6)]
print(f"Squares: {squares}")

# 6. Simple class
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}!"

dog = Animal("Dog", "Woof")
cat = Animal("Cat", "Meow")
print(dog.speak())
print(cat.speak())
