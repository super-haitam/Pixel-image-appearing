# Project that will give a place o screen for each pixel of the image, changing its color among the colors of the
#  original image till we get the exact same one.
import pygame
from PIL import Image
import random
from get_image_path import get_img_path
pygame.init()

# todo: Make the colors that are approximately the same to actually the same

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Get origin_img location path & open the image
origin_img_path = get_img_path()
origin_img = Image.open(origin_img_path)
ratio = origin_img.size[0] / origin_img.size[1]
if origin_img.size[0] >= origin_img.size[1]:
    W = min(origin_img.size[0], 350)
    origin_img = origin_img.resize((W, int(W / ratio)))
else:
    H = min(origin_img.size[1], 350)
    origin_img = origin_img.resize((int(H * ratio), H))


origin_img_w, origin_img_h = origin_img.size
loaded_px = origin_img.load()

img_colors = []
for j in range(origin_img_h):
    for i in range(origin_img_w):
        if loaded_px[i, j] not in img_colors:
            rounded_color = loaded_px[i, j]
            for img_color in img_colors:
                integer = 0
                for k in range(3):
                    if loaded_px[i, j][k] in range(img_color[k]-20, img_color[k]+20):
                        integer += 1
                if integer == 3:
                    rounded_color = img_color
                    break

            loaded_px[i, j] = rounded_color
            if rounded_color not in img_colors:
                img_colors.append(rounded_color)

print("\nThe colors that this image contains were brought down to", len(img_colors), "so that the program runs faster.")
print("And when the count raises to that number, you can say it's the exact copy of the original.")
print("Enjoy!")

# Pygame stuff
WIDTH, HEIGHT = origin_img_w*2, origin_img_h*2
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Image Appearing")
pygame_image = pygame.image.fromstring(origin_img.tobytes(), origin_img.size, origin_img.mode)
pygame_image = pygame.transform.scale(pygame_image, (WIDTH/3, WIDTH/3 / ratio)) \
    if pygame_image.get_width() >= pygame_image.get_height() else \
        pygame.transform.scale(pygame_image, (WIDTH/3 * ratio, WIDTH/3))
margin_x, margin_y = WIDTH/2.3, HEIGHT/4


# Pixel class; with properties, x, y, w, h, basically a pygame.Rect, a color
class Pixel:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect([x, y, w, h])
        self.got_colors = []
        self.random_color()

    def random_color(self):
        set1, set2 = set(img_colors), set(self.got_colors)
        self.color = random.choice(list(set1.difference(set2)))
        self.got_colors.append(self.color)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


# Functions
def draw_screen():
    global count
    screen.fill(BLACK)

    for j in range(origin_img_h):
        for i in range(origin_img_w):
            px_list[j][i].draw()

    screen.blit(pygame_image, (10, (HEIGHT - pygame_image.get_height())/2))

    font = pygame.font.SysFont("comicsans", 40)
    txt = font.render(f"Count: {count}", True, WHITE)
    screen.blit(txt, ((WIDTH - txt.get_width())/2, (margin_y - txt.get_height())/2))

    pygame.display.flip()


# Make the px_list
px_list = []
for j in range(origin_img_h):
    l = []
    for i in range(origin_img_w):
        l.append(Pixel(margin_x + i, margin_y + j, 1, 1))
    px_list.append(l)


# Mainloop
running = True
count = 0
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    draw_screen()

    for j in range(origin_img_h):
        for i in range(origin_img_w):
            px = px_list[j][i]
            if px.color != loaded_px[i, j]:
                px.random_color()
    count += 1
