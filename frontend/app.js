const askForm = document.querySelector("#ask-form");
const answerOutput = document.querySelector("#answer-output");
const contextList = document.querySelector("#context-list");
const contextForm = document.querySelector("#context-form");
const contextUsed = document.querySelector("#context-used");

const API_BASE_URL = "http://127.0.0.1:8000";

// Load context on page load for default user
document.addEventListener("DOMContentLoaded", () => {
  const userId = document.querySelector("#user-id").value;
  loadContext(userId);
});

// Auto-detect and save context from question
async function detectAndSaveContext(question, userId) {
  const q = question.toLowerCase();
  const saves = [];

  // Detect audience
  if (/como principiante|para principiantes|soy nuevo|explicame como|explica como/i.test(question)) {
    saves.push(saveContext(userId, "audience", "explicar como principiante"));
  }

  // Detect language
  const langMatch = question.match(/en (español|ingles|inglés|portugués|frances|francés)/i);
  if (langMatch) {
    saves.push(saveContext(userId, "language", langMatch[1].toLowerCase()));
  }

  // Detect examples request
  if (/con ejemplos|dame ejemplos|ejemplos de|por ejemplo|ejemplo/i.test(question)) {
    saves.push(saveContext(userId, "include_examples", "si"));
  }

  await Promise.all(saves);
}

async function saveContext(userId, key, value) {
  await fetch(`${API_BASE_URL}/api/context`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_id: userId, key, value }),
  });
}

// Ask question
askForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(askForm);
  const userId = formData.get("user_id");
  const question = formData.get("question");
  
  answerOutput.textContent = "Consultando...";
  contextUsed.style.display = "none";
  
  try {
    // Auto-detect and save context from the question
    await detectAndSaveContext(question, userId);
    
    // Now ask the question (backend will use the auto-saved context)
    const response = await fetch(`${API_BASE_URL}/api/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, question }),
    });
    const result = await response.json();
    
    // Show answer
    answerOutput.innerHTML = `<p class="answer-text">${escapeHtml(result.answer)}</p>`;
    
    // Show context used
    if (result.context_used && result.context_used.length > 0) {
      contextUsed.style.display = "block";
      contextUsed.innerHTML = `<span class="badge">Contexto usado: ${result.context_used.join(", ")}</span>`;
    } else {
      contextUsed.style.display = "none";
    }
    
    // Reload context panel (now shows auto-saved items!)
    await loadContext(userId);
  } catch (error) {
    answerOutput.textContent = `No se pudo conectar con el backend: ${error.message}`;
  }
});

// Save context
contextForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const userId = document.querySelector("#user-id").value;
  const formData = new FormData(contextForm);
  const key = formData.get("key");
  const value = formData.get("value");
  
  if (!value.trim()) return;
  
  try {
    await fetch(`${API_BASE_URL}/api/context`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, key, value }),
    });
    
    // Reload context list
    await loadContext(userId);
    
    // Reset form
    contextForm.querySelector("#context-value").value = "";
    
    // Close details
    const details = contextForm.closest("details");
    if (details) details.open = false;
  } catch (error) {
    console.error("Error saving context:", error);
  }
});

// Load context for user
async function loadContext(userId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/context?user_id=${encodeURIComponent(userId)}`);
    const result = await response.json();
    renderContext(result.context || []);
  } catch (error) {
    contextList.innerHTML = '<p class="empty-state">El modulo CAG no esta disponible.</p>';
  }
}

// Render context items
function renderContext(items) {
  if (!items || items.length === 0) {
    contextList.innerHTML = '<p class="empty-state">Sin contexto guardado.</p>';
    return;
  }
  
  contextList.innerHTML = items.map(item => `
    <div class="context-item">
      <div class="context-item-info">
        <span class="context-key">${escapeHtml(item.key)}</span>
        <span class="context-value">${escapeHtml(item.value)}</span>
      </div>
    </div>
  `).join("");
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
