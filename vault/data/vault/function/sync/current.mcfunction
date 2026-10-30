execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
execute if score @s vault.page matches 0 run function vault:sync/page_a with storage vault:macro
execute if score @s vault.page matches 1 run function vault:sync/page_b with storage vault:macro
execute if score @s vault.page matches 2 run function vault:sync/page_c with storage vault:macro
scoreboard players operation @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] vault.page = @s vault.page
scoreboard players operation @s vault.used = #used vault.tmp
