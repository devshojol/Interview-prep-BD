# Docker — batch 2: docker-005..007 (easy), docker-014..016 (medium), docker-024 (hard), docker-031 (extreme)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

D_NETWORK = ("Docker Docs — Networking overview", "https://docs.docker.com/engine/network/")
D_FIREWALL = ("Docker Docs — Packet filtering and firewalls", "https://docs.docker.com/engine/network/packet-filtering-firewalls/")
D_VOLUMES = ("Docker Docs — Volumes", "https://docs.docker.com/engine/storage/volumes/")
D_BIND = ("Docker Docs — Bind mounts", "https://docs.docker.com/engine/storage/bind-mounts/")
D_TMPFS = ("Docker Docs — tmpfs mounts", "https://docs.docker.com/engine/storage/tmpfs/")
D_CONTEXT = ("Docker Docs — Build context", "https://docs.docker.com/build/concepts/context/")
D_DOCKERFILE = ("Dockerfile reference", "https://docs.docker.com/reference/dockerfile/")
D_BEST = ("Docker Docs — Building best practices", "https://docs.docker.com/build/building/best-practices/")
D_MULTI = ("Docker Docs — Multi-stage builds", "https://docs.docker.com/build/building/multi-stage/")
D_NEXT_OUTPUT = ("Next.js Docs — output (standalone)", "https://nextjs.org/docs/app/api-reference/config/next-config-js/output")
D_COMPOSE_SERVICES = ("Compose file reference — services", "https://docs.docker.com/reference/compose-file/services/")
D_STARTUP = ("Docker Docs — Control startup order in Compose", "https://docs.docker.com/compose/how-tos/startup-order/")
D_PROFILES = ("Docker Docs — Using profiles with Compose", "https://docs.docker.com/compose/how-tos/profiles/")
D_RESOURCES = ("Docker Docs — Resource constraints", "https://docs.docker.com/engine/containers/resource_constraints/")
D_INSPECT = ("docker inspect reference", "https://docs.docker.com/reference/cli/docker/inspect/")
D_EVENTS = ("docker system events reference", "https://docs.docker.com/reference/cli/docker/system/events/")
D_NODE_PROCESS = ("Node.js — process (signal events)", "https://nodejs.org/api/process.html")
D_NODE_BP = ("Node.js Docker image — Best practices", "https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md")
D_SWARM_ROLLING = ("Docker Docs — Compose deploy specification", "https://docs.docker.com/reference/compose-file/deploy/")
N_RELOAD = ("NGINX — Controlling nginx (reload)", "https://nginx.org/en/docs/control.html")

QUESTIONS = [
    # ------------------------------------------------------------------ docker-005
    Q(
        id="docker-005", sub="Port Mapping", diff="easy", type="debugging",
        prio="high", market="both", mins=3,
        tags=["port-mapping", "localhost", "0.0.0.0", "networking", "express"],
        ver="Docker Engine 29, Node.js 24 LTS, Express 5.x", vs=False, status="stable",
        q_en=r"""
            You run `docker run -d -p 3000:3000 my-api`. `docker ps` shows the container is Up, and the logs say `API listening on 127.0.0.1:3000`. But `curl http://localhost:3000/health` from the host fails with "Connection reset by peer". Here is the startup code. What's wrong, and how do you fix it?
        """,
        q_bn=r"""
            তুমি `docker run -d -p 3000:3000 my-api` চালালে। `docker ps`-এ container Up দেখাচ্ছে, log-এ লেখা `API listening on 127.0.0.1:3000`। কিন্তু host থেকে `curl http://localhost:3000/health` চালালে "Connection reset by peer" error আসছে। নিচে startup code দেওয়া আছে। সমস্যা কী, আর কীভাবে ঠিক করবে?
        """,
        code=r"""
            // server.js
            import express from 'express';

            const app = express();
            app.get('/health', (req, res) => res.json({ ok: true }));

            app.listen(3000, '127.0.0.1', () => {
              console.log('API listening on 127.0.0.1:3000');
            });
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", label_en="Fixed: listen on all interfaces inside the container", label_bn="সমাধান: container-এর ভেতরে সব interface-এ listen করা", src=r"""
                const PORT = Number(process.env.PORT ?? 3000);
                const HOST = process.env.HOST ?? '0.0.0.0';

                app.listen(PORT, HOST, () => {
                  console.log(`API listening on ${HOST}:${PORT}`);
                });
            """),
            dict(lang="bash", label_en="Publish only on the host's loopback (when NGINX on the same host fronts the app)", label_bn="শুধু host-এর loopback-এ publish (একই host-এ NGINX সামনে থাকলে)", src=r"""
                docker run -d -p 127.0.0.1:3000:3000 my-api
                docker port my-api                                   # 3000/tcp -> 127.0.0.1:3000
                docker exec my-api wget -qO- http://127.0.0.1:3000/health   # works from inside
            """),
        ],
        a_en=r"""
            The app binds to `127.0.0.1`, but inside a container that's the **container's own loopback interface**, a separate network namespace from the host. Docker forwards published traffic to the container's network interface (an address like `172.17.0.2`), and nothing is listening there, so the connection is reset.

            **Fix:** listen on all interfaces inside the container: `0.0.0.0`, or omit the host so Node uses the unspecified address. Port publishing (`-p`) is what controls exposure on the host. If you don't want the port public, restrict it on the host side with `-p 127.0.0.1:3000:3000`.
        """,
        a_bn=r"""
            App `127.0.0.1`-এ bind করছে। কিন্তু container-এর ভেতরে এটা **container-এর নিজস্ব loopback interface**, যেটা host থেকে আলাদা একটা network namespace। Docker publish করা traffic container-এর network interface-এ (যেমন `172.17.0.2` ধরনের address) পাঠায়, আর সেখানে কেউ listen করছে না। তাই connection reset হয়ে যাচ্ছে।

            **সমাধান:** container-এর ভেতরে সব interface-এ listen করো: `0.0.0.0` দাও, অথবা host বাদ দাও, তাহলে Node unspecified address ব্যবহার করবে। Host-এ কতটা expose হবে সেটা নিয়ন্ত্রণ করে port publishing (`-p`)। Port public না চাইলে host side-এ সীমিত করো: `-p 127.0.0.1:3000:3000`।
        """,
        ex_en=r"""
            - **Prove it:** `docker exec my-api wget -qO- http://127.0.0.1:3000/health` works from inside the container, which shows the app itself is healthy and the problem is the bind address. `docker exec my-api netstat -tln` (BusyBox on Alpine) shows `127.0.0.1:3000` instead of `0.0.0.0:3000` or `:::3000`.
            - **Same trap with dev servers:** Vite listens on `localhost` by default, so use `vite --host` inside containers.
            - **Security flip side:** `-p 3000:3000` binds to all host interfaces. On a VPS that makes the app reachable from the internet, and Docker's published ports bypass ufw rules. Bind to `127.0.0.1` when a reverse proxy on the host sits in front.
        """,
        ex_bn=r"""
            - **প্রমাণ করো:** container-এর ভেতর থেকে `docker exec my-api wget -qO- http://127.0.0.1:3000/health` কাজ করে। এতে বোঝা যায় app নিজে ঠিক আছে, সমস্যা bind address-এ। `docker exec my-api netstat -tln` (Alpine-এ BusyBox) চালালে `0.0.0.0:3000` বা `:::3000`-এর বদলে `127.0.0.1:3000` দেখাবে।
            - **Dev server-এও একই ফাঁদ:** Vite default হিসেবে `localhost`-এ listen করে, তাই container-এ `vite --host` ব্যবহার করো।
            - **Security-র উল্টো দিক:** `-p 3000:3000` host-এর সব interface-এ bind করে। VPS-এ এতে app internet থেকে access করা যায়, আর Docker-এর publish করা port ufw rule bypass করে। Host-এ reverse proxy সামনে থাকলে `127.0.0.1`-এ bind করো।
        """,
        tip_en=r"""Explain it in terms of network namespaces: "localhost inside the container is not the host's localhost". Then add the host-side `127.0.0.1` binding to show you think about security too.""",
        tip_bn=r"""Network namespace দিয়ে ব্যাখ্যা করো: "container-এর ভেতরের localhost আর host-এর localhost এক না"। এরপর host side-এ `127.0.0.1` binding-এর কথা বলো, যাতে বোঝা যায় তুমি security নিয়েও ভাবো।""",
        mist_en=r"""Changing `EXPOSE` or the `-p` order to fix it, or "fixing" it by running with `--network host` and leaving the app exposed on every interface.""",
        mist_bn=r"""`EXPOSE` বা `-p`-এর order বদলে ঠিক করার চেষ্টা করা, অথবা `--network host` দিয়ে চালিয়ে "ঠিক" করা, যাতে app সব interface-এ খোলা পড়ে থাকে।""",
        follow=[
            ("Why do Docker-published ports bypass ufw, and how do you protect them?", "Docker-এর publish করা port কেন ufw bypass করে, আর কীভাবে এগুলো সুরক্ষিত রাখবে?"),
            ("How would you check which address a process is listening on inside a container?", "Container-এর ভেতরে কোনো process কোন address-এ listen করছে কীভাবে দেখবে?"),
        ],
        related=["docker-004"],
        refs=[D_NETWORK, D_FIREWALL],
    ),
    # ------------------------------------------------------------------ docker-006
    Q(
        id="docker-006", sub="Volumes and Bind Mounts", diff="easy", type="comparison",
        prio="high", market="both", mins=3,
        tags=["volumes", "bind-mounts", "tmpfs", "storage", "persistence"],
        ver="Docker Engine 29, Compose v5", vs=False, status="stable",
        q_en=r"""Compare Docker volumes, bind mounts and tmpfs mounts. When would you use each one?""",
        q_bn=r"""Docker volume, bind mount আর tmpfs mount-এর তুলনা করো। কোনটা কখন ব্যবহার করবে?""",
        a_en=r"""
            - **Named volume:** storage that Docker manages (under `/var/lib/docker/volumes/` on Linux). It's independent of the host's directory layout, survives `docker rm` and `docker compose down`, and the same volume definition works on any host or Docker Desktop (the data itself still lives on one host). **Use it for databases and any persistent app data in production.**
            - **Bind mount:** maps a specific host path into the container (`./src:/app/src`). The host and container see the same files live. **Use it for local development** (hot reload) or for sharing specific host files such as config. The downsides are host-path coupling, UID/permission mismatches and slower I/O on macOS/Windows.
            - **tmpfs:** in-memory only, never written to disk, and gone when the container stops. **Use it for scratch or sensitive temporary data**, such as `/tmp` in a read-only container.
        """,
        a_bn=r"""
            - **Named volume:** Docker নিজে যে storage manage করে (Linux-এ `/var/lib/docker/volumes/`-এর নিচে)। এটা host-এর directory structure-এর উপর নির্ভর করে না, `docker rm` বা `docker compose down`-এর পরেও থেকে যায়, আর একই volume definition যেকোনো host বা Docker Desktop-এ কাজ করে (তবে data নিজে একটা host-এই থাকে)। **Database আর production-এর যেকোনো persistent app data-র জন্য এটা ব্যবহার করো।**
            - **Bind mount:** host-এর একটা নির্দিষ্ট path container-এ map করে (`./src:/app/src`)। Host আর container একই file সরাসরি (live) দেখে। **Local development-এর জন্য ব্যবহার করো** (hot reload), অথবা config-এর মতো নির্দিষ্ট host file share করতে। অসুবিধা: host path-এর উপর নির্ভরতা, UID/permission mismatch, আর macOS/Windows-এ ধীর I/O।
            - **tmpfs:** শুধু memory-তে থাকে, কখনো disk-এ লেখা হয় না, container stop হলেই মুছে যায়। **Scratch বা sensitive temporary data-র জন্য ব্যবহার করো**, যেমন read-only container-এর `/tmp`।
        """,
        ex_en=r"""
            - **Volume initialisation:** when an **empty** named volume is mounted over a directory that already has files in the image, Docker copies those files (with their ownership) into the volume. Bind mounts don't do this. They simply hide whatever the image had at that path.
            - **Backups:** volumes are still just data on one host. Back them up (e.g. `pg_dump`, or a temporary container that tars the volume), and use managed databases when you need high availability.
            - `docker compose down` keeps named volumes; `docker compose down -v` deletes them. That's a classic way to lose a dev database.
            - **Image-specific paths matter.** For example, the PostgreSQL 18+ official image expects the volume at `/var/lib/postgresql` (older majors used `/var/lib/postgresql/data`).
            - **Prefer `--mount` syntax in scripts.** It's explicit, and it errors if a bind source doesn't exist instead of silently creating an empty root-owned directory.
        """,
        ex_bn=r"""
            - **Volume initialization:** image-এ আগে থেকে file আছে এমন directory-তে **খালি** named volume mount করলে Docker ওই file-গুলো (ownership-সহ) volume-এ copy করে দেয়। Bind mount এটা করে না। এটা শুধু image-এর ওই path-এ যা ছিল সেটা ঢেকে দেয়।
            - **Backup:** volume-ও শেষ পর্যন্ত একটা host-এর data। তাই backup নাও (যেমন `pg_dump`, বা একটা temporary container দিয়ে volume tar করা), আর high availability লাগলে managed database ব্যবহার করো।
            - `docker compose down` named volume রেখে দেয়; `docker compose down -v` সেগুলো delete করে। Dev database হারানোর এটা একটা classic উপায়।
            - **Image অনুযায়ী path গুরুত্বপূর্ণ।** যেমন PostgreSQL 18+ official image volume আশা করে `/var/lib/postgresql`-এ (আগের version-গুলো `/var/lib/postgresql/data` ব্যবহার করত)।
            - **Script-এ `--mount` syntax ব্যবহার করো।** এটা স্পষ্ট, আর bind source না থাকলে চুপচাপ root-owned খালি directory বানানোর বদলে error দেয়।
        """,
        tip_en=r"""Answer with a one-line rule: "volumes for data, bind mounts for dev, tmpfs for scratch". Then add one gotcha, such as `down -v` deleting data or bind-mount permission issues.""",
        tip_bn=r"""এক লাইনের rule দিয়ে উত্তর দাও: "data-র জন্য volume, dev-এর জন্য bind mount, scratch-এর জন্য tmpfs"। তারপর একটা gotcha যোগ করো, যেমন `down -v` দিলে data মুছে যাওয়া বা bind mount-এর permission সমস্যা।""",
        mist_en=r"""Storing database files in the container's writable layer (lost on `docker rm`), or using bind mounts to `/home/user/...` paths in production compose files.""",
        mist_bn=r"""Database file container-এর writable layer-এ রাখা (`docker rm` করলে হারিয়ে যায়), অথবা production compose file-এ `/home/user/...` ধরনের path-এ bind mount ব্যবহার করা।""",
        code=r"""
            services:
              db:
                image: postgres:18-alpine
                volumes:
                  - pgdata:/var/lib/postgresql      # named volume, managed by Docker
              api:
                build: .
                volumes:
                  - ./src:/app/src                  # bind mount, local development only
                tmpfs:
                  - /tmp                            # in-memory scratch space

            volumes:
              pgdata:
        """,
        lang="yaml",
        follow=[
            ("How would you back up and restore a named volume?", "একটা named volume-এর backup আর restore কীভাবে করবে?"),
            ("Why are bind mounts slow on Docker Desktop for macOS, and what are the alternatives?", "macOS-এর Docker Desktop-এ bind mount কেন ধীর, আর এর বিকল্প কী?"),
        ],
        related=["docker-002"],
        refs=[D_VOLUMES, D_BIND, D_TMPFS],
    ),
    # ------------------------------------------------------------------ docker-007
    Q(
        id="docker-007", sub="Build Context and .dockerignore", diff="easy", type="conceptual",
        prio="medium", market="both", mins=2,
        tags=["build-context", "dockerignore", "security", "build-performance"],
        ver="Docker Engine 29 / BuildKit", vs=False, status="stable",
        q_en=r"""What is the Docker build context, and why does every Node.js project need a `.dockerignore` file?""",
        q_bn=r"""Docker build context কী, আর প্রতিটা Node.js project-এ `.dockerignore` file কেন দরকার?""",
        a_en=r"""
            The **build context** is the set of files the builder can access during a build. In `docker build -t api .`, the final `.` is the context. `COPY` and `ADD` can only read files from it, and paths are relative to it.

            `.dockerignore` excludes files from the context, which matters for three reasons:
            - **Speed:** without it, `node_modules` and `.git` (often hundreds of MB) are transferred to the builder.
            - **Correct and cacheable builds:** a host `node_modules` built for macOS can end up inside a Linux image. Irrelevant file changes such as logs or `.git` also bust the cache of `COPY . .`.
            - **Security:** `.env` files, `.npmrc` tokens and keys are kept out of the image.
        """,
        a_bn=r"""
            **Build context** হলো build-এর সময় builder যে file-গুলো access করতে পারে তার সেট। `docker build -t api .`-এ শেষের `.`-টাই context। `COPY` আর `ADD` শুধু এখান থেকেই file পড়তে পারে, আর path-গুলো এর সাপেক্ষে ধরা হয়।

            `.dockerignore` context থেকে file বাদ দেয়। তিনটা কারণে এটা জরুরি:
            - **Speed:** এটা না থাকলে `node_modules` আর `.git` (প্রায়ই কয়েকশো MB) builder-এ পাঠানো হয়।
            - **সঠিক ও cacheable build:** macOS-এর জন্য build করা host `node_modules` Linux image-এ ঢুকে যেতে পারে। Log বা `.git`-এর মতো অপ্রাসঙ্গিক file বদলালেও `COPY . .`-এর cache নষ্ট হয়।
            - **Security:** `.env` file, `.npmrc` token আর key image-এর বাইরে থাকে।
        """,
        ex_en=r"""
            - BuildKit only transfers the files a build actually uses, and it transfers them incrementally. But `COPY . .` uses **everything** that isn't ignored, so the ignore file still matters.
            - Syntax is similar to `.gitignore`: `#` comments, `**` globs, and `!` exceptions (e.g. ignore `.env*` but keep `!.env.example`).
            - You can use a different Dockerfile location with `-f docker/api.Dockerfile` while keeping the repo root as context, which is common in monorepos. A per-Dockerfile ignore file (`api.Dockerfile.dockerignore`) is also supported.
            - If the build output shows a very large "transferring context" size, check your ignore file first.
        """,
        ex_bn=r"""
            - BuildKit শুধু সেই file-গুলো পাঠায় যেগুলো build-এ আসলে ব্যবহার হয়, আর পাঠায় incremental-ভাবে। কিন্তু `COPY . .` ignore না করা **সবকিছুই** ব্যবহার করে, তাই ignore file-এর গুরুত্ব থেকেই যায়।
            - Syntax `.gitignore`-এর মতোই: `#` comment, `**` glob, আর `!` exception (যেমন `.env*` ignore করে `!.env.example` রেখে দেওয়া)।
            - Repo root-কে context রেখেও `-f docker/api.Dockerfile` দিয়ে অন্য জায়গার Dockerfile ব্যবহার করা যায়, monorepo-তে এটা খুব common। প্রতিটা Dockerfile-এর জন্য আলাদা ignore file-ও (`api.Dockerfile.dockerignore`) support করে।
            - Build output-এ "transferring context"-এর size অনেক বড় দেখালে আগে ignore file পরীক্ষা করো।
        """,
        tip_en=r"""Name all three benefits (speed, cache correctness, security) and give a concrete example of each. "My `.env` got baked into the image" is a story interviewers remember.""",
        tip_bn=r"""তিনটা সুবিধাই (speed, cache-এর সঠিকতা, security) বলো, প্রতিটার একটা করে বাস্তব উদাহরণ দাও। "আমার `.env` image-এ ঢুকে গিয়েছিল" ধরনের গল্প interviewer-রা মনে রাখে।""",
        mist_en=r"""Assuming `.gitignore` is used by Docker (it isn't), or thinking a file is safe because it's deleted in a later `RUN` step.""",
        mist_bn=r"""ধরে নেওয়া যে Docker `.gitignore` ব্যবহার করে (করে না), অথবা ভাবা যে পরের কোনো `RUN` step-এ delete করলে file নিরাপদ।""",
        code=r"""
            # .dockerignore for a Node.js / Next.js project
            node_modules
            .next
            dist
            coverage
            .git
            .github
            *.log
            .env*
            !.env.example
            .npmrc
            Dockerfile*
            compose*.yaml
        """,
        lang="text",
        follow=[
            ("How does the build context work when the Dockerfile lives in a subfolder of a monorepo?", "Monorepo-র subfolder-এ Dockerfile থাকলে build context কীভাবে কাজ করে?"),
            ("Why can copying the host's node_modules break a Linux image?", "Host-এর node_modules copy করলে Linux image কেন ভেঙে যেতে পারে?"),
        ],
        related=["docker-012"],
        refs=[D_CONTEXT, D_BEST],
    ),
    # ------------------------------------------------------------------ docker-014
    Q(
        id="docker-014", sub="Dockerfiles", diff="medium", type="debugging",
        prio="high", market="both", mins=6,
        tags=["sigterm", "pid1", "graceful-shutdown", "exec-form", "exit-code"],
        ver="Docker Engine 29, Node.js 24 LTS", vs=False, status="stable",
        q_en=r"""
            During every deploy, users see failed requests. `docker stop api` always takes exactly 10 seconds, the container ends with exit code 137, and the app's `process.on('SIGTERM', …)` handler never logs anything. Here is the Dockerfile (`package.json` has `"start": "node server.js"`). Find the root cause and fix it.
        """,
        q_bn=r"""
            প্রতিটা deploy-এর সময় user-দের কিছু request fail করছে। `docker stop api` সবসময় ঠিক ১০ সেকেন্ড সময় নেয়, container exit code 137 দিয়ে বন্ধ হয়, আর app-এর `process.on('SIGTERM', …)` handler কিছুই log করে না। নিচে Dockerfile দেওয়া আছে (`package.json`-এ `"start": "node server.js"`)। মূল কারণ খুঁজে বের করো আর ঠিক করো।
        """,
        code=r"""
            FROM node:24-alpine
            WORKDIR /app
            COPY package*.json ./
            RUN npm ci --omit=dev
            COPY . .
            CMD npm start
        """,
        lang="dockerfile",
        extra=[
            dict(lang="dockerfile", label_en="Fixed Dockerfile (exec form, node is PID 1)", label_bn="সংশোধিত Dockerfile (exec form, node নিজেই PID 1)", src=r"""
                FROM node:24-alpine
                WORKDIR /app
                ENV NODE_ENV=production
                COPY package*.json ./
                RUN npm ci --omit=dev
                COPY . .
                USER node
                CMD ["node", "server.js"]
            """),
            dict(lang="javascript", label_en="Graceful shutdown in server.js", label_bn="server.js-এ graceful shutdown", src=r"""
                const server = app.listen(3000, '0.0.0.0');

                function shutdown(signal) {
                  console.log(`${signal} received, draining connections...`);
                  server.close(async () => {          // stop accepting, finish in-flight requests
                    await db.end();                   // close pools, flush logs, etc.
                    process.exit(0);
                  });
                  // Safety net: exit before Docker's SIGKILL deadline (default 10 s)
                  setTimeout(() => process.exit(1), 8_000).unref();
                }

                process.on('SIGTERM', shutdown);
                process.on('SIGINT', shutdown);
            """),
            dict(lang="yaml", label_en="Compose: optional init process and a longer grace period", label_bn="Compose: optional init process আর বেশি grace period", src=r"""
                services:
                  api:
                    build: .
                    init: true              # tiny init (tini) as PID 1: forwards signals, reaps zombies
                    stop_grace_period: 30s  # time between SIGTERM and SIGKILL
            """),
        ],
        a_en=r"""
            **Root cause:** `CMD npm start` is **shell form**, so Docker runs `/bin/sh -c "npm start"`. The shell becomes PID 1, with npm, and then node, as children. `docker stop` sends SIGTERM **only to PID 1**. The shell doesn't forward it, so Node never receives it and the handler never runs. After the 10-second grace period Docker sends **SIGKILL**, which gives exit code **137** (128 + 9) and kills in-flight requests.

            **Fix:**
            1. Use **exec form** and start Node directly: `CMD ["node", "server.js"]`. Node becomes PID 1 and receives the signal.
            2. Implement **graceful shutdown**: on SIGTERM call `server.close()`, finish in-flight requests, close DB pools and exit 0 before the deadline.
            3. Optionally use an init process (`docker run --init` or `init: true` in Compose) that forwards signals and reaps zombie processes. Tune `stop_grace_period` if requests can take longer than 10 seconds.
        """,
        a_bn=r"""
            **মূল কারণ:** `CMD npm start` হলো **shell form**, তাই Docker চালায় `/bin/sh -c "npm start"`। Shell হয় PID 1, আর npm ও তারপর node তার child process। `docker stop` SIGTERM পাঠায় **শুধু PID 1-কে**। Shell signal-টা forward করে না, ফলে Node কখনো SIGTERM পায় না, handler-ও চলে না। ১০ সেকেন্ডের grace period শেষে Docker **SIGKILL** পাঠায়। তাই exit code **137** (128 + 9), আর চলমান request-গুলো মাঝপথে মারা যায়।

            **সমাধান:**
            1. **Exec form** ব্যবহার করো আর সরাসরি Node চালাও: `CMD ["node", "server.js"]`। তাহলে Node নিজেই PID 1 হয় আর signal পায়।
            2. **Graceful shutdown** implement করো: SIGTERM পেলে `server.close()` call করো, চলমান request শেষ করো, DB pool বন্ধ করো, আর deadline-এর আগে exit 0 দাও।
            3. চাইলে একটা init process ব্যবহার করো (`docker run --init` বা Compose-এ `init: true`), যেটা signal forward করে আর zombie process পরিষ্কার করে। Request ১০ সেকেন্ডের বেশি সময় নিতে পারলে `stop_grace_period` বাড়াও।
        """,
        ex_en=r"""
            - **Exit codes:** 0 = clean graceful exit, 143 = terminated by SIGTERM (128 + 15) without handling it, 137 = SIGKILL (also what you see after an OOM kill, so check `OOMKilled` in `docker inspect`).
            - **PID 1 is special in Linux:** the kernel doesn't apply the default "terminate" action for signals the process hasn't installed a handler for. A bare `CMD ["node", "server.js"]` without a SIGTERM handler can therefore still ignore `docker stop`. Either handle the signal or run with `--init`.
            - Some shells happen to `exec` a single simple command, so shell form sometimes "works by luck". Don't rely on it, especially with `npm start` or `&&` chains. npm also adds an extra process layer for no benefit in production.
            - Orchestrators (Kubernetes, ECS, Swarm) use the same SIGTERM → grace period → SIGKILL sequence, so this fix matters everywhere.
            - Since Node 19, `server.close()` also closes idle keep-alive connections, so draining finishes faster.
        """,
        ex_bn=r"""
            - **Exit code:** 0 = পরিষ্কার graceful exit, 143 = SIGTERM handle না করে বন্ধ হওয়া (128 + 15), 137 = SIGKILL (OOM kill হলেও এটাই দেখা যায়, তাই `docker inspect`-এ `OOMKilled` দেখে নাও)।
            - **Linux-এ PID 1 বিশেষ:** যেসব signal-এর জন্য process handler install করেনি, সেগুলোর default "terminate" action kernel PID 1-এর ক্ষেত্রে প্রয়োগ করে না। তাই SIGTERM handler ছাড়া শুধু `CMD ["node", "server.js"]` দিলেও `docker stop` ignore হয়ে যেতে পারে। হয় signal handle করো, নয়তো `--init` দিয়ে চালাও।
            - কিছু shell একটা simple command নিজেই `exec` করে দেয়, তাই shell form মাঝে মাঝে "ভাগ্যক্রমে" কাজ করে। এর উপর ভরসা কোরো না, বিশেষ করে `npm start` বা `&&` chain-এর ক্ষেত্রে। Production-এ npm কোনো লাভ ছাড়াই একটা বাড়তি process layer যোগ করে।
            - Orchestrator-গুলোও (Kubernetes, ECS, Swarm) একই SIGTERM → grace period → SIGKILL ক্রম মানে, তাই এই fix সব জায়গায় কাজে লাগে।
            - Node 19 থেকে `server.close()` idle keep-alive connection-গুলোও বন্ধ করে, ফলে draining দ্রুত শেষ হয়।
        """,
        tip_en=r"""Connect the three symptoms to one cause: exactly 10 seconds = the grace period, 137 = SIGKILL, silent handler = the signal never reached Node. Showing you can read symptoms like that is what impresses.""",
        tip_bn=r"""তিনটা লক্ষণকে একটা কারণের সাথে মেলাও: ঠিক ১০ সেকেন্ড = grace period, 137 = SIGKILL, handler চুপ = signal Node পর্যন্ত পৌঁছায়নি। এভাবে লক্ষণ পড়তে পারাটাই interviewer-কে মুগ্ধ করে।""",
        mist_en=r""""Fixing" it by lowering the stop timeout, using `CMD ["npm", "start"]` (still an extra process layer), or calling `process.exit()` immediately on SIGTERM without draining requests.""",
        mist_bn=r"""Stop timeout কমিয়ে "ঠিক" করা, `CMD ["npm", "start"]` ব্যবহার করা (এখনো একটা বাড়তি process layer থাকে), অথবা request drain না করে SIGTERM পাওয়া মাত্র `process.exit()` call করা।""",
        follow=[
            ("What is a zombie process, and why does PID 1 need to reap them?", "Zombie process কী, আর PID 1-কে কেন এগুলো reap করতে হয়?"),
            ("How does graceful shutdown interact with a load balancer's health checks?", "Graceful shutdown-এর সাথে load balancer-এর health check কীভাবে সম্পর্কিত?"),
        ],
        related=["docker-013"],
        refs=[D_DOCKERFILE, D_NODE_BP, D_NODE_PROCESS],
    ),
    # ------------------------------------------------------------------ docker-015
    Q(
        id="docker-015", sub="Multi-stage Builds", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["multi-stage", "nextjs", "standalone", "non-root", "image-size"],
        ver="Next.js 16.4, Node.js 24 LTS, Docker Engine 29 / BuildKit", vs=True, status="stable",
        q_en=r"""
            Write a production Dockerfile for a Next.js 16 app configured with `output: 'standalone'`.

            Requirements:
            - multi-stage build based on `node:24-alpine`;
            - reproducible dependency install from `package-lock.json`, cached between builds;
            - the final image runs as a **non-root** user and contains only what's needed to run `node server.js` on port 3000 (no source code, no devDependencies, no build cache).
        """,
        q_bn=r"""
            `output: 'standalone'` configure করা একটা Next.js 16 app-এর জন্য production Dockerfile লেখো।

            Requirement:
            - `node:24-alpine`-ভিত্তিক multi-stage build;
            - `package-lock.json` থেকে reproducible dependency install, যেটা build-এর মধ্যে cache থাকবে;
            - final image **non-root** user হিসেবে চলবে, আর এতে শুধু port 3000-এ `node server.js` চালানোর জন্য যা দরকার তাই থাকবে (source code, devDependencies, build cache কিছুই না)।
        """,
        code=r"""
            # syntax=docker/dockerfile:1

            # ---- 1. Dependencies (cached until the lockfile changes)
            FROM node:24-alpine AS deps
            WORKDIR /app
            COPY package.json package-lock.json ./
            RUN --mount=type=cache,target=/root/.npm npm ci

            # ---- 2. Build
            FROM node:24-alpine AS builder
            WORKDIR /app
            COPY --from=deps /app/node_modules ./node_modules
            COPY . .
            ENV NEXT_TELEMETRY_DISABLED=1
            # NEXT_PUBLIC_* values are inlined at build time (pass them as build args if needed)
            RUN npm run build

            # ---- 3. Minimal runtime
            FROM node:24-alpine AS runner
            WORKDIR /app
            ENV NODE_ENV=production \
                NEXT_TELEMETRY_DISABLED=1 \
                PORT=3000 \
                HOSTNAME=0.0.0.0

            # standalone = server.js + only the node_modules it actually needs
            COPY --from=builder --chown=node:node /app/.next/standalone ./
            # static assets and public/ are NOT included in standalone automatically
            COPY --from=builder --chown=node:node /app/.next/static ./.next/static
            COPY --from=builder --chown=node:node /app/public ./public

            USER node
            EXPOSE 3000
            CMD ["node", "server.js"]
        """,
        lang="dockerfile",
        extra=[
            dict(lang="typescript", label_en="next.config.ts", label_bn="next.config.ts", src=r"""
                import type { NextConfig } from 'next';

                const nextConfig: NextConfig = {
                  output: 'standalone',
                };

                export default nextConfig;
            """),
        ],
        time="N/A (declarative build config)", space="N/A",
        a_en=r"""
            The solution uses three stages:

            1. **deps** copies only the manifests and runs `npm ci` with a BuildKit cache mount, so dependency installation is cached until the lockfile changes.
            2. **builder** copies `node_modules` and the source and runs `next build`. With `output: 'standalone'`, Next.js traces the files the server really imports and writes a self-contained `server.js` plus a minimal `node_modules` into `.next/standalone`.
            3. **runner** starts from a fresh `node:24-alpine` and copies only the standalone folder, `.next/static` and `public`, owned by the built-in `node` user. It runs as `USER node` with exec-form `CMD`, so Node is PID 1 and receives SIGTERM.

            The result is typically a few hundred MB smaller than shipping the full `node_modules` and source, and it doesn't contain compilers, tests or devDependencies.
        """,
        a_bn=r"""
            এই সমাধানে তিনটা stage আছে:

            1. **deps** শুধু manifest copy করে আর BuildKit cache mount দিয়ে `npm ci` চালায়। ফলে lockfile না বদলানো পর্যন্ত dependency install cache থাকে।
            2. **builder** `node_modules` আর source copy করে `next build` চালায়। `output: 'standalone'` থাকলে Next.js trace করে দেখে server আসলে কোন file-গুলো import করে, তারপর `.next/standalone`-এ একটা self-contained `server.js` আর minimal `node_modules` লেখে।
            3. **runner** নতুন একটা `node:24-alpine` থেকে শুরু করে শুধু standalone folder, `.next/static` আর `public` copy করে, built-in `node` user-এর ownership-এ। এটা `USER node` আর exec-form `CMD` দিয়ে চলে, তাই Node নিজেই PID 1 হয় আর SIGTERM পায়।

            পুরো `node_modules` আর source পাঠানোর তুলনায় এই image সাধারণত কয়েকশো MB ছোট হয়, আর এতে compiler, test বা devDependencies থাকে না।
        """,
        ex_en=r"""
            - **`HOSTNAME=0.0.0.0` matters:** Docker sets `HOSTNAME` to the container ID, and the standalone server binds to `HOSTNAME`. Without the override it may bind to the wrong interface and be unreachable through the published port.
            - **`public/` and `.next/static`** aren't copied into standalone. Forgetting them gives 404s for CSS/JS chunks and images. (If the project has no `public/` folder, that `COPY` fails, so create an empty one.)
            - **Build-time vs runtime env:** `NEXT_PUBLIC_*` variables are inlined into client bundles at build time. Server-only secrets should be provided at runtime, never as build args.
            - **Alpine (musl):** some native packages need extra handling on Alpine (Next.js examples sometimes add `libc6-compat`). If a dependency misbehaves, `node:24-slim` (glibc) is the easy fallback.
            - **Monorepos:** set `outputFileTracingRoot` so file tracing can include workspace packages.
            - **Writable cache:** ISR and image optimisation write to `.next/cache`, so it must be writable by the runtime user. The `--chown` copies handle that here.
        """,
        ex_bn=r"""
            - **`HOSTNAME=0.0.0.0` জরুরি:** Docker `HOSTNAME`-কে container ID দিয়ে set করে, আর standalone server `HOSTNAME`-এ bind করে। Override না করলে ভুল interface-এ bind হয়ে publish করা port দিয়ে access করা যায় না।
            - **`public/` আর `.next/static`** standalone-এ copy হয় না। ভুলে গেলে CSS/JS chunk আর image-এ 404 আসে। (Project-এ `public/` folder না থাকলে ওই `COPY` fail করবে, তাই একটা খালি folder বানিয়ে রাখো।)
            - **Build-time বনাম runtime env:** `NEXT_PUBLIC_*` variable build-এর সময় client bundle-এ inline হয়ে যায়। Server-only secret runtime-এ দাও, কখনো build arg হিসেবে না।
            - **Alpine (musl):** কিছু native package-এর জন্য Alpine-এ বাড়তি কাজ লাগে (Next.js-এর example-এ মাঝে মাঝে `libc6-compat` যোগ করা হয়)। কোনো dependency ঝামেলা করলে সহজ বিকল্প হলো `node:24-slim` (glibc)।
            - **Monorepo:** `outputFileTracingRoot` set করো, যাতে file tracing workspace package-গুলোও ধরতে পারে।
            - **Writable cache:** ISR আর image optimization `.next/cache`-এ লেখে, তাই runtime user-এর এখানে লেখার অনুমতি থাকতে হবে। এখানে `--chown` দিয়ে copy করায় সেটা ঠিক আছে।
        """,
        tip_en=r"""Walk through it stage by stage and say **why** each stage exists. Mentioning the `HOSTNAME` and missing-static-assets gotchas shows you've actually deployed this, not just copied a template.""",
        tip_bn=r"""Stage ধরে ধরে ব্যাখ্যা করো আর প্রতিটা stage **কেন** আছে সেটা বলো। `HOSTNAME` আর static asset বাদ পড়ার gotcha উল্লেখ করলে বোঝা যায় তুমি আসলেই এটা deploy করেছ, শুধু template copy করোনি।""",
        mist_en=r"""Running `next start` with the full `node_modules` in the final image, forgetting `.next/static`/`public`, putting secrets in `ARG`/`ENV`, and running as root.""",
        mist_bn=r"""Final image-এ পুরো `node_modules` রেখে `next start` চালানো, `.next/static`/`public` copy করতে ভুলে যাওয়া, `ARG`/`ENV`-এ secret রাখা, আর root হিসেবে চালানো।""",
        follow=[
            ("How would you pass a different `NEXT_PUBLIC_API_URL` for staging and production?", "Staging আর production-এর জন্য আলাদা `NEXT_PUBLIC_API_URL` কীভাবে দেবে?"),
            ("How would you add a health check to this image?", "এই image-এ health check কীভাবে যোগ করবে?"),
        ],
        related=["docker-012", "docker-014"],
        refs=[D_MULTI, D_NEXT_OUTPUT, D_BEST],
    ),
    # ------------------------------------------------------------------ docker-016
    Q(
        id="docker-016", sub="Docker Compose", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["compose", "depends-on", "healthcheck", "postgres", "redis"],
        ver="Docker Compose v5.6, PostgreSQL 18, Redis 8", vs=True, status="stable",
        q_en=r"""
            Write a `compose.yaml` for an Express API (built from the local Dockerfile) that needs PostgreSQL 18 and Redis 8.

            Requirements:
            - the API must not start until Postgres actually accepts connections;
            - database data must survive `docker compose down`;
            - the DB password comes from a `.env` file, and Compose should fail fast if it's missing;
            - only the API is reachable from the host, and only on `127.0.0.1:3000`;
            - a one-off `migrate` command that is **not** started by a normal `docker compose up`.
        """,
        q_bn=r"""
            একটা Express API-র জন্য `compose.yaml` লেখো (local Dockerfile থেকে build হবে), যার PostgreSQL 18 আর Redis 8 লাগে।

            Requirement:
            - Postgres সত্যিই connection নেওয়ার জন্য তৈরি না হওয়া পর্যন্ত API start হবে না;
            - `docker compose down` করলেও database-এর data থেকে যাবে;
            - DB password আসবে `.env` file থেকে, আর সেটা না থাকলে Compose সাথে সাথে fail করবে;
            - host থেকে শুধু API-তে পৌঁছানো যাবে, তাও শুধু `127.0.0.1:3000`-এ;
            - একটা one-off `migrate` command থাকবে, যেটা সাধারণ `docker compose up`-এ start **হবে না**।
        """,
        code=r"""
            # compose.yaml  (no top-level "version:" — it's obsolete)
            services:
              api:
                build: .
                ports:
                  - "127.0.0.1:3000:3000"
                environment:
                  NODE_ENV: production
                  DATABASE_URL: postgres://app:${POSTGRES_PASSWORD}@db:5432/app
                  REDIS_URL: redis://cache:6379
                depends_on:
                  db:
                    condition: service_healthy
                  cache:
                    condition: service_healthy
                restart: unless-stopped

              db:
                image: postgres:18-alpine
                environment:
                  POSTGRES_USER: app
                  POSTGRES_DB: app
                  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?set POSTGRES_PASSWORD in .env}
                volumes:
                  - pgdata:/var/lib/postgresql        # PostgreSQL 18+ image path
                healthcheck:
                  test: ["CMD-SHELL", "pg_isready -U app -d app"]
                  interval: 5s
                  timeout: 3s
                  retries: 10
                  start_period: 10s
                restart: unless-stopped

              cache:
                image: redis:8-alpine
                healthcheck:
                  test: ["CMD", "redis-cli", "ping"]
                  interval: 5s
                  timeout: 3s
                  retries: 5
                restart: unless-stopped

              migrate:
                build: .
                command: ["node", "dist/migrate.js"]
                environment:
                  DATABASE_URL: postgres://app:${POSTGRES_PASSWORD}@db:5432/app
                depends_on:
                  db:
                    condition: service_healthy
                profiles: ["tools"]                    # only runs when the profile is enabled

            volumes:
              pgdata:
        """,
        lang="yaml",
        extra=[
            dict(lang="bash", label_en="Usage", label_bn="ব্যবহার", src=r"""
                echo 'POSTGRES_PASSWORD=change-me-strong' > .env    # git-ignored
                docker compose config                               # render & validate the final file
                docker compose --profile tools run --rm migrate     # one-off migration
                docker compose up -d --build
                docker compose ps                                   # db/cache show "(healthy)"
                docker compose down                                 # keeps the pgdata volume
            """),
        ],
        time="N/A (declarative config)", space="N/A",
        a_en=r"""
            - **Startup order:** short-form `depends_on` only waits for the db **container to start**, not for Postgres to be ready. The long form with `condition: service_healthy`, combined with a `pg_isready` healthcheck, makes Compose wait until the database accepts connections.
            - **Persistence:** the named volume `pgdata` survives `docker compose down` (only `down -v` deletes it). For PostgreSQL 18+ images the volume is mounted at `/var/lib/postgresql`.
            - **Secrets and config:** `${POSTGRES_PASSWORD:?…}` is interpolated from `.env` and aborts with a clear message if it's unset. The value reaches containers only because it's referenced in `environment:`.
            - **Networking:** all services share the project's default network, so the API reaches `db:5432` and `cache:6379` by service name. Only the API publishes a port, bound to `127.0.0.1`.
            - **Profiles:** `migrate` belongs to the `tools` profile, so a plain `up` ignores it and you run it on demand.
        """,
        a_bn=r"""
            - **Startup order:** short-form `depends_on` শুধু db **container start হওয়া** পর্যন্ত অপেক্ষা করে, Postgres ready হওয়া পর্যন্ত না। Long form-এ `condition: service_healthy` আর সাথে `pg_isready` healthcheck দিলে Compose database connection নেওয়ার উপযুক্ত না হওয়া পর্যন্ত অপেক্ষা করে।
            - **Persistence:** named volume `pgdata` `docker compose down`-এর পরেও থেকে যায় (শুধু `down -v` দিলে মুছে যায়)। PostgreSQL 18+ image-এ volume mount করতে হয় `/var/lib/postgresql`-এ।
            - **Secret ও config:** `${POSTGRES_PASSWORD:?…}` `.env` থেকে interpolate হয়, আর set না থাকলে পরিষ্কার message দিয়ে থেমে যায়। Value container-এ পৌঁছায় শুধু কারণ `environment:`-এ এটা reference করা হয়েছে।
            - **Networking:** সব service project-এর default network share করে, তাই API service name দিয়েই `db:5432` আর `cache:6379`-এ পৌঁছায়। শুধু API port publish করে, তাও `127.0.0.1`-এ bind করা।
            - **Profiles:** `migrate` `tools` profile-এর অংশ, তাই সাধারণ `up` এটাকে উপেক্ষা করে আর দরকার হলে আলাদাভাবে চালানো যায়।
        """,
        ex_en=r"""
            - **No `version:` key:** Compose v2+ (now v5) ignores the top-level `version` and warns about it. The file is validated against the Compose Specification.
            - **Health check timing:** `start_period` gives Postgres time to initialise on first boot without counting failures. After that, `interval × retries` bounds how long dependants wait before Compose gives up because the dependency is unhealthy.
            - **Readiness at startup isn't enough.** The app should still retry DB connections at runtime, because the database can restart later. `depends_on` only orders startup.
            - **Passwords in URLs:** special characters in the password must be URL-encoded in `DATABASE_URL`.
            - **Production:** for real production you'd usually run Postgres as a managed service, keep secrets in `secrets:` or a secret manager, and add resource limits and log rotation (see docker-028).
        """,
        ex_bn=r"""
            - **`version:` key নেই:** Compose v2+ (এখন v5) top-level `version` উপেক্ষা করে আর warning দেয়। File-টা Compose Specification অনুযায়ী validate হয়।
            - **Health check-এর timing:** প্রথমবার boot-এ Postgres-এর initialize হতে সময় লাগে, `start_period` সেই সময়টা দেয় আর তখনকার failure গোনে না। এরপর `interval × retries` ঠিক করে dependent service সর্বোচ্চ কতক্ষণ অপেক্ষা করবে, তারপর dependency unhealthy বলে Compose হাল ছেড়ে দেয়।
            - **Startup-এর সময়ের readiness যথেষ্ট না।** Database পরে restart হতে পারে, তাই app-কে runtime-এও DB connection retry করতে হবে। `depends_on` শুধু startup-এর ক্রম ঠিক করে।
            - **URL-এ password:** password-এ special character থাকলে `DATABASE_URL`-এ সেগুলো URL-encode করতে হবে।
            - **Production:** আসল production-এ সাধারণত Postgres managed service হিসেবে চালানো হয়, secret রাখা হয় `secrets:` বা secret manager-এ, আর resource limit ও log rotation যোগ করা হয় (docker-028 দেখো)।
        """,
        tip_en=r"""Point out the difference between "container started" and "service healthy". It's the most common Compose bug in real projects. Then mention `docker compose config` as your way to verify interpolation.""",
        tip_bn=r""""Container start হয়েছে" আর "service healthy"-এর পার্থক্যটা ধরিয়ে দাও। বাস্তব project-এ Compose-এর সবচেয়ে common bug এটাই। এরপর বলো interpolation যাচাই করতে তুমি `docker compose config` ব্যবহার করো।""",
        mist_en=r"""Using `localhost` in `DATABASE_URL`, adding `version: "3.9"`, publishing Postgres on `0.0.0.0:5432` "for convenience", and using `docker compose down -v` casually.""",
        mist_bn=r"""`DATABASE_URL`-এ `localhost` ব্যবহার করা, `version: "3.9"` যোগ করা, "সুবিধার জন্য" Postgres-কে `0.0.0.0:5432`-এ publish করা, আর না ভেবে `docker compose down -v` চালানো।""",
        follow=[
            ("How would you add hot reload for local development to this setup?", "এই setup-এ local development-এর জন্য hot reload কীভাবে যোগ করবে?"),
            ("What's the difference between `.env` interpolation and `env_file:`?", "`.env` interpolation আর `env_file:`-এর মধ্যে পার্থক্য কী?"),
        ],
        related=["docker-006"],
        refs=[D_STARTUP, D_COMPOSE_SERVICES, D_PROFILES],
    ),
    # ------------------------------------------------------------------ docker-024
    Q(
        id="docker-024", sub="Container Debugging", diff="hard", type="scenario",
        prio="high", market="both", mins=10,
        tags=["exit-code-137", "oom", "debugging", "memory-limits", "nodejs-heap"],
        ver="Docker Engine 29, Node.js 24 LTS", vs=False, status="stable",
        q_en=r"""In production, your Node.js API container keeps restarting, and `docker ps` shows `Restarting (137)`. Walk me through how you would find the root cause and fix it.""",
        q_bn=r"""Production-এ তোমার Node.js API container বারবার restart হচ্ছে, আর `docker ps`-এ দেখাচ্ছে `Restarting (137)`। Root cause কীভাবে খুঁজে বের করবে আর ঠিক করবে, ধাপে ধাপে বলো।""",
        a_en=r"""
            Exit code **137 = 128 + 9**, so the main process was killed with **SIGKILL**. It didn't crash on its own; something killed it. The usual suspects are the kernel **OOM killer** (memory limit reached), a stop or deploy that ran past its grace period, or an external tool. My steps:

            1. **Confirm the cause:** `docker inspect` the `ExitCode`, `OOMKilled` and `RestartCount`. `OOMKilled=true` means the cgroup memory limit was hit.
            2. **Correlate in time:** `docker events --filter container=api` shows `oom`, `kill`, `die` and restart events with timestamps. The host's kernel log (`dmesg`/`journalctl -k`) shows OOM-killer messages, including host-level memory pressure.
            3. **Observe:** `docker stats` for memory vs limit, and `docker logs --since 30m api`. Restarts keep the same container, so earlier runs' logs are still there.
            4. **Diagnose the app:** is memory climbing steadily (a leak: unbounded caches, listeners, global arrays) or spiking (huge JSON bodies, buffering whole files)? Is the **V8 heap limit higher than the container limit**? If so, the cgroup kills the process before V8 ever throws "JavaScript heap out of memory", so you never see a JS error.
            5. **Fix:** set `--max-old-space-size` below the limit (about 75% leaves room for buffers and native memory), right-size the limit from real metrics, find the leak with heap snapshots (`--heapsnapshot-near-heap-limit`), and stream large payloads.

            If `OOMKilled=false`, look for who sent SIGKILL: deploy scripts with too-short stop timeouts, a health-check-driven restart by an orchestrator, or someone running `docker kill`.
        """,
        a_bn=r"""
            Exit code **137 = 128 + 9**, মানে main process-কে **SIGKILL** দিয়ে মারা হয়েছে। Process নিজে crash করেনি; অন্য কিছু এটাকে kill করেছে। সাধারণ সন্দেহভাজন: kernel-এর **OOM killer** (memory limit শেষ), grace period পার হয়ে যাওয়া stop বা deploy, অথবা বাইরের কোনো tool। আমার ধাপগুলো:

            1. **কারণ নিশ্চিত করো:** `docker inspect` দিয়ে `ExitCode`, `OOMKilled` আর `RestartCount` দেখো। `OOMKilled=true` মানে cgroup memory limit-এ পৌঁছে গেছে।
            2. **সময় মিলিয়ে দেখো:** `docker events --filter container=api` timestamp-সহ `oom`, `kill`, `die` আর restart event দেখায়। Host-এর kernel log (`dmesg`/`journalctl -k`) OOM-killer-এর message দেখায়, host-level memory চাপ থাকলে সেটাও।
            3. **পর্যবেক্ষণ করো:** `docker stats` দিয়ে memory বনাম limit, আর `docker logs --since 30m api`। Restart হলেও container একটাই থাকে, তাই আগের run-গুলোর log-ও পাওয়া যায়।
            4. **App diagnose করো:** memory কি ধীরে ধীরে বাড়ছে (leak: সীমাহীন cache, listener, global array) নাকি হঠাৎ লাফ দিচ্ছে (বিশাল JSON body, পুরো file buffer করা)? **V8 heap limit কি container limit-এর চেয়ে বেশি?** তাহলে V8 "JavaScript heap out of memory" throw করার আগেই cgroup process-টাকে মেরে ফেলে, ফলে কোনো JS error-ই দেখা যায় না।
            5. **সমাধান:** `--max-old-space-size` limit-এর নিচে রাখো (প্রায় ৭৫% রাখলে buffer আর native memory-র জায়গা থাকে), বাস্তব metric দেখে limit ঠিক করো, heap snapshot (`--heapsnapshot-near-heap-limit`) দিয়ে leak খুঁজে বের করো, আর বড় payload stream করো।

            `OOMKilled=false` হলে খোঁজো কে SIGKILL পাঠাল: খুব ছোট stop timeout-ওয়ালা deploy script, orchestrator-এর health-check-ভিত্তিক restart, অথবা কেউ `docker kill` চালিয়েছে কি না।
        """,
        ex_en=r"""
            - **RSS vs heap:** the container limit applies to the whole process RSS: V8 heap plus Buffers, native addons, thread stacks and worker threads. `--max-old-space-size` only caps the old-generation heap, so leave headroom.
            - **Restart policy back-off:** Docker waits progressively longer between restarts of a crash-looping container. Logs and `RestartCount` stay with the same container.
            - **Exit codes cheat sheet:** 0 = clean exit, 1 = app error (uncaught exception), 137 = SIGKILL/OOM, 139 = segfault (often a native module), 143 = SIGTERM without a handler.
            - **Don't just raise the limit.** A leak will eventually eat any limit. Use limits to make failures fast and visible, and alert on memory trends.
            - **Kubernetes parallel:** `kubectl describe pod` shows `OOMKilled` and `kubectl logs --previous` shows the last run's logs. Docker has no `--previous` flag because it's the same container.
        """,
        ex_bn=r"""
            - **RSS বনাম heap:** container limit পুরো process-এর RSS-এর উপর প্রযোজ্য: V8 heap, Buffer, native addon, thread stack আর worker thread সব মিলিয়ে। `--max-old-space-size` শুধু old-generation heap সীমিত করে, তাই বাড়তি জায়গা রাখো।
            - **Restart policy-র back-off:** কোনো container বারবার crash করলে Docker প্রতিটা restart-এর মাঝে ক্রমশ বেশি সময় অপেক্ষা করে। Log আর `RestartCount` একই container-এর সাথেই থাকে।
            - **Exit code-এর ছোট তালিকা:** 0 = পরিষ্কার exit, 1 = app error (uncaught exception), 137 = SIGKILL/OOM, 139 = segfault (প্রায়ই native module-এর কারণে), 143 = handler ছাড়া SIGTERM।
            - **শুধু limit বাড়িয়ে দিয়ো না।** Leak থাকলে শেষ পর্যন্ত যেকোনো limit খেয়ে ফেলবে। Limit ব্যবহার করো যাতে failure দ্রুত আর দৃশ্যমান হয়, আর memory trend-এর উপর alert রাখো।
            - **Kubernetes-এ একই জিনিস:** `kubectl describe pod`-এ `OOMKilled` দেখা যায়, আর `kubectl logs --previous` দিয়ে আগের run-এর log দেখা যায়। Docker-এ `--previous` flag নেই, কারণ container একটাই।
        """,
        tip_en=r"""Decode the number first ("137 means SIGKILL, so something killed it"), then show a methodical evidence trail (inspect → events → kernel log → metrics) before proposing fixes. Interviewers penalise jumping straight to "increase memory".""",
        tip_bn=r"""আগে সংখ্যাটা ব্যাখ্যা করো ("137 মানে SIGKILL, তাই অন্য কিছু এটাকে মেরেছে")। তারপর সমাধান প্রস্তাবের আগে পদ্ধতিগতভাবে প্রমাণ জোগাড় করা দেখাও (inspect → events → kernel log → metrics)। সরাসরি "memory বাড়িয়ে দাও" বললে interviewer নম্বর কাটে।""",
        mist_en=r"""Assuming 137 always means OOM (check `OOMKilled`), looking only for JS stack traces (an OOM kill leaves none), and setting the heap limit equal to the container limit.""",
        mist_bn=r"""ধরে নেওয়া যে 137 মানেই সবসময় OOM (`OOMKilled` দেখে নিশ্চিত হও), শুধু JS stack trace খোঁজা (OOM kill-এ কোনো trace থাকে না), আর heap limit-কে container limit-এর সমান রাখা।""",
        code=r"""
            # 1. Why did it die?
            docker inspect -f 'exit={{.State.ExitCode}} oom={{.State.OOMKilled}} restarts={{.RestartCount}}' api

            # 2. When, and what happened around it?
            docker events --since 1h --filter container=api
            sudo journalctl -k --since "1 hour ago" | grep -i -E "oom|killed process"

            # 3. Live memory vs limit, and recent logs
            docker stats --no-stream api
            docker logs --since 30m --timestamps api | tail -n 100
        """,
        lang="bash",
        extra=[
            dict(lang="yaml", label_en="Compose: memory limit with a matching Node heap cap", label_bn="Compose: memory limit আর মানানসই Node heap cap", src=r"""
                services:
                  api:
                    image: registry.example.com/api:2.3.1
                    restart: unless-stopped
                    environment:
                      NODE_OPTIONS: "--max-old-space-size=384"   # ~75% of the 512 MiB limit
                    deploy:
                      resources:
                        limits:
                          memory: 512M
            """),
        ],
        follow=[
            ("How would you capture a heap snapshot from a container that's about to be OOM-killed?", "OOM-kill হতে যাওয়া container থেকে heap snapshot কীভাবে নেবে?"),
            ("What would exit code 139 suggest in a Node.js container?", "Node.js container-এ exit code 139 দেখলে কী সন্দেহ করবে?"),
        ],
        related=["docker-014"],
        refs=[D_INSPECT, D_EVENTS, D_RESOURCES],
    ),
    # ------------------------------------------------------------------ docker-031
    Q(
        id="docker-031", sub="Production Deployment", diff="extreme", type="system-design",
        prio="medium", market="both", mins=20,
        tags=["zero-downtime", "blue-green", "nginx", "graceful-shutdown", "compose"],
        ver="Docker Engine 29, Compose v5, NGINX 1.30", vs=False, status="stable",
        q_en=r"""A fintech startup runs its Node.js API with Docker on two VMs behind NGINX. Every deploy (`docker compose pull && docker compose up -d`) causes 10–30 seconds of 502 errors, and the team isn't ready for Kubernetes. Design a zero-downtime deployment approach.""",
        q_bn=r"""একটা fintech startup দুটো VM-এ NGINX-এর পেছনে Docker দিয়ে তাদের Node.js API চালায়। প্রতিটা deploy-এ (`docker compose pull && docker compose up -d`) ১০–৩০ সেকেন্ড ধরে 502 error আসে, আর team এখনো Kubernetes-এর জন্য প্রস্তুত না। একটা zero-downtime deployment পদ্ধতি design করো।""",
        a_en=r"""
            **(Advanced.)** **Why it fails today:** `compose up -d` with a new image **stops the old container, then starts the new one**. NGINX keeps sending traffic to an upstream that's gone (502), and the new app isn't ready the moment it starts. Old requests are also cut off if the app doesn't drain on SIGTERM.

            **Design: blue/green per host, rolling across hosts.**
            1. **App prerequisites:** graceful shutdown on SIGTERM (stop accepting, drain, close pools); separate `/live` and `/ready` endpoints; stateless instances (sessions and caches in Redis); DB migrations in **expand/contract** style so old and new versions both work against the same schema.
            2. **Per VM:** two slots, `api_blue` on `127.0.0.1:3001` and `api_green` on `127.0.0.1:3002`. NGINX's upstream points at the active slot via an included file.
            3. **Deploy steps:** pull the new image **by digest** → start it in the idle slot → wait until its health check reports `healthy` (abort if not; the old slot is untouched) → rewrite the upstream include → `nginx -t && nginx -s reload` (graceful: old workers finish their requests) → `docker stop -t 30` the old slot so it drains → keep its image for instant rollback.
            4. **Across VMs:** deploy VM1, verify error rate and latency, then VM2. If a cloud load balancer sits in front, deregister and drain each VM first.
            5. **Rollback:** switch the include back and reload. That takes seconds and needs no rebuild.

            **Alternatives:** Docker Swarm mode (`deploy.update_config.order: start-first` gives rolling updates with health checks), or tools like Kamal that script exactly this flow. When the service count grows, a managed orchestrator (ECS, EKS) becomes worth its complexity.
        """,
        a_bn=r"""
            **(Advanced।)** **এখন কেন fail করছে:** নতুন image নিয়ে `compose up -d` করলে **আগে পুরনো container stop হয়, তারপর নতুনটা start হয়**। NGINX তখনো চলে যাওয়া upstream-এ traffic পাঠাতে থাকে (502), আর নতুন app start হওয়ার সাথে সাথেই ready থাকে না। App SIGTERM-এ drain না করলে পুরনো request-গুলোও মাঝপথে কেটে যায়।

            **Design: প্রতিটা host-এ blue/green, host-গুলোর মধ্যে rolling।**
            1. **App-এর পূর্বশর্ত:** SIGTERM-এ graceful shutdown (নতুন request নেওয়া বন্ধ, drain, pool বন্ধ); আলাদা `/live` আর `/ready` endpoint; stateless instance (session আর cache Redis-এ); DB migration **expand/contract** ধাঁচে, যাতে একই schema-তে পুরনো আর নতুন দুই version-ই চলে।
            2. **প্রতিটা VM-এ:** দুটো slot, `api_blue` আছে `127.0.0.1:3001`-এ আর `api_green` আছে `127.0.0.1:3002`-এ। NGINX-এর upstream একটা include করা file দিয়ে active slot-কে point করে।
            3. **Deploy-এর ধাপ:** নতুন image **digest দিয়ে** pull করো → idle slot-এ start করো → health check `healthy` না দেখানো পর্যন্ত অপেক্ষা করো (না হলে abort; পুরনো slot অক্ষত থাকে) → upstream include নতুন করে লেখো → `nginx -t && nginx -s reload` (graceful: পুরনো worker-রা নিজেদের request শেষ করে) → পুরনো slot-কে `docker stop -t 30` দিয়ে drain করতে দাও → তাৎক্ষণিক rollback-এর জন্য এর image রেখে দাও।
            4. **VM-গুলোর মধ্যে:** আগে VM1-এ deploy করো, error rate আর latency যাচাই করো, তারপর VM2। সামনে cloud load balancer থাকলে প্রতিটা VM আগে deregister করে drain করো।
            5. **Rollback:** include আগের মতো ফিরিয়ে reload করো। কয়েক সেকেন্ড লাগে, rebuild লাগে না।

            **বিকল্প:** Docker Swarm mode (`deploy.update_config.order: start-first` health check-সহ rolling update দেয়), অথবা Kamal-এর মতো tool, যেগুলো ঠিক এই flow-টাই script করে। Service-এর সংখ্যা বাড়লে managed orchestrator (ECS, EKS)-এর জটিলতা মেনে নেওয়ার মতো হয়ে যায়।
        """,
        ex_en=r"""
            **Failure scenarios to cover:**
            - The new version never becomes healthy → the script aborts before touching NGINX, so users never see it.
            - A bad NGINX config → `nginx -t` blocks the reload. A failed reload also leaves the old config running.
            - Long-lived WebSocket connections keep old NGINX workers alive after a reload. `worker_shutdown_timeout` bounds this, and clients must reconnect.
            - A migration that isn't backward-compatible breaks the **old** version mid-deploy. That's why expand → deploy → contract happens across separate releases.
            - Background workers (queues, cron) need the same drain-then-stop treatment, and jobs must be idempotent.

            **Observability during rollout:** watch 5xx rate, p95 latency and `$upstream_response_time` in NGINX logs, and roll back automatically when thresholds are breached.
        """,
        ex_bn=r"""
            **যেসব failure scenario কভার করতে হবে:**
            - নতুন version কখনো healthy হলো না → script NGINX-এ হাত দেওয়ার আগেই abort করে, user কিছুই টের পায় না।
            - NGINX config ভুল → `nginx -t` reload আটকে দেয়। Reload fail করলেও পুরনো config চলতে থাকে।
            - দীর্ঘস্থায়ী WebSocket connection reload-এর পরেও পুরনো NGINX worker-দের বাঁচিয়ে রাখে। `worker_shutdown_timeout` এর সময়সীমা বেঁধে দেয়, আর client-কে reconnect করতে হয়।
            - Backward-compatible না এমন migration deploy-এর মাঝখানে **পুরনো** version ভেঙে দেয়। এজন্যই expand → deploy → contract আলাদা আলাদা release-এ করা হয়।
            - Background worker-দেরও (queue, cron) একইভাবে drain করে stop করতে হয়, আর job-গুলো idempotent হতে হবে।

            **Rollout-এর সময় observability:** 5xx rate, p95 latency আর NGINX log-এর `$upstream_response_time` নজরে রাখো, threshold পার হলে নিজে থেকে rollback করো।
        """,
        tip_en=r"""Start by explaining **why** the current deploy causes 502s (stop-then-start plus no readiness). Diagnosing before designing signals seniority. Then present the flow as numbered steps and finish with failure modes and the "when to move to an orchestrator" threshold.""",
        tip_bn=r"""শুরুতেই ব্যাখ্যা করো এখনকার deploy-এ **কেন** 502 আসছে (আগে stop তারপর start, আর readiness নেই)। Design-এর আগে diagnose করলে seniority বোঝা যায়। তারপর flow-টা নম্বর দেওয়া ধাপে দেখাও, শেষ করো failure mode আর "কখন orchestrator-এ যাওয়া উচিত" সেই সীমারেখা দিয়ে।""",
        mist_en=r"""Assuming `docker compose up -d` does rolling updates, switching traffic before the new container is ready, and ignoring database migration compatibility.""",
        mist_bn=r"""ধরে নেওয়া যে `docker compose up -d` rolling update করে, নতুন container ready হওয়ার আগেই traffic switch করা, আর database migration-এর compatibility উপেক্ষা করা।""",
        code=r"""
            #!/usr/bin/env bash
            # deploy.sh <digest> — blue/green on one host behind NGINX
            set -euo pipefail
            IMAGE="registry.example.com/pay/api@${1:?usage: deploy.sh sha256:...}"

            ACTIVE=$(cat /etc/nginx/api_active 2>/dev/null || echo blue)
            if [ "$ACTIVE" = blue ]; then NEXT=green; PORT=3002; else NEXT=blue; PORT=3001; fi

            docker rm -f "api_$NEXT" 2>/dev/null || true
            docker run -d --name "api_$NEXT" --init --restart unless-stopped \
              --env-file /etc/api/env -p "127.0.0.1:$PORT:3000" \
              --health-cmd "wget -qO- http://127.0.0.1:3000/ready || exit 1" \
              --health-interval 5s --health-retries 6 \
              "$IMAGE"

            for _ in $(seq 1 30); do
              [ "$(docker inspect -f '{{.State.Health.Status}}' "api_$NEXT")" = healthy ] && break
              sleep 2
            done
            if [ "$(docker inspect -f '{{.State.Health.Status}}' "api_$NEXT")" != healthy ]; then
              echo "new version unhealthy; aborting (old version still serving)"; exit 1
            fi

            echo "server 127.0.0.1:$PORT;" > /etc/nginx/api_upstream.inc
            nginx -t && nginx -s reload          # graceful: old workers finish in-flight requests
            echo "$NEXT" > /etc/nginx/api_active

            docker stop -t 30 "api_$ACTIVE"      # SIGTERM, drain, SIGKILL only after 30 s
        """,
        lang="bash",
        extra=[
            dict(lang="nginx", label_en="NGINX upstream that includes the active slot", label_bn="Active slot include করা NGINX upstream", src=r"""
                upstream api {
                    include /etc/nginx/api_upstream.inc;   # "server 127.0.0.1:3001;" or ":3002"
                }

                server {
                    listen 443 ssl;
                    http2 on;
                    server_name api.example.com;
                    # ssl_certificate ... ;

                    location / {
                        proxy_pass http://api;
                        proxy_set_header Host $host;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_set_header X-Forwarded-Proto $scheme;
                    }
                }
            """),
        ],
        follow=[
            ("How would you run a backward-incompatible database migration with this setup?", "এই setup-এ backward-incompatible database migration কীভাবে চালাবে?"),
            ("At what point would you move this team to ECS or Kubernetes?", "কোন পর্যায়ে এই team-কে ECS বা Kubernetes-এ নিয়ে যাবে?"),
        ],
        related=["docker-014", "docker-030"],
        refs=[D_SWARM_ROLLING, D_INSPECT, N_RELOAD],
    ),
]

if __name__ == "__main__":
    save("docker", "b2", QUESTIONS)
