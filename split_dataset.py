import random
import glob
import os
import shutil


#utility function that copies the existing images and annotations into the desired new folder
def copyfiles(fil, root_dir):
    basename = os.path.basename(fil)
    filename = os.path.splitext(basename)[0]
    # image
    src = fil
    dest = os.path.join(root_dir, image_dir, f"{filename}.jpg")
    shutil.copyfile(src, dest)
    # label
    src = os.path.join(label_dir, f"{filename}.txt")
    dest = os.path.join(root_dir, label_dir, f"{filename}.txt")
    if os.path.exists(src):
        shutil.copyfile(src, dest)
        
#creation of variables for image and label directory 
image_dir = "images/"
label_dir = "labels/"
lower_limit = 0
files = glob.glob(os.path.join(image_dir, '*.jpg'))

#for randomly selecting the images for splitting
random.shuffle(files)

#split proportion of the dataset for testing and validation work
folders = {"train": 0.9, "val": 0.1}
#folders = {"train": 0.8, "val": 0.1, "test": 0.1} #when it is necessary to have some testing data as well.
check_sum = sum([folders[x] for x in folders])
assert check_sum == 1.0, "Split proportion is not equal to 1.0"

#with the required portion of the data, images and annotations are sent into the desired locations
for folder in folders:
    os.mkdir(folder)
    temp_label_dir = os.path.join(folder, label_dir)
    os.mkdir(temp_label_dir)
    temp_image_dir = os.path.join(folder, image_dir)
    os.mkdir(temp_image_dir)
    limit = round(len(files) * folders[folder])
    for fil in files[lower_limit:lower_limit + limit]:
        copyfiles(fil, folder)
    lower_limit = lower_limit + limit