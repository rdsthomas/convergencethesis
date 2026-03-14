#!/usr/bin/env bash
# Build script for "The AI Species" — Markdown → EPUB + PDF
# Usage: ./build.sh [epub|pdf|all]

set -euo pipefail
cd "$(dirname "$0")"

SOURCE="the-ai-species.md"
EPUB_OUT="output/the-ai-species.epub"
PDF_OUT="output/the-ai-species.pdf"
EPUB_CSS="styles/epub.css"
LUA_FILTER="styles/custom-divs.lua"
LATEX_TEMPLATE="styles/pdf-template.tex"
COVER="images/cover.png"

mkdir -p output

build_epub() {
    echo "📚 Building EPUB..."
    
    local args=(
        "$SOURCE"
        -o "$EPUB_OUT"
        --toc
        --toc-depth=2
        --split-level=2
        --lua-filter "$LUA_FILTER"
        --metadata title="The AI Species — Besitze sie. Sonst besitzt sie dich."
        --metadata author="Thomas Huhn"
        --metadata lang=de
        --metadata date=2026
    )
    
    [[ -f "$EPUB_CSS" ]] && args+=(--css "$EPUB_CSS")
    [[ -f "$COVER" ]] && args+=(--epub-cover-image "$COVER")
    
    pandoc "${args[@]}"
    
    echo "✅ EPUB created: $EPUB_OUT ($(du -h "$EPUB_OUT" | cut -f1))"
}

build_pdf() {
    echo "📄 Building PDF..."
    
    pandoc "$SOURCE" \
        -o "$PDF_OUT" \
        --toc \
        --toc-depth=2 \
        --top-level-division=chapter \
        --pdf-engine=xelatex \
        --lua-filter "$LUA_FILTER" \
        --template "$LATEX_TEMPLATE" \
        -V fontsize=11pt \
        -V lang=de \
        --metadata title="The AI Species — Besitze sie. Sonst besitzt sie dich." \
        --metadata author="Thomas Huhn" \
        --metadata date="2026"
    
    echo "✅ PDF created: $PDF_OUT ($(du -h "$PDF_OUT" | cut -f1))"
}

case "${1:-all}" in
    epub)  build_epub ;;
    pdf)   build_pdf ;;
    all)   build_epub; build_pdf ;;
    *)     echo "Usage: $0 [epub|pdf|all]"; exit 1 ;;
esac

echo ""
echo "🎉 Done! Output in ./output/"
ls -lh output/
