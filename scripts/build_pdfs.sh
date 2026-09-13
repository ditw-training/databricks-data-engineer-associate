#!/usr/bin/env bash
# Build the training PDFs into docs/ENG and docs/PL from the sources in
# utilization/en and utilization/pl.
#
#   ./scripts/build_pdfs.sh                      # everything, both languages
#   ./scripts/build_pdfs.sh cheatsheet           # one document, both languages
#   ./scripts/build_pdfs.sh cheatsheet PL        # one document, one language
#   PDF_OUT=/preview ./scripts/build_pdfs.sh     # write to /preview/ENG, /preview/PL
#   PDF_WORK=/tmp/w ./scripts/build_pdfs.sh      # separate work dir (parallel builds)
#
# Requires: pandoc, weasyprint  (brew install pandoc weasyprint)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/utilization"
OUT_ROOT="${PDF_OUT:-$ROOT/docs}"
CSS="$SRC/pdf_style.css"
COVER="$SRC/_cover.html"
WORK="${PDF_WORK:-$ROOT/.build}"
rm -rf "$WORK"; mkdir -p "$WORK"

for tool in pandoc weasyprint; do
    command -v "$tool" >/dev/null || { echo "Missing: $tool" >&2; exit 1; }
done

# lang | source dir | html lang | contents heading | edition line
LANGS=(
"ENG|en|en|Contents|Edition: September 2026"
"PL|pl|pl|Spis treści|Wydanie: wrzesień 2026"
)

# lang | name | source | layout | contents page | eyebrow | title | subtitle
DOCS=(
"ENG|cheatsheet_databricks_data_engineer|cheatsheet.md|chapters|yes|Training reference|Databricks Data Engineer Associate|Reference guide for the three-day course"
"ENG|quiz_databricks_data_engineer|quiz.md|continuous|no|Knowledge check|Databricks Data Engineer Associate|Course quizzes for all three days, with answer key"
"ENG|exam_objectives_map|exam_objectives_map.md|continuous|yes|Certification|Exam objectives map|The May 2026 exam guide mapped to course modules and labs"
"ENG|next_steps|next_steps.md|continuous|yes|After the course|Next steps|Exam preparation, learning path and features beyond the exam"
"ENG|external_connection_guide|external_connection.md|continuous|no|Practical guide|External connection|Connecting Unity Catalog to ADLS Gen2"
"ENG|lakeflow_connect_sqlserver_guide|lakeflow_connect_sqlserver.md|continuous|no|Practical guide|Lakeflow Connect|Ingesting Azure SQL Database with the managed SQL Server connector"
"ENG|pyspark_vs_sparksql|pyspark_vs_sparksql.md|continuous|yes|Day 1–2 supplement|PySpark and Spark SQL|Side-by-side reference for ingestion and transformations"
"PL|cheatsheet_databricks_data_engineer|cheatsheet.md|chapters|yes|Materiał referencyjny|Databricks Data Engineer Associate|Kompendium do trzydniowego szkolenia"
"PL|quiz_databricks_data_engineer|quiz.md|continuous|no|Sprawdzenie wiedzy|Databricks Data Engineer Associate|Quizy ze wszystkich trzech dni z kluczem odpowiedzi"
"PL|exam_objectives_map|exam_objectives_map.md|continuous|yes|Certyfikacja|Mapa celów egzaminu|Exam guide z maja 2026 powiązany z modułami i laboratoriami"
"PL|next_steps|next_steps.md|continuous|yes|Po szkoleniu|Dalsze kroki|Przygotowanie do egzaminu, ścieżka rozwoju i funkcje poza egzaminem"
"PL|external_connection_guide|external_connection.md|continuous|no|Przewodnik praktyczny|Połączenie z ADLS Gen2|Podłączenie Unity Catalog do Azure Data Lake Storage"
"PL|lakeflow_connect_sqlserver_guide|lakeflow_connect_sqlserver.md|continuous|no|Przewodnik praktyczny|Lakeflow Connect|Ingestia z Azure SQL Database przez zarządzany konektor SQL Server"
"PL|pyspark_vs_sparksql|pyspark_vs_sparksql.md|continuous|yes|Uzupełnienie dni 1–2|PySpark i Spark SQL|Oba interfejsy obok siebie: odczyt, transformacje, agregacje"
)

build_one() {
    local lang="$1" srcdir="$2" htmllang="$3" toc_title="$4" edition="$5"
    local name="$6" src="$7" layout="$8" toc="$9" eyebrow="${10}" title="${11}" subtitle="${12}"
    local input="$SRC/$srcdir/$src" work="$WORK/$lang-$name" out="$OUT_ROOT/$lang"
    local meta="<strong>Altkom Akademia</strong><br>$edition"

    [[ -f "$input" ]] || { echo "  SKIP $lang/$name (no source: $srcdir/$src)"; return 0; }
    mkdir -p "$out"

    python3 - "$COVER" "$eyebrow" "$title" "$subtitle" "$meta" > "$work.cover.html" <<'PY'
import sys, io
tpl = io.open(sys.argv[1], encoding="utf-8").read()
for token, value in zip(("__EYEBROW__", "__TITLE__", "__SUBTITLE__", "__META__"), sys.argv[2:6]):
    tpl = tpl.replace(token, value)
sys.stdout.write(tpl)
PY

    # gfm keeps GitHub list, table and autolink behaviour; +attributes allows
    # headings like  # Title {data-label="Module 01"};  +smart gives real quotes.
    pandoc "$input" --from=gfm+attributes+smart --to=html5 --wrap=none > "$work.body.html"

    if [[ "$toc" == "yes" ]]; then
        python3 - "$work.body.html" "$toc_title" > "$work.toc.html" <<'PY'
import io, re, sys
body = io.open(sys.argv[1], encoding="utf-8").read()
rows = []
for attrs, text in re.findall(r"<h1([^>]*)>(.*?)</h1>", body, re.S):
    ident = re.search(r'id="([^"]+)"', attrs)
    if not ident:
        continue
    label = re.search(r'data-label="([^"]+)"', attrs)
    title = re.sub(r"<[^>]+>", "", text).strip()
    rows.append(f'<li><a href="#{ident.group(1)}"><span class="toc-label">'
                f'{label.group(1) if label else ""}</span>{title}</a></li>')
sys.stdout.write(f'<nav class="toc"><h1>{sys.argv[2]}</h1><ol>' + "".join(rows) + "</ol></nav>\n")
PY
    else
        : > "$work.toc.html"
    fi

    {
        printf '<!DOCTYPE html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n' "$htmllang"
        printf '<title>%s</title>\n</head>\n<body class="%s doc-%s">\n' "$title" "$layout" "$name"
        cat "$work.cover.html" "$work.toc.html" "$work.body.html"
        printf '\n</body>\n</html>\n'
    } > "$work.html"

    # Base URL = the language folder, so ../../assets/images/... resolves.
    weasyprint -s "$CSS" -u "$SRC/$srcdir/" "$work.html" "$out/$name.pdf"
    printf "  ✓ %-4s %-40s %s\n" "$lang" "$name.pdf" "$(du -h "$out/$name.pdf" | cut -f1)"
}

only="${1:-}"
only_lang="${2:-}"
echo "Building PDFs → $OUT_ROOT/{ENG,PL}"
for lrow in "${LANGS[@]}"; do
    IFS='|' read -r lang srcdir htmllang toc_title edition <<< "$lrow"
    [[ -n "$only_lang" && "$lang" != "$only_lang" ]] && continue
    for row in "${DOCS[@]}"; do
        IFS='|' read -r dlang name src layout toc eyebrow title subtitle <<< "$row"
        [[ "$dlang" != "$lang" ]] && continue
        [[ -n "$only" && "$name" != *"$only"* ]] && continue
        build_one "$lang" "$srcdir" "$htmllang" "$toc_title" "$edition" \
                  "$name" "$src" "$layout" "$toc" "$eyebrow" "$title" "$subtitle"
    done
done
echo "Done."
