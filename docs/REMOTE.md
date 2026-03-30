# Running experiments remotely

Start a new tmux session and run the experiment, piping output to a log file:

```bash
tmux new -s experimentos
bash run.sh 2>&1 | tee experimentos.log
```

To detach from the session (leaving it running in the background):

```
Ctrl+b d
```

To reattach to the session later:

```bash
tmux attach -t experimentos
```