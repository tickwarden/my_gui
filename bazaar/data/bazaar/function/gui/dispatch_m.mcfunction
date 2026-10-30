$execute unless data storage bazaar:rt p$(pid).queue run return 0
$data modify storage bazaar:macro action set from storage bazaar:rt p$(pid).queue
$data remove storage bazaar:rt p$(pid).queue
function bazaar:gui/dispatch_call with storage bazaar:macro
