data modify storage reliquary:config set value {ready:1b,cooldown:12000,teams:1b}
team add rel.knight
team modify rel.knight color red
team modify rel.knight friendlyFire true
team modify rel.knight collisionRule always
team modify rel.knight prefix {"text":"[Şövalye] ","color":"red"}
team add rel.archer
team modify rel.archer color green
team modify rel.archer friendlyFire true
team modify rel.archer collisionRule always
team modify rel.archer prefix {"text":"[Nişancı] ","color":"green"}
team add rel.farmer
team modify rel.farmer color yellow
team modify rel.farmer friendlyFire true
team modify rel.farmer collisionRule always
team modify rel.farmer prefix {"text":"[Çiftçi] ","color":"yellow"}
team add rel.miner
team modify rel.miner color gray
team modify rel.miner friendlyFire true
team modify rel.miner collisionRule always
team modify rel.miner prefix {"text":"[Madenci] ","color":"gray"}
team add rel.alch
team modify rel.alch color light_purple
team modify rel.alch friendlyFire true
team modify rel.alch collisionRule always
team modify rel.alch prefix {"text":"[Simyacı] ","color":"light_purple"}
team add rel.expl
team modify rel.expl color aqua
team modify rel.expl friendlyFire true
team modify rel.expl collisionRule always
team modify rel.expl prefix {"text":"[Kaşif] ","color":"aqua"}
