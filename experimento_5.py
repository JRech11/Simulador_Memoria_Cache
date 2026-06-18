import main

class Experimento5:
    def __init__(self, arquivo_dados):
        self.arquivo_dados = arquivo_dados

    def executar(self):
        politica_substituicao = 'LRU'

        # Combinações: cache_kb, tam_bloco, associatividade
        combinacoes = [
            (8192,  64,  2),
            (8192,  64,  4),
            (8192,  128, 2),
            (8192,  128, 4),
            (16384, 64,  2),
            (16384, 64,  4),
            (16384, 128, 2),
            (16384, 128, 4),
        ]

        print("\n9. Anexo A:")

        for politica_escrita, nome_politica, num_tabela in [(0, 'Write-Through', 10), (1, 'Write-Back', 11)]:
            resultados = []

            for tam_cache, tam_bloco, assoc in combinacoes:
                num_linhas = tam_cache // tam_bloco

                if num_linhas < assoc:
                    continue

                simulador = main.executar_simulacao(
                    arquivo_dados=self.arquivo_dados,
                    tam_bloco=tam_bloco,
                    num_linhas=num_linhas,
                    associatividade=assoc,
                    politica_escrita=politica_escrita,
                    politica_substituicao=politica_substituicao
                )

                if not simulador or (simulador.reads + simulador.writes) == 0:
                    continue

                resultados.append({
                    'tam_cache_kb': tam_cache // 1024,
                    'tam_bloco': tam_bloco,
                    'assoc': assoc,
                    'leituras_mp': simulador.leituras_mp,
                    'escritas_mp': simulador.escritas_mp,
                    'total': simulador.leituras_mp + simulador.escritas_mp
                })

            if not resultados:
                print(f"[AVISO] Nenhum dado valido para {nome_politica}.")
                continue

            media_leituras = sum(r['leituras_mp'] for r in resultados) / len(resultados)
            media_escritas = sum(r['escritas_mp'] for r in resultados) / len(resultados)
            media_total    = sum(r['total']       for r in resultados) / len(resultados)

            print(f"\nTabela {num_tabela} - Largura de Banda da Memoria ({nome_politica})")
            cab = f"{'Cache':<8} | {'Bloco':<7} | {'Assoc':<6} | {'Leituras MP':<12} | {'Escritas MP':<12} | {'Total':<10}"
            print(cab)
            print("-" * 65)
            for r in resultados:
                print(f"{r['tam_cache_kb']:<6}KB | {r['tam_bloco']:<5}B | {r['assoc']:<6} | {r['leituras_mp']:<12} | {r['escritas_mp']:<12} | {r['total']:<10}")
            print("-" * 65)
            print(f"{'Media':<8} | {'':>7} | {'':>6} | {media_leituras:<12.2f} | {media_escritas:<12.2f} | {media_total:<10.2f}")
            print("-" * 65)