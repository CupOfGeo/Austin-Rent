# install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"


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


# gcloud auth login
# gcloud auth application-default login
sudo apt update
sudo apt install age


# Claude Code install
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
export NVM_DIR="/usr/local/share/nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install node
npm install -g @anthropic-ai/claude-code