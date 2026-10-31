$execute unless data storage atelier:rt p$(pid).queue run return 0
$data modify storage atelier:macro action set from storage atelier:rt p$(pid).queue
$data remove storage atelier:rt p$(pid).queue
function atelier:gui/dispatch_call with storage atelier:macro
