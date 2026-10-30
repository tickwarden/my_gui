execute store result score #moved bazaar.tmp run clear @s minecraft:emerald 64
execute if score #moved bazaar.tmp matches 0 run return run function bazaar:act/fail_noemerald
scoreboard players operation @s bazaar.bank += #moved bazaar.tmp
playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.6 1.3
tellraw @s [{"text":"Yatırıldı: ","color":"green"},{"score":{"name":"#moved","objective":"bazaar.tmp"},"color":"yellow"},{"text":" zümrüt","color":"gray"}]
function bazaar:gui/render
