import turtle
import random
import time

# Game settings
delay = 0.1
score = 0
high_score = 0
food_toggle = False
game_started = False
is_paused = False

# Create screen
screen = turtle.Screen()
screen.title("Snake Game")
screen.bgcolor("#0a0a0a")
screen.setup(width=600, height=600)
screen.tracer(0)

# Grid
grid = turtle.Turtle()
grid.speed(0)
grid.color("#3b4705")
grid.penup()

for x in range(-300, 301, 20):
    grid.goto(x, -300)
    grid.pendown()
    grid.goto(x, 300)
    grid.penup()

for y in range(-300, 301, 20):
    grid.goto(-300, y)
    grid.pendown()
    grid.goto(300, y)
    grid.penup()

grid.hideturtle()

# Border
border = turtle.Turtle()
border.speed(0)
border.color("#3b4705")
border.pensize(3)
border.penup()
border.goto(-300, -300)
border.pendown()

for _ in range(4):
    border.forward(600)
    border.left(90)

border.hideturtle()

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#00ff41")
head.penup()
head.goto(0, 0)
head.direction = "stop"

eye_left = turtle.Turtle()
eye_left.speed(0)
eye_left.shape("circle")
eye_left.color("#0a0a0a")
eye_left.penup()
eye_left.shapesize(0.2)
eye_left.hideturtle()

eye_right = turtle.Turtle()
eye_right.speed(0)
eye_right.shape("circle")
eye_right.color("#0a0a0a")
eye_right.penup()
eye_right.shapesize(0.2)
eye_right.hideturtle()

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#ff3131")
food.penup()
food.goto(0, 100)

# Scoreboard
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write(
    "Score: 0  High Score: 0",
    align="center",
    font=("Courier", 24, "bold")
)

# Start screen message
message = turtle.Turtle()
message.speed(0)
message.color("white")
message.penup()
message.hideturtle()
message.goto(0, 50)
message.write("S N A K E", align="center", font=("Courier", 36, "bold"))
message.goto(0, -40)
message.write("Press SPACE to Start", align="center", font=("Courier", 18, "normal"))

# Game over turtle
gameover = turtle.Turtle()
gameover.speed(0)
gameover.color("#00ff41")
gameover.penup()
gameover.hideturtle()

# ── Pause overlay turtles ──────────────────────────────────────────────────────

# The dark filled box behind the popup
pause_box = turtle.Turtle()
pause_box.speed(0)
pause_box.penup()
pause_box.hideturtle()

# Text inside the popup (heading + hint)
pause_text = turtle.Turtle()
pause_text.speed(0)
pause_text.color("#00ff41")
pause_text.penup()
pause_text.hideturtle()

# "Resume" button box
resume_btn = turtle.Turtle()
resume_btn.speed(0)
resume_btn.penup()
resume_btn.hideturtle()

# "Resume" button label
resume_label = turtle.Turtle()
resume_label.speed(0)
resume_label.color("#0a0a0a")
resume_label.penup()
resume_label.hideturtle()

# "Restart" button box
restart_btn = turtle.Turtle()
restart_btn.speed(0)
restart_btn.penup()
restart_btn.hideturtle()

# "Restart" button label
restart_label = turtle.Turtle()
restart_label.speed(0)
restart_label.color("#0a0a0a")
restart_label.penup()
restart_label.hideturtle()

# ── Helper: draw a filled rectangle ───────────────────────────────────────────
def draw_filled_rect(t, x, y, w, h, fill, outline):
    """Draw a filled rectangle. (x, y) is the bottom-left corner."""
    t.color(outline, fill)
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.begin_fill()
    for _ in range(2):
        t.forward(w)
        t.left(90)
        t.forward(h)
        t.left(90)
    t.end_fill()
    t.penup()

# ── Show / hide pause popup 
def show_pause_popup():
    px, py, pw, ph = -160, -120, 320, 240

    draw_filled_rect(pause_box, px, py, pw, ph, "#0d1a0d", "#00ff41")
    pause_box.pensize(2)

    pause_text.goto(0, 80)
    pause_text.write("PAUSED", align="center", font=("Courier", 28, "bold"))

    pause_text.goto(0, 40)
    pause_text.color("#3b4705")
    pause_text.write("─" * 28, align="center", font=("Courier", 10, "normal"))
    pause_text.color("#00ff41")

    # Resume button  (centred at y=10)
    draw_filled_rect(resume_btn, -90, -10, 180, 36, "#00ff41", "#00ff41")
    resume_label.goto(0, -4)
    resume_label.write("  Resume  (P)", align="center", font=("Courier", 14, "bold"))

    # Restart button (centred at y=-60)
    draw_filled_rect(restart_btn, -90, -80, 180, 36, "#1a3d1a", "#00ff41")
    restart_label.color("#00ff41")
    restart_label.goto(0, -74)
    restart_label.write("  Restart  (R)", align="center", font=("Courier", 14, "bold"))

    # Keyboard hint at the bottom
    pause_text.goto(0, -105)
    pause_text.color("#3b4705")
    pause_text.write("P = resume   R = restart", align="center", font=("Courier", 10, "normal"))

     # Check Head & Eyes
    if -160 <= head.xcor() <= 160 and -120 <= head.ycor() <= 120:
        head.hideturtle()
        eye_left.hideturtle()
        eye_right.hideturtle()

    # Check Food
    if -160 <= food.xcor() <= 160 and -120 <= food.ycor() <= 120:
        food.hideturtle()

    # Check Body Segments
    for seg in segments:
        if -160 <= seg.xcor() <= 160 and -120 <= seg.ycor() <= 120:
            seg.hideturtle()

def hide_pause_popup():
    pause_box.clear()
    pause_text.clear()
    resume_btn.clear()
    resume_label.clear()
    restart_btn.clear()
    restart_label.clear()

    head.showturtle()
    eye_left.showturtle()
    eye_right.showturtle()
    food.showturtle()
    for seg in segments:
        seg.showturtle()

# ── Snake body segments ────────────────────────────────────────────────────────
segments = []

offsets = {
    "up":    [(-4, 6),  (4, 6)],
    "down":  [(-4, -6), (4, -6)],
    "left":  [(-6, 4),  (-6, -4)],
    "right": [(6, 4),   (6, -4)],
    "stop":  [(-4, 4),  (4, 4)],
}

def get_segment_color(index):
    colors = ["#00e63a", "#00cc33", "#00b32d", "#009926", "#008020", "#006619", "#004d13"]
    if index >= len(colors):
        return "#004d13"
    return colors[index]

def reset_game():
    global score, game_started, is_paused

    hide_pause_popup()
    game_started = False
    is_paused = False

    head.goto(0, 0)
    head.direction = "stop"
    head.hideturtle()
    food.hideturtle()
    eye_left.hideturtle()
    eye_right.hideturtle()

    for seg in segments:
        seg.goto(1000, 1000)
    segments.clear()

    score = 0
    pen.clear()
    pen.write(
        f"Score: {score}  High Score: {high_score}",
        align="center",
        font=("Courier", 24, "bold")
    )

    gameover.clear()
    gameover.goto(0, 40)
    gameover.write("GAME OVER", align="center", font=("Courier", 36, "bold"))
    gameover.goto(0, -20)
    gameover.write("Press SPACE to Restart", align="center", font=("Courier", 16, "normal"))

# ── Movement ───────────────────────────────────────────────────────────────────
def go_up():
    if head.direction != "down" and not is_paused:
        head.direction = "up"

def go_down():
    if head.direction != "up" and not is_paused:
        head.direction = "down"

def go_left():
    if head.direction != "right" and not is_paused:
        head.direction = "left"

def go_right():
    if head.direction != "left" and not is_paused:
        head.direction = "right"

def move():
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)

def start_game():
    global game_started, is_paused
    if not game_started:
        game_started = True
        is_paused = False
        gameover.clear()
        message.clear()
        head.showturtle()
        food.showturtle()
        pen.clear()
        pen.write(
            f"Score: {score}  High Score: {high_score}",
            align="center",
            font=("Courier", 24, "bold")
        )

def toggle_pause():
    global is_paused
    if game_started:
        is_paused = not is_paused
        if is_paused:
            show_pause_popup()
        else:
            hide_pause_popup()

def restart_from_pause():
    """R key — works only while paused."""
    if is_paused:
        reset_game()

# ── Initial state ──────────────────────────────────────────────────────────────
head.hideturtle()
food.hideturtle()
pen.clear()
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "bold"))

# ── Keyboard bindings ──────────────────────────────────────────────────────────
screen.listen()
screen.onkeypress(go_up, "w")
screen.onkeypress(go_down, "s")
screen.onkeypress(go_left, "a")
screen.onkeypress(go_right, "d")
screen.onkeypress(start_game, "space")
screen.onkeypress(toggle_pause, "p")
screen.onkeypress(restart_from_pause, "r")

# ── Main game loop ─────────────────────────────────────────────────────────────
while True:
    screen.update()

    # Food pulse (runs even while paused so it doesn't freeze weirdly)
    food_toggle = not food_toggle
    food.shapesize(0.8 if food_toggle else 1.1)

    if game_started and not is_paused:

        # Wall collision
        if (
            head.xcor() > 290
            or head.xcor() < -290
            or head.ycor() > 290
            or head.ycor() < -290
        ):
            reset_game()
            time.sleep(delay)
            continue

        # Food collision
        if head.distance(food) < 20:
            x = random.randint(-270, 270)
            y = random.randint(-270, 270)
            food.goto(x, y)

            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.penup()
            segments.append(new_segment)

            for i, seg in enumerate(segments):
                seg.color(get_segment_color(i))

            score += 10
            if score > high_score:
                high_score = score

            pen.clear()
            pen.write(
                f"Score: {score}  High Score: {high_score}",
                align="center",
                font=("Courier", 24, "bold")
            )

        # Move body segments
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        # Move head
        move()

        # Update eyes
        positions = offsets.get(head.direction, offsets["stop"])
        eye_left.goto(head.xcor() + positions[0][0], head.ycor() + positions[0][1])
        eye_right.goto(head.xcor() + positions[1][0], head.ycor() + positions[1][1])
        eye_left.showturtle()
        eye_right.showturtle()

        # Self collision
        for segment in segments:
            if segment.distance(head) < 20:
                reset_game()
                break

        time.sleep(delay)

    else:
        time.sleep(0.05)