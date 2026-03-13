#import "template-v2.typ": *

#show: doc => book(doc, short-title: [THE AI SPECIES], author: [Thomas Huhn])


// Volltitel
#pagebreak(to: "odd")
#page(header: none, footer: none)[
  #v(0.9fr)
  #align(center)[
    #text(size: 30pt, weight: "bold", font: "Source Sans 3", fill: navy)[THE AI SPECIES]
    #v(10pt)
    #line(length: 68pt, stroke: 2.6pt + gold)
    #v(16pt)
    #text(size: 12.2pt, style: "italic", fill: rgb("#444"))[Besitze sie. Sonst besitzt sie dich.]
    #v(44pt)
    #text(size: 14pt, font: "Source Sans 3", weight: "medium")[Thomas Huhn]
    #v(1fr)
    #text(size: 9pt, fill: rgb("#888"))[Consensus Ventures GmbH]
  ]