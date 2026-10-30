execute store result score #moved bazaar.tmp run clear @s minecraft:emerald 0
execute if score #moved bazaar.tmp matches 0 run return run function bazaar:act/fail_noemerald
clear @s minecraft:emerald
scoreboard players operation @s bazaar.bank += #moved bazaar.tmp
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.7 1.1
tellraw @s [{"text":"Tümü yatırıldı: ","color":"green"},{"score":{"name":"#moved","objective":"bazaar.tmp"},"color":"yellow"}]
function bazaar:gui/render
