$scoreboard players set #price bazaar.tmp $(price)
$scoreboard players set #count bazaar.tmp $(count)
$scoreboard players set #stock bazaar.tmp $(stock)
$data modify storage bazaar:tmp id set value "$(id)"
$data modify storage bazaar:tmp key set value "$(key)"
$data modify storage bazaar:tmp mode set value "$(mode)"
$data modify storage bazaar:tmp name set value "$(name)"
execute store result storage bazaar:tmp count int 1 run scoreboard players get #count bazaar.tmp
execute if data storage bazaar:tmp {mode:"sell"} run return run function bazaar:act/commit_sell
function bazaar:act/commit_buy
