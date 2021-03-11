"killing previous session"
tmux kill-session -t slarkbot
echo "starting new session"
tmux new-session -d -s slarkbot ./scripts/start_bot.sh
echo "started new session"