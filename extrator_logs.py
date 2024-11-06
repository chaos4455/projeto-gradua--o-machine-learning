import glob
import os

def extrair_logs(diretorio_raiz, padrao_log, arquivo_saida):
    """
    Extrai logs de vários arquivos, os concatena em um único arquivo e remove os originais.

    Args:
        diretorio_raiz: O diretório raiz onde os arquivos de log estão localizados.
        padrao_log: O padrão de nome de arquivo para os arquivos de log (e.g., "pipeline_logs_*.log").
        arquivo_saida: O nome do arquivo para salvar os logs concatenados.
    """
    try:
        arquivos_log = glob.glob(os.path.join(diretorio_raiz, padrao_log))
        if not arquivos_log:
            print(f"Nenhum arquivo de log encontrado com o padrão '{padrao_log}' em '{diretorio_raiz}'.")
            return

        with open(os.path.join(diretorio_raiz, arquivo_saida), 'w') as saida:
            for arquivo in arquivos_log:
                try:
                    with open(arquivo, 'r') as log:
                        saida.write(f"--- Logs de {arquivo} ---\n")
                        saida.write(log.read())
                        saida.write("\n\n")
                except Exception as e:
                    print(f"Erro ao ler o arquivo '{arquivo}': {e}")
                finally:
                    try:
                        os.remove(arquivo)
                        print(f"Arquivo '{arquivo}' removido com sucesso.")
                    except OSError as e:
                        print(f"Erro ao remover o arquivo '{arquivo}': {e}")


        print(f"Logs extraídos e salvos em '{os.path.join(diretorio_raiz, arquivo_saida)}'.")

    except Exception as e:
        print(f"Erro geral: {e}")


if __name__ == "__main__":
    diretorio_raiz = "."  # Diretório atual
    padrao_log = "pipeline_logs_*.log"
    arquivo_saida = "logs_concatenados.txt"
    extrair_logs(diretorio_raiz, padrao_log, arquivo_saida)
