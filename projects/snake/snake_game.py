#!/usr/bin/env python3
"""
简单的贪吃蛇游戏
使用方向键控制蛇移动，吃到食物变长，撞墙或撞自己游戏结束
"""

import pygame
import random
import sys

# 初始化
pygame.init()

# 游戏配置
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10

# 颜色
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# 方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)

        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if not self.grow:
                self.positions.pop()
            else:
                self.grow = False

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, GREEN, 
                           (p[0] * CELL_SIZE, p[1] * CELL_SIZE, 
                            CELL_SIZE, CELL_SIZE))


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))
        if self.position in snake_positions:
            self.randomize_position(snake_positions)

    def render(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0] * CELL_SIZE,
                         self.position[1] * CELL_SIZE,
                         CELL_SIZE, CELL_SIZE))


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('贪吃蛇')

    snake = Snake()
    food = Food()
    score = 0
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        snake.update()

        # 检测是否吃到食物
        if snake.get_head_position() == food.position:
            snake.grow = True
            score += 1
            food.randomize_position(snake.positions)

        # 绘制
        screen.fill(BLACK)
        snake.render(screen)
        food.render(screen)

        # 显示分数
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
