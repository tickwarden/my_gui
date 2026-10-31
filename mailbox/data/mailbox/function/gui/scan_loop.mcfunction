execute if score #slot mailbox.tmp matches 27.. run return 0
execute store result storage mailbox:macro slot int 1 run scoreboard players get #slot mailbox.tmp
function mailbox:gui/scan_slot with storage mailbox:macro
scoreboard players add #slot mailbox.tmp 1
function mailbox:gui/scan_loop
