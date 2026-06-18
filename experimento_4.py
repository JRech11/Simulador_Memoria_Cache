import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import main

class Experimento4:
    def __init__(self, arquivo_dados):
        self.arquivo_dados = arquivo_dados

    def executar(self):
        # Parâmetros Fixos (Experimento 4)
        tam_bloco = 128
        politica_escrita = 0      # Write-Through
        associatividade = 4

        print("\n9. Anexo A:")
        print("Tabela 7 - Parametros da Simulacao (Impacto da Politica de Substituicao)")
        print(f"{'Parametro':<30} | {'Valor':<20}")
        print("-" * 55)
        print(f"{'Tamanho do Bloco':<30} | {tam_bloco} bytes")
        print(f"{'Politica de Escrita':<30} | write-through")
        print(f"{'Associatividade':<30} | {associatividade} blocos")
        print("-" * 55)

        variacoes_blocos = [2**i for i in range(4, 11)]  # 16 ate 1024
        resultados_lru = []
        resultados_aleatoria = []

        for num_linhas in variacoes_blocos:
            for politica_sub, lista in [('LRU', resultados_lru), ('ALEATORIA', resultados_aleatoria)]:
                simulador = main.executar_simulacao(
                    arquivo_dados=self.arquivo_dados,
                    tam_bloco=tam_bloco,
                    num_linhas=num_linhas,
                    associatividade=associatividade,
                    politica_escrita=politica_escrita,
                    politica_substituicao=politica_sub
                )

                if not simulador or (simulador.reads + simulador.writes) == 0:
                    continue

                total_enderecos = simulador.reads + simulador.writes
                hit_rate_global = ((simulador.read_hits + simulador.write_hits) / total_enderecos) * 100
                amat = simulador.tempo_total_simulacao / total_enderecos

                lista.append({
                    'blocos': num_linhas,
                    'tamanho_bytes': num_linhas * tam_bloco,
                    'hit_rate': hit_rate_global,
                    'amat': amat,
                    'leituras_mp': simulador.leituras_mp,
                    'escritas_mp': simulador.escritas_mp
                })

        if not resultados_lru and not resultados_aleatoria:
            print("[AVISO] Nenhum dado valido processado. Verifique o arquivo dados.txt.")
            return

        print("\nTabela 8 - Resultados da Simulacao - LRU")
        colunas = f"{'Numero de Blocos':<18} | {'Taxa de Acerto':<15} | {'Tempo medio (ns)':<18} | {'Leituras na MP':<15} | {'Escritas na MP':<15}"
        print(colunas)
        print("-" * 90)
        for res in resultados_lru:
            print(f"{res['blocos']:<18} | {res['hit_rate']:>13.4f}% | {res['amat']:>16.4f} | {res['leituras_mp']:<15} | {res['escritas_mp']:<15}")
        print("-" * 90)

        print("\nTabela 9 - Resultados da Simulacao - Aleatoria")
        print(colunas)
        print("-" * 90)
        for res in resultados_aleatoria:
            print(f"{res['blocos']:<18} | {res['hit_rate']:>13.4f}% | {res['amat']:>16.4f} | {res['leituras_mp']:<15} | {res['escritas_mp']:<15}")
        print("-" * 90)

        self._plotar_grafico(resultados_lru, resultados_aleatoria)

    def _plotar_grafico(self, resultados_lru, resultados_aleatoria):
        eixo_x_lru = [res['tamanho_bytes'] for res in resultados_lru]
        eixo_y_lru = [res['hit_rate'] for res in resultados_lru]

        eixo_x_al = [res['tamanho_bytes'] for res in resultados_aleatoria]
        eixo_y_al = [res['hit_rate'] for res in resultados_aleatoria]

        rotulos = [f"{res['blocos']} blk\n({res['tamanho_bytes']}B)" for res in resultados_lru]

        plt.figure(figsize=(11, 5))
        plt.plot(eixo_x_lru, eixo_y_lru, marker='o', linestyle='-', color='#1f77b4', linewidth=2, label='LRU')
        plt.plot(eixo_x_al, eixo_y_al, marker='s', linestyle='--', color='#ff7f0e', linewidth=2, label='Aleatoria')
        plt.title('Impacto da Politica de Substituicao na Taxa de Acerto (Experimento 4)', fontweight='bold')
        plt.xlabel('Tamanho da Cache (Blocos e Bytes)')
        plt.ylabel('Taxa de Acerto (%)')
        plt.xscale('log', base=2)
        plt.xticks(eixo_x_lru, rotulos)
        plt.ylim(-5, 105)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.legend()

        for i, val in enumerate(eixo_y_lru):
            plt.annotate(f"{val:.2f}%", (eixo_x_lru[i], eixo_y_lru[i]), textcoords="offset points", xytext=(0, 8), ha='center', fontsize=7.5)
        for i, val in enumerate(eixo_y_al):
            plt.annotate(f"{val:.2f}%", (eixo_x_al[i], eixo_y_al[i]), textcoords="offset points", xytext=(0, -16), ha='center', fontsize=7.5)

        plt.tight_layout()
        plt.savefig('grafico_experimento_4.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("\n[INFO] Grafico salvo em: grafico_experimento_4.png")