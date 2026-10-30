execute store result storage atlas:dest s5.x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:dest s5.y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:dest s5.z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:dest s5.dim int 1 run scoreboard players get #dim atlas.tmp
data modify storage atlas:dest s5.set set value 1b
data modify storage atlas:dest s5.name set value "İşaret 6"
