execute unless score @s bazaar.bank matches 1.. run return run function bazaar:act/fail_money
scoreboard players set #move bazaar.tmp 64
execute if score @s bazaar.bank < #move bazaar.tmp run scoreboard players operation #move bazaar.tmp = @s bazaar.bank
scoreboard players operation @s bazaar.bank -= #move bazaar.tmp
execute store result storage bazaar:macro n int 1 run scoreboard players get #move bazaar.tmp
function bazaar:act/give_emeralds with storage bazaar:macro
playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.6 1
tellraw @s [{"text":"Çekildi: ","color":"yellow"},{"score":{"name":"#move","objective":"bazaar.tmp"},"color":"green"},{"text":" zümrüt","color":"gray"}]
function bazaar:gui/render
