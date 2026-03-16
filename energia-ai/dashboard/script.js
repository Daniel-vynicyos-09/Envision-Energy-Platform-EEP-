const ctx = document.getElementById('grafico');

const chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Consumo',
            data: [],
            borderWidth: 2
        }]
    }
});

async function atualizar() {

    const resposta = await fetch("http://127.0.0.1:8000/dados");
    const dados = await resposta.json();

    console.log(dados); // para debug

    chart.data.labels = dados.tempo;
    chart.data.datasets[0].data = dados.consumo;

    chart.update();
}

atualizar(); // ← executa imediatamente

setInterval(atualizar, 3000);