playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.3
tellraw @s {"text":"Görev kabul edildi: Nether Gezgini","color":"green"}
title @s actionbar {"text":"Nether Gezgini aktif.","color":"yellow"}
function questboard:gui/render
