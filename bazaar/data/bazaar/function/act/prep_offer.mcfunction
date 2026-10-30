scoreboard players operation @s bazaar.back = @s bazaar.page
$execute unless data storage bazaar:shop items.$(key) run return run function bazaar:act/fail_missing
$data modify storage bazaar:tmp offer set from storage bazaar:shop items.$(key)
$data modify storage bazaar:tmp offer.key set value "$(key)"
$data modify storage bazaar:tmp offer.mode set value "$(mode)"
execute store result storage bazaar:macro pid int 1 run scoreboard players get @s bazaar.id
function bazaar:act/store_offer with storage bazaar:macro
scoreboard players set @s bazaar.page 9
function bazaar:gui/render
playsound minecraft:ui.button.click player @s ~ ~ ~ 0.5 1.15
function bazaar:act/announce_offer with storage bazaar:tmp offer
