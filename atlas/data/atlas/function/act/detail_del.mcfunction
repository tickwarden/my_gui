execute if score @s atlas.mode matches 1 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 2 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 3 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 6 unless entity @s[tag=atlas.admin] run return run function atlas:act/fail_admin
execute if score @s atlas.mode matches 1 run data modify storage atlas:dest spawn.set set value 0b
execute if score @s atlas.mode matches 2 run data modify storage atlas:dest nether.set set value 0b
execute if score @s atlas.mode matches 3 run data modify storage atlas:dest end.set set value 0b
execute if score @s atlas.mode matches 4 run function atlas:save/del_safe
execute if score @s atlas.mode matches 5 run function atlas:save/del_home
execute if score @s atlas.mode matches 6 run function atlas:save/del_server
playsound minecraft:block.fire.extinguish player @s ~ ~ ~ 0.4 1.4
title @s actionbar {"text":"Kayıt silindi.","color":"red"}
