#!/bin/bash
export GOG_KEYRING_PASSWORD=jeannie HOME=/root
mkdir -p /tmp/maschinengeld-images

download() {
  local id="$1" name="$2"
  echo "Downloading $name..."
  gog drive download "$id" --account th@consensus.ventures --output "/tmp/maschinengeld-images/$name" 2>/dev/null
}

download "1OYiFX6iYcMo52kZHTnYC-w1Y2leBtV_O" "00-konvergenz-venn-color.png"
download "12drmSIDq5fysMTpKmcQOdenRwgKxlRhA" "01-250-jahre-umbrueche-color.png"
download "1vDEgmy-WcJDD7rlrfAYjNHsTkxgp26H0" "01b-infrastruktur-vs-anwendung-color.png"
download "1n9J3k4TxGyyPAiZZrr1K0Xl7gCXbcbax" "02a-vier-phasen-ki-color.png"
download "1IIJp5wCVEXoN7Rfhjv-ZBYLKl7d3eQT2" "02b-ki-landscape-color.png"
download "1QwVzoLEgx_WtoOa5LI7exY9ttJCcdRYH" "02c-deepseek-kosten-color.png"
download "1KRfHvUy71nmHWyrDdhjhZ7ysrR2wMikb" "03a-maschine-vs-bank-color.png"
download "1Ec0foQODsj5IMHR52QRhrS9PodqSq9EF" "03b-stablecoin-vs-visa-color.png"
download "1YDP5CnbyOtX3HqDZ05hFR0vCO47TGs4W" "03c-tokenisierung-flow-color.png"
download "1hb_ptBnW7bwgkyGPKehSfJhNjtFxHJ_C" "03d-wer-tokenisiert-was-color.png"
download "12G6AiRp0NgAyGyPMkagxvIDU05E9o_yX" "03e-dao-anatomie-color.png"
download "1qPg3uJreGel0pGuQdVyCSt3u1_JvA_qK" "04a-ki-weltkarte-color.png"
download "1EC810DBu1Qya1yZp5kGhsdUi6g3T1ENt" "04b-chip-krieg-tsmc-color.png"
download "1zxv8I-cVZv_hZFoDcgvHz2fTPTOpeRUw" "05a-kraftwerk-kaeufer-color.png"
download "10RZptOx3KbIolQGVUNw9toWUFj6o-f_i" "05b-energiehunger-ki-color.png"
download "1NAqjj0aFRKlVQdCvt9vkXjaXx3tXBTbJ" "06a-jobs-verschwinden-entstehen-color.png"
download "1qGBD8zeeyKmGNKSEvJI902zTOxI7IFS-" "06b-geschichte-der-arbeit-color.png"
download "1wxZCeI6Pd6SWZPX6LPu5tk87rKlklW68" "07-regulierung-ampel-color.png"
download "1YM48_KVltcbww0H8_EkuOTT9h2-CPhR6" "08-szenario-2026-2035-color.png"
download "1CdTL-0h-zaF8KIdXN2M_MfLmznJalNvr" "09-bci-interface-evolution-color.png"
download "1wXXkgkGIg2tENsJuQkeeeMroEcQz-hNN" "11-longevity-smart-money-color.png"
download "1BIbXWzUGZ3NONrc578JYrWAMK0m943C1" "12a-barbell-strategie-color.png"
download "19KzZCGWCqKkro8coLh_DoFEG6Wu3HwPO" "12b-portfolio-varianten-color.png"
download "1IO8XnIJKqj4BCwXyVz7sKOQG3yzv0fRX" "13-risiko-matrix-color.png"

echo "Done! $(ls /tmp/maschinengeld-images/*.png 2>/dev/null | wc -l) images downloaded"
