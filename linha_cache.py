class LinhaCache:
    def __init__(self):
        self.valido = 0   # 1 se contém dados válidos, 0 caso contrário
        self.rotulo = -1  # Identificador do bloco (Tag)
        self.dirty = 0    # 1 se a linha foi modificada (usado no Write-Back)
        self.lru = 0      # Contador de uso para a política LRU