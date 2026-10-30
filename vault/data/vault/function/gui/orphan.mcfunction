scoreboard players operation #id vault.tmp = @s vault.id
execute store result storage vault:macro pid int 1 run scoreboard players get #id vault.tmp
execute if score @s vault.page matches 0 run function vault:vault/sync_orphan_a with storage vault:macro
execute if score @s vault.page matches 1 run function vault:vault/sync_orphan_b with storage vault:macro
execute if score @s vault.page matches 2 run function vault:vault/sync_orphan_c with storage vault:macro
kill @s
