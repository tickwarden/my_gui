summon minecraft:item ~ ~0.2 ~ {PickupDelay:0s,Tags:["atlas.return"],Item:{id:"minecraft:stone",count:1}}
$data modify entity @e[type=minecraft:item,tag=atlas.return,limit=1,sort=nearest] Item set from storage atlas:live Items[{Slot:$(slot)b}]
data remove entity @e[type=minecraft:item,tag=atlas.return,limit=1,sort=nearest] Item.Slot
tag @e[type=minecraft:item,tag=atlas.return,limit=1,sort=nearest] remove atlas.return
playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.4 1.2
