// ==========================================================
// Maschinengeld — Professional Book Layout Template
// ==========================================================
// Thomas Huhn
// Typeset with Typst
// Format: 148mm × 210mm (A5 — standard German book format)
// ==========================================================

// --- Page Setup ---
#set page(
  paper: "a5",
  margin: (
    top: 22mm,
    bottom: 25mm,
    inside: 20mm,   // wider inside for binding
    outside: 16mm,
  ),
  header: context {
    let page-num = counter(page).get().first()
    if page-num <= 4 { return }  // no header on first pages
    
    let sel = query(heading.where(level: 2))
    let current-chapter = sel.filter(h => h.location().page() <= here().page()).last()
    
    if calc.odd(page-num) {
      // Recto (right page): chapter title
      align(right)[
        #text(font: "Source Sans 3", size: 8pt, fill: rgb("666666"), style: "italic")[
          #current-chapter.body
        ]
      ]
    } else {
      // Verso (left page): book title
      align(left)[
        #text(font: "Source Sans 3", size: 8pt, fill: rgb("666666"), style: "italic")[
          Maschinengeld
        ]
      ]
    }
    v(-2pt)
    line(length: 100%, stroke: 0.3pt + rgb("cccccc"))
  },
  footer: context {
    let page-num = counter(page).get().first()
    if page-num <= 2 { return }
    
    align(center)[
      #text(font: "Source Sans 3", size: 8.5pt, fill: rgb("444444"))[
        #counter(page).display()
      ]
    ]
  },
)

// --- Typography ---
#set text(
  font: "EB Garamond",
  size: 10.5pt,
  lang: "de",
  region: "DE",
  hyphenate: true,
  fill: rgb("1a1a1a"),
)

#set par(
  justify: true,
  leading: 0.72em,      // line spacing
  first-line-indent: 1em,
  spacing: 0.85em,      // paragraph spacing
)

// --- Headings ---
#show heading.where(level: 1): it => {
  // Teil headers — handled manually in content
  it
}

#show heading.where(level: 2): it => {
  // Chapter headings
  set text(font: "Source Sans 3", size: 18pt, weight: "bold", fill: rgb("1a1a2e"))
  v(20%)
  block(below: 1.5em)[
    #it.body
  ]
  v(0.5em)
  line(length: 40%, stroke: 1pt + rgb("1a1a2e"))
  v(1.5em)
}

#show heading.where(level: 3): it => {
  // Section headings
  set text(font: "Source Sans 3", size: 12pt, weight: "semibold", fill: rgb("2a2a3e"))
  v(1.5em)
  block(below: 0.8em)[#it.body]
}

#show heading.where(level: 4): it => {
  // Subsection headings
  set text(font: "Source Sans 3", size: 10.5pt, weight: "semibold", fill: rgb("333355"))
  v(1em)
  block(below: 0.6em)[#it.body]
}

// --- Figures ---
#show figure: it => {
  set text(size: 9pt)
  v(1em)
  align(center)[#it]
  v(1em)
}

#show figure.caption: it => {
  set text(font: "Source Sans 3", size: 8pt, fill: rgb("555555"), style: "italic")
  it
}

// --- Block quotes ---
#show quote: it => {
  set text(style: "italic", size: 10pt)
  pad(left: 1.5em, right: 1em)[
    #block(
      stroke: (left: 2pt + rgb("1a1a2e")),
      inset: (left: 0.8em, y: 0.3em),
    )[#it.body]
  ]
}

// --- Emphasis/Strong ---
#show emph: set text(style: "italic")
#show strong: set text(weight: "bold")

// ==========================================================
// TITLE PAGES
// ==========================================================

// --- Half title (Schmutztitel) ---
#set page(header: none, footer: none)
#v(35%)
#align(center)[
  #text(font: "Source Sans 3", size: 22pt, weight: "light", fill: rgb("1a1a2e"))[
    Maschinengeld
  ]
]
#pagebreak()

// --- Blank verso ---
#pagebreak()

// --- Full title page ---
#v(20%)
#align(center)[
  #text(font: "Source Sans 3", size: 28pt, weight: "bold", fill: rgb("1a1a2e"))[
    MASCHINENGELD
  ]
  #v(0.8em)
  #line(length: 30%, stroke: 1.5pt + rgb("1a1a2e"))
  #v(0.8em)
  #text(font: "EB Garamond", size: 13pt, style: "italic", fill: rgb("444444"))[
    Warum KI, Roboter und Krypto \
    eine Ökonomie ohne Menschen erschaffen
  ]
  #v(3em)
  #text(font: "Source Sans 3", size: 14pt, weight: "regular", fill: rgb("333333"))[
    Thomas Huhn
  ]
]
#v(1fr)
#align(center)[
  #text(font: "Source Sans 3", size: 9pt, fill: rgb("888888"))[
    März 2026
  ]
]
#pagebreak()

// --- Copyright / Impressum ---
#v(1fr)
#set text(size: 8pt, fill: rgb("666666"))
#set par(first-line-indent: 0em)
*Maschinengeld* \
Warum KI, Roboter und Krypto eine Ökonomie ohne Menschen erschaffen

© 2026 Thomas Huhn. Alle Rechte vorbehalten.

Erstausgabe März 2026

Die in diesem Buch dargestellten Informationen dienen ausschließlich der allgemeinen Bildung und stellen keine Anlageberatung dar. Der Autor übernimmt keine Haftung für Verluste, die aus der Anwendung der hier beschriebenen Strategien entstehen.

Dieses Buch enthält Verweise auf Unternehmen, Produkte und Technologien. Alle Marken und eingetragenen Warenzeichen sind Eigentum ihrer jeweiligen Inhaber.

Satz und Gestaltung: Typst \
Umschlag: Thomas Huhn

#set text(size: 10.5pt, fill: rgb("1a1a1a"))
#set par(first-line-indent: 1em)
#pagebreak()

// --- Dedication ---
#v(30%)
#align(center)[
  #text(font: "EB Garamond", size: 12pt, style: "italic", fill: rgb("444444"))[
    _Für Mila._
  ]
]
#pagebreak()
#pagebreak()

// ==========================================================
// TABLE OF CONTENTS
// ==========================================================
#v(8%)
#text(font: "Source Sans 3", size: 18pt, weight: "bold", fill: rgb("1a1a2e"))[
  Inhalt
]
#v(1em)
#line(length: 40%, stroke: 1pt + rgb("1a1a2e"))
#v(1.5em)

#show outline.entry.where(level: 2): it => {
  v(0.6em)
  text(font: "EB Garamond", size: 10pt)[#it]
}

#outline(
  title: none,
  indent: 1.5em,
  depth: 2,
)

#pagebreak(to: "odd")

// ==========================================================
// CONTENT
// ==========================================================
#set page(
  header: context {
    let page-num = counter(page).get().first()
    
    let sel = query(heading.where(level: 2))
    let past = sel.filter(h => h.location().page() <= here().page())
    if past.len() == 0 { return }
    let current-chapter = past.last()
    
    // Don't show header on chapter start pages
    if current-chapter.location().page() == here().page() { return }
    
    if calc.odd(page-num) {
      align(right)[
        #text(font: "Source Sans 3", size: 8pt, fill: rgb("666666"), style: "italic")[
          #current-chapter.body
        ]
      ]
    } else {
      align(left)[
        #text(font: "Source Sans 3", size: 8pt, fill: rgb("666666"), style: "italic")[
          Maschinengeld
        ]
      ]
    }
    v(-2pt)
    line(length: 100%, stroke: 0.3pt + rgb("cccccc"))
  },
)

#include "content.typ"

// ==========================================================
// COLOPHON (last page)
// ==========================================================
#pagebreak(to: "odd")
#v(1fr)
#align(center)[
  #text(font: "Source Sans 3", size: 8pt, fill: rgb("999999"))[
    Dieses Buch wurde mit Typst gesetzt. \
    Schriften: EB Garamond (Fließtext), Source Sans 3 (Überschriften). \
    \
    convergencethesis.com
  ]
]
