function vault:sync/current
scoreboard players operation #p vault.tmp = @s vault.page
execute if score #p vault.tmp matches 0 run scoreboard players set @s vault.page 2
execute if score #p vault.tmp matches 1 run scoreboard players set @s vault.page 0
execute if score #p vault.tmp matches 2 run scoreboard players set @s vault.page 1
function vault:load/current
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.4 1.1
