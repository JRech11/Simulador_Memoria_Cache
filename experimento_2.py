import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import main

class Experimento2:
    def __init__(self, arquivo_dados):
        self.arquivo_dados = arquivo_dados

    def executar(self):
        # Parâmetros Fixos do Experimento 2 (8 KB totais)
        tamanho_total_cache_bytes = 8192  
        politica_escrita = 0              # Write-Through
        politica_substituicao = 'LRU'
        associatividade = 2               # 2-way
        
        print("\n9. Anexo A:")
        print("Tabela 3 - Parametros da Simulacao (Impacto do Bloco)")
        print(f"{'Parametro':<30} | {'Valor':<20}")
        print("-" * 55)
        print(f"{'Tamanho Total da Cache':<30} | {tamanho_total_cache_bytes // 1024} KB ({tamanho_total_cache_bytes} bytes)")
        print(f"{'Politica de Escrita':<30} | write-through")
        print(f"{'Algoritmo de Substituicao':<30} | {politica_substituicao}")
        print(f"{'Associatividade':<30} | {associatividade} blocos")
        print("-" * 55)
        
        # Variando o bloco de 8 bytes até 4096 bytes
        variacoes_bloco = [2**i for i in range(3, 13)] 
        resultados = []

        for tam_bloco in variacoes_bloco:
            num_linhas = tamanho_total_cache_bytes // tam_bloco
            
            # Validação física: Não dá para ter menos linhas do que vias de associatividade
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
                'tam_bloco': tam_bloco,
                'num_linhas': num_linhas,
                'hit_rate': hit_rate_global,
                'amat': amat,
                'leituras_mp': simulador.leituras_mp,
                'escritas_mp': simulador.escritas_mp
            })

        if not resultados:
            print("\n[AVISO] Nenhum dado valido foi processado pelas simulacoes. Verifique se o arquivo 'dados.txt' contem dados formatados.")
            return

        print("\nTabela 4 - Resultados da Simulacao (Impacto do Bloco)")
        colunas = f"{'Tamanho do Bloco':<18} | {'Taxa de Acerto':<15} | {'Tempo medio de Acesso (ns)':<26} | {'Leituras na MP':<15} | {'Escritas na MP':<15}"
        print(colunas)
        print("-" * 99)
        for res in resultados:
            print(f"{res['tam_bloco']:<18} | {res['hit_rate']:>13.4f}% | {res['amat']:>26.4f} | {res['leituras_mp']:<15} | {res['escritas_mp']:<15}")
        print("-" * 99)

        self._plotar_grafico(resultados)

    def _plotar_grafico(self, resultados):
        eixo_x = [res['tam_bloco'] for res in resultados]
        eixo_y = [res['hit_rate'] for res in resultados]
        rotulos = [f"{res['tam_bloco']}B\n({res['num_linhas']} lin)" for res in resultados]

        plt.figure(figsize=(11, 5))
        plt.plot(eixo_x, eixo_y, marker='o', linestyle='-', color='#2ca02c', linewidth=2)
        plt.title('Impacto do Tamanho do Bloco na Taxa de Acerto (Experimento 2)', fontweight='bold')
        plt.xlabel('Tamanho do Bloco (Bytes e Linhas Restantes)')
        plt.ylabel('Taxa de Acerto (%)')
        plt.xscale('log', base=2)
        plt.xticks(eixo_x, rotulos)
        plt.ylim(-5, 105)
        plt.grid(True, linestyle='--', alpha=0.5)
        
        for i, val in enumerate(eixo_y):
            plt.annotate(f"{val:.4f}%", (eixo_x[i], eixo_y[i]), textcoords="offset points", xytext=(0,8), ha='center', fontsize=8)
        plt.tight_layout()
        plt.savefig('grafico_experimento_2.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("\n[INFO] Grafico salvo em: grafico_experimento_2.png")