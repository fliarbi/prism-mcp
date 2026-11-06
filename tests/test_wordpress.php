<?php
// Test the actual PHP proxy without importing or publishing any posts.
define('ABSPATH', '/tmp/');
function plugin_dir_path($x) { return dirname($x) . '/'; }
function plugin_dir_url($x) { return 'http://example.org/'; }
function add_action(...$x) {}
function add_shortcode(...$x) {}
function get_option(...$x) { return []; }
function wp_json_encode($x) { return json_encode($x); }
function is_wp_error($x) { return false; }
function wp_remote_retrieve_body($x) { return $x['body']; }
function wp_remote_retrieve_response_code($x) { return 200; }
function wp_remote_post($url, $args) {
    $GLOBALS['last_request'] = [$url, $args];
    return ['body' => '{"ok":true,"data":{}}'];
}
require __DIR__ . '/../wordpress/wp-content/plugins/prism-research/prism-research.php';
function check($v, $message) { if (!$v) throw new Exception($message); }
prism_call('system.status', []);
check($GLOBALS['last_request'][1]['body'] === '{}', 'empty arguments must be an object');
prism_call('research.citations', ['claim'=>'A claim','limit'=>4], 30);
check(json_decode($GLOBALS['last_request'][1]['body'], true)['limit'] === 4, 'argument types preserved');
check($GLOBALS['last_request'][1]['timeout'] === 30, 'timeout forwarded');
check(prism_call('not.allowed', [])['ok'] === false, 'allowlist retained');
prism_call('system.request', ['feature'=>'compose.sections','args'=>[]], 30);
check(str_contains($GLOBALS['last_request'][1]['body'], '"args":{}'), 'nested empty arguments must be an object');
check(prism_call('system.request', ['feature'=>'system.status','args'=>[]])['ok'] === false, 'nested system calls rejected');
check(prism_call('system.request', ['feature'=>'not.allowed','args'=>[]])['ok'] === false, 'nested allowlist retained');
echo "PASS: PHP proxy empty-object encoding, arguments, timeout and allowlist\n";
