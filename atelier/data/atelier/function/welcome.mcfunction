tag @s add atelier.welcomed
execute unless score @s atelier.id matches 1.. run function atelier:assign_id
function atelier:give_key
tellraw @s [{"text":"Atölye kitabı verildi. ","color":"light_purple"},{"text":"/trigger atelier","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger atelier"}}]
