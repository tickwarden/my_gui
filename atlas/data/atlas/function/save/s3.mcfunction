execute store result storage atlas:dest s3.x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:dest s3.y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:dest s3.z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:dest s3.dim int 1 run scoreboard players get #dim atlas.tmp
data modify storage atlas:dest s3.set set value 1b
data modify storage atlas:dest s3.name set value "İşaret 4"
