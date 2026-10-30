scoreboard players operation @s atlas.back = @s atlas.page
scoreboard players set @s atlas.mode 6
scoreboard players set @s atlas.sel 2
scoreboard players set @s atlas.page 3
function atlas:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.45 1.3
