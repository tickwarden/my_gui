execute store result score #x atlas.tmp run data get entity @s Pos[0]
execute store result score #y atlas.tmp run data get entity @s Pos[1]
execute store result score #z atlas.tmp run data get entity @s Pos[2]
scoreboard players set #dim atlas.tmp -1
execute if entity @s[nbt={Dimension:"minecraft:overworld"}] run scoreboard players set #dim atlas.tmp 0
execute if entity @s[nbt={Dimension:"minecraft:the_nether"}] run scoreboard players set #dim atlas.tmp 1
execute if entity @s[nbt={Dimension:"minecraft:the_end"}] run scoreboard players set #dim atlas.tmp 2
execute if score #dim atlas.tmp matches -1 run scoreboard players set #dim atlas.tmp 0
execute store result storage atlas:macro x int 1 run scoreboard players get #x atlas.tmp
execute store result storage atlas:macro y int 1 run scoreboard players get #y atlas.tmp
execute store result storage atlas:macro z int 1 run scoreboard players get #z atlas.tmp
execute store result storage atlas:macro dim int 1 run scoreboard players get #dim atlas.tmp
execute store result storage atlas:macro pid int 1 run scoreboard players get @s atlas.id
execute store result storage atlas:macro sel int 1 run scoreboard players get @s atlas.sel
