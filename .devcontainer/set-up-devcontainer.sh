
# install gcloud 
sudo apt install python3 python3-pip -y
curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-linux-x86_64.tar.gz
sudo tar -xf google-cloud-cli-linux-x86_64.tar.gz -C /opt
rm google-cloud-cli-linux-x86_64.tar.gz
sudo /opt/google-cloud-sdk/install.sh  --quiet

cat << 'EOF' >> ~/.zshrc
# Update PATH for the Google Cloud SDK
if [ -f '/opt/google-cloud-sdk/path.zsh.inc' ]; then . '/opt/google-cloud-sdk/path.zsh.inc'; fi
# Enable shell command completion for gcloud
if [ -f '/opt/google-cloud-sdk/completion.zsh.inc' ]; then . '/opt/google-cloud-sdk/completion.zsh.inc'; fi
EOF