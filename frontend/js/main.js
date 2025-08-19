// Configuração da API
const API_URL = 'http://localhost:8000';

// Função para fazer requisições à API
async function fetchAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erro na requisição:', error);
        throw error;
    }
}

// Inicialização da aplicação
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Teste de conexão com a API
        const response = await fetchAPI('/');
        console.log('Conexão com API:', response.message);
    } catch (error) {
        console.error('Erro ao conectar com a API:', error);
    }
});
