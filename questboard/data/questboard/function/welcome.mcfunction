tag @s add questboard.welcomed
execute unless score @s questboard.id matches 1.. run function questboard:assign_id
function questboard:give_key
tellraw @s [{"text":"Görev haritası verildi. ","color":"gold"},{"text":"/trigger questboard","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger questboard"}}]
