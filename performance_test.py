import joblib
import dash
from dash import dcc, html
import plotly.graph_objects as go
import hashlib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

# Carrega o último modelo
model_path = "modelos/modelo_20241106_060145.joblib"
model = joblib.load(model_path)

# Gera dados de teste (substitua por seus dados reais)
X_test = np.linspace(0, 10, 100)
y_test = 2 * X_test + 1 + np.random.normal(0, 1, 100)
y_pred = model.predict(X_test.reshape(-1,1))

# Dados adicionais para outros gráficos
feature_importance = np.random.rand(5)  # Importância das features (aleatório)
residuals = y_test - y_pred
predictions_df = pd.DataFrame({'y_test': y_test, 'y_pred': y_pred})

# Calcula métricas
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Cria os gráficos
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=X_test, y=y_test, mode='markers', name='Valores Reais'))
fig1.add_trace(go.Scatter(x=X_test, y=y_pred, mode='lines', name='Previsões'))
fig1.update_layout(title='Previsões vs. Valores Reais', xaxis_title='X', yaxis_title='Y')

fig2 = go.Figure()
fig2.add_trace(go.Histogram(x=residuals, name='Resíduos'))
fig2.update_layout(title='Histograma dos Resíduos', xaxis_title='Resíduos', yaxis_title='Frequência')

fig3 = go.Figure()
fig3.add_trace(go.Box(y=residuals, name='Resíduos'))
fig3.update_layout(title='Boxplot dos Resíduos', yaxis_title='Resíduos')

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=X_test, y=residuals, mode='markers', name='Resíduos'))
fig4.update_layout(title='Resíduos vs. X', xaxis_title='X', yaxis_title='Resíduos')

fig5 = go.Figure()
fig5.add_trace(go.Bar(x=np.arange(len(feature_importance)), y=feature_importance, name='Importância das Features'))
fig5.update_layout(title='Importância das Features', xaxis_title='Feature', yaxis_title='Importância')

fig6 = go.Figure()
fig6.add_trace(go.Scatter(x=predictions_df['y_test'], y=predictions_df['y_pred'], mode='markers', name='Previsões vs. Reais'))
fig6.update_layout(title='Dispersão Previsões vs. Reais', xaxis_title='Valores Reais', yaxis_title='Previsões')

fig7 = go.Figure()
fig7.add_trace(go.Violin(y=residuals, name='Resíduos'))
fig7.update_layout(title='Violin Plot dos Resíduos', yaxis_title='Resíduos')

fig8 = go.Figure()
fig8.add_trace(go.Scatter(x=np.arange(len(y_test)), y=y_test, mode='lines+markers', name='Valores Reais'))
fig8.add_trace(go.Scatter(x=np.arange(len(y_pred)), y=y_pred, mode='lines+markers', name='Previsões'))
fig8.update_layout(title='Série Temporal de Previsões', xaxis_title='Tempo', yaxis_title='Valor')

fig9 = go.Figure()
fig9.add_trace(go.Scatter(x=X_test, y=abs(residuals), mode='markers', name='Erro Absoluto'))
fig9.update_layout(title='Erro Absoluto vs. X', xaxis_title='X', yaxis_title='Erro Absoluto')

fig10 = go.Figure()
fig10.add_trace(go.Scatter(x=X_test, y=y_test/y_pred, mode='markers', name='Razão'))
fig10.update_layout(title='Razão entre Valores Reais e Previsões', xaxis_title='X', yaxis_title='Razão')


# Gera um hash único para o nome do arquivo
hash_object = hashlib.sha256(str(mse).encode())
unique_hash = hash_object.hexdigest()

# Salva os gráficos
fig1.write_image(f"performance/grafico_1_{unique_hash}.png")
fig2.write_image(f"performance/grafico_2_{unique_hash}.png")
fig3.write_image(f"performance/grafico_3_{unique_hash}.png")
fig4.write_image(f"performance/grafico_4_{unique_hash}.png")
fig5.write_image(f"performance/grafico_5_{unique_hash}.png")
fig6.write_image(f"performance/grafico_6_{unique_hash}.png")
fig7.write_image(f"performance/grafico_7_{unique_hash}.png")
fig8.write_image(f"performance/grafico_8_{unique_hash}.png")
fig9.write_image(f"performance/grafico_9_{unique_hash}.png")
fig10.write_image(f"performance/grafico_10_{unique_hash}.png")

print(f"Gráficos salvos na pasta performance com hash: {unique_hash}")
print(f"MSE: {mse}")
print(f"R2: {r2}")
