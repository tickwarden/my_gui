$execute unless data storage questboard:rt p$(pid).queue run return 0
$data modify storage questboard:macro action set from storage questboard:rt p$(pid).queue
$data remove storage questboard:rt p$(pid).queue
function questboard:gui/dispatch_call with storage questboard:macro
