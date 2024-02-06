import tkinter as tk
from tkinter import messagebox
import random

class Bankroll:
    def __init__(self):
        self.amount = 1000
        self.chips = {'$1': 1, '$5': 5, '$10': 10, '$25': 25, '$50': 50, '$100': 100, '$500': 500, '$1000': 1000}

class BlackjackLogic:
    def __init__(self):
        self.cards = [{'rank': str(i), 'suit': suit} for i in range(2, 11) for suit in ['Clubs', 'Spades', 'Diamonds', 'Hearts']]
        self.cards += [{'rank': '10', 'suit': suit} for suit in ['Clubs', 'Spades', 'Diamonds', 'Hearts']] * 3
        self.cards += [{'rank': 'J', 'suit': suit} for suit in ['Clubs', 'Spades', 'Diamonds', 'Hearts']] * 4
        self.cards += [{'rank': 'Q', 'suit': suit} for suit in ['Clubs', 'Spades', 'Diamonds', 'Hearts']] * 4
        self.cards += [{'rank': 'K', 'suit': suit} for suit in ['Clubs', 'Spades', 'Diamonds', 'Hearts']] * 4
        self.cards += [{'rank': 'A', 'suit': suit} for suit in ['Clubs', 'Spades', 'Diamonds', 'Hearts']] * 4
        self.shoe = self.cards * 4
        random.shuffle(self.shoe)

    def deal_card(self, hand):
        card = self.shoe.pop()
        hand.append(card)

    def calculate_hand_value(self, hand):
        values = [card_value(card['rank']) for card in hand]
        num_aces = values.count(11)

        while sum(values) > 21 and num_aces:
            values.remove(11)
            values.append(1)
            num_aces -= 1

        return sum(values)

def card_value(rank):
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

class InteractiveGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")
        self.bankroll = Bankroll()
        self.blackjack_logic = BlackjackLogic()
        self.current_bet = tk.IntVar()
        self.player_hand = []
        self.dealer_hand = []
        self.split_hands = []
        self.result_delay = 1000
        self.show_dealer_down_card = False
        self.stand_hand_1_button = None
        self.stand_hand_2_button = None

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="green")
        self.canvas.pack()

        self.create_widgets()

    def create_widgets(self):
        self.draw_poker_chips()

        self.play_button = tk.Button(self.root, text="Play", command=self.play_button_click)
        self.play_button.pack()

        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit_button_click)
        self.hit_button.pack()

        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand_button_click, state=tk.DISABLED)
        self.stand_button.pack()

        self.double_button = tk.Button(self.root, text="Double", command=self.double_button_click, state=tk.DISABLED)
        self.double_button.pack()

        self.split_button = tk.Button(self.root, text="Split", command=self.split_button_click, state=tk.DISABLED)
        self.split_button.pack()

        self.stand_hand_1_button = tk.Button(self.root, text="Stand on Split Hand 1", command=self.stand_hand_1_button_click, state=tk.DISABLED)
        self.stand_hand_1_button.pack()

        self.stand_hand_2_button = tk.Button(self.root, text="Stand on Split Hand 2", command=self.stand_hand_2_button_click, state=tk.DISABLED)
        self.stand_hand_2_button.pack()

        self.clear_bet_button = tk.Button(self.root, text="Clear Bet", command=self.clear_bet_button_click)
        self.clear_bet_button.pack()

    def draw_poker_chips(self):
        chip_positions = {'$1': (50, 550), '$5': (120, 550), '$10': (190, 550),
                          '$25': (260, 550), '$50': (330, 550), '$100': (400, 550),
                          '$500': (470, 550), '$1000': (540, 550)}

        for chip_value, position in chip_positions.items():
            chip_button = tk.Button(self.root, text=chip_value,
                                    command=lambda value=self.bankroll.chips[chip_value]: self.add_bet(value))
            chip_button.place(x=position[0], y=position[1])

    def add_bet(self, value):
        if self.bankroll.amount >= value:
            self.current_bet.set(self.current_bet.get() + value)
            self.bankroll.amount -= value
            self.update_display()
            self.draw_poker_chips()
        else:
            messagebox.showinfo("Error", "Insufficient funds!")

    def reset_bet(self):
        self.bankroll.amount += self.current_bet.get()
        self.current_bet.set(0)
        self.update_display()

    def clear_bet_button_click(self):
        self.reset_bet()

    def update_display(self):
        self.canvas.delete("all")
        self.draw_poker_chips()
        self.draw_cards(self.dealer_hand, start_x=100, start_y=100)
        self.draw_cards(self.player_hand, start_x=100, start_y=300)

        if self.split_hands:
            if len(self.split_hands) > 0:
                self.draw_cards(self.split_hands[0], start_x=400, start_y=300, split_hand=1)
            if len(self.split_hands) > 1:
                self.draw_cards(self.split_hands[1], start_x=400, start_y=500, split_hand=2)

        self.draw_bankroll()

    def draw_cards(self, hand, start_x, start_y, split_hand=None):
        for i, card in enumerate(hand):
            x = start_x + i * 60
            y = start_y

            if split_hand:
                x += (split_hand - 1) * 300

            if not self.show_dealer_down_card and i == 0 and hand is self.dealer_hand:
                self.canvas.create_rectangle(x, y, x + 50, y + 80, fill="darkgray")
            else:
                if card:
                    rank = card['rank']
                    suit = card['suit']
                    self.canvas.create_rectangle(x, y, x + 50, y + 80, fill="lightgray")
                    self.canvas.create_text(x + 25, y + 40, text=f"{rank}\n{suit}", font=("Arial", 12), fill="black")
                else:
                    self.canvas.create_rectangle(x, y, x + 50, y + 80, fill="darkgray")

    def draw_bankroll(self):
        bankroll_text = f"Bankroll: ${self.bankroll.amount}"
        current_bet_text = f"Current Bet: ${self.current_bet.get()}"
        self.canvas.create_text(650, 50, text=bankroll_text, font=("Arial", 12), fill="white")
        self.canvas.create_text(650, 70, text=current_bet_text, font=("Arial", 12), fill="white")

    def draw_poker_chips(self):
        chip_values = ['$1', '$5', '$10', '$25', '$50', '$100', '$500', '$1000']
        num_chips = len(chip_values)
        chip_width = 50  # Adjust the width of the chips
        chip_height = 50  # Adjust the height of the chips

        # Calculate the total width needed for all chips without overlapping
        total_width = num_chips * chip_width + (num_chips - 1) * 10  # 10 is the separation between chips

        # Calculate the starting x-coordinate to center the chips
        start_x = (self.canvas.winfo_width() - total_width) / 2

        # Clear the canvas before redrawing chips
        self.canvas.delete("chips")

        for chip_value in chip_values:
            chip_image_path = f"poker_chip_{chip_value}.png"  # Replace with your actual image file paths
            chip_image = tk.PhotoImage(file=chip_image_path)

            # Scale the image to one-fourth of the size
            scaled_chip_image = chip_image.subsample(4, 4)

            chip_button = tk.Button(self.root, image=scaled_chip_image,
                                    command=lambda value=self.bankroll.chips[chip_value]: self.add_bet(value))
            chip_button.image = scaled_chip_image  # Keep a reference to prevent garbage collection

            # Place the chips equally spaced
            chip_button.place(x=start_x, y=550, anchor="center")

            # Update the starting x-coordinate for the next chip
            start_x += chip_width + 10  # 10 is the separation between chips

            # Tag the chips to clear them later
            self.canvas.create_image(start_x, 550, anchor="center", image=scaled_chip_image, tags="chips")

    def play_button_click(self):
        self.player_hand = []
        self.dealer_hand = []
        self.split_hands = []
        self.show_dealer_down_card = False
        self.stand_hand_1_button["state"] = tk.DISABLED
        self.stand_hand_2_button["state"] = tk.DISABLED

        # Do not reset the bet when the play button is clicked
        # self.reset_bet()

        for _ in range(2):
            self.blackjack_logic.deal_card(self.player_hand)
            self.blackjack_logic.deal_card(self.dealer_hand)

        self.update_display()

        player_blackjack = self.blackjack_logic.calculate_hand_value(self.player_hand) == 21
        dealer_blackjack = self.blackjack_logic.calculate_hand_value(self.dealer_hand) == 21

        if player_blackjack or dealer_blackjack:
            self.show_dealer_down_card = True
            self.update_display()
            self.root.after(self.result_delay, self.check_blackjack)
        else:
            self.stand_button["state"] = tk.NORMAL
            self.double_button["state"] = tk.NORMAL
            self.hit_button["state"] = tk.NORMAL
            self.split_button["state"] = tk.NORMAL

    def hit_button_click(self):
        self.blackjack_logic.deal_card(self.player_hand)
        self.update_display()

        player_bust = self.blackjack_logic.calculate_hand_value(self.player_hand) > 21

        if player_bust:
            self.stand_button_click()
        else:
            self.stand_button["state"] = tk.NORMAL

    def stand_button_click(self):
        self.show_dealer_down_card = True  # Show dealer's down card when player stands
        self.update_display()
        self.stand_button["state"] = tk.DISABLED
        self.hit_button["state"] = tk.DISABLED
        self.double_button["state"] = tk.DISABLED
        self.split_button["state"] = tk.DISABLED

        while self.blackjack_logic.calculate_hand_value(self.dealer_hand) < 17:
            self.blackjack_logic.deal_card(self.dealer_hand)
            self.update_display()
            self.root.after(self.result_delay)

        self.root.after(self.result_delay, self.check_result)

    def double_button_click(self):
        self.bankroll.amount -= self.current_bet.get()
        self.current_bet.set(self.current_bet.get() * 2)
        self.blackjack_logic.deal_card(self.player_hand)
        self.stand_button_click()

    def split_button_click(self):
        if len(self.player_hand) == 2 and self.player_hand[0]['rank'] == self.player_hand[1]['rank']:
            placeholder_card = {'rank': 'A', 'suit': 'Clubs'}  # A placeholder card
            self.split_hands = [self.player_hand.pop(), placeholder_card.copy()]
            self.bankroll.amount -= self.current_bet.get()
            self.current_bet.set(self.current_bet.get() * 2)
            self.stand_hand_1_button["state"] = tk.NORMAL
            self.stand_hand_2_button["state"] = tk.NORMAL
            self.update_display()
        else:
            messagebox.showinfo("Error", "Cannot split non-matching cards!")

    def stand_hand_1_button_click(self):
        self.stand_hand_1_button["state"] = tk.DISABLED
        self.hit_button["state"] = tk.DISABLED
        self.double_button["state"] = tk.DISABLED
        self.split_button["state"] = tk.DISABLED
        self.show_dealer_down_card = True

        while self.blackjack_logic.calculate_hand_value(self.dealer_hand) < 17:
            self.blackjack_logic.deal_card(self.dealer_hand)
            self.update_display()
            self.root.after(self.result_delay)

        self.root.after(self.result_delay, self.check_result)

    def stand_hand_2_button_click(self):
        self.stand_hand_2_button["state"] = tk.DISABLED
        self.hit_button["state"] = tk.DISABLED
        self.double_button["state"] = tk.DISABLED
        self.split_button["state"] = tk.DISABLED
        self.show_dealer_down_card = True

        while self.blackjack_logic.calculate_hand_value(self.dealer_hand) < 17:
            self.blackjack_logic.deal_card(self.dealer_hand)
            self.update_display()
            self.root.after(self.result_delay)

        self.root.after(self.result_delay, self.check_result)

    def check_blackjack(self):
        player_blackjack = self.blackjack_logic.calculate_hand_value(self.player_hand) == 21
        dealer_blackjack = self.blackjack_logic.calculate_hand_value(self.dealer_hand) == 21

        if player_blackjack and dealer_blackjack:
            self.update_display()
            messagebox.showinfo("Push", "Push! Both player and dealer have blackjack.")
            self.reset_game()
        elif player_blackjack:
            self.bankroll.amount += int(2.5 * self.current_bet.get())
            self.update_display()
            messagebox.showinfo("Blackjack!", "Player has blackjack. Player wins!")
            self.reset_game()
        elif dealer_blackjack:
            self.update_display()
            messagebox.showinfo("Dealer Blackjack", "Dealer has blackjack. Player loses!")
            self.reset_game()
        else:
            self.stand_button["state"] = tk.NORMAL
            self.double_button["state"] = tk.NORMAL
            self.hit_button["state"] = tk.NORMAL
            self.split_button["state"] = tk.NORMAL

    def check_result(self):
        player_value = self.blackjack_logic.calculate_hand_value(self.player_hand)
        dealer_value = self.blackjack_logic.calculate_hand_value(self.dealer_hand)

        if player_value > 21:
            self.update_display()
            messagebox.showinfo("Bust", "Player busts! Player loses!")
            self.bankroll.amount -= self.current_bet.get()  # Deduct the bet from the bankroll
            self.reset_game()
        elif dealer_value > 21:
            self.bankroll.amount += 2 * self.current_bet.get()
            self.update_display()
            messagebox.showinfo("Dealer Bust", "Dealer busts! Player wins!")
            self.reset_game()
        elif player_value == dealer_value:
            self.bankroll.amount += self.current_bet.get()
            self.update_display()
            messagebox.showinfo("Push", "Push! It's a tie.")
            self.reset_game()
        elif player_value > dealer_value:
            self.bankroll.amount += 2 * self.current_bet.get()
            self.update_display()
            messagebox.showinfo("Player Win", "Player wins!")
            self.reset_game()
        else:
            self.bankroll.amount -= self.current_bet.get()  # Deduct the bet from the bankroll
            self.update_display()
            messagebox.showinfo("Dealer Win", "Dealer wins! Player loses!")
            self.reset_game()

    def reset_game(self):
        self.blackjack_logic = BlackjackLogic()
        self.player_hand = []
        self.dealer_hand = []
        self.split_hands = []
        self.show_dealer_down_card = False
        self.stand_hand_1_button["state"] = tk.DISABLED
        self.stand_hand_2_button["state"] = tk.DISABLED

        self.update_display()

root = tk.Tk()
gui = InteractiveGUI(root)
root.mainloop()
