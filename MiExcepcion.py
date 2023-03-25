class MiExcepcion(Exception):
    
    def __init__(self, err):
        self.err = err