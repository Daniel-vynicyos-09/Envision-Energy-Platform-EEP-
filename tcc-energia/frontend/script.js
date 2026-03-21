const API = "http://192.168.1.2:8000"; // ajuste se necessário

// Referências seguras ao DOM (verifica existência)
const valorEl = document.getElementById("valor");
const previsaoEl = document.getElementById("previsao");
const dicaEl = document.getElementById("dica");
const statusEl = document.getElementById("status");
const ultimoTempoEl = document.getElementById("ultimoTempo");
const apiUrlEl = document.getElementById("apiUrl");

if (apiUrlEl) apiUrlEl.innerText = API;

// Contexto do canvas; protegemos caso canvas não exista
const canvas = document.getElementById('grafico');
if (!canvas) {
  console.error('Canvas #grafico não encontrado');
}
const ctx = canvas ? canvas.getContext('2d') : null;

// Função segura para criar gradiente — retorna cor sólida se chartArea indisponível
function createGradientSafe(ctx, chartArea) {
  if (!ctx || !chartArea) {
    // chartArea ainda não inicializado; retorna fallback
    return 'rgba(34,197,94,0.6)';
  }
  const g = ctx.createLinearGradient(0, chartArea.top, 0, chartArea.bottom);
  g.addColorStop(0, 'rgba(34,197,94,0.85)');
  g.addColorStop(0.4, 'rgba(6,182,212,0.6)');
  g.addColorStop(1, 'rgba(6,182,212,0.08)');
  return g;
}

// Configura o Chart apenas se ctx estiver disponível
let chart = null;
if (ctx) {
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Consumo (kW)',
        data: [],
        borderColor: '#22c55e', // cor inicial (será ajustada dinamicamente)
        pointRadius: 3,
        pointHoverRadius: 6,
        pointBackgroundColor: '#fff',
        pointBorderWidth: 2,
        tension: 0.35,
        fill: true,
        // backgroundColor precisa acessar chartArea de forma segura
        backgroundColor: function(context) {
          // context.chart.chartArea pode ser undefined durante primeiro render
          const chartArea = context.chart && context.chart.chartArea;
          return createGradientSafe(context.chart.ctx, chartArea);
        },
        borderWidth: 2.5
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          mode: 'index',
          intersect: false,
          padding: 10,
          backgroundColor: '#071028'
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: '#9fb0d4' }
        },
        y: {
          beginAtZero: true,
          ticks: { color: '#9fb0d4' },
          grid: { color: 'rgba(255,255,255,0.03)' }
        }
      },
      interaction: { mode: 'nearest', axis: 'x', intersect: false }
    }
  });
} else {
  console.warn('Chart não inicializado porque o contexto do canvas não foi encontrado.');
}

function getStatus(valor) {
  if (valor < 120) {
    return { texto: "Consumo baixo ✅", cor: "#10B981", textColor: "#03121A" };
  } else if (valor < 170) {
    return { texto: "Consumo moderado ⚠️", cor: "#F59E0B", textColor: "#03121A" };
  } else {
    return { texto: "Consumo alto 🚨", cor: "#EF4444", textColor: "#FFF" };
  }
}

function formatTime(date = new Date()){
  return date.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit',second:'2-digit'});
}

async function atualizar(){
  try{
    const res = await fetch(API + "/historico");
    if(!res.ok) {
      console.warn('Resposta não OK de /historico:', res.status);
      return;
    }
    const data = await res.json();
    const dados = Array.isArray(data.dados) ? data.dados : [];

    if(dados.length === 0) {
      console.warn('Nenhum dado retornado em /historico');
      return;
    }

    const maxPoints = 60;
    const sliced = dados.slice(-maxPoints);

    if (chart) {
      chart.data.labels = sliced.map((_, i) => i);
      chart.data.datasets[0].data = sliced;

      // atualizar cor de borda dinamicamente com base no último valor
      const last = sliced[sliced.length - 1] ?? 0;
      let borderColor = '#22c55e';
      if (last >= 170) borderColor = '#ef4444';
      else if (last >= 120) borderColor = '#f59e0b';
      chart.data.datasets[0].borderColor = borderColor;

      chart.update();
    }

    const ultimo = sliced[sliced.length - 1];

    if (valorEl) valorEl.innerText = Number(ultimo).toFixed(1);
    if (ultimoTempoEl) ultimoTempoEl.innerText = formatTime();

    // enviar valor para previsão / IA (se endpoint existir)
    try {
      const resposta = await fetch(API + "/dados", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({ valor: ultimo })
      });
      if (resposta.ok) {
        const ia = await resposta.json();
        if (previsaoEl) previsaoEl.innerText = ia.previsao != null ? Number(ia.previsao).toFixed(1) : "--";
        if (dicaEl) dicaEl.innerText = ia.dica ?? "--";
      } else {
        console.warn('/dados retornou status', resposta.status);
      }
    } catch(err) {
      console.warn('Erro ao chamar /dados:', err);
    }

    const status = getStatus(ultimo);
    if (statusEl) {
      statusEl.innerText = status.texto;
      statusEl.style.background = status.cor;
      statusEl.style.color = status.textColor;
    }
  } catch(err){
    console.error('Erro em atualizar():', err);
  }
}

// Primeira atualização e loop
if (chart) {
  atualizar();
  setInterval(atualizar, 3000);
} else {
  // tenta atualizar mesmo sem gráfico; útil para debug em telas pequenas
  atualizar();
  setInterval(atualizar, 3000);
}