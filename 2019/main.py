def read_general_data (fname):
    '''
    Return:
    N-number of photos
    '''

    with open(fname) as f:
        content = f.readlines()
        first_row = content[0]
       ## first_row = int(d) for d in str(first_row)
       # r,c,l,h = first_row.split()
        return first_row.split()[0]


class Picture:
  def __init__(self,id,number_of_tags,orientation,tags):
      self.id = id
      self.number_of_tags = number_of_tags
      self.orientation = orientation
      self.tags = tags

def read_picture_data(fname):
    pictures = list()

    with open(fname) as f:
        content = f.readlines()
    
        i = 0
        id = 0
        for row in content:
            if (i == 0):
                i = i+1
            else:
                information = row.split()
                j = 0
                ori = information[0]
                number_of_tags = information[1]
                print (ori)
                tags = information[2:]
               
                        
                picture = Picture(id,number_of_tags,ori,tags)
                pictures.append(picture)
                id +=1 

    return pictures

#Input
input_file_name = "files/a_example.txt"
numer_of_pictures = read_general_data(input_file_name)

pictures = read_picture_data(input_file_name)
