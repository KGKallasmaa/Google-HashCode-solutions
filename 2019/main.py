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
    with open(fname) as f:
        content = f.readlines()
        rows = content[1:]

        pizza = []
        
        for row in rows:
            splited_row = list(row)
            del splited_row[-1]
           
            pizza.append(splited_row)

        return pizza    
def efectivness(points,l,r):
    return (points)/(l*r)



#Input
file_name = "files/example.in"
r,c,l,h = read_general_data(file_name)
pizza = read_pizza(file_name)

print (pizza)