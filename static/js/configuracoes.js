function confirmarSalvar() {
    if (confirm("Tem certeza de que deseja salvar as alterações na conta?")) {
        alert("Alterações salvas com sucesso!");
        window.location.href = "index.html";
    } else {
        alert("As alterações não foram salvas.");
    }
}

function confirmarExcluir() {
    if (confirm("Tem certeza de que deseja excluir a conta? Esta ação não pode ser desfeita.")) {
        alert("Conta excluída com sucesso!");
        window.location.href = "cadastro.html";
    } else {
        alert("A conta não foi excluída.");
    }
}