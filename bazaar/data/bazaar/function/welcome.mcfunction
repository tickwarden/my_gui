tag @s add bazaar.welcomed
execute unless score @s bazaar.id matches 1.. run function bazaar:assign_id
scoreboard players set @s bazaar.day -1
function bazaar:give_key
tellraw @s [{"text":"Çarşı asası verildi. ","color":"gold"},{"text":"Sağ tıkla","color":"yellow","bold":true},{"text":" veya ","color":"gray"},{"text":"/trigger bazaar","color":"aqua","underlined":true,"clickEvent":{"action":"run_command","value":"/trigger bazaar"}}]
