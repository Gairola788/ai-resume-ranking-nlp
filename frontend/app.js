// =============================================
//   RESUME SCREENER AI — app.js
// =============================================

const API = "http://127.0.0.1:8000";

// ---------- Tab Switching ----------
document.querySelectorAll(".tab").forEach(tab => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
    tab.classList.add("active");
    document.getElementById("tab-" + tab.dataset.tab).classList.add("active");
  });
});

// =============================================
//   SCREEN TAB
// =============================================

const resumeInput    = document.getElementById("resumeInput");
const resumeZone     = document.getElementById("resumeZone");
const resumeFileName = document.getElementById("resumeFileName");
const jdText         = document.getElementById("jdText");
const analyzeBtn     = document.getElementById("analyzeBtn");
const analyzeBtnText = document.getElementById("analyzeBtnText");
const screenLoading  = document.getElementById("screenLoading");
const screenFill     = document.getElementById("screenFill");
const screenResults  = document.getElementById("screenResults");
const clearScreenBtn = document.getElementById("clearScreenBtn");

// File selected
resumeInput.addEventListener("change", () => {
  if (resumeInput.files[0]) {
    resumeFileName.textContent = resumeInput.files[0].name;
    resumeZone.classList.add("has-file");
  }
});

// Drag and drop
resumeZone.addEventListener("dragover", e => { e.preventDefault(); resumeZone.style.borderColor = "var(--purple)"; });
resumeZone.addEventListener("dragleave", () => { resumeZone.style.borderColor = ""; });
resumeZone.addEventListener("drop", e => {
  e.preventDefault();
  resumeZone.style.borderColor = "";
  const file = e.dataTransfer.files[0];
  if (file) {
    resumeInput.files = e.dataTransfer.files;
    resumeFileName.textContent = file.name;
    resumeZone.classList.add("has-file");
  }
});

// Analyze
analyzeBtn.addEventListener("click", async () => {
  const file = resumeInput.files[0];
  const jd   = jdText.value.trim();

  if (!file) { alert("Please upload a resume file."); return; }
  if (!jd)   { alert("Please paste a job description."); return; }

  // Show loading
  analyzeBtn.disabled = true;
  analyzeBtnText.textContent = "Analyzing...";
  screenResults.classList.remove("visible");
  screenLoading.classList.add("active");
  animateBar(screenFill, 2500);

  const form = new FormData();
  form.append("resume", file);
  form.append("jd_text", jd);

  try {
    const res  = await fetch(`${API}/screen`, { method: "POST", body: form });
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Server error");

    setTimeout(() => {
      screenLoading.classList.remove("active");
      renderScreenResults(data);
      analyzeBtn.disabled = false;
      analyzeBtnText.textContent = "Analyze Resume";
    }, 400);

  } catch (err) {
    screenLoading.classList.remove("active");
    analyzeBtn.disabled = false;
    analyzeBtnText.textContent = "Analyze Resume";
    alert("Error: " + err.message);
  }
});

// Clear
clearScreenBtn.addEventListener("click", () => {
  resumeInput.value = "";
  resumeFileName.textContent = "";
  resumeZone.classList.remove("has-file");
  jdText.value = "";
  screenResults.classList.remove("visible");
});

function renderScreenResults(data) {
  const final   = data.final_score   || 0;
  const semantic= data.semantic_score|| 0;
  const tfidf   = data.tfidf_score   || 0;
  const keyword = data.keyword_score || 0;

  // Verdict banner
  const verdictInfo = getVerdictInfo(data.verdict || "");
  document.getElementById("verdictBanner").style.borderColor = verdictInfo.borderColor;
  document.getElementById("verdictIcon").textContent  = verdictInfo.icon;
  document.getElementById("verdictTitle").textContent = verdictInfo.title;
  document.getElementById("verdictText").textContent  = data.verdict || "";
  document.getElementById("verdictScore").textContent = pct(final);

  // Scores
  setScore("sc-final",    pct(final));
  setScore("sc-semantic", pct(semantic));
  setScore("sc-tfidf",    pct(tfidf));
  setScore("sc-keyword",  pct(keyword));

  // Bars (animate after render)
  setTimeout(() => {
    setBar("bar-final",    final);
    setBar("bar-semantic", semantic);
    setBar("bar-tfidf",    tfidf);
    setBar("bar-keyword",  keyword);
  }, 100);

  // Skills
  const matched = data.matched_skills || [];
  const missing = data.missing_skills || [];

  document.getElementById("matchedCount").textContent = matched.length;
  document.getElementById("missingCount").textContent = missing.length;

  renderChips("matchedSkills", matched, "match");
  renderChips("missingSkills", missing, "missing");

  screenResults.classList.add("visible");
}

// =============================================
//   RANK TAB
// =============================================

const multiResumeInput = document.getElementById("multiResumeInput");
const multiUploadZone  = document.getElementById("multiUploadZone");
const fileList         = document.getElementById("fileList");
const rankJdText       = document.getElementById("rankJdText");
const rankBtn          = document.getElementById("rankBtn");
const rankBtnText      = document.getElementById("rankBtnText");
const rankLoading      = document.getElementById("rankLoading");
const rankFill         = document.getElementById("rankFill");
const rankResults      = document.getElementById("rankResults");
const rankTableBody    = document.getElementById("rankTableBody");
const clearRankBtn     = document.getElementById("clearRankBtn");

multiResumeInput.addEventListener("change", () => {
  renderFileList(Array.from(multiResumeInput.files));
});

multiUploadZone.addEventListener("dragover", e => { e.preventDefault(); multiUploadZone.style.borderColor = "var(--purple)"; });
multiUploadZone.addEventListener("dragleave", () => { multiUploadZone.style.borderColor = ""; });
multiUploadZone.addEventListener("drop", e => {
  e.preventDefault();
  multiUploadZone.style.borderColor = "";
  multiResumeInput.files = e.dataTransfer.files;
  renderFileList(Array.from(e.dataTransfer.files));
});

function renderFileList(files) {
  fileList.innerHTML = "";
  files.forEach(f => {
    const tag = document.createElement("div");
    tag.className = "file-tag";
    tag.innerHTML = `<span>📄</span> ${f.name}`;
    fileList.appendChild(tag);
  });
}

rankBtn.addEventListener("click", async () => {
  const files = multiResumeInput.files;
  const jd    = rankJdText.value.trim();

  if (!files || files.length === 0) { alert("Please upload at least one resume."); return; }
  if (!jd) { alert("Please paste a job description."); return; }
  if (files.length < 2) { alert("Upload at least 2 resumes to rank candidates."); return; }

  rankBtn.disabled = true;
  rankBtnText.textContent = "Ranking...";
  rankResults.classList.remove("visible");
  rankLoading.classList.add("active");
  animateBar(rankFill, 3000);

  const form = new FormData();
  form.append("jd_text", jd);
  Array.from(files).forEach(f => form.append("resumes", f));

  try {
    const res  = await fetch(`${API}/rank`, { method: "POST", body: form });
    const data = await res.json();

    if (!res.ok) throw new Error(data.detail || "Server error");

    setTimeout(() => {
      rankLoading.classList.remove("active");
      renderRankResults(data.ranked || []);
      rankBtn.disabled = false;
      rankBtnText.textContent = "Rank Candidates";
    }, 400);

  } catch (err) {
    rankLoading.classList.remove("active");
    rankBtn.disabled = false;
    rankBtnText.textContent = "Rank Candidates";
    alert("Error: " + err.message);
  }
});

clearRankBtn.addEventListener("click", () => {
  multiResumeInput.value = "";
  rankJdText.value = "";
  fileList.innerHTML = "";
  rankResults.classList.remove("visible");
  rankTableBody.innerHTML = "";
});

function renderRankResults(candidates) {
  rankTableBody.innerHTML = "";

  candidates.forEach((c, i) => {
    const row = document.createElement("div");
    row.className = `rank-row ${i === 0 ? "rank-1" : ""}`;

    const verdictClass = getVerdictClass(c.verdict || "");

    row.innerHTML = `
      <div class="rank-num">#${c.rank}</div>
      <div class="rank-filename" title="${c.filename}">${c.filename}</div>
      <div class="rank-score">${pct(c.semantic_score)}</div>
      <div class="rank-score">${pct(c.tfidf_score)}</div>
      <div class="rank-score">${pct(c.keyword_score)}</div>
      <div class="rank-final">${pct(c.final_score)}</div>
      <div><span class="verdict-chip ${verdictClass}">${shortVerdict(c.verdict)}</span></div>
    `;

    rankTableBody.appendChild(row);
  });

  rankResults.classList.add("visible");
}

// =============================================
//   HELPERS
// =============================================

function pct(val) {
  return Math.round((val || 0) * 100) + "%";
}

function setScore(id, val) {
  document.getElementById(id).textContent = val;
}

function setBar(id, val) {
  document.getElementById(id).style.width = (val * 100) + "%";
}

function renderChips(containerId, skills, type) {
  const el = document.getElementById(containerId);
  el.innerHTML = "";
  if (!skills || skills.length === 0) {
    el.innerHTML = `<span class="chip empty">None</span>`;
    return;
  }
  skills.forEach(skill => {
    const chip = document.createElement("span");
    chip.className = `chip ${type}`;
    chip.textContent = skill;
    el.appendChild(chip);
  });
}

function getVerdictInfo(verdict) {
  if (verdict.includes("Strong"))  return { icon: "✅", title: "Strong Match",  borderColor: "rgba(34,197,94,0.3)" };
  if (verdict.includes("Good"))    return { icon: "✦",  title: "Good Match",    borderColor: "rgba(59,130,246,0.3)" };
  if (verdict.includes("Weak"))    return { icon: "⚠",  title: "Weak Match",    borderColor: "rgba(245,158,11,0.3)" };
  return                                  { icon: "✗",  title: "Poor Match",    borderColor: "rgba(239,68,68,0.3)" };
}

function getVerdictClass(verdict) {
  if (verdict.includes("Strong"))  return "strong";
  if (verdict.includes("Good"))    return "good";
  if (verdict.includes("Weak"))    return "weak";
  return "poor";
}

function shortVerdict(verdict) {
  if (verdict.includes("Strong"))  return "Strong Match";
  if (verdict.includes("Good"))    return "Good Match";
  if (verdict.includes("Weak"))    return "Weak Match";
  return "Poor Match";
}

function animateBar(fillEl, duration) {
  fillEl.style.width = "0%";
  let start = null;
  function step(ts) {
    if (!start) start = ts;
    const progress = Math.min((ts - start) / duration, 0.92);
    fillEl.style.width = (progress * 100) + "%";
    if (progress < 0.92) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// ---------- Check API health on load ----------
window.addEventListener("load", async () => {
  try {
    const res = await fetch(`${API}/`);
    if (!res.ok) throw new Error();
    // API is up — status pill stays green (default)
  } catch {
    const pill = document.getElementById("statusPill");
    pill.style.background = "rgba(239,68,68,0.1)";
    pill.style.borderColor = "rgba(239,68,68,0.2)";
    pill.style.color = "#ef4444";
    pill.querySelector(".status-dot").style.background = "#ef4444";
    pill.innerHTML = '<span class="status-dot"></span> API Offline — start backend';
  }
});