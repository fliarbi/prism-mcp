<?php
// Live backend/proxy verification only. Never creates or updates a WP post.
require '/var/www/html/wp-load.php';
$began = microtime(true);
$start = prism_call('system.request', [
    'feature'=>'research.citations',
    'args'=>['claim'=>'Urban tree cover is associated with lower surface temperatures during summer heat waves.','limit'=>4],
], 30);
$ack = microtime(true) - $began;
if (empty($start['ok']) || empty($start['data']['request_id'])) throw new Exception(json_encode($start));
$id = $start['data']['request_id'];
$cursor = 0; $events = []; $polls = [];
do {
    $tick = microtime(true);
    $state = prism_call('system.request_status', ['request_id'=>$id,'after'=>$cursor], 30);
    $polls[] = microtime(true) - $tick;
    if (empty($state['ok'])) throw new Exception(json_encode($state));
    $data = $state['data'];
    $events = array_merge($events, $data['events']);
    $cursor = $data['next_cursor'];
    if (in_array($data['status'], ['done','failed'], true)) break;
    usleep(500000);
} while (microtime(true)-$began < 60);
if (($data['status'] ?? '') !== 'done' || empty($data['result']['ok'])) throw new Exception(json_encode($state));
echo json_encode(['plugin_version'=>PRISM_RESEARCH_VERSION,'request_id'=>$id,
    'ack_seconds'=>$ack,'total_seconds'=>microtime(true)-$began,
    'poll_seconds'=>$polls,'events'=>$events,'status'=>$data['status'],
    'citation_count'=>count($data['result']['data']['entries'] ?? []),
    'posts_written'=>false], JSON_PRETTY_PRINT);
