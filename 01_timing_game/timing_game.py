import pyxel


class TimingGame:
    obj_x: int  # 動くバーの位置
    obj_speed: float  # 動くバーのスピード：０より大きければ右、小さければ左に動く
    score: int  # スコア
    history: list[str]  # 10回分のヒット表示

    def __init__(self):
        self.obj_x = 80
        self.obj_direction = 1
        self.score = 0
        self.history = [""] * 20

        pyxel.init(160, 120, title="Timing Game")
        pyxel.run(self.update, self.draw)

    def update(self):
        """ゲームの内容を進める"""

        # 動くオブジェクトの位置を更新する
        print(self.obj_x, self.obj_direction)
        if self.obj_x >= 146 or self.obj_x <= 14:
            # 右端、または左端についたら方向を反転する
            self.obj_direction *= -1

        # 動くオブジェクトの位置を移動する
        self.obj_x += 3 * self.obj_direction

        # スペースキーを押したタイミングで点数を加える
        if pyxel.btnp(pyxel.KEY_SPACE):
            # 動くバーの位置でスコアを決める
            if 75 <= self.obj_x <= 85:
                score = 10
                text = "GREAT"
            elif 40 < self.obj_x <= 120:
                score = 2
                text = "GOOD"
            else:
                score = -4
                text = "BAD"

            # スコアを足す
            self.score += score
        else:
            text = ""

        # ヒット表示を１つずらす
        for i in range(19):
            self.history[i] = self.history[i + 1]
        self.history[19] = text

    def draw(self):
        """ゲームの内容を画面に表示する"""
        # 画面をクリアする
        pyxel.cls(0)

        # 背景のバーを描画する
        pyxel.rect(10, 60, 140, 8, 10)
        pyxel.rect(40, 60, 80, 8, 7)
        pyxel.rect(75, 60, 10, 8, 6)

        # 動くバーを描画する
        pyxel.rect(self.obj_x - 3, 60, 6, 8, 9)

        # スコアを表示する
        pyxel.text(5, 5, f"Score: {self.score}", 7)

        # 過去のスコアを表示する
        for i, text in enumerate(self.history):
            pyxel.text(80 - (len(text) * 4) // 2, 20 + i * 2, text, 7)


if __name__ == "__main__":
    TimingGame()
