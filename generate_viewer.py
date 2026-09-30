import json, shutil

with open('embedded_data.json', 'r', encoding='utf-8') as f:
    embedded_str = f.read()

with open('SBCN26078924_192621.jdps', 'r', encoding='utf-8') as f:
    orig_jdps = json.load(f)
    img1_b64 = orig_jdps.get('image1', '')
    img2_b64 = orig_jdps.get('image2', '')

html_content = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Visualizador 3D - Dimensionador TLD870</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090d16;
      --card-bg: rgba(15, 22, 36, 0.92);
      --card-hover: rgba(22, 32, 52, 0.95);
      --border: rgba(255, 255, 255, 0.12);
      --accent-cyan: #00f0ff;
      --accent-magenta: #ff007b;
      --accent-green: #00ffaa;
      --accent-amber: #ffaa00;
      --text-main: #f0f4f8;
      --text-muted: #8a99ad;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      user-select: none;
    }}
    body {{
      background-color: var(--bg);
      color: var(--text-main);
      font-family: 'Outfit', sans-serif;
      overflow: hidden;
      height: 100vh;
      width: 100vw;
    }}
    #canvas-container {{
      width: 100vw;
      height: 100vh;
      position: absolute;
      top: 0;
      left: 0;
      z-index: 1;
    }}
    .hud-panel {{
      position: absolute;
      z-index: 10;
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.65);
      pointer-events: auto;
      transition: border-color 0.2s;
    }}
    .hud-panel:hover {{
      border-color: rgba(255, 255, 255, 0.22);
    }}
    .top-bar {{
      top: 20px;
      left: 20px;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .badge {{
      background: rgba(0, 240, 255, 0.15);
      color: var(--accent-cyan);
      border: 1px solid rgba(0, 240, 255, 0.35);
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.5px;
      text-transform: uppercase;
    }}
    h1 {{
      font-size: 17px;
      font-weight: 700;
      letter-spacing: -0.3px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    .btn-load {{
      background: linear-gradient(135deg, #00f0ff 0%, #0088ff 100%);
      color: #050b14;
      font-weight: 700;
      border: none;
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 15px rgba(0, 240, 255, 0.35);
    }}
    .btn-load:hover {{
      transform: translateY(-1px);
      box-shadow: 0 6px 20px rgba(0, 240, 255, 0.5);
    }}
    #file-input {{
      display: none;
    }}
    .info-card {{
      top: 85px;
      left: 20px;
      width: 320px;
      padding: 16px;
    }}
    .info-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-top: 10px;
    }}
    .info-item {{
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.06);
      padding: 8px 12px;
      border-radius: 8px;
    }}
    .info-item .label {{
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 2px;
    }}
    .info-item .value {{
      font-size: 15px;
      font-weight: 600;
      color: #fff;
    }}
    .info-item .value span {{
      font-size: 11px;
      font-weight: 400;
      color: var(--text-muted);
      margin-left: 2px;
    }}
    .controls-card {{
      top: 20px;
      right: 20px;
      width: 305px;
      max-height: calc(100vh - 40px);
      overflow-y: auto;
      padding: 18px;
    }}
    .section-title {{
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-muted);
      margin-bottom: 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .btn-group {{
      display: flex;
      gap: 6px;
      margin-bottom: 12px;
    }}
    button {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 8px 12px;
      border-radius: 8px;
      font-family: inherit;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      flex: 1;
    }}
    button:hover {{
      background: rgba(255, 255, 255, 0.12);
      border-color: rgba(255, 255, 255, 0.25);
    }}
    button.active {{
      background: rgba(0, 240, 255, 0.18);
      border-color: var(--accent-cyan);
      color: var(--accent-cyan);
    }}
    .toggle-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 0;
      font-size: 13px;
    }}
    .toggle-row input[type="checkbox"] {{
      cursor: pointer;
      accent-color: var(--accent-cyan);
      width: 16px;
      height: 16px;
    }}
    .slider-row {{
      margin-top: 8px;
    }}
    .slider-row label {{
      font-size: 12px;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      margin-bottom: 4px;
    }}
    input[type="range"] {{
      width: 100%;
      accent-color: var(--accent-cyan);
    }}
    .filter-box {{
      background: rgba(0, 255, 170, 0.04);
      border: 1px solid rgba(0, 255, 170, 0.2);
      border-radius: 10px;
      padding: 10px 12px;
      margin-top: 10px;
      margin-bottom: 12px;
    }}
    .points-card {{
      bottom: 20px;
      left: 20px;
      width: 480px;
      max-height: 250px;
      overflow-y: auto;
      padding: 16px;
    }}
    .points-card table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12px;
      margin-top: 6px;
    }}
    .points-card th {{
      text-align: left;
      padding: 6px 8px;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border);
      font-weight: 600;
    }}
    .points-card td {{
      padding: 6px 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }}
    .dot-indicator {{
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      margin-right: 6px;
    }}
    #image-modal {{
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      z-index: 100;
      background: var(--card-bg);
      backdrop-filter: blur(20px);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      display: none;
      max-width: 92vw;
      max-height: 92vh;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.85);
    }}
    .img-container {{
      display: flex;
      gap: 16px;
      margin-top: 16px;
      overflow: auto;
    }}
    .img-container img {{
      max-width: 460px;
      max-height: 520px;
      border-radius: 10px;
      border: 1px solid var(--border);
      object-fit: contain;
      background: #000;
    }}
    #drop-overlay {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 240, 255, 0.15);
      backdrop-filter: blur(8px);
      border: 3px dashed var(--accent-cyan);
      z-index: 999;
      display: none;
      align-items: center;
      justify-content: center;
      pointer-events: none;
    }}
    #drop-overlay .drop-box {{
      background: var(--card-bg);
      padding: 30px 50px;
      border-radius: 20px;
      border: 1px solid var(--accent-cyan);
      font-size: 20px;
      font-weight: 700;
      color: var(--accent-cyan);
      box-shadow: 0 20px 50px rgba(0, 240, 255, 0.3);
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    #toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #111a2d;
      border: 1px solid var(--accent-cyan);
      color: #fff;
      padding: 12px 20px;
      border-radius: 10px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      z-index: 1000;
      font-size: 13px;
      font-weight: 500;
      display: none;
      align-items: center;
      gap: 10px;
      animation: fadeIn 0.3s ease;
    }}
    @keyframes fadeIn {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
  </style>
</head>
<body>

  <div id="drop-overlay">
    <div class="drop-box">
      <span>📥</span> Suelta aquí el archivo .jdps o .ply para visualizarlo
    </div>
  </div>

  <div id="toast"></div>

  <div id="canvas-container"></div>

  <!-- Top Bar -->
  <div class="hud-panel top-bar">
    <span class="badge">TLD870 Pallet 3D</span>
    <h1>ID: <span class="mono" id="pallet-id" style="color: var(--accent-cyan);">SBCN26078924</span></h1>
    <input type="file" id="file-input" accept=".jdps,.json,.ply" onchange="handleFileSelect(this.files)">
    <button class="btn-load" onclick="document.getElementById('file-input').click()">
      📁 Cargar Archivo (.jdps / .ply)
    </button>
  </div>

  <!-- Telemetry Card -->
  <div class="hud-panel info-card">
    <div class="section-title">Dimensiones y Telemetría</div>
    <div class="info-grid">
      <div class="info-item">
        <div class="label">Longitud (L)</div>
        <div class="value" id="val-length">145 <span>cm</span></div>
      </div>
      <div class="info-item">
        <div class="label">Anchura (W)</div>
        <div class="value" id="val-width">117 <span>cm</span></div>
      </div>
      <div class="info-item">
        <div class="label">Altura (H)</div>
        <div class="value" id="val-height">84 <span>cm</span></div>
      </div>
      <div class="info-item">
        <div class="label">Volumen</div>
        <div class="value" id="val-vol">1425.1 <span>L</span></div>
      </div>
      <div class="info-item">
        <div class="label">Peso Neto</div>
        <div class="value" id="val-weight">446.0 <span>kg</span></div>
      </div>
      <div class="info-item">
        <div class="label">Orientación</div>
        <div class="value" id="val-rot">88.0 <span>°</span></div>
      </div>
      <!-- Remontabilidad (Non-Stackable) -->
      <div class="info-item" style="grid-column: span 2; display: flex; align-items: center; justify-content: space-between; padding: 10px 14px;">
        <span class="label" style="font-size: 13px; font-weight: 600; color: #fff;">Remontabilidad</span>
        <div id="val-stackable-badge" class="badge" style="font-size: 12px; padding: 6px 14px; background: rgba(255, 0, 123, 0.18); color: var(--accent-magenta); border: 1px solid rgba(255, 0, 123, 0.4);">🚫 NO REMONTABLE</div>
      </div>
    </div>
    <button id="btn-photos" style="margin-top: 12px; width: 100%;" onclick="togglePhotos()">
      📷 Ver Fotos de Cámaras
    </button>
  </div>

  <!-- Controls Card -->
  <div class="hud-panel controls-card">
    <div class="section-title">Vistas de Cámara</div>
    <div class="btn-group">
      <button onclick="setView('iso')" class="active" id="btn-iso">3D Iso</button>
      <button onclick="setView('top')" id="btn-top">Superior</button>
      <button onclick="setView('front')" id="btn-front">Frontal</button>
      <button onclick="setView('side')" id="btn-side">Lateral</button>
    </div>

    <!-- Filtro de Suelo Section -->
    <div class="filter-box">
      <div class="section-title" style="margin-bottom: 6px; color: var(--accent-green);">
        <span>Filtro de Suelo</span>
        <span style="font-size:10px; color:var(--text-muted);">Corte Z</span>
      </div>
      <div class="toggle-row">
        <span style="font-weight:600;">Ocultar suelo por debajo</span>
        <input type="checkbox" id="chk-hide-ground" onchange="toggleGroundFilter()">
      </div>
      <div class="slider-row">
        <label>Corte Suelo Z: <span id="lbl-cut-z" class="mono" style="color:var(--accent-green);">0 mm</span></label>
        <input type="range" id="rng-cut-z" min="-50" max="150" step="5" value="0" oninput="updateGroundCut(this.value)">
      </div>
      <div class="btn-group" style="margin-top: 8px; margin-bottom: 0;">
        <button onclick="setGroundCutPreset(0)" style="font-size:11px; padding:5px 4px;">Z = 0 mm</button>
        <button onclick="setGroundCutPreset(15)" style="font-size:11px; padding:5px 4px;">Z = 15 mm</button>
        <button onclick="setGroundCutPreset(-999)" style="font-size:11px; padding:5px 4px;">Ver Todo</button>
      </div>
    </div>

    <div class="section-title">Capas 3D</div>
    <div class="toggle-row">
      <span>Nube Puntos (<span id="pts-count" class="mono">62k</span>)</span>
      <input type="checkbox" id="chk-points" checked onchange="toggleLayer('points')">
    </div>
    <div class="toggle-row">
      <span>Bounding Box 3D</span>
      <input type="checkbox" id="chk-box" checked onchange="toggleLayer('box')">
    </div>
    <div class="toggle-row">
      <span>5 Puntos de Contacto</span>
      <input type="checkbox" id="chk-touching" checked onchange="toggleLayer('touching')">
    </div>
    <div class="toggle-row">
      <span>4 Esquinas Base</span>
      <input type="checkbox" id="chk-corners" checked onchange="toggleLayer('corners')">
    </div>
    <div class="toggle-row">
      <span>Plano Rejilla</span>
      <input type="checkbox" id="chk-grid" checked onchange="toggleLayer('grid')">
    </div>

    <div class="slider-row">
      <label>Tamaño Puntos: <span id="lbl-pt-size" class="mono">2.5</span></label>
      <input type="range" id="rng-pt-size" min="1" max="8" step="0.5" value="2.5" oninput="updatePointSize(this.value)">
    </div>

    <div class="slider-row" style="margin-top: 10px;">
      <label>Modo de Color</label>
      <select id="sel-color" onchange="updateColorMode(this.value)" style="width:100%; background:#1c2538; color:#fff; border:1px solid var(--border); padding:6px; border-radius:6px;">
        <option value="height">Gradiente Altura (Z)</option>
        <option value="intensity">Intensidad Láser</option>
        <option value="cyan">Monocromo Neón</option>
      </select>
    </div>
  </div>

  <!-- Key Points Table Card -->
  <div class="hud-panel points-card">
    <div class="section-title">
      <span>9 PUNTOS ESTRUCTURALES</span>
      <span style="font-size:10px; color:var(--accent-cyan);">Coordenadas en mm</span>
    </div>
    <table>
      <thead>
        <tr>
          <th>Punto</th>
          <th>Tipo / Cara</th>
          <th class="mono">X</th>
          <th class="mono">Y</th>
          <th class="mono">Z</th>
        </tr>
      </thead>
      <tbody id="tbl-points-body"></tbody>
    </table>
  </div>

  <!-- Camera Photos Modal -->
  <div id="image-modal">
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h2 style="font-size:18px;">Fotos Capturadas por el Dimensionador</h2>
      <button onclick="togglePhotos()" style="flex:none; padding:4px 10px;">✕ Cerrar</button>
    </div>
    <div class="img-container">
      <div>
        <div style="font-size:12px; margin-bottom:6px; color:var(--text-muted);">Cámara 1</div>
        <img id="modal-img-1" src="data:image/jpeg;base64,{img1_b64}" alt="Cámara 1">
      </div>
      <div>
        <div style="font-size:12px; margin-bottom:6px; color:var(--text-muted);">Cámara 2</div>
        <img id="modal-img-2" src="data:image/jpeg;base64,{img2_b64}" alt="Cámara 2">
      </div>
    </div>
  </div>

  <script>
    let currentData = {embedded_str};

    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x090d16);

    const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 10, 15000);
    const renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    const controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.maxDistance = 8000;

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.85);
    scene.add(ambientLight);
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
    dirLight.position.set(1000, 2000, 1500);
    scene.add(dirLight);

    const groupPoints = new THREE.Group();
    const groupBox = new THREE.Group();
    const groupTouching = new THREE.Group();
    const groupCorners = new THREE.Group();
    const groupGrid = new THREE.Group();

    scene.add(groupPoints);
    scene.add(groupBox);
    scene.add(groupTouching);
    scene.add(groupCorners);
    scene.add(groupGrid);

    function toThree(x, y, z) {{
      return new THREE.Vector3(x, z, -y);
    }}

    const gridHelper = new THREE.GridHelper(3000, 30, 0x1e293b, 0x131d2e);
    gridHelper.position.y = 0;
    groupGrid.add(gridHelper);

    const axesHelper = new THREE.AxesHelper(350);
    axesHelper.position.y = 1;
    groupGrid.add(axesHelper);

    let pointCloudGeometry = null;
    let pointCloudMaterial = null;
    let pointCloudObject = null;

    let allPointsData = [];
    let currentFilteredVertices = [];
    let currentFilteredIntensities = [];

    function showToast(msg, isSuccess = true) {{
      const t = document.getElementById('toast');
      t.innerHTML = (isSuccess ? '✅ ' : '⚠️ ') + msg;
      t.style.display = 'flex';
      setTimeout(() => {{ t.style.display = 'none'; }}, 4000);
    }}

    function getColorTurbo(t) {{
      let r = 0, g = 0, b = 0;
      if (t < 0.25) {{
        const f = t / 0.25;
        r = 0.1; g = 0.3 + 0.6 * f; b = 0.9;
      }} else if (t < 0.5) {{
        const f = (t - 0.25) / 0.25;
        r = 0.1 + 0.4 * f; g = 0.9; b = 0.9 - 0.7 * f;
      }} else if (t < 0.75) {{
        const f = (t - 0.5) / 0.25;
        r = 0.5 + 0.5 * f; g = 0.9 - 0.2 * f; b = 0.2 - 0.2 * f;
      }} else {{
        const f = (t - 0.75) / 0.25;
        r = 1.0; g = 0.7 - 0.6 * f; b = 0.1;
      }}
      return {{ r, g, b }};
    }}

    function applyGroundFilter() {{
      const hideGround = document.getElementById('chk-hide-ground').checked;
      const cutZ = parseFloat(document.getElementById('rng-cut-z').value) || 0;
      const colorMode = document.getElementById('sel-color').value;
      const maxZ = currentData.height || 835;

      const total = allPointsData.length;
      if (total === 0) return;

      const filteredPos = [];
      const filteredCol = [];
      currentFilteredVertices = [];
      currentFilteredIntensities = [];

      for (let i = 0; i < total; i++) {{
        const p = allPointsData[i];
        if (hideGround && p.z < cutZ) continue;

        const pos = toThree(p.x, p.y, p.z);
        filteredPos.push(pos.x, pos.y, pos.z);
        currentFilteredVertices.push(pos);
        currentFilteredIntensities.push(p.intensity);

        if (colorMode === 'height') {{
          const t = Math.max(0, Math.min(1, p.z / maxZ));
          const col = getColorTurbo(t);
          filteredCol.push(col.r, col.g, col.b);
        }} else if (colorMode === 'intensity') {{
          const v = (p.intensity || 128) / 255;
          filteredCol.push(v, v, v);
        }} else {{
          filteredCol.push(0.0, 0.94, 1.0);
        }}
      }}

      const numPoints = filteredPos.length / 3;
      groupPoints.clear();

      pointCloudGeometry = new THREE.BufferGeometry();
      pointCloudGeometry.setAttribute('position', new THREE.Float32BufferAttribute(filteredPos, 3));
      pointCloudGeometry.setAttribute('color', new THREE.Float32BufferAttribute(filteredCol, 3));

      const ptSize = parseFloat(document.getElementById('rng-pt-size').value) || 2.5;
      pointCloudMaterial = new THREE.PointsMaterial({{
        size: ptSize,
        vertexColors: true,
        sizeAttenuation: true
      }});

      pointCloudObject = new THREE.Points(pointCloudGeometry, pointCloudMaterial);
      groupPoints.add(pointCloudObject);

      if (hideGround) {{
        document.getElementById('pts-count').innerText = numPoints.toLocaleString() + ' (sin suelo)';
      }} else {{
        document.getElementById('pts-count').innerText = numPoints.toLocaleString();
      }}
    }}

    function toggleGroundFilter() {{
      applyGroundFilter();
    }}

    function updateGroundCut(val) {{
      document.getElementById('lbl-cut-z').innerText = val + ' mm';
      if (!document.getElementById('chk-hide-ground').checked) {{
        document.getElementById('chk-hide-ground').checked = true;
      }}
      applyGroundFilter();
    }}

    function setGroundCutPreset(val) {{
      if (val === -999) {{
        document.getElementById('chk-hide-ground').checked = false;
        applyGroundFilter();
      }} else {{
        document.getElementById('chk-hide-ground').checked = true;
        document.getElementById('rng-cut-z').value = val;
        document.getElementById('lbl-cut-z').innerText = val + ' mm';
        applyGroundFilter();
      }}
    }}

    function loadEmbeddedPoints() {{
      const b64 = currentData.packedData;
      const binStr = atob(b64);
      const len = binStr.length;
      const bytes = new Uint8Array(len);
      for (let i = 0; i < len; i++) {{
        bytes[i] = binStr.charCodeAt(i);
      }}

      const view = new DataView(bytes.buffer);
      const numPoints = Math.floor(len / 7);

      allPointsData = [];
      for (let i = 0; i < numPoints; i++) {{
        const offset = i * 7;
        allPointsData.push({{
          x: view.getInt16(offset, true),
          y: view.getInt16(offset + 2, true),
          z: view.getInt16(offset + 4, true),
          intensity: view.getUint8(offset + 6)
        }});
      }}

      applyGroundFilter();
    }}

    function buildBoundingBox() {{
      groupBox.clear();
      const bbox = currentData.boundingBox;
      const H = currentData.height || 835;
      if (!bbox || bbox.length < 4) return;

      const b0 = toThree(bbox[0].x, bbox[0].y, 0);
      const b1 = toThree(bbox[1].x, bbox[1].y, 0);
      const b2 = toThree(bbox[2].x, bbox[2].y, 0);
      const b3 = toThree(bbox[3].x, bbox[3].y, 0);

      const t0 = toThree(bbox[0].x, bbox[0].y, H);
      const t1 = toThree(bbox[1].x, bbox[1].y, H);
      const t2 = toThree(bbox[2].x, bbox[2].y, H);
      const t3 = toThree(bbox[3].x, bbox[3].y, H);

      const lineIndices = [
        b0, b1,  b1, b2,  b2, b3,  b3, b0,
        t0, t1,  t1, t2,  t2, t3,  t3, t0,
        b0, t0,  b1, t1,  b2, t2,  b3, t3
      ];

      const linePoints = [];
      lineIndices.forEach(p => linePoints.push(p.x, p.y, p.z));

      const lineGeo = new THREE.BufferGeometry();
      lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePoints, 3));
      const lineMat = new THREE.LineBasicMaterial({{ color: 0x00f0ff, linewidth: 2 }});
      const wireframe = new THREE.LineSegments(lineGeo, lineMat);
      groupBox.add(wireframe);

      const faceVertices = [
        b0, b1, b2,  b0, b2, b3,
        t0, t2, t1,  t0, t3, t2,
        b0, t0, t1,  b0, t1, b1,
        b1, t1, t2,  b1, t2, b2,
        b2, t2, t3,  b2, t3, b3,
        b3, t3, t0,  b3, t0, b0
      ];
      const facePos = [];
      faceVertices.forEach(p => facePos.push(p.x, p.y, p.z));
      const shape = new THREE.BufferGeometry();
      shape.setAttribute('position', new THREE.Float32BufferAttribute(facePos, 3));
      shape.computeVertexNormals();
      const meshMat = new THREE.MeshBasicMaterial({{
        color: 0x00f0ff,
        transparent: true,
        opacity: 0.08,
        side: THREE.DoubleSide
      }});
      const mesh = new THREE.Mesh(shape, meshMat);
      groupBox.add(mesh);
    }}

    function buildKeyPoints() {{
      groupCorners.clear();
      groupTouching.clear();
      const bbox = currentData.boundingBox || [];
      const touching = currentData.touchingPoints || [];
      const tableBody = document.getElementById('tbl-points-body');
      tableBody.innerHTML = '';

      bbox.forEach((pt, idx) => {{
        const pos = toThree(pt.x, pt.y, 0);
        const sphereGeo = new THREE.SphereGeometry(18, 16, 16);
        const sphereMat = new THREE.MeshStandardMaterial({{
          color: 0x00ffaa,
          emissive: 0x00ffaa,
          emissiveIntensity: 0.5
        }});
        const sphere = new THREE.Mesh(sphereGeo, sphereMat);
        sphere.position.copy(pos);
        groupCorners.add(sphere);

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><span class="dot-indicator" style="background:#00ffaa;"></span>C${{idx+1}}</td>
          <td>Esquina Base ${{idx+1}}</td>
          <td class="mono">${{pt.x}}</td>
          <td class="mono">${{pt.y}}</td>
          <td class="mono">0</td>
        `;
        tableBody.appendChild(tr);
      }});

      const faceDesc = ['Lateral (+X)', 'Frontal (+Y)', 'Lateral (-X)', 'Trasero (-Y)', 'Superior (+Z)'];
      touching.forEach((pt, idx) => {{
        const pos = toThree(pt.x, pt.y, pt.z);
        const sphereGeo = new THREE.SphereGeometry(22, 16, 16);
        const sphereMat = new THREE.MeshStandardMaterial({{
          color: 0xff007b,
          emissive: 0xff007b,
          emissiveIntensity: 0.6
        }});
        const sphere = new THREE.Mesh(sphereGeo, sphereMat);
        sphere.position.copy(pos);
        groupTouching.add(sphere);

        if (pt.nx !== undefined && pt.ny !== undefined && pt.nz !== undefined) {{
          const dir = new THREE.Vector3(pt.nx, pt.nz, -pt.ny).normalize();
          const arrow = new THREE.ArrowHelper(dir, pos, 120, 0xff007b, 30, 15);
          groupTouching.add(arrow);
        }}

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><span class="dot-indicator" style="background:#ff007b;"></span>T${{idx+1}}</td>
          <td>${{faceDesc[idx] || 'Contacto ' + (idx+1)}}</td>
          <td class="mono">${{pt.x}}</td>
          <td class="mono">${{pt.y}}</td>
          <td class="mono">${{pt.z}}</td>
        `;
        tableBody.appendChild(tr);
      }});
    }}

    function updateTelemetryHUD(meta) {{
      document.getElementById('pallet-id').innerText = meta.id || 'N/A';
      document.getElementById('val-length').innerHTML = (meta.length || 0) + ' <span>cm</span>';
      document.getElementById('val-width').innerHTML = (meta.width || 0) + ' <span>cm</span>';
      document.getElementById('val-height').innerHTML = (meta.height || 0) + ' <span>cm</span>';
      document.getElementById('val-vol').innerHTML = (meta.volume || 0) + ' <span>L</span>';
      document.getElementById('val-weight').innerHTML = (meta.netWeight || 0) + ' <span>kg</span>';
      document.getElementById('val-rot').innerHTML = (meta.boxOrientation !== undefined ? meta.boxOrientation : 0) + ' <span>°</span>';

      // Remontabilidad: se evalúa únicamente non-stackable (1 = NO Remontable, 0 = Remontable)
      const isNonStackable = meta.nonStackable === 1 || meta.nonStackable === true || meta.nonStackable === '1';
      const badge = document.getElementById('val-stackable-badge');
      if (badge) {{
        if (isNonStackable) {{
          badge.innerText = '🚫 NO REMONTABLE';
          badge.style.background = 'rgba(255, 0, 123, 0.2)';
          badge.style.color = 'var(--accent-magenta)';
          badge.style.borderColor = 'rgba(255, 0, 123, 0.45)';
        }} else {{
          badge.innerText = '✅ REMONTABLE';
          badge.style.background = 'rgba(0, 255, 170, 0.2)';
          badge.style.color = 'var(--accent-green)';
          badge.style.borderColor = 'rgba(0, 255, 170, 0.45)';
        }}
      }}
    }}

    function setView(view) {{
      document.querySelectorAll('.btn-group button').forEach(b => b.classList.remove('active'));
      const activeBtn = document.getElementById('btn-' + view);
      if (activeBtn) activeBtn.classList.add('active');

      let targetY = (currentData.height || 835) / 2;
      let targetX = 0, targetZ = 0;
      if (currentData.boundingBox && currentData.boundingBox.length >= 4) {{
        let avgX = 0, avgY = 0;
        currentData.boundingBox.forEach(p => {{ avgX += p.x; avgY += p.y; }});
        avgX /= currentData.boundingBox.length;
        avgY /= currentData.boundingBox.length;
        const ptCenter = toThree(avgX, avgY, targetY);
        targetX = ptCenter.x;
        targetY = ptCenter.y;
        targetZ = ptCenter.z;
      }}

      const target = new THREE.Vector3(targetX, targetY, targetZ);
      controls.target.copy(target);

      if (view === 'iso') {{
        camera.position.set(targetX + 1600, targetY + 1200, targetZ + 1800);
      }} else if (view === 'top') {{
        camera.position.set(targetX, targetY + 2600, targetZ + 1);
      }} else if (view === 'front') {{
        camera.position.set(targetX, targetY + 200, targetZ + 2300);
      }} else if (view === 'side') {{
        camera.position.set(targetX + 2300, targetY + 200, targetZ);
      }}
      controls.update();
    }}

    function toggleLayer(layer) {{
      if (layer === 'points') groupPoints.visible = document.getElementById('chk-points').checked;
      if (layer === 'box') groupBox.visible = document.getElementById('chk-box').checked;
      if (layer === 'touching') groupTouching.visible = document.getElementById('chk-touching').checked;
      if (layer === 'corners') groupCorners.visible = document.getElementById('chk-corners').checked;
      if (layer === 'grid') groupGrid.visible = document.getElementById('chk-grid').checked;
    }}

    function updatePointSize(val) {{
      document.getElementById('lbl-pt-size').innerText = val;
      if (pointCloudMaterial) {{
        pointCloudMaterial.size = parseFloat(val);
      }}
    }}

    function updateColorMode(mode) {{
      applyGroundFilter();
    }}

    function togglePhotos() {{
      const modal = document.getElementById('image-modal');
      modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
    }}

    function parsePlyText(text) {{
      const lines = text.split('\\n');
      
      let startIdx = 0;
      for (let i = 0; i < Math.min(lines.length, 100); i++) {{
        if (lines[i].trim() === 'end_header') {{
          startIdx = i + 1;
          break;
        }}
      }}

      allPointsData = [];
      const step = lines.length > 150000 ? 2 : 1;

      for (let i = startIdx; i < lines.length; i += step) {{
        const line = lines[i].trim();
        if (!line) continue;
        const parts = line.split(/\\s+/);
        if (parts.length >= 3) {{
          allPointsData.push({{
            x: parseFloat(parts[0]),
            y: parseFloat(parts[1]),
            z: parseFloat(parts[2]),
            intensity: parts.length >= 4 ? parseFloat(parts[3]) : 128
          }});
        }}
      }}

      applyGroundFilter();
    }}

    function loadJdpsFile(jsonObj, filename) {{
      try {{
        const pc = jsonObj.pointCloud || {{}};
        currentData.height = pc.height || (jsonObj.height ? jsonObj.height * 10 : 835);
        currentData.boundingBox = pc.boundingBox || [];
        currentData.touchingPoints = pc.touchingPoints || [];

        // Leer campo non-stackable (1 = NO Remontable, 0 = Remontable)
        const rawNS = jsonObj['non-stackable'] !== undefined ? jsonObj['non-stackable'] : jsonObj.nonStackable;
        const meta = {{
          id: jsonObj.id || filename.replace(/\\.[^/.]+$/, ""),
          length: jsonObj.length || 0,
          width: jsonObj.width || 0,
          height: jsonObj.height || 0,
          volume: jsonObj.volume || 0,
          netWeight: jsonObj.netWeight || 0,
          boxOrientation: jsonObj.boxOrientation || 0,
          nonStackable: (rawNS === 1 || rawNS === true || rawNS === '1') ? 1 : 0
        }};
        updateTelemetryHUD(meta);

        if (jsonObj.image1) {{
          document.getElementById('modal-img-1').src = 'data:image/jpeg;base64,' + jsonObj.image1;
        }}
        if (jsonObj.image2) {{
          document.getElementById('modal-img-2').src = 'data:image/jpeg;base64,' + jsonObj.image2;
        }}

        buildBoundingBox();
        buildKeyPoints();

        if (pc.points) {{
          const plyText = atob(pc.points);
          parsePlyText(plyText);
        }}

        setView('iso');
        showToast('Cargado con éxito: ' + (meta.id || filename));
      }} catch (err) {{
        console.error(err);
        showToast('Error al procesar JDPS: ' + err.message, false);
      }}
    }}

    function handleFile(file) {{
      const reader = new FileReader();
      const fname = file.name.toLowerCase();

      if (fname.endsWith('.jdps') || fname.endsWith('.json')) {{
        reader.onload = (e) => {{
          try {{
            const parsed = JSON.parse(e.target.result);
            loadJdpsFile(parsed, file.name);
          }} catch (err) {{
            showToast('El archivo no es un JSON/JDPS válido.', false);
          }}
        }};
        reader.readAsText(file);
      }} else if (fname.endsWith('.ply')) {{
        reader.onload = (e) => {{
          parsePlyText(e.target.result);
          document.getElementById('pallet-id').innerText = file.name;
          showToast('Nube de puntos PLY cargada: ' + file.name);
        }};
        reader.readAsText(file);
      }} else {{
        showToast('Formato no soportado. Usa archivos .jdps o .ply', false);
      }}
    }}

    function handleFileSelect(files) {{
      if (files && files[0]) handleFile(files[0]);
    }}

    const dropOverlay = document.getElementById('drop-overlay');
    window.addEventListener('dragenter', (e) => {{
      e.preventDefault();
      dropOverlay.style.display = 'flex';
    }});
    window.addEventListener('dragover', (e) => {{
      e.preventDefault();
      dropOverlay.style.display = 'flex';
    }});
    window.addEventListener('dragleave', (e) => {{
      e.preventDefault();
      if (e.relatedTarget === null || e.clientX === 0 || e.clientY === 0) {{
        dropOverlay.style.display = 'none';
      }}
    }});
    window.addEventListener('drop', (e) => {{
      e.preventDefault();
      dropOverlay.style.display = 'none';
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {{
        handleFile(e.dataTransfer.files[0]);
      }}
    }});

    loadEmbeddedPoints();
    buildBoundingBox();
    buildKeyPoints();
    if (currentData.metadata) {{
      updateTelemetryHUD(currentData.metadata);
    }}
    setView('iso');

    window.addEventListener('resize', () => {{
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }});

    function animate() {{
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }}
    animate();
  </script>
</body>
</html>
'''

with open('visualizador_3d.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

shutil.copyfile('visualizador_3d.html', 'index.html')
print('Updated visualizador_3d.html and index.html (only non-stackable evaluated).')
