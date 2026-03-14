#!/usr/bin/env bash
# Build script for "The AI Species" — Markdown → EPUB + PDF
# Usage: ./build.sh [epub|pdf|all]

set -euo pipefail
cd "$(dirname "$0")"

SOURCE="the-ai-species.md"
EPUB_OUT="output/the-ai-species.epub"
PDF_OUT="output/the-ai-species.pdf"

# Create output directory
mkdir -p output

# EPUB metadata
EPUB_CSS="styles/epub.css"
COVER="images/cover.png"

build_epub() {
    echo "📚 Building EPUB..."
    
    local args=(
        "$SOURCE"
        -o "$EPUB_OUT"
        --toc
        --toc-depth=2
        --epub-chapter-level=2
        --metadata title="The AI Species — Besitze sie. Sonst besitzt sie dich."
        --metadata author="Thomas Huhn"
        --metadata lang=de
        --metadata date=2026
    )
    
    # Add CSS if exists
    if [[ -f "$EPUB_CSS" ]]; then
        args+=(--css "$EPUB_CSS")
    fi
    
    # Add cover if exists
    if [[ -f "$COVER" ]]; then
        args+=(--epub-cover-image "$COVER")
    fi
    
    pandoc "${args[@]}"
    
    echo "✅ EPUB created: $EPUB_OUT"
    echo "   Size: $(du -h "$EPUB_OUT" | cut -f1)"
}

build_pdf() {
    echo "📄 Building PDF..."
    
    pandoc "$SOURCE" \
        -o "$PDF_OUT" \
        --toc \
        --toc-depth=2 \
        --pdf-engine=xelatex \
        -V geometry:margin=2.5cm \
        -V fontsize=11pt \
        -V lang=de \
        -V mainfont="DejaVu Serif" \
        -V sansfont="DejaVu Sans" \
        -V monofont="DejaVu Sans Mono" \
        --metadata title="The AI Species" \
        --metadata author="Thomas Huhn"
    
    echo "✅ PDF created: $PDF_OUT"
    echo "   Size: $(du -h "$PDF_OUT" | cut -f1)"
}

case "${1:-all}" in
    epub)
        build_epub
        ;;
    pdf)
        build_pdf
        ;;
    all)
        build_epub
        build_pdf
        ;;
    *)
        echo "Usage: $0 [epub|pdf|all]"
        exit 1
        ;;
esac

echo ""
echo "🎉 Done! Output in ./output/"
ls -lh output/
