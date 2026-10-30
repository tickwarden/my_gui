execute store result score #now atlas.tmp run time query gametime
execute if score @s atlas.cd > #now atlas.tmp run return run function atlas:act/fail_cd
execute store result score #wait atlas.tmp run data get storage atlas:config cooldown
execute unless score #wait atlas.tmp matches 1.. run scoreboard players set #wait atlas.tmp 160
scoreboard players operation #cd atlas.tmp = #now atlas.tmp
scoreboard players operation #cd atlas.tmp += #wait atlas.tmp
scoreboard players operation @s atlas.cd = #cd atlas.tmp
execute store result storage atlas:macro x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:macro y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:macro z int 1 run scoreboard players get #z atlas.tmp
execute if score #dim atlas.tmp matches 0 run function atlas:tp/go_ow with storage atlas:macro
execute if score #dim atlas.tmp matches 1 run function atlas:tp/go_nether with storage atlas:macro
execute if score #dim atlas.tmp matches 2 run function atlas:tp/go_end with storage atlas:macro
function atlas:gui/close
execute at @s run function atlas:tp/safety
playsound minecraft:entity.enderman.teleport player @s ~ ~ ~ 1 1
playsound minecraft:block.portal.travel player @s ~ ~ ~ 0.35 1.4
title @s title {"text":"Işınlandın","color":"aqua"}
title @s subtitle {"text":"Zemin kontrol edildi","color":"gray"}
