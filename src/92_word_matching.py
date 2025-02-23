import csv
import pyxel
import random
import math

# 画面サイズ
SCREEN_W = 180
SCREEN_H = 160
CARD_W = 70
CARD_H = 20
LIFE = 3

# 単語リスト（初期状態: 空）
word_list = [
    ("猫", "Cat", 1),
    ("犬", "Dog", 1),
    ("魚", "Fish", 2),
    ("鳥", "Bird", 2),
    ("馬", "Horse", 3),
    ("赤", "Red", 3),
    ("青", "Blue", 4),
    ("緑", "Green", 4),
    ("黄", "Yellow", 5),
    ("白", "White", 5),
    ("哲学", "Philosophy", 18),
    ("宇宙", "Universe", 19),
    ("進化", "Evolution", 19),
    ("宿命", "Fate", 20),
    ("永遠", "Eternity", 20),
]
csv_filename = "words.csv"  # 読み込むCSVファイル名


def load_words_from_csv(filename):
    """CSVから単語データを読み込む"""
    global word_list
    word_list = []

    try:
        with open(filename, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # ヘッダーをスキップ

            for row in reader:
                if len(row) < 3:
                    continue  # フォーマットエラーを回避
                japanese, english, difficulty = row[0], row[1], row[2]
                try:
                    difficulty = int(difficulty)  # 難易度を整数に変換
                    word_list.append((japanese, english, difficulty))
                except ValueError:
                    continue  # 数値でないデータをスキップ
    except FileNotFoundError:
        print(f"エラー: {filename} が見つかりません。")
        word_list = []


class MatchingGame:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="単語マッチングゲーム")
        pyxel.mouse(True)
        umplus12 = pyxel.Font("umplus_j12r.bdf")
        self.font = umplus12
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """ゲームのリセット"""
        self.stage = 0
        self.lives = LIFE
        self.score = 0
        self.load_stage()

    def load_stage(self):
        """新しいステージの問題を選ぶ"""
        if not word_list:
            print("単語リストが空です。Google Sheetsを読み込んでください。")
            return

        target_difficulty = min(1 + self.stage // 2, 20)  # 目標難易度

        difficulty_weights = {
            d: math.exp(-0.2 * (d - target_difficulty) ** 2) for d in range(1, 21)
        }

        total_weight = sum(difficulty_weights.values())
        for d in difficulty_weights:
            difficulty_weights[d] /= total_weight

        candidates = [w for w in word_list]
        weights = [difficulty_weights[w[2]] for w in candidates]

        self.words = random.choices(candidates, weights=weights, k=5)

        self.japanese_cards = [w[0] for w in self.words]
        self.english_cards = [w[1] for w in self.words]
        random.shuffle(self.english_cards)

        self.selected_jp = None
        self.selected_en = None
        self.pairs_found = 0

    def update(self):
        """ゲームの更新処理"""
        if self.lives <= 0:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x, pyxel.mouse_y
            self.check_selection(x, y)

    def check_selection(self, x, y):
        """クリックされたカードの判定"""
        for i in range(len(self.japanese_cards)):
            if 10 <= x <= 10 + CARD_W and 20 + i * 25 <= y <= 20 + i * 25 + CARD_H:
                self.selected_jp = i

            if 100 <= x <= 100 + CARD_W and 20 + i * 25 <= y <= 20 + i * 25 + CARD_H:
                self.selected_en = i

        if self.selected_jp is not None and self.selected_en is not None:
            self.check_match()

    def check_match(self):
        """ペア判定"""
        jp_word = self.japanese_cards[self.selected_jp]
        en_word = self.english_cards[self.selected_en]
        correct_pair = any(jp_word == w[0] and en_word == w[1] for w in self.words)

        if correct_pair:
            self.pairs_found += 1
            del self.japanese_cards[self.selected_jp]
            del self.english_cards[self.selected_en]
        else:
            self.lives -= 1

        self.selected_jp = None
        self.selected_en = None

        if self.pairs_found == 5:
            self.stage += 1
            self.score = self.stage
            self.load_stage()

    def draw(self):
        """画面描画"""
        pyxel.cls(0)

        if self.lives <= 0:
            pyxel.text(50, 50, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(50, 70, f"Score: {self.score}", 7)
            pyxel.text(50, 100, "R key to restart", 7)
            return

        pyxel.text(5, 5, f"Stage: {self.stage+1}", 7)
        pyxel.text(120, 5, f"Lives: {self.lives}", 7)

        for i, word in enumerate(self.japanese_cards):
            color = 10 if self.selected_jp == i else 7
            pyxel.rectb(10, 20 + i * 25, CARD_W, CARD_H, color)
            pyxel.text(15, 25 + i * 25, word, color, self.font)

        for i, word in enumerate(self.english_cards):
            color = 10 if self.selected_en == i else 7
            pyxel.rectb(100, 20 + i * 25, CARD_W, CARD_H, color)
            pyxel.text(105, 25 + i * 25, word, color, self.font)


if __name__ == "__main__":
    # load_words_from_csv(csv_filename)  # CSVから単語データを読み込む
    MatchingGame()
