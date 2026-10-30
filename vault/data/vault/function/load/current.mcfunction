execute store result storage vault:macro pid int 1 run scoreboard players get @s vault.id
data merge entity @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] {Items:[]}
execute if score @s vault.page matches 0 run function vault:load/page_a with storage vault:macro
execute if score @s vault.page matches 1 run function vault:load/page_b with storage vault:macro
execute if score @s vault.page matches 2 run function vault:load/page_c with storage vault:macro
function vault:ctrl/paint
scoreboard players operation @e[type=minecraft:chest_minecart,tag=vault.this,limit=1] vault.page = @s vault.page
