import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { buildConstellationStripSvg, buildRosetteSvg, fontFaceCss } from "./luxe_collection_assets.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..", "..");
const bundledNodeModules = path.resolve(path.dirname(process.execPath), "..", "node_modules");

const documentsDir = path.join(rootDir, "documents");
const htmlDir = path.join(documentsDir, "html", "richesse_abondance");
const pdfDir = path.join(documentsDir, "pdf", "richesse_abondance");
const previewDir = path.join(documentsDir, "preview");

const htmlPath = path.join(htmlDir, "Decouverte_Phi_Coran_Rizq_Premium.html");
const pdfPath = path.join(pdfDir, "Decouverte_Phi_Coran_Rizq.pdf");
const previewPath = path.join(previewDir, "Decouverte_Phi_Coran_Rizq_Premium_page1.png");
const previewDensePath = path.join(previewDir, "Decouverte_Phi_Coran_Rizq_Premium_page6.png");

const chromeCandidates = [
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
];

const PHI = 1.618033988749895;

const discoveries = [
  {
    number: "01",
    title: "Matrice fondamentale du rizq",
    formula: "19 x 4 x phi = 122.9706 -> 123",
    target: "123 occurrences du champ du rizq",
    precision: "99.98%",
    meaning:
      "Le code 19 applique aux quatre noms du rizq produit le seuil 123. Cette formule sert d'axe d'ouverture de tout le dossier.",
    points: [
      "19 = signature numerique du Coran dans la lecture du document.",
      "4 = Razzaq, Fattah, Ghani, Mughni.",
      "76 = matrice interne ; phi projette cette matrice vers 123.",
    ],
  },
  {
    number: "02",
    title: "Rahman et corridor Fibonacci",
    formula: "55 x phi = 88.9919 -> 89",
    target: "55 -> 89",
    precision: "lecture Fibonacci",
    meaning:
      "La sourate 55, Al-Rahman, devient le seuil de bascule vers 89. Le projet lit cela comme un couloir entre misericorde, aube et manifestation.",
    points: [
      "34 -> 55 -> 89 organise l'ascension de la sequence.",
      "56, Al-Waqi'a, est placee comme porte manifeste juste apres 55.",
      "Le corridor structure plusieurs applications pratiques du PDF.",
    ],
  },
  {
    number: "03",
    title: "Ouverture et Basmala",
    formula: "489 x phi = 791.219 -> 786",
    target: "Ya Fattah -> Basmala",
    precision: "pont symbolique",
    meaning:
      "Fattah est lu comme cle d'ouverture, puis rapproche de la Basmala. Le geste rituel consiste a relier la porte, le nom et l'acte d'appel.",
    points: [
      "489 = valeur simple retenue pour Fattah dans le projet.",
      "786 devient le sceau d'entree et le seuil d'activation.",
      "Le rapport inverse 786 / phi reste voisin du meme champ.",
    ],
  },
  {
    number: "04",
    title: "Misericorde et enrichissement",
    formula: "618 x phi = 999.9454 -> 1000+",
    target: "Rahman + Rahim",
    precision: "coeur rectifie",
    meaning:
      "La refonte conserve le pivot 618 comme coeur misericordieux. C'est la version numeriquement la plus propre de l'ancien argument.",
    points: [
      "329 + 289 = 618.",
      "618 recentre le flux avant la capture materielle.",
      "La porte 618 devient centrale dans les sceaux et protocoles.",
    ],
  },
  {
    number: "05",
    title: "Cycle rituel et horizon des noms",
    formula: "61 x phi = 98.7001 -> 99",
    target: "61 -> 99",
    precision: "99.7%",
    meaning:
      "Le cycle rituel complet est projete vers l'horizon des 99 Noms. Le document l'utilise comme fermeture, protection et stabilisation.",
    points: [
      "1 + 7 + 19 + 33 + 1 = 61.",
      "61 sert de cycle operatif minimal.",
      "99 devient l'horizon de completude et de saturation vibratoire.",
    ],
  },
];

const vocabulary = [
  ["Rizq", "123", "champ de la subsistance et de la provision"],
  ["Basmala", "786", "porte d'entree et sceau d'ouverture"],
  ["Ya Fattah", "489", "nom d'ouverture et de debarrassage"],
  ["Ya Razzaq", "319", "appel direct au flux de provision"],
  ["Ya Ghani", "1060", "plenum, richesse et autosuffisance"],
  ["Ya Mughni", "1100", "densification, enrichissement et affermissement"],
  ["Rahman + Rahim", "618", "coeur misericordieux rectifie"],
  ["Cycle rituel", "61", "ouverture + istighfar + nom + salawat + sceau"],
];

const dhikrs = [
  {
    title: "Dhikr A  |  Matrice 76",
    structure: "19x Ya Razzaq + 19x Ya Fattah + 19x Ya Ghani + 19x Ya Mughni",
    use: "Travail du matin et lancement du couloir d'abondance.",
  },
  {
    title: "Dhikr B  |  Porte 786",
    structure: "1 Basmala + 79x Ya Fattah + 7 respirations lentes",
    use: "Ouverture d'une demande, dossier, vente ou entretien important.",
  },
  {
    title: "Dhikr C  |  Cycle 61",
    structure: "1 + 7 + 19 + 33 + 1",
    use: "Cycle complet pour fermer la journee ou accompagner un talisman.",
  },
  {
    title: "Dhikr D  |  Corridor 34-55-89",
    structure: "34x gratitude + 55x Ya Rahman + 89 souffles conscients",
    use: "Travail de sensibilisation du coeur avant manifestation exterieure.",
  },
  {
    title: "Dhikr E  |  Porte 618",
    structure: "61x Ya Rahman + 8x Ya Rahim",
    use: "Recentrage misericordieux quand le champ est ferme ou contracte.",
  },
];

const grabovoiCodes = [
  ["123 55 89", "Corridor Fibonacci du rizq", "Misericorde -> aube -> provision"],
  ["786 489 618", "Porte d'ouverture", "Basmala -> Fattah -> coeur misericordieux"],
  ["6119 078", "Cycle operatif complet", "61 + 19 + 7 + 8 directions"],
  ["489 319 1060 1100", "Quatre noms du flux", "Ouverture -> source -> richesse -> consolidation"],
];

const radionics = [
  "Fil cuivre : 91 cm environ pour accorder 56 x phi.",
  "Spirale primaire : 31 tours ; secondaire : 7 tours.",
  "Rayons recommandes : 75 / 46 / 29 mm pour suivre une logique phi.",
  "Centre du montage : 786 489 618.",
  "Anneau externe : 55, 89, 123, 319, 489, 61, 99, 786.",
  "Duree d'activation : 7, 21 ou 65 jours selon l'intensite voulue.",
];

const weekdayPractice = [
  ["Dimanche", "19 x phi -> 31", "31x Ya Razzaq"],
  ["Lundi", "56 x phi -> 91", "91x Basmala"],
  ["Mardi", "7 x phi -> 11", "11x Ya Fattah"],
  ["Mercredi", "61 x phi -> 99", "Cycle complet"],
  ["Jeudi", "33 x phi -> 53", "53x Salawat"],
  ["Vendredi", "489 x phi -> 791", "79x Ya Fattah"],
  ["Samedi", "618 x phi -> 1000", "110x Ya Mughni"],
];

const referenceRows = [
  ["19 x 4 = 76", "x phi", "122.97", "123 Rizq", "99.98%"],
  ["55 Rahman", "x phi", "88.99", "89 Fajr", "lecture Fibonacci"],
  ["489 Fattah", "x phi", "791.22", "786 Basmala", "pont rituel"],
  ["618 mercy-code", "x phi", "999.95", "1000+", "porte centrale"],
  ["61 cycle", "x phi", "98.70", "99 Noms", "99.7%"],
  ["786 Basmala", "/ phi", "485.77", "489 Fattah", "retour de porte"],
  ["34", "x phi", "55.01", "Rahman", "couloir"],
  ["89", "x phi", "144.00", "144", "suite Fibonacci"],
];

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function resolveChromeExecutable() {
  for (const candidate of chromeCandidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  return undefined;
}

function sectionTitle(eyebrow, title, deck = "") {
  return `
    <div class="section-head">
      <div class="eyebrow">${escapeHtml(eyebrow)}</div>
      <h2>${escapeHtml(title)}</h2>
      ${deck ? `<p class="deck">${escapeHtml(deck)}</p>` : ""}
    </div>
  `;
}

function formulaStrip(values) {
  return `
    <div class="formula-strip">
      ${values
        .map(
          (value) => `
            <div class="formula-pill">
              <span></span>${escapeHtml(value)}
            </div>`,
        )
        .join("")}
    </div>
  `;
}

function talismanSvg() {
  const labels = [
    { value: "55", x: 300, y: 74 },
    { value: "89", x: 470, y: 136 },
    { value: "123", x: 528, y: 300 },
    { value: "319", x: 470, y: 464 },
    { value: "489", x: 300, y: 526 },
    { value: "61", x: 130, y: 464 },
    { value: "99", x: 72, y: 300 },
    { value: "786", x: 130, y: 136 },
  ];

  return `
    <svg class="talisman-svg" viewBox="0 0 600 600" aria-hidden="true">
      <defs>
        <radialGradient id="phiGlow" cx="50%" cy="50%" r="70%">
          <stop offset="0%" stop-color="#fff8ec" stop-opacity="0.95" />
          <stop offset="100%" stop-color="#fff3d4" stop-opacity="0.18" />
        </radialGradient>
      </defs>
      <circle cx="300" cy="300" r="238" fill="none" stroke="#1d2434" stroke-width="1.6" />
      <circle cx="300" cy="300" r="196" fill="none" stroke="#b89552" stroke-width="1.3" stroke-dasharray="4 7" />
      <circle cx="300" cy="300" r="138" fill="none" stroke="#2a5771" stroke-width="1.3" />
      <circle cx="300" cy="300" r="86" fill="url(#phiGlow)" stroke="#d3b16b" stroke-width="2.4" />
      <polygon points="300,44 556,300 300,556 44,300" fill="none" stroke="#d7b773" stroke-width="2.2" />
      <polygon points="300,88 512,300 300,512 88,300" fill="none" stroke="#2b546d" stroke-width="1.8" />
      <g stroke="#89704a" stroke-width="1.1">
        <line x1="300" y1="48" x2="300" y2="552" />
        <line x1="48" y1="300" x2="552" y2="300" />
        <line x1="110" y1="110" x2="490" y2="490" />
        <line x1="490" y1="110" x2="110" y2="490" />
      </g>
      <text x="300" y="282" text-anchor="middle" class="phi-mark">phi</text>
      <text x="300" y="322" text-anchor="middle" class="phi-caption">123 / 618 / 99</text>
      ${labels
        .map(
          (item) => `
            <g transform="translate(${item.x}, ${item.y})">
              <rect x="-38" y="-16" width="76" height="32" rx="8" fill="#fff8ec" stroke="#b38d48" stroke-width="1.5" />
              <text text-anchor="middle" y="7" class="phi-node">${escapeHtml(item.value)}</text>
            </g>`,
        )
        .join("")}
    </svg>
  `;
}

function renderDiscoveryCards(items) {
  return items
    .map(
      (item) => `
        <article class="discovery-card">
          <div class="discovery-number">${escapeHtml(item.number)}</div>
          <div class="discovery-body">
            <h3>${escapeHtml(item.title)}</h3>
            <div class="discovery-formula">${escapeHtml(item.formula)}</div>
            <div class="discovery-meta">
              <span>${escapeHtml(item.target)}</span>
              <span>${escapeHtml(item.precision)}</span>
            </div>
            <p>${escapeHtml(item.meaning)}</p>
            <ul>
              ${item.points.map((point) => `<li>${escapeHtml(point)}</li>`).join("")}
            </ul>
          </div>
        </article>`,
    )
    .join("");
}

function buildHtml() {
  const discoveryCardsA = renderDiscoveryCards(discoveries.slice(0, 2));
  const discoveryCardsB = renderDiscoveryCards(discoveries.slice(2));
  const luxeFonts = fontFaceCss();
  const coverRosette = buildRosetteSvg({
    centerTop: "phi",
    centerBottom: "123 / 618 / 99",
    labels: ["19", "55", "89", "123", "786", "99", "61", "618"],
    dark: true,
  });
  const coverConstellation = buildConstellationStripSvg({
    items: ["19", "55", "89", "123", "618"],
    dark: true,
  });
  const vocabularyMarkup = vocabulary
    .map(
      ([label, value, meaning]) => `
        <tr>
          <td>${escapeHtml(label)}</td>
          <td>${escapeHtml(value)}</td>
          <td>${escapeHtml(meaning)}</td>
        </tr>`,
    )
    .join("");

  const dhikrMarkup = dhikrs
    .map(
      (item) => `
        <article class="ritual-card">
          <h3>${escapeHtml(item.title)}</h3>
          <p><strong>Structure.</strong> ${escapeHtml(item.structure)}</p>
          <p>${escapeHtml(item.use)}</p>
        </article>`,
    )
    .join("");

  const grabovoiMarkup = grabovoiCodes
    .map(
      ([code, title, use]) => `
        <article class="code-band">
          <div class="code-value">${escapeHtml(code)}</div>
          <div class="code-body">
            <h3>${escapeHtml(title)}</h3>
            <p>${escapeHtml(use)}</p>
          </div>
        </article>`,
    )
    .join("");

  const radionicsMarkup = radionics
    .map((item) => `<li>${escapeHtml(item)}</li>`)
    .join("");

  const weekdayMarkup = weekdayPractice
    .map(
      ([day, formula, use]) => `
        <tr>
          <td>${escapeHtml(day)}</td>
          <td>${escapeHtml(formula)}</td>
          <td>${escapeHtml(use)}</td>
        </tr>`,
    )
    .join("");

  const referenceMarkup = referenceRows
    .map(
      (row) => `
        <tr>
          ${row.map((cell) => `<td>${escapeHtml(cell)}</td>`).join("")}
        </tr>`,
    )
    .join("");

  return `<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8" />
    <title>Decouverte du Nombre d'Or dans le Coran</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      ${luxeFonts}
      :root {
        --paper: #f3efe3;
        --paper-soft: #fbf8f2;
        --ink: #1d2330;
        --muted: #615b52;
        --line: rgba(45, 67, 95, 0.18);
        --gold: #af8a4d;
        --gold-bright: #d8ba7d;
        --blue: #254b64;
        --blue-soft: #dfe8ef;
        --forest: #395f55;
        --forest-soft: #e1ebe7;
        --wine: #6d3945;
        --wine-soft: #f1e2e6;
        --night: #11161d;
        --night-2: #1d2431;
      }

      @page {
        size: A4;
        margin: 0;
      }

      * {
        box-sizing: border-box;
      }

      html, body {
        margin: 0;
        padding: 0;
        background: #d8d1c3;
        color: var(--ink);
        font-family: "LuxeText", Georgia, serif;
      }

      body {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }

      .page {
        position: relative;
        width: 210mm;
        min-height: 297mm;
        margin: 0 auto;
        padding: 16mm 16mm 14mm;
        overflow: hidden;
        page-break-after: always;
        background:
          linear-gradient(180deg, rgba(255,255,255,0.58), rgba(255,255,255,0.12)),
          radial-gradient(circle at top right, rgba(205, 176, 110, 0.22), transparent 32%),
          radial-gradient(circle at bottom left, rgba(34, 71, 103, 0.12), transparent 36%),
          var(--paper);
      }

      .page::before {
        content: "";
        position: absolute;
        inset: 8mm;
        border: 1px solid rgba(72, 67, 55, 0.22);
      }

      .page::after {
        content: "";
        position: absolute;
        inset: 11mm;
        border: 1px solid rgba(72, 67, 55, 0.08);
      }

      .page-dark {
        background:
          radial-gradient(circle at 18% 12%, rgba(221, 190, 118, 0.18), transparent 20%),
          radial-gradient(circle at 82% 24%, rgba(59, 96, 119, 0.18), transparent 24%),
          linear-gradient(180deg, var(--night-2), var(--night));
        color: #f7f0df;
      }

      .page-dark::before {
        border-color: rgba(216, 188, 126, 0.32);
      }

      .page-dark::after {
        border-color: rgba(216, 188, 126, 0.12);
      }

      .ornament {
        position: absolute;
        left: 16mm;
        right: 16mm;
        height: 7mm;
        background:
          linear-gradient(90deg, transparent, rgba(216, 188, 126, 0.7) 18%, rgba(216, 188, 126, 0.94) 50%, rgba(216, 188, 126, 0.7) 82%, transparent);
      }

      .ornament.top {
        top: 12mm;
      }

      .ornament.bottom {
        bottom: 11mm;
      }

      .cover {
        display: grid;
        grid-template-rows: auto auto auto 1fr auto;
        gap: 8mm;
        min-height: 100%;
      }

      .cover-kicker {
        display: flex;
        justify-content: space-between;
        font-size: 10px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: rgba(244, 235, 212, 0.68);
      }

      .cover h1 {
        margin: 0;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 30pt;
        line-height: 0.92;
        color: #f4e7c5;
        text-transform: uppercase;
      }

      .cover .subtitle {
        max-width: 142mm;
        margin: 4mm 0 0;
        font-size: 13.5pt;
        line-height: 1.3;
        color: rgba(247, 240, 223, 0.9);
      }

      .cover .arabic {
        font-size: 21pt;
        color: #edd39b;
        letter-spacing: 0.03em;
      }

      .cover-grid {
        display: grid;
        grid-template-columns: 1.1fr 0.9fr;
        gap: 10mm;
        align-items: start;
      }

      .cover-showcase {
        display: grid;
        grid-template-columns: 0.96fr 1.04fr;
        gap: 8mm;
        align-items: stretch;
      }

      .cover-figure {
        position: relative;
        min-height: 96mm;
        padding: 5mm 5mm 4mm;
        border: 1px solid rgba(216, 188, 126, 0.24);
        background:
          radial-gradient(circle at center, rgba(255,255,255,0.04), transparent 58%),
          rgba(255, 255, 255, 0.03);
      }

      .cover-figure::before {
        content: "";
        position: absolute;
        inset: 3mm;
        border: 1px solid rgba(216, 188, 126, 0.1);
      }

      .cover-figure .hero-rosette {
        display: block;
        width: 100%;
        max-width: 96mm;
        margin: 0 auto;
      }

      .cover-strip {
        margin-top: 4mm;
      }

      .cover-strip .constellation-strip {
        display: block;
        width: 100%;
      }

      .cover-panel,
      .cover-quote,
      .box,
      .research-note,
      .dense-panel,
      .table-shell,
      .formula-panel {
        position: relative;
        border: 1px solid rgba(183, 143, 73, 0.34);
        background: rgba(255, 249, 236, 0.78);
        padding: 6mm;
      }

      .page-dark .cover-panel,
      .page-dark .cover-quote {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(216, 188, 126, 0.28);
      }

      .page-dark .cover-panel::before,
      .page-dark .cover-quote::before,
      .box::before,
      .research-note::before,
      .dense-panel::before,
      .table-shell::before,
      .formula-panel::before {
        content: "";
        position: absolute;
        inset: 3mm;
        border: 1px solid rgba(183, 143, 73, 0.14);
      }

      .cover-panel h3,
      .cover-quote h3,
      .box h3,
      .dense-panel h3,
      .research-note h3,
      .formula-panel h3 {
        margin: 0 0 3mm;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 12pt;
        line-height: 1.1;
      }

      .cover-panel p,
      .cover-quote p,
      .box p,
      .research-note p,
      .dense-panel p,
      .formula-panel p {
        margin: 0;
        font-size: 10pt;
        line-height: 1.55;
      }

      .cover-list {
        margin: 0;
        padding-left: 18px;
        font-size: 10pt;
        line-height: 1.6;
      }

      .section-head {
        margin-bottom: 6mm;
      }

      .eyebrow {
        font-size: 9px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--gold);
        margin-bottom: 2mm;
      }

      .section-head h2 {
        margin: 0;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 21pt;
        line-height: 1;
        color: var(--ink);
      }

      .section-head .deck,
      .section-head h2 + p {
        max-width: 150mm;
      }

      .deck {
        margin: 2.5mm 0 0;
        max-width: 148mm;
        font-size: 10.5pt;
        line-height: 1.45;
        color: var(--muted);
      }

      .formula-strip {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 3mm;
      }

      .formula-pill {
        display: flex;
        align-items: center;
        gap: 2.4mm;
        min-height: 14mm;
        padding: 0 4mm;
        border: 1px solid rgba(173, 138, 73, 0.28);
        background: rgba(255, 249, 236, 0.82);
        font-size: 10pt;
      }

      .formula-pill span {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 999px;
        background: var(--gold);
      }

      .lead-grid {
        display: grid;
        grid-template-columns: 1.08fr 0.92fr;
        gap: 8mm;
      }

      .quote-badge {
        display: inline-flex;
        align-items: center;
        gap: 2mm;
        padding: 2mm 3.5mm;
        background: var(--blue-soft);
        border: 1px solid rgba(43, 84, 109, 0.16);
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 8px;
        color: var(--blue);
      }

      .quote-badge::before {
        content: "";
        width: 8px;
        height: 1px;
        background: var(--gold);
      }

      .vocab-table,
      .reference-table,
      .weekday-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 9.4pt;
        line-height: 1.45;
      }

      .vocab-table th,
      .reference-table th,
      .weekday-table th {
        text-align: left;
        padding: 3mm 3.5mm;
        font-weight: 600;
        color: var(--blue);
        border-bottom: 1px solid rgba(43, 84, 109, 0.2);
        background: rgba(223, 232, 239, 0.55);
      }

      .vocab-table td,
      .reference-table td,
      .weekday-table td {
        padding: 3mm 3.5mm;
        border-bottom: 1px solid rgba(43, 84, 109, 0.12);
        vertical-align: top;
      }

      .discoveries {
        display: grid;
        gap: 5mm;
      }

      .discovery-card {
        display: grid;
        grid-template-columns: 18mm 1fr;
        gap: 5mm;
        padding: 5mm;
        border: 1px solid rgba(176, 137, 73, 0.26);
        background: rgba(255, 250, 240, 0.82);
      }

      .discovery-number {
        display: grid;
        place-items: center;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 17pt;
        color: var(--gold);
        border: 1px solid rgba(176, 137, 73, 0.3);
        background: rgba(255, 255, 255, 0.52);
      }

      .discovery-body h3 {
        margin: 0;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 13pt;
      }

      .discovery-formula {
        margin-top: 2mm;
        font-size: 10.2pt;
        color: var(--blue);
        font-weight: 600;
      }

      .discovery-meta {
        display: flex;
        gap: 3mm;
        margin-top: 2.4mm;
        flex-wrap: wrap;
      }

      .discovery-meta span {
        display: inline-flex;
        align-items: center;
        min-height: 9mm;
        padding: 0 3.5mm;
        border-radius: 999px;
        background: var(--wine-soft);
        color: var(--wine);
        font-size: 8.8pt;
      }

      .discovery-body p {
        margin: 3mm 0 0;
        font-size: 9.8pt;
        line-height: 1.52;
      }

      .discovery-body ul,
      .box ul,
      .research-note ul {
        margin: 3mm 0 0;
        padding-left: 18px;
        font-size: 9.4pt;
        line-height: 1.55;
      }

      .split {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8mm;
      }

      .ritual-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 5mm;
      }

      .ritual-card {
        border: 1px solid rgba(176, 137, 73, 0.24);
        background: rgba(255, 249, 236, 0.82);
        padding: 5mm;
      }

      .ritual-card h3 {
        margin: 0 0 2mm;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 12pt;
        color: var(--forest);
      }

      .ritual-card p {
        margin: 0;
        font-size: 9.6pt;
        line-height: 1.5;
      }

      .ritual-card p + p {
        margin-top: 2mm;
      }

      .talisman-layout {
        display: grid;
        grid-template-columns: 1.08fr 0.92fr;
        gap: 8mm;
        align-items: center;
      }

      .talisman-svg {
        width: 100%;
        max-width: 146mm;
        display: block;
      }

      .phi-mark {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 66px;
        fill: #1c2430;
      }

      .phi-caption {
        font-size: 16px;
        fill: #7f6440;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }

      .phi-node {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 28px;
        fill: #254b64;
      }

      .code-stack {
        display: grid;
        gap: 4mm;
      }

      .code-band {
        display: grid;
        grid-template-columns: 44mm 1fr;
        gap: 5mm;
        padding: 4.5mm;
        border: 1px solid rgba(176, 137, 73, 0.24);
        background: rgba(255, 249, 236, 0.82);
      }

      .code-value {
        display: grid;
        place-items: center;
        min-height: 18mm;
        border: 1px solid rgba(37, 75, 100, 0.16);
        background: var(--blue-soft);
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 16pt;
        color: var(--blue);
      }

      .code-body h3 {
        margin: 0 0 1.5mm;
        font-size: 11pt;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
      }

      .code-body p {
        margin: 0;
        font-size: 9.5pt;
        line-height: 1.48;
      }

      .dense-list {
        margin: 0;
        padding-left: 18px;
        font-size: 9.6pt;
        line-height: 1.55;
      }

      .dense-list li + li {
        margin-top: 1.5mm;
      }

      .footer-note {
        position: absolute;
        left: 16mm;
        right: 16mm;
        bottom: 16mm;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 9px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(104, 94, 81, 0.72);
      }

      .page-dark .footer-note {
        color: rgba(240, 233, 221, 0.62);
      }
    </style>
  </head>
  <body>
    <section class="page page-dark">
      <div class="ornament top"></div>
      <div class="ornament bottom"></div>
      <div class="cover">
        <div class="cover-kicker">
          <span>Collection richesse et abondance</span>
          <span>Phase 2 luxe</span>
        </div>
        <div>
          <h1>Decouverte du nombre d'or<br />dans le Coran</h1>
          <p class="subtitle">Codes mathematiques du rizq, corridor Fibonacci, dhikr, talisman, radionique et calendrier operatif.</p>
        </div>
        <div class="arabic">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
        <div class="cover-showcase">
          <div>
            <div class="cover-panel">
              <h3>Architecture du dossier</h3>
              <ul class="cover-list">
                <li>5 decouvertes numeriques autour du rizq</li>
                <li>Une charpente fondee sur 19, 55, 89, 123, 618 et 99</li>
                <li>5 applications pratiques : dhikr, talisman, codes, radionique, calendrier</li>
                <li>Une lecture experimentale dans le meme esprit que le projet original</li>
              </ul>
            </div>
            <div class="cover-quote" style="margin-top: 5mm;">
              <h3>Formules de seuil</h3>
              <p>19 x 4 x phi -> 123</p>
              <p>55 x phi -> 89</p>
              <p>489 x phi -> 786</p>
              <p>618 x phi -> 1000</p>
              <p>61 x phi -> 99</p>
            </div>
          </div>
          <div class="cover-figure">
            ${coverRosette}
            <div class="cover-strip">${coverConstellation}</div>
          </div>
        </div>
        <div class="footer-note">
          <span>Refonte editoriale luxe</span>
          <span>Coran Num Tal</span>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Prologue", "La these generale", "Le nombre d'or est ici lu comme un multiplicateur de passage : il fait glisser une matrice numerique vers un seuil symbolique de manifestation.")}
      ${formulaStrip([
        "19 x 4 x phi -> 123",
        "34 -> 55 -> 89",
        "56 = porte manifeste",
        "618 = coeur mercy-code",
        "61 -> 99",
      ])}
      <div class="lead-grid" style="margin-top: 7mm;">
        <div class="box">
          <div class="quote-badge">Introduction</div>
          <h3 style="margin-top: 3mm;">Pourquoi ce dossier existe</h3>
          <p>La premiere version du PDF contenait beaucoup d'informations fortes mais presentait des faiblesses de mise en page, de hierarchie et de lisibilite. Cette edition premium conserve le coeur du propos et le recompose comme un veritable dossier de recherche esoterique.</p>
          <p style="margin-top: 3mm;">Le fil conducteur reste simple : le rizq n'est pas seulement lu comme un theme textuel, mais comme un champ numerique structure par quelques seuils recurrents. Ces seuils alimentent ensuite des pratiques de dhikr, de sceau et de montage.</p>
        </div>
        <div class="research-note">
          <div class="quote-badge">Nombres cles</div>
          <h3 style="margin-top: 3mm;">Vocabulaire essentiel</h3>
          <p>Les valeurs suivantes sont les pierres de la collection :</p>
          <ul>
            <li>123 : porte textuelle du rizq</li>
            <li>55 et 89 : corridor Fibonacci de misericorde et d'aube</li>
            <li>489 et 786 : paire d'ouverture</li>
            <li>618 : recentrage misericordieux du systeme</li>
            <li>61 et 99 : fermeture rituelle et completude</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Lexique", "Table des nombres-clés", "Les figures centrales du dossier sont posees ici avant le detail des cinq decouvertes.")}
      <div class="table-shell">
        <table class="vocab-table">
          <thead>
            <tr><th>Element</th><th>Valeur</th><th>Lecture operative</th></tr>
          </thead>
          <tbody>
            ${vocabularyMarkup}
          </tbody>
        </table>
      </div>
      <div class="split" style="margin-top: 7mm;">
        <div class="box">
          <h3>Couloir principal</h3>
          <p>34 -> 55 -> 56 -> 89 est interprete comme une charniere : prosperite, misericorde, manifestation, lucidite. Cette suite organise plusieurs pages du dossier et permet d'articuler le nombre d'or avec la suite de Fibonacci.</p>
        </div>
        <div class="box">
          <h3>Lecture pratique</h3>
          <p>Le dossier ne s'arrete pas aux calculs. Chaque seuil est relie a une pratique : nombre de repetitions, code a tracer, noeud a activer ou protocole a suivre sur plusieurs jours.</p>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Decouvertes I", "Les deux premieres portes", "La matrice du rizq et le corridor Rahman/Fajr forment la base de la suite.")}
      <div class="discoveries">
        ${discoveryCardsA}
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Decouvertes II", "Ouverture, misericorde, cycle", "Les trois portes suivantes transforment la lecture numerique en mecanique rituelle.")}
      <div class="discoveries">
        ${discoveryCardsB}
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Applications I", "Dhikr phi du rizq", "Cinq protocoles de rememoration, classes par fonction operatoire plutot que par pure accumulation.")}
      <div class="ritual-grid">
        ${dhikrMarkup}
      </div>
      <div class="split" style="margin-top: 7mm;">
        <div class="box">
          <h3>Routine quotidienne suggeree</h3>
          <ul>
            <li>Matin : Dhikr A + ouverture precise de l'intention.</li>
            <li>Milieu de journee : rappel 51:58 ou 65:2-3 avant une action concrete.</li>
            <li>Soir : Dhikr C ou D pour fermer le champ et enregistrer la journee.</li>
          </ul>
        </div>
        <div class="formula-panel">
          <h3>Seuils de repetition</h3>
          <p>76, 79, 61, 34/55/89 et 61/8 sont les cycles les plus naturels pour cette famille de pratiques. Ils structurent le souffle, la concentration et l'intensite sans saturer la page.</p>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Applications II", "Talisman phi du rizq", "Le sceau rassemble les cinq decouvertes sous une geometie commune : etoile a huit directions, anneaux, centre et corridor de seuils.")}
      <div class="talisman-layout">
        <div>${talismanSvg()}</div>
        <div class="box">
          <h3>Instructions de fabrication</h3>
          <ul>
            <li>Tracer deux carres superposes pour former l'etoile a 8 directions.</li>
            <li>Inscrire au centre phi ou le triplet 123 / 618 / 99.</li>
            <li>Poser 55, 89, 123, 319, 489, 61, 99 et 786 sur l'anneau externe.</li>
            <li>Ecrire au dos la formule 19 x 4 x phi -> 123.</li>
            <li>Activer avec le cycle 61 ou le corridor 34-55-89.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Applications III", "Codes Grabovoi phi", "La logique des codes est recomposee ici comme une bibliotheque courte, lisible et directement utilisable.")}
      <div class="code-stack">
        ${grabovoiMarkup}
      </div>
      <div class="split" style="margin-top: 7mm;">
        <div class="box">
          <h3>Mode de lecture</h3>
          <p>Lire chaque code lentement, chiffre par chiffre, avant de le condenser en un seul souffle. Le code sert moins de preuve que de structure attentionnelle.</p>
        </div>
        <div class="box">
          <h3>Usages suggérés</h3>
          <p>Papier, portefeuille, sous un verre d'eau, sous l'oreiller ou au centre d'un support radionique. Les cycles 7, 19, 33 et 40 jours restent les plus stables.</p>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Applications IV", "Radionique et calendrier", "Le dossier original reliait le nombre d'or au montage physique et aux jours du cycle. Cette refonte clarifie ces usages.")}
      <div class="split">
        <div class="dense-panel">
          <h3>Optimisations radioniques</h3>
          <ul class="dense-list">
            ${radionicsMarkup}
          </ul>
        </div>
        <div class="table-shell">
          <table class="weekday-table">
            <thead>
              <tr><th>Jour</th><th>Formule</th><th>Pratique</th></tr>
            </thead>
            <tbody>
              ${weekdayMarkup}
            </tbody>
          </table>
        </div>
      </div>
      <div class="box" style="margin-top: 7mm;">
        <h3>Regle de bon usage</h3>
        <p>Le calendrier sert a rythmer la pratique, pas a rigidifier le champ. Les jours, les repetitions et les codes restent des supports de focalisation. Le moteur du document est l'axe intention + nombre + repetition + action concrete.</p>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Reference", "Tableau des relations phi", "Les rapports principaux sont isoles ici pour consultation rapide.")}
      <div class="table-shell">
        <table class="reference-table">
          <thead>
            <tr><th>Base</th><th>Operation</th><th>Resultat</th><th>Cible</th><th>Lecture</th></tr>
          </thead>
          <tbody>
            ${referenceMarkup}
          </tbody>
        </table>
      </div>
      <div class="split" style="margin-top: 7mm;">
        <div class="box">
          <h3>Architecture de synthese</h3>
          <p>Source numerique -> couloir Fibonacci -> porte d'ouverture -> coeur misericordieux -> cycle de fixation. C'est cette architecture qui permet au PDF de rester lisible tout en preservant sa densite symbolique.</p>
        </div>
        <div class="box">
          <h3>Fil conducteur</h3>
          <p>Le secret du rizq, dans cette lecture, ne se situe pas dans un seul nombre. Il apparait quand les seuils se mettent a dialoguer entre eux : 19, 55, 89, 123, 618, 786, 99.</p>
        </div>
      </div>
    </section>

    <section class="page page-dark">
      <div class="ornament top"></div>
      <div class="ornament bottom"></div>
      ${sectionTitle("Conclusion", "Le dossier refondu", "Le contenu reste dans l'esprit du projet originel, mais la presentation est maintenant pensée comme un document premium, stable, lisible et coherent.")}
      <div class="cover-grid" style="margin-top: 8mm;">
        <div class="cover-panel">
          <h3>Ce que fixe cette edition</h3>
          <ul class="cover-list">
            <li>Une lecture claire des cinq decouvertes</li>
            <li>Une separation nette entre calcul, interpretation et pratique</li>
            <li>Des tables lisibles et une geometie exploitable</li>
            <li>Un vrai rythme editorial de page en page</li>
          </ul>
        </div>
        <div class="cover-quote">
          <h3>Formule finale</h3>
          <p>19 x 4 x phi -> 123</p>
          <p>55 x phi -> 89</p>
          <p>61 x phi -> 99</p>
          <p>618 au centre du champ</p>
        </div>
      </div>
      <div class="research-note" style="margin-top: 10mm; background: rgba(255,255,255,0.05); border-color: rgba(216,188,126,0.28);">
        <h3 style="color: #f0dfb5;">Wa-Allahu min wara'i al-qasd</h3>
        <p style="color: rgba(246, 237, 220, 0.86);">Dans cette version premium, le nombre ne remplace pas l'intention : il lui sert de charpente, d'ordre et de rappel.</p>
      </div>
      <div class="footer-note">
        <span>Decouverte phi coran rizq</span>
        <span>Edition premium refondue</span>
      </div>
    </section>
  </body>
</html>`;
}

async function loadPlaywright() {
  const playwrightEntry = path.join(bundledNodeModules, "playwright", "index.mjs");
  return import(pathToFileURL(playwrightEntry).href);
}

async function renderPdf() {
  ensureDir(htmlDir);
  ensureDir(pdfDir);
  ensureDir(previewDir);
  fs.writeFileSync(htmlPath, buildHtml(), "utf8");

  const { chromium } = await loadPlaywright();
  const browser = await chromium.launch({
    headless: true,
    executablePath: resolveChromeExecutable(),
  });

  try {
    const page = await browser.newPage({
      viewport: { width: 1440, height: 2048 },
      deviceScaleFactor: 2,
    });
    await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "networkidle" });
    await page.pdf({
      path: pdfPath,
      format: "A4",
      printBackground: true,
      preferCSSPageSize: true,
      margin: { top: "0mm", right: "0mm", bottom: "0mm", left: "0mm" },
    });

    await page.screenshot({ path: previewPath, fullPage: false });
    await page.evaluate(() => window.scrollTo(0, window.innerHeight * 5.2));
    await page.screenshot({ path: previewDensePath, fullPage: false });
  } finally {
    await browser.close();
  }
}

await renderPdf();
console.log(`HTML generated: ${htmlPath}`);
console.log(`PDF generated: ${pdfPath}`);
