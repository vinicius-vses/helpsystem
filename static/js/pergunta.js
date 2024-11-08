function enviarPergunta() {
    alert("Obrigado por enviar sua pergunta!");
  
    window.location.href = "index.html";
  }
  
  document.getElementById("submit-button").addEventListener("click", enviarPergunta);
  