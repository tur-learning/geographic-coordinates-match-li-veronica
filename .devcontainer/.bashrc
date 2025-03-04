# Common aliases
alias ll='ls -lah --color=auto'
alias l='ls -lrth'
alias grep='grep --color=auto'
alias py='python'
alias venv='python -m venv .venv && source .venv/bin/activate'
alias gs='git status'
alias ga='git add .'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'
alias cdw='cd /workspace'

# Activate Python virtualenv if found
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
