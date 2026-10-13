# NGINX — batch 3: nginx-008..010 (easy), nginx-017..019 (medium), nginx-025..026 (hard)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

N_HTTPS = ("NGINX — Configuring HTTPS servers", "https://nginx.org/en/docs/http/configuring_https_servers.html")
N_SSL = ("NGINX — ngx_http_ssl_module", "https://nginx.org/en/docs/http/ngx_http_ssl_module.html")
N_REWRITE = ("NGINX — ngx_http_rewrite_module (return)", "https://nginx.org/en/docs/http/ngx_http_rewrite_module.html")
N_GZIP = ("NGINX — ngx_http_gzip_module", "https://nginx.org/en/docs/http/ngx_http_gzip_module.html")
N_GZIP_STATIC = ("NGINX — ngx_http_gzip_static_module", "https://nginx.org/en/docs/http/ngx_http_gzip_static_module.html")
N_LOG = ("NGINX — ngx_http_log_module", "https://nginx.org/en/docs/http/ngx_http_log_module.html")
N_UPSTREAM = ("NGINX — ngx_http_upstream_module", "https://nginx.org/en/docs/http/ngx_http_upstream_module.html")
N_LIMIT_REQ = ("NGINX — ngx_http_limit_req_module", "https://nginx.org/en/docs/http/ngx_http_limit_req_module.html")
N_LIMIT_CONN = ("NGINX — ngx_http_limit_conn_module", "https://nginx.org/en/docs/http/ngx_http_limit_conn_module.html")
N_LB = ("NGINX — Using nginx as HTTP load balancer", "https://nginx.org/en/docs/http/load_balancing.html")
N_PROXY = ("NGINX — ngx_http_proxy_module", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html")
N_HTTP_CORE = ("NGINX — ngx_http_core_module", "https://nginx.org/en/docs/http/ngx_http_core_module.html")
N_CHANGES = ("NGINX — Changes (changelog)", "https://nginx.org/en/CHANGES")
NODE_HTTP = ("Node.js — http (server timeouts)", "https://nodejs.org/api/http.html")
NODE_STREAM = ("Node.js — Stream (pipeline)", "https://nodejs.org/api/stream.html")
MDN_HSTS = ("MDN — Strict-Transport-Security", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security")

QUESTIONS = [
    # ------------------------------------------------------------------ nginx-008
    Q(
        id="nginx-008", sub="HTTP and HTTPS", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["https", "lets-encrypt", "certbot", "redirect", "tls"],
        ver="NGINX 1.30 stable / 1.31 mainline (`http2 on;` since 1.25.1)", vs=True, status="stable",
        q_en=r"""How do you set up HTTPS on NGINX with a free Let's Encrypt certificate, redirect all HTTP traffic to HTTPS, and make sure the certificate keeps renewing?""",
        q_bn=r"""ফ্রি Let's Encrypt certificate দিয়ে NGINX-এ HTTPS কীভাবে set up করবে, সব HTTP traffic HTTPS-এ redirect করবে, আর certificate যেন নিয়মিত renew হতে থাকে সেটা কীভাবে নিশ্চিত করবে?""",
        a_en=r"""
            1. Point the domain's DNS (A/AAAA records) at the server and make sure port 80 and 443 are open.
            2. Run **certbot** with the NGINX plugin: `sudo certbot --nginx -d example.com -d www.example.com`. It proves domain control with the ACME **HTTP-01** challenge over port 80, gets the certificate and adds the TLS directives to the server block.
            3. The final config has a **port-443 server** with `listen 443 ssl;`, `http2 on;`, `ssl_certificate` (`fullchain.pem`) and `ssl_certificate_key` (`privkey.pem`), plus a **port-80 server** that does `return 301 https://$host$request_uri;`.
            4. **Renewal:** certbot installs a systemd timer (or cron job) that runs `certbot renew` regularly and renews certificates nearing expiry. NGINX must reload to pick up a new certificate, which the NGINX plugin handles; with other methods use `--deploy-hook "systemctl reload nginx"`. Verify with `certbot renew --dry-run`.

            Once HTTPS works everywhere, add HSTS so browsers stop trying plain HTTP.
        """,
        a_bn=r"""
            1. Domain-এর DNS (A/AAAA record) server-এর দিকে point করাও, আর নিশ্চিত করো port 80 আর 443 খোলা।
            2. NGINX plugin-সহ **certbot** চালাও: `sudo certbot --nginx -d example.com -d www.example.com`। এটা port 80-এর মাধ্যমে ACME **HTTP-01** challenge দিয়ে domain-এর নিয়ন্ত্রণ প্রমাণ করে, certificate নেয়, আর server block-এ TLS directive যোগ করে দেয়।
            3. শেষে config-এ থাকে একটা **port-443 server**: `listen 443 ssl;`, `http2 on;`, `ssl_certificate` (`fullchain.pem`) আর `ssl_certificate_key` (`privkey.pem`)। সাথে একটা **port-80 server**, যেটা `return 301 https://$host$request_uri;` করে।
            4. **Renewal:** certbot একটা systemd timer (বা cron job) install করে, যেটা নিয়মিত `certbot renew` চালায় আর মেয়াদ শেষ হয়ে আসা certificate renew করে। নতুন certificate নিতে NGINX-কে reload করতে হয়; NGINX plugin সেটা নিজেই করে, অন্য পদ্ধতিতে `--deploy-hook "systemctl reload nginx"` ব্যবহার করো। `certbot renew --dry-run` দিয়ে যাচাই করো।

            সব জায়গায় HTTPS ঠিকঠাক চললে HSTS যোগ করো, যাতে browser আর সাধারণ HTTP চেষ্টাই না করে।
        """,
        ex_en=r"""
            - **Use `fullchain.pem`, not `cert.pem`.** Without the intermediate certificate, some clients (older Android, some HTTP libraries) fail with "unable to verify" even though desktop browsers work.
            - **Keep port 80 reachable:** HTTP-01 renewals need it. The redirect server is fine, because certbot handles the challenge path.
            - **301 vs 308:** browsers follow 301 for GETs. For APIs where clients might POST to `http://`, a 308 preserves the method and body.
            - **Automation is mandatory:** Let's Encrypt certificates are short-lived (90 days), and CA/Browser Forum rules are shrinking maximum certificate lifetimes industry-wide (down to 47 days by 2029). Manual renewal won't scale.
            - **HTTP/2 syntax:** `http2 on;` is the current way. The old `listen 443 ssl http2;` parameter has been deprecated since 1.25.1.
        """,
        ex_bn=r"""
            - **`cert.pem` না, `fullchain.pem` ব্যবহার করো।** Intermediate certificate না থাকলে desktop browser-এ কাজ করলেও কিছু client (পুরনো Android, কিছু HTTP library) "unable to verify" দিয়ে fail করে।
            - **Port 80 খোলা রাখো:** HTTP-01 renewal-এর জন্য এটা লাগে। Redirect server থাকলেও সমস্যা নেই, কারণ challenge path certbot সামলায়।
            - **301 বনাম 308:** GET-এর জন্য browser 301 মেনে চলে। যেসব API-তে client `http://`-এ POST করতে পারে, সেখানে 308 method আর body অক্ষত রাখে।
            - **Automation বাধ্যতামূলক:** Let's Encrypt certificate স্বল্পমেয়াদি (৯০ দিন), আর CA/Browser Forum-এর নিয়মে পুরো industry-তে certificate-এর সর্বোচ্চ মেয়াদ কমছে (২০২৯ সালের মধ্যে ৪৭ দিন)। হাতে করে renew করা টেকসই না।
            - **HTTP/2 syntax:** বর্তমান উপায় হলো `http2 on;`। পুরনো `listen 443 ssl http2;` parameter 1.25.1 থেকে deprecated।
        """,
        tip_en=r"""Walk through it as a checklist (DNS → certificate → config → redirect → renewal → HSTS) and mention testing renewal with `--dry-run`. Interviewers like candidates who think about day 90, not just day 1.""",
        tip_bn=r"""একটা checklist ধরে এগোও (DNS → certificate → config → redirect → renewal → HSTS), আর `--dry-run` দিয়ে renewal test করার কথা বলো। যারা শুধু প্রথম দিন না, ৯০তম দিনের কথাও ভাবে, interviewer তাদের পছন্দ করে।""",
        mist_en=r"""Using `cert.pem` instead of `fullchain.pem`, blocking port 80 after setup (renewals fail silently), forgetting to reload NGINX after renewal, and enabling HSTS `preload` before every subdomain supports HTTPS.""",
        mist_bn=r"""`fullchain.pem`-এর বদলে `cert.pem` ব্যবহার করা, setup-এর পর port 80 বন্ধ করে দেওয়া (renewal চুপচাপ fail করে), renewal-এর পর NGINX reload করতে ভুলে যাওয়া, আর সব subdomain HTTPS support করার আগেই HSTS `preload` চালু করা।""",
        code=r"""
            server {
                listen 80;
                listen [::]:80;
                server_name example.com www.example.com;
                return 301 https://$host$request_uri;
            }

            server {
                listen 443 ssl;
                listen [::]:443 ssl;
                http2 on;
                server_name example.com www.example.com;

                ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
                ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

                add_header Strict-Transport-Security "max-age=31536000" always;

                location / {
                    proxy_pass http://127.0.0.1:3000;
                    proxy_set_header Host $host;
                    proxy_set_header X-Forwarded-Proto $scheme;
                }
            }
        """,
        lang="nginx",
        extra=[
            dict(lang="bash", label_en="Obtain and verify renewal", label_bn="Certificate নেওয়া আর renewal যাচাই", src=r"""
                sudo certbot --nginx -d example.com -d www.example.com
                sudo certbot renew --dry-run
                systemctl list-timers | grep certbot
            """),
        ],
        follow=[
            ("What is HSTS, and what's the risk of the `preload` flag?", "HSTS কী, আর `preload` flag-এর ঝুঁকি কী?"),
            ("How would you get a wildcard certificate, and why does that need a DNS-01 challenge?", "Wildcard certificate কীভাবে নেবে, আর এর জন্য DNS-01 challenge কেন লাগে?"),
        ],
        refs=[N_HTTPS, N_SSL, MDN_HSTS],
    ),
    # ------------------------------------------------------------------ nginx-009
    Q(
        id="nginx-009", sub="Compression", diff="easy", type="conceptual",
        prio="medium", market="both", mins=3,
        tags=["gzip", "compression", "brotli", "performance", "gzip_types"],
        ver="NGINX 1.30 stable / 1.31 mainline", vs=False, status="stable",
        q_en=r"""How do you enable response compression in NGINX, and which settings matter? What shouldn't be compressed?""",
        q_bn=r"""NGINX-এ response compression কীভাবে চালু করবে, আর কোন setting-গুলো গুরুত্বপূর্ণ? কোন জিনিস compress করা উচিত না?""",
        a_en=r"""
            Enable the built-in gzip module with `gzip on;` and tune a few directives:

            - **`gzip_types`:** only `text/html` is compressed by default, so add CSS, JavaScript, JSON, SVG, XML and plain text.
            - **`gzip_comp_level`:** the default is 1. Levels around 4–6 give most of the size savings without burning much CPU.
            - **`gzip_min_length`:** skip tiny responses (e.g. under 1 KB) where headers dominate.
            - **`gzip_vary on`:** adds `Vary: Accept-Encoding` so caches store compressed and uncompressed copies separately.
            - **`gzip_proxied`:** by default NGINX doesn't compress responses to requests that came through another proxy (those with a `Via` header, like many CDNs). Set it to `any` if the CDN expects compressed responses from the origin.

            **Don't compress** formats that are already compressed (JPEG, PNG, WebP, MP4, ZIP, WOFF2). It costs CPU and saves nothing. Text-based JSON API responses are the big win: often 70–90% smaller.
        """,
        a_bn=r"""
            Built-in gzip module চালু করো `gzip on;` দিয়ে, আর কয়েকটা directive tune করো:

            - **`gzip_types`:** default হিসেবে শুধু `text/html` compress হয়, তাই CSS, JavaScript, JSON, SVG, XML আর plain text যোগ করো।
            - **`gzip_comp_level`:** default হলো 1। মোটামুটি 4–6 level-এ বেশি CPU খরচ না করেই size-এর বেশিরভাগ সাশ্রয় পাওয়া যায়।
            - **`gzip_min_length`:** খুব ছোট response (যেমন 1 KB-এর কম) বাদ দাও, সেখানে header-ই বেশি জায়গা নেয়।
            - **`gzip_vary on`:** `Vary: Accept-Encoding` যোগ করে, যাতে cache compressed আর uncompressed copy আলাদাভাবে রাখে।
            - **`gzip_proxied`:** default হিসেবে NGINX অন্য proxy দিয়ে আসা request-এর (যেগুলোতে `Via` header থাকে, যেমন অনেক CDN) response compress করে না। CDN origin থেকে compressed response আশা করলে এটা `any` করো।

            **Compress কোরো না** আগে থেকেই compressed format (JPEG, PNG, WebP, MP4, ZIP, WOFF2)। এতে CPU খরচ হয়, কিন্তু কিছুই বাঁচে না। Text-ভিত্তিক JSON API response-এ লাভ সবচেয়ে বেশি: প্রায়ই ৭০–৯০% ছোট হয়।
        """,
        ex_en=r"""
            - **Brotli** usually compresses text better than gzip, but it isn't part of stock NGINX. It needs the third-party `ngx_brotli` module, or you can let the CDN do Brotli at the edge.
            - **Pre-compression:** with `gzip_static on;`, NGINX serves `app.js.gz` if it exists next to `app.js`, so you compress once at build time at maximum level with zero runtime CPU. The module is included in the official nginx.org packages.
            - **Don't double-compress:** if NGINX compresses, drop Express's `compression()` middleware (or vice versa), so Node isn't wasting CPU on work NGINX redoes.
            - **Security:** compressing HTTPS responses that mix secrets (CSRF tokens) with attacker-reflected input is the basis of the BREACH attack. Mitigate with per-request token masking rather than disabling compression everywhere.
        """,
        ex_bn=r"""
            - **Brotli** সাধারণত gzip-এর চেয়ে text ভালো compress করে, কিন্তু এটা সাধারণ NGINX-এর অংশ না। এর জন্য third-party `ngx_brotli` module লাগে, অথবা CDN-কে edge-এ Brotli করতে দাও।
            - **আগে থেকে compress করা:** `gzip_static on;` দিলে `app.js`-এর পাশে `app.js.gz` থাকলে NGINX সেটাই serve করে। এতে build-এর সময় একবার সর্বোচ্চ level-এ compress করে runtime-এ শূন্য CPU খরচ। Module-টা official nginx.org package-এ আছে।
            - **দুবার compress কোরো না:** NGINX compress করলে Express-এর `compression()` middleware বাদ দাও (বা উল্টোটা), যাতে NGINX যে কাজ আবার করবে তাতে Node CPU নষ্ট না করে।
            - **Security:** secret (CSRF token) আর attacker-এর reflect করা input মেশানো HTTPS response compress করাই BREACH attack-এর ভিত্তি। সব জায়গায় compression বন্ধ না করে প্রতি request-এ token masking দিয়ে এটা ঠেকাও।
        """,
        tip_en=r"""Mention that `gzip_types` defaults to HTML only. It's the most common reason people "enable gzip" and their JSON stays uncompressed. Verify with `curl -H 'Accept-Encoding: gzip' -I`.""",
        tip_bn=r"""বলো যে `gzip_types`-এর default শুধু HTML। মানুষ "gzip চালু" করার পরেও JSON uncompressed থেকে যাওয়ার সবচেয়ে সাধারণ কারণ এটাই। `curl -H 'Accept-Encoding: gzip' -I` দিয়ে যাচাই করো।""",
        mist_en=r"""Adding `image/jpeg` or `image/png` to `gzip_types`, setting `gzip_comp_level 9` on busy servers, and forgetting `gzip_vary`.""",
        mist_bn=r"""`gzip_types`-এ `image/jpeg` বা `image/png` যোগ করা, ব্যস্ত server-এ `gzip_comp_level 9` দেওয়া, আর `gzip_vary` ভুলে যাওয়া।""",
        code=r"""
            http {
                gzip on;
                gzip_comp_level 5;
                gzip_min_length 1024;
                gzip_vary on;
                gzip_proxied any;
                gzip_types
                    text/css text/plain text/xml
                    application/javascript application/json application/xml
                    image/svg+xml;
                # text/html is always compressed when gzip is on

                # Serve pre-compressed build files (app.js.gz) when they exist
                gzip_static on;
            }
        """,
        lang="nginx",
        extra=[
            dict(lang="bash", label_en="Verify", label_bn="যাচাই", src=r"""
                curl -s -o /dev/null -D - -H 'Accept-Encoding: gzip' https://api.example.com/products \
                  | grep -i -E 'content-encoding|vary'
                # content-encoding: gzip
                # vary: Accept-Encoding
            """),
        ],
        follow=[
            ("Should compression happen in NGINX, in Node.js, or at the CDN? Why?", "Compression NGINX-এ, Node.js-এ, নাকি CDN-এ হওয়া উচিত? কেন?"),
            ("What is the BREACH attack, in one sentence?", "এক বাক্যে বলো, BREACH attack কী?"),
        ],
        refs=[N_GZIP, N_GZIP_STATIC],
    ),
    # ------------------------------------------------------------------ nginx-010
    Q(
        id="nginx-010", sub="Logging", diff="easy", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["access-log", "log_format", "upstream_response_time", "latency"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""Users report that checkout is slow, so you add this log format. Which variable tells you how long the Node.js backend took to respond, excluding the time NGINX spent talking to a slow client?""",
        q_bn=r"""User-রা বলছে checkout ধীর, তাই তুমি এই log format যোগ করলে। কোন variable বলবে Node.js backend উত্তর দিতে কত সময় নিয়েছে, ধীর client-এর সাথে NGINX-এর কাটানো সময় বাদ দিয়ে?""",
        code=r"""
            log_format timing '$remote_addr "$request" $status $body_bytes_sent '
                              'rt=$request_time uct=$upstream_connect_time '
                              'uht=$upstream_header_time urt=$upstream_response_time';

            access_log /var/log/nginx/access.log timing;
        """,
        lang="nginx",
        options=[
            ("`$request_time`", "`$request_time`"),
            ("`$upstream_connect_time`", "`$upstream_connect_time`"),
            ("`$msec`", "`$msec`"),
            ("`$upstream_response_time`", "`$upstream_response_time`"),
        ],
        correct=3,
        a_en=r"""`$upstream_response_time` is the time from when NGINX started connecting to the upstream until it received the whole response from it, so it measures the backend. `$request_time` covers the whole request from the client's first byte to the last byte sent to the client, so it also includes slow client networks.""",
        a_bn=r"""`$upstream_response_time` হলো upstream-এর সাথে NGINX connect শুরু করা থেকে পুরো response পাওয়া পর্যন্ত সময়, তাই এটা backend-কে মাপে। `$request_time` পুরো request ধরে মাপে, client-এর প্রথম byte থেকে client-কে পাঠানো শেষ byte পর্যন্ত, তাই এতে ধীর client network-এর সময়ও থাকে।""",
        ex_en=r"""
            The tempting wrong answer is `$request_time`, the total time. Comparing the two is the actual diagnostic:
            - `rt` high but `urt` low → the backend was fast; the client's network (e.g. a weak mobile connection) or a large download is slow.
            - `urt` high → the backend is slow. Then `uht` (`$upstream_header_time`, time to the first byte) tells you whether the delay is before the response starts (slow query) or during the body (large or streamed response).
            - `uct` high → connection problems to the upstream (overload, SYN backlog, or TLS to the upstream).

            All values are in seconds with millisecond resolution. When NGINX retried several upstream servers, the variables contain comma-separated values, one per attempt. `log_format` must be defined in the `http` context.
        """,
        ex_bn=r"""
            বিভ্রান্তিকর ভুল উত্তর হলো `$request_time`, অর্থাৎ মোট সময়। আসল diagnosis হলো দুটো তুলনা করা:
            - `rt` বেশি কিন্তু `urt` কম → backend দ্রুত ছিল; client-এর network (যেমন দুর্বল mobile connection) বা বড় download ধীর।
            - `urt` বেশি → backend ধীর। তখন `uht` (`$upstream_header_time`, প্রথম byte পর্যন্ত সময়) বলে দেয় দেরিটা response শুরুর আগে (ধীর query) নাকি body পাঠানোর সময় (বড় বা streamed response)।
            - `uct` বেশি → upstream-এ connection-এর সমস্যা (overload, SYN backlog, বা upstream-এ TLS)।

            সব value second-এ, millisecond resolution-সহ। NGINX একাধিক upstream server-এ retry করলে variable-গুলোতে comma দিয়ে আলাদা করা একাধিক value থাকে, প্রতিটা চেষ্টার জন্য একটা। `log_format` define করতে হয় `http` context-এ।
        """,
        tip_en=r"""Don't just name the variable. Explain how comparing `$request_time` with `$upstream_response_time` separates network problems from backend problems. That's the real-world skill.""",
        tip_bn=r"""শুধু variable-এর নাম বোলো না। ব্যাখ্যা করো `$request_time` আর `$upstream_response_time` তুলনা করে কীভাবে network-এর সমস্যা আর backend-এর সমস্যা আলাদা করা যায়। বাস্তবে আসল দক্ষতা এটাই।""",
        related=["nginx-003"],
        refs=[N_LOG, N_UPSTREAM],
    ),
    # ------------------------------------------------------------------ nginx-017
    Q(
        id="nginx-017", sub="Rate Limiting", diff="medium", type="security-performance",
        prio="high", market="both", mins=7,
        tags=["limit_req", "rate-limiting", "brute-force", "429", "burst"],
        ver="NGINX 1.30 stable / 1.31 mainline", vs=False, status="stable",
        q_en=r"""How would you protect a Node.js API with NGINX rate limiting: a general limit for `/api/` and a much stricter one for the login endpoint? Explain `rate`, `burst`, `nodelay` and the status code clients receive.""",
        q_bn=r"""NGINX rate limiting দিয়ে একটা Node.js API কীভাবে সুরক্ষিত রাখবে: `/api/`-এর জন্য একটা সাধারণ limit, আর login endpoint-এর জন্য অনেক কড়া একটা limit? `rate`, `burst`, `nodelay` ব্যাখ্যা করো, আর client কোন status code পায় সেটাও বলো।""",
        a_en=r"""
            NGINX's `limit_req` module implements a **leaky bucket** per key.

            - **`limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;`** (in `http`) keys on the client IP (the compact binary form) and stores counters in a 10 MB shared-memory zone. `10r/s` means one request every 100 ms on average.
            - **`limit_req zone=api burst=20 nodelay;`** (in a location) allows up to 20 requests above the rate to be accepted instead of rejected.
            - **Without `nodelay`**, the excess requests are queued and delayed to match the rate, which adds latency.
            - **With `nodelay`**, they're served immediately, but the burst slots refill only at the configured rate. Anything beyond the burst is rejected.
            - **Status code:** rejected requests get **503** by default. Set `limit_req_status 429;` so clients and monitoring see the correct "Too Many Requests".

            For login, use a separate zone such as `rate=5r/m` with a small burst. That slows brute-force and credential-stuffing attempts without affecting normal browsing. Add `limit_conn` if you also need to cap concurrent connections, for example for downloads.
        """,
        a_bn=r"""
            NGINX-এর `limit_req` module প্রতিটা key-র জন্য একটা **leaky bucket** implement করে।

            - **`limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;`** (`http`-এ) client IP-কে (compact binary রূপে) key হিসেবে নেয়, আর counter রাখে 10 MB-এর একটা shared-memory zone-এ। `10r/s` মানে গড়ে প্রতি 100 ms-এ একটা request।
            - **`limit_req zone=api burst=20 nodelay;`** (location-এ) rate-এর উপরে সর্বোচ্চ ২০টা request reject না করে গ্রহণ করতে দেয়।
            - **`nodelay` না থাকলে** বাড়তি request-গুলো queue-তে রেখে দেরি করানো হয়, যাতে rate মেলে। এতে latency বাড়ে।
            - **`nodelay` থাকলে** সেগুলো সাথে সাথে serve হয়, কিন্তু burst-এর slot আবার খালি হয় শুধু নির্ধারিত rate-এ। Burst-এর বাইরে গেলে reject।
            - **Status code:** reject হওয়া request default হিসেবে **503** পায়। `limit_req_status 429;` set করো, যাতে client আর monitoring সঠিক "Too Many Requests" দেখে।

            Login-এর জন্য আলাদা zone রাখো, যেমন `rate=5r/m` আর ছোট burst। এতে সাধারণ browsing-এ প্রভাব না ফেলে brute-force আর credential-stuffing-এর চেষ্টা ধীর হয়ে যায়। একসাথে কতগুলো connection থাকবে সেটাও সীমিত করতে চাইলে (যেমন download-এর জন্য) `limit_conn` যোগ করো।
        """,
        ex_en=r"""
            - **Real client IP first:** behind a CDN or load balancer, `$binary_remote_addr` is the proxy's IP, and one limit then applies to everyone. Configure the `realip` module before rate limiting.
            - **Shared IPs:** mobile carriers and offices often put many users behind one IP (CGNAT). Keep per-IP limits generous and add per-user or per-API-key limits in the app (e.g. Redis-backed) for authenticated traffic.
            - **Per-instance counters:** each NGINX server counts separately. With three NGINX nodes, the effective limit is roughly three times higher. For a strict global limit, enforce it centrally.
            - **Rolling out safely:** `limit_req_dry_run on;` logs what **would** be rejected without blocking, which is good for tuning. `delay=N` (instead of `nodelay`) gives two-stage limiting: the first N excess requests go through immediately, then the rest are delayed.
            - **Memory:** the docs estimate about 8,000 states per MB for 128-byte states, so a 10 MB zone tracks tens of thousands of IPs. When the zone is full, NGINX evicts old states, and if it still can't create one, the request is rejected.
        """,
        ex_bn=r"""
            - **আগে আসল client IP:** CDN বা load balancer-এর পেছনে `$binary_remote_addr` হলো proxy-র IP, তখন একটা limit-ই সবার উপর প্রযোজ্য হয়। Rate limiting-এর আগে `realip` module configure করো।
            - **Shared IP:** mobile carrier আর অফিস প্রায়ই অনেক user-কে একটা IP-র পেছনে রাখে (CGNAT)। Per-IP limit উদার রাখো, আর authenticated traffic-এর জন্য app-এ per-user বা per-API-key limit যোগ করো (যেমন Redis দিয়ে)।
            - **প্রতিটা instance-এর আলাদা counter:** প্রতিটা NGINX server আলাদাভাবে গোনে। তিনটা NGINX node থাকলে কার্যকর limit মোটামুটি তিন গুণ। কড়া global limit লাগলে কেন্দ্রীয়ভাবে প্রয়োগ করো।
            - **নিরাপদে চালু করা:** `limit_req_dry_run on;` block না করে শুধু log করে কোনগুলো reject **হতো**, tuning-এর জন্য ভালো। `nodelay`-এর বদলে `delay=N` দিলে দুই ধাপের limiting হয়: প্রথম Nটা বাড়তি request সাথে সাথে যায়, বাকিগুলো দেরি করে।
            - **Memory:** docs অনুযায়ী 128-byte state হলে প্রতি MB-তে প্রায় ৮,০০০ state থাকে, তাই 10 MB zone কয়েক দশ হাজার IP track করতে পারে। Zone ভরে গেলে NGINX পুরনো state সরিয়ে দেয়, তাতেও নতুন state বানাতে না পারলে request reject হয়।
        """,
        tip_en=r"""Explain `burst` vs `nodelay` with a concrete timeline ("21 requests in the same millisecond → 21 served, the 22nd rejected; then one slot frees every 100 ms"). Then raise CDN real-IP and CGNAT issues. That's the depth interviewers look for.""",
        tip_bn=r"""একটা নির্দিষ্ট timeline দিয়ে `burst` বনাম `nodelay` ব্যাখ্যা করো ("একই millisecond-এ ২১টা request → ২১টা serve, ২২তমটা reject; তারপর প্রতি 100 ms-এ একটা slot খালি হয়")। তারপর CDN-এর real IP আর CGNAT-এর সমস্যা তোলো। Interviewer ঠিক এই গভীরতাই খোঁজে।""",
        mist_en=r"""Leaving the default 503 (which looks like an outage in monitoring), rate-limiting on the CDN's IP, and using `burst` without `nodelay` on APIs and then wondering why latency jumped.""",
        mist_bn=r"""Default 503 রেখে দেওয়া (monitoring-এ এটাকে outage মনে হয়), CDN-এর IP ধরে rate-limit করা, আর API-তে `nodelay` ছাড়া `burst` দিয়ে তারপর অবাক হওয়া যে latency কেন বেড়ে গেল।""",
        code=r"""
            http {
                limit_req_zone $binary_remote_addr zone=api:10m   rate=10r/s;
                limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
                limit_req_status 429;
                limit_req_log_level warn;

                upstream app { server 127.0.0.1:3000; }

                server {
                    listen 443 ssl;
                    http2 on;
                    server_name api.example.com;

                    location /api/ {
                        limit_req zone=api burst=20 nodelay;
                        proxy_pass http://app;
                    }

                    # exact match wins over the /api/ prefix
                    location = /api/auth/login {
                        limit_req zone=login burst=5;
                        proxy_pass http://app;
                    }
                }
            }
        """,
        lang="nginx",
        follow=[
            ("How would you rate-limit per API key instead of per IP?", "Per IP-র বদলে per API key কীভাবে rate-limit করবে?"),
            ("Why should a rate-limited API return 429 with a `Retry-After` header?", "Rate-limit করা API কেন `Retry-After` header-সহ 429 ফেরত দেবে?"),
        ],
        related=["nginx-004"],
        refs=[N_LIMIT_REQ, N_LIMIT_CONN],
    ),
    # ------------------------------------------------------------------ nginx-018
    Q(
        id="nginx-018", sub="Load Balancing", diff="medium", type="conceptual",
        prio="high", market="both", mins=6,
        tags=["upstream", "load-balancing", "least_conn", "max_fails", "health-checks"],
        ver="NGINX 1.30 stable / 1.31 mainline (open-source `sticky` since 1.29.6; `least_time` since 1.31.0)", vs=True, status="stable",
        q_en=r"""How does NGINX load-balance across several Node.js instances? Explain the main algorithms, weights and backup servers, and how open-source NGINX detects and avoids a failed backend.""",
        q_bn=r"""NGINX কীভাবে কয়েকটা Node.js instance-এর মধ্যে load balance করে? প্রধান algorithm, weight আর backup server ব্যাখ্যা করো, আর open-source NGINX কীভাবে fail করা backend চিনে ফেলে ও এড়িয়ে চলে সেটাও বলো।""",
        a_en=r"""
            You list the backends in an `upstream` block and `proxy_pass` to it.

            **Methods:**
            - **Round-robin (default, weighted):** each server in turn, proportional to `weight`.
            - **`least_conn`:** send to the server with the fewest active connections. Good when request durations vary a lot, such as reports mixed with fast reads.
            - **`ip_hash`:** the same client IP goes to the same server, a simple form of stickiness. For IPv4 it hashes only the first three octets.
            - **`hash $key consistent`:** e.g. `$request_uri` for cache locality. `consistent` (ketama) remaps only a few keys when servers are added or removed.
            - **`random two least_conn`:** pick two at random, then choose the less loaded one.
            - **Recent versions:** `sticky cookie` session affinity has been available in open source since 1.29.6 (so in 1.30 stable). `least_time` came to open source in the 1.31 mainline.

            **Weights and roles:** `weight=3` sends three times more traffic; `backup` is used only when the primaries are unavailable (not compatible with hash methods); `down` takes a server out of rotation.

            **Failure detection in open source is passive:** if a server has `max_fails` failed attempts (default 1) within `fail_timeout` (default 10s), it's marked unavailable for `fail_timeout`. What counts as a failure is defined by `proxy_next_upstream` (default: `error timeout`). The failed request is retried on the next server if that's still safe. **Active** health checks (periodic probes with `health_check`) are an NGINX Plus feature.
        """,
        a_bn=r"""
            Backend-গুলো একটা `upstream` block-এ তালিকা করো, আর তাতে `proxy_pass` করো।

            **পদ্ধতি:**
            - **Round-robin (default, weighted):** পালাক্রমে প্রতিটা server-এ, `weight` অনুপাতে।
            - **`least_conn`:** যে server-এ সবচেয়ে কম active connection, সেখানে পাঠাও। Request-এর সময় অনেক কম-বেশি হলে ভালো, যেমন দ্রুত read-এর সাথে মেশানো report।
            - **`ip_hash`:** একই client IP একই server-এ যায়, stickiness-এর একটা সহজ রূপ। IPv4-এর ক্ষেত্রে শুধু প্রথম তিনটা octet hash করে।
            - **`hash $key consistent`:** যেমন cache locality-র জন্য `$request_uri`। `consistent` (ketama) server যোগ বা বাদ দিলে অল্প কয়েকটা key-কেই নতুন জায়গায় পাঠায়।
            - **`random two least_conn`:** random-ভাবে দুটো বেছে নিয়ে তার মধ্যে কম ব্যস্তটা।
            - **সাম্প্রতিক version:** `sticky cookie` session affinity open source-এ 1.29.6 থেকে পাওয়া যায় (অর্থাৎ 1.30 stable-এ আছে)। `least_time` open source-এ এসেছে 1.31 mainline-এ।

            **Weight আর ভূমিকা:** `weight=3` তিন গুণ বেশি traffic পাঠায়; `backup` শুধু primary-রা unavailable হলে ব্যবহার হয় (hash method-এর সাথে চলে না); `down` server-কে rotation থেকে সরিয়ে রাখে।

            **Open source-এ failure ধরা হয় passive-ভাবে:** `fail_timeout`-এর (default 10s) মধ্যে কোনো server-এ `max_fails` (default 1) বার চেষ্টা fail করলে সেটা `fail_timeout` সময়ের জন্য unavailable চিহ্নিত হয়। কোনটা failure ধরা হবে তা ঠিক করে `proxy_next_upstream` (default: `error timeout`)। নিরাপদ হলে fail করা request পরের server-এ retry হয়। **Active** health check (`health_check` দিয়ে নিয়মিত probe) NGINX Plus-এর feature।
        """,
        ex_en=r"""
            - **Passive means users find the failures.** The first request to a dead server fails (and is retried if possible) before the server is marked down. Keep `proxy_connect_timeout` short (a few seconds) so a dead host is detected quickly instead of hanging for the 60 s default.
            - **Retries and idempotency:** since 1.9.13 NGINX doesn't retry non-idempotent requests (POST, PATCH) on the next server once they've been sent, unless you add `non_idempotent`. Don't, unless the endpoint is truly idempotent.
            - **Add `http_502 http_503`** (or `http_500`) to `proxy_next_upstream` if your app returns those during restarts, so NGINX tries another instance.
            - **A single server:** with only one server in the group, `max_fails` is ignored and that server is never marked unavailable.
            - **Open-source "active" checks:** you can get similar behaviour from the orchestration layer (systemd/PM2 restarts, Docker health checks with a deploy script, Kubernetes readiness probes) or a monitoring job that edits the upstream and reloads.
        """,
        ex_bn=r"""
            - **Passive মানে failure-গুলো user-রাই টের পায়।** মৃত server-এ প্রথম request fail করে (সম্ভব হলে retry হয়), তারপর server-টা down চিহ্নিত হয়। `proxy_connect_timeout` ছোট রাখো (কয়েক সেকেন্ড), যাতে মৃত host ৬০ সেকেন্ডের default ধরে ঝুলে না থেকে দ্রুত ধরা পড়ে।
            - **Retry আর idempotency:** 1.9.13 থেকে NGINX non-idempotent request (POST, PATCH) একবার পাঠানোর পর পরের server-এ retry করে না, যদি না তুমি `non_idempotent` যোগ করো। Endpoint সত্যিই idempotent না হলে এটা কোরো না।
            - Restart-এর সময় তোমার app 502/503 দিলে `proxy_next_upstream`-এ **`http_502 http_503`** (বা `http_500`) যোগ করো, যাতে NGINX অন্য instance চেষ্টা করে।
            - **একটা মাত্র server:** group-এ একটাই server থাকলে `max_fails` উপেক্ষা করা হয়, আর সেটা কখনো unavailable চিহ্নিত হয় না।
            - **Open source-এ "active" check:** orchestration layer থেকে (systemd/PM2 restart, deploy script-সহ Docker health check, Kubernetes readiness probe), অথবা upstream edit করে reload করে এমন একটা monitoring job দিয়ে কাছাকাছি আচরণ পাওয়া যায়।
        """,
        tip_en=r"""Separate "how traffic is distributed" (algorithms) from "how failures are handled" (passive checks and retries), and be precise that active health checks are NGINX Plus. Mentioning the recent open-source additions (`sticky`, `least_time`) shows you're current.""",
        tip_bn=r""""Traffic কীভাবে ভাগ হয়" (algorithm) আর "failure কীভাবে সামলানো হয়" (passive check আর retry) আলাদা করে বলো, আর নির্দিষ্ট করে বলো যে active health check NGINX Plus-এর। সাম্প্রতিক open-source সংযোজনের (`sticky`, `least_time`) কথা বললে বোঝা যায় তুমি হালনাগাদ।""",
        mist_en=r"""Claiming open-source NGINX actively probes backends, using `ip_hash` behind a CDN (every client looks like the CDN's IP), and enabling retries for POST requests.""",
        mist_bn=r"""বলা যে open-source NGINX backend-গুলোকে active-ভাবে probe করে, CDN-এর পেছনে `ip_hash` ব্যবহার করা (সব client-কেই CDN-এর IP মনে হয়), আর POST request-এ retry চালু করা।""",
        code=r"""
            upstream api {
                least_conn;
                server 10.0.1.11:3000 weight=3 max_fails=3 fail_timeout=15s;
                server 10.0.1.12:3000           max_fails=3 fail_timeout=15s;
                server 10.0.1.13:3000 backup;      # only when the others are unavailable
            }

            server {
                listen 443 ssl;
                http2 on;
                server_name api.example.com;

                location / {
                    proxy_pass http://api;
                    proxy_connect_timeout 3s;
                    proxy_next_upstream error timeout http_502 http_503;
                    proxy_next_upstream_tries 2;
                }
            }
        """,
        lang="nginx",
        follow=[
            ("When would you choose `least_conn` over round-robin?", "কখন round-robin-এর বদলে `least_conn` বেছে নেবে?"),
            ("Why isn't `ip_hash` a good stickiness mechanism for mobile users?", "Mobile user-দের জন্য `ip_hash` কেন ভালো stickiness ব্যবস্থা না?"),
        ],
        related=["nginx-005"],
        refs=[N_UPSTREAM, N_LB, N_PROXY],
    ),
    # ------------------------------------------------------------------ nginx-019
    Q(
        id="nginx-019", sub="Troubleshooting 502 and 504", diff="medium", type="comparison",
        prio="high", market="both", mins=6,
        tags=["502", "504", "503", "499", "error-log"],
        ver="NGINX 1.30 stable / 1.31 mainline", vs=False, status="stable",
        q_en=r"""Compare NGINX's 502, 503, 504 and 499 status codes. What typically causes each one behind a Node.js app, and where do you look first?""",
        q_bn=r"""NGINX-এর 502, 503, 504 আর 499 status code-এর তুলনা করো। Node.js app-এর পেছনে প্রতিটার সাধারণ কারণ কী, আর তুমি প্রথমে কোথায় খুঁজবে?""",
        a_en=r"""
            - **502 Bad Gateway:** NGINX reached out but **didn't get a valid response**. The causes are connection refused (app down, wrong port, app bound to the wrong interface), a connection reset or upstream closing early (app crash, keep-alive race), upstream response headers too big for NGINX's buffers, or "no live upstreams" (every server marked failed).
            - **504 Gateway Timeout:** the upstream **didn't respond in time**. It's usually `proxy_read_timeout` (60 s default) expiring while waiting for the response, sometimes `proxy_connect_timeout`. Causes include slow queries, a blocked event loop, deadlocks or an overloaded app.
            - **503 Service Unavailable:** often generated **by NGINX itself**. `limit_req`/`limit_conn` rejections return 503 by default, and maintenance pages use it too. It can also come from the app.
            - **499 (NGINX-specific, logs only):** the **client closed the connection** before NGINX could respond. Lots of 499s usually mean the backend is so slow that users or a load balancer give up.

            **Where I look first:** NGINX's **error log**, which states the exact reason (`Connection refused`, `upstream timed out`, `upstream prematurely closed connection`, `upstream sent too big header`). Then the access log with `$upstream_response_time` and `$upstream_addr`, then the app's logs and health.
        """,
        a_bn=r"""
            - **502 Bad Gateway:** NGINX যোগাযোগ করেছে কিন্তু **কোনো বৈধ response পায়নি**। কারণ হতে পারে connection refused (app বন্ধ, ভুল port, app ভুল interface-এ bind করা), connection reset বা upstream আগেভাগে বন্ধ করে দেওয়া (app crash, keep-alive race), NGINX-এর buffer-এর জন্য upstream-এর response header অতিরিক্ত বড়, অথবা "no live upstreams" (সব server fail চিহ্নিত)।
            - **504 Gateway Timeout:** upstream **সময়মতো উত্তর দেয়নি**। সাধারণত response-এর অপেক্ষায় থাকতে থাকতে `proxy_read_timeout` (default ৬০ সেকেন্ড) পার হয়ে যায়, কখনো `proxy_connect_timeout`। কারণ হতে পারে ধীর query, block হয়ে থাকা event loop, deadlock বা overload হওয়া app।
            - **503 Service Unavailable:** প্রায়ই **NGINX নিজেই** তৈরি করে। `limit_req`/`limit_conn` reject করলে default হিসেবে 503 দেয়, maintenance page-ও এটা ব্যবহার করে। App থেকেও আসতে পারে।
            - **499 (NGINX-নির্দিষ্ট, শুধু log-এ):** NGINX উত্তর দেওয়ার আগেই **client connection বন্ধ করে দিয়েছে**। অনেক 499 মানে সাধারণত backend এত ধীর যে user বা load balancer হাল ছেড়ে দিচ্ছে।

            **আমি প্রথমে কোথায় দেখি:** NGINX-এর **error log**, যেখানে সঠিক কারণ লেখা থাকে (`Connection refused`, `upstream timed out`, `upstream prematurely closed connection`, `upstream sent too big header`)। তারপর `$upstream_response_time` আর `$upstream_addr`-সহ access log, তারপর app-এর log আর health।
        """,
        ex_en=r"""
            **Typical fixes:**
            - **502 (refused):** start or fix the app, check the port, and make the app listen on the right interface. In containers that means `0.0.0.0`; on SELinux hosts, allow NGINX network connections.
            - **502 (too big header):** large cookies or JWT headers from the app. Raise `proxy_buffer_size`/`proxy_buffers`, or slim the headers.
            - **502 (intermittent, keep-alive):** Node closed an idle connection that NGINX reused. Make Node's keep-alive timeout longer than the upstream `keepalive_timeout`.
            - **504:** profile the slow endpoint, stream or offload long work to a job queue, and only then raise `proxy_read_timeout` for that specific location.
            - **503 from limits:** tune `limit_req`, and return 429 instead.

            A useful mental model: 502 means "the upstream answered wrongly or not at all", and 504 means "the upstream answered too slowly".
        """,
        ex_bn=r"""
            **সাধারণ সমাধান:**
            - **502 (refused):** app চালু করো বা ঠিক করো, port দেখো, আর app-কে সঠিক interface-এ listen করাও। Container-এ এর মানে `0.0.0.0`; SELinux host-এ NGINX-এর network connection অনুমোদন দাও।
            - **502 (too big header):** app থেকে বড় cookie বা JWT header আসছে। `proxy_buffer_size`/`proxy_buffers` বাড়াও, অথবা header ছোট করো।
            - **502 (মাঝে মাঝে, keep-alive):** NGINX যে idle connection reuse করেছে, Node সেটা বন্ধ করে দিয়েছে। Node-এর keep-alive timeout upstream-এর `keepalive_timeout`-এর চেয়ে বড় রাখো।
            - **504:** ধীর endpoint profile করো, দীর্ঘ কাজ stream করো বা job queue-তে পাঠাও, আর তারপরেই কেবল ওই নির্দিষ্ট location-এর `proxy_read_timeout` বাড়াও।
            - **Limit থেকে 503:** `limit_req` tune করো, আর 503-এর বদলে 429 দাও।

            মনে রাখার সহজ উপায়: 502 মানে "upstream ভুল উত্তর দিয়েছে বা উত্তরই দেয়নি", আর 504 মানে "upstream খুব দেরিতে উত্তর দিয়েছে"।
        """,
        tip_en=r"""Quote the actual error-log messages. Saying "I'd grep the error log for `upstream timed out` vs `Connection refused`" proves hands-on experience far better than textbook definitions.""",
        tip_bn=r"""আসল error log-এর message উদ্ধৃত করো। "আমি error log-এ `upstream timed out` বনাম `Connection refused` grep করব", এটা বললে textbook-এর সংজ্ঞার চেয়ে অনেক ভালোভাবে হাতে-কলমে অভিজ্ঞতা প্রমাণ হয়।""",
        mist_en=r"""Treating every 502 as "increase timeouts", confusing 499 with an NGINX bug, and debugging from the access log alone (it has the status, not the reason).""",
        mist_bn=r"""প্রতিটা 502-কে "timeout বাড়াও" ধরে নেওয়া, 499-কে NGINX-এর bug ভাবা, আর শুধু access log দেখে debug করা (সেখানে status থাকে, কারণ থাকে না)।""",
        code=r"""
            # 502 Bad Gateway
            connect() failed (111: Connection refused) while connecting to upstream
            upstream prematurely closed connection while reading response header from upstream
            upstream sent too big header while reading response header from upstream
            no live upstreams while connecting to upstream

            # 504 Gateway Timeout
            upstream timed out (110: Connection timed out) while reading response header from upstream

            # 503 (NGINX's own rate limiter, default status)
            limiting requests, excess: 20.420 by zone "api", client: 203.0.113.7

            # 499 appears only in the access log: the client gave up first
            203.0.113.7 "GET /api/report HTTP/2.0" 499 0 rt=58.112 urt=-
        """,
        lang="text",
        follow=[
            ("A spike of 499s and 504s appears together. What does that combination suggest?", "একসাথে 499 আর 504-এর spike দেখা দিল। এই সমন্বয় কী ইঙ্গিত দেয়?"),
            ("How would you find which upstream server produced a 502?", "কোন upstream server 502 দিয়েছে কীভাবে খুঁজে বের করবে?"),
        ],
        related=["nginx-010", "nginx-017"],
        refs=[N_PROXY, N_UPSTREAM, N_LOG],
    ),
    # ------------------------------------------------------------------ nginx-025
    Q(
        id="nginx-025", sub="Upstream Servers", diff="hard", type="mcq",
        prio="medium", market="both", mins=4,
        tags=["keepalive", "upstream", "proxy_http_version", "version-change", "performance"],
        ver="NGINX 1.30 stable (behaviour changed in 1.29.7) vs ≤ 1.28", vs=True, status="version-specific",
        q_en=r"""This upstream keepalive setup was written for NGINX 1.24. The servers now run NGINX 1.30 stable. Which statement is correct?""",
        q_bn=r"""এই upstream keepalive setup NGINX 1.24-এর জন্য লেখা হয়েছিল। Server-গুলো এখন NGINX 1.30 stable চালায়। কোন কথাটা সঠিক?""",
        code=r"""
            upstream api {
                server 10.0.1.11:3000;
                server 10.0.1.12:3000;
                keepalive 32;
            }

            server {
                location / {
                    proxy_pass http://api;
                    proxy_http_version 1.1;
                    proxy_set_header Connection "";
                }
            }
        """,
        lang="nginx",
        options=[
            ("Nothing changed: without these lines NGINX 1.30 still uses HTTP/1.0 and opens a new upstream connection for every request",
             "কিছুই বদলায়নি: এই line-গুলো ছাড়া NGINX 1.30 এখনো HTTP/1.0 ব্যবহার করে আর প্রতিটা request-এ নতুন upstream connection খোলে"),
            ("Since 1.29.7, upstream keepalive is on by default (`keepalive 32 local`), `proxy_http_version` defaults to 1.1 and the `Connection` header is no longer sent upstream by default, so these lines are redundant (but harmless)",
             "1.29.7 থেকে upstream keepalive default-এ চালু (`keepalive 32 local`), `proxy_http_version`-এর default 1.1, আর `Connection` header default-এ আর upstream-এ পাঠানো হয় না; তাই এই line-গুলো অপ্রয়োজনীয় (তবে ক্ষতিকর না)"),
            ("In 1.30 keepalive works only with `proxy_http_version 2`, because HTTP/1.1 upstream keepalive was removed",
             "1.30-এ keepalive শুধু `proxy_http_version 2` দিয়ে কাজ করে, কারণ HTTP/1.1 upstream keepalive সরিয়ে দেওয়া হয়েছে"),
            ("The `keepalive` directive was removed in 1.30; connection reuse is controlled only by `keepalive_timeout` in the `http` block",
             "1.30-এ `keepalive` directive সরিয়ে দেওয়া হয়েছে; connection reuse এখন শুধু `http` block-এর `keepalive_timeout` দিয়ে নিয়ন্ত্রিত"),
        ],
        correct=1,
        a_en=r"""The "on by default since 1.29.7" answer is correct. NGINX **1.29.7** (mainline, March 2026, so included in the 1.30 stable branch) changed the defaults. `keepalive` in `upstream` blocks is enabled by default with 32 idle connections per worker (`local`: not shared across locations), `proxy_http_version` defaults to **1.1**, and the `Connection` header is no longer sent to upstreams by default. The three classic lines are still valid and are required on NGINX 1.28 and older, but on 1.30 they're redundant.""",
        a_bn=r""""1.29.7 থেকে default-এ চালু" উত্তরটাই সঠিক। NGINX **1.29.7** (mainline, মার্চ ২০২৬, তাই 1.30 stable branch-এও আছে) default বদলে দিয়েছে। `upstream` block-এ `keepalive` default-এ চালু, প্রতি worker-এ ৩২টা idle connection (`local`: location-গুলোর মধ্যে share হয় না), `proxy_http_version`-এর default **1.1**, আর `Connection` header default-এ আর upstream-এ পাঠানো হয় না। পুরনো তিনটা line এখনো বৈধ, আর NGINX 1.28 বা তার আগের version-এ দরকারি, কিন্তু 1.30-এ অপ্রয়োজনীয়।""",
        ex_en=r"""
            "Nothing changed" is what most blog posts and older interview answers say, which is exactly why it's tempting. It's true for ≤ 1.28 and now outdated. The HTTP/2-only option mixes up a different feature: since 1.29.4, `proxy_http_version 2` **can** proxy to HTTP/2 backends, but HTTP/1.1 keepalive wasn't removed.

            **Why keepalive matters:** without it, every proxied request costs a new TCP (and possibly TLS) handshake to Node, and a busy proxy can exhaust ephemeral ports with sockets in TIME_WAIT.

            **A production gotcha that remains:** Node's `server.keepAliveTimeout` is only a few seconds by default, while NGINX's upstream `keepalive_timeout` defaults to 60s. NGINX can reuse a connection that Node has just closed, which shows up as sporadic 502s ("upstream prematurely closed connection"). Keep NGINX's upstream `keepalive_timeout` below Node's value, or raise Node's `keepAliveTimeout` (and its `headersTimeout`).
        """,
        ex_bn=r"""
            "কিছুই বদলায়নি" হলো বেশিরভাগ blog post আর পুরনো interview উত্তরে যা বলা হয়, ঠিক এজন্যই এটা বিভ্রান্তিকর। ≤ 1.28-এর জন্য এটা সত্য, এখন পুরনো। শুধু-HTTP/2-এর option-টা অন্য একটা feature-এর সাথে গুলিয়ে ফেলে: 1.29.4 থেকে `proxy_http_version 2` দিয়ে HTTP/2 backend-এ proxy **করা যায়**, কিন্তু HTTP/1.1 keepalive সরানো হয়নি।

            **Keepalive কেন গুরুত্বপূর্ণ:** এটা না থাকলে প্রতিটা proxied request-এ Node-এর সাথে নতুন TCP (এবং হয়তো TLS) handshake লাগে, আর ব্যস্ত proxy-তে TIME_WAIT-এ থাকা socket দিয়ে ephemeral port শেষ হয়ে যেতে পারে।

            **একটা production gotcha এখনো রয়ে গেছে:** Node-এর `server.keepAliveTimeout` default-এ মাত্র কয়েক সেকেন্ড, অথচ NGINX-এর upstream `keepalive_timeout`-এর default 60s। Node সদ্য বন্ধ করেছে এমন connection NGINX reuse করতে পারে, যেটা মাঝে মাঝে 502 হিসেবে দেখা দেয় ("upstream prematurely closed connection")। NGINX-এর upstream `keepalive_timeout` Node-এর মানের চেয়ে কম রাখো, অথবা Node-এর `keepAliveTimeout` (আর সাথে `headersTimeout`) বাড়াও।
        """,
        tip_en=r"""If you know about the 1.29.7 change, say so, but also explain the old three-line pattern, since many servers still run distro packages older than 1.29.7. Showing both makes your answer correct on any version.""",
        tip_bn=r"""1.29.7-এর পরিবর্তন জানা থাকলে সেটা বলো, তবে পুরনো তিন-line-এর pattern-টাও ব্যাখ্যা করো, কারণ অনেক server এখনো 1.29.7-এর চেয়ে পুরনো distro package চালায়। দুটোই দেখালে তোমার উত্তর যেকোনো version-এ সঠিক থাকে।""",
        related=["nginx-018", "nginx-005"],
        refs=[N_UPSTREAM, N_PROXY, N_CHANGES],
    ),
    # ------------------------------------------------------------------ nginx-026
    Q(
        id="nginx-026", sub="Timeouts", diff="hard", type="scenario",
        prio="high", market="both", mins=10,
        tags=["504", "proxy_read_timeout", "streaming", "background-jobs", "timeouts"],
        ver="NGINX 1.30 stable / 1.31 mainline, Node.js 24 LTS", vs=False, status="stable",
        q_en=r"""Admins exporting a large sales report (a CSV for the last year) get `504 Gateway Timeout` after exactly 60 seconds. Other endpoints are fine. A teammate proposes adding `proxy_read_timeout 600s;` to the `http` block. How do you analyse and fix this properly?""",
        q_bn=r"""Admin-রা একটা বড় sales report (গত এক বছরের CSV) export করতে গেলে ঠিক ৬০ সেকেন্ড পরে `504 Gateway Timeout` পায়। অন্য endpoint-গুলো ঠিক আছে। একজন teammate প্রস্তাব দিয়েছে `http` block-এ `proxy_read_timeout 600s;` যোগ করার। কীভাবে বিশ্লেষণ করবে আর ঠিকভাবে সমাধান করবে?""",
        a_en=r"""
            **Diagnose:** "exactly 60 seconds" matches `proxy_read_timeout`'s default. The error log will confirm it with `upstream timed out (110: Connection timed out) while reading response header from upstream`. The timeout is measured **between two successive reads**, not over the whole response, so Node sent **nothing** for 60 s. It's building the entire CSV in memory before responding.

            **Why not 600 s globally:** that hides the real problem and makes NGINX hold connections to hung requests for 10 minutes everywhere. During an incident that ties up connections and makes failures slower to detect. Long timeouts belong only where they're justified.

            **Fixes, from quick to best:**
            1. **Scoped timeout (stop-gap):** raise `proxy_read_timeout` only in `location = /api/reports/export`.
            2. **Stream the response:** have Node send the header row immediately and stream rows from a database cursor through a Transform into `res` (`stream.pipeline`). Data flows continuously, each read resets the timer, memory stays flat, and the user sees the download start at once.
            3. **Make it asynchronous (best for heavy reports):** `POST /reports` returns `202 Accepted` with a job ID; a worker (e.g. BullMQ on Redis) generates the file into object storage (S3); the client polls or gets an email or notification with a presigned download URL. No HTTP connection is held open, and retries and progress tracking become possible.
            4. **Make it faster:** add an index for the date range, pre-aggregate, or run the export against a read replica.

            **Check the whole chain:** every hop has its own timeout. A CDN or load balancer in front (AWS ALB's idle timeout defaults to 60 s), Node's `server.requestTimeout` (5 minutes by default in current versions) and database statement timeouts can each cut the request even after NGINX is fixed.
        """,
        a_bn=r"""
            **Diagnose:** "ঠিক ৬০ সেকেন্ড" `proxy_read_timeout`-এর default-এর সাথে মেলে। Error log-এ `upstream timed out (110: Connection timed out) while reading response header from upstream` দিয়ে এটা নিশ্চিত হবে। Timeout মাপা হয় **পরপর দুটো read-এর মাঝে**, পুরো response জুড়ে না, অর্থাৎ Node ৬০ সেকেন্ড ধরে **কিছুই** পাঠায়নি। Response দেওয়ার আগে সে পুরো CSV memory-তে বানাচ্ছে।

            **কেন globally 600 s না:** এতে আসল সমস্যা চাপা পড়ে, আর সব জায়গায় NGINX ঝুলে থাকা request-এর connection ১০ মিনিট ধরে রাখে। Incident-এর সময় এতে connection আটকে থাকে আর failure ধরতে দেরি হয়। দীর্ঘ timeout শুধু যেখানে যুক্তিসঙ্গত সেখানেই থাকা উচিত।

            **সমাধান, দ্রুত থেকে সবচেয়ে ভালো:**
            1. **নির্দিষ্ট location-এ timeout (সাময়িক ব্যবস্থা):** শুধু `location = /api/reports/export`-এ `proxy_read_timeout` বাড়াও।
            2. **Response stream করো:** Node সাথে সাথে header row পাঠাবে, তারপর database cursor থেকে row-গুলো একটা Transform-এর মধ্য দিয়ে `res`-এ stream করবে (`stream.pipeline`)। Data একটানা যায়, প্রতিটা read-এ timer reset হয়, memory স্থির থাকে, আর user সাথে সাথে download শুরু হতে দেখে।
            3. **Asynchronous করো (ভারী report-এর জন্য সবচেয়ে ভালো):** `POST /reports` job ID-সহ `202 Accepted` ফেরত দেয়; একটা worker (যেমন Redis-এর উপর BullMQ) file বানিয়ে object storage-এ (S3) রাখে; client poll করে, অথবা presigned download URL-সহ email বা notification পায়। কোনো HTTP connection খোলা থাকে না, আর retry ও progress tracking সম্ভব হয়।
            4. **দ্রুত করো:** date range-এর জন্য index যোগ করো, pre-aggregate করো, বা export-টা read replica-তে চালাও।

            **পুরো chain দেখো:** প্রতিটা hop-এর নিজস্ব timeout আছে। সামনে থাকা CDN বা load balancer (AWS ALB-এর idle timeout default ৬০ সেকেন্ড), Node-এর `server.requestTimeout` (বর্তমান version-এ default ৫ মিনিট) আর database-এর statement timeout, NGINX ঠিক করার পরেও এদের যেকোনোটা request কেটে দিতে পারে।
        """,
        ex_en=r"""
            - **NGINX timeout family:** `proxy_connect_timeout` (establishing the TCP connection; usually can't exceed 75 s), `proxy_send_timeout` (between two writes of the request to the upstream), `proxy_read_timeout` (between two reads of the response), `send_timeout` (between two writes to the **client**), and `client_body_timeout`/`client_header_timeout` (reading from the client).
            - **Buffering and big downloads:** by default NGINX buffers upstream responses and spills large ones to temp files (up to `proxy_max_temp_file_size`). For true streaming, the app can send `X-Accel-Buffering: no`, or you set `proxy_buffering off` on that location.
            - **User experience:** a spinner that dies at 60 s is worse than an immediate "your report is being prepared". The async pattern improves UX as well as reliability.
            - **Capacity:** each long synchronous request also ties up a database connection from the pool. A few concurrent exports can starve the rest of the API.
        """,
        ex_bn=r"""
            - **NGINX-এর timeout পরিবার:** `proxy_connect_timeout` (TCP connection স্থাপন; সাধারণত ৭৫ সেকেন্ডের বেশি হতে পারে না), `proxy_send_timeout` (upstream-এ request লেখার দুটো write-এর মাঝে), `proxy_read_timeout` (response-এর দুটো read-এর মাঝে), `send_timeout` (**client**-কে দুটো write-এর মাঝে), আর `client_body_timeout`/`client_header_timeout` (client থেকে পড়ার সময়)।
            - **Buffering আর বড় download:** default হিসেবে NGINX upstream response buffer করে, আর বড় হলে temp file-এ লেখে (`proxy_max_temp_file_size` পর্যন্ত)। সত্যিকারের streaming-এর জন্য app `X-Accel-Buffering: no` পাঠাতে পারে, অথবা ওই location-এ `proxy_buffering off` set করো।
            - **User experience:** ৬০ সেকেন্ডে থেমে যাওয়া spinner-এর চেয়ে সাথে সাথে "তোমার report তৈরি হচ্ছে" দেখানো ভালো। Async pattern reliability-র সাথে UX-ও উন্নত করে।
            - **Capacity:** প্রতিটা দীর্ঘ synchronous request pool থেকে একটা database connection-ও আটকে রাখে। একসাথে কয়েকটা export চললে বাকি API connection-এর অভাবে ভুগতে পারে।
        """,
        tip_en=r"""Push back politely on the global timeout first: "it treats the symptom". Then offer a ladder of fixes (scoped timeout → streaming → async job). Mentioning that `proxy_read_timeout` is **between reads** shows precise understanding.""",
        tip_bn=r"""আগে ভদ্রভাবে global timeout-এর আপত্তি জানাও: "এটা শুধু লক্ষণের চিকিৎসা"। তারপর ধাপে ধাপে সমাধান দাও (নির্দিষ্ট location-এ timeout → streaming → async job)। `proxy_read_timeout` যে **দুটো read-এর মাঝের** সময়, এটা বললে সূক্ষ্ম বোঝাপড়া প্রকাশ পায়।""",
        mist_en=r"""Raising every timeout globally, building huge CSVs in memory, and fixing NGINX but forgetting the load balancer or CDN timeout in front of it.""",
        mist_bn=r"""সব timeout globally বাড়িয়ে দেওয়া, বিশাল CSV memory-তে বানানো, আর NGINX ঠিক করে সামনে থাকা load balancer বা CDN-এর timeout ভুলে যাওয়া।""",
        code=r"""
            # Scoped stop-gap: only the export endpoint gets a longer read timeout
            location = /api/reports/export {
                proxy_pass http://app;
                proxy_read_timeout 300s;
                proxy_buffering off;          # stream rows to the client as they arrive
            }
        """,
        lang="nginx",
        extra=[
            dict(lang="javascript", label_en="Node.js: stream the CSV from a database cursor (Express 5, pg + pg-query-stream)", label_bn="Node.js: database cursor থেকে CSV stream করা (Express 5, pg + pg-query-stream)", src=r"""
                import { pipeline } from 'node:stream/promises';
                import { Transform } from 'node:stream';
                import QueryStream from 'pg-query-stream';

                app.get('/api/reports/export', async (req, res) => {
                  const client = await pool.connect();
                  try {
                    res.setHeader('Content-Type', 'text/csv; charset=utf-8');
                    res.setHeader('Content-Disposition', 'attachment; filename="sales.csv"');
                    res.write('id,total,created_at\n');          // first bytes leave immediately

                    const rows = client.query(new QueryStream(
                      'SELECT id, total, created_at FROM orders WHERE created_at >= $1 ORDER BY id',
                      [req.query.since ?? '2025-10-01'],
                    ));
                    const toCsv = new Transform({
                      objectMode: true,
                      transform(row, _enc, cb) {
                        cb(null, `${row.id},${row.total},${row.created_at.toISOString()}\n`);
                      },
                    });
                    await pipeline(rows, toCsv, res);              // backpressure-aware, flat memory
                  } finally {
                    client.release();
                  }
                });
            """),
        ],
        follow=[
            ("How would you design the asynchronous export flow end to end?", "Asynchronous export flow শুরু থেকে শেষ পর্যন্ত কীভাবে design করবে?"),
            ("Why does a long global `proxy_read_timeout` make incidents worse?", "দীর্ঘ global `proxy_read_timeout` কেন incident-কে আরও খারাপ করে?"),
        ],
        related=["nginx-019", "nginx-010"],
        refs=[N_PROXY, NODE_STREAM, NODE_HTTP],
    ),
]

if __name__ == "__main__":
    save("nginx", "b3", QUESTIONS)
