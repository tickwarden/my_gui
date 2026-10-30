function vault:sync/current
execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
execute if score @s vault.page matches 0 run function vault:compact/go_a with storage vault:macro
execute if score @s vault.page matches 1 run function vault:compact/go_b with storage vault:macro
execute if score @s vault.page matches 2 run function vault:compact/go_c with storage vault:macro
function vault:load/current
playsound minecraft:block.chest.close player @s ~ ~ ~ 0.4 1.4
title @s actionbar {"text":"Sayfa sıkıştırıldı.","color":"gold"}
