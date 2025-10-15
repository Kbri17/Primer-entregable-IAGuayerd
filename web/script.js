async function fetchResumen(){
  const res = await fetch('/api/resumen');
  return res.json();
}

async function fetchCategorias(){
  const res = await fetch('/api/categorias');
  return res.json();
}

async function fetchSucursal(nombre){
  const res = await fetch('/api/sucursal/' + encodeURIComponent(nombre));
  return res.json();
}

function renderResumen(data){
  const tbody = document.querySelector('#tabla-resumen tbody');
  tbody.innerHTML='';
  data.forEach(r => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td style="text-align:left">${r.mes}</td><td>${r.alimentos.toLocaleString()}</td><td>${r.limpieza.toLocaleString()}</td><td>${r.total.toLocaleString()}</td>`
    tbody.appendChild(tr);
  });
}

function renderCategorias(data){
  const el = document.getElementById('totales');
  el.innerHTML = `<div class="chip">Alimentos: ${data.Alimentos.toLocaleString()}</div><div class="chip">Limpieza: ${data.Limpieza.toLocaleString()}</div>`
}

function renderSucursal(data){
  const container = document.getElementById('resultado-sucursal');
  if(!data || !data.ventas) return container.innerText='No se encontraron datos';
  let html = `<h3>${data.sucursal}</h3><table style="width:100%"><thead><tr><th style="text-align:left">Mes</th><th>Alimentos</th><th>Limpieza</th></tr></thead><tbody>`;
  data.ventas.forEach(v => {
    html += `<tr><td style="text-align:left">${v.mes}</td><td>${v.alimentos.toLocaleString()}</td><td>${v.limpieza.toLocaleString()}</td></tr>`;
  });
  html += `</tbody></table>`;
  container.innerHTML = html;
}

document.getElementById('btn-buscar').addEventListener('click', async ()=>{
  const name = document.getElementById('input-sucursal').value.trim();
  if(!name) return alert('Ingresa un nombre de sucursal');
  const data = await fetchSucursal(name);
  renderSucursal(data);
});

// inicializar
(async ()=>{
  renderResumen(await fetchResumen());
  renderCategorias(await fetchCategorias());
})();
