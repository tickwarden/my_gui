playsound minecraft:entity.player.levelup player @s ~ ~ ~ 0.5 1.3
tellraw @s {"text":"Görev kabul edildi: Canavar Avı","color":"green"}
title @s actionbar {"text":"Canavar Avı aktif.","color":"yellow"}
function questboard:gui/render
