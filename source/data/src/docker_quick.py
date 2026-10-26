# Docker — quick-recall questions: docker-q01..q10 (see docs/AUTHORING.md §8a)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

D_OVERVIEW = ("Docker Docs — What is Docker?", "https://docs.docker.com/get-started/docker-overview/")
D_CONTAINER = ("Docker Docs — What is a container?", "https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/")
D_IMAGE = ("Docker Docs — What is an image?", "https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/")
D_DOCKERFILE = ("Dockerfile reference", "https://docs.docker.com/reference/dockerfile/")
D_VOLUMES = ("Docker Docs — Volumes", "https://docs.docker.com/engine/storage/volumes/")
D_NETWORK = ("Docker Docs — Networking overview", "https://docs.docker.com/engine/network/")
D_COMPOSE = ("Docker Docs — Docker Compose", "https://docs.docker.com/compose/")
D_EXEC = ("Docker CLI — docker container exec", "https://docs.docker.com/reference/cli/docker/container/exec/")
D_CONTEXT = ("Docker Docs — Build context (.dockerignore)", "https://docs.docker.com/build/concepts/context/")

QUESTIONS = [
    # ------------------------------------------------------------------ docker-q01
    Q(
        id="docker-q01", sub="Images and Containers", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["docker", "containers", "basics"],
        ver="Version-independent concept (Docker Engine 29)", vs=False, status="stable",
        q_en=r"""What is Docker, and what problem does it solve?""",
        q_bn=r"""Docker কী, আর এটা কোন সমস্যার সমাধান করে?""",
        a_en=r"""Docker is a platform for packaging an app together with its runtime, libraries and config into an **image**, and running that image as an isolated **container**. The same image runs the same way on a laptop, CI and a server, which removes most "works on my machine" problems.""",
        a_bn=r"""Docker হলো এমন একটা platform, যেটা app-কে তার runtime, library আর config-সহ একটা **image**-এ package করে, আর সেই image-কে isolated **container** হিসেবে চালায়। একই image laptop, CI আর server-এ একইভাবে চলে, তাই "আমার machine-এ তো চলে" ধরনের সমস্যা প্রায় চলে যায়।""",
        code=r"""
            docker run -d -p 8080:80 nginx:1.30-alpine   # pull (if needed) + create + start
            docker ps                                    # list running containers
        """, lang="bash",
        ex_en=r"""A container is not a VM: it's a normal Linux process isolated by the host kernel, so it starts in seconds or less and doesn't boot its own OS.""",
        ex_bn=r"""Container কোনো VM না: এটা host kernel দিয়ে isolate করা একটা সাধারণ Linux process, তাই নিজের OS boot না করেই খুব দ্রুত start হয়।""",
        tip_en=r"""Say "package once as an image, run it anywhere as a container", then give the "works on my machine" example.""",
        tip_bn=r"""বলো "একবার image হিসেবে package করো, যেকোনো জায়গায় container হিসেবে চালাও", তারপর "আমার machine-এ চলে" উদাহরণটা দাও।""",
        follow=[("How is a container different from a virtual machine?", "Container আর virtual machine-এর পার্থক্য কী?")],
        related=["docker-001", "docker-002"],
        refs=[D_OVERVIEW],
    ),
    # ------------------------------------------------------------------ docker-q02
    Q(
        id="docker-q02", sub="Images and Containers", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["dockerfile", "image", "container", "build", "run"],
        ver="Version-independent concept (Docker Engine 29)", vs=False, status="stable",
        q_en=r"""How are a Dockerfile, an image and a container related?""",
        q_bn=r"""Dockerfile, image আর container-এর মধ্যে সম্পর্ক কী?""",
        a_en=r"""A **Dockerfile** is the recipe, `docker build` turns it into a read-only **image**, and `docker run` starts a **container** from that image. You can run many containers from one image, like many objects from one class.""",
        a_bn=r"""**Dockerfile** হলো recipe, `docker build` সেটা থেকে একটা read-only **image** বানায়, আর `docker run` সেই image থেকে একটা **container** চালায়। একটা image থেকে অনেকগুলো container চালানো যায়, যেমন একটা class থেকে অনেক object।""",
        code=r"""
            docker build -t myapp:1.0 .          # Dockerfile -> image
            docker run -d --name app1 myapp:1.0  # image -> container
            docker run -d --name app2 myapp:1.0  # a second container, same image
            docker images                        # images (templates)
            docker ps -a                         # containers (instances)
        """, lang="bash",
        ex_en=r"""Each container gets its own thin writable layer on top of the image; the image itself never changes, and that layer is deleted with `docker rm`.""",
        ex_bn=r"""প্রতিটা container image-এর উপর নিজস্ব একটা পাতলা writable layer পায়; image নিজে কখনো বদলায় না, আর `docker rm` করলে ওই layer মুছে যায়।""",
        tip_en=r"""Walk the chain out loud: "Dockerfile → build → image → run → container".""",
        tip_bn=r"""ধাপগুলো মুখে বলো: "Dockerfile → build → image → run → container"।""",
        follow=[("What happens to data written inside a container when you remove it?", "Container remove করলে তার ভেতরে লেখা data-র কী হয়?")],
        related=["docker-002"],
        refs=[D_IMAGE],
    ),
    # ------------------------------------------------------------------ docker-q03
    Q(
        id="docker-q03", sub="Containers vs VMs", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["containers", "virtual-machines", "kernel"],
        ver="Version-independent concept (Docker Engine 29)", vs=False, status="stable",
        q_en=r"""Why does a container start much faster and use less memory than a virtual machine?""",
        q_bn=r"""Virtual machine-এর চেয়ে container কেন অনেক দ্রুত start হয় আর কম memory নেয়?""",
        a_en=r"""A VM boots a full guest operating system with its own kernel on virtual hardware. A container shares the host's kernel and is just an isolated process, so there's no OS to boot; the trade-off is weaker isolation than a VM.""",
        a_bn=r"""VM virtual hardware-এর উপর নিজস্ব kernel-সহ পুরো একটা guest operating system boot করে। Container host-এর kernel share করে, এটা শুধু একটা isolated process, তাই কোনো OS boot করতে হয় না; বিনিময়ে isolation VM-এর চেয়ে দুর্বল।""",
        ex_en=r"""Because the kernel is shared, a Linux container needs a Linux kernel; Docker Desktop on macOS and Windows runs a small Linux VM for that.""",
        ex_bn=r"""Kernel share হয় বলে Linux container-এর Linux kernel লাগে; তাই macOS আর Windows-এ Docker Desktop একটা ছোট Linux VM চালায়।""",
        tip_en=r"""Use the one-liner "VMs virtualise hardware, containers virtualise the OS", then name the trade-off.""",
        tip_bn=r"""এক লাইনে বলো "VM hardware virtualize করে, container OS virtualize করে", তারপর trade-off-টা বলো।""",
        follow=[("Which Linux features does Docker use to isolate a container?", "Container isolate করতে Docker Linux-এর কোন feature ব্যবহার করে?")],
        related=["docker-001"],
        refs=[D_CONTAINER],
    ),
    # ------------------------------------------------------------------ docker-q04
    Q(
        id="docker-q04", sub="Dockerfiles", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["dockerfile", "from", "run", "cmd", "workdir"],
        ver="Dockerfile syntax 1.x (Docker Engine 29), Node.js 24/26 LTS", vs=False, status="stable",
        q_en=r"""What do `FROM`, `WORKDIR`, `COPY`, `RUN` and `CMD` do in a Dockerfile?""",
        q_bn=r"""Dockerfile-এ `FROM`, `WORKDIR`, `COPY`, `RUN` আর `CMD` কী কাজ করে?""",
        a_en=r"""`FROM` picks the base image, `WORKDIR` sets the working directory and `COPY` copies files from the build context. `RUN` executes a command **at build time** and saves the result as a layer, while `CMD` is the default command run **when a container starts**.""",
        a_bn=r"""`FROM` base image ঠিক করে, `WORKDIR` working directory set করে, আর `COPY` build context থেকে file copy করে। `RUN` **build-এর সময়** command চালিয়ে ফলাফল একটা layer হিসেবে রাখে, আর `CMD` হলো **container start হওয়ার সময়** চলা default command।""",
        code=r"""
            FROM node:24-alpine
            WORKDIR /app
            COPY package.json package-lock.json ./
            RUN npm ci --omit=dev          # runs once, during docker build
            COPY . .
            CMD ["node", "server.js"]      # runs every time a container starts
        """, lang="dockerfile",
        ex_en=r"""Only the last `CMD` counts, and it can be overridden with `docker run myapp <command>`. Write it in exec form (JSON array) so Node is PID 1 and receives SIGTERM.""",
        ex_bn=r"""শুধু শেষ `CMD`-টাই কাজ করে, আর `docker run myapp <command>` দিয়ে override করা যায়। এটা exec form (JSON array)-এ লেখো, যাতে Node PID 1 হয় আর SIGTERM পায়।""",
        tip_en=r"""Stress the build-time vs start-time difference between `RUN` and `CMD`; that's what the question is really testing.""",
        tip_bn=r"""`RUN` আর `CMD`-এর build-time বনাম start-time পার্থক্যটা জোর দিয়ে বলো; প্রশ্নটা আসলে এটাই যাচাই করে।""",
        follow=[("Why copy `package.json` before the rest of the source?", "বাকি source-এর আগে `package.json` কেন copy করা হয়?")],
        related=["docker-012", "docker-013"],
        refs=[D_DOCKERFILE],
    ),
    # ------------------------------------------------------------------ docker-q05
    Q(
        id="docker-q05", sub="Dockerfiles", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["cmd", "entrypoint", "dockerfile"],
        ver="Dockerfile syntax 1.x (Docker Engine 29)", vs=False, status="stable",
        q_en=r"""What is the difference between `CMD` and `ENTRYPOINT`?""",
        q_bn=r"""`CMD` আর `ENTRYPOINT`-এর পার্থক্য কী?""",
        a_en=r"""`ENTRYPOINT` is the fixed executable the container always runs, and `CMD` gives default arguments (or the whole default command when there's no entrypoint). Arguments after the image name in `docker run` replace `CMD`; replacing the entrypoint needs `--entrypoint`.""",
        a_bn=r"""`ENTRYPOINT` হলো নির্দিষ্ট executable, যেটা container সবসময় চালায়; আর `CMD` default argument দেয় (entrypoint না থাকলে পুরো default command)। `docker run`-এ image name-এর পরের argument `CMD`-কে replace করে; entrypoint বদলাতে `--entrypoint` লাগে।""",
        code=r"""
            # Dockerfile: ENTRYPOINT ["node"]  +  CMD ["server.js"]
            docker run myapp               # → node server.js
            docker run myapp worker.js     # → node worker.js
        """, lang="bash",
        ex_en=r"""Use exec form for both. With shell-form `ENTRYPOINT`, `CMD` and run arguments are ignored and `/bin/sh` becomes PID 1.""",
        ex_bn=r"""দুটোই exec form-এ লেখো। Shell-form `ENTRYPOINT` দিলে `CMD` আর run argument ignore হয়, আর `/bin/sh` PID 1 হয়ে যায়।""",
        tip_en=r"""Say "ENTRYPOINT is the verb, CMD is the default object" and show the two `docker run` lines.""",
        tip_bn=r"""বলো "ENTRYPOINT হলো verb, CMD হলো default object", তারপর দুটো `docker run` line দেখাও।""",
        follow=[("Why is exec form preferred over shell form?", "Shell form-এর বদলে exec form কেন ভালো?")],
        related=["docker-013", "docker-014"],
        refs=[D_DOCKERFILE],
    ),
    # ------------------------------------------------------------------ docker-q06
    Q(
        id="docker-q06", sub="Volumes and Bind Mounts", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["volumes", "bind-mounts", "persistence"],
        ver="Version-independent concept (Docker Engine 29)", vs=False, status="stable",
        q_en=r"""How do you keep a database's data when its container is removed? Volume or bind mount?""",
        q_bn=r"""Container remove করলেও database-এর data কীভাবে রাখবে? Volume না bind mount?""",
        a_en=r"""Mount a **named volume** on the data directory: Docker manages it and it survives `docker rm` and `docker compose down`. A **bind mount** maps a specific host folder instead, which is handy for live-editing source code in development.""",
        a_bn=r"""Data directory-তে একটা **named volume** mount করো: এটা Docker manage করে, আর `docker rm` বা `docker compose down`-এর পরেও থেকে যায়। **Bind mount** এর বদলে host-এর একটা নির্দিষ্ট folder map করে, যেটা development-এ source code live edit করার জন্য সুবিধাজনক।""",
        code=r"""
            # named volume (managed by Docker)
            docker run -d -v pgdata:/var/lib/postgresql -e POSTGRES_PASSWORD=dev postgres:18
            # bind mount (a host folder)
            docker run -d -v "$(pwd)/src:/app/src" myapp:dev
        """, lang="bash",
        ex_en=r"""`docker compose down -v` deletes named volumes too, so don't add `-v` unless you mean to wipe the data.""",
        ex_bn=r"""`docker compose down -v` named volume-ও মুছে দেয়, তাই data মুছতে না চাইলে `-v` দিও না।""",
        tip_en=r"""Answer "volume for data, bind mount for dev code" and mention that data in the container's own layer dies with it.""",
        tip_bn=r"""উত্তর দাও "data-র জন্য volume, dev code-এর জন্য bind mount", আর বলো যে container-এর নিজের layer-এর data container-এর সাথেই মুছে যায়।""",
        follow=[("What is a tmpfs mount used for?", "tmpfs mount কী কাজে লাগে?")],
        related=["docker-006", "docker-020"],
        refs=[D_VOLUMES],
    ),
    # ------------------------------------------------------------------ docker-q07
    Q(
        id="docker-q07", sub="Port Mapping", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["ports", "publish", "networking"],
        ver="Version-independent concept (Docker Engine 29)", vs=False, status="stable",
        q_en=r"""What does `-p 8080:3000` mean in `docker run`?""",
        q_bn=r"""`docker run`-এ `-p 8080:3000` মানে কী?""",
        a_en=r"""It publishes the container's port 3000 on the host's port 8080, in `host:container` order, so `http://localhost:8080` reaches the app. Without `-p`, the app isn't reachable from the host, and the app inside must listen on `0.0.0.0`, not `127.0.0.1`.""",
        a_bn=r"""এটা container-এর port 3000-কে host-এর port 8080-এ publish করে (`host:container` ক্রমে), তাই `http://localhost:8080` দিয়ে app-এ পৌঁছানো যায়। `-p` ছাড়া host থেকে app-এ পৌঁছানো যায় না, আর ভেতরের app-কে `127.0.0.1` না, `0.0.0.0`-এ listen করতে হবে।""",
        code=r"""
            docker run -d -p 8080:3000 myapp             # public on all host interfaces
            docker run -d -p 127.0.0.1:8080:3000 myapp   # only reachable from the host itself
        """, lang="bash",
        ex_en=r"""`EXPOSE` in a Dockerfile publishes nothing; it's only documentation. Containers on the same network talk directly on the container port, no `-p` needed.""",
        ex_bn=r"""Dockerfile-এর `EXPOSE` কিছুই publish করে না, এটা শুধু documentation। একই network-এর container-রা `-p` ছাড়াই সরাসরি container port-এ কথা বলে।""",
        tip_en=r"""Say "host first, container second" and mention binding to `127.0.0.1` when NGINX sits in front.""",
        tip_bn=r"""বলো "আগে host, পরে container", আর সামনে NGINX থাকলে `127.0.0.1`-এ bind করার কথা উল্লেখ করো।""",
        follow=[("Does `EXPOSE` publish a port?", "`EXPOSE` কি port publish করে?")],
        related=["docker-004", "docker-005"],
        refs=[D_NETWORK],
    ),
    # ------------------------------------------------------------------ docker-q08
    Q(
        id="docker-q08", sub="Docker Compose", diff="easy", type="quick",
        prio="high", market="both", mins=2,
        tags=["compose", "multi-container", "cli"],
        ver="Docker Compose v5 (Compose Specification)", vs=True, status="stable",
        q_en=r"""What is Docker Compose, and which commands do you use every day?""",
        q_bn=r"""Docker Compose কী, আর প্রতিদিন কোন command-গুলো ব্যবহার করো?""",
        a_en=r"""Compose describes a multi-container app (API, database, cache) in one `compose.yaml`, with the services sharing a network where they reach each other by service name. `docker compose up -d` starts everything, `ps` and `logs -f` show status and logs, and `down` stops and removes the containers.""",
        a_bn=r"""Compose একটা `compose.yaml` file-এ multi-container app (API, database, cache) বর্ণনা করে; service-গুলো একটা network share করে, আর service name দিয়ে একে অপরকে খুঁজে পায়। `docker compose up -d` সব চালু করে, `ps` আর `logs -f` status ও log দেখায়, আর `down` container-গুলো বন্ধ করে মুছে দেয়।""",
        code=r"""
            # compose.yaml
            services:
              api:
                build: .
                ports: ["3000:3000"]
                environment:
                  DATABASE_URL: postgres://app:dev@db:5432/app
              db:
                image: postgres:18
                environment:
                  POSTGRES_PASSWORD: dev
        """, lang="yaml",
        ex_en=r"""Use `docker compose` (the CLI plugin); the old Python `docker-compose` v1 is end-of-life, and the top-level `version:` key is obsolete.""",
        ex_bn=r"""`docker compose` (CLI plugin) ব্যবহার করো; পুরনো Python `docker-compose` v1 end-of-life, আর top-level `version:` key এখন obsolete।""",
        tip_en=r"""Mention that services find each other by name (`db:5432`), not `localhost`; that's the follow-up interviewers usually probe.""",
        tip_bn=r"""উল্লেখ করো যে service-রা `localhost` না, নাম দিয়ে (`db:5432`) একে অপরকে খুঁজে পায়; interviewer সাধারণত এটাই পরের প্রশ্নে ধরে।""",
        follow=[("Does `depends_on` wait until the database is ready?", "`depends_on` কি database ready হওয়া পর্যন্ত অপেক্ষা করে?")],
        related=["docker-009", "docker-010", "docker-016"],
        refs=[D_COMPOSE],
    ),
    # ------------------------------------------------------------------ docker-q09
    Q(
        id="docker-q09", sub="Container Debugging", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["debugging", "exec", "logs", "inspect"],
        ver="Docker Engine 29 CLI", vs=False, status="stable",
        q_en=r"""A container misbehaves. Which basic Docker commands do you use to debug it?""",
        q_bn=r"""একটা container ঠিকমতো চলছে না। Debug করতে কোন basic Docker command-গুলো ব্যবহার করবে?""",
        a_en=r"""Start with `docker ps -a` for status and exit code, then `docker logs` for the app's output. `docker exec -it <name> sh` opens a shell inside a running container, and `docker inspect` shows its config, IP, mounts and state (exit code, `OOMKilled`).""",
        a_bn=r"""শুরু করো `docker ps -a` দিয়ে status আর exit code দেখতে, তারপর `docker logs` দিয়ে app-এর output। `docker exec -it <name> sh` চলমান container-এর ভেতরে shell খোলে, আর `docker inspect` তার config, IP, mount আর state (exit code, `OOMKilled`) দেখায়।""",
        code=r"""
            docker ps -a                                   # status, exit code
            docker logs --tail 100 -f api                  # app output (stdout/stderr)
            docker exec -it api sh                         # shell inside (if the image has one)
            docker inspect -f '{{.State.ExitCode}} {{.State.OOMKilled}}' api
            docker cp api:/app/config.json ./config.json   # copy a file out
            docker stats                                   # live CPU/memory usage
        """, lang="bash",
        ex_en=r"""`exec` works only on a running container and needs a shell in the image (distroless has none). For a container that keeps crashing, rely on `logs` and `inspect`. With Compose, use `docker compose logs api` and `docker compose exec api sh`.""",
        ex_bn=r"""`exec` শুধু চলমান container-এ কাজ করে, আর image-এ shell থাকতে হয় (distroless-এ নেই)। বারবার crash করা container-এর জন্য `logs` আর `inspect`-এর উপর ভরসা করো। Compose-এ `docker compose logs api` আর `docker compose exec api sh` ব্যবহার করো।""",
        tip_en=r"""Give it as an order: status → logs → inspect → exec; it shows you debug systematically.""",
        tip_bn=r"""এটা একটা ক্রম হিসেবে বলো: status → logs → inspect → exec; এতে বোঝা যায় তুমি গুছিয়ে debug করো।""",
        follow=[("What does exit code 137 tell you?", "Exit code 137 থেকে কী বোঝা যায়?")],
        related=["docker-024", "docker-011"],
        refs=[D_EXEC],
    ),
    # ------------------------------------------------------------------ docker-q10
    Q(
        id="docker-q10", sub="Build Context and .dockerignore", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["dockerignore", "build-context", "security"],
        ver="Version-independent concept (Docker Engine 29 / BuildKit)", vs=False, status="stable",
        q_en=r"""What do you put in a `.dockerignore` for a Node.js project, and why?""",
        q_bn=r"""Node.js project-এর `.dockerignore`-এ কী রাখো, আর কেন?""",
        a_en=r"""Anything the image shouldn't contain or the build doesn't need: `node_modules`, `.git`, build output, logs and `.env` files. It keeps the build context small and fast, stops the host's `node_modules` overwriting the container's, and keeps secrets out of the image.""",
        a_bn=r"""যা image-এ থাকা উচিত না বা build-এ লাগে না: `node_modules`, `.git`, build output, log আর `.env` file। এতে build context ছোট আর দ্রুত হয়, host-এর `node_modules` container-এরটাকে overwrite করে না, আর secret image-এর বাইরে থাকে।""",
        code=r"""
            # .dockerignore
            node_modules
            .git
            dist
            npm-debug.log*
            .env*
        """, lang="text",
        ex_en=r"""It works like `.gitignore` but applies to the build context: ignored files never reach the builder, so `COPY . .` can't pick them up.""",
        ex_bn=r"""এটা `.gitignore`-এর মতো, কিন্তু build context-এর জন্য: ignore করা file builder-এ পৌঁছায়ই না, তাই `COPY . .` সেগুলো তুলতে পারে না।""",
        tip_en=r"""Name the three reasons in one breath: speed, correct builds and no leaked secrets.""",
        tip_bn=r"""তিনটা কারণ এক নিঃশ্বাসে বলো: speed, সঠিক build আর secret leak না হওয়া।""",
        follow=[("What is the build context?", "Build context কী?")],
        related=["docker-007", "docker-012"],
        refs=[D_CONTEXT],
    ),
]

if __name__ == "__main__":
    save("docker", "quick", QUESTIONS)
