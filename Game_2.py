class Board:
    def __init__(self, size=9):
        self.size = size
        self.grid = [[Ship(name="Empty", size=0, player=0) for _ in range(self.size)] for _ in range(self.size)]

    def start(self):
        print("Welcome to Battleship game")
        print("Player 1's turn:")
        self.place_ships(player=1)
        print("Player 2's turn:")
        self.place_ships(player=2)
        self.print_grid()  # Print the grid after ship placement
        self.play_game()

    def place_ships(self, player):
        for i in range(4):  # Each player places 8 ships
            while True:
                print(f"Player {player}, place your ship {i + 1} on the grid:")
                row = int(input("Enter row number: "))
                col = int(input("Enter column number: "))
                if self.validate_ship_placement(row, col):
                    ship = self.select_ship(player)
                    self.grid[row][col] = ship
                    break
                else:
                    print("Invalid placement. Try again.")

    def validate_ship_placement(self, row, col):
        # Check if the cell is empty
        if self.grid[row][col].name == "Empty":
            return True
        else:
            return False

    def select_ship(self, player):
        print("Select a ship:")
        print("1. Destroyer")
        print("2. Battleship")
        print("3. Cruiser")
        print("4. Submarine")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            return Ship.destroyer(player)
        elif choice == 2:
            return Ship.battleship(player)
        elif choice == 3:
            return Ship.cruiser(player)
        elif choice == 4:
            return Ship.submarine(player)
        else:
            print("Invalid choice. Defaulting to Destroyer.")
            return Ship.destroyer(player)

    def print_grid(self):
        print("Grid after ship placement:")
        for row in self.grid:
            for cell in row:
                if cell.player == 1:
                    print(f"\033[91m{cell.name}\033[0m", end="\t")  # Red color for player 1
                elif cell.player == 2:
                    print(f"\033[94m{cell.name}\033[0m", end="\t")  # Blue color for player 2
                else:
                    print(cell.name, end="\t")
            print()  # Newline after each row

    def play_game(self):
        current_player = 1
        while True:
            print(f"Player {current_player}, it's your turn to attack (type 'quit' to end the game):")
            attack = input("Enter 'row,col' to attack: ")
            if attack.lower() == "quit":
                print("Game over. Thanks for playing!")
                break
            try:
                row, col = map(int, attack.split(","))
                target_cell = self.grid[row][col]
                if target_cell.name != "Empty":
                    print(f"Player {current_player}, you hit {target_cell.name}!")
                    target_cell.size -= 1  # Reduce ship size
                    if target_cell.size == 0:
                        print(f"Player {current_player}, you sunk {target_cell.name}!")
                        target_cell.name = "Empty"
                else:
                    print("Miss! There's no ship at this location.")
                self.print_grid()  # Print the grid after each move
                # Check if all ships of the other player are sunk
                if self.all_ships_sunk(3 - current_player):
                    print(f"Congratulations, Player {current_player}! You win!")
                    break
                # Switch players
                current_player = 3 - current_player
            except ValueError:
                print("Invalid input. Please enter 'row,col' to attack or 'quit' to end the game.")

    def all_ships_sunk(self, player):
        for row in self.grid:
            for cell in row:
                if cell.player == player and cell.size > 0:
                    return False
        return True


class Ship:
    def __init__(self, name, size, player):
        self.name = name
        self.size = size
        self.player = player

    @classmethod
    def destroyer(cls, player):
        return cls("destroyer", 2, player)

    @classmethod
    def battleship(cls, player):
        return cls("battleship", 4, player)

    @classmethod
    def cruiser(cls, player):
        return cls("cruiser", 3, player)

    @classmethod
    def submarine(cls, player):
        return cls("submarine", 1, player)


# Usage
board = Board()
board.start()