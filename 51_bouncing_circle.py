import pyxel
import random

WIDTH = 200
HEIGHT = 200
RADIUS = 15
COLORS = [7, 13, 6, 12, 5, 1, 0]


class BouncingCircle:
    def __init__(self):
        # ボールの速さを乱数で決める
        self.speed_x = random.uniform(-10, 10)
        self.speed_y = random.uniform(-10, 10)

        # ボール位置を７つまで覚えておく
        self.x = [WIDTH / 2.0] * 7
        self.y = [HEIGHT / 2.0] * 7

        # Pyxelの初期化と実行
        pyxel.init(WIDTH, HEIGHT, title="跳ねるボール")
        pyxel.cls(7)
        pyxel.run(self.update, self.draw)

    def update(self):
        # 今までのボールの位置を一番古いものを１つ忘れて、その他を覚えておく
        for i in range(6):
            self.x[i] = self.x[i + 1]
            self.y[i] = self.y[i + 1]

        # 最新の位置をスピード分だけ動かす
        x = self.x[5] + self.speed_x
        y = self.y[5] + self.speed_y

        # 跳ね返りの処理
        if x < 0:
            self.speed_x = -self.speed_x
            x = -x
        elif x > WIDTH - RADIUS:
            self.speed_x = -self.speed_x
            x = WIDTH - RADIUS - x + WIDTH - RADIUS

        if y < 0:
            self.speed_y = -self.speed_y
            y = -y
        elif y > HEIGHT - RADIUS:
            self.speed_y = -self.speed_y
            y = HEIGHT - RADIUS - y + HEIGHT - RADIUS

        # 最新の位置をボール位置配列の一番新しい場所に保存する
        self.x[6] = x
        self.y[6] = y

    def draw(self):
        # ボールと軌跡を描画
        for i in range(7):
            pyxel.elli(self.x[i], self.y[i], RADIUS, RADIUS, COLORS[i])


if __name__ == "__main__":
    BouncingCircle()
