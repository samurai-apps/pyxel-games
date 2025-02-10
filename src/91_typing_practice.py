import pyxel
import random

# タイピング用の単語リスト
KEYWORDS = [
    "def",
    "return",
    "import",
    "class",
    "self",
    "if",
    "else",
    "elif",
    "for",
    "while",
    "True",
    "False",
    "None",
    "print",
    "input",
    "list",
    "dict",
    "set",
    "tuple",
    # "lambda",  "try", "except", "finally","global","nonlocal", "yield",
]
SYMBOLS = [
    "()",
    "{}",
    "[]",
    ":",
    ";",
    ".",
    ",",
    "=",
    "+",
    "-",
    "*",
    "/",
    "<",
    ">",
    "_",
    "!",
]
PYXELS = [
    # Pyxelの基本セットアップ
    "pyxel.",
    "pyxel.init(",
    "pyxel.run(",
    "update():",
    "draw():",
    "quit()",
    # 描画関数
    "cls(",
    "text(",
    "rect(",
    "circ(",
    "blt(",
    # 色コード
    "COLOR_RED",
    "COLOR_BLUE",
    "COLOR_YELLOW",
    "COLOR_BLACK",
    "COLOR_WHITE",
    # キーボード入力
    "KEY_SPACE",
    "KEY_ENTER",
    "KEY_LEFT",
    "KEY_RIGHT",
    "if pyxel.btn(",
    "if pyxel.btnp(",
    # マウス入力
    "pyxel.mouse_x",
    "pyxel.mouse_y",
    # "pyxel.MOUSE_LEFT_BUTTON",
    # "pyxel.MOUSE_RIGHT_BUTTON",
    # 変数と数値
    "x = 0",
    "y = 0",
    "score += 1",
    "player_x = 80",
    "player_y = 60",
    "self.timer -= 1",
    "self.lives -= 1",
    # 条件分岐・ループ
    "if x > 10:",
    "if y < 50:",
    "for i in range(",
    "while True:",
    # リスト・辞書
    "bullets = []",
    "enemies = []",
    "data = {'x': 10}",
    "data['y'] = 20",
    # サウンド
    "sound(",
    "play(",
    "music(",
    # その他
    # "pyxel.fullscreen()",
    # "pyxel.frame_count",
    # "def main():",
    "return x",
]
WORDS = KEYWORDS + SYMBOLS + PYXELS

# サウンドエフェクト
SFX_CORRECT = 0
SFX_WRONG = 1
SFX_TYPE = 2

# BGM の定義
BGM_NORMAL = 0  # 通常時のBGM
BGM_FAST = 1  # 残り10秒でテンポアップ

# ゲームの制限時間（30秒 = 900フレーム）
GAME_TIME = 30 * 30
FAST_BGM_TIME = 10 * 30  # 残り10秒（300フレーム）

# ゲーム状態
STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2

# キーボード配列オプション
JIS_MODE = 0
US_MODE = 1

# QWERTY 配列（通常時）
KEYBOARD_LAYOUT = [
    ["1234567890-^\\ ", "qwertyuiop@[", "asdfghjkl;:]", "zxcvbnm,./_"],
    ["`1234567890-= ", " qwertyuiop[]\\", " asdfghjkl;'", " zxcvbnm,./"],
]

# 記号モードのキーボード配列
SYMBOL_LAYOUT = [
    [
        "!\"#$%&'() =~| ",
        "QWERTYUIOP`{",
        "ASDFGHJKL+*}",
        "ZXCVBNM<>?_",
    ],
    ["~!@#$%^&*()_+ ", " QWERTYUIOP{}|", ' ASDFGHJKL:"', " ZXCVBNM<>?"],
]

SYMBOL_KEYS: list[int, dict[int, tuple[str, str]]] = [
    {
        # １段目（通常入力 & シフト時の記号）
        pyxel.KEY_1: ("1", "!"),
        pyxel.KEY_2: ("2", '"'),
        pyxel.KEY_3: ("3", "#"),
        pyxel.KEY_4: ("4", "$"),
        pyxel.KEY_5: ("5", "%"),
        pyxel.KEY_6: ("6", "&"),
        pyxel.KEY_7: ("7", "'"),
        pyxel.KEY_8: ("8", "("),
        pyxel.KEY_9: ("9", ")"),
        pyxel.KEY_0: ("0", "~"),
        pyxel.KEY_MINUS: ("-", "="),
        pyxel.KEY_CARET: ("^", ""),
        pyxel.KEY_BACKSLASH: ("\\", "|"),
        # ２段目（通常入力 & シフト時の記号）
        pyxel.KEY_AT: ("@", "`"),
        pyxel.KEY_LEFTBRACKET: ("[", "{"),
        # ３段目（通常入力 & シフト時の記号）
        pyxel.KEY_SEMICOLON: (";", "+"),
        pyxel.KEY_COLON: (":", "*"),
        pyxel.KEY_RIGHTBRACKET: ("]", "}"),
        # ４段目（通常入力 & シフト時の記号）
        pyxel.KEY_COMMA: (",", "<"),
        pyxel.KEY_PERIOD: (".", ">"),
        pyxel.KEY_SLASH: ("/", "?"),
        pyxel.KEY_UNDERSCORE: ("_", "_"),  # 「ろ」キー
    },
    {
        # １段目（通常入力 & シフト時の記号）
        pyxel.KEY_BACKQUOTE: ("`", "~"),
        pyxel.KEY_1: ("1", "!"),
        pyxel.KEY_2: ("2", "@"),
        pyxel.KEY_3: ("3", "#"),
        pyxel.KEY_4: ("4", "$"),
        pyxel.KEY_5: ("5", "%"),
        pyxel.KEY_6: ("6", "^"),
        pyxel.KEY_7: ("7", "&"),
        pyxel.KEY_8: ("8", "*"),
        pyxel.KEY_9: ("9", "("),
        pyxel.KEY_0: ("0", ")"),
        pyxel.KEY_MINUS: ("-", "_"),
        pyxel.KEY_EQUALS: ("=", "+"),
        # ２段目（通常入力 & シフト時の記号）
        pyxel.KEY_LEFTBRACKET: ("[", "{"),
        pyxel.KEY_RIGHTBRACKET: ("]", "}"),
        pyxel.KEY_BACKSLASH: ("\\", "|"),
        # ３段目（通常入力 & シフト時の記号）
        pyxel.KEY_SEMICOLON: (";", ":"),
        pyxel.KEY_QUOTE: ("'", '"'),
        # ４段目（通常入力 & シフト時の記号）
        pyxel.KEY_COMMA: (",", "<"),
        pyxel.KEY_PERIOD: (".", ">"),
        pyxel.KEY_SLASH: ("/", "?"),
    },
]


class TypingGame:
    def __init__(self):
        pyxel.init(160, 120, title="Typing Practice", fps=30)
        self.setup_sounds()
        self.setup_music()
        self.change_state(STATE_TITLE)
        pyxel.run(self.update, self.draw)

    def setup_sounds(self):
        """効果音の設定"""
        pyxel.sounds[SFX_CORRECT].set("c3e3g3c4", "t", "6", "vffn", 10)
        pyxel.sounds[SFX_WRONG].set("c2f2a2f2", "t", "6", "vffn", 10)
        pyxel.sounds[SFX_TYPE].set("c3", "t", "5", "n", 5)

    def setup_music(self):
        """BGM の設定"""
        # 通常BGM
        pyxel.sounds[10].set("g3c4e4g4 c4e4g4c4", "t", "2", "n", 20)
        pyxel.sounds[11].set("c2 c2 g2 g2 f2 f2 g2 g2", "p", "2", "n", 20)
        pyxel.sounds[12].set("c3e3g3 c3f3a3 d3g3b3 c3e3g3", "p", "2", "n", 20)

        # 高速BGM（通常BGMのテンポアップ）
        pyxel.sounds[20].set("g3c4e4g4 c4e4g4c4", "t", "2", "n", 10)
        pyxel.sounds[21].set("c2 c2 g2 g2 f2 f2 g2 g2", "p", "2", "n", 10)
        pyxel.sounds[22].set("c3e3g3 c3f3a3 d3g3b3 c3e3g3", "p", "2", "n", 10)

        pyxel.musics[BGM_NORMAL].set([10, 11, 12])
        pyxel.musics[BGM_FAST].set([20, 21, 22])

    def get_new_word(self) -> str:
        """新しい単語を取得"""
        # next_words は十分な長さがあると仮定
        return self.next_words.pop(0)

    def change_state(self, state) -> None:
        """ゲームの状態を変更"""
        self.state = state

        if state == STATE_TITLE:
            """ゲームの初期化"""
            self.keyboard_mode = JIS_MODE  # 初期値はJIS配列
            self.input_text = ""
            self.score = 0
            self.total_chars = 0
            self.timer = GAME_TIME  # 30秒（900フレーム）
            self.shift_mode = False  # シフトキーの状態
            self.next_words = random.sample(WORDS, k=len(WORDS))
            self.word = self.get_new_word()

            pyxel.playm(BGM_NORMAL, loop=True)  # 通常BGMに戻す

        elif state == STATE_PLAYING:
            self.word = self.get_new_word()

        else:
            pyxel.stop()

    def update(self):
        """ゲームの更新処理"""
        if self.state == STATE_TITLE:
            self.update_title()
        elif self.state == STATE_GAMEOVER:
            self.update_gameover()
        else:
            self.update_playing()

    def update_title(self):
        """タイトル画面の処理"""
        if pyxel.btnp(pyxel.KEY_1):  # 1キーでJIS配列を選択
            self.keyboard_mode = JIS_MODE
            self.change_state(STATE_PLAYING)
        elif pyxel.btnp(pyxel.KEY_2):  # 2キーでUS配列を選択
            self.keyboard_mode = US_MODE
            self.change_state(STATE_PLAYING)

    def update_playing(self):
        """ゲームの更新処理"""
        self.timer -= 1

        # 残り10秒でBGMを高速に変更
        if self.timer == FAST_BGM_TIME:
            pyxel.playm(BGM_FAST, loop=True)

        # 時間切れでゲームリセット
        if self.timer <= 0:
            self.change_state(STATE_GAMEOVER)

        # タイプ音処理のため前の文字列を記憶
        text_before = self.input_text

        # シフトキーの状態を取得
        self.shift_mode = pyxel.btn(pyxel.KEY_SHIFT)

        # キーボード入力（通常の英字）
        for key in range(97, 123):  # 'a' ~ 'z'
            if pyxel.btnp(key):
                self.input_text += chr(key).upper() if self.shift_mode else chr(key)

        # 数字 & 記号キーの入力
        for key, (normal_char, shift_char) in SYMBOL_KEYS[self.keyboard_mode].items():
            if pyxel.btnp(key):
                self.input_text += shift_char if self.shift_mode else normal_char

        # スペースキーの入力
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.input_text += " "

        # バックスペース対応
        if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.input_text:
            self.input_text = self.input_text[:-1]

        if text_before != self.input_text:
            pyxel.play(3, SFX_TYPE)

        # エンターキーで判定
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.input_text == self.word:
                self.score += 8 + len(self.word) * 2
                self.total_chars += len(self.word)
                pyxel.play(3, SFX_CORRECT)
            else:
                pyxel.play(3, SFX_WRONG)
            self.word = self.get_new_word()
            self.input_text = ""

    def update_gameover(self):
        """ゲームオーバー画面の処理"""
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.change_state(STATE_TITLE)

    def draw(self):
        """画面の描画処理"""
        pyxel.cls(0)
        if self.state == STATE_TITLE:
            self.draw_title()
        elif self.state == STATE_GAMEOVER:
            self.draw_gameover()
        else:
            self.draw_playing()

    def draw_title(self):
        """タイトル画面の描画"""
        pyxel.text(50, 30, "Typing Practice", pyxel.COLOR_WHITE)
        pyxel.text(46, 60, "Your Keyboard is?", pyxel.COLOR_WHITE)
        pyxel.text(60, 70, "1: JAPANESE", pyxel.COLOR_YELLOW)
        pyxel.text(60, 80, "2: ENGLISH", pyxel.COLOR_CYAN)

    def draw_playing(self):
        """画面の描画処理"""
        pyxel.cls(0)
        pyxel.text(40, 30, f"Word:  {self.word}", pyxel.COLOR_WHITE)
        pyxel.text(40, 40, f"Input: {self.input_text}", pyxel.COLOR_YELLOW)

        # カーソルを描画
        pyxel.rect(68 + len(self.input_text) * 4, 40, 3, 7, pyxel.COLOR_YELLOW)

        # スコア表示
        pyxel.text(64, 6, f"Score: {self.score}", pyxel.COLOR_GREEN)

        # 残り時間を強調表示（10秒以下で赤色）
        color = pyxel.COLOR_WHITE if self.timer > FAST_BGM_TIME else pyxel.COLOR_RED
        pyxel.text(64, 16, f"Time: {self.timer // 30}", color)

        # キーボードの描画
        self.draw_keyboard()

    def draw_gameover(self):
        """ゲームオーバー画面の描画"""
        pyxel.text(62, 30, "Game Over", pyxel.COLOR_WHITE)
        pyxel.text(44, 44, f"Score: {self.score:3}", pyxel.COLOR_YELLOW)
        pyxel.text(
            44, 54, f"Speed: {self.total_chars / 30:.2} char/sec", pyxel.COLOR_YELLOW
        )
        pyxel.text(42, 80, "Press SPACE to Retry", pyxel.COLOR_CYAN)

    def draw_keyboard(self):
        """キーボードの描画（通常モード / 記号モード）"""
        if self.input_text == self.word:
            next_letter = "\n"
        elif len(self.input_text) < len(self.word) and self.word.startswith(
            self.input_text
        ):
            next_letter = self.word[len(self.input_text)]
        else:
            next_letter = ""

        if self.shift_mode:
            layout = SYMBOL_LAYOUT[self.keyboard_mode]
            shift_letters = "".join(KEYBOARD_LAYOUT[self.keyboard_mode]).replace(
                " ", ""
            )
        else:
            layout = KEYBOARD_LAYOUT[self.keyboard_mode]
            shift_letters = "".join(SYMBOL_LAYOUT[self.keyboard_mode]).replace(" ", "")

        max_width = (
            max(*[len(row) * 11 + idx * 4 for idx, row in enumerate(layout)]) - 2
        )
        x_left = (pyxel.width - max_width) // 2
        x_right = x_left + max_width
        for row_idx, row in enumerate(layout):
            x_offset = x_left + (row_idx * 4)
            y_offset = 54 + row_idx * 13
            for col_idx, key in enumerate(row):
                if key == " ":
                    continue

                x, y = x_offset + col_idx * 11, y_offset
                color = pyxel.COLOR_GRAY

                # 現在の単語に含まれる文字をハイライト
                if key in self.word:
                    color = pyxel.COLOR_YELLOW

                # 次に入力するべき文字を強調
                if key == next_letter:
                    color = pyxel.COLOR_RED

                pyxel.rect(x, y, 9, 10, color)
                pyxel.text(x + 3, y + 2, key, pyxel.COLOR_WHITE)

        # シフトキー
        color = (
            pyxel.COLOR_RED
            if next_letter and next_letter in shift_letters
            else pyxel.COLOR_GRAY
        )
        pyxel.rect(x_left, 93, 21, 10, color)
        pyxel.rect(
            x_left + 12 + len(layout[3]) * 11,
            93,
            x_right - (x_left + 12 + len(layout[3]) * 11),
            10,
            color,
        )

        # スペースキー
        color = pyxel.COLOR_RED if next_letter == " " else pyxel.COLOR_GRAY
        pyxel.rect((pyxel.width - 80) // 2, 106, 80, 10, color)

        # エンターキー
        color = pyxel.COLOR_RED if next_letter == "\n" else pyxel.COLOR_GRAY
        if self.keyboard_mode == JIS_MODE:
            # L字型のエンターキー
            pyxel.rect(
                x_left + 4 + len(layout[1]) * 11,
                67,
                x_right - (x_left + 4 + len(layout[1]) * 11),
                10,
                color,
            )
            pyxel.rect(
                x_left + 8 + len(layout[2]) * 11,
                77,
                x_right - (x_left + 8 + len(layout[2]) * 11),
                13,
                color,
            )
        else:
            pyxel.rect(142, 80, 16, 10, color)

        # バックスペースキー
        color = pyxel.COLOR_RED if next_letter == "" else pyxel.COLOR_GRAY
        pyxel.rect(
            x_left + (len(layout[0]) - 1) * 11,
            54,
            x_right - (x_left + (len(layout[0]) - 1) * 11),
            10,
            color,
        )


if __name__ == "__main__":
    TypingGame()
