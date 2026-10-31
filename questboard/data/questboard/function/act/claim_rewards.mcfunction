playsound minecraft:entity.experience_orb.pickup player @s ~ ~ ~ 0.7 1.2
tellraw @s {"text":"Ödüller verildi (demo zümrüt).","color":"green"}
give @s minecraft:emerald 3
function questboard:gui/render
