tag @s add vault.welcomed
execute unless score @s vault.id matches 1.. run function vault:assign_id
function vault:give_key
tellraw @s [{"text":"Kasa anahtarı verildi. ","color":"dark_aqua"},{"text":"/trigger vault","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger vault"}}]
