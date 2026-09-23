#!/bin/bash
SRC_DIR="/home/yopitek/Documents/Obsidian_vault/GX10_HQ/B_Work/02_Products/06_Hak5/manual"
WIKI_DIR="/home/yopitek/Project/yupitek-wiki"

declare -A MAPPING
MAPPING["bash_bunny"]="bash-bunny-mark-ii"
MAPPING["key_croc"]="key-croc"
MAPPING["omg_mailcious_cable_detector"]="malicious-cable-detector"
MAPPING["omg_plug"]="omg-plug"
MAPPING["omg_cable"]="omg-cable"
MAPPING["packet_squirrel"]="packet-squirrel-mark-ii"
MAPPING["plunder_bug"]="plunder-bug-lan-tap"
MAPPING["screen_crab"]="screen-crab"
MAPPING["shark_jack"]="shark-jack"
MAPPING["rubber_ducky"]="usb-rubber-ducky"
MAPPING["wifi_pineapple_enterpricse"]="wifi-pineapple-enterprise"
MAPPING["wifi_pineapple_markvii"]="wifi-pineapple-mark-vii"
# Let's map any other ones later if needed.

for base in "${!MAPPING[@]}"; do
    dest="${MAPPING[$base]}"
    
    echo "Processing $base -> $dest..."
    
    # EN -> docs/
    if [ -f "$SRC_DIR/${base}_en.md" ]; then
        mkdir -p "$WIKI_DIR/docs/02-hak5/products/$dest"
        cp "$SRC_DIR/${base}_en.md" "$WIKI_DIR/docs/02-hak5/products/$dest/index.md"
    fi
    
    # CN -> i18n/zh-CN/
    if [ -f "$SRC_DIR/${base}_cn.md" ]; then
        mkdir -p "$WIKI_DIR/i18n/zh-CN/docusaurus-plugin-content-docs/current/02-hak5/products/$dest"
        cp "$SRC_DIR/${base}_cn.md" "$WIKI_DIR/i18n/zh-CN/docusaurus-plugin-content-docs/current/02-hak5/products/$dest/index.md"
    fi
    
    # TW -> i18n/zh-TW/
    if [ -f "$SRC_DIR/${base}_tw.md" ]; then
        mkdir -p "$WIKI_DIR/i18n/zh-TW/docusaurus-plugin-content-docs/current/02-hak5/products/$dest"
        cp "$SRC_DIR/${base}_tw.md" "$WIKI_DIR/i18n/zh-TW/docusaurus-plugin-content-docs/current/02-hak5/products/$dest/index.md"
    fi
done

echo "Copy complete."
