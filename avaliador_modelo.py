import requests
from sklearn.metrics import mean_squared_error, r2_score
import hashlib
import numpy as np
import pandas as pd

def avaliar_modelo_api(X_test, y_test):
    """Avalia um modelo de machine learning usando a API e MSE e R².

    Args:
        X_test (numpy.ndarray): Dados de teste (apenas a coluna 'idade').
        y_test (numpy.ndarray): Valores reais correspondentes aos dados de teste.

    Returns:
        tuple: Uma tupla contendo o MSE, o R², e um relatório textual.
    """
    try:
        y_pred = []
        for idade in X_test:
            response = requests.post("http://0.0.0.0:12779/predict", json={"idade": int(idade)})
            response.raise_for_status()
            predicao = response.json()["predicao"]
            y_pred.append(predicao)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        #Relatório
        relatorio = f"""
        Relatório de Avaliação do Modelo (via API):

        MSE: {mse:.2f}
        R²: {r2:.2f}

        Avaliação:
        """
        if mse < 1 and r2 > 0.9:
            relatorio += "O modelo apresenta excelente performance."
        elif mse < 5 and r2 > 0.7:
            relatorio += "O modelo apresenta boa performance."
        elif mse < 10 and r2 > 0.5:
            relatorio += "O modelo apresenta performance razoável. Considerar melhorias."
        else:
            relatorio += "O modelo apresenta baixa performance. Necessário ajustes significativos."

        return mse, r2, relatorio
    except requests.exceptions.RequestException as e:
        return None, None, f"Erro ao conectar à API: {e}"
    except Exception as e:
        return None, None, f"Erro na avaliação do modelo: {e}"


#Exemplo de uso:

# Dados de teste (substitua pelos seus dados reais)
X_test = np.linspace(20, 60, 100).reshape(-1,1) # Idade entre 20 e 60
y_test = 2 * np.linspace(20, 60, 100) + 1 + np.random.normal(0, 100, 100) # Salário com ruído

mse, r2, relatorio = avaliar_modelo_api(X_test, y_test)

print(relatorio)
