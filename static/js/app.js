/* CryptoSim — Main JS */

// ── THEME ──
const btnTheme = document.getElementById('btnTheme');
const html = document.documentElement;
let theme = localStorage.getItem('theme') || 'dark';
html.setAttribute('data-theme', theme);

btnTheme.addEventListener('click', () => {
  theme = theme === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
  btnTheme.textContent = theme === 'dark' ? '◐' : '◑';
});

// ── MODES (per algo) ──
const modes = { caesar: 'encrypt', vigenere: 'encrypt', affine: 'encrypt', hill: 'encrypt', playfair: 'encrypt' };

document.querySelectorAll('.mode-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const algo = btn.dataset.algo;
    const mode = btn.dataset.mode;
    modes[algo] = mode;
    document.querySelectorAll(`.mode-btn[data-algo="${algo}"]`).forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

// ── NAV PILLS ──
document.querySelectorAll('.nav-pill').forEach(pill => {
  pill.addEventListener('click', () => {
    document.querySelectorAll('.nav-pill').forEach(p => p.classList.remove('active'));
    pill.classList.add('active');
  });
});
document.querySelectorAll('.algo-tag').forEach(tag => {
  tag.addEventListener('click', () => {
    const el = document.getElementById(tag.dataset.algo);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  });
});

// ── CAESAR SHIFT VISUAL ──
function adjustShift(algo, delta) {
  const inp = document.getElementById(`${algo}-shift`);
  let val = parseInt(inp.value) + delta;
  val = Math.max(1, Math.min(25, val));
  inp.value = val;
  if (algo === 'caesar') updateShiftVisual();
}

function updateShiftVisual() {
  const shift = parseInt(document.getElementById('caesar-shift').value) || 3;
  const container = document.getElementById('caesar-shift-visual');
  const alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  container.innerHTML = '';
  alpha.split('').forEach((c, i) => {
    const div = document.createElement('div');
    div.className = 'shift-cell' + (i < shift ? ' active' : '');
    div.textContent = c;
    container.appendChild(div);
  });
}
document.getElementById('caesar-shift').addEventListener('input', updateShiftVisual);
updateShiftVisual();

// ── VIGENÈRE KEY DISPLAY ──
document.getElementById('vigenere-key').addEventListener('input', function () {
  const container = document.getElementById('vigenere-key-display');
  container.innerHTML = '';
  this.value.replace(/[^a-zA-Z]/g, '').toUpperCase().split('').forEach(c => {
    const span = document.createElement('span');
    span.className = 'key-char';
    span.textContent = c;
    container.appendChild(span);
  });
});

// ── HILL MATRIX ──
let hillSize = 2;
const PRESET_MATRICES = {
  2: [[3, 3], [2, 5]],
  3: [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
};

function setMatrixSize(n) {
  hillSize = n;
  document.querySelectorAll('.size-btn').forEach((b, i) => {
    b.classList.toggle('active', (i === 0 && n === 2) || (i === 1 && n === 3));
  });
  renderMatrixInputs(PRESET_MATRICES[n]);
}

function renderMatrixInputs(values) {
  const container = document.getElementById('hill-matrix-input');
  container.innerHTML = '';
  for (let r = 0; r < hillSize; r++) {
    const row = document.createElement('div');
    row.className = 'matrix-row';
    for (let c = 0; c < hillSize; c++) {
      const inp = document.createElement('input');
      inp.type = 'number'; inp.className = 'matrix-cell-input';
      inp.value = (values && values[r] && values[r][c] !== undefined) ? values[r][c] : 0;
      inp.min = 0; inp.max = 25;
      row.appendChild(inp);
    }
    container.appendChild(row);
  }
}

function setPresetMatrix() { renderMatrixInputs(PRESET_MATRICES[hillSize]); }

function getHillMatrix() {
  const inputs = document.querySelectorAll('.matrix-cell-input');
  const mat = [];
  for (let r = 0; r < hillSize; r++) {
    const row = [];
    for (let c = 0; c < hillSize; c++) {
      row.push(parseInt(inputs[r * hillSize + c].value) || 0);
    }
    mat.push(row);
  }
  return mat;
}

setMatrixSize(2);

// ── PLAYFAIR MATRIX PREVIEW ──
function updatePlayfairMatrix() {
  const key = document.getElementById('playfair-key').value;
  if (!key) return;
  fetch('/api/playfair_matrix', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key })
  }).then(r => r.json()).then(data => {
    renderPlayfairMini(data.matrix);
  });
}

function renderPlayfairMini(matrix) {
  const container = document.getElementById('playfair-preview-matrix');
  container.innerHTML = '';
  matrix.forEach(row => row.forEach(cell => {
    const div = document.createElement('div');
    div.className = 'pf-cell-mini';
    div.textContent = cell;
    container.appendChild(div);
  }));
}
updatePlayfairMatrix();

// ── LOADING ──
function setLoading(on) {
  document.getElementById('loadingOverlay').classList.toggle('active', on);
}

// ── TOAST ──
function showToast(msg, duration = 2200) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), duration);
}

// ── HISTORY ──
document.getElementById('btnHistory').addEventListener('click', openHistory);

function openHistory() {
  fetch('/api/history').then(r => r.json()).then(data => {
    renderHistory(data.history);
    document.getElementById('historyPanel').classList.add('open');
    document.getElementById('historyOverlay').classList.add('open');
  });
}

function closeHistory() {
  document.getElementById('historyPanel').classList.remove('open');
  document.getElementById('historyOverlay').classList.remove('open');
}

function clearHistory() {
  fetch('/api/history/clear', { method: 'POST' }).then(() => {
    document.getElementById('historyList').innerHTML = '<div class="history-empty">Riwayat kosong</div>';
    showToast('Riwayat dihapus');
  });
}

function renderHistory(history) {
  const list = document.getElementById('historyList');
  if (!history.length) { list.innerHTML = '<div class="history-empty">Belum ada riwayat operasi</div>'; return; }
  list.innerHTML = history.slice().reverse().map(h => `
    <div class="history-entry">
      <div class="history-entry-header">
        <span class="history-algo">${h.algorithm}</span>
        <span class="${h.mode === 'encrypt' ? 'history-mode-enc' : 'history-mode-dec'}">${h.mode === 'encrypt' ? '🔐 Enkripsi' : '🔓 Dekripsi'}</span>
        <span class="history-time">${h.timestamp}</span>
      </div>
      <div class="history-row"><span class="history-label">IN:</span><span class="history-val">${escHtml(h.input)}</span></div>
      <div class="history-row"><span class="history-label">OUT:</span><span class="history-val">${escHtml(h.output)}</span></div>
    </div>`).join('');
}

function escHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

// ── COPY ──
function copyText(text) {
  navigator.clipboard.writeText(text).then(() => showToast('✓ Disalin ke clipboard'));
}

// ── STEPS TOGGLE ──
function toggleSteps(id) {
  const body = document.getElementById(id);
  const icon = document.getElementById(id + '-icon');
  if (body.classList.toggle('collapsed')) {
    icon.textContent = '▼';
  } else {
    icon.textContent = '▲';
  }
}

// ── MAIN PROCESS ──
async function processCipher(algo) {
  const mode = modes[algo];
  let payload = { mode };
  let endpoint = `/api/${algo}`;

  switch (algo) {
    case 'caesar':
      payload.text = document.getElementById('caesar-text').value;
      payload.shift = parseInt(document.getElementById('caesar-shift').value);
      break;
    case 'vigenere':
      payload.text = document.getElementById('vigenere-text').value;
      payload.key = document.getElementById('vigenere-key').value;
      break;
    case 'affine':
      payload.text = document.getElementById('affine-text').value;
      payload.a = parseInt(document.getElementById('affine-a').value);
      payload.b = parseInt(document.getElementById('affine-b').value);
      break;
    case 'hill':
      payload.text = document.getElementById('hill-text').value;
      payload.matrix = getHillMatrix();
      break;
    case 'playfair':
      payload.text = document.getElementById('playfair-text').value;
      payload.key = document.getElementById('playfair-key').value;
      break;
  }

  setLoading(true);
  try {
    const resp = await fetch(endpoint, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();
    setLoading(false);

    if (data.error) {
      showError(algo, data.error);
      return;
    }

    renderResult(algo, data, mode);
  } catch (e) {
    setLoading(false);
    showError(algo, 'Terjadi kesalahan koneksi: ' + e.message);
  }
}

function showError(algo, msg) {
  const container = document.getElementById(`${algo}-result`);
  container.classList.remove('hidden');
  container.innerHTML = `<div class="error-box">⚠ ${escHtml(msg)}</div>`;
}

function renderResult(algo, data, mode) {
  const container = document.getElementById(`${algo}-result`);
  container.classList.remove('hidden');

  const output = mode === 'encrypt' ? (data.ciphertext || '') : (data.plaintext || '');
  const outputLabel = mode === 'encrypt' ? '🔐 Hasil Enkripsi' : '🔓 Hasil Dekripsi';

  let stepsHtml = '';
  switch (algo) {
    case 'caesar':
    case 'affine':
      stepsHtml = renderStepsCaesarAffine(data.steps);
      break;
    case 'vigenere':
      stepsHtml = renderStepsVigenere(data.steps);
      break;
    case 'hill':
      stepsHtml = renderStepsHill(data, mode);
      break;
    case 'playfair':
      stepsHtml = renderStepsPlayfair(data, mode);
      break;
  }

  container.innerHTML = `
    <div class="result-output">
      <div class="result-label">
        <span>${outputLabel}</span>
        <button class="btn-copy" onclick="copyText('${escHtml(output)}')">Salin</button>
      </div>
      <div class="result-text">${escHtml(output)}</div>
    </div>
    <div class="steps-panel">
      <div class="steps-header" onclick="toggleSteps('steps-${algo}')">
        <h4>📐 Langkah Perhitungan (${data.steps ? data.steps.length : 0} langkah)</h4>
        <span class="steps-toggle" id="steps-${algo}-icon">▲</span>
      </div>
      <div class="steps-body" id="steps-${algo}">${stepsHtml}</div>
    </div>`;
}

// ── CAESAR / AFFINE STEPS ──
function renderStepsCaesarAffine(steps) {
  return steps.map(s => {
    if (s.title) return `<div class="step-info">${escHtml(s.content)}</div>`;
    const skip = s.formula && s.formula.includes('skip');
    return `<div class="step-item${skip ? ' step-skip' : ''}">
      <span class="step-char">${escHtml(String(s.char))}</span>
      <span class="step-key">${escHtml(String(s.x))}</span>
      <span class="step-formula">${escHtml(s.formula)}</span>
      <span class="step-result">${escHtml(String(s.result))}</span>
    </div>`;
  }).join('');
}

// ── VIGENÈRE STEPS ──
function renderStepsVigenere(steps) {
  return steps.map(s => {
    if (s.title) return `<div class="step-info">${escHtml(s.content)}</div>`;
    const skip = s.formula && s.formula.includes('skip');
    return `<div class="step-item${skip ? ' step-skip' : ''}">
      <span class="step-char">${escHtml(String(s.char))}</span>
      <span class="step-key">${escHtml(String(s.key_char))}</span>
      <span class="step-formula">${escHtml(s.formula)}</span>
      <span class="step-result">${escHtml(String(s.result))}</span>
    </div>`;
  }).join('');
}

// ── HILL STEPS ──
function renderStepsHill(data, mode) {
  const n = data.key_matrix.length;
  let html = '';

  // Key matrix
  html += `<div class="two-matrix">`;
  html += `<div class="matrix-block"><div class="matrix-label">Matriks Kunci K</div>${renderMatrixDisplay(data.key_matrix)}</div>`;
  if (data.inv_matrix) {
    html += `<div class="matrix-block"><div class="matrix-label">Matriks Invers K⁻¹ (mod 26)</div>${renderMatrixDisplay(data.inv_matrix)}</div>`;
  }
  html += `</div>`;

  if (data.padded_text) {
    html += `<div class="info-box">Teks yang diproses: "${escHtml(data.padded_text)}" (${n} huruf per blok)</div>`;
  }

  data.steps.forEach(s => {
    if (s.title) {
      html += `<div class="step-info">${escHtml(s.content)}</div>`;
      return;
    }
    html += `<div class="block-step">
      <div class="block-title">Blok: "${escHtml(s.block)}" → [${s.vec.join(', ')}]</div>
      <div class="block-calc">${s.calc_rows.map(r => escHtml(r)).join('\n')}</div>
      <div class="block-result-text">→ "${escHtml(s.result)}"</div>
    </div>`;
  });
  return html;
}

function renderMatrixDisplay(mat) {
  return `<div class="matrix-display">${mat.map(row =>
    `<div class="matrix-display-row">${row.map(v =>
      `<div class="matrix-display-cell">${v}</div>`).join('')}</div>`).join('')}</div>`;
}

// ── PLAYFAIR STEPS ──
function renderStepsPlayfair(data, mode) {
  const matrix = data.matrix;
  let html = '';

  // Full matrix
  html += `<div class="info-box">Tabel Playfair 5×5 (J digabung dengan I)</div>`;
  html += `<div class="playfair-matrix-full" id="pf-full-matrix">`;
  matrix.forEach(row => row.forEach(c => {
    html += `<div class="pf-cell-full">${c}</div>`;
  }));
  html += `</div>`;

  if (data.prepared) {
    html += `<div class="info-box">Teks setelah persiapan: "${escHtml(data.prepared)}"</div>`;
  }

  data.steps.forEach((s, idx) => {
    if (s.title) {
      html += `<div class="step-info">${escHtml(s.content)}</div>`;
      return;
    }
    html += `<div class="pair-step">
      <div class="pair-header">
        <span class="pair-chars">${escHtml(s.pair)}</span>
        <span>→</span>
        <span class="pair-enc">${escHtml(s.result)}</span>
      </div>
      <div class="pair-rule">${escHtml(s.rule)}</div>
    </div>`;
  });
  return html;
}

// ── KEYBOARD SHORTCUTS ──
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeHistory();
});
