// New clean client script for search/add UI
const chatBox = document.getElementById('chat-box');
const btnSearch = document.getElementById('btn-search');
const btnAdd = document.getElementById('btn-add');
const searchArea = document.getElementById('search-area');
const addArea = document.getElementById('add-area');
const inputProduct = document.getElementById('input-product');
const searchGo = document.getElementById('search-go');
const addProduct = document.getElementById('add-product');
const addPrice = document.getElementById('add-price');
const addGo = document.getElementById('add-go');

function prependMessage(html){
  const div = document.createElement('div');
  div.innerHTML = html;
  chatBox.prepend(div);
}

function clearOld(){
  const old = chatBox.querySelectorAll('.table-container, .no-results');
  old.forEach(n => n.remove());
}

btnSearch.addEventListener('click', ()=>{
  addArea.classList.add('hidden');
  searchArea.classList.toggle('hidden');
  inputProduct.focus();
});

btnAdd.addEventListener('click', ()=>{
  searchArea.classList.add('hidden');
  addArea.classList.toggle('hidden');
  addProduct.focus();
});

searchGo.addEventListener('click', async ()=>{
  const q = inputProduct.value.trim();
  if(!q) return;
  clearOld();
  prependMessage(`<div class="no-results">Buscando "${q}"...</div>`);
  try{
    const res = await fetch('/api/price?producto=' + encodeURIComponent(q));
    const data = await res.json();
    clearOld();
    if (res.status === 200 && Array.isArray(data.results)) {
      // Mostrar todos los matches con precio
      let rows = '';
      data.results.forEach(r => {
        rows += `<tr><td>${r.producto}</td><td>${r.precio ?? 'N/A'}</td></tr>`;
      });
      const html = `<div class="table-container"><table class="result-table"><thead><tr><th>Producto</th><th>Precio</th></tr></thead><tbody>${rows}</tbody></table><div class="no-results">Matches totales: ${data.matches}</div></div>`;
      prependMessage(html);
    } else if (res.status === 200 && data.mensaje) {
      prependMessage(`<div class="no-results">${data.mensaje}</div>`);
    } else if (res.status === 404) {
      prependMessage(`<div class="no-results">Producto no encontrado.</div>`);
    } else {
      prependMessage(`<div class="no-results">Error: ${JSON.stringify(data)}</div>`);
    }
  }catch(err){
    clearOld();
    prependMessage(`<div class="no-results">Error de conexión: ${err}</div>`);
  }
});

addGo.addEventListener('click', async ()=>{
  const prod = addProduct.value.trim();
  const precio = addPrice.value;
  if(!prod || !precio) return;
  try{
    const res = await fetch('/api/add_item',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({producto:prod, precio:parseFloat(precio)})});
    const data = await res.json();
    if(res.status === 201){
      prependMessage(`<div class="no-results">Item agregado: ${data.producto} — ${data.precio}</div>`);
      addProduct.value=''; addPrice.value=''; addArea.classList.add('hidden');
    } else {
      prependMessage(`<div class="no-results">Error: ${JSON.stringify(data)}</div>`);
    }
  }catch(err){
    prependMessage(`<div class="no-results">Error: ${err}</div>`);
  }
});

// initial message
prependMessage('<div class="no-results">👋 Bienvenido — usa Buscar o Agregar</div>');
