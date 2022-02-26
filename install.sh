#!/bin/bash
set -e

zip_file="$HOME"/gep.zip
gep_folder="$HOME"/GenomicPipeline
gep_folder_extracted="$gep_folder"/GenomicPipeline-main

sleep 3
echo ">>> Fetching repository from GitHub..."
wget --quiet --tries 5 --timeout 10 --output-document "$zip_file" https://codeload.github.com/ManuelArcieri/GenomicPipeline/zip/refs/heads/main

echo ">>> Unzipping repository..."
mkdir --parents "$gep_folder"
rm --force --recursive --dir "${gep_folder:?}"/*
unzip -qq -o "$zip_file" -d "$gep_folder"
rm --force "$zip_file"
mv --force "$gep_folder_extracted"/* "$gep_folder"/
rm --force --recursive --dir "$gep_folder_extracted"
chmod +x "$gep_folder"/gep.sh "$gep_folder"/install.sh

echo ">>> Creating Python virtual environment..."
python3 -m venv "$gep_folder"/env
source "$gep_folder"/env/bin/activate
pip3 install --quiet --upgrade --requirement "$gep_folder"/requirements.txt
deactivate

echo ">>> Setting 'gep' command..."
grep --fixed-strings --line-regexp --quiet "alias gep='$gep_folder/gep.sh'" "$HOME"/.bashrc || echo "alias gep='$gep_folder/gep.sh'" >>"$HOME"/.bashrc
# shellcheck disable=SC2139
alias gep="$gep_folder"/gep.sh

echo ">>> GenomicPipeline has been successfully installed or updated"
