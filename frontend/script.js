const featuresInput = document.getElementById('features');
const predictButton = document.getElementById('predict');
const resultDiv = document.getElementById('result');

predictButton.addEventListener('click', async () => {
  const features = featuresInput.value.split(',').map(Number);
  if (features.length === 0) {
    resultDiv.textContent = "Por favor, insira as features.";
    return;
  }
  try {
    const response = await fetch('http://localhost:8004/predizer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ features })
    });
    if (!response.ok) {
      const errorData = await response.json();
      resultDiv.textContent = `Erro: ${errorData.detail}`;
      return;
    }
    const data = await response.json();
    resultDiv.textContent = `Predição: ${data.prediction}`;
  } catch (error) {
    resultDiv.textContent = `Erro: ${error}`;
  }
});
