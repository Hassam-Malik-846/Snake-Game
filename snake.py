import tkinter as tk
from tkinter import messagebox
import random

# Game Constants
WIDTH = 600
HEIGHT = 400
SNAKE_SIZE = 20
SPEED = 100 # Lower is faster (milliseconds)

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game By Hassam")
        
        # Game Variables
        self.name = ""
        self.score = 0
        self.direction = "Right"
        self.snake = [(100, 100), (80, 100), (60, 100)] # List of coordinates
        self.food = None
        self.running = False

        self.setup_menu()

    def setup_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="SNAKE GAME", font=("Arial", 30, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="Enter Name:").pack()
        self.name_entry = tk.Entry(self.root, font=("Arial", 14))
        self.name_entry.pack(pady=10)
        
        tk.Button(self.root, text="START", command=self.start_game, bg="green", fg="white", width=15).pack(pady=5)
        tk.Button(self.root, text="VIEW LEADERBOARD", command=self.show_leaderboard, width=15).pack(pady=5)

    def start_game(self):
        self.name = self.name_entry.get() or "Player 1"
        self.score = 0
        self.direction = "Right"
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.running = True
        
        self.clear_screen()
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        
        # Bind Keys
        self.root.bind("<KeyPress>", self.change_direction)
        
        self.create_food()
        self.update_game()

    def create_food(self):
        x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        self.food = (x, y)

    def change_direction(self, event):
        key = event.keysym
        # Prevent 180-degree turns
        if key == "Up" and self.direction != "Down": self.direction = "Up"
        if key == "Down" and self.direction != "Up": self.direction = "Down"
        if key == "Left" and self.direction != "Right": self.direction = "Left"
        if key == "Right" and self.direction != "Left": self.direction = "Right"

    def update_game(self):
        if not self.running: return

        # 1. Calculate New Head
        head_x, head_y = self.snake[0]
        if self.direction == "Up": head_y -= SNAKE_SIZE
        if self.direction == "Down": head_y += SNAKE_SIZE
        if self.direction == "Left": head_x -= SNAKE_SIZE
        if self.direction == "Right": head_x += SNAKE_SIZE
        
        new_head = (head_x, head_y)

        # 2. Check Collisions (Wall or Self)
        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # 3. Check Food
        if new_head == self.food:
            self.score += 10
            self.create_food()
        else:
            self.snake.pop() # Remove tail

        self.draw()
        self.root.after(SPEED, self.update_game) # The "Loop"

    def draw(self):
        self.canvas.delete("all")
        # Draw Food
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0]+SNAKE_SIZE, self.food[1]+SNAKE_SIZE, fill="red")
        # Draw Snake
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+SNAKE_SIZE, y+SNAKE_SIZE, fill="green", outline="white")
        # Draw Score
        self.canvas.create_text(50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 10))

    def game_over(self):
        self.running = False
        self.save_score()
        messagebox.showinfo("Game Over", f"Hard Luck, {self.name}!\nYour Score: {self.score}")
        self.setup_menu()

    def save_score(self):
        with open("Snake_Leaderboard.txt", "a") as f:
            f.write(f"Player: {self.name} | Score: {self.score}\n")

    def show_leaderboard(self):
        try:
            with open("Snake_Leaderboard.txt", "r") as f:
                content = f.read()
            
            lb_window = tk.Toplevel(self.root)
            lb_window.title("Leaderboard")
            text = tk.Text(lb_window)
            text.insert("1.0", content if content else "No scores yet!")
            text.pack()
        except FileNotFoundError:
            messagebox.showinfo("Error", "No leaderboard file found yet.")

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()