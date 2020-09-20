import csv, os

static_folder = "C:/Users/57leo/Downloads/website-v2/Main/static/"

def get_team_data():
    # Get filepaths of existing imgs
    existing_filenames = os.listdir(os.path.join(static_folder, 'images/2018-members'))
    # 
    filename = os.path.join(static_folder, './StartLabs Team Bios.csv')
    all_data = []
    with open(filename) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            fullname = row["Name"]
            firstname, lastname = fullname.split(" ")
            possible_img_path = firstname.lower()+"-white.jpg"
            if (possible_img_path in existing_filenames):
                row["image_path"] = possible_img_path
            else:
                row["image_path"] = "anon-face"
            all_data.append(row)
    for row in all_data:
        print(row)
            

get_team_data()

