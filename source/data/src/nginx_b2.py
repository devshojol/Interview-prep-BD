# NGINX — batch 2: nginx-005..007 (easy), nginx-014..016 (medium), nginx-024 (hard), nginx-031 (extreme)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

N_PROXY = ("NGINX — ngx_http_proxy_module", "https://nginx.org/en/docs/http/ngx_http_proxy_module.html")
N_UPSTREAM = ("NGINX — ngx_http_upstream_module", "https://nginx.org/en/docs/http/ngx_http_upstream_module.html")
N_HTTP_CORE = ("NGINX — ngx_http_core_module", "https://nginx.org/en/docs/http/ngx_http_core_module.html")
N_BEGIN = ("NGINX — Beginner's Guide", "https://nginx.org/en/docs/beginners_guide.html")
N_CONTROL = ("NGINX — Controlling nginx", "https://nginx.org/en/docs/control.html")
N_WS = ("NGINX — WebSocket proxying", "https://nginx.org/en/docs/http/websocket.html")
N_MAP = ("NGINX — ngx_http_map_module", "https://nginx.org/en/docs/http/ngx_http_map_module.html")
N_SPLIT = ("NGINX — ngx_http_split_clients_module", "https://nginx.org/en/docs/http/ngx_http_split_clients_module.html")
N_CORE_MAIN = ("NGINX — Core functionality (worker_shutdown_timeout)", "https://nginx.org/en/docs/ngx_core_module.html")
EXPRESS_PROXY = ("Express — Behind proxies (trust proxy)", "https://expressjs.com/en/guide/behind-proxies.html")
D_NETWORK = ("Docker Docs — Networking overview", "https://docs.docker.com/engine/network/")
MDN_XFF = ("MDN — X-Forwarded-For", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Forwarded-For")

QUESTIONS = [
    # ------------------------------------------------------------------ nginx-005
    Q(
        id="nginx-005", sub="NGINX with Node.js", diff="easy", type="coding",
        prio="high", market="bangladesh", mins=5,
        tags=["reverse-proxy", "server-block", "proxy_pass", "express", "vps"],
        ver="NGINX 1.30 stable / 1.31 mainline (notes for older distro packages)", vs=True, status="stable",
        q_en=r"""
            Your Express API listens on `127.0.0.1:3000` on an Ubuntu VPS. Write an NGINX server block for `api.example.com` that:
            - reverse-proxies every request to the app;
            - passes the original host, the client's IP and the original protocol to Express;
            - accepts request bodies up to 10 MB;
            - writes separate access and error logs for this site.
        """,
        q_bn=r"""
            Ubuntu VPS-এ তোমার Express API `127.0.0.1:3000`-এ listen করছে। `api.example.com`-এর জন্য এমন একটা NGINX server block লেখো যা:
            - প্রতিটা request app-এ reverse-proxy করবে;
            - আসল host, client-এর IP আর আসল protocol Express-কে পাঠাবে;
            - 10 MB পর্যন্ত request body গ্রহণ করবে;
            - এই site-এর জন্য আলাদা access আর error log লিখবে।
        """,
        code=r"""
            # /etc/nginx/sites-available/api.example.com   (Debian/Ubuntu layout)
            upstream api_backend {
                server 127.0.0.1:3000;
            }

            server {
                listen 80;
                listen [::]:80;
                server_name api.example.com;

                access_log /var/log/nginx/api.access.log;
                error_log  /var/log/nginx/api.error.log warn;

                client_max_body_size 10m;

                location / {
                    proxy_pass http://api_backend;
                    proxy_set_header Host              $host;
                    proxy_set_header X-Real-IP         $remote_addr;
                    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;
                }
            }
        """,
        lang="nginx",
        extra=[
            dict(lang="bash", label_en="Enable and test", label_bn="Enable আর test করা", src=r"""
                sudo ln -s /etc/nginx/sites-available/api.example.com /etc/nginx/sites-enabled/
                sudo nginx -t && sudo systemctl reload nginx
                curl -I http://api.example.com/health
                # next step: HTTPS with certbot (see the HTTPS question)
            """),
            dict(lang="nginx", label_en="Only on NGINX older than 1.29.7 (e.g. many distro packages): enable upstream keepalive explicitly", label_bn="শুধু 1.29.7-এর পুরনো NGINX-এ (যেমন অনেক distro package): upstream keepalive নিজে চালু করতে হয়", src=r"""
                upstream api_backend {
                    server 127.0.0.1:3000;
                    keepalive 16;
                }
                # inside location /:
                #   proxy_http_version 1.1;
                #   proxy_set_header Connection "";
            """),
        ],
        time="N/A (configuration)", space="N/A",
        a_en=r"""
            - **`upstream api_backend`** names the backend, which makes it easy to add more Node instances later. Since NGINX 1.29.7 (so in 1.30 stable), upstream groups keep a pool of idle **keepalive** connections by default and proxy with HTTP/1.1, so Node isn't paying for a new TCP connection per request.
            - **`server_name` + `listen 80`** selects this virtual host for `api.example.com` over IPv4 and IPv6.
            - **`client_max_body_size 10m`** raises the 1 MB default that would otherwise return 413.
            - **`proxy_pass http://api_backend`**, with no URI part, forwards the path unchanged.
            - **`proxy_set_header Host $host`** passes the real hostname. By default NGINX sends the upstream's name instead.
            - **`X-Real-IP` and `X-Forwarded-For`** carry the client IP, and **`X-Forwarded-Proto`** tells Express whether the original request was HTTPS. In Express, set `app.set('trust proxy', 1)` so `req.ip` and `req.secure` use them.
            - **Per-site logs** make debugging one app on a shared server much easier.

            The app itself stays bound to `127.0.0.1`, so the only public entry point is NGINX.
        """,
        a_bn=r"""
            - **`upstream api_backend`** backend-কে একটা নাম দেয়, ফলে পরে আরও Node instance যোগ করা সহজ হয়। NGINX 1.29.7 থেকে (অর্থাৎ 1.30 stable-এ) upstream group default হিসেবে idle **keepalive** connection-এর একটা pool রাখে আর HTTP/1.1 দিয়ে proxy করে। ফলে Node-কে প্রতি request-এ নতুন TCP connection-এর খরচ দিতে হয় না।
            - **`server_name` + `listen 80`** IPv4 আর IPv6-এ `api.example.com`-এর জন্য এই virtual host বেছে নেয়।
            - **`client_max_body_size 10m`** 1 MB-এর default বাড়ায়, নইলে 413 আসত।
            - **`proxy_pass http://api_backend`**-এ URI অংশ নেই, তাই path অপরিবর্তিত অবস্থায় যায়।
            - **`proxy_set_header Host $host`** আসল hostname পাঠায়। Default হিসেবে NGINX এর বদলে upstream-এর নাম পাঠায়।
            - **`X-Real-IP` আর `X-Forwarded-For`** client-এর IP বহন করে, আর **`X-Forwarded-Proto`** Express-কে জানায় আসল request HTTPS ছিল কি না। Express-এ `app.set('trust proxy', 1)` set করো, যাতে `req.ip` আর `req.secure` এগুলো ব্যবহার করে।
            - **প্রতিটা site-এর আলাদা log** shared server-এ একটা app debug করা অনেক সহজ করে।

            App নিজে `127.0.0.1`-এ bind থাকে, তাই public প্রবেশপথ একটাই, NGINX।
        """,
        ex_en=r"""
            - **Check your version:** distribution packages (e.g. Ubuntu LTS) often ship an older NGINX than 1.30. Run `nginx -v`. On versions before 1.29.7 you must add `keepalive` plus `proxy_http_version 1.1` and `proxy_set_header Connection ""` yourself, as in the extra block. The official `nginx.org` repositories provide current stable and mainline builds.
            - **Firewall:** allow only 80/443 (and SSH) publicly, e.g. `ufw allow 'Nginx Full'`. Port 3000 should never be open.
            - **Next steps:** add HTTPS (certbot), sensible timeouts, gzip, and process management for Node (systemd or PM2) so the app restarts on crashes and on boot.
        """,
        ex_bn=r"""
            - **Version দেখে নাও:** distribution package (যেমন Ubuntu LTS) প্রায়ই 1.30-এর চেয়ে পুরনো NGINX দেয়। `nginx -v` চালাও। 1.29.7-এর আগের version-এ `keepalive` আর সাথে `proxy_http_version 1.1` ও `proxy_set_header Connection ""` নিজেকেই যোগ করতে হয়, extra block-এ যেমন দেখানো আছে। Official `nginx.org` repository-তে বর্তমান stable আর mainline build পাওয়া যায়।
            - **Firewall:** public-ভাবে শুধু 80/443 (আর SSH) খোলা রাখো, যেমন `ufw allow 'Nginx Full'`। Port 3000 কখনো খোলা থাকা উচিত না।
            - **পরের ধাপ:** HTTPS (certbot), যুক্তিসঙ্গত timeout, gzip, আর Node-এর জন্য process management (systemd বা PM2) যোগ করো, যাতে crash বা boot-এর পরে app নিজে থেকে restart হয়।
        """,
        tip_en=r"""Explain **why** each header exists, not just that it's there. Then mention checking `nginx -v`, because defaults changed in 1.29.7. Version awareness stands out in interviews.""",
        tip_bn=r"""প্রতিটা header **কেন** আছে সেটা ব্যাখ্যা করো, শুধু আছে বলেই থেমো না। তারপর `nginx -v` দেখার কথা বলো, কারণ 1.29.7-এ default বদলেছে। Interview-এ version-সচেতনতা আলাদাভাবে চোখে পড়ে।""",
        mist_en=r"""Leaving Node listening on `0.0.0.0:3000` with the port open, forgetting `Host`/`X-Forwarded-Proto` (broken redirects and secure cookies), and editing `nginx.conf` directly without `nginx -t`.""",
        mist_bn=r"""Port খোলা রেখে Node-কে `0.0.0.0:3000`-এ listen করতে দেওয়া, `Host`/`X-Forwarded-Proto` ভুলে যাওয়া (redirect আর secure cookie ভেঙে যায়), আর `nginx -t` ছাড়াই সরাসরি `nginx.conf` edit করা।""",
        follow=[
            ("How would you add a second Node.js instance and balance between them?", "দ্বিতীয় একটা Node.js instance যোগ করে দুটোর মধ্যে কীভাবে load balance করবে?"),
            ("Why does Express need `trust proxy` behind NGINX?", "NGINX-এর পেছনে Express-এর `trust proxy` কেন লাগে?"),
        ],
        related=["nginx-002", "nginx-004", "nginx-013"],
        refs=[N_PROXY, N_UPSTREAM, EXPRESS_PROXY],
    ),
    # ------------------------------------------------------------------ nginx-006
    Q(
        id="nginx-006", sub="SPA Fallback", diff="easy", type="debugging",
        prio="high", market="both", mins=4,
        tags=["spa", "try_files", "react", "404", "static-files"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""
            A React (Vite) single-page app is deployed with this config. The home page works and clicking around works, but refreshing the browser on `/dashboard/settings`, or opening a shared link to it, shows NGINX's 404 page. Fix it without breaking 404s for missing JS/CSS files.
        """,
        q_bn=r"""
            একটা React (Vite) single-page app এই config দিয়ে deploy করা হয়েছে। Home page কাজ করে, link-এ click করেও ঘোরা যায়, কিন্তু `/dashboard/settings`-এ browser refresh করলে বা এর share করা link খুললে NGINX-এর 404 page দেখায়। Missing JS/CSS file-এর 404 না ভেঙে এটা ঠিক করো।
        """,
        code=r"""
            server {
                listen 80;
                server_name app.example.com;
                root /var/www/app/dist;
                index index.html;

                location / {
                    try_files $uri =404;
                }
            }
        """,
        lang="nginx",
        extra=[
            dict(lang="nginx", label_en="Fixed config", label_bn="সংশোধিত config", src=r"""
                server {
                    listen 80;
                    server_name app.example.com;
                    root /var/www/app/dist;
                    index index.html;

                    # Real build assets: a missing file must stay a real 404
                    location /assets/ {
                        try_files $uri =404;
                    }

                    # API calls go to the backend, never to index.html
                    location /api/ {
                        proxy_pass http://127.0.0.1:3000;
                    }

                    # Everything else is a client-side route: serve the SPA shell
                    location / {
                        try_files $uri $uri/ /index.html;
                    }
                }
            """),
        ],
        a_en=r"""
            In an SPA, routes like `/dashboard/settings` exist only in **client-side JavaScript** (the History API). When you click a link, React Router changes the URL without asking the server. When you refresh, the browser requests `/dashboard/settings` from NGINX, there's no such file, and `try_files $uri =404` returns 404.

            **Fix:** `try_files $uri $uri/ /index.html;`. NGINX serves the file if it exists, then a directory, otherwise it does an internal redirect to `/index.html` (status 200). The SPA boots and the router renders the right page.

            Keep a separate `location /assets/ { try_files $uri =404; }`. Otherwise a missing chunk would get `index.html` back, and the browser would fail with a confusing MIME-type or "Unexpected token '<'" error instead of a clear 404. Proxy `/api/` separately so API 404s stay API 404s.
        """,
        a_bn=r"""
            SPA-তে `/dashboard/settings`-এর মতো route শুধু **client-side JavaScript**-এ থাকে (History API)। Link-এ click করলে React Router server-কে না জিজ্ঞেস করেই URL বদলে দেয়। কিন্তু refresh করলে browser NGINX-এর কাছে `/dashboard/settings` চায়, এমন কোনো file নেই, তাই `try_files $uri =404` 404 দেয়।

            **সমাধান:** `try_files $uri $uri/ /index.html;`। File থাকলে NGINX সেটা serve করে, তারপর directory দেখে, না পেলে `/index.html`-এ internal redirect করে (status 200)। SPA boot হয়, আর router সঠিক page render করে।

            আলাদা একটা `location /assets/ { try_files $uri =404; }` রাখো। নইলে কোনো chunk না থাকলে `index.html` ফেরত যাবে, আর browser পরিষ্কার 404-এর বদলে বিভ্রান্তিকর MIME-type বা "Unexpected token '<'" error দেবে। `/api/` আলাদাভাবে proxy করো, যাতে API-র 404 API-র 404-ই থাকে।
        """,
        ex_en=r"""
            - **Why the error is confusing without the assets rule:** after a new deploy, old hashed chunks are deleted. A user with the old `index.html` asks for `/assets/index-abc123.js`, gets HTML back, and the app crashes with a cryptic error.
            - **True 404 pages:** with this fallback, NGINX never returns 404 for unknown routes. The SPA should render its own "Not found" page. For SEO-critical sites, consider SSR or prerendering so crawlers get real status codes.
            - **Next.js is different:** a Next.js app with SSR runs on Node, so you proxy to it rather than using `try_files`. The SPA pattern applies only to a static export (`output: 'export'`).
            - **Caching:** pair this with `Cache-Control: no-cache` for `index.html` and long immutable caching for `/assets/`.
        """,
        ex_bn=r"""
            - **Assets rule ছাড়া error কেন বিভ্রান্তিকর:** নতুন deploy-এর পর পুরনো hashed chunk মুছে যায়। পুরনো `index.html`-ওয়ালা একজন user `/assets/index-abc123.js` চায়, ফেরত পায় HTML, আর app একটা দুর্বোধ্য error দিয়ে crash করে।
            - **সত্যিকারের 404 page:** এই fallback থাকলে অচেনা route-এ NGINX কখনো 404 দেয় না। SPA-কে নিজের "Not found" page render করতে হবে। SEO-গুরুত্বপূর্ণ site-এ SSR বা prerendering ভাবো, যাতে crawler আসল status code পায়।
            - **Next.js আলাদা:** SSR-ওয়ালা Next.js app Node-এ চলে, তাই `try_files` না দিয়ে সেখানে proxy করতে হয়। SPA pattern শুধু static export (`output: 'export'`)-এর ক্ষেত্রে খাটে।
            - **Caching:** এর সাথে `index.html`-এর জন্য `Cache-Control: no-cache` আর `/assets/`-এর জন্য দীর্ঘমেয়াদি immutable caching রাখো।
        """,
        tip_en=r"""Explain the client-side vs server-side routing distinction first, then the fix. Adding the `/assets/` exception shows you've debugged this in production, not just copied a Stack Overflow answer.""",
        tip_bn=r"""আগে client-side আর server-side routing-এর পার্থক্য বোঝাও, তারপর সমাধান। `/assets/`-এর ব্যতিক্রমটা যোগ করলে বোঝা যায় তুমি production-এ এটা debug করেছ, শুধু Stack Overflow-এর উত্তর copy করোনি।""",
        mist_en=r"""Using `error_page 404 /index.html;` (it returns status 404 for every deep link), or applying the fallback to `/assets/` and `/api/` too.""",
        mist_bn=r"""`error_page 404 /index.html;` ব্যবহার করা (এতে প্রতিটা deep link-এ status 404 যায়), অথবা `/assets/` আর `/api/`-এও fallback প্রয়োগ করে ফেলা।""",
        follow=[
            ("Why might `error_page 404 /index.html` hurt SEO compared with `try_files`?", "`try_files`-এর তুলনায় `error_page 404 /index.html` কেন SEO-র ক্ষতি করতে পারে?"),
            ("How should `index.html` and hashed assets be cached differently?", "`index.html` আর hashed asset আলাদাভাবে কীভাবে cache করা উচিত?"),
        ],
        related=["nginx-012"],
        refs=[N_HTTP_CORE, N_BEGIN],
    ),
    # ------------------------------------------------------------------ nginx-007
    Q(
        id="nginx-007", sub="Configuration Blocks", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=1,
        tags=["reload", "graceful", "signals", "nginx-s"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""What happens when you run `nginx -s reload` (or `systemctl reload nginx`)?""",
        q_bn=r"""`nginx -s reload` (বা `systemctl reload nginx`) চালালে কী ঘটে?""",
        options=[
            ("The master checks the new config; if it's valid, it starts new workers with it and tells the old workers to finish their current requests and exit",
             "Master নতুন config পরীক্ষা করে; ঠিক থাকলে সেটা দিয়ে নতুন worker চালু করে, আর পুরনো worker-দের বলে হাতের request শেষ করে exit করতে"),
            ("NGINX stops all workers immediately and starts again, dropping active connections",
             "NGINX সাথে সাথে সব worker বন্ধ করে আবার চালু হয়, চলমান connection কেটে যায়"),
            ("Only TLS certificates are reloaded; other changes need a full restart",
             "শুধু TLS certificate reload হয়; বাকি পরিবর্তনের জন্য পুরো restart লাগে"),
            ("The new config is applied to the existing workers in place, without validation",
             "কোনো validation ছাড়াই নতুন config চলমান worker-দের উপর সরাসরি প্রয়োগ হয়"),
        ],
        correct=0,
        a_en=r"""The graceful old/new worker hand-off is correct. `reload` sends **SIGHUP** to the master. The master parses and validates the new configuration and opens any new listen sockets. If everything is fine, it starts **new workers** with the new config and asks the **old workers to shut down gracefully**: they stop accepting new connections, finish in-flight requests and exit. If the config is invalid, the master logs the error and keeps running the old config.""",
        a_bn=r"""পুরনো/নতুন worker-এর graceful হাতবদলের উত্তরটাই সঠিক। `reload` master-কে **SIGHUP** পাঠায়। Master নতুন configuration parse ও validate করে, আর নতুন কোনো listen socket থাকলে খোলে। সব ঠিক থাকলে নতুন config দিয়ে **নতুন worker** চালু করে, আর **পুরনো worker-দের gracefully বন্ধ হতে** বলে: তারা নতুন connection নেওয়া বন্ধ করে, চলমান request শেষ করে, তারপর exit করে। Config ভুল হলে master error log করে আর পুরনো config-ই চালাতে থাকে।""",
        ex_en=r"""
            The "stops all workers immediately" option describes a **restart** (`systemctl restart nginx`), which briefly drops connections. That's why you reload, not restart, for config and certificate changes.

            Even though a bad config won't take NGINX down on reload, run `nginx -t` first: it fails fast in your terminal or CI instead of only in the error log. Long-lived connections (WebSockets, large downloads) can keep old workers alive for a long time after a reload. `worker_shutdown_timeout` caps how long they may linger.
        """,
        ex_bn=r"""
            "সাথে সাথে সব worker বন্ধ" option-টা হলো **restart**-এর বর্ণনা (`systemctl restart nginx`), যেটা অল্প সময়ের জন্য connection কেটে দেয়। এজন্যই config বা certificate বদলালে restart না করে reload করা হয়।

            ভুল config থাকলেও reload-এ NGINX বন্ধ হয়ে যায় না, তবু আগে `nginx -t` চালাও: শুধু error log-এ না গিয়ে তোমার terminal বা CI-তেই সাথে সাথে fail করবে। দীর্ঘস্থায়ী connection (WebSocket, বড় download) reload-এর পরেও পুরনো worker-দের অনেকক্ষণ বাঁচিয়ে রাখতে পারে। `worker_shutdown_timeout` তাদের সর্বোচ্চ কতক্ষণ থাকতে দেওয়া হবে সেটা বেঁধে দেয়।
        """,
        tip_en=r"""Say "reload is graceful, restart isn't" and mention the old/new worker hand-off. It's a short answer that shows you understand the process model.""",
        tip_bn=r"""বলো "reload graceful, restart না", আর পুরনো/নতুন worker-এর হাতবদলের কথা উল্লেখ করো। ছোট উত্তর, কিন্তু process model-টা যে তুমি বোঝো সেটা দেখায়।""",
        related=["nginx-001", "nginx-003"],
        refs=[N_CONTROL, N_BEGIN],
    ),
    # ------------------------------------------------------------------ nginx-014
    Q(
        id="nginx-014", sub="Static File Serving", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["root", "alias", "static-files", "404", "path-traversal"],
        ver="Version-independent (NGINX 1.30 / 1.31)", vs=False, status="stable",
        q_en=r"""Static files live in `/var/www/app/static/` (e.g. `/var/www/app/static/logo.png`). With this config, `GET /static/logo.png` returns 404. Which file path does NGINX actually try to open?""",
        q_bn=r"""Static file-গুলো আছে `/var/www/app/static/`-এ (যেমন `/var/www/app/static/logo.png`)। এই config দিয়ে `GET /static/logo.png` 404 দিচ্ছে। NGINX আসলে কোন file path খুলতে চেষ্টা করছে?""",
        code=r"""
            location /static/ {
                root /var/www/app/static;
            }
        """,
        lang="nginx",
        options=[
            ("`/var/www/app/static/logo.png`", "`/var/www/app/static/logo.png`"),
            ("`/var/www/app/logo.png`", "`/var/www/app/logo.png`"),
            ("`static/logo.png` relative to the NGINX install prefix", "NGINX install prefix-এর সাপেক্ষে `static/logo.png`"),
            ("`/var/www/app/static/static/logo.png`", "`/var/www/app/static/static/logo.png`"),
        ],
        correct=3,
        a_en=r"""NGINX tries `/var/www/app/static/static/logo.png`. With `root`, the path is **root + the full request URI**, so the `/static/` prefix is appended again. Fix it with `root /var/www/app;` (preferred here, because the location matches the end of the path), or with `alias /var/www/app/static/;`, which **replaces** the matched location prefix with the alias path.""",
        a_bn=r"""NGINX খুলতে চেষ্টা করছে `/var/www/app/static/static/logo.png`। `root` দিলে path হয় **root + পুরো request URI**, তাই `/static/` prefix আবার যোগ হয়ে যায়। সমাধান হলো `root /var/www/app;` (এখানে এটাই ভালো, কারণ location path-এর শেষ অংশের সাথে মেলে), অথবা `alias /var/www/app/static/;`, যেটা মিলে যাওয়া location prefix-কে alias path দিয়ে **replace** করে।""",
        ex_en=r"""
            The tempting wrong answer is `/var/www/app/static/logo.png`, from the mental model of "root points at the folder for this location". That's how `alias` behaves, not `root`.

            - `root /var/www/app;` + `/static/logo.png` → `/var/www/app/static/logo.png`
            - `alias /var/www/app/static/;` + `/static/logo.png` → `/var/www/app/static/logo.png`

            **Security gotcha with `alias`:** the location and the alias must agree on trailing slashes. `location /static { alias /var/www/app/static/; }` (no slash on the location) lets `/static../secret.env` map to `/var/www/app/static/../secret.env`. That's the well-known "off-by-slash" path traversal. Prefer `root` where possible, and when you use `alias`, end both with `/`.
        """,
        ex_bn=r"""
            বিভ্রান্তিকর ভুল উত্তর হলো `/var/www/app/static/logo.png`, এই ধারণা থেকে যে "root এই location-এর folder-কে point করে"। এটা আসলে `alias`-এর আচরণ, `root`-এর না।

            - `root /var/www/app;` + `/static/logo.png` → `/var/www/app/static/logo.png`
            - `alias /var/www/app/static/;` + `/static/logo.png` → `/var/www/app/static/logo.png`

            **`alias`-এর security gotcha:** location আর alias-এর শেষের slash মিলতে হবে। `location /static { alias /var/www/app/static/; }` (location-এ slash নেই) হলে `/static../secret.env` map হয়ে যায় `/var/www/app/static/../secret.env`-এ। এটাই বিখ্যাত "off-by-slash" path traversal। সম্ভব হলে `root` ব্যবহার করো, আর `alias` ব্যবহার করলে দুটোর শেষেই `/` দাও।
        """,
        tip_en=r"""Give the one-line rule, "root appends the URI, alias replaces the location", then mention the off-by-slash traversal. Security awareness turns an easy config question into a strong answer.""",
        tip_bn=r"""এক লাইনের নিয়মটা বলো: "root URI যোগ করে, alias location-কে replace করে"। তারপর off-by-slash traversal-এর কথা বলো। Security সচেতনতা একটা সহজ config প্রশ্নকে শক্তিশালী উত্তরে পরিণত করে।""",
        related=["nginx-012", "nginx-006"],
        refs=[N_HTTP_CORE],
    ),
    # ------------------------------------------------------------------ nginx-015
    Q(
        id="nginx-015", sub="Proxy Headers", diff="medium", type="conceptual",
        prio="high", market="both", mins=6,
        tags=["x-forwarded-for", "x-forwarded-proto", "trust-proxy", "express", "client-ip"],
        ver="NGINX 1.30 stable / 1.31 mainline, Express 5.x", vs=False, status="stable",
        q_en=r"""Behind NGINX, your Express app logs every request as coming from `127.0.0.1`, `req.secure` is always false, and a rate limiter blocks all users at once. Which proxy headers fix this, what does each one do, and what must you configure in Express?""",
        q_bn=r"""NGINX-এর পেছনে তোমার Express app প্রতিটা request `127.0.0.1` থেকে আসছে বলে log করছে, `req.secure` সবসময় false, আর rate limiter একসাথে সব user-কে block করে দিচ্ছে। কোন proxy header-গুলো এটা ঠিক করবে, প্রতিটা কী করে, আর Express-এ কী configure করতে হবে?""",
        a_en=r"""
            To Express, NGINX **is** the client: the TCP connection comes from `127.0.0.1` over plain HTTP. So every user shares one IP (one rate-limit bucket!), and HTTPS is invisible. NGINX must pass the original details in headers:

            - **`Host $host`**: the hostname the client asked for. By default NGINX sends the upstream's own name (`$proxy_host`), which breaks absolute URLs, virtual hosting and cookie domains.
            - **`X-Real-IP $remote_addr`**: the client's IP as one value.
            - **`X-Forwarded-For $proxy_add_x_forwarded_for`**: the chain of client and proxy IPs. NGINX appends `$remote_addr` to any existing header.
            - **`X-Forwarded-Proto $scheme`**: `https` or `http`, so the app knows TLS was used.

            In Express, set **`app.set('trust proxy', 1)`** (trust exactly one hop: NGINX). Then `req.ip` comes from `X-Forwarded-For`, and `req.protocol`/`req.secure` from `X-Forwarded-Proto`. That fixes per-user rate limiting, HTTPS redirects and `secure` session cookies (express-session won't send a secure cookie if it thinks the request is HTTP).
        """,
        a_bn=r"""
            Express-এর চোখে NGINX-ই client: TCP connection আসছে `127.0.0.1` থেকে, সাধারণ HTTP-তে। ফলে সব user একটা IP share করে (একটাই rate-limit bucket!), আর HTTPS চোখেই পড়ে না। NGINX-কে আসল তথ্য header-এ পাঠাতে হবে:

            - **`Host $host`**: client যে hostname চেয়েছিল। Default হিসেবে NGINX upstream-এর নিজের নাম (`$proxy_host`) পাঠায়, এতে absolute URL, virtual hosting আর cookie domain ভেঙে যায়।
            - **`X-Real-IP $remote_addr`**: client-এর IP, একটা মাত্র value হিসেবে।
            - **`X-Forwarded-For $proxy_add_x_forwarded_for`**: client আর proxy-দের IP-র chain। আগে থেকে header থাকলে NGINX তার সাথে `$remote_addr` যোগ করে।
            - **`X-Forwarded-Proto $scheme`**: `https` বা `http`, যাতে app জানে TLS ব্যবহার হয়েছিল।

            Express-এ set করো **`app.set('trust proxy', 1)`** (ঠিক একটা hop, অর্থাৎ NGINX-কে trust করো)। তখন `req.ip` আসে `X-Forwarded-For` থেকে, আর `req.protocol`/`req.secure` আসে `X-Forwarded-Proto` থেকে। এতে per-user rate limiting, HTTPS redirect আর `secure` session cookie ঠিক হয়ে যায় (request HTTP মনে করলে express-session secure cookie পাঠায় না)।
        """,
        ex_en=r"""
            - **These headers are client-controlled.** Anyone can send `X-Forwarded-For: 1.2.3.4`. Only trust as many hops as you really have. `trust proxy: true` trusts the whole chain, so a client can spoof its IP and bypass rate limits or IP allow-lists, especially if the app port is reachable directly.
            - **More hops (CDN → NGINX → app):** either trust the exact number of hops or a list of proxy CIDRs. Alternatively, resolve the real IP in NGINX with the `realip` module (`set_real_ip_from` the CDN's ranges) and pass a clean `X-Real-IP`.
            - **Rate limiters:** `express-rate-limit` keys on `req.ip`, and recent versions log validation errors when `X-Forwarded-For` is present but `trust proxy` isn't configured.
            - **The standard alternative:** the `Forwarded` header (RFC 7239) is the standardised form, but `X-Forwarded-*` remains what most stacks use.
        """,
        ex_bn=r"""
            - **এই header-গুলো client নিয়ন্ত্রণ করতে পারে।** যে কেউ `X-Forwarded-For: 1.2.3.4` পাঠাতে পারে। যতগুলো hop সত্যিই আছে, শুধু ততগুলোই trust করো। `trust proxy: true` পুরো chain trust করে, ফলে client নিজের IP spoof করে rate limit বা IP allow-list এড়িয়ে যেতে পারে, বিশেষ করে app-এর port সরাসরি পৌঁছানো গেলে।
            - **বেশি hop (CDN → NGINX → app):** হয় hop-এর নির্দিষ্ট সংখ্যা, নয়তো proxy-দের CIDR-এর তালিকা trust করো। বিকল্প হলো NGINX-এই `realip` module দিয়ে আসল IP বের করা (CDN-এর range-গুলো `set_real_ip_from`-এ), তারপর পরিষ্কার একটা `X-Real-IP` পাঠানো।
            - **Rate limiter:** `express-rate-limit` `req.ip` দিয়ে key বানায়, আর `X-Forwarded-For` আছে কিন্তু `trust proxy` configure করা নেই এমন হলে নতুন version-গুলো validation error log করে।
            - **Standard বিকল্প:** `Forwarded` header (RFC 7239) হলো standard রূপ, তবে বেশিরভাগ stack এখনো `X-Forwarded-*` ব্যবহার করে।
        """,
        tip_en=r"""Connect each symptom to its header: the wrong IP → XFF, the wrong protocol → X-Forwarded-Proto. Then raise the spoofing risk unprompted. Security-minded answers stand out.""",
        tip_bn=r"""প্রতিটা লক্ষণকে তার header-এর সাথে মেলাও: ভুল IP → XFF, ভুল protocol → X-Forwarded-Proto। তারপর কেউ জিজ্ঞেস করার আগেই spoofing-এর ঝুঁকির কথা তোলো। Security-সচেতন উত্তর আলাদাভাবে চোখে পড়ে।""",
        mist_en=r"""Setting `trust proxy` to `true` blindly, overwriting XFF with `$remote_addr` behind a CDN (losing the real IP), or reading `req.headers['x-forwarded-for']` manually and trusting the first value.""",
        mist_bn=r"""না ভেবে `trust proxy` `true` করে দেওয়া, CDN-এর পেছনে XFF-কে `$remote_addr` দিয়ে overwrite করা (আসল IP হারিয়ে যায়), অথবা হাতে `req.headers['x-forwarded-for']` পড়ে প্রথম value-টাই বিশ্বাস করা।""",
        code=r"""
            // NGINX location:
            //   proxy_set_header Host              $host;
            //   proxy_set_header X-Real-IP         $remote_addr;
            //   proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
            //   proxy_set_header X-Forwarded-Proto $scheme;

            import express from 'express';
            const app = express();

            app.set('trust proxy', 1);   // exactly one proxy hop (NGINX on this host)

            app.get('/whoami', (req, res) => {
              res.json({
                ip: req.ip,              // real client IP (from X-Forwarded-For)
                protocol: req.protocol,  // 'https' (from X-Forwarded-Proto)
                secure: req.secure,      // true behind HTTPS
                hostname: req.hostname,  // from Host
              });
            });

            app.listen(3000, '127.0.0.1');
        """,
        lang="javascript",
        follow=[
            ("How would you get the real client IP when Cloudflare sits in front of NGINX?", "NGINX-এর সামনে Cloudflare থাকলে আসল client IP কীভাবে পাবে?"),
            ("Why is `trust proxy: true` dangerous if port 3000 is publicly reachable?", "Port 3000 public-ভাবে পৌঁছানো গেলে `trust proxy: true` কেন বিপজ্জনক?"),
        ],
        related=["nginx-005", "nginx-002"],
        refs=[EXPRESS_PROXY, N_PROXY, MDN_XFF],
    ),
    # ------------------------------------------------------------------ nginx-016
    Q(
        id="nginx-016", sub="WebSocket Proxying", diff="medium", type="coding",
        prio="high", market="both", mins=6,
        tags=["websocket", "upgrade", "map", "proxy_read_timeout", "realtime"],
        ver="NGINX 1.30 stable / 1.31 mainline (proxy_http_version 1.1 default since 1.29.7)", vs=True, status="stable",
        q_en=r"""
            A Node.js WebSocket service (using the `ws` library) runs on `127.0.0.1:4000` and serves `/ws/`. Through NGINX the handshake fails (the app sees a normal HTTP GET and rejects it), and when it does work, idle connections drop after about 60 seconds.

            Write the NGINX config to proxy `wss://chat.example.com/ws/` correctly.
        """,
        q_bn=r"""
            একটা Node.js WebSocket service (`ws` library দিয়ে বানানো) `127.0.0.1:4000`-এ চলে আর `/ws/` serve করে। NGINX দিয়ে গেলে handshake fail করে (app একটা সাধারণ HTTP GET দেখে reject করে দেয়), আর যখন কাজ করে, idle connection প্রায় ৬০ সেকেন্ড পরে কেটে যায়।

            `wss://chat.example.com/ws/` ঠিকভাবে proxy করার জন্য NGINX config লেখো।
        """,
        code=r"""
            http {
                # Connection: upgrade only when the client asked for an upgrade
                map $http_upgrade $connection_upgrade {
                    default upgrade;
                    ''      close;
                }

                upstream realtime {
                    server 127.0.0.1:4000;
                }

                server {
                    listen 443 ssl;
                    http2 on;
                    server_name chat.example.com;
                    ssl_certificate     /etc/letsencrypt/live/chat.example.com/fullchain.pem;
                    ssl_certificate_key /etc/letsencrypt/live/chat.example.com/privkey.pem;

                    location /ws/ {
                        proxy_pass http://realtime;
                        proxy_http_version 1.1;        # default since 1.29.7; required on older NGINX
                        proxy_set_header Upgrade    $http_upgrade;
                        proxy_set_header Connection $connection_upgrade;
                        proxy_set_header Host       $host;
                        proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
                        proxy_set_header X-Forwarded-Proto $scheme;

                        proxy_read_timeout 1h;         # max silence from the backend
                        proxy_send_timeout 1h;
                    }
                }
            }
        """,
        lang="nginx",
        time="N/A (configuration)", space="N/A (one tunnelled connection per client)",
        a_en=r"""
            **Why the handshake failed:** a WebSocket starts as an HTTP/1.1 request with `Upgrade: websocket` and `Connection: Upgrade`. Both are **hop-by-hop headers**, so a proxy doesn't forward them. Without explicit `proxy_set_header Upgrade/Connection`, Node sees a plain GET. When the backend answers `101 Switching Protocols`, NGINX turns the connection into a bidirectional tunnel.

            **The `map`** sends `Connection: upgrade` only when the client actually requested an upgrade, and `close` otherwise, so normal HTTP requests to the same location still work.

            **Why connections dropped:** `proxy_read_timeout` defaults to **60s**, and for a tunnel it means "close if the backend sends nothing for 60 s". Raise it for this location, and also have the server send WebSocket **ping frames** (e.g. every 30 s) so dead connections are detected and middleboxes don't drop idle ones.

            TLS terminates at NGINX (`wss://` for clients), while the backend speaks plain `ws://` on localhost.
        """,
        a_bn=r"""
            **Handshake কেন fail করছিল:** WebSocket শুরু হয় `Upgrade: websocket` আর `Connection: Upgrade`-সহ একটা HTTP/1.1 request দিয়ে। দুটোই **hop-by-hop header**, তাই proxy এগুলো forward করে না। স্পষ্টভাবে `proxy_set_header Upgrade/Connection` না দিলে Node একটা সাধারণ GET দেখে। Backend `101 Switching Protocols` উত্তর দিলে NGINX connection-টাকে দুই-দিকের একটা tunnel-এ পরিণত করে।

            **`map`** শুধু client সত্যিই upgrade চাইলে `Connection: upgrade` পাঠায়, নইলে `close`। ফলে একই location-এ সাধারণ HTTP request-ও কাজ করে।

            **Connection কেন কাটছিল:** `proxy_read_timeout`-এর default **60s**, আর tunnel-এর ক্ষেত্রে এর মানে "backend ৬০ সেকেন্ড কিছু না পাঠালে বন্ধ করো"। এই location-এ এটা বাড়াও। সাথে server থেকে WebSocket **ping frame** পাঠাও (যেমন প্রতি ৩০ সেকেন্ডে), যাতে মৃত connection ধরা পড়ে আর মাঝের কোনো device idle connection কেটে না দেয়।

            TLS terminate হয় NGINX-এ (client-দের জন্য `wss://`), আর backend localhost-এ সাধারণ `ws://`-এ কথা বলে।
        """,
        ex_en=r"""
            - **Version note:** the official docs mark `proxy_http_version 1.1` as needed only before 1.29.7, so keeping it is harmless and makes the config portable to older servers.
            - **HTTP/2 on the server is fine.** Browsers open the WebSocket over its own HTTP/1.1 connection, so `http2 on;` doesn't break the upgrade.
            - **Scaling out:** with several WebSocket backends, each connection is pinned to one server for its lifetime. Libraries with an HTTP long-polling fallback (Socket.IO) also need sticky sessions, and broadcasts need a shared adapter (e.g. Redis).
            - **Reloads:** existing tunnels stay on old workers after `nginx -s reload` until they close. `worker_shutdown_timeout` bounds this, and clients must handle reconnects.
            - **Capacity:** each WebSocket holds two connections in NGINX (client + upstream) for its whole lifetime. Size `worker_connections` and file-descriptor limits accordingly.
        """,
        ex_bn=r"""
            - **Version-সংক্রান্ত নোট:** official docs-এ `proxy_http_version 1.1`-কে শুধু 1.29.7-এর আগে দরকার বলে চিহ্নিত করা আছে, তাই রেখে দিলে ক্ষতি নেই, বরং পুরনো server-এও config-টা চলে।
            - **Server-এ HTTP/2 থাকলেও সমস্যা নেই।** Browser WebSocket খোলে নিজস্ব একটা HTTP/1.1 connection-এ, তাই `http2 on;` upgrade ভাঙে না।
            - **Scale out:** একাধিক WebSocket backend থাকলে প্রতিটা connection তার পুরো আয়ু জুড়ে একটা server-এ বাঁধা থাকে। HTTP long-polling fallback-ওয়ালা library-র (Socket.IO) sticky session-ও লাগে, আর broadcast-এর জন্য shared adapter লাগে (যেমন Redis)।
            - **Reload:** `nginx -s reload`-এর পরেও চলমান tunnel বন্ধ না হওয়া পর্যন্ত পুরনো worker-এ থাকে। `worker_shutdown_timeout` এর সীমা বেঁধে দেয়, আর client-কে reconnect সামলাতে হয়।
            - **Capacity:** প্রতিটা WebSocket তার পুরো আয়ু জুড়ে NGINX-এ দুটো connection ধরে রাখে (client + upstream)। সেই অনুযায়ী `worker_connections` আর file-descriptor limit ঠিক করো।
        """,
        tip_en=r"""Use the phrase "Upgrade and Connection are hop-by-hop headers". It explains **why** the config is needed. Then separate the two symptoms (handshake vs idle timeout) and fix each explicitly.""",
        tip_bn=r""""Upgrade আর Connection hop-by-hop header", এই কথাটা ব্যবহার করো। এটা ব্যাখ্যা করে config **কেন** লাগে। তারপর দুটো লক্ষণ আলাদা করো (handshake বনাম idle timeout), আর প্রতিটা আলাদাভাবে ঠিক করো।""",
        mist_en=r"""Hard-coding `Connection "upgrade"` for a location that also serves normal requests, setting a huge timeout instead of heartbeats, and forgetting that WebSockets across multiple backends need stickiness or a shared message bus.""",
        mist_bn=r"""সাধারণ request-ও serve করে এমন location-এ `Connection "upgrade"` hard-code করা, heartbeat-এর বদলে বিশাল timeout দেওয়া, আর ভুলে যাওয়া যে একাধিক backend-এ WebSocket চালাতে stickiness বা shared message bus লাগে।""",
        follow=[
            ("How would you scale this to three Node.js instances?", "এটাকে তিনটা Node.js instance-এ কীভাবে scale করবে?"),
            ("What happens to open WebSocket connections during an NGINX reload?", "NGINX reload-এর সময় খোলা WebSocket connection-গুলোর কী হয়?"),
        ],
        related=["nginx-005", "nginx-007"],
        refs=[N_WS, N_PROXY, N_MAP],
    ),
    # ------------------------------------------------------------------ nginx-024
    Q(
        id="nginx-024", sub="NGINX with Docker", diff="hard", type="debugging",
        prio="high", market="both", mins=8,
        tags=["docker", "502", "dns", "resolver", "compose"],
        ver="NGINX 1.30 stable (upstream `resolve` in open source since 1.27.3), Docker Compose v5", vs=True, status="stable",
        q_en=r"""
            NGINX and a Node API run as Compose services on the same user-defined network.
            1. The first config used `proxy_pass http://localhost:3000;` and **every** request returned 502.
            2. After changing it to `http://api:3000` (shown below), everything works until the `api` container is recreated during a deploy. From then on NGINX returns 502 until NGINX itself is restarted.

            Explain both problems and fix the config properly.
        """,
        q_bn=r"""
            একই user-defined network-এ NGINX আর একটা Node API Compose service হিসেবে চলছে।
            1. প্রথম config-এ ছিল `proxy_pass http://localhost:3000;`, আর **প্রতিটা** request 502 দিচ্ছিল।
            2. সেটা `http://api:3000`-এ বদলানোর পর (নিচে দেখানো) সব ঠিকঠাক চলে, যতক্ষণ না deploy-এর সময় `api` container recreate হয়। তারপর থেকে NGINX নিজে restart না হওয়া পর্যন্ত 502 দেয়।

            দুটো সমস্যাই ব্যাখ্যা করো, আর config ঠিকভাবে সংশোধন করো।
        """,
        code=r"""
            # nginx/conf.d/default.conf
            server {
                listen 80;
                location / {
                    proxy_pass http://api:3000;
                }
            }

            # error.log after "docker compose up -d api" recreated the container:
            # [error] connect() failed (113: No route to host) while connecting to upstream,
            #         client: 172.18.0.1, upstream: "http://172.18.0.5:3000/"
        """,
        lang="nginx",
        extra=[
            dict(lang="nginx", label_en="Fix A (NGINX ≥ 1.27.3): upstream with runtime DNS re-resolution", label_bn="সমাধান A (NGINX ≥ 1.27.3): runtime-এ DNS আবার resolve করা upstream", src=r"""
                # Docker's embedded DNS server (user-defined networks only)
                resolver 127.0.0.11 valid=10s ipv6=off;

                upstream api {
                    zone api_upstream 64k;          # shared memory is required for "resolve"
                    server api:3000 resolve;        # re-resolved at runtime; all replicas included
                }

                server {
                    listen 80;
                    location / {
                        proxy_pass http://api;
                        proxy_set_header Host $host;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_set_header X-Forwarded-Proto $scheme;
                    }
                }
            """),
            dict(lang="nginx", label_en="Fix B (any version): a variable forces per-request resolution via the resolver", label_bn="সমাধান B (যেকোনো version): variable দিলে resolver দিয়ে request-এর সময় resolve হয়", src=r"""
                resolver 127.0.0.11 valid=10s ipv6=off;

                server {
                    listen 80;
                    location / {
                        set $api_backend http://api:3000;
                        proxy_pass $api_backend;      # URI is passed unchanged (no URI part here)
                    }
                }
            """),
        ],
        a_en=r"""
            **Problem 1: `localhost`.** Inside the NGINX container, `localhost` is the **NGINX container itself**, because each container has its own network namespace. Nothing listens on port 3000 there, so you get `connect() failed (111: Connection refused)` and a 502. Use the Compose **service name** (`api`) instead.

            **Problem 2: stale DNS.** For a hostname written literally in `proxy_pass` or an `upstream` `server` line, NGINX **resolves it once at config load** and keeps the IPs until the next reload or restart. Recreating the `api` container gives it a new IP, and NGINX keeps connecting to the old one (`No route to host` → 502).

            **Fixes:**
            - **A (NGINX ≥ 1.27.3, so 1.30 stable):** an `upstream` with a `zone` and `server api:3000 resolve;`, plus `resolver 127.0.0.11`. NGINX re-resolves at runtime while keeping upstream features (load balancing across scaled replicas, keepalive). Before 1.27.3, `resolve` was NGINX Plus-only.
            - **B (any version):** put the URL in a variable (`set $api_backend http://api:3000; proxy_pass $api_backend;`), which makes NGINX resolve through the `resolver` at request time, honouring `valid=`. It also lets NGINX start even when the `api` container doesn't exist yet. Without it you'd get `host not found in upstream` at startup.
            - **Pragmatic alternative:** reload NGINX as part of every deploy (`docker compose exec nginx nginx -s reload`).
        """,
        a_bn=r"""
            **সমস্যা ১: `localhost`।** NGINX container-এর ভেতরে `localhost` মানে **NGINX container নিজেই**, কারণ প্রতিটা container-এর নিজস্ব network namespace আছে। সেখানে port 3000-এ কেউ listen করছে না, তাই আসে `connect() failed (111: Connection refused)` আর 502। এর বদলে Compose-এর **service name** (`api`) ব্যবহার করো।

            **সমস্যা ২: পুরনো DNS।** `proxy_pass` বা `upstream`-এর `server` line-এ সরাসরি লেখা hostname NGINX **config load-এর সময় একবারই resolve করে**, আর পরের reload বা restart পর্যন্ত সেই IP রেখে দেয়। `api` container recreate হলে নতুন IP পায়, কিন্তু NGINX পুরনো IP-তেই connect করতে থাকে (`No route to host` → 502)।

            **সমাধান:**
            - **A (NGINX ≥ 1.27.3, অর্থাৎ 1.30 stable):** `zone`-সহ একটা `upstream` আর `server api:3000 resolve;`, সাথে `resolver 127.0.0.11`। NGINX runtime-এ আবার resolve করে, আর upstream-এর feature-গুলোও রাখে (scale করা replica-দের মধ্যে load balancing, keepalive)। 1.27.3-এর আগে `resolve` শুধু NGINX Plus-এ ছিল।
            - **B (যেকোনো version):** URL একটা variable-এ রাখো (`set $api_backend http://api:3000; proxy_pass $api_backend;`)। এতে NGINX request-এর সময় `resolver` দিয়ে resolve করে, `valid=` মেনে। এর আরেকটা সুবিধা: `api` container এখনো না থাকলেও NGINX start হতে পারে। এটা ছাড়া startup-এ `host not found in upstream` আসত।
            - **ব্যবহারিক বিকল্প:** প্রতিটা deploy-এর অংশ হিসেবে NGINX reload করো (`docker compose exec nginx nginx -s reload`)।
        """,
        ex_en=r"""
            **A 502 checklist for containers:**
            - The app listens on `127.0.0.1` inside **its** container → bind to `0.0.0.0`.
            - The wrong port: use the **container** port (3000), not the host-published one.
            - The services are on different Compose networks.
            - The app crashed (check `docker compose ps` and the logs).

            **On a non-Docker RHEL/Fedora host,** `connect() to 127.0.0.1:3000 failed (13: Permission denied)` is usually SELinux blocking NGINX from making network connections. Fix it with `setsebool -P httpd_can_network_connect 1`, not by disabling SELinux.

            `127.0.0.11` exists only on **user-defined** networks (which Compose always creates). On the default bridge there's no embedded DNS. Keep `valid=` short, because Docker's DNS answers don't carry a meaningful TTL for this purpose.
        """,
        ex_bn=r"""
            **Container-এ 502-এর checklist:**
            - App **নিজের** container-এর ভেতরে `127.0.0.1`-এ listen করছে → `0.0.0.0`-এ bind করো।
            - ভুল port: host-এ publish করা port না, **container** port (3000) ব্যবহার করো।
            - Service-গুলো আলাদা Compose network-এ আছে।
            - App crash করেছে (`docker compose ps` আর log দেখো)।

            **Docker ছাড়া RHEL/Fedora host-এ** `connect() to 127.0.0.1:3000 failed (13: Permission denied)` সাধারণত SELinux-এর কাজ, যেটা NGINX-কে network connection করতে দিচ্ছে না। সমাধান `setsebool -P httpd_can_network_connect 1`, SELinux বন্ধ করা না।

            `127.0.0.11` শুধু **user-defined** network-এ থাকে (Compose সবসময় এটাই তৈরি করে)। Default bridge-এ embedded DNS নেই। `valid=` ছোট রাখো, কারণ এই কাজের জন্য Docker-এর DNS উত্তরে অর্থবহ কোনো TTL থাকে না।
        """,
        tip_en=r"""Separate the two bugs clearly (namespace vs DNS caching) and read the error-log evidence aloud. Knowing that open-source NGINX gained upstream `resolve` in 1.27.3 shows you track current versions, not old blog posts.""",
        tip_bn=r"""দুটো bug স্পষ্টভাবে আলাদা করো (namespace বনাম DNS caching), আর error log-এর প্রমাণটা পড়ে শোনাও। Open-source NGINX যে 1.27.3-এ upstream `resolve` পেয়েছে সেটা জানা দেখায় তুমি পুরনো blog post না, বর্তমান version-এর খোঁজ রাখো।""",
        mist_en=r"""Using `network_mode: host` everywhere to make `localhost` work, hard-coding container IPs, or assuming NGINX re-resolves `proxy_pass` hostnames automatically.""",
        mist_bn=r"""`localhost` চালানোর জন্য সব জায়গায় `network_mode: host` ব্যবহার করা, container-এর IP hard-code করা, অথবা ধরে নেওয়া যে NGINX `proxy_pass`-এর hostname নিজে থেকেই আবার resolve করে।""",
        follow=[
            ("What changes when you run `docker compose up --scale api=3` with Fix A?", "Fix A থাকা অবস্থায় `docker compose up --scale api=3` চালালে কী পরিবর্তন হয়?"),
            ("Why might NGINX refuse to start if the `api` container isn't running yet?", "`api` container এখনো না চললে NGINX কেন start হতে অস্বীকার করতে পারে?"),
        ],
        related=["nginx-005", "nginx-013"],
        refs=[N_UPSTREAM, N_PROXY, D_NETWORK],
    ),
    # ------------------------------------------------------------------ nginx-031
    Q(
        id="nginx-031", sub="Deployment Architecture", diff="extreme", type="architecture",
        prio="medium", market="international", mins=20,
        tags=["canary", "split_clients", "traffic-splitting", "rollback", "observability"],
        ver="NGINX 1.30 stable / 1.31 mainline", vs=False, status="stable",
        q_en=r"""Design a canary release mechanism at the NGINX layer for a Node.js API. Send 5% of users to v2, let QA force v2 with a cookie, keep each user on the same version, observe errors per version, and be able to roll back instantly. What are the pitfalls?""",
        q_bn=r"""একটা Node.js API-র জন্য NGINX layer-এ canary release ব্যবস্থা design করো। ৫% user-কে v2-তে পাঠাতে হবে, QA একটা cookie দিয়ে জোর করে v2 পেতে পারবে, প্রতিটা user একই version-এ থাকবে, প্রতিটা version-এর error আলাদাভাবে দেখা যাবে, আর সাথে সাথে rollback করা যাবে। কী কী সমস্যা (pitfall) হতে পারে?""",
        a_en=r"""
            **(Advanced.)** The building blocks are two `upstream` groups (stable and canary) and a variable that picks one per request.

            1. **Consistent bucketing:** `split_clients` hashes a key (a stable user ID cookie, falling back to the IP for anonymous users) plus a release-specific salt into percentage buckets, so the same user always lands on the same version. Changing the salt reshuffles buckets for the next release.
            2. **Override:** a `map` on `$cookie_canary` lets QA force `api_canary`; otherwise the `split_clients` result is used.
            3. **Routing:** `proxy_pass http://$api_upstream;`. When a variable's value matches an upstream group name, NGINX uses that group directly, with no resolver needed.
            4. **Observability:** log the variant and `$upstream_addr`/`$upstream_response_time` with a custom `log_format`, and expose it as a response header. Compare error rate and p95 latency per variant (log pipeline or metrics) and automate the go/no-go decision.
            5. **Ramp and rollback:** move 5% → 25% → 50% → 100% by editing the percentage and running `nginx -t && nginx -s reload`. Rollback means setting the canary to 0% and reloading, a graceful change that takes seconds.

            **Pitfalls:**
            - **Data compatibility:** v1 and v2 run simultaneously against the same database, so migrations must be expand/contract, and both must read each other's cache entries and queue messages.
            - **Sticky by user, not IP:** IP bucketing behind carrier-grade NAT or office NAT puts thousands of users in one bucket.
            - **Caches:** if NGINX or a CDN caches API responses, include the variant in the cache key or bypass it for canary traffic.
            - **Long-lived connections:** WebSockets stay on the old version after a reload, bounded by `worker_shutdown_timeout`, so clients must reconnect.
            - **Statistical significance:** 5% of low traffic may hide errors. Run long enough, or use synthetic traffic.
            - **When to use something else:** NGINX canaries split by request routing. Business-logic experiments are often better served by feature flags inside the app.
        """,
        a_bn=r"""
            **(Advanced।)** মূল উপাদান হলো দুটো `upstream` group (stable আর canary), আর একটা variable, যেটা প্রতিটা request-এর জন্য একটা বেছে নেয়।

            1. **Consistent bucketing:** `split_clients` একটা key (একটা স্থায়ী user ID cookie, anonymous user-দের জন্য IP) আর release-নির্দিষ্ট একটা salt hash করে শতাংশভিত্তিক bucket-এ ভাগ করে, ফলে একই user সবসময় একই version-এ যায়। Salt বদলালে পরের release-এর জন্য bucket নতুন করে ভাগ হয়।
            2. **Override:** `$cookie_canary`-এর উপর একটা `map` QA-কে জোর করে `api_canary` পেতে দেয়; নইলে `split_clients`-এর ফলাফল ব্যবহার হয়।
            3. **Routing:** `proxy_pass http://$api_upstream;`। Variable-এর value কোনো upstream group-এর নামের সাথে মিললে NGINX সরাসরি ওই group ব্যবহার করে, resolver লাগে না।
            4. **Observability:** একটা custom `log_format`-এ variant আর `$upstream_addr`/`$upstream_response_time` log করো, আর response header হিসেবেও দেখাও। প্রতিটা variant-এর error rate আর p95 latency তুলনা করো (log pipeline বা metrics দিয়ে), আর এগোনো/থামার সিদ্ধান্ত automate করো।
            5. **Ramp আর rollback:** শতাংশ বদলে `nginx -t && nginx -s reload` চালিয়ে ৫% → ২৫% → ৫০% → ১০০%-এ এগোও। Rollback মানে canary ০% করে reload করা, একটা graceful পরিবর্তন, কয়েক সেকেন্ডের কাজ।

            **Pitfall:**
            - **Data compatibility:** v1 আর v2 একসাথে একই database-এ চলে, তাই migration হতে হবে expand/contract ধাঁচে, আর দুটো version-কেই একে অপরের cache entry ও queue message পড়তে পারতে হবে।
            - **IP না, user ধরে sticky:** carrier-grade NAT বা অফিসের NAT-এর পেছনে IP দিয়ে bucket করলে হাজার হাজার user একই bucket-এ পড়ে।
            - **Cache:** NGINX বা CDN API response cache করলে variant-কে cache key-তে রাখো, বা canary traffic-এর জন্য cache bypass করো।
            - **দীর্ঘস্থায়ী connection:** reload-এর পরেও WebSocket পুরনো version-এ থেকে যায়, `worker_shutdown_timeout` পর্যন্ত, তাই client-কে reconnect করতে হবে।
            - **Statistical significance:** কম traffic-এর ৫% error লুকিয়ে রাখতে পারে। যথেষ্ট সময় ধরে চালাও, বা synthetic traffic ব্যবহার করো।
            - **কখন অন্য উপায়:** NGINX canary request routing দিয়ে ভাগ করে। Business logic নিয়ে পরীক্ষার জন্য app-এর ভেতরের feature flag প্রায়ই ভালো।
        """,
        ex_en=r"""
            **Blue/green vs canary:** blue/green switches 100% of traffic at once (fast and simple, but every user sees a bad release). A canary limits the blast radius to a slice of users and needs per-variant metrics to be useful.

            **Draining:** the 1.29.6 `sticky` support in open source adds a `drain` server parameter, so existing sticky sessions can finish on a server while new sessions go elsewhere. That's useful when retiring an old version that holds sessions.

            **Automation:** a deploy controller (CI job or tool such as Argo Rollouts on Kubernetes) can template the percentage, reload NGINX, query metrics and roll back automatically. Humans should approve the ramps, not perform them by hand at 2 a.m.
        """,
        ex_bn=r"""
            **Blue/green বনাম canary:** blue/green একবারে ১০০% traffic switch করে (দ্রুত আর সহজ, কিন্তু খারাপ release সব user দেখে)। Canary ক্ষতির পরিধি user-দের একটা অংশে সীমিত রাখে, আর কাজে লাগাতে হলে প্রতিটা variant-এর আলাদা metric লাগে।

            **Draining:** open source-এ 1.29.6-এর `sticky` support একটা `drain` server parameter যোগ করেছে। এতে চলমান sticky session-গুলো একটা server-এ শেষ হতে পারে, আর নতুন session অন্য জায়গায় যায়। Session ধরে রাখা পুরনো version সরানোর সময় এটা কাজের।

            **Automation:** একটা deploy controller (CI job, বা Kubernetes-এ Argo Rollouts-এর মতো tool) শতাংশটা template করতে, NGINX reload করতে, metric query করতে আর নিজে থেকে rollback করতে পারে। মানুষ ramp অনুমোদন দেবে, রাত ২টায় হাতে করে করবে না।
        """,
        tip_en=r"""Draw the request flow: cookie/IP → split_clients → map override → upstream → logs. Then spend at least a third of your answer on pitfalls. Interviewers at this level care most about what can go wrong.""",
        tip_bn=r"""Request-এর প্রবাহটা এঁকে দেখাও: cookie/IP → split_clients → map override → upstream → log। তারপর উত্তরের অন্তত এক-তৃতীয়াংশ pitfall-এ দাও। এই স্তরের interviewer-রা সবচেয়ে বেশি গুরুত্ব দেয় কী কী ভুল হতে পারে তাতে।""",
        mist_en=r"""Splitting randomly per request (users flip between versions), bucketing only by IP, not logging which variant served the request, and running incompatible schema changes during the canary.""",
        mist_bn=r"""প্রতি request-এ random ভাগ করা (user-রা version-এর মধ্যে আসা-যাওয়া করে), শুধু IP দিয়ে bucket করা, কোন variant request serve করল সেটা log না করা, আর canary চলাকালীন incompatible schema পরিবর্তন চালানো।""",
        code=r"""
            upstream api_stable { server 10.0.1.11:3000; server 10.0.1.12:3000; }
            upstream api_canary { server 10.0.1.21:3000; }

            # Stable bucketing key: user-id cookie, else client IP
            map $cookie_uid $canary_key {
                ""      $remote_addr;
                default $cookie_uid;
            }

            # Change the salt ("release-42") to reshuffle buckets for the next release
            split_clients "${canary_key}-release-42" $split_upstream {
                5%      api_canary;
                *       api_stable;
            }

            # QA override: cookie canary=always forces v2
            map $cookie_canary $api_upstream {
                always  api_canary;
                default $split_upstream;
            }

            log_format canary '$remote_addr "$request" $status rt=$request_time '
                              'variant=$api_upstream up=$upstream_addr urt=$upstream_response_time';

            server {
                listen 443 ssl;
                http2 on;
                server_name api.example.com;
                access_log /var/log/nginx/api.log canary;

                location / {
                    proxy_pass http://$api_upstream;       # value matches an upstream group name
                    proxy_set_header Host $host;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    add_header X-Release-Variant $api_upstream always;
                }
            }
        """,
        lang="nginx",
        follow=[
            ("How would you automate the decision to promote or roll back the canary?", "Canary promote করা বা rollback করার সিদ্ধান্ত কীভাবে automate করবে?"),
            ("When would you choose feature flags over infrastructure-level canaries?", "কখন infrastructure-level canary-র বদলে feature flag বেছে নেবে?"),
        ],
        related=["nginx-030", "nginx-007"],
        refs=[N_SPLIT, N_MAP, N_UPSTREAM],
    ),
]

if __name__ == "__main__":
    save("nginx", "b2", QUESTIONS)
