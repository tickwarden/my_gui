$execute unless data storage reliquary:rt p$(pid).queue run return 0
$data modify storage reliquary:macro action set from storage reliquary:rt p$(pid).queue
$data remove storage reliquary:rt p$(pid).queue
function reliquary:gui/dispatch_call with storage reliquary:macro
