from dataclasses import dataclass
import pyxel

WIDTH = 160
HEIGHT = 120
FRAMES_TO_ADD_ITEM = 3


@dataclass
class Item:
    point: int  # 0: 爆弾、1-: お金
    x: int
    y: int
    speed_x: float
    speed_y: float


class CatchGame:
    player_x: int  # プレイヤーの位置
    score: int  # スコア
    items: list[Item]  # 10回分のヒット表示
    level: int  # レベル
    is_game_over: bool  # ゲームオーバーかどうか

    def __init__(self):
        self.init()
        pyxel.init(WIDTH, HEIGHT, title="Catch Game")
        pyxel.run(self.update, self.draw)

    def init(self):
        self.player_x = 80
        self.score = 0
        self.items = []
        self.level = 1
        self.is_game_over = False

    def update(self):
        """ゲームの内容を進める"""
        # ゲームオーバーの場合
        if self.is_game_over:
            # スペースキーを押したら最初の状態に戻す
            if pyxel.btn(pyxel.KEY_SPACE):
                self.init()
            return

        # アイテムを移動する
        for item in self.items:
            item.x += item.speed_x
            item.y += item.speed_y

            # アイテムの落ちる速さを徐々に速くする
            item.speed_y += 0.1

            # アイテムがプレイヤーまで落ちたか？
            if item.y > 100:
                # プレイヤーとアイテムが重なっているか？
                if abs(item.x - self.player_x) < 4:
                    # お金を取った場合はスコアを加算し、それ以外はゲームオーバー
                    if item.point > 0:
                        self.score += item.point
                        # self.items.remove(item)
                    else:
                        self.is_game_over = True
                        print(self.player_x, item.x, item.y)
                        return

                # アイテムを取らずに落とした場合は消す
                self.items.remove(item)

        # プレイヤーの位置を更新する
        if pyxel.btn(pyxel.KEY_LEFT) and self.player_x > 2:
            self.player_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < WIDTH - 4:
            self.player_x += 2

        # レベルアップ
        if self.level < 9 and self.score >= self.level**2 * 10:
            self.level += 1

        # アイテムを追加する
        if pyxel.frame_count % FRAMES_TO_ADD_ITEM == 0:
            self.items.append(
                Item(
                    point=0 if pyxel.rndi(0, 9) < self.level else self.level,
                    x=WIDTH // 2,
                    y=0,
                    speed_x=pyxel.rndf(-2, 2),
                    speed_y=0,
                )
            )

    def draw(self):
        """ゲームの内容を画面に表示する"""
        # 画面をクリアする
        pyxel.cls(0)

        # プレイヤーを描画する
        pyxel.text(self.player_x, 100, "@", 7)

        # アイテムを描画する
        for item in self.items:
            if item.point > 0:
                # お金
                pyxel.text(item.x, item.y, str(item.point), 10)
            else:
                # 爆弾
                pyxel.text(item.x, item.y, "*", 8)

        # スコアを表示する
        pyxel.text(5, 5, f"Score: {self.score}", 7)

        # ゲームオーバーの場合はメッセージを表示する
        if self.is_game_over:
            pyxel.text(WIDTH // 2 - 18, 50, "GAME OVER", 8)
            pyxel.text(WIDTH // 2 - 32, 60, "SPACE TO RESTART", 8)


if __name__ == "__main__":
    CatchGame()
