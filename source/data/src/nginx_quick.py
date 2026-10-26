# NGINX — quick-recall questions: nginx-q01..q10 (see docs/AUTHORING.md §8a)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

N_BEGIN = ("NGINX — Beginner's Guide", "https://nginx.org/en/docs/beginners_guide.html")
N_LB = ("NGINX — Using nginx as HTTP load balancer", "https://nginx.org/en/docs/http/load_balancing.html")
N_HTTP_CORE = ("NGINX — ngx_http_core_module", "https://nginx.org/en/docs/http/ngx_http_core_module.html")
N_REWRITE = ("NGINX — ngx_http_rewrite_module", "https://nginx.org/en/docs/http/ngx_http_rewrite_module.html")
N_SERVER_NAMES = ("NGINX — Server names", "https://nginx.org/en/docs/http/server_names.html")
N_CONTROL = ("NGINX — Controlling nginx", "https://nginx.org/en/docs/control.html")
N_LOG = ("NGINX — ngx_http_log_module", "https://nginx.org/en/docs/http/ngx_http_log_module.html")
N_PROXY = ("NGINX — ngx_http_proxy_module", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html")

QUESTIONS = [
    # ------------------------------------------------------------------ nginx-q01
    Q(
        id="nginx-q01", sub="Web Server Fundamentals", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["nginx", "web-server", "reverse-proxy", "basics"],
        ver="Version-independent concept (NGINX 1.30 stable / 1.31 mainline)", vs=False, status="stable",
        q_en=r"""What is NGINX, and what is it used for?""",
        q_bn=r"""NGINX কী, আর এটা কী কাজে ব্যবহার হয়?""",
        a_en=r"""NGINX is an event-driven web server that is mostly used as a **reverse proxy** in front of apps. It serves static files, terminates HTTPS, load-balances across backends, compresses and caches responses, and applies limits like rate limiting and maximum body size.""",
        a_bn=r"""NGINX হলো একটা event-driven web server, যেটা বেশিরভাগ সময় app-এর সামনে **reverse proxy** হিসেবে ব্যবহার হয়। এটা static file serve করে, HTTPS terminate করে, একাধিক backend-এ load balance করে, response compress ও cache করে, আর rate limit বা maximum body size-এর মতো সীমা বসায়।""",
        code=r"""
            server {
                listen 80;
                server_name example.com;
                location / {
                    proxy_pass http://127.0.0.1:3000;   # forward to the Node.js app
                }
            }
        """, lang="nginx",
        ex_en=r"""A few worker processes, each running an event loop, handle thousands of connections without a thread per connection, which is why it copes well with many slow clients.""",
        ex_bn=r"""কয়েকটা worker process, প্রত্যেকটা একটা event loop চালিয়ে, connection-প্রতি thread ছাড়াই হাজার হাজার connection সামলায়; এজন্যই অনেক slow client থাকলেও এটা ভালো চলে।""",
        tip_en=r"""Answer "web server and reverse proxy", then list three concrete jobs it does in front of your app.""",
        tip_bn=r"""বলো "web server আর reverse proxy", তারপর তোমার app-এর সামনে এটা কী কী করে তার তিনটা নির্দিষ্ট কাজ বলো।""",
        follow=[("Why put NGINX in front of Node.js instead of exposing Node directly?", "Node সরাসরি expose না করে সামনে NGINX কেন রাখা হয়?")],
        related=["nginx-001", "nginx-002"],
        refs=[N_BEGIN],
    ),
    # ------------------------------------------------------------------ nginx-q02
    Q(
        id="nginx-q02", sub="Reverse Proxy", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["reverse-proxy", "forward-proxy"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""Forward proxy vs reverse proxy: whom does each one represent?""",
        q_bn=r"""Forward proxy বনাম reverse proxy: কোনটা কার প্রতিনিধিত্ব করে?""",
        a_en=r"""A **forward proxy** represents clients: the client is configured to use it, and websites see the proxy instead of the user. A **reverse proxy** represents servers: clients talk to it as if it were the site, and it forwards requests to hidden backends. NGINX in front of an app is a reverse proxy.""",
        a_bn=r"""**Forward proxy** client-দের প্রতিনিধিত্ব করে: client নিজে এটা ব্যবহারের জন্য configure করা থাকে, আর website user-এর বদলে proxy-কে দেখে। **Reverse proxy** server-দের প্রতিনিধিত্ব করে: client এটাকেই আসল site ভেবে কথা বলে, আর এটা লুকানো backend-এ request পাঠায়। App-এর সামনে থাকা NGINX হলো reverse proxy।""",
        ex_en=r"""An office or school web proxy is a forward proxy; NGINX, a load balancer or a CDN in front of your servers is a reverse proxy.""",
        ex_bn=r"""অফিস বা স্কুলের web proxy হলো forward proxy; তোমার server-এর সামনে NGINX, load balancer বা CDN হলো reverse proxy।""",
        tip_en=r"""Use "forward hides the client, reverse hides the server" and give one example of each.""",
        tip_bn=r"""বলো "forward client-কে লুকায়, reverse server-কে লুকায়", তারপর দুটোরই একটা করে উদাহরণ দাও।""",
        follow=[("What does a reverse proxy give a Node.js app?", "Reverse proxy একটা Node.js app-কে কী সুবিধা দেয়?")],
        related=["nginx-002"],
        refs=[N_PROXY],
    ),
    # ------------------------------------------------------------------ nginx-q03
    Q(
        id="nginx-q03", sub="Load Balancing", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["load-balancing", "upstream", "round-robin"],
        ver="NGINX 1.30 stable / 1.31 mainline", vs=False, status="stable",
        q_en=r"""How do you load-balance several Node.js instances with NGINX?""",
        q_bn=r"""NGINX দিয়ে কয়েকটা Node.js instance-এ কীভাবে load balance করবে?""",
        a_en=r"""List the instances in an `upstream` block and `proxy_pass` to its name. The default is round-robin (weighted by `weight`); add `least_conn` to prefer the least busy server, or `ip_hash` to keep a client on the same server.""",
        a_bn=r"""Instance-গুলো একটা `upstream` block-এ লেখো, আর তার নামে `proxy_pass` করো। Default হলো round-robin (`weight` অনুযায়ী); সবচেয়ে কম ব্যস্ত server-কে বেছে নিতে `least_conn`, আর একই client-কে একই server-এ রাখতে `ip_hash` দাও।""",
        code=r"""
            upstream api {
                least_conn;              # optional; default is round-robin
                server 127.0.0.1:3001;
                server 127.0.0.1:3002;
            }
            server {
                listen 80;
                location / { proxy_pass http://api; }
            }
        """, lang="nginx",
        ex_en=r"""Open-source NGINX detects failed servers passively (`max_fails`/`fail_timeout`) and skips them for a while; active health checks are an NGINX Plus feature.""",
        ex_bn=r"""Open-source NGINX fail করা server passive-ভাবে ধরে (`max_fails`/`fail_timeout`) আর কিছুক্ষণ বাদ দেয়; active health check NGINX Plus-এর feature।""",
        tip_en=r"""Write the five-line `upstream` block from memory and name the default algorithm.""",
        tip_bn=r"""পাঁচ লাইনের `upstream` block-টা মুখস্থ লিখে দেখাও, আর default algorithm-এর নাম বলো।""",
        follow=[("When would you use `ip_hash` or sticky sessions?", "কখন `ip_hash` বা sticky session ব্যবহার করবে?")],
        related=["nginx-011", "nginx-018"],
        refs=[N_LB],
    ),
    # ------------------------------------------------------------------ nginx-q04
    Q(
        id="nginx-q04", sub="Static File Serving", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["static-files", "root", "try_files"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""How does NGINX serve static files?""",
        q_bn=r"""NGINX কীভাবে static file serve করে?""",
        a_en=r"""You set `root` to a folder, and NGINX maps each request to `root` + the request URI, then sends the file straight from disk. `try_files $uri =404;` serves the file if it exists and returns 404 otherwise, and `index` picks the default file for a directory.""",
        a_bn=r"""`root`-এ একটা folder দাও, আর NGINX প্রতিটা request-কে `root` + request URI-তে map করে সরাসরি disk থেকে file পাঠায়। `try_files $uri =404;` file থাকলে serve করে, না থাকলে 404 দেয়, আর `index` directory-র জন্য default file ঠিক করে।""",
        code=r"""
            server {
                listen 80;
                root /var/www/site;          # GET /css/app.css -> /var/www/site/css/app.css
                index index.html;
                location / {
                    try_files $uri =404;
                }
            }
        """, lang="nginx",
        ex_en=r"""`root` appends the whole URI, while `alias` replaces the matched location prefix; mixing them up is the classic "file exists but 404" bug.""",
        ex_bn=r"""`root` পুরো URI যোগ করে, আর `alias` match হওয়া location prefix-টা replace করে; এই দুটো গুলিয়ে ফেলাই "file আছে কিন্তু 404" bug-এর চিরচেনা কারণ।""",
        tip_en=r"""Explain the `root + URI` rule with one concrete path; that shows you can debug a 404.""",
        tip_bn=r"""একটা নির্দিষ্ট path দিয়ে `root + URI` নিয়মটা বোঝাও; এতে বোঝা যায় তুমি 404 debug করতে পারো।""",
        follow=[("What is the difference between `root` and `alias`?", "`root` আর `alias`-এর পার্থক্য কী?")],
        related=["nginx-014", "nginx-020"],
        refs=[N_HTTP_CORE],
    ),
    # ------------------------------------------------------------------ nginx-q05
    Q(
        id="nginx-q05", sub="SPA Fallback", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["spa", "try_files", "react", "routing"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""What does `try_files $uri $uri/ /index.html;` do, and why do React/Vue SPAs need it?""",
        q_bn=r"""`try_files $uri $uri/ /index.html;` কী করে, আর React/Vue SPA-তে এটা কেন লাগে?""",
        a_en=r"""NGINX tries the exact file, then a directory, and otherwise internally serves `/index.html`. SPA routes like `/dashboard` exist only in client-side JavaScript, so without it a page refresh or a shared link returns 404 instead of booting the app.""",
        a_bn=r"""NGINX আগে ঠিক ওই file খোঁজে, তারপর directory, আর কিছু না পেলে ভেতরে ভেতরে `/index.html` serve করে। `/dashboard`-এর মতো SPA route শুধু client-side JavaScript-এ থাকে, তাই এটা না দিলে page refresh বা shared link-এ app চালু না হয়ে 404 আসে।""",
        code=r"""
            location / {
                try_files $uri $uri/ /index.html;
            }
            location /assets/ {
                try_files $uri =404;    # missing JS/CSS should still be a real 404
            }
        """, lang="nginx",
        ex_en=r"""Keep a plain 404 for asset folders and proxy `/api/` separately; otherwise a missing chunk gets HTML back and fails with a confusing "Unexpected token '<'".""",
        ex_bn=r"""Asset folder-এর জন্য সাধারণ 404 রাখো আর `/api/` আলাদা করে proxy করো; না হলে হারানো chunk-এর বদলে HTML আসে, আর বিভ্রান্তিকর "Unexpected token '<'" error হয়।""",
        tip_en=r"""Explain it through the refresh scenario: clicking works, refreshing 404s, and this line fixes it.""",
        tip_bn=r"""Refresh-এর ঘটনা দিয়ে বোঝাও: click করলে চলে, refresh করলে 404, আর এই line সেটা ঠিক করে।""",
        follow=[("Why shouldn't missing `.js` files fall back to `index.html`?", "হারানো `.js` file কেন `index.html`-এ fallback করা উচিত না?")],
        related=["nginx-006"],
        refs=[N_HTTP_CORE],
    ),
    # ------------------------------------------------------------------ nginx-q06
    Q(
        id="nginx-q06", sub="HTTP and HTTPS", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["redirect", "return", "301", "https", "rewrite"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""How do you redirect HTTP to HTTPS (or `www` to the bare domain) in NGINX?""",
        q_bn=r"""NGINX-এ HTTP থেকে HTTPS-এ (বা `www` থেকে মূল domain-এ) কীভাবে redirect করবে?""",
        a_en=r"""Use a small `server` block with `return 301 https://example.com$request_uri;`, which keeps the path and query string. `return` is simpler and faster than `rewrite`; use 301 for permanent moves and 302 (or 307/308) for temporary ones.""",
        a_bn=r"""একটা ছোট `server` block-এ `return 301 https://example.com$request_uri;` দাও; এতে path আর query string ঠিক থাকে। `rewrite`-এর চেয়ে `return` সহজ আর দ্রুত; স্থায়ী পরিবর্তনে 301, আর অস্থায়ী হলে 302 (বা 307/308) ব্যবহার করো।""",
        code=r"""
            server {                          # all HTTP -> HTTPS
                listen 80;
                server_name example.com www.example.com;
                return 301 https://example.com$request_uri;
            }
            server {                          # https://www -> https://bare domain
                listen 443 ssl;
                server_name www.example.com;
                # ssl_certificate / ssl_certificate_key for www.example.com here
                return 301 https://example.com$request_uri;
            }
        """, lang="nginx",
        ex_en=r"""Browsers cache 301s aggressively, so test with 302 first. Use `$request_uri`, not `$uri`: `$uri` is decoded and drops the query string.""",
        ex_bn=r"""Browser 301 অনেকদিন cache করে রাখে, তাই আগে 302 দিয়ে test করো। `$uri` না, `$request_uri` ব্যবহার করো: `$uri` decode করা থাকে আর query string বাদ দেয়।""",
        tip_en=r"""Mention `return` over `rewrite` and why `$request_uri` matters; both show hands-on config experience.""",
        tip_bn=r"""`rewrite`-এর বদলে `return` কেন, আর `$request_uri` কেন জরুরি, দুটোই বলো; এতে হাতে-কলমে config করার অভিজ্ঞতা বোঝা যায়।""",
        follow=[("When do you still need `rewrite` instead of `return`?", "কখন `return`-এর বদলে এখনো `rewrite` লাগে?")],
        related=["nginx-008"],
        refs=[N_REWRITE],
    ),
    # ------------------------------------------------------------------ nginx-q07
    Q(
        id="nginx-q07", sub="Configuration Blocks", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["server_name", "default_server", "virtual-hosts"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""How does NGINX choose which `server` block handles a request?""",
        q_bn=r"""কোন `server` block একটা request সামলাবে, NGINX সেটা কীভাবে ঠিক করে?""",
        a_en=r"""First it filters by the `listen` address and port, then it matches the `Host` header against `server_name`: exact name, then the longest wildcard starting with `*`, then the longest ending with `*`, then the first matching regex. If nothing matches, the `default_server` for that port is used (or the first server block if none is marked).""",
        a_bn=r"""প্রথমে `listen` address আর port দিয়ে বাছাই করে, তারপর `Host` header-কে `server_name`-এর সাথে মেলায়: আগে exact নাম, তারপর `*` দিয়ে শুরু হওয়া সবচেয়ে লম্বা wildcard, তারপর `*` দিয়ে শেষ হওয়া সবচেয়ে লম্বা wildcard, তারপর প্রথম match করা regex। কিছুই না মিললে ওই port-এর `default_server` ব্যবহার হয় (কোনোটা mark করা না থাকলে প্রথম server block)।""",
        code=r"""
            server {
                listen 80 default_server;   # catch-all for unknown Host headers
                server_name _;              # "_" is just an invalid name, not magic
                return 444;                 # close the connection without a response
            }
            server {
                listen 80;
                server_name example.com *.example.com;
                # ...
            }
        """, lang="nginx",
        ex_en=r"""The catch-all comes from `default_server` on `listen`, not from the name `_`. Without an explicit default, a request to your bare IP lands on whichever server block comes first.""",
        ex_bn=r"""Catch-all আসে `listen`-এর `default_server` থেকে, `_` নাম থেকে না। Explicit default না দিলে তোমার bare IP-তে আসা request যে server block প্রথমে আছে সেখানে চলে যায়।""",
        tip_en=r"""Recite the match order and add the `default_server` catch-all; that covers the usual follow-up about unknown hosts.""",
        tip_bn=r"""Match-এর ক্রমটা বলো আর `default_server` catch-all-এর কথা যোগ করো; অচেনা host নিয়ে সাধারণ follow-up-টা এতেই কভার হয়।""",
        follow=[("Why add a catch-all `default_server` that returns 444?", "444 return করা একটা catch-all `default_server` কেন যোগ করবে?")],
        related=["nginx-027", "nginx-003"],
        refs=[N_SERVER_NAMES],
    ),
    # ------------------------------------------------------------------ nginx-q08
    Q(
        id="nginx-q08", sub="Configuration Blocks", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["nginx-t", "reload", "operations"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""You changed the NGINX config. How do you apply it safely without dropping traffic?""",
        q_bn=r"""NGINX config বদলেছ। Traffic না হারিয়ে কীভাবে নিরাপদে apply করবে?""",
        a_en=r"""Run `nginx -t` to check the syntax and config, then reload with `nginx -s reload` (or `systemctl reload nginx`). A reload starts new workers with the new config while the old ones finish their requests, whereas a restart stops everything and drops connections.""",
        a_bn=r"""আগে `nginx -t` চালিয়ে syntax আর config যাচাই করো, তারপর `nginx -s reload` (বা `systemctl reload nginx`) দিয়ে reload করো। Reload নতুন config দিয়ে নতুন worker চালু করে আর পুরনোরা নিজেদের request শেষ করে; কিন্তু restart সব বন্ধ করে দেয়, connection কেটে যায়।""",
        code=r"""
            sudo nginx -t && sudo systemctl reload nginx
            # nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
            # nginx: configuration file /etc/nginx/nginx.conf test is successful
        """, lang="bash",
        ex_en=r"""If the new config is invalid, a reload is rejected and the old config keeps running. `nginx -T` prints the full effective config, which helps when includes are involved.""",
        ex_bn=r"""নতুন config ভুল হলে reload বাতিল হয়, আর পুরনো config চলতেই থাকে। `nginx -T` পুরো কার্যকর config print করে, include থাকলে এটা খুব কাজে লাগে।""",
        tip_en=r"""Say the exact one-liner `nginx -t && systemctl reload nginx` and explain why reload beats restart.""",
        tip_bn=r"""হুবহু `nginx -t && systemctl reload nginx` line-টা বলো, আর restart-এর চেয়ে reload কেন ভালো সেটা ব্যাখ্যা করো।""",
        follow=[("What happens to in-flight requests during a reload?", "Reload-এর সময় চলমান request-গুলোর কী হয়?")],
        related=["nginx-007", "nginx-003"],
        refs=[N_CONTROL],
    ),
    # ------------------------------------------------------------------ nginx-q09
    Q(
        id="nginx-q09", sub="Logging", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["logs", "access-log", "error-log", "debugging"],
        ver="Version-independent (NGINX 1.30 / 1.31, Debian/Ubuntu paths)", vs=False, status="stable",
        q_en=r"""What is the difference between NGINX's access log and error log, and which do you check first for a 502?""",
        q_bn=r"""NGINX-এর access log আর error log-এর পার্থক্য কী, আর 502 হলে আগে কোনটা দেখবে?""",
        a_en=r"""The **access log** has one line per request (client IP, request, status, size, timing), and the **error log** records problems and their reasons. For a 502, check the error log first, because it says exactly why, such as `connect() failed (111: Connection refused)` when the app is down.""",
        a_bn=r"""**Access log**-এ প্রতিটা request-এর জন্য এক line থাকে (client IP, request, status, size, সময়), আর **error log**-এ সমস্যা আর তার কারণ লেখা থাকে। 502 হলে আগে error log দেখো, কারণ সেখানে ঠিক কারণটা থাকে, যেমন app বন্ধ থাকলে `connect() failed (111: Connection refused)`।""",
        code=r"""
            sudo tail -f /var/log/nginx/error.log
            sudo tail -f /var/log/nginx/access.log
            # per site: access_log /var/log/nginx/api.access.log;  error_log /var/log/nginx/api.error.log;
        """, lang="bash",
        ex_en=r"""In the official Docker image, both logs go to stdout/stderr, so you read them with `docker logs`. Add `$upstream_response_time` to the log format to see how long the backend took.""",
        ex_bn=r"""Official Docker image-এ দুটো log-ই stdout/stderr-এ যায়, তাই `docker logs` দিয়ে পড়তে হয়। Backend কত সময় নিল দেখতে log format-এ `$upstream_response_time` যোগ করো।""",
        tip_en=r"""Say "status in the access log, reason in the error log", then quote one real error message.""",
        tip_bn=r"""বলো "access log-এ status, error log-এ কারণ", তারপর একটা আসল error message উদাহরণ দাও।""",
        follow=[("What's the difference between a 502 and a 504?", "502 আর 504-এর পার্থক্য কী?")],
        related=["nginx-010", "nginx-019"],
        refs=[N_LOG],
    ),
    # ------------------------------------------------------------------ nginx-q10
    Q(
        id="nginx-q10", sub="Location Matching", diff="medium", type="quick",
        prio="medium", market="both", mins=2,
        tags=["location", "regex", "prefix", "matching"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""What do the `location` modifiers `=`, `^~`, `~` and `~*` mean?""",
        q_bn=r"""`location`-এর modifier `=`, `^~`, `~` আর `~*` মানে কী?""",
        a_en=r"""`=` is an exact match and wins immediately; no modifier is a prefix match; `^~` is a prefix match that, if it's the longest, stops the regex search. `~` and `~*` are case-sensitive and case-insensitive regexes, checked in order after the longest prefix is found, and the first matching regex beats a plain prefix.""",
        a_bn=r"""`=` হলো exact match, মিললে সাথে সাথে জেতে; modifier ছাড়া হলো prefix match; `^~` এমন prefix match, যেটা সবচেয়ে লম্বা হলে regex খোঁজা বন্ধ করে দেয়। `~` আর `~*` হলো case-sensitive ও case-insensitive regex, সবচেয়ে লম্বা prefix পাওয়ার পর ক্রম অনুযায়ী পরীক্ষা হয়, আর প্রথম match করা regex সাধারণ prefix-কে হারিয়ে দেয়।""",
        code=r"""
            location = /health    { return 200 "ok"; }       # only /health
            location ^~ /static/  { root /var/www; }         # prefix, skip regex
            location ~* \.(png|jpg)$ { expires 30d; }        # case-insensitive regex
            location /            { proxy_pass http://127.0.0.1:3000; }
        """, lang="nginx",
        ex_en=r"""The usual trap: a plain prefix like `/images/` loses to a later regex for `.png` files unless you mark it `^~`.""",
        ex_bn=r"""সাধারণ ফাঁদ: `/images/`-এর মতো সাধারণ prefix `.png` file-এর জন্য পরের একটা regex-এর কাছে হেরে যায়, যদি না সেটাকে `^~` দিয়ে mark করো।""",
        tip_en=r"""Give the order: exact, longest prefix (stop if `^~`), regexes in order, else the remembered prefix.""",
        tip_bn=r"""ক্রমটা বলো: exact, সবচেয়ে লম্বা prefix (`^~` হলে থামো), ক্রম অনুযায়ী regex, না মিললে মনে রাখা prefix।""",
        follow=[("Which location handles `/images/logo.png` if both a prefix and a regex match?", "Prefix আর regex দুটোই match করলে `/images/logo.png` কোন location সামলাবে?")],
        related=["nginx-012"],
        refs=[N_HTTP_CORE],
    ),
]

if __name__ == "__main__":
    save("nginx", "quick", QUESTIONS)
