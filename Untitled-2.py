from tkinter import*
import random

# глобальні перемінні
# настройки вікна 

# Ширина
WIDTH = 1000
# Висота
HEIGHT = 500

# Настройки ракеток

# Ширина ракетки
PAD_WIDTH = 10
# Висота ракетки
PAD_HEIGH = 100

# Настройки мяча
# наскільки буде зільшуватись скоріть після відбиття мяча
BALL_SPEED_UP = 1
# Максимальна скорість мяча
BALL_SPEED_MAX = 30
# Радіус мяча
BALL_RADIUS = 30

# Начальна скорість
SPEED_INITIAL = 8
BALL_SPEED_X = SPEED_INITIAL
BALL_SPEED_Y = SPEED_INITIAL

# Счотчик гравців
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0

right_line_distance = WIDTH - PAD_WIDTH

# оновлення счотчика
def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "right":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)

# Спавн мячика

def spawn_ball():
    global BALL_SPEED_X
    # иставляєм мяч по центру
    c.coords(BALL, WIDTH/2-BALL_RADIUS/2,
             HEIGHT/2-BALL_RADIUS/2,
             WIDTH/2+BALL_RADIUS/2,
             HEIGHT/2+BALL_RADIUS/2)
    # задаєм мячу напрвлення в чторону програвшого
    BALL_SPEED_X = -(BALL_SPEED_X * -SPEED_INITIAL) / abs(BALL_SPEED_X)

# функція відскока мяча
def bounce(action):
    global BALL_SPEED_X, BALL_SPEED_Y
    # вдарили ракеткою
    if action == "strike":
        BALL_SPEED_Y = random.randrange(-10, 10)
        if abs(BALL_SPEED_X) < BALL_SPEED_MAX:
            BALL_SPEED_X *= -BALL_SPEED_UP
        else:
            BALL_SPEED_X = -BALL_SPEED_X
    else:
        BALL_SPEED_Y = -BALL_SPEED_Y

# вікно
root = Tk()
root.title("PING PONG v1.1")

# анімації
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#03ff89")
c.pack()

# Элементи поля

# Права лінія
c.create_line(WIDTH-PAD_WIDTH, 0, WIDTH-PAD_WIDTH, HEIGHT, fill="black")

# Ліва лінія
c.create_line(PAD_WIDTH, 0, PAD_WIDTH, HEIGHT, fill="black")

# центральна лянія
c.create_line(WIDTH/2, 0, #(x;y) верхнии
              WIDTH/2, HEIGHT, #(x;y) нижнии
              fill="white")

# Dcnfyjdrf обєктів

# Мяч
BALL = c.create_oval(WIDTH/2-BALL_RADIUS/2, HEIGHT/2-BALL_RADIUS/2, WIDTH/2+BALL_RADIUS/2, HEIGHT/2+BALL_RADIUS/2, fill="white")

# Права ракетка
RIGHT_PAD = c.create_line(WIDTH-PAD_WIDTH/2, 0, WIDTH-PAD_WIDTH/2, PAD_HEIGH, width=PAD_WIDTH, fill="black")

# Ліва ракетка
LEFT_PAD = c.create_line(PAD_WIDTH/2, 0, PAD_WIDTH/2, PAD_HEIGH, width=PAD_WIDTH, fill="black")

# Счот 1 гравця
p_1_text = c.create_text(WIDTH-WIDTH/6, PAD_HEIGH/4,
                         text=PLAYER_1_SCORE,
                         font="Arial 18",
                         fill="white")

# Счот 2 гравця
p_2_text = c.create_text(WIDTH/6, PAD_HEIGH/4,
                          text=PLAYER_2_SCORE,
                          font="Arial 18",
                          fill="white")

# Скорість мячика
# По горизонталі
BALL_CHANGE_X = 15
# По вертикалі
BALL_CHANGE_Y = 0

def move_ball():
    # Кординати мячика
    ball_left, ball_top, ball_right, ball_bot = c.coords(BALL)
    ball_center = (ball_top + ball_bot) / 2

    # вертикальний відскок
    if ball_right + BALL_SPEED_X < right_line_distance and ball_left + BALL_SPEED_X > PAD_WIDTH:
        c.move(BALL, BALL_SPEED_X, BALL_SPEED_Y)
    # Якщо мяч торкається границь
    elif ball_right == right_line_distance or ball_left == PAD_WIDTH:
        if ball_right > WIDTH / 2:
            if c.coords(RIGHT_PAD)[1] < ball_center < c.coords(RIGHT_PAD)[3]:
                bounce("strike")
            else:
                update_score("left")
                spawn_ball()
        else:
            # те саме і для лівого
            if c.coords(LEFT_PAD)[1] < ball_center < c.coords(LEFT_PAD)[3]:
                bounce("strike")
            else:
                update_score("right")
                spawn_ball()
    # Мячик до центру
    else:
        if ball_right > WIDTH / 2:
            c.move(BALL, right_line_distance-ball_right, BALL_SPEED_Y)
        else:
            c.move(BALL, -ball_left+PAD_WIDTH, BALL_SPEED_Y)
    # горизонтальний відскок
    if ball_top + BALL_SPEED_Y < 0 or ball_bot + BALL_SPEED_Y > HEIGHT:
        bounce("ricochet")


# скорості ракетки
# скорось з якою їздить
PAD_SPEED = 30
# Скорость правої
RIGHT_PAD_SPEED = 0
# Скорость левої
LEFT_PAD_SPEED = 0

# Функція обох ракеток
def move_pads():
    PADS = {LEFT_PAD: LEFT_PAD_SPEED, RIGHT_PAD: RIGHT_PAD_SPEED}
    # Ракетки
    for pad in PADS:
        # двігаєм ракетку з оприділеною скорістю
        c.move(pad, 0, PADS[pad])
        # якщо какетка вилазить за поле вертаєм на місце
        if c.coords(pad)[1] < 0:
            c.move(pad, 0, -c.coords(pad)[1])
        elif c.coords(pad)[3] > HEIGHT:
            c.move(pad, 0, HEIGHT - c.coords(pad)[3])
#вийграш або пройграш
def main():
    move_ball()
    move_pads()
    if (PLAYER_1_SCORE < 10) and (PLAYER_2_SCORE < 10):
        # вИЗИВАЄМ САМОГО СЕБЕ КОЖНІ 30 МЛ
        root.after(30, main)
    else:
        text=''
        if PLAYER_1_SCORE > PLAYER_2_SCORE:
            text='Вийграв правий грвець'
        else:
            text='Вийграв лівий гравець'
        c.create_text(WIDTH / 2, PAD_HEIGH / 2,
                         text=text,
                         font='Arial 40',
                         fill='green')

# Реагування на клавіші
c.focus_set()

# Функція обробки клавіш
def movement_handler(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym == "w":
        LEFT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "s":
        LEFT_PAD_SPEED = PAD_SPEED
    elif event.keysym == "Up":
        RIGHT_PAD_SPEED = -PAD_SPEED
    elif event.keysym == "Down":
        RIGHT_PAD_SPEED = PAD_SPEED

# Привязка до Canvas функцію
c.bind("<KeyPress>", movement_handler)

# Функція реагування на відпускання клавіш
def stop_pad(event):
    global LEFT_PAD_SPEED, RIGHT_PAD_SPEED
    if event.keysym in ("w", "s"):
        LEFT_PAD_SPEED = 0
    elif event.keysym in ("Up", "Down"):
        RIGHT_PAD_SPEED = 0

# Привязка до Canvas функції
c.bind("<KeyRelease>", stop_pad)

# запускаю двіженія
main()

# запускаю вікно
root.mainloop()