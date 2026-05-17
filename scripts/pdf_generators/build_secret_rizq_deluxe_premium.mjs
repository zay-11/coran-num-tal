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

const htmlPath = path.join(htmlDir, "Secret_Rizq_Phi_Deluxe_Premium.html");
const pdfPath = path.join(pdfDir, "Secret_Rizq_Phi_Deluxe.pdf");
const previewPath = path.join(previewDir, "Secret_Rizq_Phi_Deluxe_Premium_page1.png");
const previewPortalPath = path.join(previewDir, "Secret_Rizq_Phi_Deluxe_Premium_page4.png");

const chromeCandidates = [
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  "C:/Program Files/Microsoft/Edge/Application/msedge.exe",
];

const passages = [
  {
    key: "Source",
    ref: "51:58",
    arabic: "إِنَّ اللَّهَ هُوَ الرَّزّاقُ ذُو القُوَّةِ المَتينُ",
    excerpt: "Ar-Razzaq comme source pure, anterieure au manque et a la demande.",
    code: ["319", "58", "123", "786"],
    doctrine: [
      "Le verset sert de noyau-source : la provision existe avant l'appel.",
      "Le centre 58 devient un nombre d'activation plus qu'une simple reference.",
      "Cette porte est ideale avant une action concrete ou une prise de risque.",
    ],
  },
  {
    key: "Issue",
    ref: "65:2-3",
    arabic: "وَمَن يَتَّقِ اللَّهَ يَجعَل لَهُ مَخرَجًا • وَيَرزُقهُ مِن حَيثُ لا يَحتَسِبُ",
    excerpt: "La porte d'issue travaille le deblocage, le passage et la venue d'une cause non calculee.",
    code: ["652", "653", "618", "99"],
    doctrine: [
      "La taqwa et le tawakkul y sont lus comme moteurs de deplacement du champ.",
      "C'est la charniere entre appel et manifestation.",
      "Elle gagne a etre couplee a une demande precise et a un geste concret immediat.",
    ],
  },
  {
    key: "Pluie",
    ref: "71:10-12",
    arabic: "فَقُلتُ استَغفِروا رَبَّكُم ... يُمدِدكُم بِأَموٰلٍ وَبَنينَ",
    excerpt: "Istighfar, pluie, biens, jardins et rivieres : la descente du flux prend ici une forme tres imaginale.",
    code: ["7110", "7112", "55", "89"],
    doctrine: [
      "Cette porte sert a faire descendre, pas seulement a ouvrir.",
      "Elle travaille mieux sur 7 ou 21 jours.",
      "Le verset donne une atmosphere de pluie, de renforcement et de croissance familiale.",
    ],
  },
];

const couloir = [
  ["34", "Saba", "prosperite, oubli, rupture de gratitude"],
  ["55", "Rahman", "deversement de faveur et corridor Fibonacci"],
  ["56", "Waqi'a", "bascule vers le plan manifeste"],
  ["89", "Fajr", "reveil, revelation du test et tri de l'abondance"],
];

const protocols = [
  {
    phase: "Matin",
    steps: [
      "Lecture contemplative de 51:58 ou simple regard sur le sceau-source.",
      "19x Ya Razzaq puis 19x Ya Fattah.",
      "Une phrase d'intention tres concrete, sans surcharge verbale.",
    ],
  },
  {
    phase: "Milieu de journee",
    steps: [
      "Rappel de 65:2-3 avant un appel, une vente, une creation ou une demande.",
      "Une action tangible dans le monde : service, proposition, prise de contact, ajustement.",
      "Mini lecture du code 319 489 618 786.",
    ],
  },
  {
    phase: "Soir",
    steps: [
      "Lecture ou ecoute de la sourate 56.",
      "Dhikr 61 puis 8 repetitions de Ya Rahim.",
      "Journal bref : blocage, signe, ouverture, reponse observee.",
    ],
  },
];

const domainCards = [
  ["Richesse", "56 / 51:58 / 65:2-3", "flux, issue, stabilisation materielle"],
  ["Sante", "17:82", "lecture curative et recentrage du champ vital"],
  ["Savoir", "20:114", "expansion de comprehension et assimilation"],
  ["Protection", "113 / 114", "barriere, couverture et fermeture du champ"],
];

const talismanNodes = [
  { value: "56", x: 300, y: 74 },
  { value: "58", x: 474, y: 138 },
  { value: "123", x: 530, y: 300 },
  { value: "618", x: 474, y: 462 },
  { value: "786", x: 300, y: 526 },
  { value: "99", x: 126, y: 462 },
  { value: "319", x: 70, y: 300 },
  { value: "489", x: 126, y: 138 },
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

function talismanSvg() {
  return `
    <svg class="talisman-svg" viewBox="0 0 600 600" aria-hidden="true">
      <defs>
        <radialGradient id="deluxeGlow" cx="50%" cy="50%" r="70%">
          <stop offset="0%" stop-color="#fbf1dc" stop-opacity="0.96" />
          <stop offset="100%" stop-color="#fbf1dc" stop-opacity="0.18" />
        </radialGradient>
      </defs>
      <circle cx="300" cy="300" r="236" fill="none" stroke="#ab8a49" stroke-width="1.6" />
      <circle cx="300" cy="300" r="194" fill="none" stroke="#cfb06d" stroke-width="1.2" stroke-dasharray="5 7" />
      <circle cx="300" cy="300" r="138" fill="none" stroke="#35544b" stroke-width="1.3" />
      <circle cx="300" cy="300" r="82" fill="url(#deluxeGlow)" stroke="#d6b875" stroke-width="2.3" />
      <polygon points="300,44 556,300 300,556 44,300" fill="none" stroke="#d6b875" stroke-width="2.1" />
      <polygon points="300,88 512,300 300,512 88,300" fill="none" stroke="#35544b" stroke-width="1.7" />
      <g stroke="#8b7040" stroke-width="1.1">
        <line x1="300" y1="48" x2="300" y2="552" />
        <line x1="48" y1="300" x2="552" y2="300" />
        <line x1="111" y1="111" x2="489" y2="489" />
        <line x1="489" y1="111" x2="111" y2="489" />
      </g>
      <text x="300" y="282" text-anchor="middle" class="deluxe-center">56</text>
      <text x="300" y="318" text-anchor="middle" class="deluxe-caption">sourate-maitre du rizq</text>
      ${talismanNodes
        .map(
          (item) => `
            <g transform="translate(${item.x}, ${item.y})">
              <rect x="-34" y="-16" width="68" height="32" rx="8" fill="#fbf6ea" stroke="#b28e49" stroke-width="1.4" />
              <text text-anchor="middle" y="7" class="deluxe-node">${escapeHtml(item.value)}</text>
            </g>`,
        )
        .join("")}
    </svg>
  `;
}

function buildHtml() {
  const luxeFonts = fontFaceCss();
  const coverRosette = buildRosetteSvg({
    centerTop: "56",
    centerBottom: "618 / 786",
    labels: ["51:58", "65", "71", "34", "55", "89", "319", "489"],
    dark: true,
    depth: "#35544b",
  });
  const coverConstellation = buildConstellationStripSvg({
    items: ["51:58", "65:2-3", "71:10-12", "34", "55", "56", "89"],
    dark: true,
    depth: "#35544b",
  });
  const portalMarkup = passages
    .map(
      (passage) => `
        <article class="portal-card">
          <div class="portal-meta">
            <span>${escapeHtml(passage.key)}</span>
            <span>${escapeHtml(passage.ref)}</span>
          </div>
          <h3>${escapeHtml(passage.excerpt)}</h3>
          <p class="arabic-line">${escapeHtml(passage.arabic)}</p>
          <div class="code-row">
            ${passage.code.map((value) => `<span>${escapeHtml(value)}</span>`).join("")}
          </div>
          <ul>
            ${passage.doctrine.map((item) => `<li>${escapeHtml(item)}</li>`).join("")}
          </ul>
        </article>`,
    )
    .join("");

  const couloirMarkup = couloir
    .map(
      ([value, title, meaning]) => `
        <article class="corridor-step">
          <div class="corridor-value">${escapeHtml(value)}</div>
          <h3>${escapeHtml(title)}</h3>
          <p>${escapeHtml(meaning)}</p>
        </article>`,
    )
    .join("");

  const protocolMarkup = protocols
    .map(
      (block) => `
        <article class="protocol-card">
          <h3>${escapeHtml(block.phase)}</h3>
          <ul>
            ${block.steps.map((step) => `<li>${escapeHtml(step)}</li>`).join("")}
          </ul>
        </article>`,
    )
    .join("");

  const domainsMarkup = domainCards
    .map(
      ([label, refs, meaning]) => `
        <article class="domain-card">
          <h3>${escapeHtml(label)}</h3>
          <div class="domain-ref">${escapeHtml(refs)}</div>
          <p>${escapeHtml(meaning)}</p>
        </article>`,
    )
    .join("");

  return `<!doctype html>
<html lang="fr">
  <head>
    <meta charset="utf-8" />
    <title>Le Secret du Rizq Deluxe</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <style>
      ${luxeFonts}
      :root {
        --paper: #f4eedf;
        --paper-soft: #fbf8f2;
        --ink: #1d1a16;
        --muted: #62594d;
        --line: rgba(95, 83, 61, 0.16);
        --gold: #ae8a49;
        --gold-bright: #d8bb7b;
        --forest: #35544b;
        --forest-soft: #dfe8e2;
        --blue: #224157;
        --blue-soft: #dbe6ee;
        --wine: #693442;
        --wine-soft: #f0e0e4;
        --night: #151310;
        --night-2: #1f1b16;
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
        background: #d6d0c4;
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
          radial-gradient(circle at top right, rgba(215, 186, 121, 0.24), transparent 32%),
          radial-gradient(circle at bottom left, rgba(53, 84, 75, 0.12), transparent 36%),
          var(--paper);
      }

      .page::before {
        content: "";
        position: absolute;
        inset: 8mm;
        border: 1px solid rgba(112, 93, 60, 0.24);
      }

      .page::after {
        content: "";
        position: absolute;
        inset: 11mm;
        border: 1px solid rgba(112, 93, 60, 0.08);
      }

      .page-dark {
        background:
          radial-gradient(circle at 18% 14%, rgba(215, 186, 121, 0.17), transparent 22%),
          radial-gradient(circle at 82% 22%, rgba(75, 116, 104, 0.16), transparent 24%),
          linear-gradient(180deg, var(--night-2), var(--night));
        color: #f7efde;
      }

      .page-dark::before {
        border-color: rgba(216, 188, 126, 0.3);
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
          linear-gradient(90deg, transparent, rgba(216, 188, 126, 0.74) 18%, rgba(216, 188, 126, 0.96) 50%, rgba(216, 188, 126, 0.74) 82%, transparent);
      }

      .ornament.top { top: 12mm; }
      .ornament.bottom { bottom: 11mm; }

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
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: rgba(244, 236, 220, 0.68);
      }

      .cover h1 {
        margin: 0;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 31pt;
        line-height: 0.93;
        color: #f3e3bb;
        text-transform: uppercase;
      }

      .cover .subtitle {
        max-width: 144mm;
        margin: 4mm 0 0;
        font-size: 13.8pt;
        line-height: 1.3;
        color: rgba(247, 240, 223, 0.9);
      }

      .arabic {
        font-size: 20pt;
        color: #ecd299;
        letter-spacing: 0.03em;
      }

      .cover-grid {
        display: grid;
        grid-template-columns: 1.02fr 0.98fr;
        gap: 9mm;
      }

      .cover-showcase {
        display: grid;
        grid-template-columns: 0.94fr 1.06fr;
        gap: 8mm;
        align-items: stretch;
      }

      .cover-figure {
        position: relative;
        min-height: 98mm;
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

      .panel,
      .box,
      .portal-card,
      .protocol-card,
      .domain-card {
        position: relative;
        border: 1px solid rgba(177, 141, 74, 0.3);
        background: rgba(255, 249, 236, 0.8);
        padding: 5.5mm;
      }

      .panel::before,
      .box::before,
      .portal-card::before,
      .protocol-card::before,
      .domain-card::before {
        content: "";
        position: absolute;
        inset: 3mm;
        border: 1px solid rgba(177, 141, 74, 0.14);
      }

      .page-dark .panel {
        background: rgba(255,255,255,0.04);
        border-color: rgba(216, 188, 126, 0.28);
      }

      .page-dark .panel::before {
        border-color: rgba(216, 188, 126, 0.1);
      }

      .panel h3,
      .box h3,
      .portal-card h3,
      .protocol-card h3,
      .domain-card h3 {
        margin: 0 0 2.5mm;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 12pt;
        line-height: 1.15;
      }

      .panel p,
      .box p,
      .portal-card p,
      .protocol-card p,
      .domain-card p {
        margin: 0;
        font-size: 10pt;
        line-height: 1.55;
      }

      .panel ul,
      .box ul,
      .portal-card ul,
      .protocol-card ul {
        margin: 3mm 0 0;
        padding-left: 18px;
        font-size: 9.5pt;
        line-height: 1.55;
      }

      .cover-list {
        margin: 0;
        padding-left: 18px;
        font-size: 10pt;
        line-height: 1.58;
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
      }

      .deck {
        margin: 2.5mm 0 0;
        max-width: 148mm;
        font-size: 10.5pt;
        line-height: 1.45;
        color: var(--muted);
      }

      .formula-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 3mm;
      }

      .formula-chip {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 15mm;
        padding: 0 4mm;
        background: rgba(255, 250, 240, 0.84);
        border: 1px solid rgba(177, 141, 74, 0.24);
        font-size: 10pt;
        color: var(--blue);
      }

      .split {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8mm;
      }

      .portal-grid {
        display: grid;
        gap: 5mm;
      }

      .portal-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 4mm;
        margin-bottom: 2.5mm;
        font-size: 8.5pt;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: var(--gold);
      }

      .arabic-line {
        margin-top: 2.5mm;
        font-size: 12pt;
        line-height: 1.7;
        color: var(--forest);
      }

      .code-row {
        display: flex;
        flex-wrap: wrap;
        gap: 2.2mm;
        margin-top: 3mm;
      }

      .code-row span {
        display: inline-flex;
        align-items: center;
        min-height: 9mm;
        padding: 0 3.6mm;
        border-radius: 999px;
        background: var(--blue-soft);
        color: var(--blue);
        font-size: 8.8pt;
      }

      .corridor-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 4mm;
      }

      .corridor-step {
        padding: 5mm;
        background: rgba(255, 249, 236, 0.82);
        border: 1px solid rgba(177, 141, 74, 0.24);
      }

      .corridor-value {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 18pt;
        color: var(--gold);
      }

      .corridor-step h3 {
        margin: 2mm 0 1.5mm;
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 12pt;
      }

      .corridor-step p {
        margin: 0;
        font-size: 9.5pt;
        line-height: 1.5;
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

      .deluxe-center {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 68px;
        fill: #1d1a16;
      }

      .deluxe-caption {
        font-size: 16px;
        fill: #7b6541;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }

      .deluxe-node {
        font-family: "LuxeDisplay", "Book Antiqua", serif;
        font-size: 27px;
        fill: #224157;
      }

      .protocol-grid,
      .domain-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 5mm;
      }

      .domain-grid {
        grid-template-columns: repeat(4, 1fr);
      }

      .domain-ref {
        margin-bottom: 2mm;
        font-size: 8.8pt;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--gold);
      }

      .footer-note {
        position: absolute;
        left: 16mm;
        right: 16mm;
        bottom: 16mm;
        display: flex;
        justify-content: space-between;
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
          <h1>Le Secret du Rizq<br />Deluxe</h1>
          <p class="subtitle">Phi, abjad, couloir Fibonacci, talisman, protocole et architecture de manifestation dans une version plus luxueuse et plus operatoire.</p>
        </div>
        <div class="arabic">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</div>
        <div class="cover-showcase">
          <div>
            <div class="panel">
              <h3>These du Deluxe</h3>
              <ul class="cover-list">
                <li>51:58 pose la Source pure du rizq.</li>
                <li>65:2-3 ouvre l'issue et le passage inattendu.</li>
                <li>71:10-12 fait descendre la pluie, les biens et la croissance.</li>
                <li>34 -> 55 -> 56 -> 89 organise la descente du flux vers le manifeste.</li>
              </ul>
            </div>
            <div class="panel" style="margin-top: 5mm;">
              <h3>Rectification fondatrice</h3>
              <p>Le coeur mercy-code de la collection est fixe a <strong>618</strong>. Cette edition assume pleinement ce centre pour donner au document une charpente plus stable, plus propre et plus forte visuellement.</p>
            </div>
          </div>
          <div class="cover-figure">
            ${coverRosette}
            <div class="cover-strip">${coverConstellation}</div>
          </div>
        </div>
        <div class="footer-note">
          <span>Edition luxe refondue</span>
          <span>Rizq deluxe</span>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Doctrine", "Architecture generale du secret", "La version Deluxe ne collectionne pas seulement des nombres : elle aligne source, issue, pluie, couloir et fixation.")}
      <div class="formula-row">
        <div class="formula-chip">Source : 51:58</div>
        <div class="formula-chip">Issue : 65:2-3</div>
        <div class="formula-chip">Pluie : 71:10-12</div>
        <div class="formula-chip">34 -> 55 -> 56 -> 89</div>
      </div>
      <div class="split" style="margin-top: 7mm;">
        <div class="box">
          <h3>Equation du systeme</h3>
          <p>La Source dit que la provision vient d'Allah. L'issue montre que la taqwa et le tawakkul deplacent les causes. La pluie fait descendre le flux. Le couloir organise ensuite la mise en forme de cette descente. Le Deluxe est la synthese de ces etages.</p>
        </div>
        <div class="box">
          <h3>Axiome pratique</h3>
          <p>Le nombre ne manifeste rien seul. Il structure l'attention, le souffle, la repetition et la memoire. La manifestation a besoin d'un geste reel dans le monde, sinon la formule reste purement contemplative.</p>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Portes", "Les trois passages textuels du rizq", "Chaque porte est relue comme un module : un verset, une fonction, quelques seuils et un usage.")}
      <div class="portal-grid">
        ${portalMarkup}
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Couloir", "34 -> 55 -> 56 -> 89", "Le Deluxe transforme la suite en narration : prosperite, faveur, bascule et revelation du test.")}
      <div class="corridor-grid">
        ${couloirMarkup}
      </div>
      <div class="split" style="margin-top: 7mm;">
        <div class="box">
          <h3>Lecture dynamique</h3>
          <p>Le couloir est une pedagogie. Il rappelle que la richesse n'est pas l'aboutissement final, mais une mise a l'epreuve de la conscience. La faveur ouvre, la manifestation expose, puis l'aube revele la qualite interieure.</p>
        </div>
        <div class="box">
          <h3>Position de la sourate 56</h3>
          <p>La sourate Al-Waqi'a sert ici de charniere. Elle fait basculer le couloir numerique dans un champ rituel et talismanique plus concret, d'ou son importance centrale dans la version Deluxe.</p>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Sceau", "Talisman Deluxe de la sourate-maitre", "Le talisman condense les seuils de la collection autour de la porte 56 et du centre 618.")}
      <div class="talisman-layout">
        <div>${talismanSvg()}</div>
        <div class="box">
          <h3>Activation du sceau</h3>
          <ul>
            <li>Centre : 56, comme porte maitresse de manifestation.</li>
            <li>Anneau : 58, 123, 618, 786, 99, 319, 489.</li>
            <li>Lecture recommandee : 51:58 puis 65:2-3 avant activation.</li>
            <li>Scellement : 61 invocations, puis 8 repetitions de Ya Rahim.</li>
            <li>Utilisation : carnet, autel, portefeuille, plateau radionique ou mur de travail.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Cycle", "Protocole Deluxe sur 21 jours", "La version premium clarifie le rythme quotidien pour rendre le document reellement utilisable.")}
      <div class="protocol-grid">
        ${protocolMarkup}
      </div>
      <div class="box" style="margin-top: 7mm;">
        <h3>Regle de fermeture</h3>
        <p>On n'attend pas une sensation parfaite avant d'agir. La pratique, le code et l'action doivent rester solidaires. Le protocole Deluxe n'est valide que s'il produit aussi des decisions, des demandes et des gestes observables.</p>
      </div>
    </section>

    <section class="page">
      ${sectionTitle("Extensions", "Le moteur au-dela de la richesse", "La logique numerique peut etre relue sur d'autres domaines sans casser la coherence du systeme.")}
      <div class="domain-grid">
        ${domainsMarkup}
      </div>
      <div class="split" style="margin-top: 7mm;">
        <div class="box">
          <h3>Principe commun</h3>
          <p>Reference, nombre, projection phi, anneau, repetition, action. Quelle que soit la porte, le Deluxe applique cette meme chaine pour transformer un verset en protocole operatif.</p>
        </div>
        <div class="box">
          <h3>Ce que cette edition corrige</h3>
          <p>Hierarchie typographique, densite, alignements, respiration, lisibilite des modules, place du talisman et des portes, ainsi qu'une coherente visuelle digne d'une vraie edition premium.</p>
        </div>
      </div>
    </section>

    <section class="page page-dark">
      <div class="ornament top"></div>
      <div class="ornament bottom"></div>
      ${sectionTitle("Final", "La serrure, la cle, la preuve", "Le nombre sert de serrure, la pratique de cle, et l'action de preuve. C'est le noyau du Deluxe.")}
      <div class="cover-grid" style="margin-top: 8mm;">
        <div class="panel">
          <h3>Triptyque final</h3>
          <ul class="cover-list">
            <li>Source : ce qui existe deja avant le manque</li>
            <li>Issue : ce qui deplace les causes</li>
            <li>Pluie : ce qui fait descendre et fixer</li>
          </ul>
        </div>
        <div class="panel">
          <h3>Formule de synthese</h3>
          <p>319 -> 489 -> 618 -> 786</p>
          <p>51:58 -> 65:2-3 -> 71:10-12</p>
          <p>34 -> 55 -> 56 -> 89</p>
        </div>
      </div>
      <div class="panel" style="margin-top: 10mm;">
        <h3 style="color: #f0dfb5;">Wa-Allahu min wara'i al-qasd</h3>
        <p style="color: rgba(246, 237, 220, 0.86);">Le luxe de cette edition n'est pas decoratif. Il sert a rendre enfin claire, praticable et digne la logique interne du PDF original.</p>
      </div>
      <div class="footer-note">
        <span>Secret du rizq deluxe</span>
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
    await page.evaluate(() => window.scrollTo(0, window.innerHeight * 3.5));
    await page.screenshot({ path: previewPortalPath, fullPage: false });
  } finally {
    await browser.close();
  }
}

await renderPdf();
console.log(`HTML generated: ${htmlPath}`);
console.log(`PDF generated: ${pdfPath}`);
