// The AI Species — Professional Book Template (v3)
// A5 format, EB Garamond body + Source Sans 3 headings
// Gold accent: #C8A84E, Navy: #0A0A2E

#let gold = rgb("#C8A84E")
#let navy = rgb("#0A0A2E")
#let gold-light = rgb("#F8F3E6")
#let blue-light = rgb("#EBF0F7")
#let blue-accent = rgb("#2E5090")
#let gray-light = rgb("#F5F5F5")
#let gray-rule = rgb("#CCCCCC")
#let dark-text = rgb("#1A1A1A")

// === Custom elements ===

// Pull quote — large italic with gold rules
#let pull-quote(body) = {
  v(1em)
  block(width: 100%, inset: (x: 2em, y: 0.6em))[
    #line(length: 40%, stroke: 1.5pt + gold)
    #v(0.5em)
    #set text(size: 11pt, style: "italic", fill: rgb("#333"))
    #set par(first-line-indent: 0pt, leading: 0.75em)
    #body
    #v(0.5em)
    #align(right)[#line(length: 40%, stroke: 1.5pt + gold)]
  ]
  v(1em)
}

// Callout box — gold accent for key insights
#let callout-box(body) = {
  v(0.6em)
  block(
    width: 100%,
    inset: (left: 14pt, right: 12pt, top: 12pt, bottom: 12pt),
    stroke: (left: 3pt + gold, top: 0.5pt + rgb("#E0D5B0"), bottom: 0.5pt + rgb("#E0D5B0"), right: 0.5pt + rgb("#E0D5B0")),
    fill: gold-light,
    radius: (right: 3pt),
  )[
    #set text(size: 9.5pt)
    #set par(first-line-indent: 0pt)
    #body
  ]
  v(0.6em)
}

// Info box — blue accent for definitions/facts
#let info-box(body) = {
  v(0.6em)
  block(
    width: 100%,
    inset: (left: 14pt, right: 12pt, top: 12pt, bottom: 12pt),
    stroke: (left: 3pt + blue-accent, top: 0.5pt + rgb("#B0C4DE"), bottom: 0.5pt + rgb("#B0C4DE"), right: 0.5pt + rgb("#B0C4DE")),
    fill: blue-light,
    radius: (right: 3pt),
  )[
    #set text(size: 9.5pt)
    #set par(first-line-indent: 0pt)
    #body
  ]
  v(0.6em)
}

// Glossary entry
#let glossary-entry(term, definition) = {
  v(0.3em)
  block(width: 100%, breakable: false)[
    #text(weight: "bold", font: "Source Sans 3", size: 10pt)[#term]
    #h(6pt)
    #text(size: 9.5pt)[#definition]
  ]
  v(0.15em)
}

// TEIL (Part) page — dramatic full-page design
#let teil-page(title, short-title: [THE AI SPECIES]) = {
  state("running-matter", false).update(false)
  pagebreak(to: "odd")
  page(header: none, footer: none)[
    #v(1fr)
    #align(center)[
      #line(length: 30%, stroke: 2pt + gold)
      #v(20pt)
      #text(size: 11pt, tracking: 4pt, fill: gold, font: "Source Sans 3", weight: "medium")[#short-title]
      #v(14pt)
      #text(size: 18pt, weight: "bold", tracking: 2pt, font: "Source Sans 3")[#upper(title)]
      #v(20pt)
      #line(length: 30%, stroke: 2pt + gold)
    ]
    #v(2fr)
  ]
}

// Drop cap for chapter openers
#let drop-cap(letter, rest) = {
  set par(first-line-indent: 0pt)
  grid(
    columns: (auto, 1fr),
    column-gutter: 6pt,
    align(top)[
      #text(size: 40pt, weight: "bold", fill: gold, font: "EB Garamond")[#letter]
    ],
    rest,
  )
}


// Book template
#let book(body, short-title: [THE AI SPECIES], author: [Thomas Huhn]) = {
  // === Page Setup ===
  set page(
    paper: "a5",
    margin: (
      top: 2.35cm,
      bottom: 2.55cm,
      inside: 2.45cm,
      outside: 1.75cm,
    ),
    footer: context {
      let page-num = counter(page).get().first()
      let running = state("running-matter", false).get()
      if not running { return }
      align(center, text(size: 8.3pt, font: "Source Sans 3", fill: rgb("#777"))[#page-num])
    },
    header: context {
      let running = state("running-matter", false).get()
      if not running { return }

      let page-num = counter(page).get().first()
      let headings = query(heading.where(level: 1))
      let current = headings.filter(h => h.location().page() <= here().page())
      if current.len() == 0 { return }
      let current-heading = current.last()

      // Don't show header on chapter start page
      if current-heading.location().page() == here().page() { return }

      let title = current-heading.body
      if calc.odd(page-num) {
        // Recto: chapter title
        align(right, text(size: 7.4pt, tracking: 0.3pt, font: "Source Sans 3", fill: rgb("#777"))[#title])
      } else {
        // Verso: author
        align(left, text(size: 7.4pt, tracking: 0.6pt, font: "Source Sans 3", fill: rgb("#777"))[#author])
      }
      v(-2pt)
      line(length: 100%, stroke: 0.45pt + rgb("#D2D2D2"))
    },
  )

  // === Typography ===
  set text(
    font: "EB Garamond",
    size: 10.15pt,
    lang: "de",
    hyphenate: true,
    fill: dark-text,
  )

  set par(
    justify: true,
    leading: 0.78em,
    first-line-indent: 1.1em,
    spacing: 0.92em,
  )

  // === Heading protection: no orphaned headings ===
  // Headings keep with at least 3 lines of following content
  show heading: set block(breakable: false, below: 1.2em)

  // === Headings ===
  // Chapter headings (level 1) — very prominent
  show heading.where(level: 1): it => {
    set text(font: "Source Sans 3", size: 18.3pt, weight: "bold", fill: navy)
    set par(first-line-indent: 0pt)
    set text(hyphenate: false)
    v(2.2cm)
    block(breakable: false)[
      #it.body
      #v(7pt)
      #line(length: 66pt, stroke: 2.6pt + gold)
    ]
    v(0.9cm)
  }

  // Sub-headings (level 2) — quieter and more bookish
  show heading.where(level: 2): it => {
    set text(font: "Source Sans 3", size: 11.8pt, weight: "medium", fill: rgb("#444"))
    set par(first-line-indent: 0pt)
    v(0.72cm)
    block(breakable: false)[
      #it
      #v(2pt)
      #line(length: 22pt, stroke: 0.9pt + gold)
    ]
    v(0.34cm)
  }

  // Sub-sub-headings (level 3) — subtle but clear
  show heading.where(level: 3): it => {
    set text(font: "Source Sans 3", size: 11pt, weight: "semibold", fill: rgb("#333"))
    set par(first-line-indent: 0pt)
    v(0.8cm)
    it
    v(0.3cm)
  }

  // === Figures ===
  set figure(
    gap: 0.8em,
  )
  show figure: it => {
    v(0.55em)
    block(
      width: 100%,
      inset: (top: 8pt, bottom: 10pt),
      breakable: false,
    )[
      #align(center, it.body)
      #v(7pt)
      #if it.caption != none {
        align(center)[
          #set text(size: 8.25pt, fill: rgb("#555"), hyphenate: false)
          #set par(first-line-indent: 0pt)
          #text(weight: "semibold", font: "Source Sans 3")[#it.caption.body]
        ]
      }
    ]
    v(0.6em)
  }

  // === Lists ===
  set list(
    indent: 1em,
    marker: text(fill: gold, size: 10pt)[•],
    spacing: 0.6em,
  )

  set enum(
    indent: 1em,
    spacing: 0.6em,
  )

  // === Tables ===
  set table(
    stroke: 0.5pt + rgb("#CCC"),
    inset: 8pt,
  )
  show table: it => {
    set text(size: 9pt)
    block(width: 100%)[#it]
  }

  body
}
