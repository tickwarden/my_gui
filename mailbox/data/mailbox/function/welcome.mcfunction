tag @s add mailbox.welcomed
execute unless score @s mailbox.id matches 1.. run function mailbox:assign_id
function mailbox:give_key
tellraw @s [{"text":"Posta defteri verildi. ","color":"white"},{"text":"/trigger mailbox","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger mailbox"}}]
