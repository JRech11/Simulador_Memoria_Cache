import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import main

class Experimento3:
    def __init__(self, arquivo_dados):
        self.arquivo_dados = arquivo_dados

    def executar(self):
        # Parâmetros Fixos (Experimento 3)
        tam_bloco = 128
        tamanho_total_cache_bytes = 8192
        politica_escrita = 1      
        politica_substituicao = 'LRU'

        print("\n9. Anexo A:")
        print("Tabela 5 - Parametros da Simulacao (Impacto da Associatividade)")
        print(f"{'Parametro':<30} | {'Valor':<20}")
        print("-" * 55)
        print(f"{'Tamanho do Bloco':<30} | {tam_bloco} bytes")
        print(f"{'Tamanho Total da Cache':<30} | {tamanho_total_cache_bytes // 1024} KB ({tamanho_total_cache_bytes} bytes)")
        print(f"{'Politica de Escrita':<30} | write-back")
        print(f"{'Algoritmo de Substituicao':<30} | {politica_substituicao}")
        print("-" * 55)

        # Associatividade de 1 a 64 em potências de 2
        variacoes_assoc = [2**i for i in range(0, 7)]  
        resultados = []

        for associatividade in variacoes_assoc:
            num_linhas = tamanho_total_cache_bytes // tam_bloco  

            if num_linhas < associatividade:
                continue

            simulador = main.executar_simulacao(
                arquivo_dados=self.arquivo_dados,
                tam_bloco=tam_bloco,
                num_linhas=num_linhas,
                associatividade=associatividade,
                politica_escrita=politica_escrita,
                politica_substituicao=politica_substituicao
            )

            if not simulador or (simulador.reads + simulador.writes) == 0:
                continue

            total_enderecos = simulador.reads + simulador.writes
            hit_rate_global = ((simulador.read_hits + simulador.write_hits) / total_enderecos) * 100
            amat = simulador.tempo_total_simulacao / total_enderecos

            resultados.append({
                'associatividade': associatividade,
                'num_conjuntos': num_linhas // associatividade,
                'hit_rate': hit_rate_global,
                'amat': amat,
                'leituras_mp': simulador.leituras_mp,
                'escritas_mp': simulador.escritas_mp
            })

        if not resultados:
            print("[AVISO] Nenhum dado valido processado. Verifique o arquivo dados.txt.")
            return

        print("\nTabela 6 - Resultados da Simulacao (Impacto da Associatividade)")
        colunas = f"{'Associatividade':<18} | {'Num. Conjuntos':<15} | {'Taxa de Acerto':<15} | {'Tempo medio (ns)':<18} | {'Leituras na MP':<15} | {'Escritas na MP':<15}"
        print(colunas)
        print("-" * 105)
        for res in resultados:
            print(f"{res['associatividade']:<18} | {res['num_conjuntos']:<15} | {res['hit_rate']:>13.4f}% | {res['amat']:>16.4f} | {res['leituras_mp']:<15} | {res['escritas_mp']:<15}")
        print("-" * 105)

        self._plotar_grafico(resultados)

    def _plotar_grafico(self, resultados):
        eixo_x = [res['associatividade'] for res in resultados]
        eixo_y = [res['hit_rate'] for res in resultados]
        rotulos = [f"{res['associatividade']}-way\n({res['num_conjuntos']} conj)" for res in resultados]

        plt.figure(figsize=(10, 5))
        plt.plot(eixo_x, eixo_y, marker='o', linestyle='-', color='#d62728', linewidth=2)
        plt.title('Impacto da Associatividade na Taxa de Acerto (Experimento 3)', fontweight='bold')
        plt.xlabel('Associatividade (Vias e Conjuntos)')
        plt.ylabel('Taxa de Acerto (%)')
        plt.xscale('log', base=2)
        plt.xticks(eixo_x, rotulos)
        plt.ylim(-5, 105)
        plt.grid(True, linestyle='--', alpha=0.5)

        for i, val in enumerate(eixo_y):
            plt.annotate(f"{val:.4f}%", (eixo_x[i], eixo_y[i]), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)
        plt.tight_layout()
        plt.savefig('grafico_experimento_3.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("\n[INFO] Grafico salvo em: grafico_experimento_3.png")
