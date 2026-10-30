tag @s add reliquary.welcomed
execute unless score @s reliquary.id matches 1.. run function reliquary:assign_id
function reliquary:give_key
tellraw @s [{"text":"Emanet asası verildi. ","color":"light_purple"},{"text":"/trigger reliquary","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger reliquary"}}]
