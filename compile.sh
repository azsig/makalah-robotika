#!/bin/bash

# ==============================================================================
# SCRIPT KOMPILASI OTOMATIS TEMPLATE MODULAR LATEX
# ==============================================================================
# Script ini mengompilasi main.tex (Laporan) dan slides/slides.tex (Presentasi).

# Pewarnaan Output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# File Utama
MAIN_TEX="main.tex"
SLIDES_DIR="slides"
SLIDES_TEX="slides.tex"

# Fungsi Membersihkan File Sampah LaTeX
clean_temp() {
    echo -e "${YELLOW}Membersihkan file auxiliary LaTeX...${NC}"
    # Bersihkan di root
    rm -f *.aux *.log *.toc *.lof *.lot *.out *.bbl *.blg *.xml *.bcf *.fdb_latexmk *.fls
    # Bersihkan di slides
    if [ -d "$SLIDES_DIR" ]; then
        cd "$SLIDES_DIR"
        rm -f *.aux *.log *.toc *.lof *.lot *.out *.bbl *.blg *.xml *.bcf *.fdb_latexmk *.fls *.nav *.snm
        cd ..
    fi
    echo -e "${GREEN}Pembersihan selesai!${NC}"
}

# Fungsi Kompilasi Laporan/Makalah (main.tex)
compile_paper() {
    echo -e "${BLUE}=== Mengompilasi Laporan (main.tex) ===${NC}"
    if ! command -v pdflatex &> /dev/null; then
        echo -e "${RED}Error: pdflatex tidak ditemukan. Pastikan TeX Live atau MiKTeX terinstall.${NC}"
        return 1
    fi

    echo -e "${YELLOW}Langkah 1: Running pdflatex...${NC}"
    pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null
    
    if command -v biber &> /dev/null; then
        echo -e "${YELLOW}Langkah 2: Running biber untuk sitasi...${NC}"
        biber main > /dev/null
    else
        echo -e "${YELLOW}Biber tidak ditemukan, melewatkan kompilasi sitasi.${NC}"
    fi

    echo -e "${YELLOW}Langkah 3: Running pdflatex (2)...${NC}"
    pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null
    
    echo -e "${YELLOW}Langkah 4: Running pdflatex (3) untuk cross-reference...${NC}"
    pdflatex -interaction=nonstopmode "$MAIN_TEX" > /dev/null

    if [ -f "main.pdf" ]; then
        echo -e "${GREEN}Laporan sukses dikompilasi -> main.pdf${NC}"
    else
        echo -e "${RED}Gagal menghasilkan main.pdf. Periksa log di main.log.${NC}"
    fi
}

# Fungsi Kompilasi Slide Presentasi (slides/slides.tex)
compile_slides() {
    echo -e "${BLUE}=== Mengompilasi Slide (slides/slides.tex) ===${NC}"
    if [ ! -d "$SLIDES_DIR" ] || [ ! -f "$SLIDES_DIR/$SLIDES_TEX" ]; then
        echo -e "${RED}Error: Direktori atau file slides/slides.tex tidak ditemukan.${NC}"
        return 1
    fi

    cd "$SLIDES_DIR"
    
    echo -e "${YELLOW}Langkah 1: Running pdflatex...${NC}"
    pdflatex -interaction=nonstopmode "$SLIDES_TEX" > /dev/null
    
    echo -e "${YELLOW}Langkah 2: Running pdflatex (2) untuk link/outline...${NC}"
    pdflatex -interaction=nonstopmode "$SLIDES_TEX" > /dev/null
    
    cd ..

    if [ -f "$SLIDES_DIR/slides.pdf" ]; then
        echo -e "${GREEN}Slide sukses dikompilasi -> slides/slides.pdf${NC}"
    else
        echo -e "${RED}Gagal menghasilkan slides/slides.pdf. Periksa log di slides/slides.log.${NC}"
    fi
}

# Argumen Menu
case "$1" in
    paper)
        compile_paper
        ;;
    slides)
        compile_slides
        ;;
    clean)
        clean_temp
        ;;
    all|"")
        compile_paper
        compile_slides
        ;;
    *)
        echo -e "Penggunaan: $0 {paper|slides|clean|all}"
        echo -e "  paper  : Mengompilasi laporan utama (main.tex)"
        echo -e "  slides : Mengompilasi presentasi Beamer (slides/slides.tex)"
        echo -e "  clean  : Menghapus file auxiliary hasil kompilasi"
        echo -e "  all    : Mengompilasi laporan dan presentasi (default)"
        exit 1
        ;;
esac
