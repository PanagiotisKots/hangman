import tkinter as tk
from tkinter import messagebox
import random


class HangmanGameGUI:
    def __init__(self, root, word_list):
        """
        Initializes the Hangman game.
        - root: The Tkinter root window.
        - word_list: A list of possible words for the game.
        """
        self.root = root  # Tkinter root window
        self.word_list = word_list  # List of words for the game
        self.word_to_guess = ""  # The word the player needs to guess
        self.guessed_letters = set()  # Set of letters the player has guessed
        self.remaining_attempts = 6  # Number of attempts left before losing
        self.display_word = []  # The word being guessed, displayed with underscores
        self.hearts = ["❤️"] * self.remaining_attempts  # Hearts representing attempts
        self.timer_seconds = 60  # Timer for the game
        self.timer_running = False  # Flag to control the timer
        self.difficulty = "Medium"  # Default difficulty setting
        self.setup_menu()  # Set up the main menu

    def setup_menu(self):
        """Sets up the main menu with difficulty selection and exit options."""
        self.clear_window()  # Clear the window before displaying menu

        self.root.title("Hangman Game")  # Set window title
        self.root.geometry("800x600")  # Set window size

        # Title label
        title_label = tk.Label(self.root, text="Welcome to Hangman!", font=("Helvetica", 32, "bold"), pady=30)
        title_label.pack()

        # Difficulty selection buttons
        tk.Label(self.root, text="Choose Difficulty:", font=("Helvetica", 20)).pack(pady=20)
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack()

        # Buttons for selecting difficulty
        tk.Button(difficulty_frame, text="Easy", font=("Helvetica", 16), width=10,
                  command=lambda: self.start_game("Easy")).pack(side=tk.LEFT, padx=10)
        tk.Button(difficulty_frame, text="Medium", font=("Helvetica", 16), width=10,
                  command=lambda: self.start_game("Medium")).pack(side=tk.LEFT, padx=10)
        tk.Button(difficulty_frame, text="Hard", font=("Helvetica", 16), width=10,
                  command=lambda: self.start_game("Hard")).pack(side=tk.LEFT, padx=10)

        # Exit button
        tk.Button(self.root, text="Exit", font=("Helvetica", 16), width=10, command=self.root.quit).pack(pady=30)

        # Footer label
        footer_label = tk.Label(self.root, text="Made with ❤️ by Panagiotis Kotsorgios", font=("Helvetica", 12), fg="gray")
        footer_label.pack(side=tk.BOTTOM, pady=10)

    def start_game(self, difficulty="Medium"):
        """
        Starts a new game with the selected difficulty.
        - difficulty: The difficulty level chosen by the player.
        """
        self.difficulty = difficulty  # Set difficulty
        # Set difficulty-specific game parameters
        if difficulty == "Easy":
            self.remaining_attempts = 8
            self.timer_seconds = 300
        elif difficulty == "Hard":
            self.remaining_attempts = 4
            self.timer_seconds = 60
        else:
            self.remaining_attempts = 6
            self.timer_seconds = 180

        # Select a random word from the word list
        self.word_to_guess = random.choice(self.word_list).upper()
        self.guessed_letters = set()  # Reset guessed letters
        self.display_word = ["_" for _ in self.word_to_guess]  # Initialize the word to guess with underscores
        self.hearts = ["❤️"] * self.remaining_attempts  # Reset hearts for the remaining attempts
        self.timer_running = True  # Start the timer

        self.setup_game_gui()  # Set up the game screen

    def setup_game_gui(self):
        """Sets up the game screen after starting a new game."""
        self.clear_window()  # Clear the window before displaying the game screen

        self.root.title("Hangman Game")  # Set window title for game
        self.root.geometry("900x600")  # Set window size for game

        # Title frame
        title_frame = tk.Frame(self.root, relief=tk.RAISED, bd=2, bg="lightgray")
        title_frame.pack(fill=tk.X)

        # Title label
        tk.Label(title_frame, text="Hangman Game", font=("Helvetica", 28, "bold"), bg="lightgray").pack(pady=10)

        # Main game frame
        game_frame = tk.Frame(self.root, bg="white")
        game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Display the word with underscores and letters
        self.word_label = tk.Label(game_frame, text=" ".join(self.display_word), font=("Helvetica", 32), pady=20)
        self.word_label.grid(row=0, column=0, columnspan=2, sticky="w")

        # Display the number of lives (hearts)
        self.hearts_label = tk.Label(game_frame, text="Lives: " + "".join(self.hearts), font=("Helvetica", 16), fg="red")
        self.hearts_label.grid(row=1, column=0, sticky="w", pady=10)

        # Display the timer
        self.timer_label = tk.Label(game_frame, text=f"Time: {self.timer_seconds}s", font=("Helvetica", 16), fg="blue")
        self.timer_label.grid(row=1, column=1, sticky="e", pady=10)

        # Input frame for entering guesses
        self.input_frame = tk.Frame(game_frame)
        self.input_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")
        tk.Label(self.input_frame, text="Enter a letter:", font=("Helvetica", 16)).pack(side=tk.LEFT)
        self.input_entry = tk.Entry(self.input_frame, font=("Helvetica", 16), width=5)
        self.input_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(self.input_frame, text="Guess", font=("Helvetica", 16), command=self.make_guess).pack(side=tk.LEFT)

        # Guessed letters display
        self.guessed_label = tk.Label(game_frame, text="Guessed letters: ", font=("Helvetica", 14))
        self.guessed_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")

        # Buttons for restarting or going to the main menu
        tk.Button(game_frame, text="Restart", font=("Helvetica", 14),
                  command=lambda: self.start_game(self.difficulty)).grid(row=4, column=0, pady=20, sticky="w")
        tk.Button(game_frame, text="Main Menu", font=("Helvetica", 14), command=self.setup_menu).grid(row=4, column=1,
                                                                                                      pady=20,
                                                                                                      sticky="e")

        # Canvas for drawing the hangman scaffold and figure
        self.canvas_frame = tk.Frame(self.root, relief=tk.SUNKEN, bd=2, bg="white")
        self.canvas_frame.place(x=630, y=100, width=250, height=350)

        self.canvas = tk.Canvas(self.canvas_frame, width=250, height=300, bg="white", highlightthickness=0)
        self.canvas.pack()
        self.draw_base()  # Draw the scaffold base

        self.update_timer()  # Start the timer updates

    def draw_base(self):
        """Draws the hangman scaffold on the canvas."""
        self.canvas.delete("all")  # Clear the canvas
        self.canvas.create_line(50, 280, 200, 280, width=2)  # Base line
        self.canvas.create_line(125, 280, 125, 50, width=2)  # Vertical pole
        self.canvas.create_line(125, 50, 200, 50, width=2)   # Beam
        self.canvas.create_line(200, 50, 200, 80, width=2)   # Rope

    def draw_hangman(self):
        """Draws parts of the hangman based on remaining attempts."""
        parts = [
            lambda: self.canvas.create_oval(180, 80, 220, 120, width=2),  # Head
            lambda: self.canvas.create_line(200, 120, 200, 200, width=2),  # Body
            lambda: self.canvas.create_line(200, 140, 180, 170, width=2),  # Left arm
            lambda: self.canvas.create_line(200, 140, 220, 170, width=2),  # Right arm
            lambda: self.canvas.create_line(200, 200, 180, 250, width=2),  # Left leg
            lambda: self.canvas.create_line(200, 200, 220, 250, width=2),  # Right leg
        ]
        if 6 - self.remaining_attempts <= len(parts):
            parts[6 - self.remaining_attempts - 1]()  # Draw the next part of the hangman figure

    def draw_fire(self):
        """Draws fire under the hangman if the player loses."""
        colors = ["red", "orange", "yellow"]
        for i in range(3):
            self.canvas.create_oval(150 - i * 5, 280 - i * 5, 250 + i * 5, 290 + i * 10, fill=colors[i], outline="")

    def update_word_display(self):
        """Updates the displayed word with guessed letters."""
        self.word_label.config(text=" ".join(self.display_word))

    def update_hearts_display(self):
        """Updates the hearts display based on remaining attempts."""
        self.hearts_label.config(text="Lives: " + "".join(self.hearts))

    def update_guessed_letters(self):
        """Updates the guessed letters display."""
        self.guessed_label.config(
            text=f"Guessed letters: {', '.join(sorted(self.guessed_letters))}"
        )

    def make_guess(self):
        """
        Processes the player's guess and updates game state.
        - Checks if the guess is valid, updates word display, and handles correct/incorrect guesses.
        """
        guess = self.input_entry.get().upper()  # Get the player's guess
        self.input_entry.delete(0, tk.END)  # Clear the input field

        if not guess.isalpha() or len(guess) != 1:
            messagebox.showerror("Invalid Input", "Please enter a single alphabetical letter.")  # Validate input
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Already Guessed", f"You already guessed '{guess}'.")  # Warn if letter was guessed
            return

        self.guessed_letters.add(guess)  # Add the guess to the set of guessed letters

        if guess in self.word_to_guess:
            # Update the display word with correct guesses
            for idx, letter in enumerate(self.word_to_guess):
                if letter == guess:
                    self.display_word[idx] = guess
            self.update_word_display()

            if "_" not in self.display_word:
                self.end_game(won=True)  # End game if all letters are guessed correctly
        else:
            self.remaining_attempts -= 1  # Decrease remaining attempts for incorrect guesses
            self.hearts.pop()  # Remove a heart
            self.update_hearts_display()  # Update hearts display
            self.draw_hangman()  # Draw the next part of the hangman

            if self.remaining_attempts == 0:
                self.end_game(won=False)  # End game if the player runs out of attempts

        self.update_guessed_letters()  # Update the guessed letters display

    def update_timer(self):
        """Updates the game timer each second."""
        if self.timer_running:
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.timer_label.config(text=f"Time: {self.timer_seconds}s")
                self.root.after(1000, self.update_timer)  # Update every second
            else:
                self.end_game(won=False, time_up=True)  # End game if time is up

    def end_game(self, won, time_up=False):
        """Ends the game and displays the result message."""
        self.timer_running = False  # Stop the timer
        if won:
            messagebox.showinfo("Game Over", f"Congratulations! You guessed the word: {self.word_to_guess}")
        elif time_up:
            messagebox.showerror("Game Over", f"Time's up! The word was: {self.word_to_guess}")
        else:
            self.draw_fire()  # Draw fire if the player loses
            messagebox.showerror("Game Over", f"You lost. The word was: {self.word_to_guess}")
        self.setup_menu()  # Go back to the main menu

    def clear_window(self):
        """Clears all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    # List of words to be used in the game
    word_list = ["Python", "Hangman", "Programming", "Development", "Challenge"]
    root = tk.Tk()  # Create the Tkinter window
    game = HangmanGameGUI(root, word_list)  # Instantiate the Hangman game
    root.mainloop()  # Start the Tkinter main event loop
