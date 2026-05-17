import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { buildConstellationStripSvg, buildRosetteSvg, fontFaceCss } from "./luxe_collection_assets.mjs";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..", "..");
const bundledNodeModules = path.resolve(path.dirname(process.execPath), "..", "node_modules");

const documentsDir = path.join(rootDir, "documents");
const htmlDir = path.join(documentsDir, "html", "richesse_abondance");
const pdfDir = path.join(documentsDir, "pdf", "richesse_abondance");
const previewDir = path.join(documentsDir, "preview");

const htmlPath = path.join(htmlDir, "Secret_Rizq_Phi_Grabovoi_Esoterique_Premium.html");
const pdfPath = path.join(pdfDir, "Secret_Rizq_Phi_Grabovoi_Esoterique.pdf");
const previewPath = path.join(previewDir, "Secret_Rizq_Phi_Grabovoi_Esoterique_Premium_page1.png");

const chromeCandidates = [
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
];

const keyFormulae = [
  "19 x 4 x phi -> 123",
  "34 -> 55 -> 89",
  "61 x phi -> 99",
  "618 au centre du champ",
  "786 / phi ~ 489",
];

const textualGates = [
  "51:58 : Ar-Razzaq comme source pure de la subsistance.",
  "65:2-3 : taqwa, issue subtile et provision inattendue.",
  "71:10-12 : istighfar, pluie, biens et renforcement du foyer.",
  "14:7 : gratitude, augmentation et stabilisation du flux.",
  "2:261 / 34:39 : depense juste, multiplication et remplacement.",
  "89:15-20 : richesse et restriction comme epreuve de discernement.",
];

const rootMatrix = [
  { root: "RZQ", count: "123", meaning: "champ lexical du rizq, de la provision et de la subsistance" },
  { root: "SHKR", count: "75", meaning: "gratitude, reconnaissance, activation de l'augmentation" },
  { root: "BRK", count: "32", meaning: "baraka, stabilisation et benediction du flux" },
  { root: "WQY", count: "258", meaning: "taqwa, protection vibratoire et garde interieure" },
];

const numericCore = [
  ["19", "code coranique"],
  ["61", "cycle complet du rituel"],
  ["76", "19 x 4, matrice des 4 noms"],
  ["99", "horizon complet des Noms"],
  ["123", "racine textuelle du rizq"],
  ["307", "abjad de RZQ"],
  ["319", "abjad de Ya Razzaq"],
  ["489", "abjad simple de Fattah"],
  ["618", "Rahman + Rahim"],
  ["786", "Basmala"],
];

const phiPorts = [
  {
    number: "01",
    title: "Corridor Saba -> Rahman",
    formula: "34 x phi = 55.0132 -> seuil Rahman",
    reading:
      "Saba parle de prosperite et de gratitude. Rahman deverse les faveurs. Les deux nombres se suivent comme marches d'un meme axe.",
  },
  {
    number: "02",
    title: "Corridor Rahman -> Fajr",
    formula: "55 x phi = 88.9919 -> seuil Fajr",
    reading:
      "L'abondance ne s'arrete pas a la faveur. Elle se prolonge vers la lucidite, le discernement et la revelation du test.",
  },
  {
    number: "03",
    title: "Matrice des 4 noms",
    formula: "19 x 4 = 76 ; 76 x phi = 122.9706",
    reading:
      "Le code 19 applique a quatre noms du rizq touche le palier 123 dans la lecture numerologique de la racine RZQ.",
  },
  {
    number: "04",
    title: "Cycle operatif",
    formula: "61 x phi = 98.7001 -> horizon 99",
    reading:
      "Le rituel se ferme sur 61, puis se projette vers 99 comme completude des Noms et amplification du champ.",
  },
  {
    number: "05",
    title: "Coeur misericordieux",
    formula: "329 + 289 = 618 ; 618 x phi = 999.9454",
    reading:
      "Le vrai pivot du systeme reconstruit est 618. Rahman et Rahim recentrent le flux sur la misericorde avant la capture materielle.",
  },
  {
    number: "06",
    title: "Basmala et Fattah",
    formula: "786 / phi = 485.7717 ~ 489",
    reading:
      "La resonance n'est pas exacte, mais le rapprochement Basmala / Fattah reste operatif dans le langage rituel du document.",
  },
];

const grabovoiCodes = [
  {
    code: "123 55 89",
    title: "Corridor phi du rizq",
    composition: "123 = rizq ; 55 = Rahman ; 89 = Fajr",
    use: "Ouverture, reception, clarification de l'intention.",
  },
  {
    code: "786 489 618",
    title: "Porte d'ouverture misericordieuse",
    composition: "786 = Basmala ; 489 = Fattah ; 618 = Rahman + Rahim",
    use: "Code d'entree avant dhikr, talisman ou montage radionique.",
  },
  {
    code: "6119 078",
    title: "Cycle operatif complet",
    composition: "61 = rituel ; 19 = code ; 07 = multiplication ; 8 = directions",
    use: "Stabilisation sur 7 ou 21 jours.",
  },
  {
    code: "319 489 618 786",
    title: "Echelle integrale du flux",
    composition: "Ya Razzaq -> Fattah -> Rahman/Rahim -> Basmala",
    use: "Montee progressive : appel, ouverture, effusion, sceau.",
  },
  {
    code: "307 123 786",
    title: "Racine -> manifestation -> porte",
    composition: "307 = abjad de rizq ; 123 = occurrences ; 786 = ouverture",
    use: "Concretisation materielle et mentale.",
  },
];

const dhikrs = [
  {
    title: "Dhikr A  |  Matrice 76",
    structure: "19x Ya Razzaq + 19x Ya Fattah + 19x Ya Ghani + 19x Ya Mughni",
    purpose: "Structure minimale pour appeler les quatre piliers du flux.",
  },
  {
    title: "Dhikr B  |  Cycle 61",
    structure: "1 Basmala + 7 Istighfar + 19 Ya Razzaq + 33 Salawat + 1 sceau",
    purpose: "Cycle rituel complet, utile avant sommeil ou avant un travail important.",
  },
  {
    title: "Dhikr C  |  Corridor 34-55-89",
    structure: "34x gratitude + 55x Ya Rahman + 89 respirations conscientes",
    purpose: "Travail sur la conscience de l'abondance avant sa manifestation externe.",
  },
  {
    title: "Dhikr D  |  Porte 618",
    structure: "61x Ya Rahman + 8x Ya Rahim, ou 34x/55x selon le ressenti",
    purpose: "Axe de deblocage lorsque le coeur est ferme et que le flux materiel stagne.",
  },
];

const radionics = [
  "Spirale primaire : 7 tours en cuivre.",
  "Longueur conseillee : 61.8 cm pour signer la porte 618.",
  "Centre : 786 489 618 en triangle ou en spirale.",
  "Anneau externe : 8 directions avec 55, 89, 123, 319, 489, 618, 786, 99.",
  "Quartz ou pierre claire au centre si le montage est physique.",
  "Activation : 1 cycle Dhikr B par jour sur 7, 14 ou 21 jours.",
];

const routine = [
  {
    label: "Matin",
    items: [
      "Basmala 1x",
      "Dhikr A ou lecture du code 123 55 89",
      "Intention ecrite en une phrase tres precise",
    ],
  },
  {
    label: "Milieu de journee",
    items: [
      "Rappel 51:58 ou 65:2-3",
      "Action concrete : appel, travail, vente, creation, demande, service",
      "Mini lecture du code 319 489 618 786",
    ],
  },
  {
    label: "Soir",
    items: [
      "Dhikr B",
      "3 lectures lentes de 786 489 618",
      "Journal : signe, synchronicite, blocage, ouverture observee",
    ],
  },
];

const sources = [
  "Quranic Arabic Corpus - racine RZQ.",
  "Quranic Arabic Corpus - racine BRK.",
  "Study Quran Arabic - racine SHKR.",
  "Quranic Arabic Corpus - racine WQY.",
  "Versets de travail : 2:261, 7:96, 14:7, 34:15, 51:58, 62:10, 65:2-3, 71:10-12, 89:15-20.",
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

function sectionTitle(eyebrow, title, deck = "") {
  return `
    <div class="section-head">
      <div class="eyebrow">${escapeHtml(eyebrow)}</div>
      <h2>${escapeHtml(title)}</h2>
      ${deck ? `<p class="deck">${escapeHtml(deck)}</p>` : ""}
    </div>
  `;
}

function formulaChips(items) {
  return `
    <div class="formula-grid">
      ${items
        .map((item) => `<div class="formula-chip"><span></span>${escapeHtml(item)}</div>`)
        .join("")}
    </div>
  `;
}

function rootTable() {
  return `
    <table class="root-table">
      <thead>
        <tr><th>Racine</th><th>Compte</th><th>Lecture</th></tr>
      </thead>
      <tbody>
        ${rootMatrix
          .map(
            (row) => `
              <tr>
                <td>${escapeHtml(row.root)}</td>
                <td>${escapeHtml(row.count)}</td>
                <td>${escapeHtml(row.meaning)}</td>
              </tr>`,
          )
          .join("")}
      </tbody>
    </table>
  `;
}

function talismanSvg() {
  const labels = [
    { value: "55", x: 300, y: 78 },
    { value: "89", x: 455, y: 132 },
    { value: "123", x: 520, y: 300 },
    { value: "319", x: 455, y: 468 },
    { value: "489", x: 300, y: 522 },
    { value: "61", x: 145, y: 468 },
    { value: "99", x: 80, y: 300 },
    { value: "786", x: 145, y: 132 },
  ];
  return `
    <svg class="talisman-svg" viewBox="0 0 600 600" aria-hidden="true">
      <defs>
        <radialGradient id="glow" cx="50%" cy="50%" r="70%">
          <stop offset="0%" stop-color="#f7f1de" stop-opacity="0.95" />
          <stop offset="100%" stop-color="#efe4c0" stop-opacity="0.2" />
        </radialGradient>
      </defs>
      <rect width="600" height="600" fill="none" />
      <circle cx="300" cy="300" r="222" fill="none" stroke="#aa8450" stroke-width="1.5" />
      <circle cx="300" cy="300" r="182" fill="none" stroke="#d8b776" stroke-width="1.2" stroke-dasharray="4 6" />
      <circle cx="300" cy="300" r="125" fill="none" stroke="#8b6b3f" stroke-width="1.2" />
      <polygon points="300,68 532,300 300,532 68,300" fill="none" stroke="#d6b16d" stroke-width="2" />
      <polygon points="300,35 565,300 300,565 35,300" fill="none" stroke="#70552f" stroke-width="1.4" />
      <g stroke="#a47f46" stroke-width="1.2">
        <line x1="300" y1="70" x2="300" y2="530" />
        <line x1="70" y1="300" x2="530" y2="300" />
        <line x1="123" y1="123" x2="477" y2="477" />
        <line x1="477" y1="123" x2="123" y2="477" />
      </g>
      <circle cx="300" cy="300" r="72" fill="url(#glow)" stroke="#d0ad66" stroke-width="2.2" />
      <text x="300" y="288" text-anchor="middle" class="talisman-center">618</text>
      <text x="300" y="320" text-anchor="middle" class="talisman-caption">Rahman + Rahim</text>
      ${labels
        .map(
          (label) => `
            <g transform="translate(${label.x}, ${label.y})">
              <rect x="-36" y="-17" width="72" height="34" rx="8" fill="#f7f2e3" stroke="#b59254" stroke-width="1.4" />
              <text text-anchor="middle" y="8" class="talisman-node">${escapeHtml(label.value)}</text>
            </g>`,
        )
        .join("")}
    </svg>
  `;
}

function buildHtml() {
  const luxeFonts = fontFaceCss();
  const coverRosette = buildRosetteSvg({
    centerTop: "618",
    centerBottom: "rizq / mercy-code",
    labels: ["19", "55", "89", "123", "307", "319", "489", "786"],
    dark: true,
    depth: "#2d4b42",
  });
  const coverConstellation = buildConstellationStripSvg({
    items: ["19", "76", "123", "618", "786", "99"],
    dark: true,
    depth: "#2d4b42",
  });
  const portalsMarkup = phiPorts
    .map(
      (port) => `
        <article class="portal-card">
          <div class="portal-number">${escapeHtml(port.number)}</div>
          <h3>${escapeHtml(port.title)}</h3>
          <div class="portal-formula">${escapeHtml(port.formula)}</div>
          <p>${escapeHtml(port.reading)}</p>
        </article>`,
    )
    .join("");

  const grabovoiMarkup = grabovoiCodes
    .map(
      (item) => `
        <article class="code-band">
          <div class="code-value">${escapeHtml(item.code)}</div>
          <div class="code-meta">
            <h3>${escapeHtml(item.title)}</h3>
            <p><strong>Composition.</strong> ${escapeHtml(item.composition)}</p>
            <p><strong>Usage.</strong> ${escapeHtml(item.use)}</p>
          </div>
        </article>`,
    )
    .join("");

  const dhikrMarkup = dhikrs
    .map(
      (item) => `
        <article class="ritual-card">
          <h3>${escapeHtml(item.title)}</h3>
          <p class="ritual-line"><strong>Structure.</strong> ${escapeHtml(item.structure)}</p>
          <p>${escapeHtml(item.purpose)}</p>
        </article>`,
    )
    .join("");

  const routineMarkup = routine
    .map(
      (block) => `
        <article class="routine-card">
          <h3>${escapeHtml(block.label)}</h3>
          <ul>
            ${block.items.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </article>`,
    )
    .join("");

  const numericCoreMarkup = numericCore
    .map(
      ([value, meaning]) => `
        <div class="numeric-chip">
          <div class="numeric-value">${escapeHtml(value)}</div>
          <div class="numeric-meaning">${escapeHtml(meaning)}</div>
        </div>`,
    )
    .join("");

  return `<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8" />
    <title>Le Secret du Rizq — Edition Premium</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      ${luxeFonts}
      :root {
        --paper: #f3ecda;
        --paper-soft: #fbf8f1;
        --ink: #1f1b16;
        --muted: #6f6558;
        --line: rgba(120, 95, 54, 0.28);
        --gold: #a98545;
        --gold-bright: #d6ba79;
        --forest: #2d4b42;
        --forest-soft: #dfe8e3;
        --wine: #6b3141;
        --wine-soft: #f0dde2;
        --night: #171512;
        --night-2: #232019;
        --sand: #e7dcc0;
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
        background: #d9d3c6;
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
          linear-gradient(180deg, rgba(255,255,255,0.55), rgba(255,255,255,0.12)),
          radial-gradient(circle at top right, rgba(215, 186, 121, 0.26), transparent 34%),
          radial-gradient(circle at bottom left, rgba(72, 103, 93, 0.12), transparent 36%),
          var(--paper);
      }

      .page::before {
        content: "";
        position: absolute;
        inset: 8mm;
        border: 1px solid rgba(128, 99, 54, 0.28);
        pointer-events: none;
      }

      .page::after {
        content: "";
        position: absolute;
        inset: 11mm;
        border: 1px solid rgba(128, 99, 54, 0.1);
        pointer-events: none;
      }

      .page-dark {
        background:
          radial-gradient(circle at 18% 15%, rgba(219, 187, 110, 0.18), transparent 20%),
          radial-gradient(circle at 80% 24%, rgba(92, 127, 115, 0.16), transparent 22%),
          linear-gradient(180deg, #1b1814 0%, #13110d 100%);
        color: #f4ecdb;
      }

      .page-dark::before {
        border-color: rgba(216, 188, 126, 0.28);
      }

      .page-dark::after {
        border-color: rgba(216, 188, 126, 0.14);
      }

      .top-ornament,
      .bottom-ornament {
        position: absolute;
        left: 16mm;
        right: 16mm;
        height: 7mm;
        background:
          linear-gradient(90deg, transparent 0%, rgba(169, 133, 69, 0.65) 18%, rgba(214, 186, 121, 0.95) 50%, rgba(169, 133, 69, 0.65) 82%, transparent 100%);
      }

      .top-ornament {
        top: 12mm;
      }

      .bottom-ornament {
        bottom: 11mm;
      }

      .cover {
        display: grid;
        grid-template-rows: auto auto 1fr auto;
        gap: 8mm;
        height: 100%;
      }

      .cover-kicker {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 10px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: rgba(244, 236, 219, 0.62);
      }

      .cover-hero {
        position: relative;
        padding-top: 18mm;
      }

      .cover-hero h1 {
        margin: 0;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 31pt;
        line-height: 0.95;
        color: #f3e4bc;
        text-transform: uppercase;
      }

      .cover-hero .subtitle {
        margin: 5mm 0 0;
        max-width: 140mm;
        font-size: 13.5pt;
        line-height: 1.28;
        color: rgba(243, 232, 208, 0.86);
      }

      .arabic-line {
        margin-top: 7mm;
        font-size: 22pt;
        color: #dfc182;
        letter-spacing: 0.03em;
      }

      .cover-grid {
        display: grid;
        grid-template-columns: 1.4fr 0.8fr;
        gap: 10mm;
        align-items: start;
      }

      .cover-rosette-shell {
        position: relative;
        margin-top: 6mm;
        padding: 5mm 5mm 4mm;
        border: 1px solid rgba(214, 186, 121, 0.18);
        background:
          radial-gradient(circle at center, rgba(255,255,255,0.05), transparent 58%),
          rgba(255,255,255,0.03);
      }

      .cover-rosette-shell::before {
        content: "";
        position: absolute;
        inset: 3mm;
        border: 1px solid rgba(214, 186, 121, 0.1);
      }

      .cover-rosette-shell .hero-rosette {
        display: block;
        width: 100%;
        max-width: 84mm;
        margin: 0 auto;
      }

      .cover-constellation {
        margin-top: 4mm;
      }

      .cover-constellation .constellation-strip {
        display: block;
        width: 100%;
      }

      .formula-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 3.5mm;
      }

      .formula-chip {
        display: flex;
        align-items: center;
        gap: 3mm;
        padding: 3.4mm 4mm;
        border: 1px solid rgba(214, 186, 121, 0.28);
        background: rgba(255, 255, 255, 0.03);
        min-height: 16mm;
        font-size: 10.5pt;
        line-height: 1.25;
      }

      .formula-chip span {
        width: 7px;
        height: 7px;
        border-radius: 999px;
        background: linear-gradient(180deg, #e6c47a, #8b6530);
        flex: none;
      }

      .manifesto {
        padding: 5mm;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(214, 186, 121, 0.18);
      }

      .manifesto h3,
      .side-note h3,
      .ritual-card h3,
      .portal-card h3,
      .routine-card h3,
      .code-meta h3 {
        margin: 0 0 2.5mm;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 15pt;
        line-height: 1.08;
        color: var(--ink);
      }

      .page-dark .manifesto h3 {
        color: #f1dfb7;
      }

      .manifesto p {
        margin: 0;
        font-size: 10pt;
        line-height: 1.55;
        color: rgba(243, 232, 208, 0.84);
      }

      .cover-footer {
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 10mm;
        font-size: 9pt;
        color: rgba(243, 232, 208, 0.62);
      }

      .folio {
        position: absolute;
        right: 18mm;
        bottom: 16mm;
        font-size: 8.5pt;
        color: var(--muted);
      }

      .page-dark .folio {
        color: rgba(243, 232, 208, 0.54);
      }

      .section-head {
        margin-bottom: 7mm;
      }

      .eyebrow {
        font-size: 8.5pt;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--gold);
        margin-bottom: 2.5mm;
      }

      h2 {
        margin: 0;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 24pt;
        line-height: 1;
        color: var(--ink);
      }

      .deck {
        margin: 3mm 0 0;
        max-width: 155mm;
        font-size: 11pt;
        line-height: 1.5;
        color: var(--muted);
      }

      .lede {
        font-size: 11.2pt;
        line-height: 1.7;
        margin: 0 0 5mm;
      }

      .text-columns {
        display: grid;
        grid-template-columns: 1.15fr 0.85fr;
        gap: 8mm;
      }

      .side-note,
      .note-panel,
      .root-panel,
      .numeric-panel,
      .corridor-panel {
        background: rgba(255, 255, 255, 0.54);
        border: 1px solid var(--line);
        padding: 5.2mm;
      }

      .root-panel {
        background: linear-gradient(180deg, rgba(255,255,255,0.72), rgba(247, 241, 225, 0.9));
      }

      .numeric-panel {
        background: linear-gradient(180deg, rgba(241, 233, 213, 0.98), rgba(231, 220, 192, 0.82));
      }

      .note-panel.success {
        background: linear-gradient(180deg, rgba(223, 232, 227, 0.95), rgba(252, 250, 244, 0.9));
      }

      .note-panel.warning {
        background: linear-gradient(180deg, rgba(240, 221, 226, 0.9), rgba(252, 248, 242, 0.9));
      }

      .side-note p,
      .note-panel p,
      .root-panel p,
      .numeric-panel p,
      .corridor-panel p {
        margin: 0;
        font-size: 10pt;
        line-height: 1.58;
      }

      .bullet-list {
        margin: 0;
        padding: 0;
        list-style: none;
        display: grid;
        gap: 2.2mm;
      }

      .bullet-list li {
        position: relative;
        padding-left: 5mm;
        font-size: 10pt;
        line-height: 1.52;
      }

      .bullet-list li::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0.72em;
        width: 6px;
        height: 6px;
        border-radius: 999px;
        background: linear-gradient(180deg, var(--gold-bright), var(--gold));
      }

      .number-strip {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 3mm;
        margin-bottom: 6mm;
      }

      .numeric-chip {
        background: rgba(255, 255, 255, 0.4);
        border: 1px solid var(--line);
        padding: 3mm;
        min-height: 20mm;
      }

      .numeric-value {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 17pt;
        line-height: 1;
        color: var(--forest);
      }

      .numeric-meaning {
        margin-top: 1.5mm;
        font-size: 8.7pt;
        line-height: 1.35;
        color: var(--muted);
      }

      .root-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 9.3pt;
      }

      .root-table th,
      .root-table td {
        border-bottom: 1px solid rgba(120, 95, 54, 0.18);
        padding: 3mm 2.4mm;
        text-align: left;
        vertical-align: top;
      }

      .root-table th {
        font-size: 8.3pt;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--muted);
      }

      .portals-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 4.4mm;
      }

      .portal-card,
      .ritual-card {
        position: relative;
        background: rgba(255,255,255,0.6);
        border: 1px solid var(--line);
        padding: 5mm;
        min-height: 40mm;
      }

      .portal-number {
        position: absolute;
        top: 4mm;
        right: 4mm;
        font-size: 8pt;
        letter-spacing: 0.16em;
        color: var(--gold);
      }

      .portal-formula {
        margin: 2mm 0 3mm;
        font-size: 9.2pt;
        line-height: 1.42;
        color: var(--forest);
        font-weight: 600;
      }

      .portal-card p,
      .ritual-card p {
        margin: 0;
        font-size: 9.6pt;
        line-height: 1.5;
      }

      .corridor-layout {
        display: grid;
        grid-template-columns: 1.15fr 0.85fr;
        gap: 8mm;
      }

      .corridor-track {
        position: relative;
        padding: 8mm 7mm 6mm;
        background:
          linear-gradient(180deg, rgba(255,255,255,0.72), rgba(247, 241, 225, 0.86));
        border: 1px solid var(--line);
      }

      .corridor-line {
        position: relative;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        align-items: center;
        gap: 4mm;
        margin-top: 4mm;
      }

      .corridor-line::before {
        content: "";
        position: absolute;
        left: 10%;
        right: 10%;
        top: 14mm;
        border-top: 1.4px solid rgba(110, 93, 56, 0.6);
      }

      .corridor-node {
        position: relative;
        text-align: center;
        background: var(--paper-soft);
        border: 1px solid rgba(150, 120, 69, 0.26);
        padding: 5mm 2mm 4mm;
        min-height: 30mm;
      }

      .corridor-node .n {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 21pt;
        line-height: 1;
        color: var(--wine);
      }

      .corridor-node .l {
        margin-top: 1.6mm;
        font-size: 8.6pt;
        line-height: 1.25;
        color: var(--muted);
      }

      .code-stack {
        display: grid;
        gap: 4mm;
      }

      .code-band {
        display: grid;
        grid-template-columns: 56mm 1fr;
        gap: 5mm;
        padding: 5mm;
        border: 1px solid var(--line);
        background: rgba(255,255,255,0.62);
      }

      .code-value {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 17pt;
        line-height: 1.1;
        color: var(--forest);
        padding-right: 4mm;
        border-right: 1px solid rgba(120, 95, 54, 0.18);
      }

      .code-meta p {
        margin: 1.3mm 0 0;
        font-size: 9.5pt;
        line-height: 1.45;
      }

      .ritual-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 4mm;
      }

      .ritual-line {
        color: var(--forest);
      }

      .talisman-page {
        display: grid;
        grid-template-columns: 1.05fr 0.95fr;
        gap: 7mm;
        align-items: start;
      }

      .talisman-figure {
        background:
          radial-gradient(circle at 50% 50%, rgba(214, 186, 121, 0.16), transparent 55%),
          rgba(255,255,255,0.35);
        border: 1px solid var(--line);
        padding: 4mm;
      }

      .talisman-svg {
        width: 100%;
        height: auto;
        display: block;
      }

      .talisman-center {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 40px;
        fill: #5b2f3f;
        letter-spacing: 0.02em;
      }

      .talisman-caption {
        font-family: "LuxeText", Georgia, serif;
        font-size: 12px;
        fill: #7b6236;
        letter-spacing: 0.06em;
        text-transform: uppercase;
      }

      .talisman-node {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 22px;
        fill: #28463f;
      }

      .radionics-grid,
      .protocol-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6mm;
      }

      .schema-card,
      .routine-card {
        background: rgba(255,255,255,0.62);
        border: 1px solid var(--line);
        padding: 5mm;
      }

      .schema-card ul,
      .routine-card ul {
        margin: 0;
        padding-left: 5mm;
        display: grid;
        gap: 2.2mm;
      }

      .schema-card li,
      .routine-card li {
        font-size: 9.7pt;
        line-height: 1.48;
      }

      .footer-note {
        margin-top: 5mm;
        padding-top: 4mm;
        border-top: 1px solid rgba(120, 95, 54, 0.18);
        font-size: 9.7pt;
        line-height: 1.55;
        color: var(--muted);
      }

      .source-list {
        display: grid;
        gap: 2.4mm;
        margin: 0;
        padding-left: 4.5mm;
      }

      .source-list li {
        font-size: 9.6pt;
        line-height: 1.48;
      }
    </style>
  </head>
  <body>
    <section class="page page-dark">
      <div class="top-ornament"></div>
      <div class="cover">
        <div class="cover-kicker">
          <span>Coran Num Tal</span>
          <span>Phase 2 luxe 2026</span>
        </div>
        <div class="cover-hero">
          <h1>Le Secret du Rizq</h1>
          <p class="subtitle">Phi, abjad, architecture du nombre, codes de recherche et pratiques operatives autour de la richesse, de la misericorde et de l'ouverture des causes.</p>
          <div class="arabic-line">بسم الله الرحمن الرحيم</div>
        </div>
        <div class="cover-grid">
          <div>${formulaChips(keyFormulae)}</div>
          <div class="manifesto">
            <h3>Cadre de lecture</h3>
            <p>Cette edition traite le dossier comme un laboratoire mystique et editorial. Les proportions sont assumees comme symboliques, les rectifications numeriques sont rendues explicites, et la pratique est reliee a une intention concrete.</p>
          </div>
        </div>
        <div class="cover-rosette-shell">
          ${coverRosette}
          <div class="cover-constellation">${coverConstellation}</div>
        </div>
        <div class="cover-footer">
          <div>Dhikr operatif, talisman contemplatif, montage radionique et protocole sur 21 jours.</div>
          <div>Version mystique, non academique, structuree comme un volume de travail.</div>
        </div>
      </div>
      <div class="bottom-ornament"></div>
      <div class="folio">01</div>
    </section>

    <section class="page">
      ${sectionTitle("Preambule", "Le fil conducteur du secret", "Richesse, misericorde, texte sacre et pratique sont traites ici comme les quatre faces d'un meme dispositif symbolique.")}
      <div class="text-columns">
        <div>
          <p class="lede">Dans cette reconstruction, la richesse n'est pas seulement monetaire. Elle est comprise comme flux de rizq, ouverture des causes, intensification de la baraka et descente d'une permission subtile. Le nombre d'or sert de passerelle entre des nombres coraniques, des valeurs abjad, des sequences Fibonacci et des codes de travail operatif.</p>
          <p class="lede">Le projet repose sur trois plans : le texte et ses nombres, les resonances gematriques, puis l'application pratique par le dhikr, le talisman et la radionique. L'objectif n'est pas la demonstration academique, mais la coherence d'un circuit interieur.</p>
        </div>
        <div class="side-note">
          <h3>Methode</h3>
          <ul class="bullet-list">
            <li>Lecture esoterique et experimentale.</li>
            <li>Les rectifications numeriques sont indiquees quand elles changent la structure.</li>
            <li>Le montage final doit servir la conscience, l'intention et la pratique.</li>
            <li>Aucune page n'est concue comme preuve scientifique ou religieuse definitive.</li>
          </ul>
        </div>
      </div>
      <div style="height: 6mm"></div>
      ${sectionTitle("Portes textuelles", "Versets de travail", "Le champ du rizq s'ouvre d'abord dans le texte, puis dans l'interpretation numerique.")} 
      <div class="note-panel success">
        <ul class="bullet-list">
          ${textualGates.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
        </ul>
      </div>
      <div class="folio">02</div>
    </section>

    <section class="page">
      ${sectionTitle("Matrice", "Nombres-souches et racines", "Le pivot numerique du dossier est recentre sur 618, non sur l'ancienne somme fautive.")} 
      <div class="numeric-panel">
        <div class="number-strip">${numericCoreMarkup}</div>
      </div>
      <div style="height: 5mm"></div>
      <div class="text-columns">
        <div class="root-panel">
          <h3>Index de travail</h3>
          ${rootTable()}
        </div>
        <div class="note-panel warning">
          <h3>Rectification centrale</h3>
          <p>Le couple <strong>Rahman + Rahim</strong> donne 618, non 684. Ce recentrage change l'axe du projet : la misericorde devient le coeur du flux avant la materialisation.</p>
          <div style="height: 4mm"></div>
          <p><strong>Fattah</strong> vaut 489 en abjad simple ; <strong>Ya Fattah</strong> monte a 500. Cette distinction est conservee pour eviter les confusions de l'ancienne version.</p>
        </div>
      </div>
      <div class="folio">03</div>
    </section>

    <section class="page">
      ${sectionTitle("Portes phi", "Six resonances majeures", "Les six portes sont reformulees comme cartes de lecture, avec formules visibles et interpretations editorialisees.")} 
      <div class="portals-grid">
        ${portalsMarkup}
      </div>
      <div class="folio">04</div>
    </section>

    <section class="page">
      ${sectionTitle("Corridor", "Le fil 34 -> 55 -> 89", "Saba, Rahman, Waqi'a et Fajr sont mis en scene comme un parcours, pas comme une juxtaposition de nombres.")} 
      <div class="corridor-layout">
        <div class="corridor-track">
          <div class="corridor-line">
            <div class="corridor-node"><div class="n">34</div><div class="l">Saba<br />prosperite et gratitude</div></div>
            <div class="corridor-node"><div class="n">55</div><div class="l">Rahman<br />faveur visible</div></div>
            <div class="corridor-node"><div class="n">56</div><div class="l">Waqi'a<br />bascule manifeste</div></div>
            <div class="corridor-node"><div class="n">89</div><div class="l">Fajr<br />lucidite du test</div></div>
          </div>
        </div>
        <div class="corridor-panel">
          <h3>Lecture du corridor</h3>
          <ul class="bullet-list">
            <li>34 / 21 = 1.6190, seuil de preparation.</li>
            <li>55 / 34 = 1.6176, phi montant.</li>
            <li>89 / 55 = 1.6182, phi montant.</li>
            <li>144 = 55 + 89, fermeture du corridor.</li>
          </ul>
        </div>
      </div>
      <div class="footer-note">Le corridor ne dit pas seulement comment attirer. Il dit aussi comment ne pas se perdre dans l'attraction. Sans gratitude, le flux se fissure. Sans lucidite, la richesse devient test.</div>
      <div class="folio">05</div>
    </section>

    <section class="page">
      ${sectionTitle("Codes", "Sequences Grabovoi reconstruites", "Chaque code est traite comme une adresse symbolique et non comme un substitut au dhikr.")} 
      <div class="code-stack">
        ${grabovoiMarkup}
      </div>
      <div class="footer-note">Conseil operatif : lire le code lentement, chiffre par chiffre, puis le laisser se compacter dans le coeur ou entre les sourcils. Le code accompagne la pratique, il ne la remplace pas.</div>
      <div class="folio">06</div>
    </section>

    <section class="page">
      ${sectionTitle("Dhikr", "Nombre et intention", "Les cycles sont remises en page comme des rituels lisibles, respirables, utilisables.")} 
      <div class="ritual-grid">
        ${dhikrMarkup}
      </div>
      <div class="note-panel success" style="margin-top: 5mm;">
        <h3>Sceau verbal conseille</h3>
        <p>Finir chaque session par : Bismillah, tawakkaltu 'ala Allah, wa ma bika min ni'matin fa-min Allah. L'objectif est de relier l'appel du flux a sa source pour eviter l'avidite brute.</p>
      </div>
      <div class="folio">07</div>
    </section>

    <section class="page">
      ${sectionTitle("Talisman", "Sceau contemplatif du rizq", "Cette page remplace le schema fruste initial par un grand signe centralise, construit pour la contemplation et la lisibilite.")} 
      <div class="talisman-page">
        <div class="talisman-figure">${talismanSvg()}</div>
        <div class="schema-card">
          <h3>Usage du talisman</h3>
          <ul>
            <li>Centre 618 : misericorde source du flux.</li>
            <li>Est 123 : materialisation du rizq.</li>
            <li>Sud 489 : ouverture des portes.</li>
            <li>Ouest 99 : completude du champ divin.</li>
            <li>Nord 55 : rappel de Rahman.</li>
            <li>Support de visualisation, de carnet, de meditation ou de fixation rituelle.</li>
          </ul>
        </div>
      </div>
      <div class="folio">08</div>
    </section>

    <section class="page">
      ${sectionTitle("Radionique", "Montage phi et discipline du champ", "La page est recomposee comme une fiche technique haut de gamme, avec schema de principes et activation.")} 
      <div class="radionics-grid">
        <div class="schema-card">
          <h3>Schema recommande</h3>
          <ul>
            ${radionics.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </div>
        <div class="schema-card">
          <h3>Activation</h3>
          <ul>
            <li>Jour 1 a 7 : un cycle Dhikr B devant le montage.</li>
            <li>Jour 8 a 14 : ajouter 786 489 618 en lecture lente trois fois.</li>
            <li>Jour 15 a 21 : travail avec le talisman huit minutes matin et soir.</li>
            <li>Toujours relier la demande a une action concrete dans la vie reelle.</li>
          </ul>
        </div>
      </div>
      <div class="footer-note">Le montage n'est pas un substitut a l'effort. Il sert a aligner intention, langage, nombre, matiere et repetition. La densite du champ depend de la coherence entre ces cinq niveaux.</div>
      <div class="folio">09</div>
    </section>

    <section class="page">
      ${sectionTitle("Protocole", "Routine de manifestation sur 21 jours", "Le secret est traite comme une boucle complete : nom, nombre, souffle, intention, geste et gratitude.")} 
      <div class="protocol-grid">
        ${routineMarkup}
      </div>
      <div class="note-panel success" style="margin-top: 6mm;">
        <h3>Cle du protocole</h3>
        <p>Le secret n'est pas le nombre seul. Le secret est la boucle complete : nom -> nombre -> souffle -> intention -> geste -> gratitude. Quand cette boucle se ferme, le code devient vivant.</p>
      </div>
      <div class="folio">10</div>
    </section>

    <section class="page">
      ${sectionTitle("Sources", "Rectifications et conclusion", "La refonte garde l'ame esoterique du dossier tout en durcissant la coherence de sa structure numerique.")} 
      <div class="text-columns">
        <div class="note-panel warning">
          <h3>Rectifications retenues</h3>
          <ul class="bullet-list">
            <li>Rahman + Rahim = 618, non 684.</li>
            <li>Fattah = 489 en abjad simple ; Ya Fattah = 500.</li>
            <li>Le pivot editorial est la misericorde comme source du flux avant la capture materielle.</li>
          </ul>
        </div>
        <div class="schema-card">
          <h3>Sources de base</h3>
          <ol class="source-list">
            ${sources.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ol>
        </div>
      </div>
      <div class="footer-note" style="margin-top: 8mm; font-size: 10.2pt;">
        Le secret du rizq, dans cette lecture, est que la misericorde precalcule le flux avant la matiere. Le code 618 place Rahman et Rahim au centre. Phi sert alors de passerelle entre le coeur, le nom, la proportion, la parole et l'effet.
      </div>
      <div class="footer-note" style="font-family: 'LuxeDisplay', 'Book Antiqua', serif; font-size: 12pt; color: var(--gold); text-align: center; border-top: none;">
        Wa-Allahu min wara'i al-qasd.
      </div>
      <div class="folio">11</div>
    </section>
  </body>
</html>`;
}

function findBrowserPath() {
  for (const candidate of chromeCandidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  return undefined;
}

async function renderPdf() {
  const playwrightModuleUrl = new URL(
    `file:///${path.join(bundledNodeModules, "playwright", "index.mjs").replaceAll("\\", "/")}`,
  );
  const { chromium } = await import(playwrightModuleUrl.href);

  ensureDir(htmlDir);
  ensureDir(pdfDir);
  ensureDir(previewDir);

  fs.writeFileSync(htmlPath, buildHtml(), "utf8");

  const browser = await chromium.launch({
    headless: true,
    executablePath: findBrowserPath(),
  });

  const page = await browser.newPage({
    viewport: { width: 1400, height: 1980 },
    deviceScaleFactor: 2,
  });

  await page.goto(`file:///${htmlPath.replaceAll("\\", "/")}`, {
    waitUntil: "networkidle",
  });
  await page.screenshot({ path: previewPath, fullPage: false });
  await page.pdf({
    path: pdfPath,
    printBackground: true,
    preferCSSPageSize: true,
  });
  await browser.close();

  return {
    htmlPath,
    pdfPath,
    previewPath,
  };
}

renderPdf()
  .then((result) => {
    console.log(JSON.stringify(result, null, 2));
  })
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
