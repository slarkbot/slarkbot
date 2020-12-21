#!/bin/bash
# tmux has-session -t $session 2>/dev/null

if [ $? == 0 ]; then
    echo "found session slarkbot" 
    echo "killing session"
    tmux kill-session -t slarkbot
fi

cd scripts
echo "starting new session"
tmux new -d -s slarkbot start_bot.sh
echo "started new session"