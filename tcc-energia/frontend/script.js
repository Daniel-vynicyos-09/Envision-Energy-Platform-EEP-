const ctx = document.getElementById('grafico').getContext('2d');

let chart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Consumo',
            data: []
        }]
    }
});

async function atualizar() {
    let res = await fetch("http://127.0.0.1:8000/historico");
    let data = await res.json();

    chart.data.labels = data.dados.map((_, i) => i);
    chart.data.datasets[0].data = data.dados;

    chart.update();
}

setInterval(atualizar, 2000);v