from typing import List, Union


class Person:
    """
    Represents a person with a name, surname, and age.
    Tracks the number of vehicles owned.
    """
    def __init__(self, name: str, surname: str, age: int) -> None:
        self.name = name
        self.surname = surname
        self.age = age
        self._vehicle_count: int = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return (
            self.name == other.name and
            self.surname == other.surname and
            self.age == other.age
        )

    @property
    def vehicle_count(self) -> int:
        """Returns the count of vehicles owned by the person."""
        return self._vehicle_count

    def increment_vehicle_count(self) -> None:
        """Increments the count of vehicles owned by the person."""
        self._vehicle_count += 1

    def decrement_vehicle_count(self) -> None:
        """Decrements the count of vehicles owned by the person."""
        if self._vehicle_count > 0:
            self._vehicle_count -= 1


class Vehicle:
    """
    Represents a vehicle with a registration plate, creation date, and owner.
    """
    def __init__(self, registration_plate: str, creation_date: str, owner: Person) -> None:
        self.registration_plate = registration_plate
        self.creation_date = creation_date
        self.owner = owner

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vehicle):
            return NotImplemented
        return self.registration_plate == other.registration_plate


class Register:
    """
    Maintains a register of vehicles and their owners.
    Allows operations to add, update, and delete vehicles, as well as list vehicles and owners.
    """
    def __init__(self) -> None:
        self.vehicles: List[Vehicle] = []
        self.owners: List[Person] = []

    def insert_vehicle(self, vehicle: Vehicle) -> int:
        """Adds a vehicle to the register. Returns 1 if successful, 0 if already exists."""
        if vehicle in self.vehicles:
            return 0

        self.vehicles.append(vehicle)

        if vehicle.owner not in self.owners:
            self.owners.append(vehicle.owner)

        vehicle.owner.increment_vehicle_count()
        return 1

    def update_vehicle_owner(self, registration_plate: str, new_owner: Person) -> int:
        """Updates the owner of a vehicle. Returns 1 if successful, 0 otherwise."""
        vehicle = self._find_vehicle_by_plate(registration_plate)
        if not vehicle or vehicle.owner == new_owner:
            return 0

        old_owner = vehicle.owner
        old_owner.decrement_vehicle_count()

        if old_owner.vehicle_count == 0:
            self.owners.remove(old_owner)

        vehicle.owner = new_owner

        if new_owner not in self.owners:
            self.owners.append(new_owner)

        new_owner.increment_vehicle_count()
        return 1

    def delete_vehicle(self, registration_plate: str) -> int:
        """Removes a vehicle from the register. Returns 1 if successful, 0 if not found."""
        vehicle = self._find_vehicle_by_plate(registration_plate)
        if not vehicle:
            return 0

        owner = vehicle.owner
        self.vehicles.remove(vehicle)
        owner.decrement_vehicle_count()

        if owner.vehicle_count == 0:
            self.owners.remove(owner)

        return 1

    def list_vehicles(self) -> List[Vehicle]:
        """Returns a list of all vehicles in the register."""
        return self.vehicles

    def list_owners(self) -> List[Person]:
        """Returns a list of all owners in the register."""
        return self.owners

    def list_vehicle_by_owner(self, owner: Person) -> List[Vehicle]:
        """Returns a list of vehicles owned by a specific person."""
        return [vehicle for vehicle in self.vehicles if vehicle.owner == owner]

    def _find_vehicle_by_plate(self, registration_plate: str) -> Union[Vehicle, None]:
        """Finds a vehicle by its registration plate. Returns None if not found."""
        for vehicle in self.vehicles:
            if vehicle.registration_plate == registration_plate:
                return vehicle
        return None

# Testing code
register = Register()

person1 = Person("John", "Doe", 20)
person2 = Person("Alice", "Doe", 22)

car1 = Vehicle("abc0", "20221122", person1)
car2 = Vehicle("abc1", "20221123", person1)
car3 = Vehicle("abc0", "20221122", person1)
car4 = Vehicle("xyz", "20221124", person2)

# test insertion
assert register.insert_vehicle(car1) == 1
assert register.insert_vehicle(car2) == 1
assert register.insert_vehicle(car3) == 0
assert register.insert_vehicle(car4) == 1
assert register.list_vehicles() == [
    Vehicle("abc0", "20221122", person1),
    Vehicle("abc1", "20221123", person1),
    Vehicle("xyz", "20221124", person2)
]
assert register.list_owners() == [
    Person("John", "Doe", 20),
    Person("Alice", "Doe", 22)
] and register.list_owners()[0].vehicle_count == 2 and register.list_owners()[1].vehicle_count == 1

# test update
assert register.update_vehicle_owner("abc1", person1) == 0
assert register.update_vehicle_owner("not in register", person1) == 0
assert register.update_vehicle_owner("abc1", person2) == 1
assert register.list_vehicles() == [
    Vehicle("abc0", "20221122", person1),
    Vehicle("abc1", "20221123", person2),
    Vehicle("xyz", "20221124", person2)
]
assert register.list_owners() == [
    Person("John", "Doe", 20),
    Person("Alice", "Doe", 22)
] and register.list_owners()[0].vehicle_count == 1 and register.list_owners()[1].vehicle_count == 2
assert register.update_vehicle_owner("abc0", person2) == 1
assert register.list_vehicles() == [
    Vehicle("abc0", "20221122", person2),
    Vehicle("abc1", "20221123", person2),
    Vehicle("xyz", "20221124", person2)
]
assert register.list_owners() == [
    Person("Alice", "Doe", 22)
] and register.list_owners()[0].vehicle_count == 3

# test delete
assert register.delete_vehicle("not in register") == 0
assert register.delete_vehicle("abc0") == 1
assert register.delete_vehicle("abc1") == 1
assert register.delete_vehicle("xyz") == 1
assert register.list_vehicles() == []
assert register.list_owners() == []

# test lists
car1 = Vehicle("abc0", "20221122", person1)
car2 = Vehicle("abc1", "20221123", person1)
car3 = Vehicle("abc0", "20221122", person1)
car4 = Vehicle("xyz", "20221124", person2)

register.insert_vehicle(car1)
register.insert_vehicle(car2)
register.insert_vehicle(car3)
register.insert_vehicle(car4)

assert register.list_vehicles() == [
    Vehicle("abc0", "20221122", person1),
    Vehicle("abc1", "20221123", person1),
    Vehicle("xyz", "20221124", person2)
]
assert register.list_owners() == [
    Person("John", "Doe", 20),
    Person("Alice", "Doe", 22)
]
assert register.list_vehicle_by_owner(person1) == [
    Vehicle("abc0", "20221122", person1),
    Vehicle("abc1", "20221123", person1)
]
