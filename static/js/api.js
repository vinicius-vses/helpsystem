const URL_BASE = "http://localhost:3000";

const api = {
  async buscarSolicitacoes() {
    try {
      const response = await fetch(`${URL_BASE}/solicitacoes`);
      return await response.json();
    } catch (error) {
      alert("Erro!");
      throw error;    
    }
  },
};

export default api;
