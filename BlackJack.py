# Baney Casino BlackJack!
# For my CS and Math Undergrad portfolio

import tkinter as tk
from tkinter import messagebox
import random
from tkinter import PhotoImage


class Bankroll:
    def __init__(self):
        self.amount = 1000
        self.chips = {
            '$1': 1,
            '$5': 5,
            '$10': 10,
            '$25': 25,
            '$50': 50,
            '$100': 100,
            '$500': 500,
            '$1000': 1000
        }


class BlackjackLogic:
    def __init__(self):
        self.ranks = ['2', '3', '4', '5', '6',
                      '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.suits = ['Clubs', 'Spades', 'Diamonds', 'Hearts']
        self.cards = [{'rank': rank, 'suit': suit}
                      for rank in self.ranks for suit in self.suits]
        self.total_decks = 4  # Number of decks used
        self.shoe = self.cards * self.total_decks  # Assuming a 4-deck shoe
        random.shuffle(self.shoe)

        # New variables for counting
        self.running_count = 0
        self.total_cards_dealt = 0

    def deal_card(self, hand):
        if not self.shoe:
            # Reshuffle the shoe if all cards have been dealt
            self.shoe = self.cards * self.total_decks
            random.shuffle(self.shoe)
            self.running_count = 0  # Reset running count when reshuffling
            self.total_cards_dealt = 0  # Reset total cards dealt
            messagebox.showinfo(
                "Baney Casino - Shuffling Decks", "The decks are being reshuffled!")

        card = self.shoe.pop()
        hand.append(card)

        # Update running count and total cards dealt
        self.update_running_count(card)
        self.total_cards_dealt += 1

    def update_running_count(self, card):
        # Hi-Lo card counting system
        rank = card['rank']
        if rank in ['2', '3', '4', '5', '6']:
            self.running_count += 1
        elif rank in ['10', 'J', 'Q', 'K', 'A']:
            self.running_count -= 1
        # Cards 7, 8, 9 count as 0, so no change

    def calculate_hand_value(self, hand):
        values = [card_value(card['rank']) for card in hand]
        total = sum(values)
        num_aces = values.count(11)

        while total > 21 and num_aces:
            total -= 10  # Adjust ace from 11 to 1
            num_aces -= 1

        return total

    def get_running_count(self):
        return self.running_count

    def get_total_cards_dealt(self):
        return self.total_cards_dealt

    def get_decks_remaining(self):
        cards_remaining = len(self.shoe)
        decks_remaining = cards_remaining / 52.0  # Each deck has 52 cards
        return decks_remaining

    def get_true_count(self):
        decks_remaining = self.get_decks_remaining()
        if decks_remaining == 0:
            return 0  # Avoid division by zero
        true_count = self.running_count / decks_remaining
        return round(true_count, 2)  # Round to 2 decimal places


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
        self.root.title("Baney Casino - BlackJack!")

        # Start in full screen
        self.root.attributes("-fullscreen", True)

        self.bankroll = Bankroll()
        self.blackjack_logic = BlackjackLogic()
        self.current_bet = tk.IntVar()
        self.player_hands = []  # List of player hands
        self.bets = []  # List of bets corresponding to each hand
        self.dealer_hand = []
        self.result_delay = 1000
        self.show_dealer_down_card = False
        self.play_button_clicked = False
        self.current_hand_index = 0  # Index of the current hand being played

        self.canvas = tk.Canvas(self.root, bg="green")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()
        self.load_images()
        self.draw_poker_chips()
        self.update_info_label()
        self.update_display()

    def load_images(self):
        self.card_images = {}
        for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']:
            for suit in ['Clubs', 'Spades', 'Diamonds', 'Hearts']:
                filename = f"images/{rank}_{suit}.png"  # Update the path to your images
                try:
                    original_image = PhotoImage(file=filename)
                    resized_image = original_image.subsample(5, 5)
                    self.card_images[(rank, suit)] = resized_image
                except Exception as e:
                    messagebox.showerror(
                        "Image Load Error", f"Failed to load image {filename}: {e}")

        face_down_filename = "images/face_down_card.png"  # Update the path
        try:
            face_down_image = PhotoImage(file=face_down_filename)
            self.face_down_card_image = face_down_image.subsample(5, 5)
        except Exception as e:
            messagebox.showerror(
                "Image Load Error", f"Failed to load image {face_down_filename}: {e}")

        bg_filename = "images/BLACKJACKbaney.png"  # Update the path
        try:
            self.bg_image = tk.PhotoImage(file=bg_filename)
        except Exception as e:
            messagebox.showerror(
                "Image Load Error", f"Failed to load image {bg_filename}: {e}")

    def create_widgets(self):
        self.play_button = tk.Button(
            self.root, text="Play", command=self.play_button_click)
        self.play_button.place(
            relx=0.9, rely=0.1, anchor="center", width=100, height=30)

        self.hit_button = tk.Button(
            self.root, text="Hit", command=self.hit_button_click, state=tk.DISABLED)
        self.hit_button.place(
            relx=0.9, rely=0.2, anchor="center", width=100, height=30)

        self.stand_button = tk.Button(
            self.root, text="Stand", command=self.stand_button_click, state=tk.DISABLED)
        self.stand_button.place(
            relx=0.9, rely=0.3, anchor="center", width=100, height=30)

        self.double_button = tk.Button(
            self.root, text="Double", command=self.double_button_click, state=tk.DISABLED)
        self.double_button.place(
            relx=0.9, rely=0.4, anchor="center", width=100, height=30)

        self.split_button = tk.Button(
            self.root, text="Split", command=self.split_button_click, state=tk.DISABLED)
        self.split_button.place(
            relx=0.9, rely=0.5, anchor="center", width=100, height=30)

        self.reset_bet_button = tk.Button(
            self.root, text="Reset Bet", command=self.reset_bet_button_click)
        self.reset_bet_button.place(
            relx=0.9, rely=0.6, anchor="center", width=100, height=30)

        # Add a Quit button
        self.quit_button = tk.Button(
            self.root, text="Quit", command=self.quit_game)
        self.quit_button.place(
            relx=0.9, rely=0.7, anchor="center", width=100, height=30)

        # Place the info_label under the Quit button
        self.info_label = tk.Label(self.root, text="", font=(
            "Arial", 12), anchor="n", justify="center", wraplength=200)
        self.info_label.place(relx=0.9, rely=0.8, anchor="n", width=200)

    def quit_game(self):
        self.root.destroy()

    def draw_poker_chips(self):
        chip_positions = {
            '$1': 50,
            '$5': 130,
            '$10': 210,
            '$25': 290,
            '$50': 370,
            '$100': 450,
            '$500': 530,
            '$1000': 610
        }
        # Decrease subsample factor to increase size
        chip_size = 4

        for chip_value, x_offset in chip_positions.items():
            x_offset += 10
            filename = f"images/poker_chip_{chip_value}.png"
            try:
                chip_image = tk.PhotoImage(file=filename)
                chip_image = chip_image.subsample(chip_size, chip_size)
                chip_button = tk.Button(
                    self.root, image=chip_image, command=lambda value=self.bankroll.chips[chip_value]: self.add_bet(value), bd=0)
                chip_button.photo = chip_image
                chip_button.place(
                    x=x_offset, y=self.root.winfo_screenheight() - 100, anchor="center")
            except Exception as e:
                messagebox.showerror(
                    "Image Load Error", f"Failed to load image {filename}: {e}")

    def add_bet(self, value):
        if self.bankroll.amount >= value:
            self.current_bet.set(self.current_bet.get() + value)
            self.bankroll.amount -= value
            self.update_display()
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
        if hasattr(self, 'bg_image'):
            self.canvas.create_image(
                0, 0, anchor=tk.NW, image=self.bg_image)
        self.draw_poker_chips()
        self.draw_cards(self.dealer_hand, start_x=100,
                        start_y=150)  # Adjusted y position

        # Calculate x position for hand values (to the left of info_label)
        screen_width = self.root.winfo_screenwidth()
        hand_values_x = int(screen_width * 0.7)  # Adjust as needed

        y_position = 150  # Starting y position for hand values

        # Display dealer's hand value
        if self.show_dealer_down_card:
            dealer_value = self.blackjack_logic.calculate_hand_value(
                self.dealer_hand)
            self.canvas.create_text(
                hand_values_x, y_position, text=f"Dealer Hand Value: {dealer_value}", font=("Arial", 12), fill="white", anchor="w")
        else:
            self.canvas.create_text(
                hand_values_x, y_position, text="Dealer Hand Value: ?", font=("Arial", 12), fill="white", anchor="w")

        y_position += 30  # Increment y_position for next text

        # Display player's hand values
        for index, hand in enumerate(self.player_hands):
            start_y = 300 + index * 150  # Adjust spacing between hands
            self.draw_cards(
                hand, start_x=100, start_y=start_y, hand_number=index + 1)

            player_value = self.blackjack_logic.calculate_hand_value(hand)
            indicator = "<-- Playing" if index == self.current_hand_index else ""
            self.canvas.create_text(
                hand_values_x, y_position, text=f"Hand {index + 1} Value: {player_value} {indicator}", font=("Arial", 12), fill="white", anchor="w")
            y_position += 30  # Increment y_position for next hand

        # Display Running Count, Divisor, True Count, and Total Cards Dealt
        running_count = self.blackjack_logic.get_running_count()
        decks_remaining = self.blackjack_logic.get_decks_remaining()
        true_count = self.blackjack_logic.get_true_count()
        total_cards_dealt = self.blackjack_logic.get_total_cards_dealt()

        self.canvas.create_text(
            hand_values_x, y_position, text=f"Running Count: {running_count}", font=("Arial", 12), fill="white", anchor="w")
        y_position += 30
        self.canvas.create_text(
            hand_values_x, y_position, text=f"Decks Remaining: {decks_remaining:.2f}", font=("Arial", 12), fill="white", anchor="w")
        y_position += 30
        self.canvas.create_text(
            hand_values_x, y_position, text=f"True Count: {true_count}", font=("Arial", 12), fill="white", anchor="w")
        y_position += 30
        self.canvas.create_text(
            hand_values_x, y_position, text=f"Total Cards Dealt: {total_cards_dealt}", font=("Arial", 12), fill="white", anchor="w")

        self.draw_bankroll()
        self.update_info_label()

    def update_info_label(self):
        info_text = f"Welcome to Baney Casino's BlackJack!\n"
        info_text += f"Dealer stands on all 17s.\nBlackjack pays out 3:2.\n"
        info_text += f"This game is in Beta testing on GitHub.\n"
        info_text += f"All bug fixes can be emailed to:\n"
        info_text += f"me@joshbaney.com\n"
        info_text += f"Version 1.0.0-b.1"

        self.info_label.config(text=info_text)

    def draw_cards(self, hand, start_x, start_y, hand_number=None):
        card_width = 50
        card_height = 80

        if hand_number:
            self.canvas.create_text(
                start_x, start_y - 20, text=f"Hand {hand_number}", font=("Arial", 14), fill="yellow", anchor="w")

        for i, card in enumerate(hand):
            x = start_x + i * 60
            y = start_y

            if not self.show_dealer_down_card and i == 0 and hand is self.dealer_hand:
                self.canvas.create_image(
                    x + card_width / 2, y + card_height / 2, image=self.face_down_card_image)
            else:
                if card:
                    rank = card['rank']
                    suit = card['suit']
                    card_image = self.card_images.get((rank, suit), None)
                    if card_image:
                        self.canvas.create_image(
                            x + card_width / 2, y + card_height / 2, image=card_image)

    def draw_bankroll(self):
        bankroll_text = f"Bankroll: ${self.bankroll.amount}"
        current_bet_text = f"Current Bet: ${self.current_bet.get()}"
        self.canvas.create_text(
            self.root.winfo_screenwidth() - 200, 50, text=bankroll_text,
            font=("Arial", 12), fill="white", anchor="e")
        self.canvas.create_text(
            self.root.winfo_screenwidth() - 200, 70, text=current_bet_text,
            font=("Arial", 12), fill="white", anchor="e")

    def play_button_click(self):
        if not self.play_button_clicked:
            if self.current_bet.get() == 0:
                messagebox.showinfo(
                    "Error", "Please place a bet before playing!")
                return

            if self.bankroll.amount < 0:
                messagebox.showinfo(
                    "Game Over", "You've run out of funds!")
                self.root.destroy()
                return

            self.play_button_clicked = True
            self.dealer_hand = []
            self.player_hands = []
            self.bets = []
            self.current_hand_index = 0
            self.show_dealer_down_card = False

            self.bet_per_hand = self.current_bet.get()
            self.bets.append(self.bet_per_hand)

            # Create the initial hand
            initial_hand = []
            for _ in range(2):
                self.blackjack_logic.deal_card(initial_hand)
            self.player_hands.append(initial_hand)

            # Deal dealer's hand
            for _ in range(2):
                self.blackjack_logic.deal_card(self.dealer_hand)

            self.update_display()

            # Check for Blackjack on initial hand
            hand_value = self.blackjack_logic.calculate_hand_value(initial_hand)
            if hand_value == 21:
                messagebox.showinfo("Blackjack", "Player has Blackjack!")
                self.advance_to_next_hand()
            else:
                self.enable_action_buttons()

    def enable_action_buttons(self):
        self.stand_button["state"] = tk.NORMAL
        self.double_button["state"] = tk.NORMAL
        self.hit_button["state"] = tk.NORMAL
        self.split_button["state"] = tk.NORMAL

    def disable_action_buttons(self):
        self.stand_button["state"] = tk.DISABLED
        self.double_button["state"] = tk.DISABLED
        self.hit_button["state"] = tk.DISABLED
        self.split_button["state"] = tk.DISABLED

    def hit_button_click(self):
        current_hand = self.player_hands[self.current_hand_index]
        self.blackjack_logic.deal_card(current_hand)
        self.update_display()

        hand_value = self.blackjack_logic.calculate_hand_value(current_hand)
        if hand_value > 21:
            messagebox.showinfo(
                "Bust", f"Hand {self.current_hand_index + 1} busts!")
            self.advance_to_next_hand()
        elif hand_value == 21:
            messagebox.showinfo(
                "21", f"Hand {self.current_hand_index + 1} has 21!")
            self.advance_to_next_hand()

    def stand_button_click(self):
        self.advance_to_next_hand()

    def double_button_click(self):
        if self.bankroll.amount >= self.bets[self.current_hand_index]:
            self.bankroll.amount -= self.bets[self.current_hand_index]
            self.bets[self.current_hand_index] *= 2
            current_hand = self.player_hands[self.current_hand_index]
            self.blackjack_logic.deal_card(current_hand)
            self.update_display()
            self.advance_to_next_hand()
        else:
            messagebox.showinfo(
                "Error", "Insufficient funds to double down!")

    def split_button_click(self):
        current_hand = self.player_hands[self.current_hand_index]
        if len(current_hand) == 2 and card_value(current_hand[0]['rank']) == card_value(current_hand[1]['rank']):
            if self.bankroll.amount >= self.bet_per_hand:
                self.bankroll.amount -= self.bet_per_hand
                self.bets.append(self.bet_per_hand)
                # Split the current hand into two hands
                card1 = current_hand[0]
                card2 = current_hand[1]
                current_hand.clear()
                current_hand.append(card1)
                new_hand = [card2]
                self.player_hands.insert(
                    self.current_hand_index + 1, new_hand)

                # Deal one additional card to each hand
                self.blackjack_logic.deal_card(current_hand)
                self.blackjack_logic.deal_card(new_hand)
                self.update_display()
            else:
                messagebox.showinfo(
                    "Error", "Insufficient funds to split!")
        else:
            messagebox.showinfo(
                "Error", "Cannot split non-matching cards!")

    def advance_to_next_hand(self):
        self.disable_action_buttons()
        self.current_hand_index += 1
        if self.current_hand_index < len(self.player_hands):
            current_hand = self.player_hands[self.current_hand_index]
            hand_value = self.blackjack_logic.calculate_hand_value(
                current_hand)
            if hand_value == 21:
                messagebox.showinfo(
                    "Blackjack", f"Hand {self.current_hand_index + 1} has Blackjack!")
                self.advance_to_next_hand()
            elif hand_value > 21:
                messagebox.showinfo(
                    "Bust", f"Hand {self.current_hand_index + 1} busts!")
                self.advance_to_next_hand()
            else:
                self.enable_action_buttons()
            self.update_display()
        else:
            self.finish_round()

    def finish_round(self):
        self.disable_action_buttons()
        self.show_dealer_down_card = True
        self.update_display()
        # Dealer plays
        while self.blackjack_logic.calculate_hand_value(self.dealer_hand) < 17:
            self.blackjack_logic.deal_card(self.dealer_hand)
            self.update_display()
            self.root.after(self.result_delay)
        self.root.after(self.result_delay, self.check_results)

    def check_results(self):
        dealer_value = self.blackjack_logic.calculate_hand_value(
            self.dealer_hand)
        for i, hand in enumerate(self.player_hands):
            player_value = self.blackjack_logic.calculate_hand_value(hand)
            bet = self.bets[i]
            if player_value > 21:
                # Player loses
                messagebox.showinfo(
                    f"Hand {i+1} Lose", f"Hand {i+1} busts! Dealer wins.")
                # Bet is already deducted
            elif dealer_value > 21:
                winnings = bet * 2
                self.bankroll.amount += winnings
                messagebox.showinfo(
                    f"Hand {i+1} Win", f"Dealer busts! Player wins Hand {i+1}! Won ${bet}.")
            elif player_value > dealer_value:
                winnings = bet * 2
                self.bankroll.amount += winnings
                messagebox.showinfo(
                    f"Hand {i+1} Win", f"Player wins Hand {i+1}! Won ${bet}.")
            elif player_value == dealer_value:
                self.bankroll.amount += bet
                messagebox.showinfo(
                    f"Hand {i+1} Push", f"Push on Hand {i+1}! Bet returned.")
            else:
                messagebox.showinfo(
                    f"Hand {i+1} Lose", f"Dealer wins Hand {i+1}!")
                # Bet is already deducted

        self.reset_game()

    def reset_game(self):
        self.play_button_clicked = False
        self.player_hands = []
        self.dealer_hand = []
        self.bets = []
        self.current_hand_index = 0
        self.show_dealer_down_card = False
        self.disable_action_buttons()
        self.update_display()

        if self.bankroll.amount <= 0:
            messagebox.showinfo("Game Over", "You've run out of funds!")
            self.root.destroy()
        else:
            self.prompt_for_new_bet()

    def prompt_for_new_bet(self):
        if self.bankroll.amount <= 0:
            messagebox.showinfo("Game Over", "You've run out of funds!")
            self.root.destroy()
            return

        response = messagebox.askquestion(
            "Next Round", "Do you want to keep the current bet or make a new bet?", icon='question',
            type=messagebox.YESNO, default=messagebox.YES)

        if response == 'yes':
            # Check if player has enough funds to keep the current bet
            if self.bankroll.amount >= self.current_bet.get():
                # Deduct the bet amount from the bankroll
                self.bankroll.amount -= self.current_bet.get()
                self.update_display()
                self.play_button_click()
            else:
                messagebox.showinfo("Insufficient Funds",
                                    "You don't have enough funds to keep the current bet.")
                self.reset_bet()
        else:
            # Player wants to make a new bet
            self.reset_bet()
            messagebox.showinfo(
                "Place Bet", "Please place a new bet and press Play to start.")

    def reset_bet(self):
        # Add the current bet back to the bankroll
        self.bankroll.amount += self.current_bet.get()
        self.current_bet.set(0)
        self.update_display()


root = tk.Tk()
gui = InteractiveGUI(root)
root.mainloop()
