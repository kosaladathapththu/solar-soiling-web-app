/* ─────────────────────────────────────────────────────────────
   SDS-YOLO · Solar Panel Soiling Detection · script.js v21
   ───────────────────────────────────────────────────────────── */

console.log("[SDS-YOLO] script.js loaded — v21");

// ─── DOM refs ─────────────────────────────────────────────────
const imageInput      = document.getElementById("imageInput");
const uploadZone      = document.getElementById("uploadZone");
const uploadContent   = document.getElementById("uploadContent");
const uploadPreview   = document.getElementById("uploadPreview");
const previewImage    = document.getElementById("previewImage");
const previewFilename = document.getElementById("previewFilename");
const fileMeta        = document.getElementById("fileMeta");
const metaName        = document.getElementById("metaName");
const metaSize        = document.getElementById("metaSize");
const metaType        = document.getElementById("metaType");
const runBtn          = document.getElementById("runBtn");
const btnLoading      = document.getElementById("btnLoading");
const btnInner        = document.getElementById("btnInner");

const statusDot       = document.getElementById("statusDot");
const statusLabel     = document.getElementById("statusLabel");
const contentMeta     = document.getElementById("contentMeta");

const resultsIdle     = document.getElementById("resultsIdle");
const resultsContent  = document.getElementById("resultsContent");
const resultsError    = document.getElementById("resultsError");

const summaryStatus   = document.getElementById("summaryStatus");
const summaryCount    = document.getElementById("summaryCount");
const summaryConf     = document.getElementById("summaryConf");
const detCountBadge   = document.getElementById("detCountBadge");
const imgDims         = document.getElementById("imgDims");
const resultImage     = document.getElementById("resultImage");
const detectionsList  = document.getElementById("detectionsList");
const errorTitle      = document.getElementById("errorTitle");
const errorBody       = document.getElementById("errorBody");

// ─── Helpers ──────────────────────────────────────────────────
function formatBytes(bytes) {
  if (bytes < 1024)         return bytes + " B";
  if (bytes < 1024 * 1024)  return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(2) + " MB";
}

function setStatus(state, label) {
  statusDot.className = "sys-status-dot" + (state ? " " + state : "");
  statusLabel.textContent = label;
}

function showState(which) {
  // which: "Idle" | "Content" | "Error"
  resultsIdle.classList.add("hidden");
  resultsContent.classList.add("hidden");
  resultsError.classList.add("hidden");
  const el = document.getElementById("results" + which);
  if (el) el.classList.remove("hidden");
}

function classDotType(className) {
  const lc = (className || "").toLowerCase();
  if (lc.includes("dust") || lc.includes("particle") || lc.includes("soil")) return "dust";
  if (lc.includes("bird") || lc.includes("drop") || lc.includes("droppings")) return "bird";
  return "other";
}

function confidencePct(raw) {
  if (typeof raw === "number") return raw <= 1 ? Math.round(raw * 100) : Math.round(raw);
  const s = String(raw).replace("%", "").trim();
  const n = parseFloat(s);
  if (isNaN(n)) return 0;
  return n <= 1 ? Math.round(n * 100) : Math.round(n);
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function nowTimestamp() {
  return new Date().toLocaleTimeString("en-US", {
    hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false
  });
}

// ─── Upload / Preview ─────────────────────────────────────────
imageInput.addEventListener("change", previewSelectedImage);

uploadZone.addEventListener("dragover", e => {
  e.preventDefault();
  uploadZone.classList.add("dragover");
});

uploadZone.addEventListener("dragleave", () => {
  uploadZone.classList.remove("dragover");
});

uploadZone.addEventListener("drop", e => {
  e.preventDefault();
  uploadZone.classList.remove("dragover");
  if (e.dataTransfer.files && e.dataTransfer.files[0]) {
    imageInput.files = e.dataTransfer.files;
    previewSelectedImage();
  }
});

function previewSelectedImage() {
  const file = imageInput.files[0];
  if (!file) return;

  console.log("[SDS-YOLO] File selected:", file.name);

  const url = URL.createObjectURL(file);
  previewImage.src = url;
  previewFilename.textContent = file.name;

  uploadContent.classList.add("hidden");
  uploadPreview.classList.remove("hidden");

  metaName.textContent = file.name.length > 36 ? file.name.slice(0, 33) + "…" : file.name;
  metaSize.textContent = formatBytes(file.size);
  metaType.textContent = file.type || "unknown";
  fileMeta.classList.remove("hidden");

  runBtn.disabled = false;
  showState("Idle");
  setStatus("", "READY");
  contentMeta.textContent = "—";
}

// ─── Predict ──────────────────────────────────────────────────
async function predictImage() {
  const file = imageInput.files[0];
  if (!file) return;

  // Loading state
  btnInner.classList.add("hidden");
  btnLoading.classList.remove("hidden");
  runBtn.disabled = true;
  setStatus("processing", "PROCESSING");
  showState("Idle");

  const formData = new FormData();
  formData.append("image", file);

  const startTime = Date.now();

  try {
    const response = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
    console.log("[SDS-YOLO] Response:", data);

    // Restore button
    btnInner.classList.remove("hidden");
    btnLoading.classList.add("hidden");
    runBtn.disabled = false;

    if (!response.ok || !data.success) {
      setStatus("error", "ERROR");
      showState("Error");
      errorTitle.textContent = "Detection Failed";
      errorBody.textContent =
        data.error || data.stderr || data.message || "An unknown backend error occurred.";
      contentMeta.textContent = "failed · " + nowTimestamp();
      return;
    }

    // ── Success ───────────────────────────────────────────────
    const count = data.detected_count ?? (data.detections ? data.detections.length : 0);
    const detections = data.detections || [];

    setStatus("", count > 0 ? "SOILING DETECTED" : "CLEAN");
    contentMeta.textContent = `${elapsed}s · ${nowTimestamp()}`;

    // Metrics
    summaryCount.textContent = count;
    detCountBadge.textContent = count + (count === 1 ? " object" : " objects");

    if (count === 0) {
      summaryStatus.textContent = "Clean";
      summaryStatus.className = "metric-value ok";
    } else {
      summaryStatus.textContent = "Soiling Detected";
      summaryStatus.className = "metric-value warn";
    }

    // Average confidence
    if (detections.length > 0) {
      const avg = detections.reduce((s, d) => s + confidencePct(d.confidence), 0) / detections.length;
      summaryConf.textContent = Math.round(avg) + "%";
    } else {
      summaryConf.textContent = "—";
    }

    // Result image
    if (data.result_image) {
      resultImage.src = data.result_image + "?t=" + Date.now();
      resultImage.style.display = "block";
      imgDims.textContent = "";
      // Try to read natural dims once loaded
      resultImage.onload = () => {
        if (resultImage.naturalWidth) {
          imgDims.textContent = resultImage.naturalWidth + " × " + resultImage.naturalHeight;
        }
      };
    } else {
      resultImage.style.display = "none";
      imgDims.textContent = "";
    }

    // Detection rows
    detectionsList.innerHTML = "";

    if (detections.length > 0) {
      detections.forEach((item, i) => {
        const pct    = confidencePct(item.confidence);
        const dotCls = classDotType(item.class_name);
        const delay  = i * 35;

        const row = document.createElement("div");
        row.className = "det-row";
        row.style.animationDelay = delay + "ms";

        row.innerHTML = `
          <span class="det-index">${String(i + 1).padStart(2, "0")}</span>
          <span class="det-class-tag">
            <span class="det-dot ${dotCls}"></span>
            <span class="det-class-name">${escHtml(item.class_name)}</span>
          </span>
          <span class="det-conf">${pct}%</span>
          <span class="det-bar-wrap">
            <span class="det-bar" style="width:${pct}%"></span>
          </span>
        `;

        detectionsList.appendChild(row);
      });
    } else {
      detectionsList.innerHTML = `
        <div class="no-detection">
          <div class="no-detection-inner">
            <svg width="13" height="13" viewBox="0 0 13 13" fill="none">
              <path d="M2 6.5l3 3 6-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            No soiling detected
          </div>
        </div>
      `;
    }

    showState("Content");
    resultsContent.scrollIntoView({ behavior: "smooth", block: "nearest" });

  } catch (err) {
    btnInner.classList.remove("hidden");
    btnLoading.classList.add("hidden");
    runBtn.disabled = false;
    setStatus("error", "ERROR");
    showState("Error");
    errorTitle.textContent = "Connection Error";
    errorBody.textContent = err.message || "Could not reach the backend server.";
    contentMeta.textContent = "failed · " + nowTimestamp();
    console.error("[SDS-YOLO] Fetch error:", err);
  }
}