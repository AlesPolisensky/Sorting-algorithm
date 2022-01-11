import pygame
import random
import math

pygame.init()

class Information:
    SIDES = 100
    TOP = 150
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    BLACK = 0, 0, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    BACKGROUND = BLACK
    GRADIENTS = [(128, 128, 128), #LIGHT GREY
                 (160, 160, 160), #GREY
                 (192,192,192)]   #DARK GREY
    FONT = pygame.font.SysFont("opensans", 30)
    LARGE_FONT = pygame.font.SysFont("opensans", 40)
    
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm")
        self.set_list(lst)
    
    def set_list(self, lst):
        TOP = 150
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)
        self.pixel_width = round((self.width - self.SIDES) / len(lst))
        self.pixel_height = math.floor((self.height - TOP) / (self.max_val - self.min_val))
        self.start_x = self.SIDES // 2

def bubble(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            number1 = lst[j]
            number2 = lst[j + 1]

            if (number1 > number2 and ascending) or (number1 < number2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_lst(draw_info, {j: draw_info.BLUE, j + 1: draw_info.RED}, True)
                yield True

    return lst

def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_lst(draw_info, {i - 1: draw_info.BLUE, i: draw_info.RED}, True)
            yield True

    return lst

def generate_lst(n, min, max):
    lst = []
    
    for _ in range(n):
        val = random.randint(min, max)
        lst.append(val)
    return lst

def draw_lst(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst
    
    if clear_bg:
        clear_rect = (draw_info.SIDES//2, draw_info.TOP, 
                    draw_info.width - draw_info.SIDES, draw_info.height - draw_info.TOP)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND, clear_rect)
    
    for idx, val in enumerate(lst):
        x = draw_info.start_x + idx * draw_info.pixel_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.pixel_height
        color = draw_info.GRADIENTS[idx % 3]
        
        if idx in color_positions:
    	    color = color_positions[idx]       
        
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.pixel_width, draw_info.height))
        
    if clear_bg:
        pygame.display.update()

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND)
    title = draw_info.LARGE_FONT.render(f"{algo_name} : {'Ascending' if ascending else 'Descending'}", 1, draw_info.WHITE)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))
    controls = draw_info.FONT.render("PRESS: Reset : R | Start Sorting : SPACE | Ascending : A | Descending : D", 1, draw_info.WHITE)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))
    sorting = draw_info.FONT.render("PRESS: Insertion Sort : I | Bubble Sort : B", 1, draw_info.WHITE)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))
    draw_lst(draw_info)
    pygame.display.update()
    
    
def main():
    run = True
    clock = pygame.time.Clock()
    n = 50
    min = 0
    max = 100
    lst = generate_lst(n, min, max)
    draw_info = Information(1400, 1000, lst)
    sort = False
    ascending = True
    sorting_algorithm = bubble
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
    
    while run:
        clock.tick(80)
        if sort:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sort = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
        
        
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            
            if i.type != pygame.KEYDOWN:
                continue
            if i.key == pygame.K_r:
                lst = generate_lst(n, min, max)
                draw_info.set_list(lst)
            elif i.key == pygame.K_i and not sort:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif i.key == pygame.K_b and not sort:
                sorting_algorithm = bubble
                sorting_algo_name = "Bubble Sort"
            elif i.key == pygame.K_SPACE and sort == False:
                sort = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
            elif i.key == pygame.K_a and not sort:
                ascending = True
            elif i.key == pygame.K_d and not sort:
                ascending = False
                
                
    pygame.quit()
    
    
if __name__ == "__main__":
    main()