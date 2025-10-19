const chatBox = document.getElementById("chat-box");
const inputArea = document.getElementById("input-area");
const inputText = document.getElementById("input-text");
const btnEnviar = document.getElementById("btn-enviar");

// Acción actual del input: "buscar_cliente" | "buscar_producto" | null
let currentAction = null;

function addMessage(text, sender = "bot", isOptions = false) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.innerHTML = text;
  if (isOptions) div.dataset.options = "true";
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function cargarOpciones() {
  currentAction = null;
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

  // Reset acción por defecto
  currentAction = null;

  if (id === "resumen_mes") {
    const res = await fetch("/api/resumen_mes");
    const data = await res.json();
    let html = `<div class="table-container"><table class="result-table"><thead><tr><th>Mes</th><th>Ventas</th></tr></thead><tbody>`;
    data.forEach(r => html += `<tr><td>${r.fecha || r.Mes || r[Object.keys(r)[0]]}</td><td>${r.ventas}</td></tr>`);
    html += `</tbody></table></div>`;
    addMessage(html);
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
    currentAction = "buscar_cliente";
    inputText.placeholder = "Nombre del cliente...";
    inputArea.style.display = "flex";
    addMessage("🔎 Escribe el nombre del cliente que deseas buscar:");
    setTimeout(()=> inputText.focus(), 50);
  }
  else if (id === "productos_top" || id === "productos_mas_cantidades") {
    const res = await fetch(`/api/${id}`);
    const data = await res.json();
    let html = `<div class="table-container"><table class="result-table"><thead><tr>`;
    Object.keys(data[0] || {}).forEach(k => html += `<th>${k}</th>`);
    html += `</tr></thead><tbody>`;
    data.forEach(r => {
      html += `<tr>${Object.values(r).map(v => `<td>${v}</td>`).join('')}</tr>`;
    });
    html += `</tbody></table></div>`;
    addMessage(html);
    setTimeout(cargarOpciones, 300);
  }
  else if (id === "ticket_promedio") {
    const res = await fetch("/api/ticket_promedio");
    const data = await res.json();
    addMessage(`💵 Ticket promedio: <b>S/ ${data.ticket_promedio}</b><br>🧾 Total de ventas: ${data.total_ventas}`);
    setTimeout(cargarOpciones, 300);
  }
  else if (id === "buscar_producto") {
    currentAction = "buscar_producto";
    inputText.placeholder = "Nombre del producto...";
    inputArea.style.display = "flex";
    addMessage("🔎 Escribe el nombre del producto que deseas buscar:");
    setTimeout(()=> inputText.focus(), 50);
  }
}

btnEnviar.addEventListener("click", async () => {
  const nombre = inputText.value.trim();
  if (!nombre) return;
  addMessage(nombre, "user");

  // Determinar endpoint según acción actual (por defecto cliente)
  const endpoint = currentAction === "buscar_producto" ? "/api/buscar_producto" : "/api/buscar_cliente";

  const res = await fetch(endpoint, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ nombre })
  });
  const data = await res.json();
  inputText.value = "";

  if (data.error) {
    addMessage(`<div class="table-container"><div class="no-results">${data.error}</div></div>`);
  } else if (data.mensaje) {
    addMessage(`<div class="table-container"><div class="no-results">${data.mensaje}</div></div>`);
  } else if (Array.isArray(data)) {
    // Si hay filas, renderizar tabla tomando las claves de la primera fila
    if (data.length === 0) {
      addMessage(`<div class="table-container"><div class="no-results">No se encontraron resultados.</div></div>`);
    } else {
      let html = `<div class="table-container"><table class="result-table"><thead><tr>`;
      Object.keys(data[0]).forEach(k => html += `<th>${k}</th>`);
      html += `</tr></thead><tbody>`;
      data.forEach(r => {
        html += `<tr>${Object.values(r).map(v => `<td>${v}</td>`).join('')}</tr>`;
      });
      html += `</tbody></table></div>`;
      addMessage(html);
    }
  } else {
    addMessage(`<div class="table-container"><div class="no-results">Respuesta inesperada del servidor.</div></div>`);
  }

  // Reset estado del input
  inputArea.style.display = "none";
  currentAction = null;
  setTimeout(cargarOpciones, 300);
});

// Inicializar chat
addMessage("👋 ¡Bienvenido al Chat de Ventas Interactivo!");
cargarOpciones();
