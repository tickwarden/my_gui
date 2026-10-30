execute store result score #day bazaar.tmp run time query day
execute unless score @s bazaar.day < #day bazaar.tmp run return run function bazaar:act/fail_daily
scoreboard players operation @s bazaar.day = #day bazaar.tmp
execute store result score #gift bazaar.tmp run data get storage bazaar:config daily
execute unless score #gift bazaar.tmp matches 1.. run scoreboard players set #gift bazaar.tmp 8
scoreboard players operation @s bazaar.bank += #gift bazaar.tmp
playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.6 1.4
tellraw @s [{"text":"Günlük ödül: ","color":"gold"},{"score":{"name":"#gift","objective":"bazaar.tmp"},"color":"green"},{"text":" zümrüt bankana eklendi.","color":"gray"}]
function bazaar:gui/render
