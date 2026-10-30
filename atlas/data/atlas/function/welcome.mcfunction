tag @s add atlas.welcomed
execute unless score @s atlas.id matches 1.. run function atlas:assign_id
function atlas:give_key
tellraw @s [{"text":"Atlas değneği verildi. ","color":"aqua"},{"text":"/trigger atlas","color":"yellow","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger atlas"}}]
