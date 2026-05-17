import { pathToFileURL } from "node:url";

const fontUrls = {
  display: pathToFileURL("C:/Windows/Fonts/BOOKOSB.TTF").href,
  displayItalic: pathToFileURL("C:/Windows/Fonts/BOOKOSBI.TTF").href,
  body: pathToFileURL("C:/Windows/Fonts/georgia.ttf").href,
  bodyBold: pathToFileURL("C:/Windows/Fonts/georgiab.ttf").href,
  bodyItalic: pathToFileURL("C:/Windows/Fonts/georgiai.ttf").href,
  accent: pathToFileURL("C:/Windows/Fonts/GOUDYSTO.TTF").href,
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

export function fontFaceCss() {
  return `
    @font-face {
      font-family: "LuxeDisplay";
      src: url("${fontUrls.display}") format("truetype");
      font-weight: 700;
      font-style: normal;
    }

    @font-face {
      font-family: "LuxeDisplay";
      src: url("${fontUrls.displayItalic}") format("truetype");
      font-weight: 700;
      font-style: italic;
    }

    @font-face {
      font-family: "LuxeText";
      src: url("${fontUrls.body}") format("truetype");
      font-weight: 400;
      font-style: normal;
    }

    @font-face {
      font-family: "LuxeText";
      src: url("${fontUrls.bodyBold}") format("truetype");
      font-weight: 700;
      font-style: normal;
    }

    @font-face {
      font-family: "LuxeText";
      src: url("${fontUrls.bodyItalic}") format("truetype");
      font-weight: 400;
      font-style: italic;
    }

    @font-face {
      font-family: "LuxeAccent";
      src: url("${fontUrls.accent}") format("truetype");
      font-weight: 400;
      font-style: normal;
    }
  `;
}

export function buildRosetteSvg({
  centerTop = "phi",
  centerBottom = "",
  labels = [],
  accent = "#d7b773",
  accentSoft = "#f6edd9",
  depth = "#284c64",
  dark = false,
} = {}) {
  const palette = {
    frame: accent,
    frameSoft: dark ? "rgba(247, 240, 223, 0.18)" : "rgba(38, 56, 71, 0.18)",
    fill: dark ? "rgba(255,255,255,0.04)" : "#fcf8ef",
    fillSoft: dark ? "rgba(255,255,255,0.02)" : "rgba(255,255,255,0.68)",
    text: dark ? "#f4e4bb" : "#1f2330",
    sub: dark ? "#dbc48c" : "#735b39",
    accentSoft,
    depth,
  };

  const ringLabels = labels.slice(0, 8);
  const nodes = ringLabels
    .map((label, index) => {
      const angle = (-90 + index * 45) * (Math.PI / 180);
      const x = 300 + Math.cos(angle) * 222;
      const y = 300 + Math.sin(angle) * 222;
      return `
        <g transform="translate(${x.toFixed(2)}, ${y.toFixed(2)})">
          <rect x="-34" y="-15" width="68" height="30" rx="8" fill="${palette.fill}" stroke="${palette.frame}" stroke-width="1.35" />
          <text text-anchor="middle" y="7" class="ring-node">${escapeHtml(label)}</text>
        </g>`;
    })
    .join("");

  return `
    <svg class="hero-rosette" viewBox="0 0 600 600" aria-hidden="true">
      <defs>
        <radialGradient id="rosetteGlow" cx="50%" cy="50%" r="70%">
          <stop offset="0%" stop-color="${palette.accentSoft}" stop-opacity="0.96" />
          <stop offset="100%" stop-color="${palette.accentSoft}" stop-opacity="0.12" />
        </radialGradient>
      </defs>
      <circle cx="300" cy="300" r="258" fill="none" stroke="${palette.frame}" stroke-width="1.5" />
      <circle cx="300" cy="300" r="232" fill="none" stroke="${palette.frameSoft}" stroke-width="1.2" />
      <circle cx="300" cy="300" r="190" fill="none" stroke="${palette.frame}" stroke-width="1.1" stroke-dasharray="4 7" />
      <circle cx="300" cy="300" r="136" fill="none" stroke="${palette.depth}" stroke-width="1.35" />
      <circle cx="300" cy="300" r="82" fill="url(#rosetteGlow)" stroke="${palette.frame}" stroke-width="2.4" />
      <polygon points="300,50 550,300 300,550 50,300" fill="none" stroke="${palette.frame}" stroke-width="2.1" />
      <polygon points="300,92 508,300 300,508 92,300" fill="none" stroke="${palette.depth}" stroke-width="1.7" />
      <g stroke="${palette.frame}" stroke-width="0.95" opacity="0.7">
        <line x1="300" y1="48" x2="300" y2="552" />
        <line x1="48" y1="300" x2="552" y2="300" />
        <line x1="112" y1="112" x2="488" y2="488" />
        <line x1="488" y1="112" x2="112" y2="488" />
      </g>
      <g stroke="${palette.frameSoft}" stroke-width="0.85">
        <line x1="171" y1="80" x2="429" y2="520" />
        <line x1="429" y1="80" x2="171" y2="520" />
      </g>
      <text x="300" y="276" text-anchor="middle" class="center-top">${escapeHtml(centerTop)}</text>
      ${centerBottom ? `<text x="300" y="320" text-anchor="middle" class="center-bottom">${escapeHtml(centerBottom)}</text>` : ""}
      ${nodes}
      <style>
        .hero-rosette .center-top {
          font-family: "LuxeDisplay", "Book Antiqua", serif;
          font-size: 68px;
          fill: ${palette.text};
        }
        .hero-rosette .center-bottom {
          font-family: "LuxeAccent", "Book Antiqua", serif;
          font-size: 22px;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          fill: ${palette.sub};
        }
        .hero-rosette .ring-node {
          font-family: "LuxeDisplay", "Book Antiqua", serif;
          font-size: 28px;
          fill: ${palette.depth};
        }
      </style>
    </svg>
  `;
}

export function buildConstellationStripSvg({
  items = [],
  accent = "#d7b773",
  depth = "#2a4f68",
  dark = false,
} = {}) {
  const count = Math.max(items.length, 2);
  const innerWidth = 960;
  const startX = 72;
  const spacing = (innerWidth - startX * 2) / (count - 1);
  const nodes = items
    .map((item, index) => {
      const x = startX + index * spacing;
      const y = 100 + (index % 2 === 0 ? 0 : 30);
      return { label: item, x, y };
    });

  const lines = nodes
    .slice(0, -1)
    .map(
      (node, index) =>
        `<line x1="${node.x}" y1="${node.y}" x2="${nodes[index + 1].x}" y2="${nodes[index + 1].y}" stroke="${accent}" stroke-width="2" opacity="0.6" />`,
    )
    .join("");

  const labels = nodes
    .map(
      (node) => `
        <g transform="translate(${node.x}, ${node.y})">
          <circle r="11" fill="${dark ? "rgba(255,255,255,0.05)" : "#fff8ec"}" stroke="${accent}" stroke-width="2" />
          <text text-anchor="middle" y="-22" class="strip-label">${escapeHtml(node.label)}</text>
          <circle r="4" fill="${depth}" />
        </g>`,
    )
    .join("");

  return `
    <svg class="constellation-strip" viewBox="0 0 960 180" aria-hidden="true">
      <rect width="960" height="180" rx="28" fill="${dark ? "rgba(255,255,255,0.03)" : "rgba(255,255,255,0.62)"}" stroke="${accent}" stroke-width="1.1" opacity="0.9" />
      ${lines}
      ${labels}
      <style>
        .constellation-strip .strip-label {
          font-family: "LuxeText", Georgia, serif;
          font-size: 26px;
          fill: ${dark ? "#f1dfb6" : "#38566b"};
          letter-spacing: 0.04em;
        }
      </style>
    </svg>
  `;
}
