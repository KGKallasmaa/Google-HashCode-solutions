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
        print (first_row)

def efectivness(points,l,r):
    return (points)/(l*r)



#Input
file_name = "files/example.in"
read_general_data(file_name)