<?php
/**
 * Plugin Name: Prism Research
 * Description: Research-grade writing inside WordPress, powered by Fliar BI Prism — evidence for a claim, an audit of a draft, sections ranked by evidence, charts, and whole articles built from the papers and news on a subject.
 * Version: 0.1.4
 * Author: Fliar BI
 * Requires at least: 6.4
 * Requires PHP: 8.1
 * Text Domain: prism-research
 */
if (!defined('ABSPATH')) exit;

define('PRISM_RESEARCH_VERSION', '0.1.4');
define('PRISM_RESEARCH_DIR', plugin_dir_path(__FILE__));
define('PRISM_RESEARCH_URL', plugin_dir_url(__FILE__));

/* ───────────────────────── settings ───────────────────────── */
function prism_settings(): array {
    $d = ['base_url' => 'http://host.docker.internal:8790', 'timeout' => 120, 'default_status' => 'draft'];
    $s = get_option('prism_research_settings', []);
    return array_merge($d, is_array($s) ? $s : []);
}

add_action('admin_init', function () {
    register_setting('prism_research', 'prism_research_settings', [
        'type' => 'array',
        'sanitize_callback' => function ($in) {
            return [
                'base_url' => rtrim(esc_url_raw($in['base_url'] ?? ''), '/'),
                'timeout' => max(30, (int)($in['timeout'] ?? 120)),
                'default_status' => in_array($in['default_status'] ?? 'draft', ['draft', 'pending', 'publish'], true) ? $in['default_status'] : 'draft',
            ];
        },
    ]);
});

/* ───────────────────────── the Prism client ───────────────────────── */
/** Every feature the plugin may call. A browser cannot ask for anything else. */
const PRISM_ALLOWED = [
    'research.evidence', 'research.counter_evidence', 'research.statistics', 'research.audit',
    'research.citations', 'research.evidence_card', 'research.browse',
    'compose.continue', 'compose.sections', 'compose.section', 'compose.titles', 'compose.chart',
    'compose.quick_story', 'compose.article',
    'news.trends', 'news.recent', 'news.critical', 'news.overview', 'news.resolve',
    'system.job', 'system.jobs', 'system.status', 'system.resolve',
    'system.request', 'system.request_status',
];

function prism_call(string $feature, array $args, ?int $timeout = null): array {
    if (!in_array($feature, PRISM_ALLOWED, true)) {
        return ['ok' => false, 'error' => ['kind' => 'forbidden', 'reason' => "feature not allowed: $feature"]];
    }
    if ($feature === 'system.request') {
        $nested = $args['feature'] ?? '';
        if (!in_array($nested, PRISM_ALLOWED, true) || str_starts_with($nested, 'system.') || in_array($nested, ['compose.article', 'compose.chart', 'compose.quick_story'], true) || !is_array($args['args'] ?? null)) {
            return ['ok' => false, 'error' => ['kind' => 'forbidden', 'reason' => 'This request is not allowed.']];
        }
        $args['args'] = (object)$args['args'];
    }
    $s = prism_settings();
    $url = $s['base_url'] . '/v1/' . rawurlencode($feature);
    $r = wp_remote_post($url, [
        'timeout' => $timeout ?? (int)$s['timeout'],
        'headers' => ['Content-Type' => 'application/json', 'User-Agent' => 'prism-research-wp/' . PRISM_RESEARCH_VERSION],
        // PHP encodes an empty array as []; the API requires a JSON object.
        'body' => wp_json_encode((object)$args),
    ]);
    if (is_wp_error($r)) {
        return ['ok' => false, 'error' => ['kind' => 'transport', 'reason' => $r->get_error_message()]];
    }
    $body = json_decode(wp_remote_retrieve_body($r), true);
    if (!is_array($body)) {
        return ['ok' => false, 'error' => ['kind' => 'bad_response', 'reason' => 'Prism returned no JSON', 'status' => wp_remote_retrieve_response_code($r)]];
    }
    return $body;
}

/* ───────────────────────── REST proxy for the editor ───────────────────────── */
add_action('rest_api_init', function () {
    register_rest_route('prism/v1', '/call', [
        'methods' => 'POST',
        'permission_callback' => fn() => current_user_can('edit_posts'),
        'callback' => function (WP_REST_Request $req) {
            $feature = (string)$req->get_param('feature');
            $args = $req->get_param('args');
            $args = is_array($args) ? $args : [];
            $timeout = min(300, max(30, (int)($req->get_param('timeout') ?: 120)));
            return rest_ensure_response(prism_call($feature, $args, $timeout));
        },
    ]);
    register_rest_route('prism/v1', '/import', [
        'methods' => 'POST',
        'permission_callback' => fn() => current_user_can('edit_posts'),
        'callback' => 'prism_import_article',
    ]);
});

/** Turn a finished quick_story result into a post: the HTML as content, the hero as featured image, the checks as meta. */
function prism_import_article(WP_REST_Request $req) {
    $a = $req->get_json_params();
    $title = sanitize_text_field($a['title'] ?? 'Untitled');
    $html = (string)($a['html'] ?? '');
    if ($html === '' && !empty($a['markdown'])) $html = prism_md_to_html((string)$a['markdown']);
    $status = prism_settings()['default_status'];
    $post_id = wp_insert_post([
        'post_title' => $title,
        'post_content' => wp_kses_post($html),
        'post_status' => $status,
        'post_type' => 'post',
        'post_author' => get_current_user_id(),
    ], true);
    if (is_wp_error($post_id)) return new WP_Error('insert_failed', $post_id->get_error_message(), ['status' => 500]);
    update_post_meta($post_id, '_prism_subject', sanitize_text_field($a['subject'] ?? ''));
    update_post_meta($post_id, '_prism_checks', wp_json_encode($a['checks'] ?? []));
    update_post_meta($post_id, '_prism_reader', wp_json_encode($a['reader_rounds'] ?? []));
    update_post_meta($post_id, '_prism_papers', wp_json_encode($a['papers'] ?? []));
    update_post_meta($post_id, '_prism_publishable', !empty($a['publishable']) ? '1' : '0');
    $featured = null;
    foreach ((array)($a['images'] ?? []) as $img) {
        if (!empty($img['url']) && (($img['where'] ?? 'hero') === 'hero')) { $featured = $img['url']; break; }
    }
    if (!$featured && !empty($a['images'][0]['url'])) $featured = $a['images'][0]['url'];
    if ($featured) {
        // the hero becomes the featured image; the theme shows it above the title, so it must not also open the body
        $stripped = preg_replace('#<figure class="wp-block-image">\s*<img src="' . preg_quote($featured, '#') . '"[^>]*/?>\s*</figure>\s*#', '', $html, 1);
        if ($stripped !== null && $stripped !== $html) wp_update_post(['ID' => $post_id, 'post_content' => wp_kses_post($stripped)]);
        require_once ABSPATH . 'wp-admin/includes/media.php';
        require_once ABSPATH . 'wp-admin/includes/file.php';
        require_once ABSPATH . 'wp-admin/includes/image.php';
        $att = media_sideload_image($featured, $post_id, $title, 'id');
        if (!is_wp_error($att)) set_post_thumbnail($post_id, $att);
    }
    return rest_ensure_response(['ok' => true, 'post_id' => $post_id, 'edit_url' => get_edit_post_link($post_id, 'raw'), 'view_url' => get_permalink($post_id), 'status' => $status]);
}

/** Minimal markdown for the fallback path. Prism normally sends HTML. */
function prism_md_to_html(string $md): string {
    $out = []; $para = [];
    $flush = function () use (&$out, &$para) { if ($para) { $out[] = '<p>' . prism_inline(implode(' ', $para)) . '</p>'; $para = []; } };
    foreach (explode("\n", $md) as $line) {
        $l = rtrim($line);
        if (preg_match('/^\s*!\[([^\]]*)\]\((https?:[^)]+)\)\s*$/', $l, $m)) { $flush(); $out[] = '<figure class="wp-block-image"><img src="' . esc_url($m[2]) . '" alt="' . esc_attr($m[1]) . '"/></figure>'; continue; }
        if (preg_match('/^(#{1,6})\s+(.*)$/', $l, $m)) { $flush(); if (strlen($m[1]) === 1) continue; $lvl = min(strlen($m[1]), 4); $out[] = "<h$lvl>" . esc_html($m[2]) . "</h$lvl>"; continue; }
        if (trim($l) === '') { $flush(); continue; }
        $para[] = $l;
    }
    $flush();
    return implode("\n", $out);
}
function prism_inline(string $t): string {
    $t = esc_html($t);
    $t = preg_replace('/\*\*(.+?)\*\*/', '<strong>$1</strong>', $t);
    $t = preg_replace('/(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)/', '<em>$1</em>', $t);
    return preg_replace('/\[([^\]]+)\]\((https?:[^)]+)\)/', '<a href="$2" rel="noopener">$1</a>', $t);
}

/* ───────────────────────── admin menu ───────────────────────── */
add_action('admin_menu', function () {
    add_menu_page('Prism Research', 'Prism', 'edit_posts', 'prism-research', 'prism_page_new_article', 'dashicons-analytics', 26);
    add_submenu_page('prism-research', 'New article', 'New article', 'edit_posts', 'prism-research', 'prism_page_new_article');
    add_submenu_page('prism-research', 'Jobs', 'Jobs', 'edit_posts', 'prism-research-jobs', 'prism_page_jobs');
    add_submenu_page('prism-research', 'Settings', 'Settings', 'manage_options', 'prism-research-settings', 'prism_page_settings');
});

add_action('admin_enqueue_scripts', function ($hook) {
    $on_prism = str_contains((string)$hook, 'prism-research');
    $on_editor = in_array($hook, ['post.php', 'post-new.php'], true);
    if (!$on_prism && !$on_editor) return;
    wp_enqueue_style('prism-research', PRISM_RESEARCH_URL . 'assets/admin.css', [], PRISM_RESEARCH_VERSION);
    wp_enqueue_script('prism-research', PRISM_RESEARCH_URL . 'assets/admin.js', ['wp-api-fetch'], PRISM_RESEARCH_VERSION, true);
    wp_localize_script('prism-research', 'PRISM', [
        'rest' => esc_url_raw(rest_url('prism/v1/')),
        'nonce' => wp_create_nonce('wp_rest'),
        'editor' => $on_editor,
        'adminUrl' => admin_url(),
    ]);
});

function prism_page_new_article() { ?>
    <div class="wrap prism-wrap">
        <h1>Prism · New article</h1>
        <p class="prism-lede">Give Prism a subject. It shortlists the dozen papers most about it, reads each abstract against a fixed checklist, finds the recent news, plans a story, writes it, draws two illustrations and two charts, and sends the draft to a cold reader until it reads. Every figure is verified against its source before you see it. About four to seven minutes.</p>
        <form id="prism-new-article" onsubmit="return false">
            <table class="form-table" role="presentation">
                <tr><th scope="row"><label for="prism-subject">Subject</label></th>
                    <td><input type="text" id="prism-subject" class="regular-text" placeholder="e.g. electric vehicle charging infrastructure in India" required>
                        <p class="description">One subject, the way a reader would say it. A place at the end ("in India") scopes the news.</p></td></tr>
                <tr><th scope="row"><label for="prism-k">Papers to read</label></th>
                    <td><input type="number" id="prism-k" value="12" min="6" max="24" class="small-text"></td></tr>
            </table>
            <p><button class="button button-primary button-hero" id="prism-start">Build the article</button></p>
        </form>
        <div id="prism-progress" hidden>
            <div class="prism-bar"><div class="prism-bar-fill" id="prism-bar-fill"></div></div>
            <p id="prism-progress-label" class="prism-mono">queued…</p>
        </div>
        <div id="prism-result" hidden></div>
    </div>
<?php }

function prism_page_jobs() { ?>
    <div class="wrap prism-wrap">
        <h1>Prism · Jobs</h1>
        <p class="prism-lede">Background work Prism has done for this site, newest first.</p>
        <div id="prism-jobs" data-autoload="1">loading…</div>
    </div>
<?php }

function prism_page_settings() {
    $s = prism_settings(); ?>
    <div class="wrap prism-wrap">
        <h1>Prism · Settings</h1>
        <form method="post" action="options.php">
            <?php settings_fields('prism_research'); ?>
            <table class="form-table" role="presentation">
                <tr><th scope="row"><label>Prism API base URL</label></th>
                    <td><input type="url" name="prism_research_settings[base_url]" value="<?php echo esc_attr($s['base_url']); ?>" class="regular-text">
                        <p class="description">The Prism HTTP server, e.g. <code>http://host.docker.internal:8790</code> from Docker or <code>https://prism.yourhost</code> in production. Never exposed to the browser.</p></td></tr>
                <tr><th scope="row"><label>Timeout (seconds)</label></th>
                    <td><input type="number" name="prism_research_settings[timeout]" value="<?php echo (int)$s['timeout']; ?>" class="small-text" min="30" max="300"></td></tr>
                <tr><th scope="row"><label>Imported articles are saved as</label></th>
                    <td><select name="prism_research_settings[default_status]">
                        <?php foreach (['draft' => 'Draft', 'pending' => 'Pending review', 'publish' => 'Published'] as $k => $v) printf('<option value="%s"%s>%s</option>', $k, selected($s['default_status'], $k, false), $v); ?>
                    </select></td></tr>
            </table>
            <?php submit_button(); ?>
        </form>
        <h2>Connection</h2>
        <div id="prism-status" data-autoload="1">checking…</div>
    </div>
<?php }

/* ───────────────────────── the editor meta box ───────────────────────── */
add_action('add_meta_boxes', function () {
    foreach (['post', 'page'] as $t) {
        add_meta_box('prism-research-box', 'Prism Research', 'prism_meta_box', $t, 'normal', 'high');
    }
});
function prism_meta_box($post) {
    $checks = get_post_meta($post->ID, '_prism_checks', true);
    $reader = get_post_meta($post->ID, '_prism_reader', true); ?>
    <div class="prism-box" id="prism-box">
        <?php if ($checks): ?>
        <details class="prism-provenance"><summary>This draft was built by Prism — checks and reader rounds</summary>
            <pre class="prism-mono"><?php echo esc_html(wp_json_encode(json_decode($checks), JSON_PRETTY_PRINT)); ?></pre>
            <pre class="prism-mono"><?php echo esc_html(wp_json_encode(json_decode($reader), JSON_PRETTY_PRINT)); ?></pre>
        </details>
        <?php endif; ?>
        <div class="prism-row">
            <label for="prism-claim">Claim or topic</label>
            <textarea id="prism-claim" rows="2" placeholder="Select text in the editor and press “Use selection”, or type a claim: “Coffee lowers the risk of heart disease.”"></textarea>
            <div class="prism-actions">
                <button type="button" class="button" data-prism="selection">Use selection</button>
                <button type="button" class="button button-primary" data-prism="research.evidence">Find evidence</button>
                <button type="button" class="button" data-prism="research.counter_evidence">What disagrees</button>
                <button type="button" class="button" data-prism="research.statistics">Numbers I can use</button>
                <button type="button" class="button" data-prism="research.citations">Find citations</button>
                <button type="button" class="button" data-prism="compose.sections">Suggest sections</button>
                <button type="button" class="button" data-prism="compose.continue">Continue my paragraph</button>
                <button type="button" class="button" data-prism="research.audit">Audit the whole draft</button>
                <button type="button" class="button" data-prism="news.trends">News trend</button>
            </div>
            <div class="prism-actions prism-chart-row">
                <select id="prism-chart-card">
                    <option value="stance">Chart: how the research leans</option>
                    <option value="verdicts">Chart: what the papers said about this claim</option>
                    <option value="season">Chart: when the news covers it</option>
                    <option value="growth">Chart: what is rising inside it</option>
                </select>
                <button type="button" class="button" data-prism="compose.chart">Make chart</button>
            </div>
        </div>
        <div id="prism-out" class="prism-out" aria-live="polite"></div>
    </div>
<?php }

/* ───────────────────────── shortcodes ───────────────────────── */
add_shortcode('prism_chart', function ($atts) {
    $a = shortcode_atts(['topic' => '', 'card' => 'stance', 'kind' => 'bars'], $atts);
    if (!$a['topic']) return '';
    $key = 'prism_chart_' . md5(wp_json_encode($a));
    $html = get_transient($key);
    if ($html === false) {
        $r = prism_call('compose.chart', ['topic' => $a['topic'], 'card' => $a['card'], 'kind' => $a['kind']], 240);
        $d = $r['data'] ?? [];
        $html = !empty($d['embed_html']) ? $d['embed_html'] : (!empty($d['url']) ? '<figure class="wp-block-image"><img src="' . esc_url($d['url']) . '" alt="" loading="lazy"/></figure>' : '');
        set_transient($key, $html, DAY_IN_SECONDS);
    }
    return $html;
});
add_shortcode('prism_trend', function ($atts) {
    $a = shortcode_atts(['term' => '', 'granularity' => 'quarterly', 'since' => '2024-01-01'], $atts);
    if (!$a['term']) return '';
    $key = 'prism_trend_' . md5(wp_json_encode($a));
    $html = get_transient($key);
    if ($html === false) {
        $r = prism_call('news.trends', ['term' => $a['term'], 'granularity' => $a['granularity'], 'since' => $a['since']], 120);
        $pts = $r['data']['points'] ?? [];
        $rows = '';
        foreach ($pts as $p) $rows .= sprintf('<tr><td>%s</td><td>%s</td><td>%s%%</td></tr>', esc_html(substr($p['period'] ?? '', 0, 7)), number_format_i18n((int)($p['articles'] ?? 0)), esc_html($p['critical_pct'] ?? ''));
        $html = $rows ? '<figure class="wp-block-table prism-trend"><table><thead><tr><th>period</th><th>articles</th><th>critical</th></tr></thead><tbody>' . $rows . '</tbody></table><figcaption>News mentioning “' . esc_html($a['term']) . '”, measured by Fliar BI Prism.</figcaption></figure>' : '';
        set_transient($key, $html, 6 * HOUR_IN_SECONDS);
    }
    return $html;
});
