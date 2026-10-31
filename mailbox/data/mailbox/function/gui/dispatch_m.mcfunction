$execute unless data storage mailbox:rt p$(pid).queue run return 0
$data modify storage mailbox:macro action set from storage mailbox:rt p$(pid).queue
$data remove storage mailbox:rt p$(pid).queue
function mailbox:gui/dispatch_call with storage mailbox:macro
