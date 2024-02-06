#Baney Casino BlackJack!
#For my CS and Math Undergrad portfolio

import tkinter as tk
from tkinter import messagebox
import random
from tkinter import PhotoImage


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
        self.root.title("Baney Casino- BlackJack!")
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
        self.play_button_clicked = False  # Track whether the play button is clicked

        # Use grid for better control over layout
        self.canvas = tk.Canvas(self.root, bg="green")
        self.canvas.grid(row=0, column=0, rowspan=6, padx=10, pady=10, sticky="nsew")

        # Adding a Label for game information
        self.info_label = tk.Label(self.root, text="", font=("Arial", 12), anchor="e", justify="right", wraplength=200)
        self.info_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Set row and column configurations to expand
        for i in range(6):
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.create_widgets()
        self.draw_poker_chips()
        self.card_images = {}
        for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
            for suit in ['Clubs', 'Spades', 'Diamonds', 'Hearts']:
                filename = f"{rank}_{suit}.png"  # Replace with your actual image filenames
                original_image = PhotoImage(file=filename)
                resized_image = original_image.subsample(5, 5)  # Adjust the subsample factor as needed
                self.card_images[(rank, suit)] = resized_image
        face_down_filename = "face_up_card.png"  # Replace with your actual image filename
        face_down_image = PhotoImage(file=face_down_filename)
        self.face_down_card_image = face_down_image.subsample(5, 5)  # Adjust the subsample factor as needed

        # Load the background image
        self.bg_image = tk.PhotoImage(file="BLACKJACKbaney.png")  # Update the path to your image file
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)

    def shuffle_deck(self):

        messagebox.showinfo("Baney Casino- Shuffling Decks", "The decks are being shuffled!")
        self.shoe = self.cards * 4
        random.shuffle(self.shoe)
    def create_widgets(self):

        self.play_button = tk.Button(self.root, text="Play", command=self.play_button_click)
        self.play_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.hit_button = tk.Button(self.root, text="Hit", command=self.hit_button_click)
        self.hit_button.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.stand_button = tk.Button(self.root, text="Stand", command=self.stand_button_click, state=tk.DISABLED)
        self.stand_button.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        self.double_button = tk.Button(self.root, text="Double", command=self.double_button_click, state=tk.DISABLED)
        self.double_button.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        self.split_button = tk.Button(self.root, text="Split", command=self.split_button_click, state=tk.DISABLED)
        self.split_button.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

        self.stand_hand_1_button = tk.Button(self.root, text="Stand on Split Hand 1", command=self.stand_hand_1_button_click, state=tk.DISABLED)
        self.stand_hand_1_button.grid(row=6, column=1, padx=10, pady=10, sticky="nsew")

        self.stand_hand_2_button = tk.Button(self.root, text="Stand on Split Hand 2", command=self.stand_hand_2_button_click, state=tk.DISABLED)
        self.stand_hand_2_button.grid(row=7, column=1, padx=10, pady=10, sticky="nsew")

        self.reset_bet_button = tk.Button(self.root, text="Reset Bet", command=self.reset_bet_button_click)
        self.reset_bet_button.grid(row=8, column=1, padx=10, pady=10, sticky="nsew")
    def draw_poker_chips(self):
        chip_positions = {'$1': 50, '$5': 120, '$10': 190, '$25': 260, '$50': 330, '$100': 400, '$500': 470, '$1000': 540}

        chip_size = 6  # Adjust the size of the chips

        for chip_value, x_offset in chip_positions.items():
            x_offset += 10  # Add an offset to avoid the left edge

            # Load the chip image
            chip_image = tk.PhotoImage(file=f"poker_chip_{chip_value}.png")
            chip_image = chip_image.subsample(chip_size, chip_size)  # Resize the image

            # Create a button with the chip image
            chip_button = tk.Button(self.root, image=chip_image, command=lambda value=self.bankroll.chips[chip_value]: self.add_bet(value))
            chip_button.photo = chip_image  # Keep a reference to the image to prevent it from being garbage collected
            chip_button.place(x=x_offset, y=550, anchor="center")  # Anchor the center point

    def add_bet(self, value):
        if self.bankroll.amount >= value:
            self.current_bet.set(self.current_bet.get() + value)
            self.bankroll.amount -= value
            self.update_display()
            self.draw_poker_chips()
        else:
            messagebox.showinfo("Error", "Insufficient funds!")

    def reset_bet_button_click(self):
        self.reset_bet()
        self.update_display()

    def reset_bet(self):
        self.bankroll.amount += self.current_bet.get()
        self.current_bet.set(0)
        self.update_display()

    def update_display(self):
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)  # Redraw background image
        self.draw_poker_chips()
        self.draw_cards(self.dealer_hand, start_x=100, start_y=100)
        self.draw_cards(self.player_hand, start_x=100, start_y=300)

        if self.split_hands:
            if len(self.split_hands) > 0:
                self.draw_cards(self.split_hands[0], start_x=400, start_y=300, split_hand=1)
            if len(self.split_hands) > 1:
                self.draw_cards(self.split_hands[1], start_x=400, start_y=500, split_hand=2)

        self.draw_bankroll()
        self.update_info_label()

        # Display current hand values
        player_value = self.blackjack_logic.calculate_hand_value(self.player_hand)
        self.canvas.create_text(650, 90, text=f"Player Hand Value: {player_value}", font=("Arial", 12), fill="white")

        if self.show_dealer_down_card:
            dealer_value = self.blackjack_logic.calculate_hand_value(self.dealer_hand)
            self.canvas.create_text(650, 110, text=f"Dealer Hand Value: {dealer_value}", font=("Arial", 12),
                                    fill="white")


    def update_info_label(self):
        info_text = f"Welcome to Baney Casino's BlackJack!\n"
        info_text += f"Dealer Stands on all 17s.\n BlackJack pays out 3/2.\n"
        info_text += f"This game is in Beta testing on GitHub.\n"
        info_text += f"All Bug fixes can be emailed to:\n"
        info_text += f"me@joshbaney.com\n"
        info_text += f"Version 1.0.0-b.1"

        # Display additional game information as needed

        self.info_label.config(text=info_text)

    def draw_cards(self, hand, start_x, start_y, split_hand=None):
        card_width = 50  # Adjust as needed
        card_height = 80  # Adjust as needed

        for i, card in enumerate(hand):
            x = start_x + i * 60
            y = start_y

            if split_hand:
                x += (split_hand - 1) * 300

            if not self.show_dealer_down_card and i == 0 and hand is self.dealer_hand:
                # Show face-down card
                self.canvas.create_image(x + card_width / 2, y + card_height / 2, image=self.face_down_card_image)
            else:
                if card:
                    rank = card['rank']
                    suit = card['suit']
                    card_image = self.card_images.get((rank, suit), None)
                    if card_image:
                        self.canvas.create_image(x + card_width / 2, y + card_height / 2, image=card_image)
                    else:
                        # Handle empty slots if needed
                        pass
                else:
                    # Handle empty slots if needed
                    pass

    def draw_bankroll(self):
        bankroll_text = f"Bankroll: ${self.bankroll.amount}"
        current_bet_text = f"Current Bet: ${self.current_bet.get()}"
        self.canvas.create_text(650, 50, text=bankroll_text, font=("Arial", 12), fill="white")
        self.canvas.create_text(650, 70, text=current_bet_text, font=("Arial", 12), fill="white")

    def play_button_click(self):
        if not self.play_button_clicked:
            self.play_button_clicked = True
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

            # Enable the play button at the start of a new round
            self.root.after(self.result_delay, self.enable_play_button)


    def enable_play_button(self):
        self.play_button_clicked = False

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
            messagebox.showinfo("Error", "Cannot split non-matching cards! \n If you are seeing this with cards of values of 10, \n You're an idiot. Never split 10s.")

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
            self.update_display()
            messagebox.showinfo("Push", "Push! It's a tie.")
            # No change to the bankroll on a push
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

        # Do not reset the current bet
        # self.current_bet.set(0)

        self.update_display()

root = tk.Tk()
gui = InteractiveGUI(root)
root.mainloop()
