import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import main

class Experimento1:
    def __init__(self, arquivo_dados):
        self.arquivo_dados = arquivo_dados

    def executar(self):
        # Parâmetros Fixos (Experimento 1)
        tam_bloco = 128           
        politica_escrita = 0      # 0 = Write-Through
        politica_substituicao = 'LRU'
        associatividade = 4       
        
        print("\n9. Anexo A:")
        print("Tabela 1 - Parametros da Simulacao")
        print(f"{'Parametro':<30} | {'Valor':<20}")
        print("-" * 55)
        print(f"{'Tamanho do Bloco':<30} | {tam_bloco} bytes")
        print(f"{'Politica de Escrita':<30} | write-through")
        print(f"{'Algoritmo de Substituicao':<30} | {politica_substituicao}")
        print(f"{'Associatividade':<30} | {associatividade} blocos")
        print("-" * 55)
        
        variacoes_blocos = [2**i for i in range(3, 11)] # 8 ate 1024
        resultados = []

        for num_linhas in variacoes_blocos:
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
                'blocos': num_linhas,
                'tamanho_bytes': num_linhas * tam_bloco,
                'hit_rate': hit_rate_global,
                'amat': amat,
                'leituras_mp': simulador.leituras_mp,
                'escritas_mp': simulador.escritas_mp
            })

        if not resultados:
            print("[AVISO] Nenhum dado valido processado. Verifique o arquivo dados.txt.")
            return

        print("\nTabela 2 - Resultados da Simulacao")
        colunas = f"{'Numero de Blocos':<18} | {'Taxa de Acerto':<15} | {'Tempo medio de Acesso (ns)':<26} | {'Leituras na MP':<15} | {'Escritas na MP':<15}"
        print(colunas)
        print("-" * 99)
        for res in resultados:
            print(f"{res['blocos']:<18} | {res['hit_rate']:>13.4f}% | {res['amat']:>26.4f} | {res['leituras_mp']:<15} | {res['escritas_mp']:<15}")
        print("-" * 99)

        self._plotar_grafico(resultados)

    def _plotar_grafico(self, resultados):
        eixo_x = [res['tamanho_bytes'] for res in resultados]
        eixo_y = [res['hit_rate'] for res in resultados]
        rotulos = [f"{res['blocos']} blk\n({res['tamanho_bytes']}B)" for res in resultados]

        plt.figure(figsize=(10, 5))
        plt.plot(eixo_x, eixo_y, marker='o', linestyle='-', color='#1f77b4', linewidth=2)
        plt.title('Impacto do Tamanho da Cache na Taxa de Acerto (Experimento 1)', fontweight='bold')
        plt.xlabel('Tamanho da Cache (Blocos e Bytes)')
        plt.ylabel('Taxa de Acerto (%)')
        plt.xscale('log', base=2)
        plt.xticks(eixo_x, rotulos)
        plt.ylim(-5, 105)
        plt.grid(True, linestyle='--', alpha=0.5)
        
        for i, val in enumerate(eixo_y):
            plt.annotate(f"{val:.4f}%", (eixo_x[i], eixo_y[i]), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)
        plt.tight_layout()
        plt.savefig('grafico_experimento_1.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("\n[INFO] Grafico salvo em: grafico_experimento_1.png")