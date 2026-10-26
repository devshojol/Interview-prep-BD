# Docker — batch 3: docker-008..010 (easy), docker-017..019 (medium), docker-025..026 (hard)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

D_DOCKERFILE = ("Dockerfile reference", "https://docs.docker.com/reference/dockerfile/")
D_SECRETS = ("Docker Docs — Build secrets", "https://docs.docker.com/build/building/secrets/")
D_COMPOSE_VERSION = ("Compose file reference — version and name", "https://docs.docker.com/reference/compose-file/version-and-name/")
D_COMPOSE_MIGRATE = ("Docker Docs — Migrate to Compose v2", "https://docs.docker.com/compose/releases/migrate/")
D_COMPOSE = ("Docker Docs — Docker Compose", "https://docs.docker.com/compose/")
D_NETWORK = ("Docker Docs — Networking overview", "https://docs.docker.com/engine/network/")
D_BRIDGE = ("Docker Docs — Bridge network driver", "https://docs.docker.com/engine/network/drivers/bridge/")
D_HOST_NET = ("Docker Docs — Host network driver", "https://docs.docker.com/engine/network/drivers/host/")
D_FIREWALL = ("Docker Docs — Packet filtering and firewalls", "https://docs.docker.com/engine/network/packet-filtering-firewalls/")
D_SECURITY = ("Docker Docs — Docker Engine security", "https://docs.docker.com/engine/security/")
D_COMPOSE_SERVICES = ("Compose file reference — services", "https://docs.docker.com/reference/compose-file/services/")
D_NODE_BP = ("Node.js Docker image — Best practices", "https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md")
D_RESTART = ("Docker Docs — Start containers automatically", "https://docs.docker.com/engine/containers/start-containers-automatically/")
D_CACHE_OPT = ("Docker Docs — Optimize cache usage in builds", "https://docs.docker.com/build/cache/optimize/")
D_CACHE = ("Docker Docs — Docker build cache", "https://docs.docker.com/build/cache/")
OWASP_DOCKER = ("OWASP — Docker Security Cheat Sheet", "https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html")

QUESTIONS = [
    # ------------------------------------------------------------------ docker-008
    Q(
        id="docker-008", sub="Environment Variables", diff="easy", type="mcq",
        prio="high", market="bangladesh", mins=2,
        tags=["arg", "env", "dockerfile", "build-args"],
        ver="Dockerfile syntax 1.x (BuildKit, Docker Engine 29)", vs=False, status="stable",
        q_en=r"""Which statement about `ARG` and `ENV` in a Dockerfile is correct?""",
        q_bn=r"""Dockerfile-এর `ARG` আর `ENV` সম্পর্কে কোন কথাটা সঠিক?""",
        options=[
            ("`ARG` values are automatically available to the running container as environment variables",
             "`ARG`-এর value চলমান container-এ নিজে থেকেই environment variable হিসেবে পাওয়া যায়"),
            ("`ENV` values are only available during the build and are discarded in the final image",
             "`ENV`-এর value শুধু build-এর সময় থাকে, final image-এ বাদ পড়ে যায়"),
            ("An `ARG` declared before the first `FROM` is automatically available inside every build stage",
             "প্রথম `FROM`-এর আগে declare করা `ARG` নিজে থেকেই প্রতিটা build stage-এর ভেতরে পাওয়া যায়"),
            ("`ARG` exists only during the build (unless copied into an `ENV`), and build-arg values can still appear in image history/provenance, so neither is suitable for secrets",
             "`ARG` শুধু build-এর সময় থাকে (`ENV`-এ copy না করলে), আর build-arg-এর value image history/provenance-এ দেখা যেতে পারে; তাই দুটোর কোনোটাই secret-এর জন্য উপযুক্ত না"),
        ],
        correct=3,
        a_en=r"""The "build time only, and not for secrets" answer is correct. `ARG` is a build-time variable, set with `docker build --build-arg NAME=value`, that disappears after the build unless you copy it into an `ENV`. `ENV` is stored in the image config and is present in every container started from the image (overridable with `docker run -e`). Build-arg values can show up in `docker history` and provenance attestations, and `ENV` is visible via `docker inspect`, so neither is safe for secrets. Use BuildKit secret mounts for those.""",
        a_bn=r""""শুধু build time, আর secret-এর জন্য না" উত্তরটাই সঠিক। `ARG` হলো build-time variable, যেটা `docker build --build-arg NAME=value` দিয়ে set করা হয়, আর `ENV`-এ copy না করলে build শেষে হারিয়ে যায়। `ENV` image config-এ সংরক্ষিত থাকে, আর ওই image থেকে চালানো প্রতিটা container-এ থাকে (`docker run -e` দিয়ে override করা যায়)। Build-arg-এর value `docker history` আর provenance attestation-এ দেখা যেতে পারে, আর `ENV` `docker inspect`-এ দেখা যায়। তাই কোনোটাই secret-এর জন্য নিরাপদ না। Secret-এর জন্য BuildKit secret mount ব্যবহার করো।""",
        quick_en=r"""`ARG` exists only during the build (unless copied into an `ENV`), while `ENV` is stored in the image and present in every container. Build-arg values can show up in history and provenance, and `ENV` in `docker inspect`, so neither is safe for secrets; use BuildKit secret mounts.""",
        quick_bn=r"""`ARG` শুধু build-এর সময় থাকে (`ENV`-এ copy না করলে), আর `ENV` image-এ থেকে যায়, প্রতিটা container-এ পাওয়া যায়। Build-arg-এর value history আর provenance-এ, আর `ENV` `docker inspect`-এ দেখা যায়, তাই কোনোটাই secret-এর জন্য নিরাপদ না; secret-এর জন্য BuildKit secret mount ব্যবহার করো।""",
        ex_en=r"""
            The "available inside every build stage" option is the tempting trap. An `ARG` before the first `FROM` can only be used **in `FROM` lines** (e.g. `ARG NODE_VERSION=24` then `FROM node:${NODE_VERSION}-alpine`). To use it inside a stage, redeclare `ARG NODE_VERSION` after that stage's `FROM`.

            A common pattern is a build-time default that also becomes runtime config: `ARG APP_VERSION` followed by `ENV APP_VERSION=$APP_VERSION`. Remember that changing an `ARG` value invalidates the build cache from the first instruction that uses it.
        """,
        ex_bn=r"""
            "প্রতিটা build stage-এর ভেতরে পাওয়া যায়" option-টাই বিভ্রান্তিকর ফাঁদ। প্রথম `FROM`-এর আগের `ARG` শুধু **`FROM` line-এই** ব্যবহার করা যায় (যেমন `ARG NODE_VERSION=24`, তারপর `FROM node:${NODE_VERSION}-alpine`)। কোনো stage-এর ভেতরে ব্যবহার করতে চাইলে সেই stage-এর `FROM`-এর পরে আবার `ARG NODE_VERSION` declare করতে হয়।

            একটা common pattern হলো build-time default-কে runtime config-ও বানানো: `ARG APP_VERSION`, তারপর `ENV APP_VERSION=$APP_VERSION`। মনে রেখো, `ARG`-এর value বদলালে যে instruction-এ এটা প্রথম ব্যবহার হয়েছে সেখান থেকে build cache invalid হয়ে যায়।
        """,
        tip_en=r"""Summarise it as "ARG = build time, ENV = build time and run time", then add "neither is for secrets". That last part is what interviewers are really checking.""",
        tip_bn=r"""এভাবে সংক্ষেপে বলো: "ARG = build time, ENV = build time ও run time", তারপর যোগ করো "কোনোটাই secret-এর জন্য না"। Interviewer আসলে শেষের অংশটাই যাচাই করছে।""",
        related=["docker-023"],
        refs=[D_DOCKERFILE, D_SECRETS],
    ),
    # ------------------------------------------------------------------ docker-009
    Q(
        id="docker-009", sub="Docker Compose", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["compose", "version-key", "docker-compose-v1", "compose-spec"],
        ver="Docker Compose v5.6 (Compose Specification)", vs=True, status="stable",
        q_en=r"""A repo has a `docker-compose.yml` that starts with `version: "3.8"`, and its README says to run `docker-compose up`. On a machine with current Docker (Engine 29, Compose v5), which statement is correct?""",
        q_bn=r"""একটা repo-তে `docker-compose.yml` আছে যেটা `version: "3.8"` দিয়ে শুরু, আর README-তে লেখা `docker-compose up` চালাতে। বর্তমান Docker (Engine 29, Compose v5) আছে এমন machine-এ কোন কথাটা সঠিক?""",
        options=[
            ("The file won't run until you delete `version:`, because Compose v5 rejects it",
             "`version:` মুছে না ফেলা পর্যন্ত file-টা চলবে না, কারণ Compose v5 এটা reject করে"),
            ("`version:` is obsolete: Compose ignores it with a warning and validates against the Compose Specification. Use the `docker compose` CLI plugin; the old Python `docker-compose` v1 is end-of-life",
             "`version:` obsolete: Compose একটা warning দিয়ে এটা উপেক্ষা করে আর Compose Specification অনুযায়ী validate করে। `docker compose` CLI plugin ব্যবহার করো; পুরনো Python `docker-compose` v1 end-of-life"),
            ("You must keep `version: \"3.8\"`, because `depends_on` conditions need the 3.x schema",
             "`version: \"3.8\"` রাখতেই হবে, কারণ `depends_on` condition-এর জন্য 3.x schema লাগে"),
            ("Compose v5 only reads files named `compose.yaml`, so `docker-compose.yml` is ignored",
             "Compose v5 শুধু `compose.yaml` নামের file পড়ে, তাই `docker-compose.yml` উপেক্ষা করা হয়"),
        ],
        correct=1,
        a_en=r"""The "`version:` is obsolete" answer is correct. Modern Compose implements the **Compose Specification**, where the top-level `version` is obsolete and only triggers a warning. Run it as `docker compose up` (a space, the Docker CLI plugin). The original Python `docker-compose` v1 reached end-of-life in 2023. Prefer naming new files `compose.yaml` and simply delete the `version:` line.""",
        a_bn=r""""`version:` obsolete" উত্তরটাই সঠিক। আধুনিক Compose **Compose Specification** implement করে, যেখানে top-level `version` obsolete, এটা শুধু একটা warning দেয়। চালাও `docker compose up` দিয়ে (মাঝে space, Docker CLI plugin)। আসল Python-ভিত্তিক `docker-compose` v1 ২০২৩ সালে end-of-life হয়ে গেছে। নতুন file-এর নাম `compose.yaml` রাখাই ভালো, আর `version:` line-টা মুছে দাও।""",
        quick_en=r"""`version:` is obsolete: modern Compose ignores it with a warning and validates against the Compose Specification. Run `docker compose up` (the CLI plugin), because the old Python `docker-compose` v1 is end-of-life, and simply delete the `version:` line.""",
        quick_bn=r"""`version:` এখন obsolete: আধুনিক Compose এটা warning দিয়ে ignore করে আর Compose Specification অনুযায়ী validate করে। `docker compose up` (CLI plugin) চালাও, কারণ পুরনো Python `docker-compose` v1 end-of-life; আর `version:` line-টা মুছে দাও।""",
        ex_en=r"""
            "Compose v5 rejects `version:`" is the tempting wrong answer. Compose doesn't fail on `version:`; it warns that the attribute is obsolete. The `depends_on` option reflects history: the old v3 **file format** dropped `depends_on` conditions, but the Compose Specification brought them back (`condition: service_healthy`) with no version key needed. As for file names, Compose still looks for `compose.yaml`, `compose.yml`, `docker-compose.yaml` and `docker-compose.yml`, preferring `compose.yaml`.

            On some Linux distributions `docker-compose` (with a hyphen) is installed as a standalone binary of the **new** Go-based Compose. The real problem is the legacy Python v1, which doesn't understand newer features such as profiles or `develop.watch`.
        """,
        ex_bn=r"""
            "Compose v5 `version:` reject করে" হলো বিভ্রান্তিকর ভুল উত্তর। `version:` থাকলে Compose fail করে না, শুধু warning দেয় যে attribute-টা obsolete। `depends_on`-এর option-টা আসলে ইতিহাস: পুরনো v3 **file format** `depends_on` condition বাদ দিয়েছিল, কিন্তু Compose Specification সেগুলো (`condition: service_healthy`) ফিরিয়ে এনেছে, কোনো version key ছাড়াই। File name-এর ক্ষেত্রে: Compose এখনো `compose.yaml`, `compose.yml`, `docker-compose.yaml` আর `docker-compose.yml` খোঁজে, তবে `compose.yaml`-কে অগ্রাধিকার দেয়।

            কিছু Linux distribution-এ `docker-compose` (hyphen-সহ) আসলে **নতুন** Go-ভিত্তিক Compose-এর standalone binary হিসেবে install করা থাকে। আসল সমস্যা হলো legacy Python v1, যেটা profiles বা `develop.watch`-এর মতো নতুন feature বোঝে না।
        """,
        tip_en=r"""Mentioning "the Compose Specification replaced the versioned file formats" shows you've kept up to date, which is a quick credibility win in DevOps interviews.""",
        tip_bn=r""""Compose Specification version-ভিত্তিক file format-গুলোর জায়গা নিয়েছে" বললে বোঝা যায় তুমি হালনাগাদ আছ। DevOps interview-এ এটা দ্রুত বিশ্বাসযোগ্যতা এনে দেয়।""",
        related=["docker-016"],
        refs=[D_COMPOSE_VERSION, D_COMPOSE_MIGRATE, D_COMPOSE],
    ),
    # ------------------------------------------------------------------ docker-010
    Q(
        id="docker-010", sub="Networks and DNS", diff="easy", type="debugging",
        prio="high", market="both", mins=3,
        tags=["compose", "localhost", "service-name", "dns", "econnrefused"],
        ver="Docker Compose v5, PostgreSQL 18", vs=False, status="stable",
        q_en=r"""
            The API worked when it ran on the laptop with `npm run dev`. After moving it into Compose, it crashes on startup with `Error: connect ECONNREFUSED 127.0.0.1:5432`, even though `docker compose ps` shows the `db` service running. What's wrong, and how do you fix it?
        """,
        q_bn=r"""
            Laptop-এ `npm run dev` দিয়ে চালালে API ঠিকঠাক কাজ করত। Compose-এ নেওয়ার পর startup-এই `Error: connect ECONNREFUSED 127.0.0.1:5432` দিয়ে crash করছে, যদিও `docker compose ps`-এ `db` service running দেখাচ্ছে। সমস্যা কী, আর কীভাবে ঠিক করবে?
        """,
        code=r"""
            services:
              api:
                build: .
                ports:
                  - "127.0.0.1:3000:3000"
                environment:
                  DATABASE_URL: postgres://app:secret@localhost:5432/app

              db:
                image: postgres:18-alpine
                environment:
                  POSTGRES_USER: app
                  POSTGRES_PASSWORD: secret
                  POSTGRES_DB: app
                ports:
                  - "5432:5432"
        """,
        lang="yaml",
        extra=[
            dict(lang="yaml", label_en="Fixed compose.yaml", label_bn="সংশোধিত compose.yaml", src=r"""
                services:
                  api:
                    build: .
                    ports:
                      - "127.0.0.1:3000:3000"
                    environment:
                      DATABASE_URL: postgres://app:secret@db:5432/app   # service name, not localhost
                    depends_on:
                      db:
                        condition: service_healthy

                  db:
                    image: postgres:18-alpine
                    environment:
                      POSTGRES_USER: app
                      POSTGRES_PASSWORD: secret        # demo only; use .env/secrets for real setups
                      POSTGRES_DB: app
                    healthcheck:
                      test: ["CMD-SHELL", "pg_isready -U app -d app"]
                      interval: 5s
                      retries: 10
                    # no "ports:" needed; the API reaches db over the Compose network
            """),
        ],
        a_en=r"""
            Inside the `api` container, `localhost` (127.0.0.1) means **the api container itself**. Each container has its own network namespace, and Postgres isn't running there. On the laptop it worked because both processes shared the host's loopback.

            **Fix:** use the **service name** as the hostname: `postgres://app:secret@db:5432/app`. Compose puts all services on a project network with built-in DNS, so `db` resolves to the database container's IP. Also add a healthcheck plus `depends_on: condition: service_healthy` so the API doesn't race Postgres on startup. You can drop `ports: "5432:5432"` unless you really need host access (and then bind it to `127.0.0.1`).
        """,
        a_bn=r"""
            `api` container-এর ভেতরে `localhost` (127.0.0.1) মানে **api container নিজেই**। প্রতিটা container-এর নিজস্ব network namespace থাকে, আর Postgres সেখানে চলছে না। Laptop-এ কাজ করত কারণ দুটো process-ই host-এর একই loopback share করত।

            **সমাধান:** hostname হিসেবে **service name** ব্যবহার করো: `postgres://app:secret@db:5432/app`। Compose সব service-কে built-in DNS-সহ একটা project network-এ রাখে, তাই `db` database container-এর IP-তে resolve হয়। সাথে healthcheck আর `depends_on: condition: service_healthy` যোগ করো, যাতে startup-এ API Postgres-এর সাথে race না করে। Host থেকে access সত্যিই না লাগলে `ports: "5432:5432"` বাদ দিতে পারো (লাগলে `127.0.0.1`-এ bind করো)।
        """,
        quick_en=r"""Inside the `api` container, `localhost` is the api container itself, not Postgres. Use the service name as the host (`db:5432`), which Compose's DNS resolves, and add a healthcheck with `depends_on: condition: service_healthy` so the API doesn't race the database on startup.""",
        quick_bn=r"""`api` container-এর ভেতরে `localhost` মানে api container নিজেই, Postgres না। Host হিসেবে service name (`db:5432`) দাও, Compose-এর DNS এটা resolve করে। সাথে healthcheck আর `depends_on: condition: service_healthy` দাও, যাতে startup-এ API database-এর আগে দৌড়ে না যায়।""",
        ex_en=r"""
            - **Published ports are for the host, not for container-to-container traffic.** Containers talk directly over the network on the **container** port (5432), whatever the host mapping is.
            - **The DB runs on the host, not in Compose?** Use `host.docker.internal`. Docker Desktop provides it automatically. On Linux, add `extra_hosts: ["host.docker.internal:host-gateway"]`.
            - Publishing Postgres on `0.0.0.0:5432` on a VPS exposes it to the internet, and Docker's rules bypass ufw. Avoid it.
            - **Debug quickly:** `docker compose exec api getent hosts db` (or `nslookup db`) checks DNS, and `docker compose exec api nc -zv db 5432` checks the port (if those tools exist in the image).
        """,
        ex_bn=r"""
            - **Publish করা port host-এর জন্য, container-থেকে-container traffic-এর জন্য না।** Container-রা host mapping যাই হোক, network-এর মধ্য দিয়ে সরাসরি **container** port (5432)-এ কথা বলে।
            - **DB Compose-এ না চলে host-এ চললে?** `host.docker.internal` ব্যবহার করো। Docker Desktop এটা নিজে থেকেই দেয়। Linux-এ `extra_hosts: ["host.docker.internal:host-gateway"]` যোগ করো।
            - VPS-এ Postgres `0.0.0.0:5432`-এ publish করলে সেটা internet-এ খুলে যায়, আর Docker-এর rule ufw bypass করে। এটা এড়িয়ে চলো।
            - **দ্রুত debug:** `docker compose exec api getent hosts db` (বা `nslookup db`) দিয়ে DNS, আর `docker compose exec api nc -zv db 5432` দিয়ে port যাচাই করো (image-এ tool-গুলো থাকলে)।
        """,
        tip_en=r"""Say the key sentence explicitly: "localhost inside a container is that container". Then give both fixes: the service name for Compose services, and `host.docker.internal` for services on the host.""",
        tip_bn=r"""মূল বাক্যটা স্পষ্ট করে বলো: "container-এর ভেতরের localhost মানে ওই container নিজেই"। তারপর দুটো সমাধানই দাও: Compose service-এর জন্য service name, আর host-এ চলা service-এর জন্য `host.docker.internal`।""",
        mist_en=r"""Using the host-mapped port instead of the container port, using container IP addresses (they change on recreate), or switching everything to `network_mode: host` to "fix" it.""",
        mist_bn=r"""Container port-এর বদলে host-এ map করা port ব্যবহার করা, container-এর IP address ব্যবহার করা (recreate করলে বদলে যায়), অথবা "ঠিক" করতে সবকিছু `network_mode: host`-এ নিয়ে যাওয়া।""",
        follow=[
            ("How does Docker's embedded DNS resolve service names?", "Docker-এর embedded DNS কীভাবে service name resolve করে?"),
            ("How would the API reach a Postgres instance running directly on the host machine?", "সরাসরি host machine-এ চলা Postgres-এ API কীভাবে পৌঁছাবে?"),
        ],
        related=["docker-005", "docker-016"],
        refs=[D_NETWORK, D_BRIDGE, D_COMPOSE_SERVICES],
    ),
    # ------------------------------------------------------------------ docker-017
    Q(
        id="docker-017", sub="Non-root Containers", diff="medium", type="security-performance",
        prio="high", market="both", mins=6,
        tags=["non-root", "user", "capabilities", "read-only", "hardening"],
        ver="Docker Engine 29, Node.js 24 (Maintenance LTS) images", vs=False, status="stable",
        q_en=r"""Why shouldn't a production container run as root? How do you run a Node.js container as a non-root user, and what else would you lock down?""",
        q_bn=r"""Production container root হিসেবে চালানো কেন উচিত না? Node.js container কীভাবে non-root user হিসেবে চালাবে, আর এর বাইরে কী কী lock down করবে?""",
        a_en=r"""
            By default, the process in a container runs as **root (UID 0)**. Without user-namespace remapping or rootless mode, that's the same UID 0 as on the host. Namespaces and the default capability set limit it, but if an attacker gets code execution (for example through a vulnerable npm package), as root they can modify app files, install tools, read every mounted secret and abuse writable bind mounts. If a container-escape bug exists, they become root on the host. Running as non-root **limits the blast radius**.

            **How:** official `node` images ship a `node` user (UID 1000). Copy files with `COPY --chown=node:node`, make only the directories that truly need writing owned by `node`, switch with `USER node`, and listen on a high port such as 3000.

            **Defence in depth:**
            - read-only root filesystem (`read_only: true` plus a `tmpfs` for `/tmp`);
            - `cap_drop: [ALL]` (a Node API needs no Linux capabilities);
            - `no-new-privileges` so setuid binaries can't escalate;
            - never `--privileged`, never mount `/var/run/docker.sock`;
            - memory/CPU/PID limits, a minimal base image and CVE scanning.
        """,
        a_bn=r"""
            Default হিসেবে container-এর process চলে **root (UID 0)** হিসেবে। User-namespace remapping বা rootless mode না থাকলে এটা host-এর UID 0-এর সমান। Namespace আর default capability set এটাকে কিছুটা সীমিত করে। কিন্তু attacker যদি code execution পেয়ে যায় (যেমন vulnerable npm package দিয়ে), root হিসেবে সে app file বদলাতে পারে, tool install করতে পারে, mount করা সব secret পড়তে পারে, আর writable bind mount অপব্যবহার করতে পারে। Container-escape bug থাকলে host-এরও root হয়ে যায়। Non-root চালালে **ক্ষতির পরিধি (blast radius) কমে**।

            **কীভাবে:** official `node` image-এ একটা `node` user (UID 1000) থাকে। `COPY --chown=node:node` দিয়ে file copy করো, শুধু যেসব directory-তে সত্যিই লেখা দরকার সেগুলো `node`-এর ownership-এ দাও, `USER node` দিয়ে switch করো, আর 3000-এর মতো high port-এ listen করো।

            **Defence in depth:**
            - read-only root filesystem (`read_only: true`, আর `/tmp`-এর জন্য একটা `tmpfs`);
            - `cap_drop: [ALL]` (Node API-র কোনো Linux capability লাগে না);
            - `no-new-privileges`, যাতে setuid binary দিয়ে privilege বাড়ানো না যায়;
            - কখনো `--privileged` না, কখনো `/var/run/docker.sock` mount না;
            - memory/CPU/PID limit, minimal base image আর CVE scanning।
        """,
        quick_en=r"""Without user-namespace remapping or rootless mode, root in a container is UID 0 on the host too, so a compromised app can do far more damage, especially after a container escape. Run as the image's `node` user (`COPY --chown`, `USER node`) and add a read-only filesystem, `cap_drop: [ALL]` and `no-new-privileges`.""",
        quick_bn=r"""User-namespace remapping বা rootless mode ছাড়া container-এর root আর host-এর root একই UID 0, তাই app hack হলে অনেক বেশি ক্ষতি হতে পারে, বিশেষ করে container escape হলে। Image-এর `node` user দিয়ে চালাও (`COPY --chown`, `USER node`), সাথে read-only filesystem, `cap_drop: [ALL]` আর `no-new-privileges` দাও।""",
        ex_en=r"""
            - **Verify it:** `docker exec api id` should print `uid=1000(node)`, and `docker inspect -f '{{.Config.User}}' image` shows the configured user.
            - **Kubernetes `runAsNonRoot: true`** can only verify a **numeric** UID. If you target Kubernetes, `USER 1000:1000` (or setting `runAsUser`) avoids a "cannot verify user is non-root" error.
            - **Permissions trap:** `WORKDIR` creates directories as root. Anything the app writes (uploads, `.next/cache`) must be `chown`ed in the Dockerfile, or it will fail with `EACCES`.
            - **Port binding:** stick to high ports in the container and map 80/443 on the host or reverse proxy. It's portable across runtimes and avoids needing extra capabilities.
            - **Stronger isolation:** user-namespace remapping or rootless Docker make container root map to an unprivileged host UID.
        """,
        ex_bn=r"""
            - **যাচাই করো:** `docker exec api id` চালালে `uid=1000(node)` দেখানো উচিত, আর `docker inspect -f '{{.Config.User}}' image` configure করা user দেখায়।
            - **Kubernetes-এর `runAsNonRoot: true`** শুধু **numeric** UID যাচাই করতে পারে। Kubernetes-এ চালালে `USER 1000:1000` দিলে (বা `runAsUser` set করলে) "cannot verify user is non-root" error এড়ানো যায়।
            - **Permission-এর ফাঁদ:** `WORKDIR` directory তৈরি করে root হিসেবে। App যেখানে লেখে (upload, `.next/cache`), সেগুলো Dockerfile-এ `chown` করতে হবে, নইলে `EACCES` দিয়ে fail করবে।
            - **Port binding:** container-এ high port ব্যবহার করো আর 80/443 host বা reverse proxy-তে map করো। এটা সব runtime-এ portable, আর বাড়তি capability লাগে না।
            - **আরও শক্ত isolation:** user-namespace remapping বা rootless Docker container-এর root-কে host-এর একটা unprivileged UID-তে map করে।
        """,
        tip_en=r"""Frame it as risk → mitigation: "If someone gets RCE through a dependency, what can they do?" Then layer the controls. Mentioning `cap_drop: [ALL]` and read-only filesystems shows you go beyond the basic `USER` line.""",
        tip_bn=r"""Risk → mitigation ধাঁচে সাজাও: "কেউ dependency দিয়ে RCE পেলে কী করতে পারবে?" তারপর control-গুলো একটার পর একটা যোগ করো। `cap_drop: [ALL]` আর read-only filesystem উল্লেখ করলে বোঝা যায় তুমি শুধু `USER` line-এ থেমে থাকো না।""",
        mist_en=r"""Thinking "it's in a container, so root is harmless", adding `USER node` but leaving writable directories owned by root (runtime `EACCES`), or running containers with `--privileged` to fix permission errors.""",
        mist_bn=r"""ভাবা যে "container-এর ভেতরে আছে, তাই root ক্ষতিকর না", `USER node` যোগ করে writable directory-গুলো root-এর ownership-এ রেখে দেওয়া (runtime-এ `EACCES`), অথবা permission error ঠিক করতে `--privileged` দিয়ে container চালানো।""",
        code=r"""
            FROM node:24-slim
            WORKDIR /app
            ENV NODE_ENV=production
            COPY --chown=node:node package*.json ./
            RUN npm ci --omit=dev
            COPY --chown=node:node . .
            # Only the uploads dir must be writable at runtime
            RUN mkdir -p /app/uploads && chown node:node /app/uploads
            USER node
            EXPOSE 3000
            CMD ["node", "server.js"]
        """,
        lang="dockerfile",
        extra=[
            dict(lang="yaml", label_en="Runtime hardening in compose.yaml", label_bn="compose.yaml-এ runtime hardening", src=r"""
                services:
                  api:
                    image: registry.example.com/api:1.4.0
                    read_only: true
                    tmpfs:
                      - /tmp
                    volumes:
                      - uploads:/app/uploads      # the only writable path
                    cap_drop: ["ALL"]
                    security_opt:
                      - "no-new-privileges:true"
                    deploy:
                      resources:
                        limits:
                          memory: 512M
                          cpus: "1.0"
                          pids: 200               # PID limit (don't also set a conflicting pids_limit)

                volumes:
                  uploads:
            """),
        ],
        follow=[
            ("What does rootless Docker change compared with simply using `USER node`?", "শুধু `USER node` ব্যবহারের তুলনায় rootless Docker কী পরিবর্তন আনে?"),
            ("Why is mounting the Docker socket into a container equivalent to giving it root on the host?", "Container-এ Docker socket mount করা কেন host-এর root দেওয়ার সমান?"),
        ],
        related=["docker-014", "docker-015"],
        refs=[D_SECURITY, D_NODE_BP, OWASP_DOCKER],
    ),
    # ------------------------------------------------------------------ docker-018
    Q(
        id="docker-018", sub="Health Checks", diff="medium", type="conceptual",
        prio="high", market="both", mins=5,
        tags=["healthcheck", "readiness", "liveness", "compose", "restart"],
        ver="Docker Engine 29 (start-interval needs Engine 25+), Compose v5", vs=True, status="stable",
        q_en=r"""How do Docker health checks work? Write a health check for a Node.js API image, and explain what Docker does (and doesn't do) when a container becomes unhealthy.""",
        q_bn=r"""Docker health check কীভাবে কাজ করে? একটা Node.js API image-এর জন্য health check লেখো, আর ব্যাখ্যা করো container unhealthy হলে Docker কী করে (আর কী করে না)।""",
        a_en=r"""
            A health check is a command Docker runs **inside the container** on a schedule. Exit code `0` means healthy and `1` means unhealthy. The container's status moves from `starting` to `healthy`, or to `unhealthy` after `retries` consecutive failures. You define it with `HEALTHCHECK` in the Dockerfile or `healthcheck:` in Compose. The options are `interval`, `timeout`, `start-period` (failures don't count while the app boots), `start-interval` (faster probing during start) and `retries`.

            **What uses the status:** `docker ps` shows it. Compose's `depends_on: condition: service_healthy` waits for it. Swarm replaces unhealthy tasks, and deploy scripts can gate traffic switching on it.

            **What Docker does not do:** the standalone Docker Engine **doesn't restart an unhealthy container**. Restart policies only react to the process **exiting**. Kubernetes ignores the image's `HEALTHCHECK` entirely and uses its own liveness/readiness probes, and ECS defines health checks in the task definition.
        """,
        a_bn=r"""
            Health check হলো একটা command, যেটা Docker নির্দিষ্ট সময় পরপর **container-এর ভেতরে** চালায়। Exit code `0` মানে healthy, `1` মানে unhealthy। Container-এর status `starting` থেকে `healthy`-তে যায়, অথবা পরপর `retries` বার fail করলে `unhealthy` হয়। এটা Dockerfile-এ `HEALTHCHECK` দিয়ে বা Compose-এ `healthcheck:` দিয়ে define করা হয়। Option-গুলো হলো `interval`, `timeout`, `start-period` (app boot হওয়ার সময়ের failure গোনা হয় না), `start-interval` (start-এর সময় দ্রুত probe করা) আর `retries`।

            **Status-টা কে ব্যবহার করে:** `docker ps` এটা দেখায়। Compose-এর `depends_on: condition: service_healthy` এর জন্য অপেক্ষা করে। Swarm unhealthy task replace করে, আর deploy script traffic switch করার আগে এটা দেখে নিতে পারে।

            **Docker যা করে না:** standalone Docker Engine **unhealthy container restart করে না**। Restart policy শুধু process **exit** করলে প্রতিক্রিয়া দেখায়। Kubernetes image-এর `HEALTHCHECK` পুরোপুরি উপেক্ষা করে নিজের liveness/readiness probe ব্যবহার করে, আর ECS-এ health check define করা হয় task definition-এ।
        """,
        quick_en=r"""A health check is a command Docker runs inside the container on a schedule (exit 0 means healthy), giving a healthy or unhealthy status. Compose's `service_healthy` and deploy scripts use it, but standalone Docker doesn't restart an unhealthy container: restart policies only react to the process exiting.""",
        quick_bn=r"""Health check হলো একটা command, যেটা Docker নির্দিষ্ট সময় পরপর container-এর ভেতরে চালায় (exit 0 মানে healthy), আর তা থেকে status healthy বা unhealthy হয়। Compose-এর `service_healthy` আর deploy script এটা ব্যবহার করে, কিন্তু standalone Docker unhealthy container restart করে না; restart policy শুধু process exit করলে কাজ করে।""",
        ex_en=r"""
            - **Tooling inside the image:** `node:24-alpine` includes BusyBox `wget`, but `node:24-slim` has neither `curl` nor `wget`, and distroless has no shell. A small `node -e "fetch(...)"` check works on any Node image without adding packages.
            - **Liveness vs readiness:** a health endpoint that checks the database can turn a short DB blip into every replica being marked unhealthy, or restarted by an orchestrator. Keep liveness cheap ("is the event loop responsive?") and put dependency checks in readiness.
            - **Defaults:** `interval` 30s, `timeout` 30s, `start-period` 0s, `retries` 3. Tune them so a slow cold start doesn't flap.
            - **Cost:** every check spawns a process. With many containers, a 1-second interval isn't free.
        """,
        ex_bn=r"""
            - **Image-এর ভেতরের tool:** `node:24-alpine`-এ BusyBox `wget` আছে, কিন্তু `node:24-slim`-এ `curl` বা `wget` কোনোটাই নেই, আর distroless-এ shell-ই নেই। ছোট একটা `node -e "fetch(...)"` check কোনো package যোগ না করেই যেকোনো Node image-এ কাজ করে।
            - **Liveness বনাম readiness:** health endpoint database check করলে DB-র সাময়িক সমস্যাতেই সব replica unhealthy হয়ে যেতে পারে, বা orchestrator সবগুলো restart করে দিতে পারে। Liveness হালকা রাখো ("event loop কি সাড়া দিচ্ছে?"), আর dependency check রাখো readiness-এ।
            - **Default মান:** `interval` 30s, `timeout` 30s, `start-period` 0s, `retries` 3। এমনভাবে tune করো যাতে ধীর cold start-এ status বারবার ওঠানামা (flap) না করে।
            - **খরচ:** প্রতিটা check একটা process spawn করে। অনেক container থাকলে 1 সেকেন্ডের interval বিনা খরচে আসে না।
        """,
        tip_en=r"""The detail that "plain Docker doesn't restart unhealthy containers" surprises many candidates. State it clearly, then contrast it with Swarm, Kubernetes probes and ECS.""",
        tip_bn=r""""সাধারণ Docker unhealthy container restart করে না", এই তথ্য অনেক candidate-কে অবাক করে। এটা স্পষ্টভাবে বলো, তারপর Swarm, Kubernetes probe আর ECS-এর সাথে তুলনা করো।""",
        mist_en=r"""Using `curl` in a slim image that doesn't contain it (the check always fails), assuming `restart: always` handles unhealthy containers, and making the health endpoint depend on every downstream service.""",
        mist_bn=r"""যে slim image-এ `curl` নেই সেখানে `curl` দিয়ে check লেখা (check সবসময় fail করে), ধরে নেওয়া যে `restart: always` unhealthy container সামলায়, আর health endpoint-কে সব downstream service-এর উপর নির্ভরশীল করে ফেলা।""",
        code=r"""
            FROM node:24-slim
            WORKDIR /app
            COPY --chown=node:node . .
            USER node
            EXPOSE 3000

            # No curl/wget in slim images, so use Node's built-in fetch
            HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
              CMD node -e "fetch('http://127.0.0.1:3000/healthz').then(r => process.exit(r.ok ? 0 : 1)).catch(() => process.exit(1))"

            CMD ["node", "server.js"]
        """,
        lang="dockerfile",
        extra=[
            dict(lang="bash", label_en="Inspecting health status", label_bn="Health status পরীক্ষা করা", src=r"""
                docker ps                                   # STATUS: Up 2 minutes (healthy)
                docker inspect -f '{{.State.Health.Status}}' api
                docker inspect -f '{{json .State.Health.Log}}' api   # last probe outputs
            """),
        ],
        follow=[
            ("What should a liveness endpoint check versus a readiness endpoint?", "Liveness endpoint আর readiness endpoint আলাদাভাবে কী কী check করবে?"),
            ("How would you make Docker replace unhealthy containers automatically?", "Unhealthy container Docker দিয়ে স্বয়ংক্রিয়ভাবে replace করাতে চাইলে কী করবে?"),
        ],
        related=["docker-016", "docker-015"],
        refs=[D_DOCKERFILE, D_COMPOSE_SERVICES],
    ),
    # ------------------------------------------------------------------ docker-019
    Q(
        id="docker-019", sub="Production Deployment", diff="medium", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["restart-policy", "unless-stopped", "always", "on-failure"],
        ver="Docker Engine 29", vs=False, status="stable",
        q_en=r"""Which statement about Docker restart policies is correct?""",
        q_bn=r"""Docker restart policy সম্পর্কে কোন কথাটা সঠিক?""",
        options=[
            ("With `unless-stopped`, a container you stopped manually stays stopped even after the Docker daemon or host restarts; with `always`, it is started again when the daemon restarts",
             "`unless-stopped` থাকলে হাতে stop করা container Docker daemon বা host restart হওয়ার পরেও বন্ধ থাকে; `always` থাকলে daemon restart হলে আবার start হয়"),
            ("`restart: always` also restarts a container when its HEALTHCHECK reports `unhealthy`",
             "HEALTHCHECK `unhealthy` দেখালে `restart: always` container-টা restart করে দেয়"),
            ("`on-failure` restarts the container after any exit, including exit code 0",
             "`on-failure` যেকোনো exit-এর পরেই container restart করে, exit code 0 হলেও"),
            ("Restart policies only work for containers started with Docker Compose",
             "Restart policy শুধু Docker Compose দিয়ে চালানো container-এ কাজ করে"),
        ],
        correct=0,
        a_en=r"""The `unless-stopped` answer is correct. Both `always` and `unless-stopped` restart a container whenever it exits. The difference shows up after a **manual stop**: on the next daemon start (e.g. after a server reboot), `always` brings the container back, while `unless-stopped` respects that you stopped it. `on-failure[:N]` restarts only on a non-zero exit code, optionally at most N times.""",
        a_bn=r"""`unless-stopped`-এর উত্তরটাই সঠিক। `always` আর `unless-stopped` দুটোই container exit করলেই restart করে। পার্থক্য দেখা যায় **হাতে stop করার** পরে: পরের বার daemon start হলে (যেমন server reboot-এর পরে) `always` container-টা আবার চালু করে, কিন্তু `unless-stopped` তোমার stop করার সিদ্ধান্ত মেনে নেয়। `on-failure[:N]` শুধু non-zero exit code-এ restart করে, চাইলে সর্বোচ্চ N বার।""",
        quick_en=r"""With `unless-stopped`, a container you stopped manually stays stopped after a daemon or host restart, while `always` brings it back. Both restart on any exit; `on-failure` restarts only on a non-zero exit code.""",
        quick_bn=r"""`unless-stopped`-এ হাতে stop করা container daemon বা host restart-এর পরেও বন্ধ থাকে, কিন্তু `always` সেটা আবার চালু করে। দুটোই যেকোনো exit-এ restart করে; `on-failure` শুধু non-zero exit code-এ restart করে।""",
        ex_en=r"""
            The tempting wrong answer is the claim that `restart: always` reacts to `unhealthy`. Restart policies react only to the main process **exiting**; health status doesn't trigger them. Replacing unhealthy containers is an orchestrator feature (Swarm, Kubernetes, ECS).

            Other details:
            - A restart policy only takes effect after the container has stayed up for at least 10 seconds, which prevents tight restart loops on boot failures. Docker also backs off exponentially between restarts.
            - The policy works with plain `docker run --restart unless-stopped`. Compose just sets the same container property.
            - For a single-VPS deployment, `unless-stopped` is the usual choice. A deliberate `docker stop` during maintenance won't be undone by a reboot.
        """,
        ex_bn=r"""
            বিভ্রান্তিকর ভুল উত্তর হলো এই দাবি যে `restart: always` `unhealthy`-তে সাড়া দেয়। Restart policy শুধু main process **exit** করলে কাজ করে; health status দিয়ে এটা trigger হয় না। Unhealthy container replace করা orchestrator-এর feature (Swarm, Kubernetes, ECS)।

            অন্যান্য detail:
            - Container কমপক্ষে ১০ সেকেন্ড চালু থাকার পরেই restart policy কার্যকর হয়। এতে boot failure-এর সময় দ্রুত বারবার restart-এর loop হয় না। Docker restart-গুলোর মাঝে exponential back-off-ও করে।
            - Policy সাধারণ `docker run --restart unless-stopped`-এই কাজ করে। Compose শুধু container-এর একই property set করে।
            - একটা VPS-এ deploy করলে সাধারণত `unless-stopped` বেছে নেওয়া হয়। Maintenance-এর সময় ইচ্ছা করে করা `docker stop` reboot-এ উল্টে যায় না।
        """,
        tip_en=r"""Explain the difference with the reboot scenario. It's concrete, and it's exactly the situation where the two policies behave differently.""",
        tip_bn=r"""Reboot-এর উদাহরণ দিয়ে পার্থক্যটা ব্যাখ্যা করো। এটা বাস্তবসম্মত, আর ঠিক এই পরিস্থিতিতেই দুটো policy আলাদা আচরণ করে।""",
        related=["docker-018"],
        refs=[D_RESTART],
    ),
    # ------------------------------------------------------------------ docker-025
    Q(
        id="docker-025", sub="Networks and DNS", diff="hard", type="conceptual",
        prio="medium", market="both", mins=8,
        tags=["bridge", "user-defined-network", "embedded-dns", "host-network", "network-isolation"],
        ver="Docker Engine 29, Compose v5", vs=False, status="stable",
        q_en=r"""Explain how containers on a user-defined bridge network find and talk to each other. How does that differ from the default bridge network and from host networking, and how would you isolate a database so only the API can reach it?""",
        q_bn=r"""User-defined bridge network-এ container-রা কীভাবে একে অপরকে খুঁজে পায় আর কথা বলে, ব্যাখ্যা করো। এটা default bridge network আর host networking থেকে কীভাবে আলাদা? আর database-কে কীভাবে isolate করবে যাতে শুধু API সেখানে পৌঁছাতে পারে?""",
        a_en=r"""
            **User-defined bridge** (what Compose creates per project): each container gets its own network namespace with a virtual interface attached to a Linux bridge, and an IP on that network's subnet. Docker runs an **embedded DNS server** (reachable at `127.0.0.11` inside containers) that resolves container names, Compose service names and aliases to current IPs. When a service is scaled to several replicas, its name resolves to multiple addresses. Containers on different user-defined networks can't talk unless a container is attached to both.

            **Default bridge (`docker0`):** containers started without `--network` land here. There's **no name-based DNS** (only the legacy `--link`), and every container on it can reach every other one, so it's weaker isolation. Avoid it for multi-container apps.

            **Host network:** the container shares the host's network stack. There's no NAT, `-p` is ignored, and ports bind directly on the host. It's useful for very high packet rates or tools that must see host interfaces, but you lose isolation and can get port conflicts. It's mainly a Linux feature.

            **Isolating the DB:** put services on segmented networks. NGINX and the API go on `frontend`; the API and Postgres go on `backend`, marked `internal: true` (no outbound internet access, no published ports). Postgres never publishes a host port, so the only path to it is through the API container.
        """,
        a_bn=r"""
            **User-defined bridge** (Compose প্রতিটা project-এর জন্য এটাই তৈরি করে): প্রতিটা container নিজস্ব network namespace পায়, যার virtual interface একটা Linux bridge-এর সাথে যুক্ত, আর ওই network-এর subnet থেকে একটা IP পায়। Docker একটা **embedded DNS server** চালায় (container-এর ভেতর থেকে `127.0.0.11`-এ পাওয়া যায়), যেটা container name, Compose service name আর alias-কে বর্তমান IP-তে resolve করে। কোনো service-এর একাধিক replica চালালে নামটা একাধিক address-এ resolve হয়। আলাদা user-defined network-এর container-রা নিজেদের মধ্যে কথা বলতে পারে না, যদি না কোনো container দুটো network-এই যুক্ত থাকে।

            **Default bridge (`docker0`):** `--network` ছাড়া চালানো container এখানে যায়। এখানে **নাম দিয়ে DNS resolution নেই** (শুধু legacy `--link`), আর এর সব container একে অপরের কাছে পৌঁছাতে পারে, তাই isolation দুর্বল। Multi-container app-এ এটা এড়িয়ে চলো।

            **Host network:** container host-এর network stack share করে। কোনো NAT নেই, `-p` উপেক্ষা করা হয়, port সরাসরি host-এ bind হয়। খুব বেশি packet rate বা host interface দেখতে হয় এমন tool-এর জন্য কাজের, কিন্তু isolation হারাতে হয় আর port conflict হতে পারে। এটা মূলত Linux-এর feature।

            **DB isolate করা:** service-গুলোকে আলাদা network-এ ভাগ করো। NGINX আর API থাকবে `frontend`-এ; API আর Postgres থাকবে `backend`-এ, যেটা `internal: true` (outbound internet নেই, publish করা port নেই)। Postgres কোনো host port publish করবে না, ফলে এর কাছে পৌঁছানোর একমাত্র পথ API container।
        """,
        quick_en=r"""On a user-defined bridge, Docker's embedded DNS (`127.0.0.11`) resolves container and service names; the default bridge has no name-based DNS, and host networking shares the host's stack with no isolation. To isolate a database, attach it only to an `internal: true` network shared with the API and publish no port.""",
        quick_bn=r"""User-defined bridge-এ Docker-এর embedded DNS (`127.0.0.11`) container আর service name resolve করে; default bridge-এ name দিয়ে DNS নেই, আর host networking host-এর network stack share করে, কোনো isolation থাকে না। Database isolate করতে সেটাকে শুধু API-র সাথে share করা একটা `internal: true` network-এ রাখো, কোনো port publish কোরো না।""",
        ex_en=r"""
            - **DNS caching pitfalls:** some clients resolve a hostname once and cache the IP forever (NGINX does this for static `proxy_pass` hosts). When a container is recreated with a new IP, they keep calling the old one. Re-resolve, or use the service's DNS-aware options.
            - **Firewalls:** Docker programs iptables/nftables NAT rules for published ports. Those rules sit in front of ufw's rules, so ufw doesn't protect published ports. Filter in the `DOCKER-USER` chain or bind ports to `127.0.0.1`.
            - **Multi-host:** bridge networks are single-host. Swarm's overlay networks or Kubernetes CNI plugins span hosts.
            - **Docker Desktop specifics:** on macOS/Windows, containers run inside a VM, so "host" means the VM. Use `host.docker.internal` to reach services on your laptop.
        """,
        ex_bn=r"""
            - **DNS caching-এর ফাঁদ:** কিছু client একবার hostname resolve করে IP চিরদিনের জন্য cache করে রাখে (static `proxy_pass` host-এর ক্ষেত্রে NGINX এটাই করে)। নতুন IP নিয়ে container recreate হলে তারা পুরনো IP-তেই call করতে থাকে। আবার resolve করো, অথবা service-এর DNS-সচেতন option ব্যবহার করো।
            - **Firewall:** publish করা port-এর জন্য Docker iptables/nftables-এ NAT rule বসায়। এই rule-গুলো ufw-এর rule-এর আগেই কাজ করে, তাই ufw publish করা port রক্ষা করে না। `DOCKER-USER` chain-এ filter করো, অথবা port `127.0.0.1`-এ bind করো।
            - **Multi-host:** bridge network শুধু এক host-এর মধ্যে কাজ করে। একাধিক host জুড়ে চলে Swarm-এর overlay network বা Kubernetes-এর CNI plugin।
            - **Docker Desktop-এর বিশেষত্ব:** macOS/Windows-এ container চলে একটা VM-এর ভেতরে, তাই "host" মানে ওই VM। Laptop-এর service-এ পৌঁছাতে `host.docker.internal` ব্যবহার করো।
        """,
        tip_en=r"""Draw it while you talk: two networks, three boxes, NGINX bridging the edge and the API bridging both. Mentioning `127.0.0.11` and the ufw bypass shows hands-on depth beyond "containers can talk by name".""",
        tip_bn=r"""বলতে বলতে একটা ছবি আঁকো: দুটো network, তিনটা box, edge-এ NGINX আর দুই network-এর মাঝে API। `127.0.0.11` আর ufw bypass-এর কথা বললে বোঝা যায় তোমার জ্ঞান "container নাম দিয়ে কথা বলে"-এর চেয়ে গভীর, হাতে-কলমে।""",
        mist_en=r"""Assuming the default bridge resolves container names, publishing database ports "just for debugging" on a server, and hard-coding container IPs.""",
        mist_bn=r"""ধরে নেওয়া যে default bridge container name resolve করে, server-এ "শুধু debugging-এর জন্য" database port publish করা, আর container-এর IP hard-code করা।""",
        code=r"""
            services:
              nginx:
                image: nginx:1.30-alpine
                ports: ["80:80", "443:443"]
                networks: [frontend]

              api:
                build: .
                networks: [frontend, backend]   # the only bridge between the two

              db:
                image: postgres:18-alpine
                networks: [backend]              # no ports: published

            networks:
              frontend: {}
              backend:
                internal: true                   # no outbound internet, no published ports
        """,
        lang="yaml",
        extra=[
            dict(lang="bash", label_en="Inspecting networks and DNS", label_bn="Network আর DNS পরীক্ষা করা", src=r"""
                docker network ls
                docker network inspect myproj_backend --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'
                docker compose exec api cat /etc/resolv.conf     # nameserver 127.0.0.11
                docker compose exec api getent hosts db
            """),
        ],
        follow=[
            ("Why might NGINX keep sending traffic to an old container IP after a redeploy?", "Redeploy-এর পরেও NGINX কেন পুরনো container IP-তে traffic পাঠাতে পারে?"),
            ("How would you restrict which external IPs can reach a published port?", "Publish করা port-এ কোন কোন external IP পৌঁছাতে পারবে, সেটা কীভাবে সীমিত করবে?"),
        ],
        related=["docker-010", "docker-005"],
        refs=[D_BRIDGE, D_HOST_NET, D_FIREWALL],
    ),
    # ------------------------------------------------------------------ docker-026
    Q(
        id="docker-026", sub="Layers and Caching", diff="hard", type="mcq",
        prio="medium", market="both", mins=3,
        tags=["buildkit", "cache-mount", "build-cache", "ci"],
        ver="Docker Engine 29 / BuildKit (Dockerfile syntax 1.x)", vs=True, status="stable",
        q_en=r"""In `RUN --mount=type=cache,target=/root/.npm npm ci`, which statement about the cache mount is correct?""",
        q_bn=r"""`RUN --mount=type=cache,target=/root/.npm npm ci`-এ cache mount সম্পর্কে কোন কথাটা সঠিক?""",
        options=[
            ("The contents of `/root/.npm` are committed into the image layer, making the image larger but `docker pull` faster",
             "`/root/.npm`-এর content image layer-এ commit হয়, ফলে image বড় হয় কিন্তু `docker pull` দ্রুত হয়"),
            ("The cache directory persists between builds on the same builder and is never included in the image; it speeds up `npm ci` even when the layer itself must be rebuilt",
             "Cache directory একই builder-এ এক build থেকে আরেক build-এ থেকে যায় আর কখনো image-এ ঢোকে না; layer নিজে আবার build করতে হলেও এটা `npm ci` দ্রুত করে"),
            ("Because of the cache mount, `npm ci` is skipped on every later build, even when `package-lock.json` changes",
             "Cache mount-এর কারণে পরের প্রতিটা build-এ `npm ci` skip হয়, `package-lock.json` বদলালেও"),
            ("Exporting build cache with `--cache-to type=registry,mode=max` also uploads the cache mount's contents, so every CI runner shares it automatically",
             "`--cache-to type=registry,mode=max` দিয়ে build cache export করলে cache mount-এর content-ও upload হয়, তাই সব CI runner স্বয়ংক্রিয়ভাবে এটা share করে"),
        ],
        correct=1,
        a_en=r"""The "persists between builds, never in the image" answer is correct. A cache mount is a persistent directory managed by the builder and mounted only while that `RUN` executes. It isn't part of the layer, so it adds nothing to the image. Its value shows up exactly when the **layer cache misses** (e.g. the lockfile changed): npm re-runs, but it finds most packages already downloaded in `/root/.npm`.""",
        a_bn=r""""Build-এর মধ্যে থেকে যায়, কখনো image-এ ঢোকে না" উত্তরটাই সঠিক। Cache mount হলো builder-এর manage করা একটা স্থায়ী directory, যেটা শুধু ওই `RUN` চলার সময় mount থাকে। এটা layer-এর অংশ না, তাই image-এ কিছুই যোগ করে না। এর আসল সুবিধা দেখা যায় ঠিক তখন, যখন **layer cache miss হয়** (যেমন lockfile বদলেছে): npm আবার চলে, কিন্তু বেশিরভাগ package `/root/.npm`-এ আগে থেকেই download করা পায়।""",
        quick_en=r"""The cache mount persists between builds on the same builder and is never part of the image. It pays off when the layer cache misses (the lockfile changed): `npm ci` still runs, but it reuses packages already downloaded into `/root/.npm`.""",
        quick_bn=r"""Cache mount একই builder-এ এক build থেকে আরেক build-এ থেকে যায়, কিন্তু কখনো image-এর অংশ হয় না। Layer cache miss করলে (lockfile বদলালে) এর লাভ বোঝা যায়: `npm ci` আবার চলে, কিন্তু `/root/.npm`-এ আগে download হওয়া package reuse করে।""",
        ex_en=r"""
            The tempting wrong answer is the one about `--cache-to … mode=max` uploading the mount. `--cache-to`/`--cache-from` export **layer** cache (the results of instructions), not the contents of cache mounts. Cache mounts live on the builder instance, so a fresh ephemeral CI runner starts with an empty one. You either use a persistent builder, accept the cold cache, or use CI-specific workarounds that save and restore the mount directory.

            Two separate cache layers are at work:
            - **Layer cache:** skips the whole `RUN` when its inputs are unchanged.
            - **Cache mount:** makes the `RUN` cheaper when it does have to run.

            Options include `id=` (share one cache between Dockerfiles), `sharing=locked` (serialise access, e.g. for `apt`), and `uid`/`gid` for non-root build steps.
        """,
        ex_bn=r"""
            বিভ্রান্তিকর ভুল উত্তর হলো `--cache-to … mode=max` দিয়ে mount upload হওয়ার কথাটা। `--cache-to`/`--cache-from` **layer** cache (instruction-এর ফলাফল) export করে, cache mount-এর content না। Cache mount থাকে builder instance-এর মধ্যে, তাই নতুন ephemeral CI runner খালি cache নিয়ে শুরু করে। সমাধান হলো persistent builder ব্যবহার করা, cold cache মেনে নেওয়া, অথবা CI-নির্দিষ্ট workaround দিয়ে mount directory save ও restore করা।

            এখানে দুটো আলাদা cache কাজ করছে:
            - **Layer cache:** input না বদলালে পুরো `RUN` skip করে।
            - **Cache mount:** `RUN` চালাতেই হলে সেটাকে সস্তা করে।

            কিছু option: `id=` (একাধিক Dockerfile-এর মধ্যে একটা cache share করা), `sharing=locked` (access এক এক করে দেওয়া, যেমন `apt`-এর জন্য), আর non-root build step-এর জন্য `uid`/`gid`।
        """,
        tip_en=r"""Contrast "layer cache" and "cache mount" in one sentence each. Interviewers use this question to see whether you understand **why** builds are slow on CI.""",
        tip_bn=r""""Layer cache" আর "cache mount"-এর পার্থক্য প্রতিটা এক বাক্যে বলো। CI-তে build **কেন** ধীর সেটা তুমি বোঝো কি না, interviewer এই প্রশ্ন দিয়ে সেটাই দেখে।""",
        related=["docker-012", "docker-030"],
        refs=[D_CACHE_OPT, D_CACHE],
    ),
]

if __name__ == "__main__":
    save("docker", "b3", QUESTIONS)
