$execute unless data storage vault:rt p$(pid).queue run return 0
$data modify storage vault:macro action set from storage vault:rt p$(pid).queue
$data remove storage vault:rt p$(pid).queue
function vault:gui/dispatch_call with storage vault:macro
