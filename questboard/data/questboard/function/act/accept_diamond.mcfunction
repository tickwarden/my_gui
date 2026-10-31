playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.3
tellraw @s {"text":"Görev kabul edildi: Elmas Madencisi","color":"green"}
title @s actionbar {"text":"Elmas Madencisi aktif.","color":"yellow"}
function questboard:gui/render
