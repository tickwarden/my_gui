summon minecraft:item ~ ~0.2 ~ {PickupDelay:0s,Tags:["bazaar.return"],Item:{id:"minecraft:stone",count:1}}
$data modify entity @e[type=minecraft:item,tag=bazaar.return,limit=1,sort=nearest] Item set from storage bazaar:live Items[{Slot:$(slot)b}]
data remove entity @e[type=minecraft:item,tag=bazaar.return,limit=1,sort=nearest] Item.Slot
tag @e[type=minecraft:item,tag=bazaar.return,limit=1,sort=nearest] remove bazaar.return
playsound minecraft:entity.item.pickup player @s ~ ~ ~ 0.4 1.2
