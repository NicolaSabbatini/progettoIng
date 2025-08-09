class Auto:
    def __init__(self, marca, modello, anno):
        self.marca = marca
        self.modello = modello
        self.anno = anno

    def scheda(self):
        return f"{self.marca} {self.modello} ({self.anno})"