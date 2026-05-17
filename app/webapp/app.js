const state = {
  lastResult: null,
  quranSuras: [],
  quranDomains: {},
  genericDomains: {},
  schemes: {},
  corpora: [],
};

const $ = (id) => document.getElementById(id);

async function api(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || "Erreur API");
  }
  return data;
}

function setStatus(text) {
  $("statusBox").textContent = text;
}

function switchTab(target) {
  document.querySelectorAll(".tab").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.tab === target);
  });
  document.querySelectorAll(".panel").forEach((panel) => {
    panel.classList.toggle("active", panel.id === `tab-${target}`);
  });
}

function fillSelect(select, entries, labelKey = "label", valueKey = "value") {
  select.innerHTML = "";
  for (const entry of entries) {
    const opt = document.createElement("option");
    opt.value = entry[valueKey];
    opt.textContent = entry[labelKey];
    select.appendChild(opt);
  }
}

function resultSummary(result) {
  if (result.metrics && result.signature) {
    const metrics = result.metrics;
    const signature = result.signature;
    const spirit = result.spirit?.reading || result.domain?.intent || "";
    return [
      `Source: ${result.source}`,
      `Domaine: ${result.domain?.label || result.domain?.key || ""}`,
      `Total numérique: ${metrics.abjad_total ?? metrics.value_total}`,
      `Mots / lettres: ${metrics.word_count} / ${metrics.letter_count}`,
      `Centre du talisman: ${result.talisman?.center ?? signature.center}`,
      `Pont phi: ${(signature.golden_bridge || [metrics.golden_words, metrics.golden_letters, metrics.golden_value]).join(" / ")}`,
      spirit,
    ].join("\n");
  }
  return JSON.stringify(result, null, 2);
}

function showResult(result, mode) {
  state.lastResult = result;
  $("resultMode").textContent = mode;
  $("resultSummary").textContent = resultSummary(result);
  $("resultJson").textContent = JSON.stringify(result, null, 2);
  $("talismanPreview").innerHTML = "";
}

async function renderCurrentTalisman(title) {
  if (!state.lastResult) {
    setStatus("Aucun résultat à rendre.");
    return;
  }
  setStatus("Rendu du talisman en cours…");
  const res = await api("/api/render/talisman", {
    method: "POST",
    body: JSON.stringify({ result: state.lastResult, title }),
  });
  $("talismanPreview").innerHTML = `<img src="${res.path}?t=${Date.now()}" alt="Talisman rendu" />`;
  setStatus(`Talisman généré : ${res.path}`);
}

async function loadDomains() {
  const data = await api("/api/domains");
  state.quranDomains = data.quran_domains;
  state.genericDomains = data.generic_domains;
  state.schemes = data.schemes;

  const quranDomainEntries = Object.entries(state.quranDomains).map(([key, value]) => ({
    value: key,
    label: value.label,
  }));
  fillSelect($("quranDomain"), quranDomainEntries);

  const genericDomainEntries = Object.entries(state.genericDomains).map(([key, value]) => ({
    value: key,
    label: value.label,
  }));
  fillSelect($("genericDomain"), genericDomainEntries);
  fillSelect($("corpusDomain"), genericDomainEntries);
  fillSelect($("vivantDomain"), genericDomainEntries);

  const schemeEntries = Object.entries(state.schemes).map(([key, value]) => ({
    value: key,
    label: value.label,
  }));
  fillSelect($("genericScheme"), schemeEntries);
  fillSelect($("importScheme"), schemeEntries);
}

async function loadSuras() {
  const suras = await api("/api/quran/suras");
  state.quranSuras = suras;
  fillSelect(
    $("quranSura"),
    suras.map((s) => ({
      value: s.index,
      label: `${String(s.index).padStart(3, "0")} — ${s.tname} (${s.ayas})`,
    }))
  );
}

async function loadCorpora() {
  const corpora = await api("/api/corpora");
  state.corpora = corpora;
  fillSelect(
    $("corpusSelect"),
    corpora.length
      ? corpora.map((c) => ({ value: c.corpus_id, label: `${c.name} (${c.entry_count})` }))
      : [{ value: "", label: "Aucun corpus importé" }]
  );
  if (corpora.length) {
    await loadCorpusRefs(corpora[0].corpus_id);
  } else {
    fillSelect($("corpusRef"), [{ value: "", label: "Aucune référence" }]);
  }
}

async function loadCorpusRefs(corpusId) {
  if (!corpusId) return;
  const refs = await api(`/api/corpus/refs?corpus_id=${encodeURIComponent(corpusId)}`);
  fillSelect(
    $("corpusRef"),
    refs.map((ref) => ({ value: ref, label: ref }))
  );
}

async function analyzeQuran() {
  setStatus("Analyse coranique en cours…");
  const payload = {
    sura: $("quranSura").value,
    ayah: $("quranAyah").value || null,
    end: $("quranEnd").value || null,
    domain: $("quranDomain").value,
  };
  const result = await api("/api/analyze/quran", { method: "POST", body: JSON.stringify(payload) });
  showResult(result, "Coran");
  setStatus(`Analyse terminée pour ${result.source}.`);
}

async function analyzeGeneric() {
  setStatus("Analyse du texte sacré en cours…");
  const payload = {
    text: $("genericText").value,
    scheme: $("genericScheme").value,
    domain: $("genericDomain").value,
    ref_label: $("genericRef").value || "custom-text",
  };
  const result = await api("/api/analyze/text", { method: "POST", body: JSON.stringify(payload) });
  showResult(result, "Texte sacré");
  setStatus(`Analyse terminée pour ${result.source}.`);
}

async function importCorpus() {
  setStatus("Import du corpus en cours…");
  const payload = {
    name: $("importName").value,
    scheme: $("importScheme").value,
    description: $("importDescription").value,
    raw_entries: $("importEntries").value,
  };
  const result = await api("/api/import/corpus", { method: "POST", body: JSON.stringify(payload) });
  setStatus(`Corpus importé : ${result.name}`);
  await loadCorpora();
}

async function analyzeCorpus() {
  setStatus("Analyse de l’entrée importée…");
  const payload = {
    corpus_id: $("corpusSelect").value,
    ref: $("corpusRef").value,
    domain: $("corpusDomain").value,
  };
  const result = await api("/api/analyze/corpus", { method: "POST", body: JSON.stringify(payload) });
  showResult(result, "Corpus importé");
  setStatus(`Analyse terminée pour ${result.source}.`);
}

async function loadLibrary() {
  setStatus("Chargement de la bibliothèque…");
  const data = await api("/api/library");
  const container = $("libraryOutput");
  container.innerHTML = "";
  data.entries.slice(0, 24).forEach((entry) => {
    const card = document.createElement("div");
    card.className = "library-card";
    card.innerHTML = `
      <strong>${String(entry.sura).padStart(3, "0")} — ${entry.tname}</strong><br />
      ${entry.name_ar} • ${entry.ayas} versets<br />
      <a href="/${entry.canonical_talisman}" target="_blank">Talisman canonique</a>
    `;
    container.appendChild(card);
  });
  setStatus(`Bibliothèque chargée : ${data.entries.length} sourates.`);
}

async function analyzeVivant() {
  setStatus("Generation du Talisman Vivant en cours…");
  const payload = {
    name: $("vivantName").value || "Chercheur",
    domain: $("vivantDomain").value,
    date: $("vivantDate").value || "",
  };
  const result = await api("/api/talisman/vivant", { method: "POST", body: JSON.stringify(payload) });
  showResult(result, "Talisman Vivant");
  if (result.vivant) {
    const v = result.vivant;
    $("vivantInfo").innerHTML = `
      <strong>Nom:</strong> ${v.name} | <strong>Abjad:</strong> ${v.name_abjad} (racine ${v.name_root})
      | <strong>Mansion lunaire:</strong> ${v.lunar_mansion}/28
      | <strong>Centre du talisman:</strong> ${result.talisman.center}
    `;
  }
  setStatus(`Talisman Vivant genere pour ${result.vivant.name}.`);
}

function bindEvents() {
  document.querySelectorAll(".tab").forEach((btn) => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });
  $("analyzeQuranBtn").addEventListener("click", analyzeQuran);
  $("renderQuranTalismanBtn").addEventListener("click", () => renderCurrentTalisman("Quran Talisman"));
  $("analyzeGenericBtn").addEventListener("click", analyzeGeneric);
  $("renderGenericTalismanBtn").addEventListener("click", () => renderCurrentTalisman("Sacred Text Talisman"));
  $("importCorpusBtn").addEventListener("click", importCorpus);
  $("analyzeCorpusBtn").addEventListener("click", analyzeCorpus);
  $("loadLibraryBtn").addEventListener("click", loadLibrary);
  $("analyzeVivantBtn").addEventListener("click", analyzeVivant);
  $("renderVivantTalismanBtn").addEventListener("click", () => renderCurrentTalisman("Talisman Vivant"));
  $("corpusSelect").addEventListener("change", async (e) => {
    await loadCorpusRefs(e.target.value);
  });
}

async function boot() {
  bindEvents();
  await loadDomains();
  await loadSuras();
  await loadCorpora();
  setStatus("Application prête.");
}

boot().catch((err) => {
  console.error(err);
  setStatus(`Erreur : ${err.message}`);
});
