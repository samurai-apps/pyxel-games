import random
import pyxel

WIDTH = 80
HEIGHT = 60

MAZE_W = 21
MAZE_H = 21

ISLE = 16
START = 15
GOAL = 14
TEMP_WALL = 13
WALL = 1


class MazeGame:
    player_x: int  # プレイヤーの位置
    player_y: int  # プレイヤーの位置
    maze_map: dict[tuple[int, int], int]
    is_game_over: bool  # ゲームオーバーかどうか

    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="Catch Game")
        self.init()
        pyxel.run(self.update, self.draw)

    def extend_wall(self, x, y, wall) -> bool:
        if self.maze_map[(x, y)] != ISLE and self.maze_map[(x, y)] != TEMP_WALL:
            return True

        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            mx, my = x + dx * 2, y + dy * 2

            if self.maze_map[(mx, my)] == TEMP_WALL:
                continue

            self.maze_map[(x, y)] = TEMP_WALL

            if self.extend_wall(mx, my, wall):
                self.maze_map[(x + dx, y + dy)] = wall
                self.maze_map[(mx, my)] = wall
                return True

        return False

    def init(self):
        self.player_x = 1
        self.player_y = 1
        self.is_game_over = False
        self.maze_map = {}
        for x in range(MAZE_W):
            for y in range(MAZE_H):
                if x == 0 or y == 0 or x == MAZE_W - 1 or y == MAZE_H - 1:
                    self.maze_map[(x, y)] = WALL
                else:
                    self.maze_map[(x, y)] = ISLE

        nodes = [
            (x, y) for x in range(2, MAZE_W - 2, 2) for y in range(2, MAZE_H - 2, 2)
        ]
        random.shuffle(nodes)

        while nodes:
            x, y = nodes.pop()

            if self.maze_map[(x, y)] == WALL:
                continue

            # self.extend_wall(x, y, WALL)
            if self.extend_wall(x, y, WALL):
                self.maze_map[(x, y)] = WALL

        self.maze_map[(1, 1)] = START
        self.maze_map[(MAZE_W - 2, MAZE_H - 2)] = GOAL

    def update(self):
        """ゲームの内容を進める"""
        if self.is_game_over:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.init()
            return

        if (
            pyxel.btnp(pyxel.KEY_LEFT, repeat=6)
            and self.maze_map[(self.player_x - 1, self.player_y)] >= 14
        ):
            self.player_x -= 1
        elif (
            pyxel.btnp(pyxel.KEY_RIGHT, repeat=6)
            and self.maze_map[(self.player_x + 1, self.player_y)] >= 14
        ):
            self.player_x += 1
        elif (
            pyxel.btnp(pyxel.KEY_UP, repeat=6)
            and self.maze_map[(self.player_x, self.player_y - 1)] >= 14
        ):
            self.player_y -= 1
        elif (
            pyxel.btnp(pyxel.KEY_DOWN, repeat=6)
            and self.maze_map[(self.player_x, self.player_y + 1)] >= 14
        ):
            self.player_y += 1

        if self.maze_map[(self.player_x, self.player_y)] == GOAL:
            self.is_game_over = True

    def draw(self):
        """ゲームの内容を画面に表示する"""
        # 画面をクリアする
        pyxel.cls(0)

        # 迷路を描画する
        for x in range(MAZE_W):
            for y in range(MAZE_H):
                if self.maze_map[(x, y)] > 0:
                    pyxel.rect(
                        (x - self.player_x) * 10 + WIDTH // 2 - 5,
                        (y - self.player_y) * 10 + HEIGHT // 2 - 5,
                        9,
                        9,
                        self.maze_map[(x, y)] % 16,
                    )

        # プレイヤーを描画する
        pyxel.rect(WIDTH // 2 - 4, HEIGHT // 2 - 4, 7, 7, 7)

        # ゲームオーバーの場合
        if self.is_game_over:
            pyxel.text(WIDTH // 2 - 16, HEIGHT // 2 - 9, "GOAL !!!", 8)
            pyxel.text(WIDTH // 2 - 40, HEIGHT // 2 + 1, "HIT SPACE TO RESTART", 8)


if __name__ == "__main__":
    MazeGame()
