# NGINX — batch 1: nginx-001..004 (easy), nginx-012..013 (medium), nginx-023 (hard), nginx-030 (extreme)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

N_BEGIN = ("NGINX — Beginner's Guide", "https://nginx.org/en/docs/beginners_guide.html")
N_CORE_MAIN = ("NGINX — Core functionality (worker_processes, events)", "https://nginx.org/en/docs/ngx_core_module.html")
N_EVENTS = ("NGINX — Connection processing methods", "https://nginx.org/en/docs/events.html")
N_PROXY = ("NGINX — ngx_http_proxy_module", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html")
N_TUNNEL = ("NGINX — ngx_http_tunnel_module (1.31 mainline)", "https://nginx.org/en/docs/http/ngx_http_tunnel_module.html")
N_HTTP_CORE = ("NGINX — ngx_http_core_module", "https://nginx.org/en/docs/http/ngx_http_core_module.html")
N_CONTROL = ("NGINX — Controlling nginx", "https://nginx.org/en/docs/control.html")
N_HEADERS = ("NGINX — ngx_http_headers_module", "https://nginx.org/en/docs/http/ngx_http_headers_module.html")
N_REQ_PROC = ("NGINX — How nginx processes a request", "https://nginx.org/en/docs/http/request_processing.html")
N_UPSTREAM = ("NGINX — ngx_http_upstream_module", "https://nginx.org/en/docs/http/ngx_http_upstream_module.html")
N_REALIP = ("NGINX — ngx_http_realip_module", "https://nginx.org/en/docs/http/ngx_http_realip_module.html")
N_LIMIT_REQ = ("NGINX — ngx_http_limit_req_module", "https://nginx.org/en/docs/http/ngx_http_limit_req_module.html")
N_STUB = ("NGINX — ngx_http_stub_status_module", "https://nginx.org/en/docs/http/ngx_http_stub_status_module.html")
N_MAP = ("NGINX — ngx_http_map_module", "https://nginx.org/en/docs/http/ngx_http_map_module.html")
EXPRESS_UPLOAD = ("Express 5.x API — express.json() limit", "https://expressjs.com/en/5x/api.html")

QUESTIONS = [
    # ------------------------------------------------------------------ nginx-001
    Q(
        id="nginx-001", sub="Web Server Fundamentals", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["master-worker", "event-driven", "worker_processes", "worker_connections", "architecture"],
        ver="NGINX 1.30 stable / 1.31 mainline", vs=False, status="stable",
        q_en=r"""How does NGINX handle many thousands of concurrent connections? Explain its master/worker process model and event-driven architecture.""",
        q_bn=r"""NGINX কীভাবে হাজার হাজার concurrent connection সামলায়? এর master/worker process model আর event-driven architecture ব্যাখ্যা করো।""",
        a_en=r"""
            NGINX runs **one master process and several worker processes**.

            - The **master** (usually root) reads and validates the configuration, opens the listening sockets (80/443), starts and monitors workers, and handles control signals such as reload and binary upgrade. It doesn't serve requests.
            - The **workers** (an unprivileged user such as `nginx` or `www-data`) do all the real work. Each worker runs an **event loop** on the OS's efficient notification mechanism (`epoll` on Linux, `kqueue` on BSD/macOS) and handles thousands of connections with **non-blocking I/O**. There's no thread or process per connection.

            `worker_processes auto;` starts one worker per CPU core, and `worker_connections` caps simultaneous connections per worker. Because an idle keep-alive connection costs only a little memory and no thread, NGINX copes well with slow clients and huge connection counts. That's why it sits so well in front of Node.js, which uses the same event-loop idea.
        """,
        a_bn=r"""
            NGINX চালায় **একটা master process আর কয়েকটা worker process**।

            - **Master** (সাধারণত root) configuration পড়ে ও validate করে, listening socket (80/443) খোলে, worker-দের start ও monitor করে, আর reload বা binary upgrade-এর মতো control signal সামলায়। এটা নিজে কোনো request serve করে না।
            - **Worker**-রা (`nginx` বা `www-data`-এর মতো unprivileged user) আসল সব কাজ করে। প্রতিটা worker OS-এর দক্ষ notification ব্যবস্থার (Linux-এ `epoll`, BSD/macOS-এ `kqueue`) উপর একটা **event loop** চালায়, আর **non-blocking I/O** দিয়ে হাজার হাজার connection সামলায়। প্রতি connection-এর জন্য আলাদা thread বা process নেই।

            `worker_processes auto;` প্রতিটা CPU core-এর জন্য একটা worker চালু করে, আর `worker_connections` প্রতিটা worker-এর একসাথে কতগুলো connection থাকতে পারবে তার সীমা ঠিক করে। একটা idle keep-alive connection-এর জন্য সামান্য memory লাগে আর কোনো thread লাগে না, তাই ধীর client আর বিপুল সংখ্যক connection NGINX ভালোভাবে সামলাতে পারে। এজন্যই Node.js-এর সামনে এটা এত ভালো মানায়, কারণ Node.js-ও একই event-loop ধারণা ব্যবহার করে।
        """,
        quick_en=r"""One master process reads the config, opens the listening ports and manages workers; the workers do all the work. Each worker runs a non-blocking event loop (`epoll`/`kqueue`) that handles thousands of connections without a thread per connection, and `worker_processes auto` starts one worker per CPU core.""",
        quick_bn=r"""একটা master process config পড়ে, listening port খোলে আর worker-গুলো manage করে; আসল কাজ সব worker-রা করে। প্রতিটা worker একটা non-blocking event loop (`epoll`/`kqueue`) চালায়, connection-প্রতি thread ছাড়াই হাজার হাজার connection সামলায়, আর `worker_processes auto` প্রতি CPU core-এ একটা worker চালু করে।""",
        ex_en=r"""
            - **Why one worker per core:** CPU-heavy work such as TLS handshakes and gzip happens inside workers. More workers than cores just adds context switching.
            - **Blocking is the enemy:** anything that blocks a worker (slow disk reads, synchronous modules) stalls **all** its connections. NGINX offers thread pools (`aio threads`) for that.
            - **Other processes:** with `proxy_cache`, you'll also see a **cache loader** and a **cache manager** process.
            - **Graceful reloads:** on reload the master starts new workers with the new config while the old ones finish their in-flight requests. That's how configuration changes avoid downtime.
            - **Contrast:** a classic thread/process-per-connection server (e.g. Apache prefork) needs far more memory for the same number of idle connections.
        """,
        ex_bn=r"""
            - **কেন প্রতি core-এ একটা worker:** TLS handshake আর gzip-এর মতো CPU-ভারী কাজ worker-এর ভেতরেই হয়। Core-এর চেয়ে বেশি worker হলে শুধু context switching বাড়ে।
            - **Blocking হলো শত্রু:** worker-কে block করে এমন যেকোনো কিছু (ধীর disk read, synchronous module) ওই worker-এর **সব** connection থামিয়ে দেয়। এর জন্য NGINX thread pool (`aio threads`) দেয়।
            - **অন্যান্য process:** `proxy_cache` ব্যবহার করলে একটা **cache loader** আর একটা **cache manager** process-ও দেখা যায়।
            - **Graceful reload:** reload-এর সময় master নতুন config দিয়ে নতুন worker চালু করে, আর পুরনোরা হাতে থাকা request শেষ করে। এভাবেই downtime ছাড়া configuration বদলানো যায়।
            - **তুলনা:** প্রতি connection-এ একটা thread/process দেওয়া classic server (যেমন Apache prefork)-এর একই সংখ্যক idle connection রাখতে অনেক বেশি memory লাগে।
        """,
        tip_en=r"""Use the phrase "a few workers, each with an event loop, instead of a thread per connection", then link it to a real benefit: slow mobile clients on 3G/4G don't tie up your Node.js processes when NGINX buffers in front of them.""",
        tip_bn=r""""প্রতি connection-এ thread-এর বদলে কয়েকটা worker, প্রত্যেকের একটা event loop", এই কথাটা ব্যবহার করো। তারপর একটা বাস্তব সুবিধার সাথে যুক্ত করো: NGINX সামনে থেকে buffer করলে 3G/4G-এর ধীর mobile client তোমার Node.js process আটকে রাখতে পারে না।""",
        mist_en=r"""Saying NGINX is "multi-threaded with one thread per request", setting `worker_processes` far above the CPU count, or thinking the master process handles traffic.""",
        mist_bn=r"""NGINX-কে "প্রতি request-এ একটা thread-ওয়ালা multi-threaded server" বলা, CPU-র সংখ্যার চেয়ে অনেক বেশি `worker_processes` set করা, অথবা ভাবা যে master process traffic সামলায়।""",
        code=r"""
            $ ps -o pid,user,cmd -C nginx
                PID USER     CMD
               1021 root     nginx: master process /usr/sbin/nginx -c /etc/nginx/nginx.conf
               1022 nginx    nginx: worker process
               1023 nginx    nginx: worker process
               1024 nginx    nginx: worker process
               1025 nginx    nginx: worker process

            # nginx.conf (main + events contexts)
            #   worker_processes auto;
            #   events { worker_connections 1024; }
        """,
        lang="bash",
        follow=[
            ("What happens to in-flight requests during `nginx -s reload`?", "`nginx -s reload`-এর সময় চলমান request-গুলোর কী হয়?"),
            ("Why can a blocking operation inside a worker hurt many users at once?", "একটা worker-এর ভেতরে blocking operation কেন একসাথে অনেক user-এর ক্ষতি করতে পারে?"),
        ],
        refs=[N_BEGIN, N_CORE_MAIN, N_EVENTS],
    ),
    # ------------------------------------------------------------------ nginx-002
    Q(
        id="nginx-002", sub="Reverse Proxy", diff="easy", type="comparison",
        prio="high", market="bangladesh", mins=3,
        tags=["reverse-proxy", "forward-proxy", "cdn", "load-balancer"],
        ver="NGINX 1.30 stable / 1.31 mainline", vs=False, status="stable",
        q_en=r"""What is the difference between a forward proxy and a reverse proxy? Why do we put NGINX as a reverse proxy in front of a Node.js app?""",
        q_bn=r"""Forward proxy আর reverse proxy-র মধ্যে পার্থক্য কী? Node.js app-এর সামনে NGINX-কে reverse proxy হিসেবে কেন বসানো হয়?""",
        a_en=r"""
            - A **forward proxy** sits in front of **clients** and makes requests to the internet on their behalf, like a corporate or university proxy. The client is configured to use it, and websites see the proxy instead of the user. It's used for filtering, caching, auditing or anonymity.
            - A **reverse proxy** sits in front of **servers** and receives requests on their behalf. The client thinks it's talking to the real site and has no idea which backend actually served it.

            In front of Node.js, NGINX as a reverse proxy gives me:
            - **TLS termination** and HTTP/2/HTTP/3 support;
            - **load balancing** across several Node processes or hosts;
            - fast **static file** serving, **compression** and **caching**;
            - **buffering** of slow clients, so Node isn't tied up;
            - rate limiting, request size limits and security headers;
            - hiding internal ports and topology. The app listens only on `127.0.0.1:3000`.
        """,
        a_bn=r"""
            - **Forward proxy** বসে **client-দের** সামনে, আর তাদের হয়ে internet-এ request পাঠায়, যেমন অফিস বা বিশ্ববিদ্যালয়ের proxy। Client-কে এটা ব্যবহারের জন্য configure করা থাকে, আর website user-এর বদলে proxy-কে দেখে। এটা ব্যবহার হয় filtering, caching, auditing বা anonymity-র জন্য।
            - **Reverse proxy** বসে **server-দের** সামনে, আর তাদের হয়ে request গ্রহণ করে। Client ভাবে সে আসল site-এর সাথেই কথা বলছে, কোন backend আসলে উত্তর দিল সে জানেই না।

            Node.js-এর সামনে NGINX reverse proxy হিসেবে আমাকে দেয়:
            - **TLS termination** আর HTTP/2/HTTP/3 support;
            - একাধিক Node process বা host-এর মধ্যে **load balancing**;
            - দ্রুত **static file** serving, **compression** আর **caching**;
            - ধীর client-দের **buffering**, যাতে Node আটকে না থাকে;
            - rate limiting, request size limit আর security header;
            - ভেতরের port আর topology লুকিয়ে রাখা। App শুধু `127.0.0.1:3000`-এ listen করে।
        """,
        quick_en=r"""A forward proxy acts for clients (like an office proxy), while a reverse proxy sits in front of servers and receives requests on their behalf. In front of Node.js, NGINX adds TLS termination, load balancing, fast static files, compression, slow-client buffering and rate limits, and keeps the app private on `127.0.0.1`.""",
        quick_bn=r"""Forward proxy client-দের হয়ে কাজ করে (যেমন অফিসের proxy), আর reverse proxy server-দের সামনে বসে তাদের হয়ে request নেয়। Node.js-এর সামনে NGINX TLS termination, load balancing, দ্রুত static file, compression, slow client buffering আর rate limit দেয়, আর app-কে `127.0.0.1`-এ লুকিয়ে রাখে।""",
        ex_en=r"""
            - **Who knows about the proxy?** With a forward proxy the **client** knows and configures it. With a reverse proxy only the **server operator** knows. That's the cleanest way to tell them apart.
            - **Same family:** CDNs, API gateways and cloud load balancers (e.g. AWS ALB) are all reverse proxies with extra features.
            - **NGINX as a forward proxy:** NGINX was designed as a reverse proxy. HTTPS forward proxying needs the `CONNECT` method, which stock NGINX didn't support until the `ngx_http_tunnel_module` appeared in the **1.31 mainline** (it's not in 1.30 stable). Dedicated tools like Squid remain the usual choice for forward proxies.
            - **Side effect:** the app now sees NGINX's IP as the client, so you must forward the real client IP and protocol with proxy headers.
        """,
        ex_bn=r"""
            - **Proxy-র কথা কে জানে?** Forward proxy-র ক্ষেত্রে **client** জানে আর নিজেই configure করে। Reverse proxy-র ক্ষেত্রে শুধু **server operator** জানে। দুটোকে আলাদা করার সবচেয়ে পরিষ্কার উপায় এটাই।
            - **একই পরিবার:** CDN, API gateway আর cloud load balancer (যেমন AWS ALB) সবই বাড়তি feature-ওয়ালা reverse proxy।
            - **Forward proxy হিসেবে NGINX:** NGINX reverse proxy হিসেবেই design করা। HTTPS forward proxying-এর জন্য `CONNECT` method লাগে, যেটা সাধারণ NGINX-এ ছিল না, যতদিন না **1.31 mainline**-এ `ngx_http_tunnel_module` এল (1.30 stable-এ নেই)। Forward proxy-র জন্য এখনো Squid-এর মতো নিবেদিত tool-ই সাধারণ পছন্দ।
            - **পার্শ্বপ্রতিক্রিয়া:** app এখন client হিসেবে NGINX-এর IP দেখে, তাই proxy header দিয়ে আসল client IP আর protocol পাঠাতে হয়।
        """,
        tip_en=r"""Use the "who is configured to know about the proxy" test, then list three or four concrete benefits for a Node.js deployment. Concrete benefits beat abstract definitions.""",
        tip_bn=r""""Proxy-র কথা জানার জন্য কাকে configure করা হয়েছে", এই পরীক্ষাটা ব্যবহার করো। তারপর Node.js deployment-এর জন্য তিন-চারটা বাস্তব সুবিধা বলো। বিমূর্ত সংজ্ঞার চেয়ে বাস্তব সুবিধা বেশি কাজে দেয়।""",
        mist_en=r"""Calling a VPN a forward proxy (it works at a different layer), or forgetting that the app needs `X-Forwarded-*` headers once it sits behind a reverse proxy.""",
        mist_bn=r"""VPN-কে forward proxy বলা (এটা অন্য layer-এ কাজ করে), অথবা ভুলে যাওয়া যে reverse proxy-র পেছনে বসার পর app-এর `X-Forwarded-*` header লাগে।""",
        code=r"""
            # Reverse proxy: clients talk to NGINX, NGINX talks to Node on localhost
            server {
                listen 80;
                server_name api.example.com;

                location / {
                    proxy_pass http://127.0.0.1:3000;
                    proxy_set_header Host $host;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;
                }
            }

            # Forward proxy, from the client's side (the client must be configured):
            #   curl -x http://proxy.corp.local:3128 https://example.com
        """,
        lang="nginx",
        follow=[
            ("Is a CDN a forward or a reverse proxy? Why?", "CDN কি forward proxy না reverse proxy? কেন?"),
            ("What does the Node app lose by default when it sits behind a reverse proxy?", "Reverse proxy-র পেছনে বসলে Node app default হিসেবে কী কী তথ্য হারায়?"),
        ],
        related=["nginx-001"],
        refs=[N_PROXY, N_BEGIN, N_TUNNEL],
    ),
    # ------------------------------------------------------------------ nginx-003
    Q(
        id="nginx-003", sub="Configuration Blocks", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["contexts", "server-block", "location", "inheritance", "nginx-t"],
        ver="NGINX 1.30 stable / 1.31 mainline (add_header_inherit since 1.29.3)", vs=True, status="stable",
        q_en=r"""Explain how an NGINX configuration is structured. What are contexts, how does directive inheritance work, and how do you safely apply a change?""",
        q_bn=r"""NGINX configuration-এর গঠন কেমন, ব্যাখ্যা করো। Context কী, directive inheritance কীভাবে কাজ করে, আর একটা পরিবর্তন নিরাপদে কীভাবে প্রয়োগ করবে?""",
        a_en=r"""
            A config is made of **directives**: simple ones (`name value;`) and block ones that open a **context**. The hierarchy is:

            - **main** (top level): `user`, `worker_processes`, `error_log`, `pid`.
            - **`events {}`**: connection processing, e.g. `worker_connections`.
            - **`http {}`**: everything HTTP. MIME types, logs, gzip, `upstream` groups, `map`s and rate-limit zones live here.
            - **`server {}`**: a virtual host, with `listen`, `server_name` and TLS certificates.
            - **`location {}`**: per-URI handling inside a server, such as `proxy_pass`, `root` or `try_files`.

            There's also `stream {}` for TCP/UDP proxying.

            **Inheritance:** a directive set in an outer context applies to inner ones unless the inner context redefines it. The classic gotcha is "array" directives such as `proxy_set_header` and `add_header`: defining **even one** at an inner level drops **all** the inherited ones.

            **Applying a change safely:** run `nginx -t` (syntax and config test), optionally `nginx -T` to dump the full effective config, then `nginx -s reload` or `systemctl reload nginx`. Reloads are graceful, and an invalid config is rejected while the old one keeps running.
        """,
        a_bn=r"""
            Config তৈরি হয় **directive** দিয়ে: সাধারণ directive (`name value;`) আর block directive, যেটা একটা **context** খোলে। Hierarchy হলো:

            - **main** (সবচেয়ে উপরের স্তর): `user`, `worker_processes`, `error_log`, `pid`।
            - **`events {}`**: connection processing, যেমন `worker_connections`।
            - **`http {}`**: HTTP-সংক্রান্ত সবকিছু। MIME type, log, gzip, `upstream` group, `map` আর rate-limit zone এখানে থাকে।
            - **`server {}`**: একটা virtual host, যেখানে থাকে `listen`, `server_name` আর TLS certificate।
            - **`location {}`**: server-এর ভেতরে প্রতিটা URI কীভাবে handle হবে, যেমন `proxy_pass`, `root` বা `try_files`।

            TCP/UDP proxying-এর জন্য `stream {}`-ও আছে।

            **Inheritance:** বাইরের context-এ set করা directive ভেতরের context-এও প্রযোজ্য, যদি না ভেতরের context সেটা নতুন করে define করে। Classic gotcha হলো `proxy_set_header` আর `add_header`-এর মতো "array" directive: ভেতরের স্তরে **একটাও** define করলে inherit হওয়া **সবগুলো** বাদ পড়ে যায়।

            **নিরাপদে পরিবর্তন প্রয়োগ:** `nginx -t` চালাও (syntax আর config test), চাইলে `nginx -T` দিয়ে পুরো কার্যকর config দেখে নাও, তারপর `nginx -s reload` বা `systemctl reload nginx`। Reload graceful হয়, আর config ভুল হলে সেটা reject হয়, পুরনোটা চলতে থাকে।
        """,
        quick_en=r"""The config is nested contexts (main, `events`, `http`, `server`, `location`), and inner contexts inherit outer directives unless they redefine them. The catch: one `add_header` or `proxy_set_header` at an inner level drops all inherited ones; apply changes with `nginx -t` and then a graceful reload.""",
        quick_bn=r"""Config হলো nested context (main, `events`, `http`, `server`, `location`), আর ভেতরের context বাইরের directive inherit করে, যদি না নিজে আবার define করে। সাবধান: ভেতরের level-এ একটা `add_header` বা `proxy_set_header` দিলেই inherit হওয়া সবগুলো বাদ পড়ে যায়; পরিবর্তন apply করো `nginx -t` চালিয়ে, তারপর graceful reload দিয়ে।""",
        ex_en=r"""
            - **File layout:** `nginx.org` packages include `/etc/nginx/conf.d/*.conf` from `nginx.conf`, while Debian/Ubuntu packages also use `sites-available/` with symlinks in `sites-enabled/`. Know which one your server uses before adding files.
            - **The inheritance gotcha in practice:** you set HSTS with `add_header` in the `server` block, then add one `add_header Cache-Control …` inside a `location`. Responses from that location silently lose HSTS. NGINX 1.29.3+ (so 1.30 stable) adds `add_header_inherit merge;` to change this behaviour. On older versions, repeat the headers or use a shared `include` snippet.
            - **Order:** the order of `location` blocks in the file doesn't decide matching (except among regex locations). Matching rules are a separate topic.
            - A reload applies configuration only. Upgrading the NGINX binary itself needs a restart or the on-the-fly binary upgrade procedure (`USR2` signal).
        """,
        ex_bn=r"""
            - **File layout:** `nginx.org`-এর package `nginx.conf` থেকে `/etc/nginx/conf.d/*.conf` include করে, আর Debian/Ubuntu-র package এর সাথে `sites-available/` আর `sites-enabled/`-এ symlink ব্যবহার করে। নতুন file যোগ করার আগে জেনে নাও তোমার server কোনটা ব্যবহার করে।
            - **বাস্তবে inheritance-এর gotcha:** `server` block-এ `add_header` দিয়ে HSTS set করলে, তারপর একটা `location`-এ একটা `add_header Cache-Control …` যোগ করলে। ওই location-এর response থেকে HSTS চুপচাপ হারিয়ে যায়। NGINX 1.29.3+ (অর্থাৎ 1.30 stable) এই আচরণ বদলাতে `add_header_inherit merge;` যোগ করেছে। পুরনো version-এ header-গুলো আবার লেখো, বা একটা shared `include` snippet ব্যবহার করো।
            - **ক্রম:** file-এ `location` block-এর ক্রম matching ঠিক করে না (regex location-গুলোর মধ্যে ছাড়া)। Matching-এর নিয়ম আলাদা একটা বিষয়।
            - Reload শুধু configuration প্রয়োগ করে। NGINX-এর binary নিজেই upgrade করতে হলে restart লাগে, অথবা on-the-fly binary upgrade পদ্ধতি (`USR2` signal)।
        """,
        tip_en=r"""Sketch the nesting (main → events/http → server → location) out loud, then mention the `add_header`/`proxy_set_header` inheritance trap. Many experienced engineers have been bitten by it, so it signals real-world experience.""",
        tip_bn=r"""Nesting-টা মুখে মুখে এঁকে দেখাও (main → events/http → server → location), তারপর `add_header`/`proxy_set_header` inheritance-এর ফাঁদটা উল্লেখ করো। অনেক অভিজ্ঞ engineer এতে ধরা খেয়েছে, তাই এটা বাস্তব অভিজ্ঞতার পরিচয় দেয়।""",
        mist_en=r"""Running `systemctl restart nginx` for every change (it drops connections), editing without `nginx -t`, or putting `upstream`/`map` blocks inside `server`.""",
        mist_bn=r"""প্রতিটা পরিবর্তনে `systemctl restart nginx` চালানো (এতে connection কেটে যায়), `nginx -t` না চালিয়েই edit করা, অথবা `upstream`/`map` block `server`-এর ভেতরে রাখা।""",
        code=r"""
            user  nginx;
            worker_processes  auto;                     # main context
            error_log  /var/log/nginx/error.log warn;

            events {
                worker_connections  1024;
            }

            http {
                include       /etc/nginx/mime.types;
                default_type  application/octet-stream;
                sendfile      on;

                upstream app {                          # lives in http
                    server 127.0.0.1:3000;
                }

                server {                                # virtual host
                    listen 80;
                    server_name example.com;

                    location / {                        # per-URI rules
                        proxy_pass http://app;
                    }
                }

                include /etc/nginx/conf.d/*.conf;
            }
        """,
        lang="nginx",
        extra=[
            dict(lang="bash", label_en="Safe change workflow", label_bn="নিরাপদে পরিবর্তনের ধাপ", src=r"""
                sudo nginx -t                  # test syntax + config
                sudo nginx -T | less           # full effective config, all includes expanded
                sudo systemctl reload nginx    # graceful (same as nginx -s reload)
            """),
        ],
        follow=[
            ("Why do security headers sometimes disappear on certain URLs?", "কিছু URL-এ security header মাঝে মাঝে কেন হারিয়ে যায়?"),
            ("What's the difference between `reload` and `restart` for NGINX?", "NGINX-এর `reload` আর `restart`-এর মধ্যে পার্থক্য কী?"),
        ],
        related=["nginx-001"],
        refs=[N_BEGIN, N_CONTROL, N_HEADERS],
    ),
    # ------------------------------------------------------------------ nginx-004
    Q(
        id="nginx-004", sub="Request Size Limits", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["413", "client_max_body_size", "uploads"],
        ver="NGINX 1.30 stable / 1.31 mainline", vs=False, status="stable",
        q_en=r"""Users get `413 Request Entity Too Large` from NGINX when uploading a 5 MB profile photo to your Express API. Which directive fixes it?""",
        q_bn=r"""Express API-তে 5 MB-এর একটা profile photo upload করার সময় user-রা NGINX থেকে `413 Request Entity Too Large` পাচ্ছে। কোন directive এটা ঠিক করবে?""",
        options=[
            ("`proxy_buffer_size 8m;`", "`proxy_buffer_size 8m;`"),
            ("`client_body_buffer_size 10m;`", "`client_body_buffer_size 10m;`"),
            ("`client_max_body_size 10m;`", "`client_max_body_size 10m;`"),
            ("`large_client_header_buffers 4 10m;`", "`large_client_header_buffers 4 10m;`"),
        ],
        correct=2,
        a_en=r"""`client_max_body_size` sets the largest request body NGINX accepts. Its default is **1m**, so a 5 MB upload is rejected with 413 before it ever reaches Node. Raise it, ideally only on the upload route (e.g. `location /api/uploads { client_max_body_size 10m; … }`), instead of globally.""",
        a_bn=r"""`client_max_body_size` ঠিক করে NGINX সর্বোচ্চ কত বড় request body গ্রহণ করবে। এর default **1m**, তাই 5 MB-এর upload Node-এ পৌঁছানোর আগেই 413 দিয়ে reject হয়। এটা বাড়াও, তবে globally না করে সম্ভব হলে শুধু upload route-এ (যেমন `location /api/uploads { client_max_body_size 10m; … }`)।""",
        quick_en=r"""`client_max_body_size 10m;`. Its default is 1m, so NGINX rejects the 5 MB upload with 413 before it reaches Node; raise it on the upload location rather than globally.""",
        quick_bn=r"""`client_max_body_size 10m;`। এর default 1m, তাই 5 MB upload Node-এ পৌঁছানোর আগেই NGINX 413 দিয়ে ফিরিয়ে দেয়; global-এ না বাড়িয়ে শুধু upload location-এ বাড়াও।""",
        ex_en=r"""
            The tempting wrong answer is `client_body_buffer_size`. It controls how much of the body is buffered **in memory** before NGINX spills it to a temporary file. It doesn't change the size limit. `proxy_buffer_size` concerns the **upstream response** headers, and `large_client_header_buffers` limits request **headers**.

            Also check the app layer. `express.json()` defaults to a 100kb limit (larger bodies fail with a 413 `PayloadTooLargeError`), and multer's `limits.fileSize` raises a `MulterError` (`LIMIT_FILE_SIZE`) that your error handler should map to 413. NGINX's own 413 is a small HTML page that mentions nginx, while the app's response comes from your Express error handler, which helps you tell which layer rejected the request. Setting `client_max_body_size 0;` disables the check entirely. Avoid that on public endpoints.
        """,
        ex_bn=r"""
            বিভ্রান্তিকর ভুল উত্তর হলো `client_body_buffer_size`। এটা ঠিক করে body-র কতটা **memory-তে** buffer হবে, তারপর NGINX বাকিটা temporary file-এ লেখে। এটা size limit বদলায় না। `proxy_buffer_size` **upstream response**-এর header-এর সাথে সম্পর্কিত, আর `large_client_header_buffers` request-এর **header** সীমিত করে।

            App layer-ও দেখে নাও। `express.json()`-এর default limit 100kb (এর চেয়ে বড় body 413 `PayloadTooLargeError` দিয়ে fail করে), আর multer-এর `limits.fileSize` পার হলে একটা `MulterError` (`LIMIT_FILE_SIZE`) আসে, যেটা তোমার error handler-এ 413-এ map করা উচিত। NGINX-এর নিজের 413 হলো nginx-এর নাম লেখা ছোট একটা HTML page, আর app-এর response আসে তোমার Express error handler থেকে। এতে বোঝা যায় কোন layer request reject করেছে। `client_max_body_size 0;` দিলে check পুরোপুরি বন্ধ হয়ে যায়। Public endpoint-এ এটা এড়িয়ে চলো।
        """,
        tip_en=r"""Mention the 1 MB default and scoping the limit to the upload location. It shows you think about DoS surface, not just making the error disappear.""",
        tip_bn=r"""1 MB-এর default আর limit শুধু upload location-এ সীমিত রাখার কথা বলো। এতে বোঝা যায় তুমি শুধু error দূর করার কথা না, DoS-এর ঝুঁকির কথাও ভাবো।""",
        related=["nginx-003"],
        refs=[N_HTTP_CORE, EXPRESS_UPLOAD],
    ),
    # ------------------------------------------------------------------ nginx-012
    Q(
        id="nginx-012", sub="Location Matching", diff="medium", type="mcq",
        prio="high", market="both", mins=3,
        tags=["location", "regex", "prefix", "matching-order"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""Given this server block, which response does `GET /images/photo.png` return?""",
        q_bn=r"""এই server block দেখে বলো, `GET /images/photo.png` কোন response দেবে?""",
        code=r"""
            server {
                listen 80;

                location / {
                    return 200 "root";
                }
                location /images/ {
                    return 200 "images";
                }
                location ^~ /images/icons/ {
                    return 200 "icons";
                }
                location ~* \.(png|jpe?g|gif)$ {
                    return 200 "regex";
                }
                location = /images/logo.png {
                    return 200 "exact";
                }
            }
        """,
        lang="nginx",
        options=[
            ("`images`: `/images/` is the longest matching prefix", "`images`: `/images/` হলো সবচেয়ে লম্বা মিলে যাওয়া prefix"),
            ("`regex`: the regex location wins over a plain prefix match", "`regex`: সাধারণ prefix match-এর উপর regex location জিতে যায়"),
            ("`icons`: `^~` locations are always checked first", "`icons`: `^~` location সবসময় আগে check করা হয়"),
            ("`root`: `/` matches every request", "`root`: `/` সব request-এর সাথেই মেলে"),
        ],
        correct=1,
        a_en=r"""The response is `regex` (option **B**). NGINX first checks exact (`=`) matches, then finds the **longest prefix** match, which is `/images/` here, and remembers it. Because that prefix isn't marked `^~`, NGINX then tests **regex locations in the order they appear**. `~* \.(png|jpe?g|gif)$` matches, so it wins. The remembered prefix is used only if no regex matches.""",
        a_bn=r"""Response হবে `regex` (option **B**)। NGINX প্রথমে exact (`=`) match দেখে, তারপর **সবচেয়ে লম্বা prefix** match খোঁজে, এখানে `/images/`, আর সেটা মনে রাখে। ওই prefix-এ `^~` চিহ্ন নেই, তাই NGINX এরপর **file-এ যে ক্রমে আছে সেই ক্রমে regex location** পরীক্ষা করে। `~* \.(png|jpe?g|gif)$` মিলে যায়, তাই এটাই জেতে। কোনো regex না মিললে তবেই মনে রাখা prefix ব্যবহার হয়।""",
        quick_en=r"""`regex`: NGINX remembers the longest prefix match (`/images/`), but since it isn't marked `^~`, it then tests regex locations in order and the image regex matches. The remembered prefix is used only if no regex matches.""",
        quick_bn=r"""`regex`: NGINX সবচেয়ে লম্বা prefix match (`/images/`) মনে রাখে, কিন্তু সেটা `^~` দিয়ে mark করা নেই, তাই এরপর regex location-গুলো ক্রম অনুযায়ী পরীক্ষা করে, আর image-এর regex match করে। কোনো regex match না করলে তবেই মনে রাখা prefix ব্যবহার হয়।""",
        ex_en=r"""
            The full algorithm:
            1. `=` exact match → use it immediately (`/images/logo.png` → `exact`).
            2. Find the longest prefix match. If it's marked `^~`, use it and **skip regexes** (`/images/icons/cart.png` → `icons`, even though it ends in `.png`).
            3. Otherwise check `~` (case-sensitive) and `~*` (case-insensitive) regexes in file order; the first match wins (`/images/photo.png` → `regex`).
            4. If no regex matches, use the longest prefix from step 2 (`/images/readme.txt` → `images`; `/about` → `root`).

            The most common wrong choice is option A (`images`), from people who assume "longest prefix always wins". Option C (`icons`) is wrong because `^~` only wins when it **is** the longest prefix match. It isn't "checked first".
        """,
        ex_bn=r"""
            পুরো algorithm:
            1. `=` exact match → সাথে সাথে সেটা ব্যবহার (`/images/logo.png` → `exact`)।
            2. সবচেয়ে লম্বা prefix match খোঁজো। সেটা `^~` চিহ্নিত হলে সেটাই ব্যবহার করো আর **regex বাদ দাও** (`/images/icons/cart.png` → `icons`, যদিও শেষে `.png`)।
            3. না হলে file-এর ক্রমে `~` (case-sensitive) আর `~*` (case-insensitive) regex পরীক্ষা করো; প্রথম যেটা মেলে সেটা জেতে (`/images/photo.png` → `regex`)।
            4. কোনো regex না মিললে ধাপ ২-এর সবচেয়ে লম্বা prefix ব্যবহার করো (`/images/readme.txt` → `images`; `/about` → `root`)।

            সবচেয়ে বেশি মানুষ যে ভুলটা করে সেটা option A (`images`): তারা ধরে নেয় "সবচেয়ে লম্বা prefix সবসময় জেতে"। Option C (`icons`) ভুল, কারণ `^~` তখনই জেতে যখন সেটাই সবচেয়ে লম্বা prefix match। এটা "আগে check করা হয়" না।
        """,
        tip_en=r"""Recite the order as "exact, longest prefix (stop if `^~`), regex in file order, else the prefix". Then trace two or three URLs through it out loud. Tracing shows understanding, not memorisation.""",
        tip_bn=r"""ক্রমটা এভাবে বলো: "exact, সবচেয়ে লম্বা prefix (`^~` হলে থামো), file-এর ক্রমে regex, নইলে সেই prefix"। তারপর দুই-তিনটা URL এর মধ্য দিয়ে মুখে মুখে trace করো। Trace করা মুখস্থ না, বোঝাপড়া দেখায়।""",
        follow=[
            ("What would `GET /images/icons/cart.png` return, and why does its `.png` ending not matter?", "`GET /images/icons/cart.png` কী return করবে, আর এর শেষে `.png` থাকলেও কেন কিছু যায় আসে না?"),
            ("If you moved the regex location above `location /images/`, would any response change?", "Regex location-টা `location /images/`-এর উপরে সরালে কি কোনো response বদলাবে?"),
        ],
        related=["nginx-003"],
        refs=[N_HTTP_CORE, N_REQ_PROC],
    ),
    # ------------------------------------------------------------------ nginx-013
    Q(
        id="nginx-013", sub="Reverse Proxy", diff="medium", type="debugging",
        prio="high", market="both", mins=5,
        tags=["proxy_pass", "trailing-slash", "uri-rewriting", "express", "404"],
        ver="NGINX 1.30 stable / 1.31 mainline, Express 5.x", vs=False, status="stable",
        q_en=r"""
            The React app loads fine, but every API call returns 404. The Express app defines its routes as `app.use('/api/products', productsRouter)`, and its logs show `GET /products 404`. Find the bug in this NGINX config.
        """,
        q_bn=r"""
            React app ঠিকঠাক load হচ্ছে, কিন্তু প্রতিটা API call 404 দিচ্ছে। Express app-এ route define করা আছে `app.use('/api/products', productsRouter)` দিয়ে, আর এর log-এ দেখা যাচ্ছে `GET /products 404`। এই NGINX config-এর bug খুঁজে বের করো।
        """,
        code=r"""
            server {
                listen 80;
                server_name shop.example.com;

                root /var/www/shop/dist;

                location / {
                    try_files $uri /index.html;
                }

                location /api/ {
                    proxy_pass http://127.0.0.1:4000/;
                }
            }
        """,
        lang="nginx",
        extra=[
            dict(lang="nginx", label_en="Fixed: no URI part in proxy_pass, so /api/... is passed unchanged", label_bn="সমাধান: proxy_pass-এ URI অংশ নেই, তাই /api/... যেমন আছে তেমনই যায়", src=r"""
                location /api/ {
                    proxy_pass http://127.0.0.1:4000;        # no trailing slash / URI
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;
                }
            """),
        ],
        a_en=r"""
            The bug is the trailing slash in `proxy_pass http://127.0.0.1:4000/;`.

            The rule: if `proxy_pass` contains a **URI part** (anything after host:port, even a lone `/`), NGINX **replaces the part of the request URI that matched the location** with that URI. Here `/api/` is replaced by `/`, so `/api/products` reaches Express as `/products`, and no route matches.

            If `proxy_pass` has **no URI**, the original request URI is passed unchanged.

            **Fix:** use `proxy_pass http://127.0.0.1:4000;` so Express receives `/api/products`. The alternative, keeping the slash, is fine only if you **intend** to strip the prefix and mount Express routes at `/products`. Either way, pick one convention and document it.
        """,
        a_bn=r"""
            Bug-টা হলো `proxy_pass http://127.0.0.1:4000/;`-এর শেষের slash।

            নিয়মটা হলো: `proxy_pass`-এ **URI অংশ** থাকলে (host:port-এর পরে যেকোনো কিছু, শুধু একটা `/` হলেও), NGINX request URI-এর **যে অংশ location-এর সাথে মিলেছে** সেটাকে ওই URI দিয়ে replace করে। এখানে `/api/` replace হয়ে যায় `/` দিয়ে, তাই `/api/products` Express-এ পৌঁছায় `/products` হয়ে, আর কোনো route মেলে না।

            `proxy_pass`-এ **কোনো URI না থাকলে** আসল request URI অপরিবর্তিত অবস্থায় যায়।

            **সমাধান:** `proxy_pass http://127.0.0.1:4000;` ব্যবহার করো, তাহলে Express পাবে `/api/products`। বিকল্প হলো slash রেখে দেওয়া, তবে সেটা তখনই ঠিক যখন তুমি **ইচ্ছা করেই** prefix কেটে Express route `/products`-এ mount করতে চাও। যেটাই করো, একটা নিয়ম বেছে নিয়ে document করো।
        """,
        quick_en=r"""The trailing slash in `proxy_pass http://127.0.0.1:4000/;` is a URI part, so NGINX replaces the matched `/api/` with `/` and Express receives `/products`. Drop it (`proxy_pass http://127.0.0.1:4000;`) to pass the original path unchanged.""",
        quick_bn=r"""`proxy_pass http://127.0.0.1:4000/;`-এর শেষের slash একটা URI part, তাই NGINX match হওয়া `/api/`-কে `/` দিয়ে replace করে, আর Express পায় `/products`। Slash-টা বাদ দাও (`proxy_pass http://127.0.0.1:4000;`), তাহলে আসল path অপরিবর্তিত যাবে।""",
        ex_en=r"""
            - **Mismatched slashes cause stranger bugs:** with `location /api` (no slash) and `proxy_pass http://127.0.0.1:4000/;`, the request `/api/products` becomes `//products`, and `/apiary` also matches the location.
            - **Regex and named locations:** NGINX can't tell which part to replace, so `proxy_pass` there must not have a URI (`nginx -t` reports an error otherwise). Use `rewrite … break` if you need to change the path.
            - **With variables** (e.g. `proxy_pass http://$backend;`), a URI given in the directive replaces the whole request URI. That's another source of surprises.
            - **Debugging trick:** compare NGINX's access log (`$request_uri`) with the backend's log, or temporarily `return 200 "$uri\n";` in the location to see what NGINX matched.
        """,
        ex_bn=r"""
            - **Slash না মিললে আরও অদ্ভুত bug:** `location /api` (slash ছাড়া) আর `proxy_pass http://127.0.0.1:4000/;` হলে `/api/products` হয়ে যায় `//products`, আর `/apiary`-ও ওই location-এর সাথে মিলে যায়।
            - **Regex আর named location:** NGINX বুঝতে পারে না কোন অংশ replace করবে, তাই সেখানে `proxy_pass`-এ URI রাখা যায় না (রাখলে `nginx -t` error দেখায়)। Path বদলাতে চাইলে `rewrite … break` ব্যবহার করো।
            - **Variable থাকলে** (যেমন `proxy_pass http://$backend;`) directive-এ দেওয়া URI পুরো request URI-কেই replace করে। এটাও বিস্ময়ের আরেকটা উৎস।
            - **Debugging-এর কৌশল:** NGINX-এর access log (`$request_uri`) আর backend-এর log মিলিয়ে দেখো, অথবা location-এ সাময়িকভাবে `return 200 "$uri\n";` দিয়ে দেখো NGINX কী match করেছে।
        """,
        tip_en=r"""State the rule in one sentence: "URI in proxy_pass means replace the matched prefix; no URI means pass it through". Then show the before/after path. Interviewers love this question because the bug is one character.""",
        tip_bn=r"""নিয়মটা এক বাক্যে বলো: "proxy_pass-এ URI থাকলে মিলে যাওয়া prefix replace হয়; URI না থাকলে যেমন আছে তেমনই যায়"। তারপর আগে/পরের path দেখাও। Interviewer-রা এই প্রশ্ন পছন্দ করে, কারণ পুরো bug-টা একটা character-এর।""",
        mist_en=r"""Adding Express rewrites to "fix" the path instead of correcting `proxy_pass`, or assuming the trailing slash is purely cosmetic.""",
        mist_bn=r"""`proxy_pass` ঠিক না করে path "ঠিক" করতে Express-এ rewrite যোগ করা, অথবা ধরে নেওয়া যে শেষের slash শুধুই দেখার ব্যাপার।""",
        follow=[
            ("How would you strip `/api` intentionally inside a regex location?", "Regex location-এর ভেতরে ইচ্ছা করে `/api` কীভাবে কেটে ফেলবে?"),
            ("Why does the SPA's `try_files` not interfere with the `/api/` location here?", "এখানে SPA-র `try_files` কেন `/api/` location-এ হস্তক্ষেপ করে না?"),
        ],
        related=["nginx-012", "nginx-002"],
        refs=[N_PROXY, N_HTTP_CORE],
    ),
    # ------------------------------------------------------------------ nginx-023
    Q(
        id="nginx-023", sub="Caching", diff="hard", type="coding",
        prio="medium", market="both", mins=12,
        tags=["proxy_cache", "microcaching", "cache-stampede", "stale", "performance"],
        ver="NGINX 1.30 stable / 1.31 mainline", vs=False, status="stable",
        q_en=r"""
            Your public `GET /api/products` endpoint (Node.js) is hammered during sales campaigns. The data may be up to 10 seconds stale, but requests from logged-in users (an `Authorization` header or a `session` cookie) must never be cached.

            Write the NGINX config to:
            - micro-cache successful responses for 10 seconds;
            - send only **one** request to Node when a cache entry is missing or expired (no stampede);
            - serve stale content if Node errors or times out;
            - expose whether a response was a cache HIT/MISS.
        """,
        q_bn=r"""
            Sale campaign-এর সময় তোমার public `GET /api/products` endpoint (Node.js)-এ প্রচণ্ড চাপ পড়ে। Data সর্বোচ্চ ১০ সেকেন্ড পুরনো হলেও চলবে, কিন্তু logged-in user-দের request (`Authorization` header বা `session` cookie থাকলে) কখনো cache করা যাবে না।

            এমন NGINX config লেখো যা:
            - সফল response ১০ সেকেন্ডের জন্য micro-cache করবে;
            - cache entry না থাকলে বা expire হলে Node-এ মাত্র **একটা** request পাঠাবে (কোনো stampede নয়);
            - Node error দিলে বা timeout হলে stale content serve করবে;
            - response cache HIT না MISS ছিল সেটা দেখাবে।
        """,
        code=r"""
            http {
                proxy_cache_path /var/cache/nginx/api levels=1:2 keys_zone=api_cache:50m
                                 max_size=2g inactive=10m use_temp_path=off;

                # 1 = skip the cache when the request carries credentials
                map $http_authorization$cookie_session $skip_cache {
                    default 1;
                    ""      0;
                }

                upstream app {
                    server 127.0.0.1:3000;
                }

                server {
                    listen 443 ssl;
                    http2 on;
                    server_name shop.example.com;
                    # ssl_certificate ... ;

                    location = /api/products {
                        proxy_pass http://app;
                        proxy_set_header Host $host;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_set_header X-Forwarded-Proto $scheme;

                        proxy_cache            api_cache;
                        proxy_cache_key        "$scheme$request_method$host$request_uri";
                        proxy_cache_valid      200 10s;
                        proxy_cache_valid      404 5s;

                        proxy_cache_lock       on;            # one request fills a missing entry
                        proxy_cache_use_stale  error timeout updating http_500 http_502 http_503 http_504;
                        proxy_cache_background_update on;     # refresh expired entries in the background

                        proxy_cache_bypass     $skip_cache;   # don't serve from cache
                        proxy_no_cache         $skip_cache;   # don't store in cache

                        add_header X-Cache-Status $upstream_cache_status always;
                    }
                }
            }
        """,
        lang="nginx",
        time="O(1) cache lookup per request (hashed key in shared memory)", space="O(entries): keys in keys_zone, bodies on disk up to max_size",
        a_en=r"""
            - **`proxy_cache_path`** defines the on-disk cache and a shared-memory **keys zone** (`api_cache:50m` holds the keys and metadata; bodies live on disk, capped by `max_size`). `inactive=10m` evicts entries that nobody requested for 10 minutes.
            - **`proxy_cache_valid 200 10s`** is the micro-cache TTL. Even 1–10 seconds collapses thousands of identical requests per second into a handful of upstream calls.
            - **Stampede protection:** `proxy_cache_lock on` lets only one request populate a missing entry while the others wait. `proxy_cache_use_stale updating` plus `proxy_cache_background_update on` serve the old copy while a single background request refreshes an expired one.
            - **Resilience:** `proxy_cache_use_stale error timeout http_5xx` keeps the catalogue online if Node fails.
            - **Never cache personal data:** the `map` sets `$skip_cache` to 1 when an `Authorization` header or a `session` cookie is present. `proxy_cache_bypass` skips reading the cache, and `proxy_no_cache` skips storing.
            - **Observability:** `$upstream_cache_status` (HIT, MISS, EXPIRED, STALE, UPDATING, BYPASS) in a header and in access logs.
        """,
        a_bn=r"""
            - **`proxy_cache_path`** disk-এ cache আর একটা shared-memory **keys zone** define করে (`api_cache:50m`-এ key আর metadata থাকে; body থাকে disk-এ, `max_size` পর্যন্ত)। `inactive=10m` মানে ১০ মিনিট কেউ request না করা entry সরিয়ে দেওয়া হয়।
            - **`proxy_cache_valid 200 10s`** হলো micro-cache-এর TTL। মাত্র ১–১০ সেকেন্ডও প্রতি সেকেন্ডের হাজার হাজার একই request-কে অল্প কয়েকটা upstream call-এ নামিয়ে আনে।
            - **Stampede থেকে সুরক্ষা:** `proxy_cache_lock on` থাকলে না-থাকা entry পূরণ করে শুধু একটা request, বাকিরা অপেক্ষা করে। `proxy_cache_use_stale updating` আর `proxy_cache_background_update on` মিলে expire হওয়া entry-র পুরনো copy serve করে, আর background-এ একটা মাত্র request সেটা refresh করে।
            - **Resilience:** Node fail করলেও `proxy_cache_use_stale error timeout http_5xx` catalogue online রাখে।
            - **ব্যক্তিগত data কখনো cache নয়:** `Authorization` header বা `session` cookie থাকলে `map` `$skip_cache`-কে 1 করে দেয়। `proxy_cache_bypass` cache থেকে পড়া বাদ দেয়, আর `proxy_no_cache` store করা বাদ দেয়।
            - **Observability:** `$upstream_cache_status` (HIT, MISS, EXPIRED, STALE, UPDATING, BYPASS) header-এ আর access log-এ।
        """,
        quick_en=r"""Cache 200s for 10 seconds in a `proxy_cache_path` zone, with `proxy_cache_lock on` against stampedes and `proxy_cache_use_stale` for errors and updates. A `map` on the `Authorization` header and session cookie feeds `proxy_cache_bypass`/`proxy_no_cache`, and `$upstream_cache_status` shows HIT or MISS.""",
        quick_bn=r"""একটা `proxy_cache_path` zone-এ 200 response ১০ সেকেন্ড cache করো; stampede ঠেকাতে `proxy_cache_lock on`, আর error ও update-এর সময় `proxy_cache_use_stale`। `Authorization` header আর session cookie-র উপর একটা `map` `proxy_cache_bypass`/`proxy_no_cache` চালায়, আর `$upstream_cache_status` দেখায় HIT না MISS।""",
        ex_en=r"""
            - **Upstream headers win:** `Cache-Control: no-store/private`, `Expires` or `X-Accel-Expires` from Node override `proxy_cache_valid`. By default, responses with `Set-Cookie` aren't cached, and only `GET`/`HEAD` are cached. Never add `proxy_ignore_headers Set-Cookie` without understanding that it can cache one user's cookie for everyone.
            - **Cache key design:** include everything that changes the response (scheme, host, full URI with query string). If the response depends on a header such as language, add it to the key or rely on `Vary`.
            - **Purging:** `proxy_cache_purge` is an NGINX Plus feature. In open source, use short TTLs, versioned URLs/keys, or a third-party purge module.
            - **Edge cases:** keep `keys_zone` big enough (roughly 8,000 keys per MB) and put the cache on fast disk. Also watch `$upstream_cache_status` ratios after deploys.
        """,
        ex_bn=r"""
            - **Upstream header-ই জেতে:** Node থেকে আসা `Cache-Control: no-store/private`, `Expires` বা `X-Accel-Expires` `proxy_cache_valid`-কে override করে। Default হিসেবে `Set-Cookie` থাকা response cache হয় না, আর শুধু `GET`/`HEAD` cache হয়। না বুঝে কখনো `proxy_ignore_headers Set-Cookie` যোগ কোরো না, এতে একজনের cookie সবার জন্য cache হয়ে যেতে পারে।
            - **Cache key design:** response বদলায় এমন সবকিছু key-তে রাখো (scheme, host, query string-সহ পুরো URI)। Response কোনো header-এর উপর নির্ভর করলে (যেমন ভাষা), সেটা key-তে যোগ করো বা `Vary`-এর উপর ভরসা করো।
            - **Purge:** `proxy_cache_purge` NGINX Plus-এর feature। Open source-এ ছোট TTL, versioned URL/key বা third-party purge module ব্যবহার করো।
            - **Edge case:** `keys_zone` যথেষ্ট বড় রাখো (প্রতি MB-তে মোটামুটি ৮,০০০ key), cache দ্রুত disk-এ রাখো। Deploy-এর পরে `$upstream_cache_status`-এর অনুপাতও নজরে রাখো।
        """,
        tip_en=r"""Explain the three separate concerns, freshness (TTL), stampede (lock and background update) and safety (bypass for authenticated users), before you write directives. Ending with "upstream `Cache-Control` and `Set-Cookie` override this" shows you know the sharp edges.""",
        tip_bn=r"""Directive লেখার আগে তিনটা আলাদা বিষয় ব্যাখ্যা করো: freshness (TTL), stampede (lock আর background update) আর safety (authenticated user-এর জন্য bypass)। শেষে "upstream-এর `Cache-Control` আর `Set-Cookie` এটাকে override করে" বললে বোঝা যায় তুমি ধারালো কোণগুলোও জানো।""",
        mist_en=r"""Caching responses for logged-in users, forgetting `proxy_no_cache` (bypassed responses still get stored), using a huge TTL for "performance", and ignoring `Set-Cookie`.""",
        mist_bn=r"""Logged-in user-দের response cache করা, `proxy_no_cache` ভুলে যাওয়া (bypass করা response-ও তখন store হয়ে যায়), "performance"-এর জন্য বিশাল TTL দেওয়া, আর `Set-Cookie` উপেক্ষা করা।""",
        follow=[
            ("How would you invalidate the product cache immediately after an admin edits a price?", "Admin দাম বদলানোর সাথে সাথে product cache কীভাবে invalidate করবে?"),
            ("What's the difference between `proxy_cache_bypass` and `proxy_no_cache`?", "`proxy_cache_bypass` আর `proxy_no_cache`-এর মধ্যে পার্থক্য কী?"),
        ],
        related=["nginx-013"],
        refs=[N_PROXY, N_MAP],
    ),
    # ------------------------------------------------------------------ nginx-030
    Q(
        id="nginx-030", sub="Deployment Architecture", diff="extreme", type="system-design",
        prio="medium", market="both", mins=25,
        tags=["system-design", "cdn", "load-balancing", "flash-sale", "rate-limiting", "microcaching"],
        ver="NGINX 1.30 stable (keepalive-to-upstream default since 1.29.7)", vs=True, status="stable",
        q_en=r"""An e-commerce company expects a 20× traffic spike during a midnight flash sale. The stack is a Next.js storefront and a Node.js API on a few VMs, with PostgreSQL and Redis. Design the edge and NGINX layer (CDN → NGINX → app replicas) so the site stays up, checkout stays fair and the database survives.""",
        q_bn=r"""একটা e-commerce company মধ্যরাতের flash sale-এ স্বাভাবিকের ২০ গুণ traffic আশা করছে। Stack হলো কয়েকটা VM-এ একটা Next.js storefront আর একটা Node.js API, সাথে PostgreSQL আর Redis। Edge আর NGINX layer (CDN → NGINX → app replica) এমনভাবে design করো যাতে site চালু থাকে, checkout ন্যায্য থাকে আর database টিকে থাকে।""",
        a_en=r"""
            **(Advanced, senior system design.)** First I'd clarify the numbers: peak requests per second, the read/write mix (browsing is ~95% reads; checkout is the scarce write path), inventory size and acceptable staleness.

            **Layered design:**
            1. **CDN (Cloudflare/CloudFront):** serves all static assets (`/_next/static`, images) with long immutable caching, absorbs bots and DDoS, and terminates TLS close to users. Product and category pages can be edge-cached for a few seconds.
            2. **Load balancer tier:** two or more NGINX nodes behind a cloud LB (or a keepalived floating IP), so NGINX isn't a single point of failure.
            3. **NGINX:** real client IP, rate limits, micro-caching, load balancing and timeouts (details below).
            4. **App tier:** stateless Node replicas (sessions and carts in Redis), pre-scaled **before** midnight because autoscaling reacts too slowly to a cliff-edge spike.
            5. **Checkout fairness and DB protection:** atomic stock reservation in Redis (`DECR`/Lua) before hitting Postgres; a queue or virtual waiting room when checkout concurrency exceeds what the DB can commit; idempotency keys for payment callbacks.
            6. **Observability:** NGINX logs with `$request_time` and `$upstream_response_time`, `stub_status` metrics, cache hit ratio, 429/5xx rates and dashboards, plus a load test at 2× the expected peak beforehand.

            **NGINX layer details:**
            - **Real client IP** from the CDN (`set_real_ip_from` the CDN ranges, `real_ip_header`); otherwise every limit sees the CDN's IP.
            - **Rate limits** per IP for the API and a tighter per-session limit on `/checkout`, returning 429.
            - **Micro-caching** (1–5 s) of public catalogue APIs with `proxy_cache_lock` and `use_stale`, so a 20× spike becomes a few upstream requests per second.
            - **`least_conn` load balancing** with upstream keepalive (on by default since 1.29.7) and passive health checks (`max_fails`/`fail_timeout`).
            - **Tight timeouts**, and no retries for non-idempotent requests (NGINX's default).
        """,
        a_bn=r"""
            **(Advanced, senior system design।)** প্রথমে আমি সংখ্যাগুলো পরিষ্কার করব: peak-এ প্রতি সেকেন্ডে কত request, read/write-এর অনুপাত (browsing প্রায় ৯৫% read; checkout হলো দুর্লভ write path), inventory-র আকার, আর কতটা পুরনো data চলবে।

            **স্তরভিত্তিক design:**
            1. **CDN (Cloudflare/CloudFront):** সব static asset (`/_next/static`, image) দীর্ঘমেয়াদি immutable caching-সহ serve করে, bot আর DDoS সামলায়, আর user-এর কাছাকাছি TLS terminate করে। Product আর category page কয়েক সেকেন্ডের জন্য edge-এ cache করা যায়।
            2. **Load balancer tier:** একটা cloud LB (বা keepalived floating IP)-এর পেছনে দুই বা ততোধিক NGINX node, যাতে NGINX single point of failure না হয়।
            3. **NGINX:** আসল client IP, rate limit, micro-caching, load balancing আর timeout (বিস্তারিত নিচে)।
            4. **App tier:** stateless Node replica (session আর cart Redis-এ), মধ্যরাতের **আগেই** pre-scale করা, কারণ হঠাৎ খাড়া spike-এ autoscaling খুব দেরিতে সাড়া দেয়।
            5. **Checkout-এর ন্যায্যতা আর DB-র সুরক্ষা:** Postgres-এ যাওয়ার আগে Redis-এ atomic stock reservation (`DECR`/Lua); DB যতটা commit করতে পারে checkout-এর concurrency তার বেশি হলে একটা queue বা virtual waiting room; payment callback-এর জন্য idempotency key।
            6. **Observability:** `$request_time` আর `$upstream_response_time`-সহ NGINX log, `stub_status` metrics, cache hit ratio, 429/5xx-এর হার আর dashboard। আর আগেই প্রত্যাশিত peak-এর দ্বিগুণে একটা load test।

            **NGINX layer-এর বিস্তারিত:**
            - CDN থেকে **আসল client IP** (CDN-এর range-গুলো `set_real_ip_from`-এ, সাথে `real_ip_header`); নইলে প্রতিটা limit শুধু CDN-এর IP দেখবে।
            - API-র জন্য প্রতি IP-তে **rate limit**, আর `/checkout`-এ প্রতি session-এ আরও কড়া limit, যেটা 429 ফেরত দেয়।
            - Public catalogue API-র **micro-caching** (১–৫ সেকেন্ড), `proxy_cache_lock` আর `use_stale`-সহ, যাতে ২০ গুণ spike প্রতি সেকেন্ডে অল্প কয়েকটা upstream request-এ নেমে আসে।
            - Upstream keepalive (1.29.7 থেকে default চালু) আর passive health check (`max_fails`/`fail_timeout`)-সহ **`least_conn` load balancing**।
            - **কড়া timeout**, আর non-idempotent request-এ retry নয় (NGINX-এর default)।
        """,
        quick_en=r"""Layer it: a CDN for static assets and bot or DDoS traffic, redundant NGINX nodes doing real-IP, rate limits, micro-caching and `least_conn`, and stateless app replicas pre-scaled before midnight. Protect checkout and the database with atomic Redis stock reservation, a queue or waiting room and idempotency keys.""",
        quick_bn=r"""Layer করে সাজাও: static asset আর bot বা DDoS traffic-এর জন্য CDN, একাধিক NGINX node যারা real IP, rate limit, micro-caching আর `least_conn` সামলায়, আর মাঝরাতের আগেই scale করে রাখা stateless app replica। Checkout আর database বাঁচাতে Redis-এ atomic stock reservation, queue বা waiting room আর idempotency key ব্যবহার করো।""",
        ex_en=r"""
            **Failure scenarios:**
            - **Node replica dies:** passive health checks stop sending traffic to it after `max_fails`, and the others absorb the load. Without active checks (NGINX Plus), the first failures still hit real users. Keep timeouts short.
            - **Origin overloaded:** micro-cache plus `proxy_cache_use_stale` keep browsing alive, and rate limits shed abusive load with 429 instead of letting everything time out.
            - **Postgres saturated:** the waiting room caps concurrent checkouts, and read replicas or Redis caches serve product reads.
            - **An NGINX node dies:** the LB health check removes it.
            - **Bad deploy during the sale:** a deploy freeze, with rollback by switching back the upstream.

            **Trade-offs:** more caching means staler prices and stock counts, so show "only N left" from Redis, not from the cached page. Per-IP limits hurt users behind carrier-grade NAT, so use per-session/per-user limits for logged-in flows.
        """,
        ex_bn=r"""
            **Failure scenario:**
            - **একটা Node replica মারা গেল:** `max_fails`-এর পরে passive health check সেটায় traffic পাঠানো বন্ধ করে, বাকিরা চাপ সামলায়। Active check (NGINX Plus) না থাকায় প্রথম কয়েকটা failure আসল user-দের গায়েই লাগে। Timeout ছোট রাখো।
            - **Origin overload:** micro-cache আর `proxy_cache_use_stale` browsing চালু রাখে, আর rate limit সবকিছু timeout হতে না দিয়ে অপব্যবহারকারী load 429 দিয়ে ঝেড়ে ফেলে।
            - **Postgres saturated:** waiting room একসাথে কতগুলো checkout হবে তার সীমা বেঁধে দেয়, আর read replica বা Redis cache product read serve করে।
            - **একটা NGINX node মারা গেল:** LB-এর health check সেটাকে সরিয়ে দেয়।
            - **Sale চলাকালীন খারাপ deploy:** deploy freeze রাখো, আর upstream আগের অবস্থায় ফিরিয়ে rollback করো।

            **Trade-off:** caching বেশি হলে দাম আর stock-এর সংখ্যা বেশি পুরনো দেখায়, তাই "আর মাত্র Nটা বাকি" cached page থেকে না দেখিয়ে Redis থেকে দেখাও। Carrier-grade NAT-এর পেছনে থাকা user-রা per-IP limit-এ ক্ষতিগ্রস্ত হয়, তাই logged-in flow-তে per-session/per-user limit ব্যবহার করো।
        """,
        tip_en=r"""Structure it as requirements → layers (edge, proxy, app, data) → failure scenarios → trade-offs, and draw the request path. Name concrete numbers (TTL 1–5 s, a 429 limit) so the design feels real, not generic.""",
        tip_bn=r"""এভাবে সাজাও: requirement → layer (edge, proxy, app, data) → failure scenario → trade-off, আর request-এর পথটা এঁকে দেখাও। নির্দিষ্ট সংখ্যা বলো (TTL ১–৫ সেকেন্ড, একটা 429 limit), যাতে design-টা বাস্তব মনে হয়, গৎবাঁধা না।""",
        mist_en=r"""Relying on autoscaling alone for a cliff-edge spike, rate-limiting on the CDN's IP instead of the real client IP, and caching personalised or checkout responses.""",
        mist_bn=r"""হঠাৎ খাড়া spike-এর জন্য শুধু autoscaling-এর উপর ভরসা করা, আসল client IP-র বদলে CDN-এর IP দিয়ে rate-limit করা, আর personalised বা checkout response cache করা।""",
        code=r"""
            http {
                # Real client IP from the CDN (use the CDN's published ranges)
                set_real_ip_from  203.0.113.0/24;
                real_ip_header    X-Forwarded-For;
                real_ip_recursive on;

                limit_req_zone $binary_remote_addr zone=api_ip:20m      rate=20r/s;
                limit_req_zone $cookie_session     zone=checkout_s:10m  rate=2r/s;
                limit_req_status 429;

                proxy_cache_path /var/cache/nginx/catalog keys_zone=catalog:50m max_size=1g inactive=5m;

                upstream app {
                    least_conn;
                    server 10.0.1.11:3000 max_fails=3 fail_timeout=10s;
                    server 10.0.1.12:3000 max_fails=3 fail_timeout=10s;
                    server 10.0.1.13:3000 max_fails=3 fail_timeout=10s;
                    keepalive 64;              # default is 32 per worker since 1.29.7
                }

                server {
                    listen 443 ssl;
                    http2 on;
                    server_name shop.example.com;

                    location /api/catalog/ {
                        limit_req zone=api_ip burst=40 nodelay;
                        proxy_cache catalog;
                        proxy_cache_valid 200 3s;
                        proxy_cache_lock on;
                        proxy_cache_use_stale error timeout updating http_502 http_503 http_504;
                        proxy_pass http://app;
                    }

                    location /api/checkout/ {
                        limit_req zone=checkout_s burst=5;
                        limit_req zone=api_ip burst=20 nodelay;
                        proxy_read_timeout 15s;
                        proxy_pass http://app;     # never cached; POSTs are not retried by default
                    }

                    location = /nginx_status {
                        stub_status;
                        allow 10.0.0.0/8;
                        deny all;
                    }
                }
            }
        """,
        lang="nginx",
        follow=[
            ("How would you implement a virtual waiting room in front of checkout?", "Checkout-এর সামনে একটা virtual waiting room কীভাবে implement করবে?"),
            ("How do you prevent overselling when thousands of users buy the last 100 items at once?", "হাজার হাজার user একসাথে শেষ ১০০টা item কিনতে চাইলে overselling কীভাবে আটকাবে?"),
            ("Why might per-IP rate limiting be unfair to some users?", "Per-IP rate limiting কেন কিছু user-এর প্রতি অন্যায্য হতে পারে?"),
        ],
        related=["nginx-023", "nginx-001"],
        refs=[N_REALIP, N_LIMIT_REQ, N_UPSTREAM],
    ),
]

if __name__ == "__main__":
    save("nginx", "b1", QUESTIONS)
