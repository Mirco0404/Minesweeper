import pygame
import os


class Settings():
    width = 1280
    height = 720
    fps = 60
    title = "images"
    file_path = os.path.dirname(os.path.abspath(__file__))
    images_path = os.path.join(file_path, "resources")

    @staticmethod
    def get_dim():
        return (Settings.width, Settings.height)

images = []
images.append(pygame.image.load(os.path.join(Settings.images_path, "mine5.png")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "tile.png")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "one.jpg")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "two.jpg")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "three.jpg")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "four.jpg")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "five.jpg")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "six.jpg")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "seven.jpg")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "eight.jpg")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "clear.png")))
images.append(pygame.image.load(os.path.join(Settings.images_path, "flag.jpg")))