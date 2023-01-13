from .vehicle import Board

class Game():
    def __init__(self, input_file):
        # initialise board
        Board(input_file)

        # start solving the rush hour board
        self.make_move()

        """
        Ja ik weet even niet of we deze class nodig hebben. Misschien zodat we
        board.py alleen gebruiken voor initialising the board en dan dat we in deze hem gaan oplossen
        idk...

        :)

        ik weet ook niet of t werkt
        hehe
        
        """



    