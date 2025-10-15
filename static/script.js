const chatBox = document.getElementById("chat-box");
const inputArea = document.getElementById("input-area");
const inputText = document.getElementById("input-text");
const btnEnviar = document.getElementById("btn-enviar");

function addMessage(text, sender = "bot", isOptions = false) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.innerHTML = text;
  if (isOptions) div.dataset.options = "true";
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function cargarOpciones() {
  const res = await fetch("/api/opciones");
  const opciones = await res.json();
  // Crear contenedor para opciones (se marca como options para poder eliminarlo al seleccionar)
  let html = "<div class=\"options-list\">";
  opciones.forEach(op => {
    // pasar texto también para mostrar como mensaje de usuario
    const safeText = op.texto.replace(/'/g, "\\'");
    html += `<div class="option" onclick="handleOption('${op.id}','${safeText}')">${op.texto}</div>`;
  });
  html += "</div>";
  addMessage(html, 'bot', true);
}

async function handleOption(id, text) {
  // quitar las opciones visibles (si las hay)
  const optionMsgs = document.querySelectorAll('[data-options="true"]');
  optionMsgs.forEach(n => n.remove());

  // Mostrar la opción seleccionada como mensaje del usuario
  if (text) addMessage(text, 'user');

  if (id === "resumen_mes") {
    const res = await fetch("/api/resumen_mes");
    const data = await res.json();
    let html = `<div class="table-container"><table class="result-table"><thead><tr><th>Mes</th><th>Ventas</th></tr></thead><tbody>`;
    data.forEach(r => html += `<tr><td>${r.fecha || r.Mes || r[Object.keys(r)[0]]}</td><td>${r.ventas}</td></tr>`);
    html += `</tbody></table></div>`;
    addMessage(html);
    // volver a mostrar opciones debajo
    setTimeout(cargarOpciones, 300);
  } 
  else if (id === "por_medio") {
    const res = await fetch("/api/por_medio");
    const data = await res.json();
    let html = `<div class="table-container"><table class="result-table"><thead><tr><th>Medio de Pago</th><th>Cantidad</th></tr></thead><tbody>`;
    data.forEach(r => html += `<tr><td>${r["Medio de Pago"]}</td><td>${r.Cantidad}</td></tr>`);
    html += `</tbody></table></div>`;
    addMessage(html);
    setTimeout(cargarOpciones, 300);
  } 
  else if (id === "buscar_cliente") {
    inputArea.style.display = "flex";
    addMessage("🔎 Escribe el nombre del cliente que deseas buscar:");
    // focus en input
    setTimeout(()=> inputText.focus(), 50);
  }
}

btnEnviar.addEventListener("click", async () => {
  const nombre = inputText.value.trim();
  if (!nombre) return;
  addMessage(nombre, "user");
  const res = await fetch("/api/buscar_cliente", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ nombre })
  });
  const data = await res.json();
  inputText.value = "";
  if (data.mensaje) {
    addMessage(`<div class="table-container"><div class="no-results">${data.mensaje}</div></div>`);
  } else if (Array.isArray(data)) {
    let html = `<div class="table-container"><table class="result-table"><thead><tr><th>ID</th><th>Fecha</th><th>Cliente</th><th>Medio Pago</th></tr></thead><tbody>`;
    data.forEach(r => {
      html += `<tr><td>${r.id_venta}</td><td>${r.fecha || ''}</td><td>${r.nombre_cliente}</td><td>${r.medio_pago}</td></tr>`;
    });
    html += `</tbody></table></div>`;
    addMessage(html);
  }
  inputArea.style.display = "none";
  // re-renderizar las opciones automáticamente
  setTimeout(cargarOpciones, 300);
});

// Inicializar chat
addMessage("👋 ¡Bienvenido al Chat de Ventas Interactivo!");
cargarOpciones();
