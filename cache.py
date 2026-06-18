import math
import random
from linha_cache import LinhaCache

class CacheAssociativaConjunto:
    def __init__(self, tam_linha, num_linhas, associatividade, politica_escrita, politica_substituicao):
        self.tam_linha = tam_linha
        self.num_linhas = num_linhas
        self.vias = associatividade
        self.politica_escrita = politica_escrita
        self.politica_substituicao = politica_substituicao.upper()
        
        # Tempos de acesso
        self.HIT_TIME = 5
        self.MEM_ACCESS_TIME = 70
        self.tempo_total_simulacao = 0.0

        # Cálculo do número de conjuntos
        self.num_conjuntos = num_linhas // associatividade
        if self.num_conjuntos < 1:
            raise ValueError("A associatividade não pode ser maior que o número total de linhas.")

        # Matriz da cache: Conjuntos x Vias
        self.cache = [[LinhaCache() for _ in range(self.vias)] for _ in range(self.num_conjuntos)]
        
        # Estatísticas de acessos
        self.reads = 0
        self.writes = 0
        self.read_hits = 0
        self.read_misses = 0
        self.write_hits = 0
        self.write_misses = 0
        
        self.leituras_mp = 0
        self.escritas_mp = 0
        self.ciclo_global = 0

    def processar_acesso(self, endereco_hex, operacao):
        self.ciclo_global += 1
        endereco = int(endereco_hex, 16)
        
        bits_offset = int(math.log2(self.tam_linha))
        bits_indice = int(math.log2(self.num_conjuntos)) if self.num_conjuntos > 1 else 0
        
        endereco_bloco = endereco >> bits_offset
        if bits_indice > 0:
            indice_conjunto = endereco_bloco & ((1 << bits_indice) - 1)
            rotulo = endereco_bloco >> bits_indice
        else:
            indice_conjunto = 0
            rotulo = endereco_bloco

        conjunto = self.cache[indice_conjunto]
        hit = False
        linha_atingida = None

        for linha in conjunto:
            if linha.valido == 1 and linha.rotulo == rotulo:
                hit = True
                linha_atingida = linha
                break

        self.tempo_total_simulacao += self.HIT_TIME

        if operacao == 'R':
            self.reads += 1
            if hit:
                self.read_hits += 1
                linha_atingida.lru = self.ciclo_global
            else:
                self.read_misses += 1
                self.leituras_mp += 1
                self.tempo_total_simulacao += self.MEM_ACCESS_TIME
                self._substituir_e_alocar(conjunto, rotulo, operacao)

        elif operacao == 'W':
            self.writes += 1
            if hit:
                self.write_hits += 1
                linha_atingida.lru = self.ciclo_global
                
                if self.politica_escrita == 0:  # Write-Through
                    self.escritas_mp += 1  
                    self.tempo_total_simulacao += self.MEM_ACCESS_TIME
                else:                           # Write-Back
                    linha_atingida.dirty = 1
            else:
                self.write_misses += 1
                if self.politica_escrita == 0:  # Write-Through (No-Write-Allocate)
                    self.escritas_mp += 1  
                    self.tempo_total_simulacao += self.MEM_ACCESS_TIME
                else:                           # Write-Back (Write-Allocate)
                    self.leituras_mp += 1  
                    self.tempo_total_simulacao += self.MEM_ACCESS_TIME
                    self._substituir_e_alocar(conjunto, rotulo, operacao)

    def _substituir_e_alocar(self, conjunto, rotulo, operacao):
        linha_substituir = None
        for linha in conjunto:
            if linha.valido == 0:
                linha_substituir = linha
                break
        
        if not linha_substituir:
            if self.politica_substituicao == 'LRU':
                linha_substituir = min(conjunto, key=lambda l: l.lru)
            elif self.politica_substituicao == 'ALEATORIA':
                linha_substituir = random.choice(conjunto)
            else:
                linha_substituir = conjunto[0]

            if self.politica_escrita == 1 and linha_substituir.dirty == 1:
                self.escritas_mp += 1
                self.tempo_total_simulacao += self.MEM_ACCESS_TIME

        linha_substituir.valido = 1
        linha_substituir.rotulo = rotulo
        linha_substituir.lru = self.ciclo_global
        
        if self.politica_escrita == 1 and operacao == 'W':
            linha_substituir.dirty = 1
        else:
            linha_substituir.dirty = 0