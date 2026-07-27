// app.js — Rind Report frontend logic.
// Talks to the real backend at POST /api/diagnose. No mock/fallback
// prediction lives here; if the model isn't trained yet, the API returns
// HTTP 503 and this file just displays that honestly.

(() => {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("file-input");
  const dropzone = document.getElementById("dropzone");
  const dzEmpty = document.getElementById("dropzone-empty");
  const dzPreview = document.getElementById("dropzone-preview");
  const previewImg = document.getElementById("preview-img");
  const submitBtn = document.getElementById("submit-btn");
  const clearBtn = document.getElementById("clear-btn");
  const statusEl = document.getElementById("form-status");

  const resultSection = document.getElementById("result");
  const gradientMarker = document.getElementById("gradient-marker");
  const stampLabel = document.getElementById("stamp-label");
  const stampStage = document.getElementById("stamp-stage");
  const confidenceValue = document.getElementById("confidence-value");
  const causeText = document.getElementById("cause-text");
  const actionsList = document.getElementById("actions-list");

  // Rough illustrative position of each class along the green -> yellow ->
  // brown peel-life gradient shown in the result. Purely visual, not a
  // model output — the actual class/confidence come straight from the API.
  const GRADIENT_POSITION = {
    healthy: 6,
    pest_damage: 22,
    scars: 30,
    sunburn: 38,
    yellowing: 55,
    dehydration: 62,
    mechanical_damage: 72,
    brown_spot: 82,
    microbial_damage: 94,
  };

  let selectedFile = null;

  function setStatus(message, tone) {
    statusEl.textContent = message || "";
    if (tone) {
      statusEl.setAttribute("data-tone", tone);
    } else {
      statusEl.removeAttribute("data-tone");
    }
  }

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      previewImg.src = e.target.result;
      dzEmpty.hidden = true;
      dzPreview.hidden = false;
    };
    reader.readAsDataURL(file);
  }

  function selectFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setStatus("That doesn't look like an image file.", "error");
      return;
    }
    selectedFile = file;
    showPreview(file);
    submitBtn.disabled = false;
    clearBtn.hidden = false;
    setStatus("");
    resultSection.hidden = true;
  }

  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files[0]) {
      selectFile(fileInput.files[0]);
    }
  });

  ["dragover", "dragenter"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.style.background = "#E7E4D2";
    });
  });

  ["dragleave", "drop"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      dropzone.style.background = "";
    });
  });

  dropzone.addEventListener("drop", (e) => {
    const file = e.dataTransfer.files && e.dataTransfer.files[0];
    if (file) selectFile(file);
  });

  clearBtn.addEventListener("click", () => {
    selectedFile = null;
    fileInput.value = "";
    dzEmpty.hidden = false;
    dzPreview.hidden = true;
    submitBtn.disabled = true;
    clearBtn.hidden = true;
    resultSection.hidden = true;
    setStatus("");
  });

  function renderResult(data) {
    const info = data.diagnosis;
    stampLabel.textContent = info.label;
    stampStage.textContent = info.stage === "none" ? "no damage" : info.stage;
    confidenceValue.textContent = Math.round(data.confidence * 100) + "%";
    causeText.textContent = info.cause;

    actionsList.innerHTML = "";
    info.actions.forEach((action) => {
      const li = document.createElement("li");
      li.textContent = action;
      actionsList.appendChild(li);
    });

    const pos = GRADIENT_POSITION[data.predicted_class] ?? 50;
    gradientMarker.style.left = pos + "%";

    resultSection.hidden = false;
    resultSection.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    submitBtn.disabled = true;
    setStatus("Reading the peel…", "pending");
    resultSection.hidden = true;

    const body = new FormData();
    body.append("image", selectedFile);

    try {
      const res = await fetch("/api/diagnose", { method: "POST", body });
      const data = await res.json();

      if (!res.ok) {
        if (res.status === 503) {
          setStatus(
            "The model isn't trained yet on this server, so there's no diagnosis to show. Ask the CV team to run model/train.py and drop the saved model in.",
            "error"
          );
        } else {
          setStatus(data.error || "Something went wrong reading that photo.", "error");
        }
        return;
      }

      setStatus("");
      renderResult(data);
    } catch (err) {
      setStatus("Couldn't reach the server. Check your connection and try again.", "error");
    } finally {
      submitBtn.disabled = false;
    }
  });
})();
