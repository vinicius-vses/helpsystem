function enviarPergunta() {
    alert("Obrigado por enviar sua pergunta!");

    window.location.href = "/";
  }

  document.getElementById("submit-button").addEventListener("click", enviarPergunta);
