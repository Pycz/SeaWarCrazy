SeaWarCrazy
===========

Judge for bot players in SeaWar with GUI on wxPython and with simple bot

How to install (Ubuntu)
--------------

```bash
sudo apt install wx3.0
python frame.py
```

**bot.py** - simple bot for watch, how it works.


Bot interface
-------------

All commands must be sent by standart input/output.

Judge interface:

NB! All commands must be on the new line!

1) Print the name of the bot.

2) Print "OK". It'll show the judge, that the bot is ready.

3) Read a line. If it is "0" - you'll be first. If it's "1" - second.

4) If bot is 1st or if enemy "miss"ed - it must print a coordinate of his strike in "b4" format. Possible letters: "abcdefghij". Possible digits: "1 2 3 4 5 6 7 8 9 10".

5) Then it must read a line. "miss" means that you missed, "ou" means that you piped some enemy's ship and "kill" means that you killed it.

6) Read a line. If it is "nend" - game isn`t ended, "win" - you are a winner, "lose" - you are a loser. In case of "win"/"lose" bot may be terminated.

7) If you "ou"ed or "kill"ed enemy - repeat steps 4-7. Else go to step 8.

8) If bot is 2nd or it is "miss"ed, it must read a line. It is coordinates of enemy's strike in "b4" format.

9) You must print a string "miss"/"ou"/"kill" - according to enemy's strike.

10) Read a line. If it is "nend" - game isn`t ended, "win" - you are a winner, "lose" - you are a loser. In case of "win"/"lose" bot may be terminated.

11) If enemy's strike is "ou"/"kill" - repeat steps 8-11. Else go to step 4.

