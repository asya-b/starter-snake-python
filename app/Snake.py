class Snake:
    
    def __init__(self, boardData):
        self.headX = boardData['you']['body'][0]['x']
        self.headY = boardData['you']['body'][0]['y']
        self.neckX = boardData['you']['body'][1]['x']
        self.neckY = boardData['you']['body'][1]['y']
        
    COLOUR = "#000000"
