# AWS quick-recall — aws-q01 … aws-q10 (plain viva-style fundamentals; see AUTHORING §8a)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

QUESTIONS = [
    # ------------------------------------------------------------------ aws-q01
    Q(
        id="aws-q01", sub="Cloud Computing & Shared Responsibility", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["cloud-computing", "iaas", "paas", "saas"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""What are IaaS, PaaS and SaaS? Give an example of each.""",
        q_bn=r"""IaaS, PaaS আর SaaS কী? প্রতিটার একটা করে উদাহরণ দাও।""",
        a_en=r"""They differ in how much you manage. **IaaS** gives you raw infrastructure (servers, storage, network) and you manage the OS and up, like EC2. **PaaS** runs the platform for you so you only bring code or data, like RDS or Elastic Beanstalk. **SaaS** is finished software you just use, like Gmail or Slack.""",
        a_bn=r"""পার্থক্য হলো কতটুকু তোমাকে নিজে manage করতে হয়। **IaaS** কাঁচা infrastructure দেয় (server, storage, network), OS থেকে উপরের সব তুমি manage করো, যেমন EC2। **PaaS**-এ platform provider চালায়, তুমি শুধু code বা data দাও, যেমন RDS বা Elastic Beanstalk। **SaaS** হলো তৈরি software, শুধু ব্যবহার করো, যেমন Gmail বা Slack।""",
        ex_en=r"""The more managed the service, the less patching you do, but the less control you get. Lambda is often called serverless or FaaS: even more managed than PaaS.""",
        ex_bn=r"""Service যত বেশি managed, তোমার patch করার কাজ তত কম, কিন্তু control-ও তত কম। Lambda-কে সাধারণত serverless বা FaaS বলা হয়: PaaS-এর চেয়েও বেশি managed।""",
        tip_en=r"""Say "it's about who manages what" and give one example per model (an AWS one for IaaS and PaaS).""",
        tip_bn=r"""বলো "আসল কথা হলো কে কী manage করে", তারপর প্রতিটা model-এর একটা উদাহরণ দাও (IaaS আর PaaS-এর জন্য AWS-এর)।""",
        follow=[("Who patches the OS on EC2, and who patches it on RDS?", "EC2-তে OS patch কে করে, আর RDS-এ কে করে?")],
        related=["aws-001"],
        refs=[("AWS Whitepaper — Types of cloud computing", "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/types-of-cloud-computing.html")],
    ),
    # ------------------------------------------------------------------ aws-q02
    Q(
        id="aws-q02", sub="Regions & Availability Zones", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["region", "availability-zone", "edge-location", "high-availability"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""What is the difference between an AWS Region, an Availability Zone and an edge location?""",
        q_bn=r"""AWS Region, Availability Zone আর edge location-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""A **Region** is a separate geographic area, such as `ap-south-1` (Mumbai). Each Region has several isolated **Availability Zones (AZs)**: one or more data centres with their own power and networking. **Edge locations** are many smaller sites that CloudFront (and Route 53) use to serve users from nearby.""",
        a_bn=r"""**Region** হলো আলাদা একটা geographic এলাকা, যেমন `ap-south-1` (Mumbai)। প্রতিটা Region-এ কয়েকটা isolated **Availability Zone (AZ)** থাকে: এক বা একাধিক data centre, যাদের power আর networking আলাদা। **Edge location** হলো অনেকগুলো ছোট site, যেগুলো CloudFront (আর Route 53) ব্যবহার করে user-এর কাছাকাছি থেকে serve করতে।""",
        ex_en=r"""Running in two or more AZs protects you from one data-centre failure (high availability). It does not protect you from a whole-Region outage; that needs a second Region (disaster recovery).""",
        ex_bn=r"""দুই বা বেশি AZ-এ চালালে একটা data centre fail করলেও app চলে (high availability)। কিন্তু পুরো Region down হলে এটা বাঁচায় না; তার জন্য দ্বিতীয় Region লাগে (disaster recovery)।""",
        tip_en=r"""Name a real Region code and say "multi-AZ for HA, multi-Region for DR".""",
        tip_bn=r"""একটা আসল Region code বলো, আর বলো "HA-র জন্য multi-AZ, DR-এর জন্য multi-Region"।""",
        follow=[("How do you choose a Region for users in Bangladesh?", "বাংলাদেশের user-দের জন্য Region কীভাবে বেছে নেবে?")],
        related=["aws-002"],
        refs=[("Amazon EC2 — Regions and Zones", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html")],
    ),
    # ------------------------------------------------------------------ aws-q03
    Q(
        id="aws-q03", sub="EC2 Fundamentals", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["ec2", "ebs", "stop", "terminate"],
        ver="Amazon EC2 (EBS-backed instances)", vs=False, status="stable",
        q_en=r"""What is EC2, and what is the difference between stopping and terminating an instance?""",
        q_bn=r"""EC2 কী, আর instance stop করা আর terminate করার মধ্যে পার্থক্য কী?""",
        a_en=r"""EC2 gives you virtual servers (instances) that you rent by the second or hour. **Stopping** shuts the instance down but keeps its EBS volumes, so you can start it again; you stop paying for compute but still pay for the storage. **Terminating** deletes the instance for good, and by default its root EBS volume is deleted too.""",
        a_bn=r"""EC2 virtual server (instance) দেয়, যেটা second বা ঘণ্টা হিসেবে ভাড়া নাও। **Stop** করলে instance বন্ধ হয় কিন্তু EBS volume থেকে যায়, পরে আবার start করা যায়; compute-এর খরচ বন্ধ হয়, কিন্তু storage-এর খরচ চলে। **Terminate** করলে instance চিরতরে মুছে যায়, আর default-ভাবে root EBS volume-ও delete হয়।""",
        ex_en=r"""On stop/start the auto-assigned public IP changes (use an Elastic IP if it must stay), and instance store data is lost. Turn on termination protection for important servers.""",
        ex_bn=r"""Stop/start করলে auto-assign হওয়া public IP বদলে যায় (একই রাখতে Elastic IP নাও), আর instance store-এর data হারায়। গুরুত্বপূর্ণ server-এ termination protection চালু রাখো।""",
        tip_en=r"""Answer with what survives: "stop keeps the disk, terminate deletes it".""",
        tip_bn=r"""কী টিকে থাকে সেটা দিয়ে উত্তর দাও: "stop-এ disk থাকে, terminate-এ মুছে যায়"।""",
        follow=[("Why did my server's public IP change after a restart?", "Restart-এর পরে server-এর public IP বদলে গেল কেন?")],
        related=["aws-005", "aws-020"],
        refs=[("Amazon EC2 — Stop and start instances", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Stop_Start.html")],
    ),
    # ------------------------------------------------------------------ aws-q04
    Q(
        id="aws-q04", sub="S3 Storage Classes, Versioning & Lifecycle", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["s3", "object-storage", "bucket", "key"],
        ver="Amazon S3 (general purpose buckets)", vs=False, status="stable",
        q_en=r"""What is Amazon S3? Explain bucket, object and key.""",
        q_bn=r"""Amazon S3 কী? Bucket, object আর key ব্যাখ্যা করো।""",
        a_en=r"""S3 is object storage: you store files as **objects** inside a **bucket**, and each object is found by its **key** (its full name, like `images/logo.png`). It isn't a disk or a normal file system; "folders" are just key prefixes. New buckets are private by default, and you read and write objects over HTTPS APIs.""",
        a_bn=r"""S3 হলো object storage: file-গুলো **bucket**-এর ভেতরে **object** হিসেবে রাখা হয়, আর প্রতিটা object খোঁজা হয় তার **key** দিয়ে (পুরো নাম, যেমন `images/logo.png`)। এটা disk বা সাধারণ file system না; "folder" আসলে শুধু key-এর prefix। নতুন bucket default-ভাবে private, আর object পড়া-লেখা হয় HTTPS API দিয়ে।""",
        code=r"""
            aws s3 cp ./logo.png s3://my-app-assets/images/logo.png
            aws s3 ls s3://my-app-assets/images/
        """, lang="bash",
        ex_en=r"""General purpose bucket names are globally unique. For a database-like disk attached to a server you use EBS, not S3.""",
        ex_bn=r"""General purpose bucket-এর নাম পুরো AWS জুড়ে unique হতে হয়। Server-এ লাগানো disk দরকার হলে EBS নাও, S3 না।""",
        tip_en=r"""Contrast it with EBS: "S3 is object storage over an API, EBS is a block disk for one instance".""",
        tip_bn=r"""EBS-এর সাথে তুলনা করো: "S3 হলো API দিয়ে চলা object storage, EBS হলো একটা instance-এর block disk"।""",
        follow=[("How do you let a user download a private S3 file for a few minutes?", "Private S3 file কয়েক মিনিটের জন্য user-কে download করতে দেবে কীভাবে?")],
        related=["aws-006", "aws-007", "aws-014"],
        refs=[("Amazon S3 — What is Amazon S3?", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html")],
    ),
    # ------------------------------------------------------------------ aws-q05
    Q(
        id="aws-q05", sub="IAM Users, Groups, Roles & Policies", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["iam", "user", "role", "sts"],
        ver="AWS IAM (current best practices)", vs=False, status="stable",
        q_en=r"""What is the difference between an IAM user and an IAM role?""",
        q_bn=r"""IAM user আর IAM role-এর মধ্যে পার্থক্য কী?""",
        a_en=r"""An **IAM user** is a long-term identity with its own password and/or access keys. An **IAM role** has permissions but no long-term credentials; a person, service or EC2 instance **assumes** it and gets temporary credentials that expire. Applications on AWS should use roles, not stored access keys.""",
        a_bn=r"""**IAM user** হলো long-term identity, যার নিজের password আর/বা access key থাকে। **IAM role**-এর permission আছে কিন্তু কোনো long-term credential নেই; কোনো মানুষ, service বা EC2 instance সেটা **assume** করে আর temporary credential পায়, যেটা নিজে থেকে expire হয়। AWS-এ চলা application-এ role ব্যবহার করা উচিত, save করা access key না।""",
        code=r"""
            {
              "Version": "2012-10-17",
              "Statement": [{
                "Effect": "Allow",
                "Principal": { "Service": "ec2.amazonaws.com" },
                "Action": "sts:AssumeRole"
              }]
            }
        """, lang="json",
        ex_en=r"""The JSON above is a role's trust policy: it says *who* may assume the role (here, EC2). A separate permissions policy says *what* the role can do.""",
        ex_bn=r"""উপরের JSON হলো role-এর trust policy: এটা বলে role-টা *কে* assume করতে পারবে (এখানে EC2)। Role *কী* করতে পারবে সেটা বলে আলাদা permissions policy।""",
        tip_en=r"""Say "user = long-term keys, role = temporary credentials" and give the EC2-to-S3 example.""",
        tip_bn=r"""বলো "user = long-term key, role = temporary credential", তারপর EC2 থেকে S3 access-এর উদাহরণ দাও।""",
        follow=[("How does an Express app on EC2 get credentials without a `.env` key?", "`.env`-এ key ছাড়া EC2-এর Express app credential পায় কীভাবে?")],
        related=["aws-003", "aws-004"],
        refs=[("IAM — Roles", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html")],
    ),
    # ------------------------------------------------------------------ aws-q06
    Q(
        id="aws-q06", sub="Security Groups vs NACLs", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["security-group", "firewall", "stateful", "vpc"],
        ver="Version-independent concept (Amazon VPC)", vs=False, status="stable",
        q_en=r"""What is a security group, and what does it mean that it is "stateful"?""",
        q_bn=r"""Security group কী, আর এটা "stateful" বলতে কী বোঝায়?""",
        a_en=r"""A security group is a virtual firewall attached to an instance, load balancer or database, with **allow** rules only. "Stateful" means that if a request is allowed in, its response is automatically allowed back out, so you don't write a rule for return traffic. A new security group allows no inbound and all outbound traffic.""",
        a_bn=r"""Security group হলো instance, load balancer বা database-এ লাগানো একটা virtual firewall, যাতে শুধু **allow** rule থাকে। "Stateful" মানে কোনো request ভেতরে আসতে allow হলে তার response নিজে থেকেই বাইরে যেতে পারে, return traffic-এর জন্য আলাদা rule লাগে না। নতুন security group-এ কোনো inbound allow থাকে না, আর সব outbound allow থাকে।""",
        code=r"""
            # allow port 3000 only from the load balancer's security group
            aws ec2 authorize-security-group-ingress \
              --group-id sg-0app1234567890abc --protocol tcp --port 3000 \
              --source-group sg-0alb1234567890abc
        """, lang="bash",
        ex_en=r"""A rule can point to another security group instead of an IP range, which is how you chain ALB → app → database. A NACL, by contrast, is stateless and works at the subnet level.""",
        ex_bn=r"""Rule-এ IP range-এর বদলে আরেকটা security group দেওয়া যায়, এভাবেই ALB → app → database chain করা হয়। উল্টো দিকে NACL stateless আর subnet level-এ কাজ করে।""",
        tip_en=r"""Explain "stateful" with one request/response example, then mention referencing another security group.""",
        tip_bn=r"""একটা request/response উদাহরণ দিয়ে "stateful" বোঝাও, তারপর অন্য security group reference করার কথা বলো।""",
        follow=[("How is a NACL different from a security group?", "NACL আর security group-এর পার্থক্য কী?")],
        related=["aws-008", "aws-009"],
        refs=[("Amazon VPC — Security groups", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html")],
    ),
    # ------------------------------------------------------------------ aws-q07
    Q(
        id="aws-q07", sub="RDS High Availability & Backups", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["rds", "managed-database", "postgresql", "mysql"],
        ver="Amazon RDS (2026)", vs=False, status="stable",
        q_en=r"""What is Amazon RDS, and why use it instead of installing a database on EC2?""",
        q_bn=r"""Amazon RDS কী, আর EC2-তে নিজে database install না করে RDS কেন ব্যবহার করবে?""",
        a_en=r"""RDS is a managed relational database service for engines like PostgreSQL, MySQL, MariaDB, SQL Server and Oracle. AWS handles provisioning, OS and engine patching, automated backups with point-in-time restore, Multi-AZ failover and read replicas. On EC2 you would do all of that yourself; the trade-off is less control (no SSH to the host).""",
        a_bn=r"""RDS হলো managed relational database service, PostgreSQL, MySQL, MariaDB, SQL Server, Oracle-এর মতো engine-এর জন্য। Provisioning, OS আর engine patching, point-in-time restore-সহ automated backup, Multi-AZ failover আর read replica AWS সামলায়। EC2-তে এসব নিজেকেই করতে হতো; বিনিময়ে control কম (host-এ SSH করা যায় না)।""",
        ex_en=r"""You still own database users, network access (private subnet, security group), encryption settings and query performance. Aurora is AWS's own MySQL/PostgreSQL-compatible engine inside RDS.""",
        ex_bn=r"""Database user, network access (private subnet, security group), encryption setting আর query performance এখনো তোমার দায়িত্ব। Aurora হলো RDS-এর ভেতরে AWS-এর নিজের MySQL/PostgreSQL-compatible engine।""",
        tip_en=r"""List three things AWS takes off your plate (patching, backups, failover), then name one trade-off.""",
        tip_bn=r"""AWS কোন তিনটা কাজ তোমার কাঁধ থেকে নেয় বলো (patching, backup, failover), তারপর একটা trade-off বলো।""",
        follow=[("What is the difference between Multi-AZ and a read replica?", "Multi-AZ আর read replica-র পার্থক্য কী?")],
        related=["aws-018"],
        refs=[("Amazon RDS — What is Amazon RDS?", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html")],
    ),
    # ------------------------------------------------------------------ aws-q08
    Q(
        id="aws-q08", sub="Lambda Fundamentals", diff="easy", type="quick",
        prio="high", market="both", mins=1,
        tags=["lambda", "serverless", "handler", "nodejs"],
        ver="AWS Lambda (nodejs24.x)", vs=True, status="stable",
        q_en=r"""What is AWS Lambda, and what does "serverless" mean?""",
        q_bn=r"""AWS Lambda কী, আর "serverless" বলতে কী বোঝায়?""",
        a_en=r"""Lambda runs your function when an event happens (an HTTP request, an S3 upload, a queue message) and you pay only for requests and run time. "Serverless" doesn't mean there are no servers; it means AWS manages them, scaling and patching, so you just ship code. A single invocation can run for at most 15 minutes.""",
        a_bn=r"""কোনো event ঘটলে (HTTP request, S3 upload, queue message) Lambda তোমার function চালায়, আর তুমি শুধু request আর চলার সময়ের জন্য টাকা দাও। "Serverless" মানে server নেই এমন না; মানে server, scaling আর patching AWS সামলায়, তুমি শুধু code দাও। একটা invocation সর্বোচ্চ 15 মিনিট চলতে পারে।""",
        code=r"""
            export const handler = async (event) => {
              const name = event.name ?? "world";
              return { statusCode: 200, body: JSON.stringify({ message: `Hello, ${name}` }) };
            };
            // handler({ name: "Dhaka" })
            // → { statusCode: 200, body: '{"message":"Hello, Dhaka"}' }
        """, lang="javascript",
        ex_en=r"""On `nodejs24.x`, handlers must be `async` (or synchronous); callback-style handlers only work up to Node.js 22. A cold start is the extra delay when Lambda creates a new environment.""",
        ex_bn=r"""`nodejs24.x`-এ handler `async` (বা synchronous) হতে হবে; callback-style handler শুধু Node.js 22 পর্যন্ত চলে। নতুন environment তৈরির সময় যে বাড়তি দেরি হয়, সেটাই cold start।""",
        tip_en=r"""Correct the myth first ("there are servers, AWS runs them"), then give one event example.""",
        tip_bn=r"""আগে ভুল ধারণাটা ঠিক করো ("server আছে, AWS চালায়"), তারপর একটা event-এর উদাহরণ দাও।""",
        follow=[("What is a cold start, and how do you reduce it?", "Cold start কী, আর কীভাবে কমাবে?")],
        related=["aws-010", "aws-025"],
        refs=[("AWS Lambda — Define the handler in Node.js", "https://docs.aws.amazon.com/lambda/latest/dg/nodejs-handler.html")],
    ),
    # ------------------------------------------------------------------ aws-q09
    Q(
        id="aws-q09", sub="S3 + CloudFront Static Hosting", diff="easy", type="quick",
        prio="medium", market="both", mins=1,
        tags=["cloudfront", "cdn", "edge-location", "caching"],
        ver="Amazon CloudFront (OAC)", vs=False, status="stable",
        q_en=r"""What is CloudFront, and why would you put it in front of S3 or an API?""",
        q_bn=r"""CloudFront কী, আর S3 বা API-এর সামনে কেন এটা বসাবে?""",
        a_en=r"""CloudFront is AWS's CDN: it caches your content at edge locations close to users, so pages load faster and your origin (S3, an ALB or an API) gets fewer requests. It also gives you HTTPS with a free ACM certificate, a custom domain, and a place to attach AWS WAF.""",
        a_bn=r"""CloudFront হলো AWS-এর CDN: user-এর কাছাকাছি edge location-এ content cache করে, ফলে page দ্রুত load হয় আর তোমার origin-এ (S3, ALB বা API) request কম যায়। এর সাথে free ACM certificate দিয়ে HTTPS, custom domain, আর AWS WAF লাগানোর জায়গাও পাও।""",
        ex_en=r"""With S3, keep the bucket private and let only CloudFront read it through Origin Access Control (OAC); OAI is the legacy way. After a deploy, invalidate changed files such as `/index.html`.""",
        ex_bn=r"""S3-এর সাথে bucket private রাখো, আর Origin Access Control (OAC) দিয়ে শুধু CloudFront-কে পড়তে দাও; OAI হলো legacy পদ্ধতি। Deploy-এর পরে বদলানো file, যেমন `/index.html`, invalidate করো।""",
        tip_en=r"""Give the two wins, speed and less origin load, then mention OAC for private buckets.""",
        tip_bn=r"""দুটো লাভ বলো, speed আর origin-এ কম load, তারপর private bucket-এর জন্য OAC-এর কথা বলো।""",
        follow=[("Why must the CloudFront certificate be in us-east-1?", "CloudFront-এর certificate কেন us-east-1-এ থাকতে হয়?")],
        related=["aws-013", "aws-023"],
        refs=[("Amazon CloudFront — What is Amazon CloudFront?", "https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html")],
    ),
    # ------------------------------------------------------------------ aws-q10
    Q(
        id="aws-q10", sub="Auto Scaling", diff="medium", type="quick",
        prio="high", market="both", mins=2,
        tags=["auto-scaling", "ec2", "target-tracking", "health-check"],
        ver="Amazon EC2 Auto Scaling (launch templates)", vs=False, status="stable",
        q_en=r"""What is an EC2 Auto Scaling group, and how does it decide when to add or remove instances?""",
        q_bn=r"""EC2 Auto Scaling group কী, আর কখন instance বাড়াবে বা কমাবে সেটা কীভাবে ঠিক করে?""",
        a_en=r"""An Auto Scaling group launches instances from a **launch template** and keeps the count between a **min** and **max**, starting at the **desired** capacity, across several AZs. A scaling policy changes the desired count: **target tracking** (for example, keep average CPU at 50%) is the usual choice. It also replaces instances that fail health checks.""",
        a_bn=r"""Auto Scaling group একটা **launch template** থেকে instance চালু করে, আর কয়েকটা AZ জুড়ে instance-এর সংখ্যা **min** আর **max**-এর মধ্যে রাখে, শুরু হয় **desired** capacity থেকে। Scaling policy desired সংখ্যা বদলায়: সাধারণত **target tracking** নেওয়া হয় (যেমন average CPU 50%-এ রাখো)। Health check-এ fail করা instance-ও এটা বদলে দেয়।""",
        code=r"""
            aws autoscaling put-scaling-policy \
              --auto-scaling-group-name api-asg --policy-name cpu50 \
              --policy-type TargetTrackingScaling \
              --target-tracking-configuration '{"PredefinedMetricSpecification":{"PredefinedMetricType":"ASGAverageCPUUtilization"},"TargetValue":50.0}'
        """, lang="bash",
        ex_en=r"""Behind a load balancer, turn on **ELB health checks** so an instance whose app is broken (not just its VM) gets replaced. Scaling only works if the app is stateless: sessions in Redis or tokens, files in S3.""",
        ex_bn=r"""Load balancer-এর পেছনে থাকলে **ELB health check** চালু করো, যাতে শুধু VM না, app ভেঙে গেলেও instance বদলায়। App stateless হলেই scaling কাজ করে: session Redis-এ বা token-এ, file S3-এ।""",
        tip_en=r"""Say "min/desired/max, a target-tracking policy, and health-check replacement", then add the stateless-app point.""",
        tip_bn=r"""বলো "min/desired/max, target-tracking policy, আর health check দিয়ে replacement", তারপর stateless app-এর কথাটা যোগ করো।""",
        follow=[("Why does an app need to be stateless before you auto scale it?", "Auto scale করার আগে app-কে stateless হতে হয় কেন?"),
                ("What is the difference between EC2 and ELB health checks in an Auto Scaling group?", "Auto Scaling group-এ EC2 health check আর ELB health check-এর পার্থক্য কী?")],
        related=["aws-023", "aws-019"],
        refs=[("Amazon EC2 Auto Scaling — Target tracking scaling policies", "https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html")],
    ),
]

if __name__ == "__main__":
    save("aws", "quick", QUESTIONS)
