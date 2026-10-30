execute if score @s atlas.mode matches 1 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 2 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 3 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 6 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
function atlas:save/capture
execute if score @s atlas.mode matches 1 run function atlas:save/spawn
execute if score @s atlas.mode matches 2 run function atlas:save/nether
execute if score @s atlas.mode matches 3 run function atlas:save/end
execute if score @s atlas.mode matches 4 run function atlas:save/safe
execute if score @s atlas.mode matches 5 run function atlas:save/home
execute if score @s atlas.mode matches 6 run function atlas:save/server
playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1.2
title @s actionbar {"text":"Konum kaydedildi.","color":"green"}
