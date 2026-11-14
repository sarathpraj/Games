"""
19 - Snake Game
===============
The classic: eat the food, grow longer, don't hit the walls or yourself.
Built with turtle, which comes with Python (nothing to install).

Controls: arrow keys or W A S D. Space = pause.

Concepts you'll practise:
  - A GAME LOOP: update -> draw -> wait -> repeat (screen.ontimer)
  - Turning off auto-drawing (tracer(0)) and calling update() ourselves for smooth motion
  - Keyboard events with onkeypress
  - A list of turtles as the snake's body. Each step, every segment moves to
    where the segment in front of it used to be.
  - Collision detection with .distance()
  - A class that keeps the whole game's state together

Run:  python 19_snake_game.py

Challenges:
  1. Save the high score to a file so it survives restarts.
  2. Add "golden food" worth 50 points that disappears after 5 seconds.
  3. Let the snake wrap around the edges instead of dying.
"""
import random
import turtle

WIDTH = HEIGHT = 600
CELL = 20                     # one grid square, in pixels
START_DELAY = 120             # milliseconds between moves (lower = faster)
MIN_DELAY = 50
LIMIT = WIDTH // 2 - CELL     # furthest the head can go from the centre (280)

MOVES = {"up": (0, CELL), "down": (0, -CELL), "left": (-CELL, 0), "right": (CELL, 0)}
OPPOSITE = {"up": "down", "down": "up", "left": "right", "right": "left"}
KEYS = [("Up", "up"), ("w", "up"), ("Down", "down"), ("s", "down"),
        ("Left", "left"), ("a", "left"), ("Right", "right"), ("d", "right")]


def make_turtle(shape, colour):
    t = turtle.Turtle(shape)
    t.color(colour)
    t.penup()          # don't draw lines when moving
    t.speed(0)
    return t


class SnakeGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Snake")
        self.screen.bgcolor("black")
        self.screen.setup(WIDTH + 40, HEIGHT + 80)
        self.screen.tracer(0)                # we'll call update() ourselves

        self.head = make_turtle("square", "lime")
        self.food = make_turtle("circle", "red")
        self.pen = make_turtle("square", "white")
        self.pen.hideturtle()
        self.body = []
        self.high_score = 0

        self.draw_border()
        self.bind_keys()
        self.reset("Press an arrow key to start")

    # ---------- setup ----------
    def draw_border(self):
        border = make_turtle("classic", "gray")
        border.hideturtle()
        edge = LIMIT + CELL // 2
        border.goto(-edge, -edge)
        border.pendown()
        for x, y in [(edge, -edge), (edge, edge), (-edge, edge), (-edge, -edge)]:
            border.goto(x, y)

    def bind_keys(self):
        self.screen.listen()
        for key, direction in KEYS:
            self.screen.onkeypress(lambda d=direction: self.change_direction(d), key)
        self.screen.onkeypress(self.toggle_pause, "space")

    def reset(self, message):
        for segment in self.body:
            segment.hideturtle()
        self.body = []
        self.head.goto(0, 0)
        self.direction = "stop"
        self.next_direction = "stop"
        self.score = 0
        self.delay = START_DELAY
        self.paused = False
        self.place_food()
        self.draw_text(message)

    # ---------- controls ----------
    def change_direction(self, new_direction):
        if self.direction == "stop":
            self.draw_text()                 # clear the "press a key" message
        if new_direction != OPPOSITE.get(self.direction):   # no 180-degree turns
            self.next_direction = new_direction

    def toggle_pause(self):
        self.paused = not self.paused
        self.draw_text("Paused" if self.paused else None)

    # ---------- drawing ----------
    def draw_text(self, message=None):
        self.pen.clear()
        self.pen.goto(0, HEIGHT // 2 + 2)
        self.pen.write(f"Score: {self.score}    High score: {self.high_score}",
                       align="center", font=("Courier", 16, "bold"))
        if message:
            self.pen.goto(0, 60)
            self.pen.write(message, align="center", font=("Courier", 18, "normal"))

    def place_food(self):
        while True:
            x = random.randint(-LIMIT // CELL, LIMIT // CELL) * CELL
            y = random.randint(-LIMIT // CELL, LIMIT // CELL) * CELL
            on_snake = self.head.distance(x, y) < 1 or any(
                segment.distance(x, y) < 1 for segment in self.body)
            if not on_snake:
                self.food.goto(x, y)
                return

    # ---------- the game loop ----------
    def tick(self):
        if not self.paused and self.next_direction != "stop":
            self.direction = self.next_direction
            self.step()
        self.screen.update()                           # draw everything once
        self.screen.ontimer(self.tick, self.delay)     # ...and come back soon

    def step(self):
        # 1. Move the body, starting from the tail
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].goto(self.body[i - 1].position())
        if self.body:
            self.body[0].goto(self.head.position())

        # 2. Move the head
        dx, dy = MOVES[self.direction]
        self.head.goto(self.head.xcor() + dx, self.head.ycor() + dy)

        # 3. Crashed into a wall or into ourselves?
        hit_wall = abs(self.head.xcor()) > LIMIT or abs(self.head.ycor()) > LIMIT
        hit_self = any(segment.distance(self.head) < CELL / 2 for segment in self.body)
        if hit_wall or hit_self:
            self.reset(f"Game over! You scored {self.score}. Press an arrow key.")
            return

        # 4. Eaten the food?
        if self.head.distance(self.food) < CELL / 2:
            tail = self.body[-1] if self.body else self.head
            segment = make_turtle("square", "green")
            segment.goto(tail.position())
            self.body.append(segment)

            self.score += 10
            self.high_score = max(self.high_score, self.score)
            self.delay = max(MIN_DELAY, self.delay - 3)   # speed up a little
            self.place_food()
            self.draw_text()

    def run(self):
        self.tick()
        self.screen.mainloop()


if __name__ == "__main__":
    SnakeGame().run()
