import os
import fnmatch
import shutil

from collections import defaultdict


class ImageSorter:
    def __init__(self):
        self.extensions = ('*.jpg', '*.png', '*.jpeg')
        self.origin_dir = self.get_original_images_dir()
        self.images_dict = defaultdict(list)
        self.images_dir = os.path.join(os.getcwd(), 'images')
        self.image_counter = 0


    def get_original_images_dir(self):
        pathfile = os.path.join(os.getcwd(), 'dir_path.txt')
        with open(pathfile, 'r') as file:
            for line in file:
                return line.replace('\n', '')


    def find_images(self) -> None:
        for dirpath, _, filenames in os.walk(self.origin_dir):
            for extension in self.extensions:
                for filename in fnmatch.filter(filenames, extension):
                    self.images_dict[os.path.basename(dirpath)].append(os.path.join(dirpath, filename))
                    self.image_counter += 1
                    print(filename)
                    print(f'{self.image_counter} Images', end='\r')


    def move_images(self) -> None:
        os.chdir(self.images_dir)

        for dir_name, images in self.images_dict.items():
            try:
                os.mkdir(dir_name)
            except FileExistsError:
                pass

            for image in images:
                destination = os.path.join(dir_name, image.split('\\')[-1])
                try:
                    shutil.copy2(image, destination)
                except PermissionError:
                    pass
        print('\nDone.')


if __name__=='__main__':
    image_sorter = ImageSorter()
    image_sorter.find_images()
    image_sorter.move_images()
