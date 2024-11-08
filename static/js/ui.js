import api from "./api.js";

let quill;

function inicializarEditorQuill() {
  quill = new Quill('#quillInput', {
    theme: "snow",
    placeholder: "Descreva sua pergunta...",
    modules: {
      toolbar: [
        [{ 'header': [1, 2, false] }],
        ['bold', 'italic', 'underline'],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        ['link', 'image'],
        ['clean']
      ]
    }
  });
}

const ui = {
  async renderizarSolicitacoes() {
    const listaSolicitacoes = document.getElementById("lista-solicitacoes");

    try {
      const solicitacoes = await api.buscarSolicitacoes();
      listaSolicitacoes.innerHTML = "";

      solicitacoes.forEach(solicitacao => {
        const statusTexto = solicitacao.status === 1 ? "Resolvido" : "Não resolvido";
        const statusClasse = solicitacao.status === 1 ? "resolvido" : "nao-resolvido";

        listaSolicitacoes.innerHTML += `
          <div class="question-box">
            <a href="resposta.html" class="question-link">${solicitacao.titulo}</a>
            <span class="info">Enviado por: Usuário ${solicitacao.id_usuario} às ${new Date(solicitacao.data_criacao).toLocaleString()}</span>
            <span class="status ${statusClasse}">
              Status: ${statusTexto}
            </span>
          </div>
        `;
      });
    } catch (error) {
      console.error("Erro ao buscar solicitações:", error);
    }
  },

  async adicionarSolicitacao() {
    const titulo = document.getElementById("titulo").value;
    const categoria = parseInt(document.getElementById("categoria").value, 10);
    const descricao = quill.root.innerHTML;

    const novaSolicitacao = {
      titulo: titulo,
      id_categoria: categoria,
      descricao: descricao,
      status: 0, 
      data_criacao: new Date().toISOString()
    };

    try {
      const response = await fetch("http://localhost:3000/solicitacoes", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(novaSolicitacao)
      });

      if (response.ok) {
        alert("Solicitação adicionada com sucesso!");
        
        document.getElementById("titulo").value = "";
        document.getElementById("categoria").selectedIndex = 0;
        quill.setText('');
        
        await ui.renderizarSolicitacoes();
      } else {
        alert("Erro ao adicionar solicitação.");
      }
    } catch (error) {
      console.error("Erro:", error);
      alert("Erro ao se comunicar com o servidor.");
    }
  }
};

function inicializar() {
  inicializarEditorQuill();
  document.getElementById("submit-button").addEventListener("click", () => ui.adicionarSolicitacao());
}

window.addEventListener("load", inicializar);

export default ui;
