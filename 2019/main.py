def read_general_data (fname):
    '''
    Return:
    R-rows
    C-columns
    L-min number of each ingritient
    H-max slize size
    '''
    with open(fname) as f:
        content = f.readlines()
        first_row = content[0]
       ## first_row = int(d) for d in str(first_row)
       # r,c,l,h = first_row.split()
        return first_row.split()

def read_pizza (fname):
    '''
    Return:
    
    '''
    pizza = []
    with open(fname) as f:
        content = f.readlines()
        rows = content[1:]

       
        for row in rows:
            splited_row = list(row)
            del splited_row[-1]
           
            pizza.append(splited_row)
    return pizza    

def read_results (fname):
    '''
    Return: nr of points
    '''
    points = 0
    with open(fname) as f:
        content = f.readlines()
        number_of_slizes = content[0]
        silzes = content[1:]

        for slize in silzes:
            all_numbers = slize.split()
            print (all_numbers)
            one = int(all_numbers[0]) #0
            two = int(all_numbers[1]) #0
            three = int(all_numbers[2])#2
            four = int(all_numbers[3])#1

            x = one+three
            y = two+four

            points = x*y+1

       ## first_row = int(d) for d in str(first_row)
       # r,c,l,h = first_row.split()
    return points


def efectivness(points,l,r):
    x = float(points)
    
    y = float(l)*float(r)
    result = x/y
    print("The effectivness of the funcion is: ")
    print (result)
    return (result)



#Input
input_file_name = "files/example.in"
r,c,l,h = read_general_data(input_file_name)
original_pizza = read_pizza(input_file_name)

#Read results
result_file_name = "results.txt"
points = read_results(result_file_name)
efectivness(points,r,c)
