import pygame
from collections import deque


class Ripple:
    def __init__(self, max_r, max_a, color):
        self.radius = 0
        self.max_radius = max_r
        self.max_alpha = max_a
        self.color = color

    def step(self):
        alpha = (1 - abs(2 * self.radius / self.max_radius - 1)) * self.max_alpha
        c = pygame.Color(*self.color, int(alpha))
        pygame.draw.circle(surface, c, (width / 2, height / 2), self.radius)
        if self.radius / self.max_radius >= 1 / 8:
            pygame.draw.circle(surface, (0, 0, 0), (width / 2, height / 2),
                               self.max_radius * (8 * self.radius / self.max_radius - 1) / (8 - 1))
        self.radius += 1


if __name__ == '__main__':
    pygame.init()
    width, height = 2560, 1600
    pygame.mouse.set_visible(False)
    screen = pygame.display.set_mode((width, height))
    pygame.mixer.set_num_channels(256)
    surface = screen.convert_alpha()
    pianoKey = ['c',  'c#',  'd',  'd#',  'e',  'f',  'f#',  'g',  'g#',  'a',  'a#',  'b',
                'c1', 'c1#', 'd1', 'd1#', 'e1', 'f1', 'f1#', 'g1', 'g1#', 'a1', 'a1#', 'b1',
                'c2', 'c2#', 'd2', 'd2#', 'e2', 'f2', 'f2#', 'g2', 'g2#', 'a2', 'a2#', 'b2']
    boardKey = [pygame.K_t, pygame.K_5, pygame.K_r, pygame.K_4, pygame.K_e, pygame.K_w,
                pygame.K_2, pygame.K_a, pygame.K_q, pygame.K_z, pygame.K_s, pygame.K_x,
                pygame.K_c, pygame.K_f, pygame.K_v, pygame.K_g, pygame.K_b, pygame.K_n,
                pygame.K_j, pygame.K_m, pygame.K_k, pygame.K_COMMA, pygame.K_l, pygame.K_PERIOD,
                pygame.K_SLASH, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_RIGHTBRACKET,
                pygame.K_LEFTBRACKET, pygame.K_p, pygame.K_0, pygame.K_o, pygame.K_9,
                pygame.K_i, pygame.K_8, pygame.K_u]
    keyDict = {bk: pk for bk, pk in zip(boardKey, pianoKey)}
    colorDict = {bk: (4*i, 4*i, 4*i) for i, bk in enumerate(boardKey, 1)}
    max_radius, max_alpha = 512, 128
    q = deque()
    out = False
    while not out:
        for _ in range(len(q)):
            r = q.popleft()
            r.step()
            if r.radius < max_radius:
                q.append(r)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        pygame.draw.circle(surface, (0, 0, 0), (width / 2, height / 2), max_radius)
        screen.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_ESCAPE:
                    pygame.quit()
                    out = True
                elif key in keyDict.keys():
                    fileName = "./audios/" + str(keyDict[key]) + ".wav"
                    pygame.mixer.Sound(fileName).play()
                    q.append(Ripple(max_radius, max_alpha, color=colorDict[key]))
