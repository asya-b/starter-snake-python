class Board:
    
    def __init__(self, boardData):
        self.width = boardData['board']['width']
        self.height = boardData['board']['height']
        
        self.foodSources = boardData['board']['food']
        self.snakes = boardData['board']['snakes']