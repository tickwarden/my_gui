scoreboard players add #next mailbox.id 1
scoreboard players operation @s mailbox.id = #next mailbox.id
execute store result storage mailbox:macro pid int 1 run scoreboard players get @s mailbox.id
function mailbox:assign_store with storage mailbox:macro
