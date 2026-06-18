import sys

def executar_simulacao(arquivo_dados, tam_bloco, num_linhas, associatividade, politica_escrita, politica_substituicao):
    """
    Motor genérico da simulação. Tenta importar a cache de forma segura,
    processa o arquivo de trace linha por linha e captura erros para não fechar do nada.
    """
    try:
        from cache import CacheAssociativaConjunto
    except ImportError:
        print("\n[ERRO] Não foi possível encontrar o arquivo 'cache.py'. Verifique se ele está nesta pasta!")
        return None

    try:
        simulador = CacheAssociativaConjunto(
            tam_linha=tam_bloco,
            num_linhas=num_linhas,
            associatividade=associatividade,
            politica_escrita=politica_escrita,
            politica_substituicao=politica_substituicao
        )
    except Exception as e:
        print(f"\n[ERRO de Configuração] Falha ao criar a Cache (Bloco: {tam_bloco}B, Linhas: {num_linhas}, Vias: {associatividade}). Motivo: {e}")
        return None
    
    try:
        with open(arquivo_dados, 'r') as arquivo:
            for linha in arquivo:
                linha_limpa = linha.strip()
                if not linha_limpa:
                    continue
                partes = linha_limpa.split()
                if len(partes) == 2:
                    endereco_hex, operacao = partes
                    if operacao in ['R', 'W', 'r', 'w']:
                        simulador.processar_acesso(endereco_hex, operacao.upper())
    except FileNotFoundError:
        print(f"\n[ERRO] O arquivo '{arquivo_dados}' nao foi encontrado nesta pasta!")
        return None
    except Exception as e:
        print(f"\n[ERRO de Leitura] Falha ao processar o arquivo de dados. Motivo: {e}")
        return None

    return simulador

def menu_principal():
    arquivo_trace = "dados.txt"
    
    while True:
        print("\n" + "=" * 60)
        print("          SIMULADOR DE CACHE ASSOCIATIVA - MENU          ")
        print("=" * 60)
        print("1. Executar Experimento 1 (Impacto do Tamanho da Cache)")
        print("2. Executar Experimento 2 (Impacto do Tamanho do Bloco)")
        print("3. Executar Experimento 3 (Impacto da Associatividade)")
        print("4. Executar Experimento 4 (Impacto da Politica de Substituicao)")
        print("5. Executar Experimento 5 (Largura de Banda da Memoria)")
        print("0. Sair")
        print("-" * 60)
        
        opcao = input("Escolha uma opcao: ").strip()
        
        if opcao == "1":
            print("\n[INFO] Solicitando Experimento 1...")
            try:
                from experimento_1 import Experimento1
                exp1 = Experimento1(arquivo_trace)
                exp1.executar()
            except Exception as e:
                print(f"[ERRO] Falha ao rodar Experimento 1: {e}")
        elif opcao == "2":
            print("\n[INFO] Solicitando Experimento 2...")
            try:
                from experimento_2 import Experimento2
                exp2 = Experimento2(arquivo_trace)
                exp2.executar()
            except Exception as e:
                print(f"[ERRO] Falha ao rodar Experimento 2: {e}")
        elif opcao == "3":
            print("\n[INFO] Solicitando Experimento 3...")
            try:
                from experimento_3 import Experimento3
                exp3 = Experimento3(arquivo_trace)
                exp3.executar()
            except Exception as e:
                print(f"[ERRO] Falha ao rodar Experimento 3: {e}")
        elif opcao == "4":
            print("\n[INFO] Solicitando Experimento 4...")
            try:
                from experimento_4 import Experimento4
                exp4 = Experimento4(arquivo_trace)
                exp4.executar()
            except Exception as e:
                print(f"[ERRO] Falha ao rodar Experimento 4: {e}")
        elif opcao == "5":
            print("\n[INFO] Solicitando Experimento 5...")
            try:
                from experimento_5 import Experimento5
                exp5 = Experimento5(arquivo_trace)
                exp5.executar()
            except Exception as e:
                print(f"[ERRO] Falha ao rodar Experimento 5: {e}")
        elif opcao == "0":
            print("\nSaindo do simulador. Até logo!")
            break
        else:
            print("\nOpcao invalida! Tente novamente.")

if __name__ == "__main__":
    menu_principal()