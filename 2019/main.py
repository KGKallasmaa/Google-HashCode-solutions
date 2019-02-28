def read_general_data(fname):
    '''
    Return:
    N-number of photos
    '''

    with open(fname) as f:
        content = f.readlines()
        first_row = content[0]
        return first_row.split()[0]


class Picture:
    def __init__(self, id, is_used, number_of_tags, orientation, tags):
        self.id = id
        self.number_of_tags = number_of_tags
        self.is_used = is_used
        self.orientation = orientation
        self.tags = tags


def read_picture_data(fname):
    pictures = list()

    with open(fname) as f:
        content = f.readlines()

        i = 0
        id = 0
        for row in content:
            if i == 0:
                i = i + 1
            else:
                information = row.split()
                j = 0
                ori = information[0]
                number_of_tags = information[1]
                tags = information[2:]

                picture = Picture(id, False, number_of_tags, ori, tags)
                pictures.append(picture)
                id += 1

    return pictures


def input_is_correct(input_pics):
    ids = list()

    for pic in input_pics:
        ids.append(pic.id)

    # Are ids uniqye
    if len(ids) != len(set(ids)):
        print("Picture ids are not unique!")
        return False

    # Are they connected by tags

    i = 0
    current_tags = list()
    for pic in input_pics:
        if i == 0:
            current_tags = pic.tags
            i += 1
        else:
            my_tags = pic.tags

            # They share
            if not (bool(set(my_tags) & set(current_tags))):
                print("Picture tags do not match. " + str(my_tags) + " vs " + str(current_tags))
                return False
            current_tags = pic.tags

    return True


def number_of_slides(pictures):
    number_of_slides = 0

    number_of_verticals_at_current_slide = 0

    for pic in pictures:
        if pic.orientation == "H":
            number_of_slides += 1
        else:
            if number_of_verticals_at_current_slide == 0:
                number_of_slides += 0
                number_of_verticals_at_current_slide = 1
            elif number_of_verticals_at_current_slide == 1:
                number_of_slides += 1
                number_of_verticals_at_current_slide = 0

    return number_of_slides


def make_output_file(input_pics):
    f = open("submit_file.txt", "a")

    "Check if input is correct"
    correct_input = input_is_correct(input_pics)
    if not correct_input:
        print("Picture slides are not formated correclty")
    # return None

    current_submitformat_is_horistonal = True

    nuber_of_pics = str(number_of_slides(input_pics))
    f.write(nuber_of_pics + "\n")

    for pic in input_pics:
        pic_id = str(pic.id)
        pic_orientation = str(pic.orientation)

        # picture is horistonal
        if pic_orientation == "H":
            f.write(pic_id + "\n")
            current_submitformat_is_horistonal = True
        # is vertical
        else:
            if current_submitformat_is_horistonal:
                f.write(pic_id + " ")
                current_submitformat_is_horistonal = False
            else:
                f.write(pic_id + "\n")

    f.close()


# Input
input_file_name = "files/a_example.txt"
numer_of_pictures = read_general_data(input_file_name)

pictures = read_picture_data(input_file_name)

make_output_file(pictures)
