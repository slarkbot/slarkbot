
session="slarkbot"

tmux has-session -t $session 2>/dev/null

if [ $? == 0 ]; then
    echo "found session $session"
    tmux kill-session -t slarkbot
fi

tmux new-session -d -s "slarkbot" ./start_bot.sh