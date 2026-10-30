$execute unless data storage atlas:rt p$(pid).queue run return 0
$data modify storage atlas:macro action set from storage atlas:rt p$(pid).queue
$data remove storage atlas:rt p$(pid).queue
function atlas:gui/dispatch_call with storage atlas:macro
