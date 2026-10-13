# AWS batch 2 — aws-008 … aws-013 (security groups, SSH debugging, Lambda, Route 53, junior deployments)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

SG = ("Amazon VPC — Security groups", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html")
NACL = ("Amazon VPC — Network ACLs", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html")
SSH_TS = ("Amazon EC2 — Troubleshoot connecting to your instance", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html")
IGW = ("Amazon VPC — Internet gateways", "https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html")
SSM_SESSION = ("AWS Systems Manager — Session Manager", "https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html")
LAMBDA_WELCOME = ("AWS Lambda — What is AWS Lambda?", "https://docs.aws.amazon.com/lambda/latest/dg/welcome.html")
LAMBDA_RUNTIMES = ("AWS Lambda — Runtimes", "https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html")
LAMBDA_NODE_HANDLER = ("AWS Lambda — Define a Node.js function handler", "https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html")
R53_ALIAS = ("Route 53 — Choosing between alias and non-alias records", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-choosing-alias-non-alias.html")
R53_ROUTING = ("Route 53 — Choosing a routing policy", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html")
EC2_ROLES = ("Amazon EC2 — IAM roles for Amazon EC2", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html")
EIP = ("Amazon EC2 — Elastic IP addresses", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html")
R53_MIGRATE = ("Route 53 — Making Route 53 the DNS service for a domain that's in use", "https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/migrate-dns-domain-in-use.html")
CF_OAC = ("CloudFront — Restrict access to an Amazon S3 origin (OAC)", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html")
CF_EXPIRATION = ("CloudFront — Manage how long content stays in the cache", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html")
NEXT_STATIC = ("Next.js — Static Exports", "https://nextjs.org/docs/app/guides/static-exports")

QUESTIONS = [
    # ------------------------------------------------------------------ aws-008
    Q(
        id="aws-008", sub="Security Groups vs NACLs", diff="easy", type="comparison",
        prio="high", market="both", mins=3,
        tags=["vpc", "security-groups", "nacl", "networking", "firewall"],
        ver="Version-independent concept (Amazon VPC)", vs=False, status="stable",
        q_en=r"""What is the difference between a security group and a network ACL (NACL) in a VPC?""",
        q_bn=r"""VPC-তে security group আর network ACL (NACL)-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""
            - **Where they apply:** a security group attaches to network interfaces, so to instances, ALBs, RDS and so on. A NACL attaches to a subnet.
            - **State:** a security group is **stateful**. If inbound traffic is allowed, the response is automatically allowed back out. A NACL is **stateless**, so you need explicit rules in both directions, including the ephemeral port range (typically 1024–65535) for return traffic.
            - **Rule types:** security groups only have *allow* rules. NACLs have *allow* and *deny* rules, evaluated in rule-number order, and the first match wins.
            - **Defaults:** a new security group allows no inbound and all outbound traffic. The default NACL allows everything, but a newly created custom NACL denies everything until you add rules.

            In practice I do almost all filtering with security groups. For example, the ALB's group allows 443 from the internet, and the app servers' group allows port 3000 only from the ALB's security group. I use NACLs as a coarse extra layer, like blocking a known bad IP range for a whole subnet.
        """,
        a_bn=r"""
            - **কোথায় apply হয়:** security group network interface-এ attach হয়, মানে instance, ALB, RDS ইত্যাদিতে। NACL attach হয় subnet-এ।
            - **State:** security group **stateful**। Inbound traffic allow হলে তার response নিজে থেকেই বাইরে যেতে পারে। NACL **stateless**, তাই দুই দিকেই আলাদা rule লাগে, ফিরতি traffic-এর জন্য ephemeral port range (সাধারণত 1024–65535)-সহ।
            - **Rule-এর ধরন:** security group-এ শুধু *allow* rule থাকে। NACL-এ *allow* আর *deny* দুটোই থাকে; rule number অনুযায়ী ক্রমানুসারে evaluate হয়, প্রথম match-টাই কার্যকর।
            - **Default:** নতুন security group-এ কোনো inbound allow নেই, সব outbound allow। Default NACL সব allow করে, কিন্তু নতুন বানানো custom NACL rule যোগ না করা পর্যন্ত সব deny করে।

            বাস্তবে আমি প্রায় সব filtering security group দিয়েই করি। যেমন ALB-এর group internet থেকে 443 allow করে, আর app server-এর group port 3000 শুধু ALB-এর security group থেকে allow করে। NACL ব্যবহার করি বাড়তি একটা মোটা দাগের layer হিসেবে, যেমন পুরো subnet-এর জন্য পরিচিত কোনো খারাপ IP range block করা।
        """,
        ex_en=r"""
            - **Security groups can reference other security groups** ("allow 5432 from the app tier's SG"). That keeps rules correct as instances scale in and out, and NACLs can't do it.
            - A classic NACL bug: you allow inbound 443 but forget the outbound ephemeral range, so connections hang and time out. Because NACLs are stateless, return traffic is just another rule to write.
            - To *block* a specific IP you need a NACL deny rule or AWS WAF, because security groups can't deny.
            - Rule changes apply immediately to new connections, and you don't need to restart the instance.
        """,
        ex_bn=r"""
            - **Security group অন্য security group-কে reference করতে পারে** ("app tier-এর SG থেকে 5432 allow")। Instance বাড়লে বা কমলেও rule ঠিক থাকে। NACL এটা পারে না।
            - Classic NACL bug: inbound 443 allow করেছ কিন্তু outbound ephemeral range দাওনি, তাই connection ঝুলে থেকে timeout হয়। NACL stateless বলে ফিরতি traffic-এর জন্যও আলাদা rule লিখতে হয়।
            - নির্দিষ্ট কোনো IP *block* করতে NACL-এর deny rule বা AWS WAF লাগে, কারণ security group deny করতে পারে না।
            - Rule পরিবর্তন নতুন connection-এ সাথে সাথে কার্যকর হয়, instance restart করতে হয় না।
        """,
        tip_en=r"""Structure it as four rows: scope, state, rule types, defaults. Then give the "ALB SG → app SG" example. An answer laid out like a table is easy for an interviewer to follow.""",
        tip_bn=r"""চারটা row ধরে বলো: scope, state, rule-এর ধরন, default। তারপর "ALB SG → app SG" উদাহরণটা দাও। Table-এর মতো সাজানো উত্তর interviewer-এর জন্য বোঝা সহজ।""",
        mist_en=r"""Saying security groups are stateless, trying to add a "deny" rule to a security group, or opening the app port (3000) to `0.0.0.0/0` instead of to the load balancer's security group.""",
        mist_bn=r"""Security group-কে stateless বলা, security group-এ "deny" rule দেওয়ার চেষ্টা করা, বা app port (3000) load balancer-এর security group-এর বদলে `0.0.0.0/0`-এর জন্য খুলে দেওয়া।""",
        code=r"""
            # Allow port 3000 on the app servers only from the load balancer's security group
            aws ec2 authorize-security-group-ingress \
              --group-id sg-0app1234567890abc \
              --protocol tcp --port 3000 \
              --source-group sg-0alb1234567890abc
        """,
        lang="bash",
        follow=[
            ("Why do NACL rules need the ephemeral port range for outbound traffic?", "NACL-এর outbound rule-এ ephemeral port range কেন লাগে?"),
            ("How would you block a single abusive IP address hitting your ALB?", "তোমার ALB-তে আঘাত করা একটা abusive IP address কীভাবে block করবে?"),
        ],
        related=["aws-009", "aws-017"],
        refs=[SG, NACL],
    ),
    # ------------------------------------------------------------------ aws-009
    Q(
        id="aws-009", sub="EC2 Connectivity Troubleshooting", diff="easy", type="debugging",
        prio="high", market="both", mins=4,
        tags=["ec2", "ssh", "security-groups", "route-tables", "troubleshooting"],
        ver="Amazon EC2 (Amazon Linux 2023)", vs=False, status="stable",
        q_en=r"""You launched an Amazon Linux 2023 instance in a new VPC, but SSH fails as shown below. What is wrong, and how do you fix it?""",
        q_bn=r"""নতুন একটা VPC-তে Amazon Linux 2023 instance launch করেছ, কিন্তু নিচের মতো SSH fail করছে। সমস্যা কী, আর কীভাবে ঠিক করবে?""",
        code=r"""
            $ ssh -i mykey.pem ec2-user@203.0.113.25
            ssh: connect to host 203.0.113.25 port 22: Connection timed out

            Instance:          t3.micro, Amazon Linux 2023, state = running, all status checks passed
            Public IPv4:       203.0.113.25
            Subnet route table:
              Destination      Target
              10.0.0.0/16      local
            Security group (inbound):
              TCP 3000         0.0.0.0/0
        """,
        lang="text",
        a_en=r"""
            "Connection timed out" means packets never get an answer. That's a network-path problem, not a key problem. There are two bugs here:
            1. **The subnet isn't public.** Its route table only has the `local` route, with no `0.0.0.0/0 → Internet Gateway` route. A public IP alone isn't enough, because return traffic has no path to the internet. Fix: attach an IGW to the VPC and add the default route.
            2. **The security group doesn't allow port 22.** Only 3000 is open (to the whole world, which is also bad). Fix: allow TCP 22 from *my own IP* (`/32`), not from `0.0.0.0/0`, and close 3000 or restrict it to the load balancer.

            If there's a custom NACL, check that it allows inbound 22 and outbound ephemeral ports. Even better, skip port 22 altogether and use **SSM Session Manager** or EC2 Instance Connect.
        """,
        a_bn=r"""
            "Connection timed out" মানে packet-এর কোনো উত্তর আসছে না। এটা network path-এর সমস্যা, key-এর না। এখানে দুইটা bug আছে:
            1. **Subnet-টা public না।** Route table-এ শুধু `local` route আছে, `0.0.0.0/0 → Internet Gateway` route নেই। শুধু public IP থাকলেই হয় না, কারণ ফিরতি traffic-এর internet-এ যাওয়ার পথ নেই। সমাধান: VPC-তে IGW attach করে default route যোগ করো।
            2. **Security group-এ port 22 allow করা নেই।** শুধু 3000 খোলা (তাও সারা দুনিয়ার জন্য, যেটা নিজেই খারাপ)। সমাধান: TCP 22 শুধু *নিজের IP* (`/32`) থেকে allow করো, `0.0.0.0/0` থেকে না; আর 3000 বন্ধ করো বা শুধু load balancer-এর জন্য রাখো।

            Custom NACL থাকলে দেখো inbound 22 আর outbound ephemeral port allow আছে কি না। আরও ভালো হয় port 22 একদম না খুলে **SSM Session Manager** বা EC2 Instance Connect ব্যবহার করলে।
        """,
        ex_en=r"""
            The error message tells you where to look:
            - **`Connection timed out`**: packets are dropped. Check the security group, NACL, route table / IGW, whether the instance has a public IP, or whether your own network blocks outbound port 22.
            - **`Connection refused`**: you reached the host, but nothing is listening on port 22 (sshd stopped, wrong port).
            - **`Permission denied (publickey)`**: networking is fine. The key pair or the username is wrong (`ec2-user` on Amazon Linux, `ubuntu` on Ubuntu).
            - **`UNPROTECTED PRIVATE KEY FILE`**: run `chmod 400 mykey.pem`.

            The VPC Reachability Analyzer can trace the path and point to the exact blocking component.
        """,
        ex_bn=r"""
            Error message-ই বলে দেয় কোথায় খুঁজতে হবে:
            - **`Connection timed out`**: packet drop হচ্ছে। Security group, NACL, route table / IGW, instance-এর public IP আছে কি না, আর তোমার নিজের network outbound port 22 block করছে কি না দেখো।
            - **`Connection refused`**: host পর্যন্ত পৌঁছেছ, কিন্তু port 22-এ কেউ listen করছে না (sshd বন্ধ, ভুল port)।
            - **`Permission denied (publickey)`**: network ঠিক আছে; key pair বা username ভুল (Amazon Linux-এ `ec2-user`, Ubuntu-তে `ubuntu`)।
            - **`UNPROTECTED PRIVATE KEY FILE`**: `chmod 400 mykey.pem` চালাও।

            VPC Reachability Analyzer পুরো path trace করে ঠিক কোন component block করছে তা দেখিয়ে দিতে পারে।
        """,
        tip_en=r"""Start by classifying the error (timeout vs refused vs permission denied), then walk outward: SG → NACL → route table/IGW → public IP. A systematic order impresses more than guessing.""",
        tip_bn=r"""প্রথমে error-টা শ্রেণিবদ্ধ করো (timeout, refused, নাকি permission denied), তারপর ধাপে ধাপে বাইরের দিকে যাও: SG → NACL → route table/IGW → public IP। অনুমানের চেয়ে এমন গোছানো ক্রম অনেক বেশি impress করে।""",
        mist_en=r"""Regenerating the key pair for a timeout error, or "fixing" it by opening all ports to `0.0.0.0/0`.""",
        mist_bn=r"""Timeout error-এর জন্য key pair নতুন করে বানানো, বা সব port `0.0.0.0/0`-এর জন্য খুলে দিয়ে "ঠিক" করা।""",
        extra=[dict(lang="bash", label_en="Fix", label_bn="সমাধান", src=r"""
            # 1. Make the subnet public: default route to the VPC's Internet Gateway
            aws ec2 create-route --route-table-id rtb-0abc1234567890def \
              --destination-cidr-block 0.0.0.0/0 --gateway-id igw-0def1234567890abc

            # 2. Allow SSH only from your own public IP
            aws ec2 authorize-security-group-ingress --group-id sg-0123456789abcdef0 \
              --protocol tcp --port 22 --cidr 198.51.100.7/32

            # 3. Correct key permissions and default user, then connect
            chmod 400 mykey.pem
            ssh -i mykey.pem ec2-user@203.0.113.25

            # Better: no port 22 at all (needs the SSM agent + an instance role with AmazonSSMManagedInstanceCore)
            aws ssm start-session --target i-0123456789abcdef0
        """)],
        follow=[
            ("What would `Permission denied (publickey)` tell you instead?", "এর বদলে `Permission denied (publickey)` এলে সেটা কী বোঝাত?"),
            ("How does Session Manager let you connect without opening port 22?", "Port 22 না খুলে Session Manager কীভাবে connect করতে দেয়?"),
        ],
        related=["aws-008", "aws-017"],
        refs=[SSH_TS, IGW, SSM_SESSION],
    ),
    # ------------------------------------------------------------------ aws-010
    Q(
        id="aws-010", sub="Lambda Fundamentals", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["lambda", "serverless", "cold-start", "nodejs24", "concurrency"],
        ver="AWS Lambda (nodejs24.x GA; nodejs26.x preview — 2026)", vs=True, status="stable",
        q_en=r"""What is AWS Lambda, and what are its key characteristics and limits (Node.js runtimes, timeout, memory, cold starts, concurrency)?""",
        q_bn=r"""AWS Lambda কী? এর মূল বৈশিষ্ট্য আর limit-গুলো কী (Node.js runtime, timeout, memory, cold start, concurrency)?""",
        a_en=r"""
            Lambda runs your function in response to events, and you never manage servers. You pay per request and per unit of compute time (GB-seconds). Typical event sources are API Gateway or function URLs, S3 events, SQS, SNS, EventBridge (including schedules), DynamoDB Streams and Kinesis.

            Key facts:
            - **Maximum timeout is 15 minutes.** Memory goes from 128 MB to **10,240 MB (10 GB)**, and CPU scales with the memory you allocate.
            - **Node.js runtimes:** `nodejs24.x` is the current GA runtime and `nodejs22.x` is still supported. `nodejs26.x` is in public preview, so I don't use it in production yet. From Node.js 24 on, handlers must be `async` (or plain synchronous); callback-style handlers only work up to Node.js 22.
            - **Cold start:** when no warm execution environment is free, Lambda creates one, loads your code and runs the init code outside the handler, which adds latency. Warm invocations reuse the environment, so I create SDK clients and DB pools *outside* the handler.
            - **Concurrency:** each in-flight request needs its own environment, and there's a regional account-level quota. *Reserved concurrency* guarantees and caps a function's share. *Provisioned concurrency* keeps environments pre-initialised to remove cold starts for latency-sensitive paths.
        """,
        a_bn=r"""
            Lambda event-এর response-এ তোমার function চালায়, server manage করতে হয় না। প্রতি request আর compute সময়ের (GB-second) হিসাবে টাকা দিতে হয়। সাধারণ event source: API Gateway বা function URL, S3 event, SQS, SNS, EventBridge (schedule-সহ), DynamoDB Streams, Kinesis।

            মূল তথ্য:
            - **সর্বোচ্চ timeout ১৫ মিনিট।** Memory 128 MB থেকে **10,240 MB (10 GB)** পর্যন্ত, আর যত memory দাও CPU-ও সেই অনুপাতে বাড়ে।
            - **Node.js runtime:** `nodejs24.x` বর্তমান GA runtime, `nodejs22.x`-ও এখনো supported। `nodejs26.x` public preview-তে আছে, তাই production-এ এখনো ব্যবহার করি না। Node.js 24 থেকে handler হতে হবে `async` (বা সাধারণ synchronous); callback-style handler শুধু Node.js 22 পর্যন্ত চলে।
            - **Cold start:** কোনো warm execution environment খালি না থাকলে Lambda নতুন একটা বানায়, code load করে, handler-এর বাইরের init code চালায়, ফলে latency বাড়ে। Warm invocation-এ environment reuse হয়, তাই SDK client আর DB pool আমি handler-এর *বাইরে* তৈরি করি।
            - **Concurrency:** চলমান প্রতিটা request-এর জন্য আলাদা environment লাগে, আর account-এর regional quota আছে। *Reserved concurrency* একটা function-এর ভাগ নিশ্চিত করে, আবার সর্বোচ্চ সীমাও বেঁধে দেয়। *Provisioned concurrency* environment আগে থেকে initialise করে রাখে, ফলে latency-sensitive path-এ cold start থাকে না।
        """,
        ex_en=r"""
            - **When Lambda is a poor fit:** jobs longer than 15 minutes, steady high-throughput traffic (containers often cost less), workloads that need persistent connections or local state, or opening many direct connections to RDS (use RDS Proxy).
            - Synchronous invocations have a 6 MB request/response payload limit, so for large files hand the client a presigned S3 URL instead.
            - `/tmp` is ephemeral scratch space (512 MB by default, configurable up to 10 GB). It is not shared between environments and is not durable.
            - Lambda delivers events at least once for most async sources, so handlers that change data should be idempotent.
        """,
        ex_bn=r"""
            - **কখন Lambda ভালো choice না:** ১৫ মিনিটের বেশি সময়ের job, সারাক্ষণ বেশি throughput-এর traffic (container প্রায়ই সস্তা পড়ে), persistent connection বা local state লাগে এমন workload, বা RDS-এ সরাসরি অনেক connection খোলা (RDS Proxy ব্যবহার করো)।
            - Synchronous invocation-এ request/response payload-এর limit 6 MB, তাই বড় file-এর জন্য client-কে presigned S3 URL দাও।
            - `/tmp` সাময়িক scratch space (default 512 MB, 10 GB পর্যন্ত বাড়ানো যায়)। এটা environment-গুলোর মধ্যে shared না, আর durable-ও না।
            - বেশিরভাগ async source-এ Lambda event অন্তত একবার (at least once) deliver করে, তাই data পরিবর্তন করে এমন handler idempotent হওয়া উচিত।
        """,
        tip_en=r"""Quote the hard limits correctly (15 minutes, 10 GB) and name the current runtime (`nodejs24.x`). Then explain cold starts with the "init outside the handler" trick. Precise numbers build credibility.""",
        tip_bn=r"""Hard limit-গুলো ঠিকভাবে বলো (১৫ মিনিট, 10 GB) আর বর্তমান runtime-এর নাম বলো (`nodejs24.x`)। তারপর "handler-এর বাইরে init" কৌশল দিয়ে cold start ব্যাখ্যা করো। সঠিক সংখ্যা বললে বিশ্বাসযোগ্যতা বাড়ে।""",
        mist_en=r"""Saying the timeout is 5 minutes (an old limit), writing callback-style handlers on `nodejs24.x`, or creating a new DB connection inside every invocation.""",
        mist_bn=r"""Timeout ৫ মিনিট বলা (পুরনো limit), `nodejs24.x`-এ callback-style handler লেখা, বা প্রতিটা invocation-এর ভেতরে নতুন DB connection তৈরি করা।""",
        code=r"""
            // index.mjs — runtime: nodejs24.x
            import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";

            // Runs once per execution environment (during the cold start), then reused
            const s3 = new S3Client({});

            export const handler = async (event) => {
              const { bucket, key } = event;
              const res = await s3.send(new GetObjectCommand({ Bucket: bucket, Key: key }));
              const text = await res.Body.transformToString();
              return { statusCode: 200, body: JSON.stringify({ length: text.length }) };
            };
        """,
        lang="javascript",
        follow=[
            ("What is the difference between reserved and provisioned concurrency?", "Reserved আর provisioned concurrency-র পার্থক্য কী?"),
            ("How would you reduce cold-start latency for a Node.js function?", "Node.js function-এর cold-start latency কীভাবে কমাবে?"),
        ],
        related=["aws-025", "aws-031"],
        refs=[LAMBDA_WELCOME, LAMBDA_RUNTIMES, LAMBDA_NODE_HANDLER],
    ),
    # ------------------------------------------------------------------ aws-011
    Q(
        id="aws-011", sub="Route 53 Records & Routing Policies", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["route53", "dns", "alias-record", "alb", "routing-policy"],
        ver="Version-independent concept (Amazon Route 53)", vs=False, status="stable",
        q_en=r"""You want both `example.com` (the apex/root domain) and `www.example.com` to point to your Application Load Balancer. Which Route 53 setup is correct?""",
        q_bn=r"""`example.com` (apex/root domain) আর `www.example.com` দুটোই তোমার Application Load Balancer-এ point করাতে চাও। Route 53-এ কোন setup সঠিক?""",
        options=[
            ("A CNAME record for `example.com` pointing to the ALB's DNS name",
             "`example.com`-এর জন্য ALB-এর DNS name-এ point করা একটা CNAME record"),
            ("An A record for `example.com` containing the ALB's current IP addresses",
             "`example.com`-এর জন্য ALB-এর বর্তমান IP address-গুলো দিয়ে একটা A record"),
            ("Alias A (and AAAA) records for `example.com` and `www.example.com` that target the ALB",
             "`example.com` আর `www.example.com` দুটোর জন্যই ALB-কে target করা Alias A (ও AAAA) record"),
            ("Only a CNAME for `www.example.com`, because an apex domain cannot point to an AWS load balancer",
             "শুধু `www.example.com`-এর জন্য একটা CNAME, কারণ apex domain AWS load balancer-এ point করানো যায় না"),
        ],
        correct=2,
        a_en=r"""
            Option 3. An **alias record** is a Route 53 extension that points a name at an AWS resource (ALB, CloudFront, API Gateway, an S3 website endpoint, and others). Route 53 answers with the resource's *current* IPs. Unlike a CNAME, an alias works at the zone apex. Alias queries to AWS resources are free, and an alias can evaluate the target's health.
        """,
        a_bn=r"""
            Option 3। **Alias record** হলো Route 53-এর একটা extension, যেটা একটা name-কে AWS resource-এ (ALB, CloudFront, API Gateway, S3 website endpoint ইত্যাদি) point করায়। Route 53 resource-এর *বর্তমান* IP দিয়ে উত্তর দেয়। CNAME-এর মতো না, alias zone apex-এও কাজ করে। AWS resource-এর জন্য alias query-তে টাকা লাগে না, আর alias target-এর health-ও evaluate করতে পারে।
        """,
        ex_en=r"""
            - **Option 1 is the tempting one.** It works for `www`, but the DNS standard doesn't allow a CNAME at the zone apex, because it would conflict with the SOA and NS records there.
            - Option 2 breaks silently. ALB IP addresses change over time, so hardcoded IPs eventually point to nothing.
            - Option 4 is a misconception that alias records exist to solve.
            - Records can use **routing policies**: simple, weighted (canary or A/B splits), latency-based (send users to the closest Region), failover (with health checks, for DR), geolocation, geoproximity, multivalue answer and IP-based.
        """,
        ex_bn=r"""
            - **Option 1-টাই আকর্ষণীয়।** `www`-এর জন্য এটা কাজ করে, কিন্তু DNS standard zone apex-এ CNAME রাখতে দেয় না, কারণ সেখানকার SOA আর NS record-এর সাথে conflict হয়।
            - Option 2 নিঃশব্দে ভেঙে যায়। ALB-এর IP address সময়ের সাথে বদলায়, তাই hardcode করা IP একসময় ভুল জায়গায় point করে।
            - Option 4 একটা ভুল ধারণা, আর ঠিক এই সমস্যা সমাধানের জন্যই alias record আছে।
            - Record-এ **routing policy** ব্যবহার করা যায়: simple, weighted (canary বা A/B split), latency-based (user-কে সবচেয়ে কাছের Region-এ পাঠানো), failover (health check-সহ, DR-এর জন্য), geolocation, geoproximity, multivalue answer আর IP-based।
        """,
        tip_en=r"""Explain *why* a CNAME can't sit at the apex (it would clash with SOA/NS records). Then name two or three routing policies with a use case each, like weighted for canary and failover for DR.""",
        tip_bn=r"""Apex-এ CNAME কেন রাখা যায় না সেটা ব্যাখ্যা করো (SOA/NS record-এর সাথে conflict হয়)। তারপর দুই-তিনটা routing policy-র নাম use case-সহ বলো, যেমন canary-র জন্য weighted, DR-এর জন্য failover।""",
        related=["aws-012", "aws-020"],
        refs=[R53_ALIAS, R53_ROUTING],
    ),
    # ------------------------------------------------------------------ aws-012
    Q(
        id="aws-012", sub="Deploying Node.js on EC2", diff="medium", type="scenario",
        prio="high", market="bangladesh", mins=8,
        tags=["ec2", "nginx", "pm2", "route53", "deployment"],
        ver="Amazon Linux 2023 / Ubuntu LTS, Node.js 24 LTS, NGINX 1.30, PM2", vs=True, status="stable",
        q_en=r"""Walk me through deploying an Express (Node.js) API to a single EC2 instance with NGINX as a reverse proxy, PM2 (or systemd) as the process manager, HTTPS, and a custom domain managed in Route 53.""",
        q_bn=r"""একটা Express (Node.js) API একটা EC2 instance-এ deploy করার পুরো ধাপগুলো বলো: reverse proxy হিসেবে NGINX, process manager হিসেবে PM2 (বা systemd), HTTPS, আর Route 53-এ manage করা custom domain।""",
        a_en=r"""
            1. **Launch:** an Amazon Linux 2023 or Ubuntu LTS instance (a small `t3`/`t4g` is fine to start) in a public subnet. Attach an **IAM role** (instance profile) instead of access keys, and allocate an **Elastic IP** so the address survives stop/start.
            2. **Security group:** 80 and 443 from anywhere, and 22 only from my IP (or no 22 at all, using SSM Session Manager). Port 3000 stays **closed** to the internet.
            3. **Install:** Node.js 24 LTS (NodeSource, nvm or official binaries), NGINX and git. Clone, build, and run `npm ci --omit=dev`.
            4. **Config and secrets:** read from SSM Parameter Store / Secrets Manager at startup instead of committing a `.env` file. The app listens on `127.0.0.1:3000`.
            5. **Process manager:** `pm2 start ecosystem.config.cjs`, then `pm2 startup` + `pm2 save` so it comes back after a reboot. Alternatively, write a systemd unit with `Restart=always`.
            6. **NGINX:** a server block with `server_name api.example.com` and `proxy_pass http://127.0.0.1:3000` plus the forwarding headers. Check with `nginx -t`, then reload.
            7. **DNS:** in the Route 53 hosted zone, an A record `api.example.com` → the Elastic IP. If the domain was bought elsewhere, point the registrar's nameservers to the hosted zone's four NS records.
            8. **HTTPS:** Let's Encrypt with `certbot --nginx` (with auto-renewal), or put an ALB in front with a free ACM certificate.
            9. **Operate:** CloudWatch agent for logs and memory metrics, log rotation, alarms, and EBS snapshots through AWS Backup.
        """,
        a_bn=r"""
            1. **Launch:** public subnet-এ একটা Amazon Linux 2023 বা Ubuntu LTS instance (শুরুতে ছোট `t3`/`t4g`-ই যথেষ্ট)। Access key-এর বদলে **IAM role** (instance profile) attach করো, আর stop/start-এর পরেও address যেন না বদলায় সেজন্য **Elastic IP** নাও।
            2. **Security group:** 80 আর 443 সবার জন্য খোলা, 22 শুধু আমার IP থেকে (বা SSM Session Manager ব্যবহার করে 22 একদমই না খোলা)। Port 3000 internet-এর জন্য **বন্ধ** থাকবে।
            3. **Install:** Node.js 24 LTS (NodeSource, nvm বা official binary), NGINX, git। তারপর clone, build, আর `npm ci --omit=dev`।
            4. **Config আর secret:** `.env` file commit না করে startup-এ SSM Parameter Store / Secrets Manager থেকে পড়ো। App শুনবে `127.0.0.1:3000`-এ।
            5. **Process manager:** `pm2 start ecosystem.config.cjs`, তারপর `pm2 startup` + `pm2 save`, যাতে reboot-এর পরে app আবার চালু হয়। বিকল্প হিসেবে `Restart=always`-সহ systemd unit লেখা যায়।
            6. **NGINX:** `server_name api.example.com` আর `proxy_pass http://127.0.0.1:3000`-সহ forwarding header দিয়ে server block। `nginx -t` দিয়ে check করে reload করো।
            7. **DNS:** Route 53 hosted zone-এ `api.example.com` → Elastic IP একটা A record। Domain অন্য কোথাও থেকে কেনা হলে registrar-এর nameserver hosted zone-এর চারটা NS record-এ বদলে দাও।
            8. **HTTPS:** `certbot --nginx` দিয়ে Let's Encrypt (auto-renewal-সহ), অথবা সামনে ALB বসিয়ে free ACM certificate।
            9. **চালানো:** log আর memory metric-এর জন্য CloudWatch agent, log rotation, alarm, আর AWS Backup দিয়ে EBS snapshot।
        """,
        ex_en=r"""
            - **Why NGINX in front of Node:** TLS termination, gzip, static files, request size limits and buffering of slow clients. Node also stays on an unprivileged port as a non-root user.
            - Set `app.set('trust proxy', 1)` in Express so `req.ip` and `req.protocol` reflect the real client behind NGINX. Rate limiters and secure cookies depend on this.
            - PM2 cluster mode (`instances: "max"`) uses all vCPUs, and `pm2 reload` restarts workers one at a time for near-zero-downtime updates.
            - **Trade-off:** a single instance is a single point of failure. The next steps are an ALB with an Auto Scaling group across two AZs (or ECS on Fargate), RDS instead of a database on the same box, and CI/CD through GitHub Actions with an OIDC role instead of stored keys.
        """,
        ex_bn=r"""
            - **Node-এর সামনে NGINX কেন:** TLS termination, gzip, static file, request size limit আর ধীর client-এর buffering সামলায়। Node-ও non-root user হিসেবে unprivileged port-এ থাকতে পারে।
            - Express-এ `app.set('trust proxy', 1)` দাও, যাতে NGINX-এর পেছনেও `req.ip` আর `req.protocol` আসল client-এর মান দেখায়। Rate limiter আর secure cookie এর উপর নির্ভর করে।
            - PM2 cluster mode (`instances: "max"`) সব vCPU ব্যবহার করে, আর `pm2 reload` worker-গুলো একটা একটা করে restart করে, ফলে update-এ downtime প্রায় শূন্য থাকে।
            - **Trade-off:** একটা instance মানে single point of failure। পরের ধাপ: দুইটা AZ জুড়ে ALB + Auto Scaling group (বা Fargate-এ ECS), একই server-এ database না রেখে RDS, আর key জমা না রেখে OIDC role দিয়ে GitHub Actions-এ CI/CD।
        """,
        tip_en=r"""Present it as numbered steps from network to process to DNS to TLS. Then volunteer the weaknesses of the single-instance setup and how you'd evolve it. That shows you think beyond "it works".""",
        tip_bn=r"""Network → process → DNS → TLS, এই ক্রমে নম্বর দিয়ে ধাপগুলো বলো। তারপর নিজে থেকেই single-instance setup-এর দুর্বলতা আর কীভাবে এটাকে উন্নত করবে সেটা বলো। এতে বোঝা যায় তুমি "চলছে তো" পর্যন্ত থেমে থাকো না।""",
        mist_en=r"""Opening port 3000 to the world and skipping NGINX, running Node as root on port 80, putting AWS access keys in `.env`, or forgetting `pm2 startup` so the app is gone after a reboot.""",
        mist_bn=r"""Port 3000 সবার জন্য খুলে NGINX বাদ দেওয়া, port 80-তে root হিসেবে Node চালানো, `.env`-এ AWS access key রাখা, বা `pm2 startup` ভুলে যাওয়া, যার ফলে reboot-এর পরে app আর চলে না।""",
        code=r"""
            # /etc/nginx/conf.d/api.conf  (certbot --nginx later adds the 443/TLS block)
            server {
                listen 80;
                server_name api.example.com;

                location / {
                    proxy_pass http://127.0.0.1:3000;
                    proxy_http_version 1.1;
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;
                }
            }
        """,
        lang="nginx",
        extra=[
            dict(lang="javascript", label_en="ecosystem.config.cjs (PM2)", label_bn="ecosystem.config.cjs (PM2)", src=r"""
                module.exports = {
                  apps: [
                    {
                      name: "api",
                      script: "dist/server.js",
                      instances: "max",      // one worker per vCPU
                      exec_mode: "cluster",
                      env: { NODE_ENV: "production", PORT: 3000 },
                    },
                  ],
                };
            """),
            dict(lang="bash", label_en="Start, persist across reboots, enable HTTPS", label_bn="Start, reboot-এর পরেও চালু রাখা, HTTPS চালু করা", src=r"""
                pm2 start ecosystem.config.cjs
                pm2 save
                pm2 startup systemd          # prints a command to run with sudo
                sudo nginx -t && sudo systemctl reload nginx
                sudo certbot --nginx -d api.example.com
            """),
        ],
        follow=[
            ("How would you deploy a new version with zero downtime on this setup?", "এই setup-এ zero downtime-এ নতুন version কীভাবে deploy করবে?"),
            ("What changes when you add a second instance behind a load balancer?", "Load balancer-এর পেছনে দ্বিতীয় instance যোগ করলে কী কী বদলাতে হবে?"),
        ],
        related=["aws-005", "aws-016", "aws-020", "aws-023"],
        refs=[EC2_ROLES, EIP, R53_MIGRATE],
    ),
    # ------------------------------------------------------------------ aws-013
    Q(
        id="aws-013", sub="S3 + CloudFront Static Hosting", diff="medium", type="scenario",
        prio="high", market="both", mins=7,
        tags=["s3", "cloudfront", "oac", "spa", "nextjs-export"],
        ver="Amazon S3 + CloudFront (OAC); Next.js 16.4 static export; Vite 8", vs=True, status="stable",
        q_en=r"""How would you host a React (Vite) SPA or a Next.js static export (`output: 'export'`) on S3 and CloudFront with HTTPS and a custom domain? How do you handle client-side routes like `/dashboard` and deep links like `/about`?""",
        q_bn=r"""একটা React (Vite) SPA বা Next.js static export (`output: 'export'`) HTTPS আর custom domain-সহ S3 + CloudFront-এ কীভাবে host করবে? `/dashboard`-এর মতো client-side route আর `/about`-এর মতো deep link কীভাবে সামলাবে?""",
        a_en=r"""
            1. **Build:** `vite build` produces `dist/`. Next.js with `output: 'export'` produces `out/`, which only works for static features: no SSR, no Server Actions, no ISR, and no default image optimisation.
            2. **Private bucket:** keep Block Public Access on and upload with `aws s3 sync`.
            3. **CloudFront + OAC:** use the bucket's **REST endpoint** as the origin with **Origin Access Control**. The bucket policy allows only the `cloudfront.amazonaws.com` service principal, with `AWS:SourceArn` set to this distribution. OAI is the legacy approach, and S3 *website* endpoints are HTTP-only and can't use OAC.
            4. **HTTPS and domain:** request an ACM certificate in **us-east-1** (CloudFront requires that Region), add the alternate domain name, redirect HTTP to HTTPS, and create Route 53 alias A/AAAA records to the distribution.
            5. **Routing:** set the default root object to `index.html`. For an **SPA**, map 403 and 404 errors to `/index.html` with status 200 (or rewrite with a CloudFront Function). For a **Next.js export**, pages are `about.html` or `about/index.html` (with `trailingSlash: true`). The default root object only applies to `/`, so add a CloudFront Function that rewrites `/about/` → `/about/index.html`.
            6. **Caching:** hashed assets get `Cache-Control: public, max-age=31536000, immutable`, and `index.html` gets `no-cache`. After each deploy, invalidate `/index.html` (or `/*`).
        """,
        a_bn=r"""
            1. **Build:** `vite build` বানায় `dist/`। Next.js-এ `output: 'export'` দিলে বানায় `out/`, তবে এটা শুধু static feature-এর জন্য: SSR, Server Actions, ISR বা default image optimisation চলবে না।
            2. **Private bucket:** Block Public Access চালু রাখো, `aws s3 sync` দিয়ে upload করো।
            3. **CloudFront + OAC:** bucket-এর **REST endpoint**-কে origin বানাও, সাথে **Origin Access Control**। Bucket policy শুধু `cloudfront.amazonaws.com` service principal-কে allow করবে, `AWS:SourceArn` = এই distribution শর্তে। OAI হলো legacy পদ্ধতি, আর S3 *website* endpoint শুধু HTTP-তে চলে, OAC ব্যবহার করতে পারে না।
            4. **HTTPS ও domain:** ACM certificate নাও **us-east-1**-এ (CloudFront এই Region-ই চায়), alternate domain name যোগ করো, HTTP থেকে HTTPS-এ redirect করো, আর distribution-এর জন্য Route 53 alias A/AAAA record বানাও।
            5. **Routing:** default root object `index.html`। **SPA**-র জন্য 403 আর 404 error-কে status 200-সহ `/index.html`-এ map করো (বা CloudFront Function দিয়ে rewrite করো)। **Next.js export**-এ page হয় `about.html` বা `about/index.html` (`trailingSlash: true` দিলে)। Default root object শুধু `/`-এর জন্য কাজ করে, তাই একটা CloudFront Function দিয়ে `/about/` → `/about/index.html` rewrite করো।
            6. **Caching:** hash-যুক্ত asset-এ `Cache-Control: public, max-age=31536000, immutable`, আর `index.html`-এ `no-cache`। প্রতিটা deploy-এর পরে `/index.html` (বা `/*`) invalidate করো।
        """,
        ex_en=r"""
            - **Why 403 and not 404?** With OAC, CloudFront can only `GetObject`. Without `s3:ListBucket`, S3 returns **403 Access Denied** for a missing key instead of 404, so the SPA fallback must handle 403 too.
            - S3 static website hosting still works for quick demos, but it needs a public bucket and only serves HTTP. CloudFront + OAC gives you HTTPS, a private bucket, caching at edge locations and AWS WAF support.
            - Next.js static export also can't run `proxy.ts`, rewrites/redirects/headers from `next.config`, or dynamic routes without `generateStaticParams`. If you need those, deploy the Node.js server (for example as a container) instead.
            - Invalidations take a few minutes, and only a limited number of invalidation paths are free each month. Content-hashed filenames mean you rarely need to invalidate more than `index.html`.
            - **Cache key:** use a cache policy such as the managed `CachingOptimized` for the S3 behaviour, and keep headers, cookies and query strings out of the cache key unless the content really varies by them. Forwarding everything destroys the cache hit ratio.
        """,
        ex_bn=r"""
            - **404-এর বদলে 403 কেন?** OAC-তে CloudFront শুধু `GetObject` করতে পারে। `s3:ListBucket` না থাকলে না-থাকা key-এর জন্য S3 404-এর বদলে **403 Access Denied** দেয়, তাই SPA fallback-এ 403-ও ধরতে হবে।
            - S3 static website hosting দ্রুত demo-র জন্য এখনো চলে, কিন্তু এতে public bucket লাগে আর শুধু HTTP serve করে। CloudFront + OAC দিলে HTTPS, private bucket, edge location-এ caching আর AWS WAF support পাওয়া যায়।
            - Next.js static export-এ `proxy.ts`, `next.config`-এর rewrites/redirects/headers, বা `generateStaticParams` ছাড়া dynamic route-ও চলে না। এগুলো লাগলে Node.js server deploy করো (যেমন container হিসেবে)।
            - Invalidation-এ কয়েক মিনিট লাগে, আর মাসে নির্দিষ্ট সংখ্যক invalidation path-ই free। File name-এ content hash থাকলে সাধারণত `index.html` ছাড়া আর কিছু invalidate করতে হয় না।
            - **Cache key:** S3 behaviour-এর জন্য managed `CachingOptimized`-এর মতো cache policy ব্যবহার করো। Content সত্যিই header, cookie বা query string অনুযায়ী না বদলালে এগুলো cache key-তে রেখো না। সব forward করলে cache hit ratio নষ্ট হয়ে যায়।
        """,
        tip_en=r"""Name the three things juniors usually miss: OAC instead of a public bucket, the ACM certificate in us-east-1, and the 403/404 → `index.html` rule (or a CloudFront Function) for client-side routes.""",
        tip_bn=r"""Junior-রা সাধারণত যে তিনটা জিনিস মিস করে সেগুলো বলো: public bucket-এর বদলে OAC, us-east-1-এ ACM certificate, আর client-side route-এর জন্য 403/404 → `index.html` rule (বা CloudFront Function)।""",
        mist_en=r"""Making the bucket public, requesting the ACM certificate in the app's Region (for example `ap-south-1`), or caching `index.html` for a year so users never see new deployments.""",
        mist_bn=r"""Bucket public করে দেওয়া, app-এর Region-এ (যেমন `ap-south-1`) ACM certificate নেওয়া, বা `index.html` এক বছরের জন্য cache করা, যার ফলে user নতুন deploy কখনো দেখে না।""",
        code=r"""
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "AllowCloudFrontServicePrincipalReadOnly",
                  "Effect": "Allow",
                  "Principal": { "Service": "cloudfront.amazonaws.com" },
                  "Action": "s3:GetObject",
                  "Resource": "arn:aws:s3:::my-spa-bucket/*",
                  "Condition": {
                    "StringEquals": {
                      "AWS:SourceArn": "arn:aws:cloudfront::111122223333:distribution/EDFDVBD6EXAMPLE"
                    }
                  }
                }
              ]
            }
        """,
        lang="json",
        extra=[
            dict(lang="javascript", label_en="CloudFront Function (viewer request) for a Next.js export with trailingSlash: true", label_bn="Next.js export (trailingSlash: true)-এর জন্য CloudFront Function (viewer request)", src=r"""
                // Runtime: cloudfront-js-2.0 — add index.html to "directory" URLs
                function handler(event) {
                  var request = event.request;
                  var uri = request.uri;
                  if (uri.endsWith('/')) {
                    request.uri += 'index.html';
                  } else if (!uri.includes('.')) {
                    request.uri += '/index.html';
                  }
                  return request;
                }
            """),
            dict(lang="bash", label_en="Deploy with correct cache headers", label_bn="সঠিক cache header-সহ deploy", src=r"""
                # Long-lived, immutable hashed assets. No --delete: tabs still running the
                # previous build may lazy-load old chunks; prune them later (e.g. a cleanup job)
                aws s3 sync dist/ s3://my-spa-bucket/ \
                  --exclude index.html \
                  --cache-control "public, max-age=31536000, immutable"
                # index.html must always be revalidated
                aws s3 cp dist/index.html s3://my-spa-bucket/index.html \
                  --cache-control "no-cache"
                aws cloudfront create-invalidation --distribution-id EDFDVBD6EXAMPLE --paths "/index.html"
            """),
        ],
        follow=[
            ("Why must the CloudFront certificate be in us-east-1?", "CloudFront-এর certificate কেন us-east-1-এ হতে হয়?"),
            ("Users still see the old version after a deploy. What do you check?", "Deploy-এর পরেও user পুরনো version দেখছে। কী কী check করবে?"),
        ],
        related=["aws-007", "aws-011"],
        refs=[CF_OAC, CF_EXPIRATION, NEXT_STATIC],
    ),
]

if __name__ == "__main__":
    save("aws", "b2", QUESTIONS)
