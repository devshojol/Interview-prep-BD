# AWS batch 4 — aws-020 … aws-026 (DNS debugging, ECS/ECR, CloudWatch, HA architecture, IAM & Lambda debugging, cost)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

R53_MIGRATE = ("Route 53 — Making Route 53 the DNS service for a domain that's in use", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/migrate-dns-domain-in-use.html")
R53_TS = ("Route 53 — Routing traffic to an Amazon EC2 instance", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-ec2-instance.html")
EIP = ("Amazon EC2 — Elastic IP addresses", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html")
ECS_WELCOME = ("Amazon ECS — What is Amazon ECS?", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html")
ECS_TASKDEF = ("Amazon ECS — Task definitions", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definitions.html")
ECR = ("Amazon ECR — What is Amazon Elastic Container Registry?", "https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html")
CW_WHAT = ("Amazon CloudWatch — What is Amazon CloudWatch?", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html")
CW_AGENT = ("Amazon CloudWatch — Collect metrics and logs with the CloudWatch agent", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html")
ALB_METRICS = ("Elastic Load Balancing — CloudWatch metrics for your Application Load Balancer", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-cloudwatch-metrics.html")
XRAY = ("AWS X-Ray — What is AWS X-Ray?", "https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html")
WA = ("AWS Well-Architected Framework", "https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html")
ASG_TT = ("Amazon EC2 Auto Scaling — Target tracking scaling policies", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html")
ASG_LT = ("Amazon EC2 Auto Scaling — Launch templates", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-templates.html")
IAM_EVAL = ("IAM — Policy evaluation logic", "https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html")
IAM_TS_DENIED = ("IAM — Troubleshoot access denied error messages", "https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html")
S3_SSE_KMS = ("Amazon S3 — Using server-side encryption with AWS KMS keys (SSE-KMS)", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html")
LAMBDA_VPC = ("AWS Lambda — Giving Lambda functions access to resources in an Amazon VPC", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-vpc.html")
RDS_PROXY = ("Amazon RDS Proxy", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html")
LAMBDA_CONCURRENCY = ("AWS Lambda — Understanding Lambda function scaling (concurrency)", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-concurrency.html")
CE = ("AWS Cost Explorer", "https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html")
BUDGETS = ("AWS Budgets — Managing your costs with AWS Budgets", "https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html")
VPC_PRICING = ("Amazon VPC pricing (NAT Gateway, data processing)", "https://aws.amazon.com/vpc/pricing/")

QUESTIONS = [
    # ------------------------------------------------------------------ aws-020
    Q(
        id="aws-020", sub="Domain & DNS Troubleshooting", diff="medium", type="debugging",
        prio="high", market="bangladesh", mins=6,
        tags=["route53", "dns", "nameservers", "nginx", "https"],
        ver="Amazon Route 53; NGINX 1.30 (http2 on;); Let's Encrypt certbot", vs=True, status="stable",
        q_en=r"""Your Express app works at `http://203.0.113.25`, but `https://shop.example.com` doesn't load. The domain was bought from a local registrar, and you created a Route 53 hosted zone with an A record for `shop`. Using the output below, find every problem and explain the fix.""",
        q_bn=r"""তোমার Express app `http://203.0.113.25`-এ চলে, কিন্তু `https://shop.example.com` load হয় না। Domain একটা local registrar থেকে কেনা, আর তুমি Route 53-এ hosted zone বানিয়ে `shop`-এর জন্য A record দিয়েছ। নিচের output দেখে সব সমস্যা খুঁজে বের করো আর সমাধান ব্যাখ্যা করো।""",
        code=r"""
            $ dig +short NS example.com
            ns1.local-registrar-dns.com.
            ns2.local-registrar-dns.com.

            $ dig +short shop.example.com @ns-123.awsdns-15.com
            203.0.113.25

            $ dig +short shop.example.com
            (no answer)

            $ curl -I http://203.0.113.25
            HTTP/1.1 200 OK
            Server: nginx

            Security group inbound: TCP 22 (my IP), TCP 80 (0.0.0.0/0)
            Instance public IP: 203.0.113.25 (auto-assigned, no Elastic IP)

            # /etc/nginx/conf.d/shop.conf
            server {
                listen 80;
                server_name _;
                location / { proxy_pass http://127.0.0.1:3000; }
            }
        """,
        lang="text",
        a_en=r"""
            There are four problems:
            1. **DNS delegation.** The domain's NS records still point to the registrar's nameservers, so the world never asks Route 53. The record exists in the hosted zone (querying `awsdns` directly works), but that zone isn't authoritative. Fix: at the registrar, replace the nameservers with the **four NS records** shown in the Route 53 hosted zone (or create the A record in the registrar's own DNS instead). Delegation changes can take up to a day or two to propagate, depending on TTLs.
            2. **Port 443 is closed** in the security group. Fix: allow TCP 443 from `0.0.0.0/0` (and `::/0` for IPv6).
            3. **No TLS server in NGINX** and a catch-all `server_name _`. Fix: set `server_name shop.example.com`, then run `certbot --nginx -d shop.example.com`. The HTTP-01 challenge only succeeds *after* DNS resolves to this server, so fix DNS first.
            4. **No Elastic IP.** The auto-assigned public IP changes on stop/start, which would silently break the A record. Fix: allocate an Elastic IP and update the record (or put an ALB in front and use an alias record).
        """,
        a_bn=r"""
            এখানে চারটা সমস্যা:
            1. **DNS delegation।** Domain-এর NS record এখনো registrar-এর nameserver-এ point করছে, তাই দুনিয়া কখনো Route 53-কে জিজ্ঞেস করে না। Hosted zone-এ record আছে (`awsdns`-কে সরাসরি query করলে উত্তর আসে), কিন্তু ওই zone authoritative না। সমাধান: registrar-এ গিয়ে nameserver বদলে Route 53 hosted zone-এ দেখানো **চারটা NS record** বসাও (অথবা registrar-এর নিজের DNS-এ A record বানাও)। TTL অনুযায়ী delegation পরিবর্তন ছড়াতে এক-দুই দিন পর্যন্ত লাগতে পারে।
            2. **Security group-এ port 443 বন্ধ।** সমাধান: `0.0.0.0/0` থেকে (IPv6-এর জন্য `::/0`-ও) TCP 443 allow করো।
            3. **NGINX-এ কোনো TLS server নেই**, আর `server_name _` সবকিছু ধরছে। সমাধান: `server_name shop.example.com` দাও, তারপর `certbot --nginx -d shop.example.com` চালাও। HTTP-01 challenge তখনই সফল হয় যখন DNS এই server-এ resolve করে, তাই আগে DNS ঠিক করো।
            4. **Elastic IP নেই।** Auto-assigned public IP stop/start করলে বদলে যায়, তখন A record নিঃশব্দে ভেঙে যাবে। সমাধান: Elastic IP নিয়ে record update করো (অথবা সামনে ALB বসিয়ে alias record ব্যবহার করো)।
        """,
        quick_en=r"""Four problems: the registrar still delegates to its own nameservers instead of the Route 53 NS records, port 443 is closed in the security group, NGINX has no TLS server block (run certbot after DNS works), and there's no Elastic IP, so the IP changes on stop/start. Fix DNS delegation first.""",
        quick_bn=r"""চারটা সমস্যা: registrar এখনো নিজের nameserver-এ delegate করছে, Route 53-এর NS record-এ না; security group-এ port 443 বন্ধ; NGINX-এ কোনো TLS server block নেই (DNS ঠিক হলে certbot চালাও); আর Elastic IP নেই, তাই stop/start-এ IP বদলে যায়। আগে DNS delegation ঠিক করো।""",
        ex_en=r"""
            - **How to read the clues:** `dig NS` shows who is authoritative. Querying a specific nameserver (`@ns-…awsdns…`) tests the hosted zone in isolation. When the direct query works but the public one doesn't, it's always a delegation problem.
            - Creating a hosted zone does *not* change anything at the registrar. That's a manual step, and it's often forgotten when the domain is registered outside AWS, as is common with local registrars.
            - `curl -I http://IP` only proves NGINX and the app work. Test the real hostname and HTTPS with `curl -I https://shop.example.com` and `curl -v` to see TLS errors.
            - After DNS changes, local caches (browser, OS, ISP resolver) can still return old answers until the TTL expires. Use `dig @1.1.1.1` or `dig @8.8.8.8` to check public resolvers.
        """,
        ex_bn=r"""
            - **Clue কীভাবে পড়বে:** `dig NS` দেখায় কে authoritative। নির্দিষ্ট nameserver-কে query করলে (`@ns-…awsdns…`) শুধু hosted zone-টা আলাদাভাবে test হয়। সরাসরি query কাজ করে কিন্তু public query করে না, এমন হলে সমস্যা সবসময় delegation-এ।
            - Hosted zone বানালে registrar-এ কিছুই বদলায় *না*। এটা manual ধাপ, আর domain AWS-এর বাইরে register করা হলে (local registrar-এ যেমন প্রায়ই হয়) এটা অনেকেই ভুলে যায়।
            - `curl -I http://IP` শুধু প্রমাণ করে NGINX আর app চলছে। আসল hostname আর HTTPS test করো `curl -I https://shop.example.com` দিয়ে, আর TLS error দেখতে `curl -v` ব্যবহার করো।
            - DNS বদলানোর পরেও local cache (browser, OS, ISP resolver) TTL শেষ না হওয়া পর্যন্ত পুরনো উত্তর দিতে পারে। Public resolver যাচাই করতে `dig @1.1.1.1` বা `dig @8.8.8.8` ব্যবহার করো।
        """,
        tip_en=r"""Walk the request path in order: DNS resolution → network (SG port) → web server config (server_name, TLS) → certificate. Saying "DNS first, because certbot needs it" shows you understand the dependencies.""",
        tip_bn=r"""Request-এর পথ ধরে ক্রমানুসারে এগোও: DNS resolution → network (SG port) → web server config (server_name, TLS) → certificate। "আগে DNS, কারণ certbot-এর এটা লাগে" বললে বোঝা যায় তুমি dependency-গুলো বোঝো।""",
        mist_en=r"""Waiting days for "propagation" when the nameservers were never changed, opening only port 80, or running certbot before DNS points to the server.""",
        mist_bn=r"""Nameserver কখনো বদলানোই হয়নি, অথচ দিনের পর দিন "propagation"-এর জন্য অপেক্ষা করা, শুধু port 80 খোলা, বা DNS server-এ point করার আগেই certbot চালানো।""",
        extra=[
            dict(lang="nginx", label_en="Fixed NGINX config (after certbot)", label_bn="সংশোধিত NGINX config (certbot-এর পরে)", src=r"""
                server {
                    listen 80;
                    server_name shop.example.com;
                    return 301 https://$host$request_uri;
                }

                server {
                    listen 443 ssl;
                    http2 on;
                    server_name shop.example.com;

                    ssl_certificate     /etc/letsencrypt/live/shop.example.com/fullchain.pem;
                    ssl_certificate_key /etc/letsencrypt/live/shop.example.com/privkey.pem;

                    location / {
                        proxy_pass http://127.0.0.1:3000;
                        proxy_set_header Host $host;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_set_header X-Forwarded-Proto $scheme;
                    }
                }
            """),
            dict(lang="bash", label_en="Verify and fix", label_bn="যাচাই ও সমাধান", src=r"""
                # After updating the nameservers at the registrar:
                dig +short NS example.com              # must list the 4 awsdns servers of the hosted zone
                dig +short shop.example.com @8.8.8.8   # must return the Elastic IP

                aws ec2 authorize-security-group-ingress --group-id sg-0123456789abcdef0 \
                  --protocol tcp --port 443 --cidr 0.0.0.0/0
                sudo certbot --nginx -d shop.example.com
                curl -I https://shop.example.com
            """),
        ],
        follow=[
            ("What is the difference between a hosted zone's NS records and the registrar's nameserver setting?", "Hosted zone-এর NS record আর registrar-এর nameserver setting-এর পার্থক্য কী?"),
            ("How would you move this setup behind an ALB with an ACM certificate?", "এই setup-কে ACM certificate-সহ একটা ALB-এর পেছনে কীভাবে নেবে?"),
        ],
        related=["aws-011", "aws-012", "aws-009"],
        refs=[R53_MIGRATE, R53_TS, EIP],
    ),
    # ------------------------------------------------------------------ aws-021
    Q(
        id="aws-021", sub="ECS & ECR Fundamentals", diff="medium", type="conceptual",
        prio="medium", market="both", mins=5,
        tags=["ecs", "fargate", "ecr", "task-definition", "containers"],
        ver="Amazon ECS / AWS Fargate / Amazon ECR (2026)", vs=False, status="stable",
        q_en=r"""How would you run a containerized Node.js API on Amazon ECS? Explain clusters, task definitions, tasks and services, when you'd choose Fargate vs the EC2 launch type, and where ECR fits.""",
        q_bn=r"""Amazon ECS-এ একটা containerized Node.js API কীভাবে চালাবে? Cluster, task definition, task আর service ব্যাখ্যা করো; কখন Fargate আর কখন EC2 launch type বেছে নেবে, আর ECR কোথায় কাজে আসে?""",
        a_en=r"""
            - **ECR** is the private container registry. CI builds the image, tags it with the git SHA (not just `latest`), scans it and pushes it to ECR.
            - A **task definition** is a versioned JSON blueprint: image, CPU/memory, port mappings, environment variables and `secrets` (from Secrets Manager or Parameter Store), log configuration (`awslogs` → CloudWatch Logs), health check, and two IAM roles. The **task role** holds the app's AWS permissions. The **task execution role** lets ECS pull the image, write logs and fetch the secrets.
            - A **task** is a running copy of a task definition (one or more containers).
            - A **service** keeps N tasks running, replaces unhealthy ones, registers them with an ALB target group, performs rolling (or blue/green) deployments, and scales with Service Auto Scaling (target tracking on CPU or ALB requests per target).
            - A **cluster** is the logical grouping, with capacity providers.

            **Fargate** is serverless: no EC2 instances to patch, you pay per task vCPU/memory, and each task gets its own ENI and security group (`awsvpc` mode). The **EC2 launch type** means managing instances yourself (Auto Scaling group, AMI patching). In return you get cheaper capacity at steady high utilisation, GPUs or specific instance types, and more host-level control. I default to Fargate (and Fargate Spot for interruptible work) unless one of those reasons applies.
        """,
        a_bn=r"""
            - **ECR** হলো private container registry। CI image build করে, git SHA দিয়ে tag করে (শুধু `latest` না), scan করে, তারপর ECR-এ push করে।
            - **Task definition** হলো versioned JSON blueprint: image, CPU/memory, port mapping, environment variable আর `secrets` (Secrets Manager বা Parameter Store থেকে), log configuration (`awslogs` → CloudWatch Logs), health check, আর দুইটা IAM role। **Task role**-এ থাকে app-এর AWS permission। **Task execution role** দিয়ে ECS image pull করে, log লেখে আর secret আনে।
            - **Task** হলো task definition-এর একটা চলমান copy (এক বা একাধিক container)।
            - **Service** N-টা task চালু রাখে, unhealthy task replace করে, ALB target group-এ register করে, rolling (বা blue/green) deployment করে, আর Service Auto Scaling দিয়ে scale করে (CPU বা ALB-এর প্রতি target-এ request-এর উপর target tracking)।
            - **Cluster** হলো logical grouping, capacity provider-সহ।

            **Fargate** serverless: patch করার মতো কোনো EC2 instance নেই, task-এর vCPU/memory অনুযায়ী টাকা দাও, আর প্রতিটা task নিজের ENI আর security group পায় (`awsvpc` mode)। **EC2 launch type**-এ instance নিজে manage করতে হয় (Auto Scaling group, AMI patching)। বিনিময়ে পাও স্থির বেশি utilisation-এ সস্তা capacity, GPU বা নির্দিষ্ট instance type, আর host-level control বেশি। এই কারণগুলোর কোনোটা না থাকলে আমি default হিসেবে Fargate নিই (আর interrupt হলেও চলে এমন কাজের জন্য Fargate Spot)।
        """,
        quick_en=r"""ECR stores images, a task definition is the versioned blueprint (image, CPU/memory, secrets, logs, task and execution roles), a task is a running copy, and a service keeps N tasks healthy behind an ALB. Default to Fargate (no servers to patch); pick the EC2 launch type for steady high utilisation, GPUs or host-level control.""",
        quick_bn=r"""ECR image রাখে, task definition হলো versioned blueprint (image, CPU/memory, secret, log, task role আর execution role), task হলো তার চলমান copy, আর service ALB-এর পেছনে N-টা task সুস্থ রাখে। Default হিসেবে Fargate নাও (patch করার server নেই); টানা বেশি utilisation, GPU বা host-level control লাগলে EC2 launch type নাও।""",
        ex_en=r"""
            - **Task role vs execution role** is the most common confusion. If the *app* gets AccessDenied calling S3, fix the task role. If the task fails to *start* with errors pulling the image or reading secrets, fix the execution role.
            - Tasks in private subnets need a route to ECR: either a NAT Gateway, or VPC endpoints (`ecr.api`, `ecr.dkr`, an S3 gateway endpoint for image layers, and `logs`). Otherwise tasks fail with image-pull timeouts.
            - Build multi-arch or ARM64 images if you run on Graviton (`runtimePlatform.cpuArchitecture: ARM64`).
            - Enable the deployment circuit breaker with rollback so a broken image doesn't loop forever. Also set a health-check grace period long enough for the app to boot.
            - ECS vs EKS: ECS is simpler and AWS-native. EKS makes sense when you need Kubernetes APIs, portability or its ecosystem.
        """,
        ex_bn=r"""
            - **Task role বনাম execution role** নিয়েই সবচেয়ে বেশি গুলিয়ে যায়। *App* S3 call করে AccessDenied পেলে task role ঠিক করো। Image pull বা secret পড়তে error দিয়ে task *start*-ই না হলে execution role ঠিক করো।
            - Private subnet-এর task-এর ECR পর্যন্ত route লাগে: হয় NAT Gateway, নয়তো VPC endpoint (`ecr.api`, `ecr.dkr`, image layer-এর জন্য S3 gateway endpoint, আর `logs`)। না থাকলে task image-pull timeout দিয়ে fail করে।
            - Graviton-এ চালালে multi-arch বা ARM64 image build করো (`runtimePlatform.cpuArchitecture: ARM64`)।
            - Deployment circuit breaker rollback-সহ চালু রাখো, যাতে ভাঙা image অনন্তকাল loop না করে। App boot হওয়ার মতো যথেষ্ট লম্বা health-check grace period-ও দাও।
            - ECS বনাম EKS: ECS সহজ আর AWS-native। Kubernetes API, portability বা তার ecosystem লাগলে EKS যুক্তিসংগত।
        """,
        tip_en=r"""Build the answer bottom-up (image in ECR → task definition → task → service → cluster), then make the Fargate vs EC2 call with a reason. Explaining task role vs execution role is a strong differentiator.""",
        tip_bn=r"""নিচ থেকে উপরে সাজাও (ECR-এ image → task definition → task → service → cluster), তারপর কারণসহ Fargate বনাম EC2-এর সিদ্ধান্ত দাও। Task role বনাম execution role ব্যাখ্যা করতে পারলে তুমি অন্যদের থেকে আলাদা হয়ে যাবে।""",
        mist_en=r"""Deploying with the `latest` tag (you can't tell which version is running or roll back reliably), putting secrets in plain `environment` values, or giving the execution role the app's S3 permissions.""",
        mist_bn=r"""`latest` tag দিয়ে deploy করা (কোন version চলছে বোঝা যায় না, ঠিকমতো rollback-ও করা যায় না), secret সাধারণ `environment` value হিসেবে রাখা, বা app-এর S3 permission execution role-কে দিয়ে দেওয়া।""",
        code=r"""
            {
              "family": "orders-api",
              "requiresCompatibilities": ["FARGATE"],
              "networkMode": "awsvpc",
              "cpu": "512",
              "memory": "1024",
              "runtimePlatform": { "cpuArchitecture": "ARM64", "operatingSystemFamily": "LINUX" },
              "executionRoleArn": "arn:aws:iam::111122223333:role/ordersTaskExecutionRole",
              "taskRoleArn": "arn:aws:iam::111122223333:role/ordersTaskRole",
              "containerDefinitions": [
                {
                  "name": "api",
                  "image": "111122223333.dkr.ecr.ap-south-1.amazonaws.com/orders-api:3f9c2ab",
                  "essential": true,
                  "portMappings": [{ "containerPort": 3000, "protocol": "tcp" }],
                  "environment": [{ "name": "NODE_ENV", "value": "production" }],
                  "secrets": [
                    {
                      "name": "DATABASE_URL",
                      "valueFrom": "arn:aws:secretsmanager:ap-south-1:111122223333:secret:prod/orders/db-url-AbCdEf"
                    }
                  ],
                  "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                      "awslogs-group": "/ecs/orders-api",
                      "awslogs-region": "ap-south-1",
                      "awslogs-stream-prefix": "api"
                    }
                  }
                }
              ]
            }
        """,
        lang="json",
        follow=[
            ("A task keeps stopping with `CannotPullContainerError`. What do you check?", "একটা task বারবার `CannotPullContainerError` দিয়ে বন্ধ হচ্ছে। কী কী check করবে?"),
            ("When would you pick EKS over ECS?", "কখন ECS-এর বদলে EKS বেছে নেবে?"),
        ],
        related=["aws-016", "aws-028"],
        refs=[ECS_WELCOME, ECS_TASKDEF, ECR],
    ),
    # ------------------------------------------------------------------ aws-022
    Q(
        id="aws-022", sub="CloudWatch Monitoring & X-Ray", diff="medium", type="scenario",
        prio="high", market="both", mins=7,
        tags=["cloudwatch", "alarms", "logs", "x-ray", "observability"],
        ver="Amazon CloudWatch / AWS X-Ray (2026); Node.js 24", vs=False, status="stable",
        q_en=r"""Your Node.js API runs on EC2 behind an ALB. Users report slowness and occasional 5xx errors, but there's no monitoring yet. What would you set up with CloudWatch (and X-Ray), and which alarms would you create first?""",
        q_bn=r"""তোমার Node.js API একটা ALB-এর পেছনে EC2-তে চলে। User-রা ধীরগতি আর মাঝে মাঝে 5xx error-এর অভিযোগ করছে, কিন্তু এখনো কোনো monitoring নেই। CloudWatch (আর X-Ray) দিয়ে কী কী setup করবে, আর প্রথমে কোন alarm-গুলো বানাবে?""",
        a_en=r"""
            - **Metrics:** the ALB publishes `RequestCount`, `TargetResponseTime`, `HTTPCode_Target_5XX_Count`, `HTTPCode_ELB_5XX_Count` and `UnHealthyHostCount` automatically. EC2 provides CPU, network and status checks. **Memory and disk usage are not collected by default**, so I install the **CloudWatch agent** for those. On RDS I watch CPU, `DatabaseConnections`, `FreeStorageSpace` and read/write latency.
            - **Logs:** ship structured JSON app logs and NGINX logs to CloudWatch Logs with the agent, and set a **retention period** (the default is never expire). Use **Logs Insights** to query errors by route, and metric filters to turn log patterns into metrics.
            - **Alarms → SNS** (email, chat or paging): target 5xx count or rate, p95/p99 `TargetResponseTime` above the SLO, `UnHealthyHostCount > 0`, CPU high for 15 minutes, disk above 80%, low RDS free storage, and failed status checks (with auto-recovery).
            - **Dashboards** give one shared view per service.
            - **Tracing:** instrument the app with OpenTelemetry (AWS Distro for OpenTelemetry) and send traces to **X-Ray**, so I can see which downstream call (DB query, external API) makes requests slow.
        """,
        a_bn=r"""
            - **Metric:** ALB নিজে থেকেই `RequestCount`, `TargetResponseTime`, `HTTPCode_Target_5XX_Count`, `HTTPCode_ELB_5XX_Count` আর `UnHealthyHostCount` publish করে। EC2 দেয় CPU, network আর status check। **Memory আর disk usage default-এ collect হয় না**, তাই এগুলোর জন্য **CloudWatch agent** install করি। RDS-এ দেখি CPU, `DatabaseConnections`, `FreeStorageSpace` আর read/write latency।
            - **Log:** agent দিয়ে structured JSON app log আর NGINX log CloudWatch Logs-এ পাঠাই, আর **retention period** set করি (default হলো কখনো expire না হওয়া)। Route অনুযায়ী error খুঁজতে **Logs Insights** query, আর log pattern থেকে metric বানাতে metric filter ব্যবহার করি।
            - **Alarm → SNS** (email, chat বা paging): target 5xx-এর সংখ্যা বা rate, SLO-র উপরে p95/p99 `TargetResponseTime`, `UnHealthyHostCount > 0`, ১৫ মিনিট ধরে বেশি CPU, ৮০%-এর বেশি disk, RDS-এর free storage কম, আর status check fail (auto-recovery-সহ)।
            - **Dashboard** প্রতিটা service-এর জন্য একটা shared view দেয়।
            - **Tracing:** OpenTelemetry (AWS Distro for OpenTelemetry) দিয়ে app instrument করে trace **X-Ray**-তে পাঠাই, যাতে বোঝা যায় কোন downstream call (DB query, external API) request ধীর করছে।
        """,
        quick_en=r"""Use the built-in ALB and EC2 metrics plus the CloudWatch agent for memory, disk and logs (with a retention period), then alarm through SNS on target 5xx, p95/p99 `TargetResponseTime`, `UnHealthyHostCount`, CPU and disk. Add OpenTelemetry tracing to X-Ray to see which downstream call is slow.""",
        quick_bn=r"""ALB আর EC2-এর built-in metric নাও, আর memory, disk ও log-এর জন্য CloudWatch agent বসাও (retention period-সহ); তারপর target 5xx, p95/p99 `TargetResponseTime`, `UnHealthyHostCount`, CPU আর disk-এর ওপর SNS-এ alarm দাও। কোন downstream call ধীর সেটা দেখতে OpenTelemetry দিয়ে X-Ray-তে trace পাঠাও।""",
        ex_en=r"""
            - **ELB 5xx vs target 5xx** tells you where the problem is. `HTTPCode_Target_5XX` means your app returned the error. `HTTPCode_ELB_5XX` (502/503/504) means the load balancer couldn't get a good response: no healthy targets, timeouts, or connections closed by the backend.
            - **A classic cause of random 502s with Node behind an ALB:** the ALB's idle timeout defaults to 60 s, but Node's `server.keepAliveTimeout` defaults to 5 s. Node closes idle keep-alive sockets the ALB still wants to reuse. Set Node's keep-alive timeout *higher* than the ALB idle timeout.
            - **Good alarm hygiene:** alarm on percentiles, not averages. Use "M out of N" datapoints to avoid flapping, decide how missing data is treated, and combine signals with composite alarms to reduce noise.
            - **Cost:** verbose debug logging, logs with no retention, and high-cardinality custom metrics (one metric per user ID) can cost more than the servers.
        """,
        ex_bn=r"""
            - **ELB 5xx বনাম target 5xx** দেখে বোঝা যায় সমস্যা কোথায়। `HTTPCode_Target_5XX` মানে তোমার app error দিয়েছে। `HTTPCode_ELB_5XX` (502/503/504) মানে load balancer ঠিকঠাক response পায়নি: কোনো healthy target নেই, timeout হয়েছে, বা backend connection বন্ধ করে দিয়েছে।
            - **ALB-এর পেছনে Node-এ এলোমেলো 502-এর একটা classic কারণ:** ALB-এর idle timeout default 60 s, কিন্তু Node-এর `server.keepAliveTimeout` default 5 s। ALB যে idle keep-alive socket আবার ব্যবহার করতে চায়, Node সেটা বন্ধ করে দেয়। Node-এর keep-alive timeout ALB-এর idle timeout-এর চেয়ে *বেশি* রাখো।
            - **ভালো alarm-এর নিয়ম:** average-এর বদলে percentile-এ alarm দাও। Flapping এড়াতে "N-এর মধ্যে M" datapoint ব্যবহার করো, missing data কীভাবে ধরা হবে ঠিক করো, আর noise কমাতে composite alarm দিয়ে signal একত্র করো।
            - **খরচ:** বেশি debug logging, retention ছাড়া log, আর high-cardinality custom metric (প্রতি user ID-তে একটা metric) server-এর চেয়েও বেশি খরচ করাতে পারে।
        """,
        tip_en=r"""Organise the answer as metrics → logs → alarms → traces, then use the ELB-5xx vs target-5xx split to show how you'd actually debug the reported problem. The keep-alive timeout detail is memorable.""",
        tip_bn=r"""উত্তর সাজাও metric → log → alarm → trace ক্রমে, তারপর ELB-5xx বনাম target-5xx ভাগ দিয়ে দেখাও যে অভিযোগ করা সমস্যাটা আসলে কীভাবে debug করবে। Keep-alive timeout-এর detail-টা interviewer-এর মনে থাকে।""",
        mist_en=r"""Expecting memory metrics without the agent, alarming on average latency only, or leaving log groups on "never expire".""",
        mist_bn=r"""Agent ছাড়াই memory metric আশা করা, শুধু average latency-তে alarm দেওয়া, বা log group "never expire" অবস্থায় রেখে দেওয়া।""",
        code=r"""
            # Alarm when the app returns more than 10 5xx responses/minute in 3 of the last 5 minutes
            aws cloudwatch put-metric-alarm \
              --alarm-name api-target-5xx \
              --namespace AWS/ApplicationELB \
              --metric-name HTTPCode_Target_5XX_Count \
              --dimensions Name=LoadBalancer,Value=app/prod-alb/50dc6c495c0c9188 \
              --statistic Sum --period 60 \
              --evaluation-periods 5 --datapoints-to-alarm 3 \
              --threshold 10 --comparison-operator GreaterThanThreshold \
              --treat-missing-data notBreaching \
              --alarm-actions arn:aws:sns:ap-south-1:111122223333:oncall-alerts
        """,
        lang="bash",
        extra=[dict(lang="javascript", label_en="Fix for intermittent 502s behind an ALB", label_bn="ALB-এর পেছনে মাঝে মাঝে 502-এর সমাধান", src=r"""
            const server = app.listen(3000);
            // ALB idle timeout defaults to 60 s; keep idle sockets open longer on the Node side
            server.keepAliveTimeout = 65_000;
            server.headersTimeout = 66_000; // keep it above keepAliveTimeout (required on older Node versions)
        """)],
        follow=[
            ("How do you tell whether a 502 comes from the load balancer or from your app?", "502-টা load balancer থেকে আসছে নাকি তোমার app থেকে, কীভাবে বুঝবে?"),
            ("Why alarm on p99 latency instead of average latency?", "Average-এর বদলে p99 latency-তে alarm কেন দেবে?"),
        ],
        related=["aws-019", "aws-023"],
        refs=[CW_WHAT, CW_AGENT, ALB_METRICS],
    ),
    # ------------------------------------------------------------------ aws-023
    Q(
        id="aws-023", sub="High Availability Architecture", diff="hard", type="architecture",
        prio="high", market="international", mins=12,
        tags=["high-availability", "multi-az", "auto-scaling", "alb", "well-architected"],
        ver="AWS (2026): ALB, EC2 Auto Scaling / ECS, RDS Multi-AZ, CloudFront", vs=False, status="stable",
        q_en=r"""Design a highly available three-tier web application (React frontend, Node.js API, PostgreSQL) on AWS that survives the loss of an entire Availability Zone. Explain the components, data flow, failure scenarios, and how you'd review the design against the Well-Architected Framework.""",
        q_bn=r"""AWS-এ একটা highly available three-tier web application (React frontend, Node.js API, PostgreSQL) design করো, যেটা পুরো একটা Availability Zone নষ্ট হলেও টিকে থাকবে। Component, data flow, failure scenario, আর Well-Architected Framework অনুযায়ী design কীভাবে review করবে তা ব্যাখ্যা করো।""",
        a_en=r"""
            First I'd clarify requirements: target availability (99.9% vs 99.99%), peak traffic, RPO/RTO, compliance and budget.

            **Design (across three AZs):**
            - **Edge:** Route 53 alias → **CloudFront** with **AWS WAF**. The default behaviour serves the React build from a private S3 bucket through OAC. A `/api/*` behaviour forwards to the ALB with caching disabled.
            - **API tier:** an **ALB** in public subnets → an **Auto Scaling group** (launch template: Amazon Linux 2023 AMI, instance profile, IMDSv2 required) or an ECS Fargate service in private subnets in every AZ. Scaling uses **target tracking** (CPU around 50%, or `ALBRequestCountPerTarget`), and **ELB health checks** replace bad instances. The app is **stateless**: sessions in ElastiCache or signed tokens, files in S3.
            - **Data:** **RDS PostgreSQL Multi-AZ** (or Aurora with replicas in other AZs) with automated backups and PITR. Read replicas absorb read-heavy traffic, RDS Proxy handles connection storms, and ElastiCache (Redis/Valkey) runs Multi-AZ with automatic failover.
            - **Network:** public, app and DB subnets in each AZ, one zonal NAT Gateway per AZ (or a regional NAT Gateway), an S3 gateway endpoint, and security groups chained ALB → app → DB.
            - **Operations:** IaC (CloudFormation/CDK/Terraform), CloudWatch alarms and dashboards, tracing, and blue/green or canary deployments.

            **Failure scenarios:** if an AZ dies, the ALB stops routing to it, the remaining AZs already have enough capacity (static stability), and RDS fails over to the standby. A crashed instance fails its health check and gets replaced. A bad deploy triggers alarms and rollback. A full Region outage is out of scope for HA; that's the DR design.
        """,
        a_bn=r"""
            আগে requirement পরিষ্কার করব: target availability (99.9% নাকি 99.99%), peak traffic, RPO/RTO, compliance আর budget।

            **Design (তিনটা AZ জুড়ে):**
            - **Edge:** Route 53 alias → **CloudFront**, সাথে **AWS WAF**। Default behaviour OAC দিয়ে private S3 bucket থেকে React build serve করে। `/api/*` behaviour caching বন্ধ রেখে ALB-তে forward করে।
            - **API tier:** public subnet-এ **ALB** → প্রতিটা AZ-এর private subnet-এ একটা **Auto Scaling group** (launch template: Amazon Linux 2023 AMI, instance profile, IMDSv2 required) বা ECS Fargate service। Scaling হয় **target tracking** দিয়ে (CPU প্রায় 50%, বা `ALBRequestCountPerTarget`), আর **ELB health check** খারাপ instance replace করে। App **stateless**: session থাকে ElastiCache-এ বা signed token-এ, file থাকে S3-এ।
            - **Data:** automated backup আর PITR-সহ **RDS PostgreSQL Multi-AZ** (বা অন্য AZ-এ replica-সহ Aurora)। Read-heavy traffic সামলায় read replica, connection storm সামলায় RDS Proxy, আর ElastiCache (Redis/Valkey) Multi-AZ-এ automatic failover-সহ চলে।
            - **Network:** প্রতি AZ-এ public, app আর DB subnet, প্রতি AZ-এ একটা zonal NAT Gateway (অথবা একটা regional NAT Gateway), একটা S3 gateway endpoint, আর ALB → app → DB পর্যন্ত চেইন করা security group।
            - **Operations:** IaC (CloudFormation/CDK/Terraform), CloudWatch alarm ও dashboard, tracing, আর blue/green বা canary deployment।

            **Failure scenario:** একটা AZ নষ্ট হলে ALB সেখানে routing বন্ধ করে, বাকি AZ-গুলোতে আগে থেকেই যথেষ্ট capacity আছে (static stability), আর RDS standby-তে failover করে। কোনো instance crash করলে health check fail করে replace হয়। খারাপ deploy হলে alarm বাজে আর rollback হয়। পুরো Region down হওয়া HA-র scope-এর বাইরে; সেটা DR design-এর কাজ।
        """,
        quick_en=r"""Spread every tier across AZs: CloudFront with WAF in front of a private S3 bucket and an ALB, a stateless API in an Auto Scaling group or ECS service with health checks, and RDS Multi-AZ. Size capacity so the remaining AZs carry the load (static stability); a full-Region outage is a DR problem, not HA.""",
        quick_bn=r"""প্রতিটা tier কয়েকটা AZ জুড়ে ছড়াও: private S3 bucket আর ALB-এর সামনে WAF-সহ CloudFront, health check-সহ Auto Scaling group বা ECS service-এ stateless API, আর RDS Multi-AZ। Capacity এমনভাবে রাখো যেন বাকি AZ-গুলো পুরো load নিতে পারে (static stability); পুরো Region down হওয়া DR-এর বিষয়, HA-র না।""",
        ex_en=r"""
            *Advanced material.* Points that separate senior answers:
            - **Static stability:** don't depend on scaling *during* an AZ failure, because capacity may be scarce exactly then. With three AZs, run each at no more than about two-thirds of what it could handle at peak, so two AZs can carry the full load. That's the cost of N+1.
            - **Health check depth:** if `/healthz` checks the database, a DB blip can mark *every* instance unhealthy and take the whole fleet out. Keep the load balancer's health check shallow (is the process alive?) and alarm on dependency health separately.
            - **Failover behaviour:** clients must retry with exponential backoff and jitter, reconnect after the RDS DNS flip, and not cache DNS for too long. RDS Proxy shortens the impact.
            - **CloudFront cache policies:** use the managed `CachingDisabled` policy plus an origin request policy for `/api/*`, and `CachingOptimized` for static assets.
            - **Well-Architected review (6 pillars):** *Operational Excellence* (IaC, runbooks, observability), *Security* (least-privilege IAM, encryption, WAF), *Reliability* (multi-AZ, backups, health checks), *Performance Efficiency* (caching, right instance families), *Cost Optimization* (Savings Plans for the baseline, Spot for burst, right-sizing), *Sustainability* (Graviton, scaling with demand).
        """,
        ex_bn=r"""
            *Advanced বিষয়।* যে পয়েন্টগুলো senior উত্তরকে আলাদা করে:
            - **Static stability:** AZ failure-এর *সময়* scaling-এর উপর নির্ভর কোরো না, কারণ ঠিক তখনই capacity কম পাওয়া যেতে পারে। তিনটা AZ থাকলে peak-এ প্রতিটা AZ-কে তার ক্ষমতার মোটামুটি দুই-তৃতীয়াংশের বেশি চালিও না, যাতে দুইটা AZ পুরো load নিতে পারে। N+1-এর খরচ এটাই।
            - **Health check কতটা গভীর:** `/healthz` যদি database check করে, তাহলে DB-র সামান্য সমস্যাতেই *সব* instance unhealthy হয়ে পুরো fleet বাদ পড়ে যেতে পারে। Load balancer-এর health check হালকা রাখো (process বেঁচে আছে কি না), আর dependency-র health-এর জন্য আলাদা alarm দাও।
            - **Failover-এর আচরণ:** client-কে exponential backoff আর jitter-সহ retry করতে হবে, RDS-এর DNS বদলের পরে reconnect করতে হবে, আর DNS বেশিক্ষণ cache করা যাবে না। RDS Proxy প্রভাবের সময়টা কমায়।
            - **CloudFront cache policy:** `/api/*`-এর জন্য managed `CachingDisabled` policy আর একটা origin request policy, static asset-এর জন্য `CachingOptimized`।
            - **Well-Architected review (৬টা pillar):** *Operational Excellence* (IaC, runbook, observability), *Security* (least-privilege IAM, encryption, WAF), *Reliability* (multi-AZ, backup, health check), *Performance Efficiency* (caching, সঠিক instance family), *Cost Optimization* (baseline-এর জন্য Savings Plans, burst-এর জন্য Spot, right-sizing), *Sustainability* (Graviton, demand অনুযায়ী scaling)।
        """,
        tip_en=r"""Clarify requirements first, then go outside-in (DNS → edge → LB → compute → data). Finish with explicit failure scenarios. Naming all six Well-Architected pillars, including Sustainability, signals you've done real design reviews.""",
        tip_bn=r"""আগে requirement পরিষ্কার করো, তারপর বাইরে থেকে ভেতরে যাও (DNS → edge → LB → compute → data)। শেষ করো নির্দিষ্ট failure scenario দিয়ে। Sustainability-সহ Well-Architected-এর ছয়টা pillar-এর নাম বলতে পারলে বোঝা যায় তুমি সত্যিকারের design review করেছ।""",
        mist_en=r"""Running everything in one AZ "with an Auto Scaling group", storing sessions or uploads on instance disks, using one zonal NAT Gateway for all AZs, or making the health check depend on the database.""",
        mist_bn=r""""Auto Scaling group আছে" বলে সবকিছু একটা AZ-এ চালানো, instance-এর disk-এ session বা upload রাখা, সব AZ-এর জন্য একটা zonal NAT Gateway, বা health check-কে database-এর উপর নির্ভরশীল করা।""",
        code=r"""
            Users ─► Route 53 (alias) ─► CloudFront + AWS WAF
                                          ├── /*      ─► S3 (private, OAC)        React build
                                          └── /api/*  ─► ALB (public subnets: AZ-a | AZ-b | AZ-c)
                                                          │  health check: GET /healthz (shallow)
                                                          ▼
                                 Auto Scaling group / ECS service (private app subnets, 3 AZs)
                                 target tracking: ALBRequestCountPerTarget or CPU ~50%
                                                          │
                          ┌───────────────────────────────┼─────────────────────────────┐
                          ▼                               ▼                             ▼
              ElastiCache (Multi-AZ)          RDS Proxy ─► RDS PostgreSQL Multi-AZ     S3 (uploads)
                                                           (+ read replica, PITR backups)
        """,
        lang="text",
        follow=[
            ("How much spare capacity do you need per AZ to survive losing one of three AZs?", "তিনটা AZ-এর একটা হারালেও টিকে থাকতে প্রতি AZ-এ কতটা বাড়তি capacity লাগে?"),
            ("What would you change to also survive a full Region outage?", "পুরো Region outage-এও টিকে থাকতে কী বদলাবে?"),
        ],
        related=["aws-017", "aws-018", "aws-019", "aws-030"],
        refs=[WA, ASG_TT, ASG_LT],
    ),
    # ------------------------------------------------------------------ aws-024
    Q(
        id="aws-024", sub="IAM Policy Evaluation & AccessDenied", diff="hard", type="debugging",
        prio="high", market="both", mins=8,
        tags=["iam", "access-denied", "policy-evaluation", "kms", "s3"],
        ver="IAM policy evaluation logic; Amazon S3 SSE-KMS; AWS SDK for JavaScript v3", vs=False, status="stable",
        q_en=r"""A Lambda function writes reports to S3 but fails with the error below. Find **all** the causes, then explain how you'd systematically debug IAM `AccessDenied` errors in general.""",
        q_bn=r"""একটা Lambda function S3-এ report লেখে, কিন্তু নিচের error দিয়ে fail করছে। **সবগুলো** কারণ খুঁজে বের করো, তারপর সাধারণভাবে IAM `AccessDenied` error কীভাবে ধাপে ধাপে debug করবে তা ব্যাখ্যা করো।""",
        code=r"""
            Error (Lambda logs):
            AccessDenied: User: arn:aws:sts::111122223333:assumed-role/report-fn-role/report-fn
            is not authorized to perform: s3:PutObject on resource:
            "arn:aws:s3:::acme-reports/2026/10/report.pdf"

            --- Identity policy attached to report-fn-role ---
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Effect": "Allow",
                  "Action": ["s3:PutObject", "s3:GetObject"],
                  "Resource": "arn:aws:s3:::acme-reports"
                }
              ]
            }

            --- Bucket policy on acme-reports (default encryption: SSE-KMS with a customer managed key) ---
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "DenyUploadsWithoutKmsHeader",
                  "Effect": "Deny",
                  "Principal": "*",
                  "Action": "s3:PutObject",
                  "Resource": "arn:aws:s3:::acme-reports/*",
                  "Condition": {
                    "StringNotEquals": { "s3:x-amz-server-side-encryption": "aws:kms" }
                  }
                }
              ]
            }

            --- Upload code ---
            await s3.send(new PutObjectCommand({ Bucket: "acme-reports", Key: key, Body: pdf }));
        """,
        lang="text",
        a_en=r"""
            Three separate problems, and each alone would cause `AccessDenied`:
            1. **Wrong resource ARN (no Allow).** `s3:PutObject` is an *object* action, but the policy grants it on the *bucket* ARN. The resource must be `arn:aws:s3:::acme-reports/*` (ideally narrowed to a prefix). As written, nothing allows the action, so it's implicitly denied.
            2. **Explicit Deny in the bucket policy.** The code doesn't send `x-amz-server-side-encryption: aws:kms`. When a condition key is *missing*, a negated operator like `StringNotEquals` evaluates to **true**, so the Deny applies, even though bucket default encryption would have encrypted the object with KMS anyway. An explicit Deny always wins. Fix: send `ServerSideEncryption: "aws:kms"` in the request, or change the policy so it denies only when the header is present with the wrong value (add a `Null` check), and rely on default encryption.
            3. **Missing KMS permission.** Writing an SSE-KMS object requires `kms:GenerateDataKey` on the key (and reading requires `kms:Decrypt`). The key policy must also allow it, either directly or by delegating to IAM in the account.

            **General method:** read the full error, since many services now say which policy type denied the request. Confirm *which principal* actually made the call (CloudTrail `userIdentity`), because wrong credentials are common. Then walk the evaluation chain: explicit Deny anywhere (SCPs/RCPs, resource policy, identity policy, permissions boundary, session policy) → is there an Allow in the identity or resource policy → do the SCP and permissions boundary also allow it → KMS key policy → VPC endpoint policy. Test fixes with the IAM policy simulator and IAM Access Analyzer.
        """,
        a_bn=r"""
            তিনটা আলাদা সমস্যা, আর যেকোনো একটাই `AccessDenied`-এর জন্য যথেষ্ট:
            1. **ভুল resource ARN (কোনো Allow নেই)।** `s3:PutObject` হলো *object* action, কিন্তু policy সেটা দিয়েছে *bucket* ARN-এ। Resource হওয়া উচিত `arn:aws:s3:::acme-reports/*` (সম্ভব হলে কোনো prefix-এ সীমিত)। এখন যেভাবে লেখা, কিছুই action-টা allow করে না, তাই implicitly deny।
            2. **Bucket policy-তে explicit Deny।** Code `x-amz-server-side-encryption: aws:kms` header পাঠায় না। Condition key *না থাকলে* `StringNotEquals`-এর মতো negated operator **true** হয়, তাই Deny কার্যকর হয়, যদিও bucket-এর default encryption এমনিতেই object-টা KMS দিয়ে encrypt করত। Explicit Deny সবসময় জেতে। সমাধান: request-এ `ServerSideEncryption: "aws:kms"` পাঠাও, অথবা policy বদলে শুধু header থাকলে আর value ভুল হলে deny করো (`Null` check যোগ করে), আর default encryption-এর উপর ভরসা রাখো।
            3. **KMS permission নেই।** SSE-KMS object লিখতে key-তে `kms:GenerateDataKey` লাগে (আর পড়তে `kms:Decrypt`)। Key policy-কেও এটা allow করতে হবে, সরাসরি অথবা account-এর IAM-কে delegate করে।

            **সাধারণ পদ্ধতি:** পুরো error পড়ো, কারণ অনেক service এখন বলে দেয় কোন ধরনের policy request deny করেছে। *আসলে কোন principal* call করেছে সেটা নিশ্চিত হও (CloudTrail-এর `userIdentity`), কারণ ভুল credential খুবই common। তারপর evaluation chain ধরে এগোও: কোথাও explicit Deny আছে কি না (SCP/RCP, resource policy, identity policy, permissions boundary, session policy) → identity বা resource policy-তে Allow আছে কি না → SCP আর permissions boundary-ও allow করে কি না → KMS key policy → VPC endpoint policy। Fix test করো IAM policy simulator আর IAM Access Analyzer দিয়ে।
        """,
        quick_en=r"""Three causes: `s3:PutObject` is granted on the bucket ARN instead of `bucket/*`, the bucket policy's `StringNotEquals` Deny fires because the encryption header is missing, and the role lacks `kms:GenerateDataKey`. To debug, confirm the caller in CloudTrail, then check explicit Deny, Allow, SCPs/boundaries and the key policy.""",
        quick_bn=r"""তিনটা কারণ: `s3:PutObject` দেওয়া হয়েছে bucket ARN-এ, `bucket/*`-এ না; encryption header না থাকায় bucket policy-র `StringNotEquals` Deny লেগে যায়; আর role-এর `kms:GenerateDataKey` নেই। যেকোনো AccessDenied debug করতে আগে CloudTrail-এ আসল caller কে দেখো, তারপর explicit Deny, Allow, SCP/boundary আর key policy পরপর check করো।""",
        ex_en=r"""
            - **Evaluation order in one sentence:** default deny → any explicit Deny wins → otherwise you need an Allow, and every guardrail that applies (SCP, RCP, permissions boundary, session policy) must also allow the action.
            - **Same account vs cross-account:** in the same account, an Allow in *either* the identity policy or the resource policy is usually enough. Cross-account access needs an Allow on *both* sides.
            - **Why the old bucket policy pattern backfires:** "deny uploads without the encryption header" predates default encryption. Today S3 encrypts every new object by default, so that policy mainly breaks clients that rely on bucket defaults.
            - **Classic look-alikes:** the app runs with a different role than you think (local credentials, a wrong profile, a CI role), a typo in the bucket name, a request to the wrong Region, or a VPC endpoint policy that only allows certain buckets.
        """,
        ex_bn=r"""
            - **Evaluation-এর ক্রম এক বাক্যে:** default deny → কোথাও explicit Deny থাকলে সেটাই জেতে → না হলে Allow লাগবে, আর প্রযোজ্য প্রতিটা guardrail-কেও (SCP, RCP, permissions boundary, session policy) action-টা allow করতে হবে।
            - **একই account বনাম cross-account:** একই account-এ সাধারণত identity policy *অথবা* resource policy-র যেকোনো একটায় Allow থাকলেই চলে। Cross-account access-এ *দুই দিকেই* Allow লাগে।
            - **পুরনো bucket policy pattern কেন উল্টো ফল দেয়:** "encryption header ছাড়া upload deny" pattern-টা default encryption আসার আগের। এখন S3 প্রতিটা নতুন object default-এ encrypt করে, তাই এই policy মূলত bucket default-এর উপর নির্ভর করা client-দেরই ভেঙে দেয়।
            - **একই রকম দেখতে classic কারণ:** app তুমি যা ভাবছ তার চেয়ে আলাদা role-এ চলছে (local credential, ভুল profile, CI role), bucket name-এ typo, ভুল Region-এ request, বা এমন VPC endpoint policy যেটা শুধু নির্দিষ্ট bucket allow করে।
        """,
        tip_en=r"""Say the evaluation rule out loud first ("explicit deny wins, otherwise an allow is needed and every guardrail must agree"), then apply it to each policy in turn. Finding the KMS issue is usually the sign of real hands-on experience.""",
        tip_bn=r"""প্রথমে evaluation-এর নিয়মটা জোরে বলো ("explicit deny জেতে, নাহলে allow লাগবে আর প্রতিটা guardrail-কে রাজি হতে হবে"), তারপর একে একে প্রতিটা policy-তে প্রয়োগ করো। KMS-এর সমস্যাটা ধরতে পারা সাধারণত সত্যিকারের hands-on অভিজ্ঞতার লক্ষণ।""",
        mist_en=r"""Fixing it with `"Action": "s3:*", "Resource": "*"` (that still fails because of the explicit Deny and KMS), or assuming an Allow can override a Deny.""",
        mist_bn=r"""`"Action": "s3:*", "Resource": "*"` দিয়ে ঠিক করার চেষ্টা (explicit Deny আর KMS-এর কারণে তবুও fail করবে), বা ভাবা যে Allow দিয়ে Deny override করা যায়।""",
        extra=[
            dict(lang="json", label_en="Fixed identity policy", label_bn="সংশোধিত identity policy", src=r"""
                {
                  "Version": "2012-10-17",
                  "Statement": [
                    {
                      "Sid": "WriteReports",
                      "Effect": "Allow",
                      "Action": ["s3:PutObject", "s3:GetObject"],
                      "Resource": "arn:aws:s3:::acme-reports/*"
                    },
                    {
                      "Sid": "UseReportsKey",
                      "Effect": "Allow",
                      "Action": ["kms:GenerateDataKey", "kms:Decrypt"],
                      "Resource": "arn:aws:kms:ap-south-1:111122223333:key/1234abcd-12ab-34cd-56ef-1234567890ab"
                    }
                  ]
                }
            """),
            dict(lang="javascript", label_en="Upload that satisfies the bucket policy", label_bn="Bucket policy মেনে upload", src=r"""
                await s3.send(new PutObjectCommand({
                  Bucket: "acme-reports",
                  Key: key,
                  Body: pdf,
                  ContentType: "application/pdf",
                  ServerSideEncryption: "aws:kms",
                  SSEKMSKeyId: process.env.REPORTS_KMS_KEY_ARN,
                }));
            """),
        ],
        follow=[
            ("Your policy simulator says 'allowed' but the real call is denied. What could differ?", "Policy simulator বলছে 'allowed', কিন্তু আসল call deny হচ্ছে। কী কী আলাদা হতে পারে?"),
            ("How does cross-account S3 access change the evaluation?", "Cross-account S3 access-এ evaluation কীভাবে বদলায়?"),
        ],
        related=["aws-003", "aws-015", "aws-032"],
        refs=[IAM_EVAL, IAM_TS_DENIED, S3_SSE_KMS],
    ),
    # ------------------------------------------------------------------ aws-025
    Q(
        id="aws-025", sub="Lambda with RDS in a VPC", diff="hard", type="debugging",
        prio="high", market="both", mins=8,
        tags=["lambda", "rds-proxy", "vpc", "nat-gateway", "connections"],
        ver="AWS Lambda nodejs24.x; RDS Proxy; node-postgres (pg) 8.x", vs=True, status="stable",
        q_en=r"""This `nodejs24.x` Lambda function (attached to private subnets) reads an order from RDS PostgreSQL and fetches a rate from a third-party API. It worked in testing, but under production load many invocations hit the 30-second timeout, RDS reports connection exhaustion, and every call to the external API times out. What's wrong, and how do you fix it?""",
        q_bn=r"""এই `nodejs24.x` Lambda function (private subnet-এ attach করা) RDS PostgreSQL থেকে একটা order পড়ে আর একটা third-party API থেকে rate আনে। Testing-এ চলেছিল, কিন্তু production load-এ অনেক invocation 30 second timeout-এ পড়ছে, RDS connection শেষ হয়ে যাওয়ার কথা বলছে, আর external API-র প্রতিটা call timeout হচ্ছে। সমস্যা কী, আর কীভাবে ঠিক করবে?""",
        code=r"""
            // runtime: nodejs24.x — timeout 30 s — VPC: private subnets, security group sg-lambda
            import pg from "pg";

            export const handler = async (event) => {
              const client = new pg.Client({
                host: process.env.DB_HOST,
                user: "app",
                password: process.env.DB_PASSWORD,
                database: "shop",
              });
              await client.connect();

              const { rows } = await client.query(
                "SELECT * FROM orders WHERE id = " + event.pathParameters.id
              );

              const rate = await fetch("https://api.payments.example/rates").then((r) => r.json());

              return { statusCode: 200, body: JSON.stringify({ order: rows[0], rate }) };
            };
        """,
        lang="javascript",
        a_en=r"""
            1. **Connection leak and connection storm.** Each invocation opens a new connection and never closes it. Warm environments keep those sockets open while frozen, and at high concurrency hundreds of environments each hold connections until PostgreSQL's `max_connections` is exhausted. New `connect()` calls then hang until the Lambda timeout. Fix: create the pool **outside the handler** (reused per environment, `max: 1`), connect through **RDS Proxy** (pools and multiplexes connections, and makes failovers smoother), and cap concurrency with **reserved concurrency** so the database is protected.
            2. **No internet access from the VPC.** A Lambda function in a VPC has no public IP, so private subnets need a route to a **NAT Gateway** to reach external APIs. Attaching the function to a *public* subnet does **not** give it internet access. For AWS services, use VPC endpoints instead.
            3. **No client-side timeouts.** Without `connectionTimeoutMillis`, a `statement_timeout` and `AbortSignal.timeout()` on `fetch`, every stuck dependency burns the full 30 seconds. Fail fast and return a clear error. Remember that API Gateway's default integration timeout (29 s) is shorter than this function's timeout.
            4. **Also fix:** SQL injection through string concatenation (use `$1` parameters), the plain-text password (use Secrets Manager or RDS Proxy IAM authentication), and `SELECT *`.

            Also check the network path: the RDS security group must allow 5432 from `sg-lambda`. If it doesn't, *every* call times out, not just the ones under load.
        """,
        a_bn=r"""
            1. **Connection leak আর connection storm।** প্রতিটা invocation নতুন connection খোলে, কখনো বন্ধ করে না। Warm environment freeze থাকা অবস্থায়ও socket-গুলো খোলা রাখে, আর বেশি concurrency-তে শত শত environment connection ধরে রাখে, যতক্ষণ না PostgreSQL-এর `max_connections` শেষ হয়ে যায়। তখন নতুন `connect()` Lambda timeout পর্যন্ত ঝুলে থাকে। সমাধান: pool **handler-এর বাইরে** বানাও (প্রতি environment-এ reuse, `max: 1`), **RDS Proxy** দিয়ে connect করো (connection pool ও multiplex করে, failover-ও মসৃণ করে), আর database রক্ষা করতে **reserved concurrency** দিয়ে concurrency সীমিত করো।
            2. **VPC থেকে internet access নেই।** VPC-তে থাকা Lambda-র public IP থাকে না, তাই external API-তে পৌঁছাতে private subnet-এর **NAT Gateway** পর্যন্ত route লাগে। Function-কে *public* subnet-এ attach করলেও internet access **হয় না**। AWS service-এর জন্য বরং VPC endpoint ব্যবহার করো।
            3. **Client-side timeout নেই।** `connectionTimeoutMillis`, `statement_timeout` আর `fetch`-এ `AbortSignal.timeout()` না থাকলে প্রতিটা আটকে থাকা dependency পুরো 30 second খেয়ে ফেলে। দ্রুত fail করে পরিষ্কার error return করো। মনে রেখো, API Gateway-এর default integration timeout (29 s) এই function-এর timeout-এর চেয়ে কম।
            4. **আরও ঠিক করো:** string জোড়া দিয়ে SQL injection (`$1` parameter ব্যবহার করো), plain-text password (Secrets Manager বা RDS Proxy-র IAM authentication ব্যবহার করো), আর `SELECT *`।

            Network path-ও check করো: RDS security group-কে `sg-lambda` থেকে 5432 allow করতে হবে। না করলে শুধু load-এর সময় না, *প্রতিটা* call timeout হবে।
        """,
        quick_en=r"""Each invocation opens a DB connection and never closes it, exhausting RDS: create one pool outside the handler, use RDS Proxy and cap reserved concurrency. A Lambda in private subnets has no internet route, so add a NAT Gateway (VPC endpoints for AWS services), and set client timeouts so calls fail fast.""",
        quick_bn=r"""প্রতিটা invocation একটা DB connection খোলে আর বন্ধ করে না, ফলে RDS-এর connection শেষ হয়ে যায়: handler-এর বাইরে একটা pool বানাও, RDS Proxy ব্যবহার করো আর reserved concurrency দিয়ে cap দাও। Private subnet-এর Lambda-র internet route নেই, তাই NAT Gateway যোগ করো (AWS service-এর জন্য VPC endpoint), আর client timeout দাও যাতে call দ্রুত fail করে।""",
        ex_en=r"""
            - **Why testing didn't catch it:** with one or two warm environments, a few leaked connections are harmless. The bug only appears when concurrency multiplies the leak. Lambda scales out *environments*, and each one holds its own connection.
            - **How to diagnose:** RDS `DatabaseConnections` climbing in step with Lambda `ConcurrentExecutions`, Lambda `Duration` pinned at the timeout, and logs that stop right after `connect()` or `fetch()`. X-Ray or OpenTelemetry traces show which segment hangs.
            - **Idle sockets and freezing:** pool timers don't run while an environment is frozen, and the server may drop idle connections. RDS Proxy absorbs this, and `pg`'s pool discards the broken client and reconnects on the next query, as long as you attach a `pool.on("error")` listener (an unhandled `error` event crashes the process).
            - Since Node.js 24, Lambda only supports async (or sync) handlers. Callback-era tricks like `context.callbackWaitsForEmptyEventLoop = false` belong to callback handlers, which only work up to Node.js 22.
        """,
        ex_bn=r"""
            - **Testing-এ কেন ধরা পড়েনি:** এক-দুইটা warm environment-এ কয়েকটা leak হওয়া connection-এ ক্ষতি হয় না। Concurrency বাড়লে leak গুণ হয়, তখনই bug দেখা দেয়। Lambda *environment* বাড়িয়ে scale করে, আর প্রতিটা environment নিজের connection ধরে রাখে।
            - **কীভাবে diagnose করবে:** RDS-এর `DatabaseConnections` Lambda-র `ConcurrentExecutions`-এর সাথে তাল মিলিয়ে বাড়ছে, Lambda-র `Duration` timeout-এ আটকে আছে, আর log `connect()` বা `fetch()`-এর ঠিক পরেই থেমে যাচ্ছে। X-Ray বা OpenTelemetry trace দেখায় কোন segment ঝুলে আছে।
            - **Idle socket আর freeze:** environment freeze থাকা অবস্থায় pool-এর timer চলে না, আর server idle connection কেটে দিতে পারে। RDS Proxy এটা সামলে নেয়, আর `pg`-এর pool ভাঙা client বাদ দিয়ে পরের query-তে reconnect করে, তবে শর্ত হলো pool-এ একটা `pool.on("error")` listener থাকতে হবে (handle না করা `error` event process crash করায়)।
            - Node.js 24 থেকে Lambda শুধু async (বা sync) handler support করে। `context.callbackWaitsForEmptyEventLoop = false`-এর মতো callback যুগের কৌশল callback handler-এর জন্য, যেটা শুধু Node.js 22 পর্যন্ত চলে।
        """,
        tip_en=r"""Separate the symptoms: "DB timeouts under load" points to connection management (RDS Proxy), and "external API always times out" points to the network (NAT). Matching each symptom to a cause shows structured debugging.""",
        tip_bn=r"""Symptom-গুলো আলাদা করো: "load-এর সময় DB timeout" ইঙ্গিত করে connection management-এর দিকে (RDS Proxy), আর "external API সবসময় timeout" ইঙ্গিত করে network-এর দিকে (NAT)। প্রতিটা symptom-কে একটা কারণের সাথে মেলালে গোছানো debugging বোঝা যায়।""",
        mist_en=r"""Raising the Lambda timeout to 15 minutes, moving the function to a public subnet to "get internet", or adding `client.end()` while still opening a new connection on every request (it works, but connection setup and TLS cost every time and storms still happen).""",
        mist_bn=r"""Lambda timeout বাড়িয়ে ১৫ মিনিট করা, "internet পেতে" function-কে public subnet-এ সরানো, বা প্রতি request-এ নতুন connection খোলা চালু রেখে শুধু `client.end()` যোগ করা (কাজ করে, কিন্তু প্রতিবার connection setup আর TLS-এর খরচ লাগে, storm-ও থেকে যায়)।""",
        extra=[dict(lang="javascript", label_en="Fixed handler (via RDS Proxy, pool reused per environment)", label_bn="সংশোধিত handler (RDS Proxy দিয়ে, প্রতি environment-এ pool reuse)", src=r"""
            // runtime: nodejs24.x — private subnets with a NAT Gateway route; reserved concurrency set
            import pg from "pg";

            // Created once per execution environment and reused by warm invocations
            const pool = new pg.Pool({
              host: process.env.DB_PROXY_ENDPOINT,  // RDS Proxy endpoint, not the instance
              user: "app",
              password: process.env.DB_PASSWORD,    // better: Secrets Manager or an IAM auth token
              database: "shop",
              max: 1,                               // one connection per environment
              connectionTimeoutMillis: 3000,
              statement_timeout: 5000,
            });
            // An idle client can error while the environment is frozen; without a listener
            // the pool's 'error' event would crash the process
            pool.on("error", (err) => console.error("idle pg client error", err.message));

            export const handler = async (event) => {
              const id = Number(event.pathParameters?.id);
              if (!Number.isInteger(id)) return { statusCode: 400, body: "invalid id" };

              const { rows } = await pool.query(
                "SELECT id, status, total FROM orders WHERE id = $1",
                [id]
              );

              const res = await fetch("https://api.payments.example/rates", {
                signal: AbortSignal.timeout(3000),
              });
              const rate = await res.json();

              return { statusCode: 200, body: JSON.stringify({ order: rows[0] ?? null, rate }) };
            };
        """)],
        follow=[
            ("When does a Lambda function need to be in a VPC at all?", "Lambda function-কে আদৌ কখন VPC-তে রাখা দরকার?"),
            ("How does RDS Proxy behave during a Multi-AZ failover?", "Multi-AZ failover-এর সময় RDS Proxy কেমন আচরণ করে?"),
        ],
        related=["aws-010", "aws-017", "aws-018"],
        refs=[LAMBDA_VPC, RDS_PROXY, LAMBDA_CONCURRENCY],
    ),
    # ------------------------------------------------------------------ aws-026
    Q(
        id="aws-026", sub="Cost Optimization", diff="hard", type="scenario",
        prio="high", market="international", mins=10,
        tags=["cost-optimization", "nat-gateway", "data-transfer", "savings-plans", "cost-explorer"],
        ver="AWS cost management tools (2026); prices vary by Region — compare relatively", vs=False, status="stable",
        q_en=r"""Your startup's AWS bill roughly doubled in one month, but traffic didn't. How do you find the cause, fix it, and stop it from happening again?""",
        q_bn=r"""তোমার startup-এর AWS bill এক মাসে প্রায় দ্বিগুণ হয়ে গেছে, অথচ traffic বাড়েনি। কারণ কীভাবে খুঁজবে, কীভাবে ঠিক করবে, আর ভবিষ্যতে যেন আবার না হয় তার জন্য কী করবে?""",
        a_en=r"""
            **1. Find it, with data instead of guesses.** In **Cost Explorer**, compare month over month grouped by service, then by **usage type**, then by account or tag. Usage types like `NatGateway-Bytes`, `DataTransfer-Out-Bytes` or `DataTransfer-Regional-Bytes` (cross-AZ) jump out quickly. For line-item detail, query the Cost and Usage Report (Data Exports) with Athena. Turn on **Cost Anomaly Detection**. VPC Flow Logs show *which* resources are pushing traffic through the NAT.

            **2. Usual suspects and fixes:**
            - **NAT Gateway data processing:** private instances or containers pulling from S3/ECR or calling AWS APIs through NAT. Add **S3/DynamoDB gateway endpoints** (no extra charge), add interface endpoints for high-volume services like ECR and CloudWatch Logs, and keep one zonal NAT per AZ so traffic doesn't cross AZs.
            - **Data transfer:** internet egress (serve through CloudFront, compress, cache), chatty cross-AZ calls between services, unexpected cross-Region replication.
            - **Waste:** unattached EBS volumes, old snapshots and AMIs, idle load balancers, unused Elastic IPs (every public IPv4 address, in use or idle, has been charged hourly since February 2024), dev environments running 24/7, oversized instances (check AWS Compute Optimizer).
            - **Logs and metrics:** debug-level logging into CloudWatch Logs with no retention, and high-cardinality custom metrics.
            - **Storage:** S3 lifecycle rules or Intelligent-Tiering, expiring noncurrent versions and incomplete multipart uploads, and moving EBS from gp2 to gp3.

            **3. Structural savings:** Compute **Savings Plans** for the steady baseline (they apply across EC2, Fargate and Lambda), **Spot** for stateless, batch and CI workloads, and Graviton instances.

            **4. Prevent:** **AWS Budgets** with actual *and* forecasted alerts, anomaly alerts to Slack or email, mandatory cost-allocation tags, a monthly cost review, and guardrails (for example SCPs blocking very large instance types in sandbox accounts).
        """,
        a_bn=r"""
            **1. অনুমান না করে data দিয়ে খোঁজো।** **Cost Explorer**-এ মাসের সাথে মাস তুলনা করো: আগে service অনুযায়ী, তারপর **usage type** অনুযায়ী, তারপর account বা tag অনুযায়ী group করো। `NatGateway-Bytes`, `DataTransfer-Out-Bytes` বা `DataTransfer-Regional-Bytes` (cross-AZ)-এর মতো usage type দ্রুত চোখে পড়ে। Line-item পর্যায়ের detail-এর জন্য Cost and Usage Report (Data Exports) Athena দিয়ে query করো। **Cost Anomaly Detection** চালু করো। VPC Flow Logs দেখায় *কোন* resource NAT দিয়ে traffic পাঠাচ্ছে।

            **2. সাধারণ সন্দেহভাজন আর সমাধান:**
            - **NAT Gateway data processing:** private instance বা container NAT দিয়ে S3/ECR থেকে data টানছে বা AWS API call করছে। **S3/DynamoDB gateway endpoint** যোগ করো (বাড়তি খরচ নেই), ECR আর CloudWatch Logs-এর মতো বেশি volume-এর service-এর জন্য interface endpoint দাও, আর প্রতি AZ-এ একটা zonal NAT রাখো যাতে traffic AZ পার না হয়।
            - **Data transfer:** internet egress (CloudFront দিয়ে serve, compress, cache করো), service-গুলোর মধ্যে বেশি বেশি cross-AZ call, অপ্রত্যাশিত cross-Region replication।
            - **অপচয়:** কোথাও attach না থাকা EBS volume, পুরনো snapshot আর AMI, অলস load balancer, ব্যবহার না হওয়া Elastic IP (February 2024 থেকে প্রতিটা public IPv4 address-এর জন্য, ব্যবহার হোক বা না হোক, ঘণ্টা হিসেবে charge হয়), ২৪ ঘণ্টা চালু dev environment, বড় করে নেওয়া instance (AWS Compute Optimizer দেখো)।
            - **Log আর metric:** retention ছাড়া CloudWatch Logs-এ debug-level logging, আর high-cardinality custom metric।
            - **Storage:** S3 lifecycle rule বা Intelligent-Tiering, noncurrent version আর অসম্পূর্ণ multipart upload expire করা, আর EBS-কে gp2 থেকে gp3-তে নেওয়া।

            **3. কাঠামোগত সাশ্রয়:** স্থির baseline-এর জন্য Compute **Savings Plans** (EC2, Fargate আর Lambda সবখানে খাটে), stateless, batch আর CI workload-এর জন্য **Spot**, আর Graviton instance।

            **4. প্রতিরোধ:** actual *আর* forecasted দুই ধরনের alert-সহ **AWS Budgets**, Slack বা email-এ anomaly alert, বাধ্যতামূলক cost-allocation tag, মাসিক cost review, আর guardrail (যেমন sandbox account-এ খুব বড় instance type আটকাতে SCP)।
        """,
        quick_en=r"""Find the jump in Cost Explorer grouped by service, then usage type (often NAT Gateway bytes, data transfer, idle resources or logs), and fix it with gateway endpoints, cleanup, lifecycle rules and right-sizing. Prevent repeats with AWS Budgets, Cost Anomaly Detection, cost-allocation tags and Savings Plans for the baseline.""",
        quick_bn=r"""Cost Explorer-এ service, তারপর usage type দিয়ে group করে বাড়তি খরচটা খুঁজে বের করো (প্রায়ই NAT Gateway bytes, data transfer, অলস resource বা log), তারপর gateway endpoint, cleanup, lifecycle rule আর right-sizing দিয়ে ঠিক করো। আবার যেন না হয়, সেজন্য AWS Budgets, Cost Anomaly Detection, cost-allocation tag, আর baseline-এর জন্য Savings Plans রাখো।""",
        ex_en=r"""
            *Advanced material.* A typical real story: a new image-processing feature runs in ECS tasks in private subnets. Each task downloads originals from S3 and uploads thumbnails, so terabytes flow through the NAT Gateway, and every GB pays NAT processing. The traffic count didn't change, but the *bytes per request* did. One S3 gateway endpoint removes that whole line item, because EC2-to-S3 traffic in the same Region has no data transfer charge.

            - **Commit carefully:** size Savings Plans to the *minimum* steady usage of the last one to two months, not the average. Over-committing locks in waste.
            - **Spot needs design work:** handle the two-minute interruption notice, keep workloads stateless, and diversify across instance types and AZs.
            - **Unit economics** (cost per order or per active user) tell you whether spend is healthy as you grow. A rising bill with a flat cost per order is fine. A doubling cost per order isn't.
            - Don't quote prices from memory in an interview. They vary by Region and change over time. Explain the *cost drivers* and how you'd measure them.
        """,
        ex_bn=r"""
            *Advanced বিষয়।* একটা সাধারণ বাস্তব গল্প: নতুন image-processing feature private subnet-এর ECS task-এ চলে। প্রতিটা task S3 থেকে original download করে আর thumbnail upload করে, ফলে terabyte-এর পর terabyte NAT Gateway দিয়ে যায়, আর প্রতি GB-তে NAT processing charge লাগে। Traffic-এর সংখ্যা বদলায়নি, বদলেছে *প্রতি request-এ byte*। একটা S3 gateway endpoint দিলেই পুরো খরচের line-টা চলে যায়, কারণ একই Region-এ EC2 থেকে S3-এ traffic-এর কোনো data transfer charge নেই।

            - **সাবধানে commit করো:** Savings Plans-এর আকার ঠিক করো গত এক-দুই মাসের *সর্বনিম্ন* স্থির usage দেখে, গড় দেখে না। বেশি commit করলে অপচয় আটকে যায়।
            - **Spot-এর জন্য design লাগে:** দুই মিনিটের interruption notice সামলাতে হবে, workload stateless রাখতে হবে, আর একাধিক instance type ও AZ-এ ছড়িয়ে দিতে হবে।
            - **Unit economics** (প্রতি order বা প্রতি active user-এ খরচ) দেখায় বাড়ার সাথে সাথে খরচ সুস্থ আছে কি না। Bill বাড়ছে কিন্তু প্রতি order-এ খরচ স্থির থাকলে সমস্যা নেই। প্রতি order-এ খরচ দ্বিগুণ হলে সমস্যা।
            - Interview-তে মুখস্থ দাম বোলো না। দাম Region অনুযায়ী আলাদা আর সময়ের সাথে বদলায়। বরং *খরচের driver*-গুলো আর কীভাবে মাপবে সেটা ব্যাখ্যা করো।
        """,
        tip_en=r"""Use a clear structure: find (Cost Explorer by usage type) → fix (top three culprits) → commit (Savings Plans/Spot) → prevent (Budgets, anomaly alerts, tags). Telling the NAT Gateway story makes the answer memorable.""",
        tip_bn=r"""পরিষ্কার কাঠামো ব্যবহার করো: খোঁজা (usage type অনুযায়ী Cost Explorer) → ঠিক করা (প্রধান তিনটা কারণ) → commit (Savings Plans/Spot) → প্রতিরোধ (Budgets, anomaly alert, tag)। NAT Gateway-এর গল্পটা বললে উত্তরটা মনে রাখার মতো হয়।""",
        mist_en=r"""Jumping straight to "buy Reserved Instances" before finding the cause, deleting resources without checking ownership tags, or ignoring data transfer because "compute is the expensive part".""",
        mist_bn=r"""কারণ খোঁজার আগেই "Reserved Instances কিনে ফেলো" বলা, ownership tag না দেখে resource delete করা, বা "compute-ই তো দামি" ভেবে data transfer উপেক্ষা করা।""",
        code=r"""
            # Which usage types grew? Month-over-month, grouped by usage type
            aws ce get-cost-and-usage \
              --time-period Start=2026-08-01,End=2026-10-01 \
              --granularity MONTHLY \
              --metrics UnblendedCost \
              --group-by Type=DIMENSION,Key=USAGE_TYPE

            # Add an S3 gateway endpoint (no extra charge) to the private route tables
            aws ec2 create-vpc-endpoint \
              --vpc-id vpc-0abc1234567890def \
              --vpc-endpoint-type Gateway \
              --service-name com.amazonaws.ap-south-1.s3 \
              --route-table-ids rtb-0a1b2c3d4e5f60718 rtb-0f1e2d3c4b5a69788
        """,
        lang="bash",
        follow=[
            ("How would you decide the size of a Savings Plans commitment?", "Savings Plans commitment-এর আকার কীভাবে ঠিক করবে?"),
            ("Which workloads are good candidates for Spot, and which are not?", "কোন workload Spot-এর জন্য ভালো, আর কোনগুলো না?"),
        ],
        related=["aws-017", "aws-006", "aws-005"],
        refs=[CE, BUDGETS, VPC_PRICING],
    ),
]

if __name__ == "__main__":
    save("aws", "b4", QUESTIONS)
