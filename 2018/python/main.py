# Imports
import matplotlib.pyplot as plt
import matplotlib as mpl
import pylab
import numpy as np

'''
Problem description:

'''


# Initial Data
def read_general_data(file_name):
    # noinspection SpellCheckingInspection
    '''
         3 4 2 3 2 10  3 rows, 4 columns, 2 vehicles, 3 rides, 2 bonus and 10 stepsise
         0 0 1 3 2 9 ride from [0,0] to [1,3], earliest stat 2, latest finish 9
        ...
         '''
    lines = [line.rstrip('\n') for line in open(file_name)]

    while True:
        for first_line in lines:
            first_line = first_line.split()
            r = first_line[0]  # number of rows of the grid
            c = first_line[1]  # number of columns of the grid
            f = first_line[2]  # number of vehicles in the fleet
            n = first_line[3]  # number of rides
            b = first_line[4]  # per-ride bonus fro starting the ride on time
            t = first_line[5]  # number of stems in the simulation

            return r, c, f, n, b, t


def read_ride_data(file_name):
    '''
     3 4 2 3 2 10  3 rows, 4 columns, 2 vehicles, 3 rides, 2 bonus and 10 stepsize
     0 0 1 3 2 9 ride from [0,0] to [1,3], earliest stat 2, latest finish 9
    ...
     '''
    lines = [line.rstrip('\n') for line in open(file_name)]

    ride_start_x_coordinate_array = []
    ride_start_y_coordinate_array = []
    ride_end_x_coordinate_array = []
    ride_end_y_coordinate_array = []

    ride_earliest_start_array = []
    ride_latest_finish_array = []

    i = 0
    for line in lines:
        if i < 1:
            # Skip the first line
            i += 1
        else:
            line = line.split()

            start_x_coordinate = [line[0]]
            start_y_coordinate = [line[1]]
            end_x_coordinate = [line[2]]
            end_y_coordinate = [line[3]]

            earliest_start_time = [line[4]]
            latest_finish_time = [line[5]]

            ride_start_x_coordinate_array.extend(start_x_coordinate)
            ride_start_y_coordinate_array.extend(start_y_coordinate)
            ride_end_x_coordinate_array.extend(end_x_coordinate)
            ride_end_y_coordinate_array.extend(end_y_coordinate)

            ride_earliest_start_array.extend(earliest_start_time)
            ride_latest_finish_array.extend(latest_finish_time)

    return ride_start_x_coordinate_array, ride_start_y_coordinate_array, ride_end_x_coordinate_array, ride_end_y_coordinate_array, ride_earliest_start_array, ride_latest_finish_array


# r = number of rows of the grid
# c =  number of columns of the grid
# f =  number of vehicles in the fleet
# n =  number of rides
# b =  per-ride bonus fro starting the ride on time
# t =  number of stems in the simulation

r, c, f, n, b, t = read_general_data('data.txt')

ride_start_x_coordinate_array, ride_start_y_coordinate_array, ride_end_x_coordinate_array, ride_end_y_coordinate_array, ride_earliest_start_array, ride_latest_finish_array = read_ride_data(
    'data.txt')

start_x = np.array(ride_start_x_coordinate_array)  # x-coordinate
start_y = np.array(ride_start_y_coordinate_array)  # y-coordinate

end_x = np.array(ride_end_x_coordinate_array)  # x-coordinate
end_y = np.array(ride_end_y_coordinate_array)  # y-coordinate


# Show ride start and end points

def plot_start_end():
    plt.scatter(start_x, start_y, label='start')  # blue tot
    plt.scatter(end_x, end_y, label='end')  # orange tot

    for i in range(0, len(start_x)):
        plt.plot([start_x[i], end_x[i]], [start_y[i], end_y[i]])
        plt.show()


def revenue_from_ride(my_x, my_y, passenger, current_time, ride_bonus):
    # Ride has expired
    if current_time > passenger.latest_finish:
        return 0

    # The passanger dose not exist
    if passenger is None:
        return 0

    time_from_me_to_passenger = abs(my_x - passenger.start_x) + abs(my_y - passenger.start_y)
    time_from_passenger_to_final = abs(passenger.start_x - passenger.end_x) + abs(passenger.start_y - passenger.end_y)

    travel_time = time_from_me_to_passenger + time_from_passenger_to_final

    # Can I handle the ride

    if (current_time + travel_time) > passenger.latest_finish or (current_time + travel_time) < passenger.earliest_start:
        return 0

    # base revenue
    distance_revenue = time_from_passenger_to_final

    # bonus revenue
    bonus_revenue = 0
    if (current_time + time_from_me_to_passenger) == passenger.earliest_start:
        bonus_revenue += int(ride_bonus)

    return distance_revenue + bonus_revenue


# Generate Classes
class Passenger:
    def __init__(self, id, start_x, start_y, end_x, end_y, earliest_start, latest_finish):
        self.id = int(id)
        self.start_x = int(start_x)
        self.start_y = int(start_y)
        self.end_x = int(end_x)
        self.end_y = int(end_y)
        self.earliest_start = int(earliest_start)
        self.latest_finish = int(latest_finish)


class Car:
    def __init__(self, id, x_coordinate, y_coordinate):
        self.id = int(id)
        self.x_coordinate = int(x_coordinate)
        self.y_coordinate = int(y_coordinate)
        self.time_available = 0

    def make_a_ride(self, current_time, passenger, ride_bonus):
        time_from_me_to_passenger = abs(self.x_coordinate - passenger.start_x) + abs(
            self.y_coordinate - passenger.start_y)
        time_from_passenger_to_end = abs(passenger.start_x - passenger.end_x) + abs(passenger.start_y - passenger.end_y)
        travel_time = time_from_me_to_passenger + time_from_passenger_to_end

        # Would I arrive at the start too early or finish too late
        if (current_time + travel_time) < passenger.earliest_start or (
                current_time + travel_time) > passenger.latest_finish:
            return 0

        self.time_available = self.time_available + travel_time

        self.x_coordinate = passenger.end_x
        self.y_coordinate = passenger.end_y

        # Add ride info to the file
        # TODO
        report_ride(passenger)

        # Return revenue from ride
        return revenue_from_ride(self.x_coordinate, self.y_coordinate, passenger, current_time, ride_bonus)

    def move_closer(self, current_time, passenger_array):
        # Find the nearest passenger
        dictionary_distance_passenger = {}

        if len(passenger_array) == 0:
            return False

        for passenger in passenger_array:
            # Distance
            distance_to_passenger = abs(self.x_coordinate - passenger.start_x) + abs(self.y_coordinate - passenger.start_y)

            # Add passenger info to the dictionary
            if distance_to_passenger in dictionary_distance_passenger:
                current_passengers = dictionary_distance_passenger[distance_to_passenger]
                current_passengers.append(passenger)

                dictionary_distance_passenger[distance_to_passenger] = current_passengers
            else:
                current_passengers = [passenger]

                dictionary_distance_passenger[distance_to_passenger] = current_passengers

        # Find the nearest passenger

        smallest_distance_key = min(dictionary_distance_passenger.keys())
        smallest_distance_passengers = dictionary_distance_passenger[smallest_distance_key]

        nearest_passenger = smallest_distance_passengers[0]

        # Dose the car have the same x-coordinate as the nearest passenger?

        if self.x_coordinate != nearest_passenger.start_x:
            # Move x by +/- 1
            x_coordinate_move = 0
            if (nearest_passenger.start_x - self.x_coordinate) > 0:
                x_coordinate_move += 1
            else:
                x_coordinate_move -= 1

            self.x_coordinate = self.x_coordinate + x_coordinate_move

            self.time_available = current_time + 1

        elif self.y_coordinate != nearest_passenger.start_y:
            # Move y by +/- 1
            y_coordinate_move = 0
            if (nearest_passenger.start_y - self.y_coordinate) > 0:
                y_coordinate_move += 1
            else:
                y_coordinate_move -= 1

            self.y_coordinate = self.y_coordinate + y_coordinate_move

            self.time_available = current_time + 1

        return True

        # TODO Are there multiple passengers who are at same distance?

    def is_available(self, current_time):
        return current_time >= self.time_available


def report_ride(passenger):
    '''
    1 0     this vehicle is assigned 1 ride: [0]
    2 2 1   this vehicle is assigned 2 rides: [2, 1]
    '''

    #TODO
    # with open("results/testresults.txt", "a") as myfile:
    # Find a line that contains the id of this car
    # myfile.write("\n")
    return None

def generate_passengers(start_x_array, start_y_array, end_x_array, end_y_array, earliest_start_array,
                        latest_finish_array):
    passenger_array = []

    i = 0
    while i < len(start_x_array):
        start_x = start_x_array[i]
        start_y = start_y_array[i]

        end_x = end_x_array[i]
        end_y = end_y_array[i]

        earliest_start = earliest_start_array[i]
        latest_finish = latest_finish_array[i]

        # Using i as ID
        passenger = [Passenger(i, start_x, start_y, end_x, end_y, earliest_start, latest_finish)]
        passenger_array.extend(passenger)

        i += 1
    return passenger_array


def generate_cars(n):
    car_array = []
    i = 0
    while i < int(n):
        # i as id
        car = [Car(i, 0, 0)]
        i += 1
        car_array.extend(car)

    return car_array


def filter_passengers(passengers, current_time):
    for passenger in passengers:
        if passenger.latest_finish < current_time:
            passengers.remove(passenger)

    return passengers

def find_time_increment(current_time,car_array):
    #1. Are there any cars available
    #TODO: implement lamda
    for car in car_array:
        if car.is_available(current_time):
            return 1

    #2. Find the time that the earliest car is available
    time_available = float('inf')
    for car in car_array:
        if car.time_available < time_available:
            time_available = car.time_available

    #Finding the right increment
    return time_available-current_time
         

# Main logic
def taxify(method_name, car_array, passenger_array, max_time, ride_bonus):
    revenue = 0

    number_of_passengers = len(passenger_array)
    number_of_rides = 0

    i = 0
    while i < int(max_time) and len(passenger_array) > 0:
       # time_till_expiery = int(max_time)-i
       # print (str(time_till_expiery))

        # Remove passengers who's latest finish time is already over
        passenger_array = filter_passengers(passenger_array, i)

        if len(passenger_array) == 0:
            break

        #TODO
        # Find the best car
        '''
         registered_car_methods = {
            "biggest_profit": best_car_biggest_profit(car_array, passenger_array, i, ride_bonus)
        }
         ranked_cars = registered_car_methods[method_name]

        '''
        ranked_cars = car_array       
       
        for car in ranked_cars:
            if car.is_available(i):
                # Find the best match for a given 
                registered_passanger_methods = {
                    "biggest_profit": best_passenger_biggest_profit_match(passenger_array, car, i, ride_bonus),
                }

                best_passengers = registered_passanger_methods[method_name]

                if best_passengers is not None:
                    old_revenue = revenue
                    revenue += car.make_a_ride(i, best_passengers[0], ride_bonus)

                    if (revenue - old_revenue) > 0:
                        number_of_rides += 1
                        passenger_array.remove(best_passengers[0])

                # Move the car closer to the nearest passenger
                # TODO booking a passenger
                else:
                    car.move_closer(i, passenger_array)

          
            i += find_time_increment(i,car_array)

    print('Number of original passangers ' + str(number_of_passengers))
    print('Number of rides ' + str(number_of_rides))

    return revenue


def best_passenger_biggest_profit_match(passenger_array, car, current_time, bonus):
    if len(passenger_array) == 0:
        return None

    dictionary_profit_passenger = {}

    #1. Find the profit genrated by evru single passanger
    for passenger in passenger_array:
        # Revenue
        revenue_from_passenger = revenue_from_ride(car.x_coordinate, car.y_coordinate, passenger, current_time, bonus)
        # Expense
        distance_to_passenger = abs(car.x_coordinate - passenger.start_x) + abs(car.y_coordinate - passenger.start_y)
        # Profit
        profit = revenue_from_passenger - distance_to_passenger

        # Add passenger info to the dictionary
        if profit in dictionary_profit_passenger:
            current_passengers = dictionary_profit_passenger[profit]
            current_passengers.append(passenger)
            dictionary_profit_passenger[profit] = current_passengers
        else:
            current_passengers = [passenger]
            dictionary_profit_passenger[profit] = current_passengers

    # Find passengers with the highest profit
    biggest_profit_key = max(dictionary_profit_passenger.keys())
    biggest_profit_passengers = dictionary_profit_passenger[biggest_profit_key]

    #Is there only one GREAT passenger
    if len(biggest_profit_passengers) == 1:
        return dictionary_profit_passenger[biggest_profit_key]
    else:
        #Find a passenger who is nearest to us
        dictionary_distance_passenger = {}

        for passenger in dictionary_profit_passenger[biggest_profit_key]:
            # Expense
            distance_to_passenger = abs(car.x_coordinate - passenger.start_x) + abs(
                car.y_coordinate - passenger.start_y)

            # Add passenger info to the dictionary
            if distance_to_passenger in dictionary_distance_passenger:
                current_passengers = dictionary_distance_passenger[distance_to_passenger]
                current_passengers.append(passenger)

                dictionary_distance_passenger[distance_to_passenger] = current_passengers
            else:
                current_passengers = [passenger]

                dictionary_distance_passenger[distance_to_passenger] = current_passengers

        smallest_distance_key = min(dictionary_distance_passenger.keys())
        shortest_distance_passangers = dictionary_distance_passenger[smallest_distance_key]

        # Is there only one passanger who's nearest to us?
        if len(shortest_distance_passangers) == 1:
            return dictionary_distance_passenger[smallest_distance_key]

        print ('HI')
        # todo- improve
        return dictionary_distance_passenger[smallest_distance_key]



# Used to evaluate the effectiveness of the algorithm
def max_revenue(passengers, ride_bonus):
    revenue = 0

    for passenger in passengers:
        distance_revenue = abs(passenger.start_x - passenger.end_x) + abs(passenger.start_y - passenger.end_y)
        revenue += distance_revenue + int(ride_bonus)

    return revenue


# Initial values
passengers = generate_passengers(ride_start_x_coordinate_array, ride_start_y_coordinate_array,
                                 ride_end_x_coordinate_array,
                                 ride_end_y_coordinate_array, ride_earliest_start_array, ride_latest_finish_array)
passengers2 = generate_passengers(ride_start_x_coordinate_array, ride_start_y_coordinate_array,
                                  ride_end_x_coordinate_array,
                                  ride_end_y_coordinate_array, ride_earliest_start_array, ride_latest_finish_array)

cars = generate_cars(f)

# Innate the simulation
max_revenue = float(max_revenue(passengers, b))

print("Biggest profit method")
biggest_profit_revenue = float(taxify("biggest_profit", cars, passengers, t, b))
efficiency_biggest_profit = biggest_profit_revenue / max_revenue
print("Methods efficiency(%): " + str(100 * efficiency_biggest_profit))

# TODO
# Investicate whter the submitted files are correct (no double rides and no passanger sharing)