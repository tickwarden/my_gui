execute unless entity @s[tag=bazaar.admin] run return run function bazaar:act/fail_admin
data modify storage bazaar:shop items set from storage bazaar:defaults items
playsound minecraft:block.amethyst_block.chime player @s ~ ~ ~ 1 1
tellraw @s {"text":"Stok ve fiyatlar varsayılana döndü.","color":"green"}
function bazaar:gui/render
