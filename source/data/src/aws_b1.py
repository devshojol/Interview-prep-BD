# AWS batch 1 — aws-001 … aws-007 (fundamentals: cloud models, Regions/AZs, IAM, EC2, S3)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

SHARED_RESP = ("AWS — Shared Responsibility Model", "https://aws.amazon.com/compliance/shared-responsibility-model/")
CLOUD_TYPES = ("AWS Whitepaper — Types of cloud computing", "https://docs.aws.amazon.com/whitepapers/latest/aws-overview/types-of-cloud-computing.html")
REGIONS_AZ = ("Amazon EC2 — Regions and Zones", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html")
GLOBAL_INFRA = ("AWS Global Infrastructure — Regions and AZs", "https://aws.amazon.com/about-aws/global-infrastructure/regions_az/")
IAM_BP = ("IAM — Security best practices", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html")
IAM_ROLES = ("IAM — Roles", "https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html")
IDC = ("IAM Identity Center — What is IAM Identity Center?", "https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html")
EC2_ROLES = ("Amazon EC2 — IAM roles for Amazon EC2", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html")
IMDS = ("Amazon EC2 — Configure the Instance Metadata Service", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html")
EC2_TYPES = ("Amazon EC2 — Instance types", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-types.html")
EC2_PURCHASE = ("Amazon EC2 — Instance purchasing options", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html")
EC2_STORE = ("Amazon EC2 — Instance store", "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html")
S3_CLASSES = ("Amazon S3 — Storage classes", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html")
S3_VERSIONING = ("Amazon S3 — Versioning", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html")
S3_LIFECYCLE = ("Amazon S3 — Managing the lifecycle of objects", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html")
S3_BPA = ("Amazon S3 — Blocking public access", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html")
S3_OWNERSHIP = ("Amazon S3 — Object Ownership (disabling ACLs)", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html")
S3_ENC = ("Amazon S3 — Default encryption", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-bucket-encryption.html")

QUESTIONS = [
    # ------------------------------------------------------------------ aws-001
    Q(
        id="aws-001", sub="Cloud Computing & Shared Responsibility", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["cloud-computing", "iaas", "paas", "saas", "shared-responsibility"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""What are IaaS, PaaS and SaaS, and how does the AWS shared responsibility model change between EC2, RDS and Lambda?""",
        q_bn=r"""IaaS, PaaS আর SaaS কী? EC2, RDS আর Lambda-তে AWS-এর shared responsibility model কীভাবে বদলায়?""",
        a_en=r"""
            The three models differ in how much of the stack you manage yourself:
            - **IaaS** (Infrastructure as a Service): you rent virtual servers, storage and networking, and you manage the OS and everything above it. EC2 is the classic example.
            - **PaaS** (Platform as a Service): the provider runs the platform and you bring code or data. RDS (managed databases) and Elastic Beanstalk fit here. Serverless services like Lambda go even further.
            - **SaaS** (Software as a Service): you just use finished software, like Gmail or Slack.

            The **shared responsibility model** splits security this way: AWS secures the cloud itself (data centres, hardware, hypervisor, global network), and you secure what you put in it (your data, IAM, configuration). Where the line falls depends on the service. On **EC2** I patch the OS and runtime and configure security groups and the app. On **RDS**, AWS patches the database engine and OS, but I still own database users, network access, encryption settings and backup retention. On **Lambda**, AWS manages the servers and runtime patching. I own the code, the IAM role's permissions and the data, and I have to move off a runtime before it's deprecated.
        """,
        a_bn=r"""
            তিনটা model-এর পার্থক্য হলো stack-এর কতটুকু তোমাকে নিজে manage করতে হয়:
            - **IaaS** (Infrastructure as a Service): virtual server, storage আর network ভাড়া নাও; OS থেকে উপরের সবকিছু তুমি manage করো। Classic উদাহরণ EC2।
            - **PaaS** (Platform as a Service): platform provider চালায়, তুমি শুধু code বা data দাও। RDS (managed database) আর Elastic Beanstalk এই ধরনের; Lambda-র মতো serverless service আরও এক ধাপ এগিয়ে।
            - **SaaS** (Software as a Service): তৈরি software সরাসরি ব্যবহার করো, যেমন Gmail বা Slack।

            **Shared responsibility model** অনুযায়ী security ভাগ হয় এভাবে: cloud-টা নিজে (data centre, hardware, hypervisor, global network) secure রাখার দায়িত্ব AWS-এর। আর cloud-এ তুমি যা রাখো (data, IAM, configuration), সেটা secure রাখার দায়িত্ব তোমার। কোন service ব্যবহার করছ তার উপর এই সীমারেখা বদলায়। **EC2**-তে আমি নিজে OS ও runtime patch করি, security group আর app configure করি। **RDS**-এ database engine আর OS AWS patch করে, কিন্তু DB user, network access, encryption setting আর backup retention আমার দায়িত্ব। **Lambda**-তে server আর runtime patching AWS-এর হাতে; code, IAM role-এর permission আর data আমার দায়িত্ব। কোনো runtime deprecated হওয়ার আগে নতুন runtime-এ migrate করাও আমার কাজ।
        """,
        ex_en=r"""
            - The more managed the service, the less operational work you have, but you also get less control (no SSH into RDS, no custom kernel on Lambda).
            - Some things stay your job on every service: IAM permissions, data classification, encryption choices, network exposure and client-side security.
            - Most real cloud breaches are customer-side misconfigurations: a public S3 bucket, leaked access keys or an SSH port open to the world. AWS was not "hacked" in those cases.
            - Runtime lifecycle is easy to forget. Lambda Node.js runtimes have deprecation dates (for example `nodejs22.x` on 2027-04-30), so upgrading to `nodejs24.x` falls on you. On EC2 you have to move off Amazon Linux 2, which reached end of support on 2026-06-30.
        """,
        ex_bn=r"""
            - Service যত বেশি managed, operational কাজ তত কম, কিন্তু control-ও তত কম (RDS-এ SSH করা যায় না, Lambda-তে custom kernel নেই)।
            - কিছু জিনিস সব service-এই তোমার দায়িত্ব: IAM permission, data classification, encryption-এর সিদ্ধান্ত, network exposure আর client-side security।
            - বাস্তবে বেশিরভাগ cloud breach customer-এর ভুল configuration থেকে হয়: public S3 bucket, leak হওয়া access key, বা সবার জন্য খোলা SSH port। এগুলোতে AWS "hack" হয়নি।
            - Runtime lifecycle-এর কথা অনেকে ভুলে যায়। Lambda-র Node.js runtime-এর deprecation date থাকে (যেমন `nodejs22.x`-এর 2027-04-30), তাই `nodejs24.x`-এ upgrade করা তোমার কাজ। EC2-তে Amazon Linux 2 থেকে সরতে হবে, কারণ এর support 2026-06-30-এ শেষ হয়েছে।
        """,
        tip_en=r"""Use the phrase "security OF the cloud vs security IN the cloud", then give one concrete example per service (EC2, RDS, Lambda). Concrete examples are what make this answer stand out.""",
        tip_bn=r""""security OF the cloud বনাম security IN the cloud" কথাটা বলো, তারপর প্রতিটা service-এর (EC2, RDS, Lambda) জন্য একটা করে concrete উদাহরণ দাও। এই উদাহরণগুলোই তোমার উত্তরকে আলাদা করবে।""",
        mist_en=r"""Saying "serverless means I have no security responsibility", or assuming AWS is responsible when a misconfigured S3 bucket leaks data.""",
        mist_bn=r""""Serverless মানে আমার কোনো security দায়িত্ব নেই" বলা, অথবা ভুল configure করা S3 bucket থেকে data leak হলে সেটা AWS-এর দায় ভাবা।""",
        follow=[
            ("Who patches the operating system on an EC2 instance vs an RDS instance?", "EC2 instance আর RDS instance-এর OS কে patch করে?"),
            ("Where does a container running on Fargate fall in the shared responsibility model?", "Fargate-এ চলা container shared responsibility model-এর কোথায় পড়ে?"),
        ],
        related=["aws-003", "aws-027"],
        refs=[SHARED_RESP, CLOUD_TYPES],
    ),
    # ------------------------------------------------------------------ aws-002
    Q(
        id="aws-002", sub="Regions & Availability Zones", diff="easy", type="mcq",
        prio="high", market="both", mins=1,
        tags=["regions", "availability-zones", "edge-locations", "high-availability"],
        ver="Version-independent concept", vs=False, status="stable",
        q_en=r"""Which statement about AWS Regions and Availability Zones (AZs) is correct?""",
        q_bn=r"""AWS Region আর Availability Zone (AZ) নিয়ে কোন কথাটা সঠিক?""",
        options=[
            ("An Availability Zone is exactly one data centre, and a Region is a group of CloudFront edge locations",
             "একটা Availability Zone মানে ঠিক একটা data centre, আর Region হলো কয়েকটা CloudFront edge location-এর group"),
            ("A Region is a separate geographic area with multiple isolated AZs; each AZ is one or more data centres with independent power and networking, linked to the other AZs by low-latency connections",
             "Region হলো আলাদা একটা ভৌগোলিক এলাকা, যেখানে একাধিক isolated AZ থাকে; প্রতিটা AZ এক বা একাধিক data centre, যার power ও networking আলাদা, আর অন্য AZ-গুলোর সাথে low-latency link দিয়ে যুক্ত"),
            ("EC2 instances and subnets are global resources that AWS automatically replicates to every Region",
             "EC2 instance আর subnet global resource, AWS এগুলো automatically সব Region-এ replicate করে"),
            ("Deploying your app across two AZs in one Region also protects it from a full Region outage",
             "একই Region-এর দুইটা AZ-তে app deploy করলে পুরো Region down হলেও app চালু থাকে"),
        ],
        correct=1,
        a_en=r"""
            The second option is correct. A Region (for example `ap-south-1` Mumbai or `ap-southeast-1` Singapore) is an isolated geographic area, and it contains several AZs. Each AZ is one or more data centres with redundant power and networking. You spread an app across AZs for **high availability**, and across Regions for **disaster recovery**, lower latency for distant users, or data-residency rules.
        """,
        a_bn=r"""
            দ্বিতীয় option-টা সঠিক। Region (যেমন `ap-south-1` Mumbai বা `ap-southeast-1` Singapore) হলো একটা isolated ভৌগোলিক এলাকা, যার ভেতরে কয়েকটা AZ থাকে। প্রতিটা AZ এক বা একাধিক data centre, যেখানে power আর networking redundant। **High availability**-র জন্য app একাধিক AZ-তে ছড়িয়ে রাখি। আর **disaster recovery**, দূরের user-দের জন্য কম latency, বা data-residency নিয়মের জন্য একাধিক Region ব্যবহার করি।
        """,
        ex_en=r"""
            - **Option 4 is the tempting trap.** Multi-AZ protects you from a data centre or AZ failure, not from a Region-wide problem. Surviving a Region outage needs a multi-Region DR strategy.
            - Option 1 is wrong twice. An AZ can be more than one data centre, and edge locations are a separate, much larger network of points of presence used by CloudFront and Route 53.
            - Option 3 is wrong because most resources are regional (EC2, VPC, RDS), and a subnet lives in exactly one AZ. Only a few services are global, such as IAM, Route 53 and CloudFront.
            - Detail: AZ *names* like `ap-south-1a` can map to different physical zones in different accounts. AZ *IDs* like `aps1-az1` are consistent across accounts, so use the IDs when you coordinate between accounts.
            - Teams in Bangladesh often pick a nearby Region such as Mumbai or Singapore. Measure latency and check service availability and price in each Region before you decide.
        """,
        ex_bn=r"""
            - **Option 4 হলো আকর্ষণীয় ফাঁদ।** Multi-AZ setup একটা data centre বা AZ fail করলে বাঁচায়, পুরো Region-এর সমস্যায় নয়। Region outage সামলাতে multi-Region DR strategy লাগে।
            - Option 1 দুই কারণে ভুল: একটা AZ একাধিক data centre হতে পারে, আর edge location আলাদা ও অনেক বড় একটা point-of-presence network, যা CloudFront আর Route 53 ব্যবহার করে।
            - Option 3 ভুল, কারণ বেশিরভাগ resource regional (EC2, VPC, RDS), আর একটা subnet ঠিক একটা AZ-এর ভেতরে থাকে। IAM, Route 53, CloudFront-এর মতো অল্প কিছু service global।
            - খুঁটিনাটি: `ap-south-1a`-এর মতো AZ *name* আলাদা account-এ আলাদা physical zone বোঝাতে পারে। `aps1-az1`-এর মতো AZ *ID* সব account-এ একই থাকে, তাই account-এর মধ্যে সমন্বয়ের সময় ID ব্যবহার করো।
            - বাংলাদেশের team-গুলো প্রায়ই Mumbai বা Singapore-এর মতো কাছের Region বেছে নেয়। সিদ্ধান্তের আগে latency মেপে দেখো, আর প্রতিটা Region-এ service availability ও দাম যাচাই করো।
        """,
        tip_en=r"""Name the three layers (Region, AZ, edge location) and link each to a design goal: Region → DR, residency and latency; AZ → high availability; edge → caching and DNS close to users.""",
        tip_bn=r"""তিনটা layer-এর নাম বলো (Region, AZ, edge location), আর প্রতিটাকে একটা design goal-এর সাথে মেলাও: Region → DR, data residency, latency; AZ → high availability; edge → user-এর কাছাকাছি caching ও DNS।""",
        refs=[REGIONS_AZ, GLOBAL_INFRA],
    ),
    # ------------------------------------------------------------------ aws-003
    Q(
        id="aws-003", sub="IAM Users, Groups, Roles & Policies", diff="easy", type="conceptual",
        prio="high", market="both", mins=3,
        tags=["iam", "roles", "policies", "sts", "identity-center"],
        ver="AWS IAM (current best practices, 2026)", vs=False, status="stable",
        q_en=r"""Explain IAM users, groups, roles and policies. How should humans and applications get access to AWS today?""",
        q_bn=r"""IAM user, group, role আর policy ব্যাখ্যা করো। এখনকার best practice অনুযায়ী মানুষ আর application কীভাবে AWS access পাবে?""",
        a_en=r"""
            - **Policy**: a JSON document that allows or denies actions on resources. *Identity-based* policies attach to users, groups or roles. *Resource-based* policies, like an S3 bucket policy, attach to the resource itself.
            - **User**: a long-term identity with a console password and/or access keys.
            - **Group**: a set of users that share policies. A group is not an identity, so it can't be a principal and can't sign in.
            - **Role**: an identity with permissions but no long-term credentials. Whoever assumes it (a person, an EC2 instance, a Lambda function, another account) gets **temporary credentials from STS** that expire automatically.

            Best practice today: people sign in through **IAM Identity Center** (or federation with the company IdP) using MFA, and get roles with short-lived credentials. Workloads use roles: an EC2 instance profile, a Lambda execution role or an ECS task role. I avoid IAM users with long-lived access keys. The root user is locked away with MFA and only used for the few tasks that require it. Every policy follows least privilege.
        """,
        a_bn=r"""
            - **Policy**: JSON document, যেটা কোন resource-এ কোন action allow বা deny হবে তা বলে। *Identity-based* policy user, group বা role-এ attach হয়। *Resource-based* policy (যেমন S3 bucket policy) সরাসরি resource-এ attach হয়।
            - **User**: long-term identity, যার console password আর/অথবা access key থাকে।
            - **Group**: কয়েকজন user-এর সেট, যাদের একই policy লাগে। Group নিজে identity না, তাই principal হতে পারে না, login-ও করতে পারে না।
            - **Role**: permission আছে, কিন্তু long-term credential নেই। যে assume করে (মানুষ, EC2 instance, Lambda function বা অন্য account), সে **STS থেকে temporary credential** পায়, যা নিজে থেকেই expire হয়।

            এখনকার best practice: মানুষ **IAM Identity Center** (বা company IdP-র সাথে federation) দিয়ে MFA-সহ login করে, আর short-lived credential-সহ role পায়। Workload-গুলো role ব্যবহার করে: EC2 instance profile, Lambda execution role বা ECS task role। Long-lived access key-ওয়ালা IAM user আমি এড়িয়ে চলি। Root user MFA দিয়ে lock করে রাখি, শুধু যে অল্প কিছু কাজে root লাগে তখনই ব্যবহার করি। আর প্রতিটা policy least privilege মেনে লিখি।
        """,
        ex_en=r"""
            - **Evaluation basics:** everything is denied by default. A request needs an explicit `Allow`, and an explicit `Deny` in any applicable policy always wins.
            - **A role has two policies.** The *trust policy* says who may assume the role (for example `ec2.amazonaws.com` or a GitHub OIDC provider). The *permissions policy* says what the role can do.
            - **CI/CD without keys:** GitHub Actions and other CI systems can use OIDC federation to assume a role, so no access keys get stored as CI secrets.
            - If a long-lived key really can't be avoided (for example a legacy on-prem tool), scope it tightly, rotate it, and monitor its use with IAM's last-accessed information.
        """,
        ex_bn=r"""
            - **Evaluation-এর মূল নিয়ম:** default-এ সবকিছু deny। Request সফল হতে একটা explicit `Allow` লাগে, আর প্রযোজ্য যেকোনো policy-তে explicit `Deny` থাকলে সেটাই সবসময় জেতে।
            - **Role-এর দুইটা policy থাকে।** *Trust policy* বলে কে role-টা assume করতে পারবে (যেমন `ec2.amazonaws.com` বা GitHub OIDC provider)। *Permissions policy* বলে role-টা কী কী করতে পারবে।
            - **Key ছাড়া CI/CD:** GitHub Actions-সহ অন্যান্য CI system OIDC federation দিয়ে role assume করতে পারে, তাই CI secret-এ access key রাখতে হয় না।
            - Long-lived key একেবারে এড়ানো না গেলে (যেমন পুরনো on-prem tool), সেটার scope ছোট রাখো, নিয়মিত rotate করো, আর IAM-এর last-accessed তথ্য দিয়ে ব্যবহার monitor করো।
        """,
        tip_en=r"""Define the four terms in one sentence each, then pivot to "how I'd set it up today": Identity Center for people, roles for workloads, no long-lived keys. Interviewers want to hear that pivot.""",
        tip_bn=r"""চারটা term এক বাক্যে করে define করো, তারপর "আজকে আমি কীভাবে setup করতাম" সেদিকে যাও: মানুষের জন্য Identity Center, workload-এর জন্য role, কোনো long-lived key নয়। Interviewer এই অংশটাই শুনতে চায়।""",
        mist_en=r"""Thinking a group can be assumed like a role, sharing one IAM user between several developers, or committing access keys to Git or a `.env` file.""",
        mist_bn=r"""Group-কে role-এর মতো assume করা যায় ভাবা, কয়েকজন developer মিলে একটা IAM user শেয়ার করা, বা access key Git-এ বা `.env` file-এ commit করা।""",
        follow=[
            ("What is the difference between a role's trust policy and its permissions policy?", "Role-এর trust policy আর permissions policy-র পার্থক্য কী?"),
            ("How would you let GitHub Actions deploy to AWS without storing access keys?", "Access key না রেখে GitHub Actions থেকে AWS-এ deploy করার ব্যবস্থা কীভাবে করবে?"),
        ],
        related=["aws-004", "aws-015", "aws-024"],
        refs=[IAM_BP, IAM_ROLES, IDC],
    ),
    # ------------------------------------------------------------------ aws-004
    Q(
        id="aws-004", sub="IAM Roles for EC2", diff="easy", type="mcq",
        prio="high", market="both", mins=2,
        tags=["iam", "ec2", "instance-profile", "credentials", "imdsv2"],
        ver="AWS IAM / EC2 (AWS SDK for JavaScript v3)", vs=False, status="stable",
        q_en=r"""Your Express app on an EC2 instance needs to read and write objects in one S3 bucket. What is the recommended way to give it AWS credentials?""",
        q_bn=r"""EC2 instance-এ চলা তোমার Express app-কে একটা S3 bucket-এ object read/write করতে হবে। App-কে AWS credential দেওয়ার recommended উপায় কোনটা?""",
        options=[
            ("Create an IAM user and put its access key ID and secret access key in the app's `.env` file on the server",
             "একটা IAM user বানিয়ে তার access key ID আর secret access key server-এর `.env` file-এ রাখা"),
            ("Attach an IAM role with a least-privilege policy to the instance (instance profile); the AWS SDK picks up temporary credentials automatically",
             "Instance-এ least-privilege policy-সহ একটা IAM role attach করা (instance profile); AWS SDK নিজে থেকেই temporary credential নিয়ে নেবে"),
            ("Run `aws configure` on the instance with the root user's access keys so the app never gets `AccessDenied`",
             "Instance-এ root user-এর access key দিয়ে `aws configure` চালানো, যাতে app কখনো `AccessDenied` না পায়"),
            ("Pass the access key and secret through EC2 user data so they become environment variables at boot",
             "EC2 user data দিয়ে access key আর secret পাঠানো, যাতে boot-এর সময় সেগুলো environment variable হয়ে যায়"),
        ],
        correct=1,
        a_en=r"""
            Option 2. An **instance profile** delivers the role's temporary credentials through the Instance Metadata Service. The SDK's default credential provider chain (for example `new S3Client({})` in SDK v3) finds them with no extra code, and they rotate automatically. Nothing secret sits on disk or in Git, and the policy can be limited to the one bucket.
        """,
        a_bn=r"""
            Option 2। **Instance profile** Instance Metadata Service-এর মাধ্যমে role-এর temporary credential পৌঁছে দেয়। SDK-এর default credential provider chain (যেমন SDK v3-এ `new S3Client({})`) কোনো বাড়তি code ছাড়াই সেগুলো খুঁজে নেয়, আর credential নিজে থেকেই rotate হয়। Disk বা Git-এ কোনো secret থাকে না, আর policy-টা শুধু ওই একটা bucket-এ সীমাবদ্ধ রাখা যায়।
        """,
        ex_en=r"""
            - **Option 1 is the tempting one** because many tutorials do it and it works. But long-lived keys leak through Git pushes, backups, AMIs and screenshots. They never rotate on their own, and anyone with shell access can copy them.
            - Option 4 is wrong because user data is not a secret store. Anyone with permission to read instance attributes can see it, and so can any process on the instance through the metadata service.
            - Option 3 is the worst choice: root keys give unlimited access to the whole account.
            - **IMDSv2** (session-token based) protects the metadata endpoint against SSRF-style credential theft. Amazon Linux 2023 AMIs require IMDSv2, and you can set an account-level default so every new instance requires it.
        """,
        ex_bn=r"""
            - **Option 1-টাই আকর্ষণীয়**, কারণ অনেক tutorial এটা দেখায় আর এতে কাজও হয়। কিন্তু long-lived key Git push, backup, AMI, screenshot ইত্যাদি দিয়ে leak হয়। এগুলো নিজে থেকে কখনো rotate হয় না, আর shell access থাকলে যে কেউ copy করে নিতে পারে।
            - Option 4 ভুল, কারণ user data কোনো secret store না। Instance attribute পড়ার permission থাকলে যে কেউ এটা দেখতে পারে, আর instance-এর ভেতরের যেকোনো process metadata service থেকে এটা পড়তে পারে।
            - Option 3 সবচেয়ে খারাপ: root key পুরো account-এ সীমাহীন access দেয়।
            - **IMDSv2** (session token-ভিত্তিক) metadata endpoint-কে SSRF ধরনের credential চুরি থেকে রক্ষা করে। Amazon Linux 2023 AMI-তে IMDSv2 required থাকে, আর account-level default set করলে প্রতিটা নতুন instance-এ IMDSv2 বাধ্যতামূলক হয়।
        """,
        tip_en=r"""Say "instance profile + temporary credentials + least privilege" and mention IMDSv2. Then add that the same pattern applies to Lambda execution roles and ECS task roles.""",
        tip_bn=r""""instance profile + temporary credential + least privilege" বলো, সাথে IMDSv2-এর কথা উল্লেখ করো। তারপর যোগ করো যে Lambda execution role আর ECS task role-এও একই pattern খাটে।""",
        related=["aws-003", "aws-015"],
        refs=[EC2_ROLES, IAM_BP, IMDS],
    ),
    # ------------------------------------------------------------------ aws-005
    Q(
        id="aws-005", sub="EC2 Fundamentals", diff="easy", type="conceptual",
        prio="high", market="both", mins=4,
        tags=["ec2", "ami", "ebs", "instance-store", "user-data"],
        ver="Amazon EC2 (Amazon Linux 2023; Amazon Linux 2 end of support 2026-06-30)", vs=True, status="stable",
        q_en=r"""What is EC2? Explain instance types, AMIs, EBS vs instance store, user data and the main purchasing options.""",
        q_bn=r"""EC2 কী? Instance type, AMI, EBS বনাম instance store, user data আর প্রধান purchasing option-গুলো ব্যাখ্যা করো।""",
        a_en=r"""
            EC2 gives you virtual servers (instances) that run inside a subnet of your VPC.
            - **Instance type** is the size and hardware profile. The main families are general purpose (`t`, `m`), compute optimised (`c`), memory optimised (`r`, `x`), storage optimised (`i`) and accelerated (`g`, `p`). Burstable `t` types suit small, spiky apps. A `g` after the generation number (`t4g`, `m7g`) means an AWS Graviton (Arm) processor, which usually gives better price-performance.
            - **AMI** is the image an instance boots from. For new Linux servers I use **Amazon Linux 2023** or an Ubuntu LTS image. Amazon Linux 2 reached end of support on 2026-06-30.
            - **EBS** is a network-attached block volume that persists independently of the instance. It survives stop/start and can be snapshotted. **Instance store** is fast local disk that is physically attached, but its data is lost when the instance stops, hibernates or terminates, so I only use it for caches and scratch data.
            - **User data** is a script that runs at first boot (through cloud-init) to install packages and start the app.
            - **Purchasing options:** On-Demand (no commitment), Savings Plans or Reserved Instances (1- or 3-year commitment for a discount), Spot (spare capacity at a big discount, but AWS can reclaim it with a two-minute warning), and Dedicated Hosts for licensing or compliance needs.
        """,
        a_bn=r"""
            EC2 তোমাকে virtual server (instance) দেয়, যেগুলো তোমার VPC-র কোনো subnet-এ চলে।
            - **Instance type** মানে size আর hardware profile। প্রধান family-গুলো: general purpose (`t`, `m`), compute optimised (`c`), memory optimised (`r`, `x`), storage optimised (`i`) আর accelerated (`g`, `p`)। ছোট, মাঝে মাঝে traffic বাড়ে এমন app-এর জন্য burstable `t` type ভালো। Generation number-এর পরে `g` থাকলে (`t4g`, `m7g`) সেটা AWS Graviton (Arm) processor, যেটায় সাধারণত price-performance ভালো পাওয়া যায়।
            - **AMI** হলো image, যেটা দিয়ে instance boot হয়। নতুন Linux server-এর জন্য আমি **Amazon Linux 2023** বা Ubuntu LTS ব্যবহার করি। Amazon Linux 2-এর support 2026-06-30-এ শেষ হয়ে গেছে।
            - **EBS** network-attached block volume, যেটা instance থেকে স্বাধীনভাবে টিকে থাকে। Stop/start করলেও data থাকে, আর snapshot নেওয়া যায়। **Instance store** physically attached দ্রুত local disk, কিন্তু instance stop, hibernate বা terminate হলে এর data হারিয়ে যায়। তাই এটা শুধু cache আর scratch data-র জন্য ব্যবহার করি।
            - **User data** হলো একটা script, যেটা প্রথম boot-এ (cloud-init দিয়ে) চলে, package install করে app চালু করে।
            - **Purchasing option:** On-Demand (কোনো commitment নেই), Savings Plans বা Reserved Instances (১ বা ৩ বছরের commitment-এ discount), Spot (খালি পড়ে থাকা capacity অনেক কম দামে, কিন্তু AWS দুই মিনিটের notice দিয়ে ফেরত নিতে পারে), আর licensing বা compliance-এর প্রয়োজনে Dedicated Host।
        """,
        ex_en=r"""
            - **Stop vs terminate:** a stopped instance keeps its EBS volumes, and you don't pay for compute while it's stopped (you still pay for storage). Terminating deletes the root volume by default (`DeleteOnTermination`).
            - **The public IP changes on stop/start** unless you attach an Elastic IP. This is a common reason a DNS record "suddenly" breaks.
            - User data runs once, as root, on first boot by default. On Amazon Linux its output is in `/var/log/cloud-init-output.log`, which is the first place to look when bootstrapping fails.
            - Right-sizing: watch CloudWatch metrics and AWS Compute Optimizer recommendations, and don't guess instance sizes.
        """,
        ex_bn=r"""
            - **Stop বনাম terminate:** stop করা instance-এর EBS volume থেকে যায়, আর stop থাকা অবস্থায় compute-এর জন্য টাকা লাগে না (storage-এর জন্য লাগে)। Terminate করলে default-এ root volume delete হয়ে যায় (`DeleteOnTermination`)।
            - **Stop/start করলে public IP বদলে যায়**, যদি না Elastic IP attach করা থাকে। DNS record "হঠাৎ" কাজ না করার এটা একটা সাধারণ কারণ।
            - User data default-এ প্রথম boot-এ একবার, root হিসেবে চলে। Amazon Linux-এ এর output থাকে `/var/log/cloud-init-output.log`-এ; bootstrap fail করলে প্রথমে এখানেই দেখো।
            - Right-sizing: অনুমান করে instance size ঠিক না করে CloudWatch metric আর AWS Compute Optimizer-এর recommendation দেখো।
        """,
        tip_en=r"""Keep each concept to one crisp line, and add one practical gotcha (instance store data loss, or the public IP changing). Gotchas show you've actually run servers.""",
        tip_bn=r"""প্রতিটা concept এক লাইনে পরিষ্কার করে বলো, আর একটা বাস্তব gotcha যোগ করো (instance store-এর data হারানো বা public IP বদলে যাওয়া)। এতে বোঝা যায় তুমি সত্যিই server চালিয়েছ।""",
        mist_en=r"""Storing a database on instance store, assuming the public IP is permanent, or still choosing Amazon Linux 2 for new servers.""",
        mist_bn=r"""Instance store-এ database রাখা, public IP স্থায়ী ভাবা, বা নতুন server-এর জন্য এখনো Amazon Linux 2 বেছে নেওয়া।""",
        code=r"""
            #!/bin/bash
            # EC2 user data — runs once as root on first boot (Amazon Linux 2023 uses dnf)
            dnf update -y
            dnf install -y nginx git
            systemctl enable --now nginx
        """,
        lang="bash",
        follow=[
            ("What happens to the data and the public IP when you stop and start an instance?", "Instance stop করে আবার start করলে data আর public IP-র কী হয়?"),
            ("When would you choose Graviton (Arm) instances, and what could break?", "কখন Graviton (Arm) instance বেছে নেবে, আর কী কী সমস্যা হতে পারে?"),
        ],
        related=["aws-012", "aws-026"],
        refs=[EC2_TYPES, EC2_PURCHASE, EC2_STORE],
    ),
    # ------------------------------------------------------------------ aws-006
    Q(
        id="aws-006", sub="S3 Storage Classes, Versioning & Lifecycle", diff="easy", type="conceptual",
        prio="medium", market="both", mins=4,
        tags=["s3", "storage-classes", "versioning", "lifecycle", "cost"],
        ver="Amazon S3 (current storage classes, 2026)", vs=False, status="stable",
        q_en=r"""What are S3 storage classes, and how do versioning and lifecycle rules help you manage data and cost?""",
        q_bn=r"""S3 storage class কী? Versioning আর lifecycle rule কীভাবে data আর খরচ manage করতে সাহায্য করে?""",
        a_en=r"""
            S3 stores objects in buckets. Each storage class trades storage price against access cost and retrieval speed:
            - **S3 Standard** for frequently accessed data.
            - **S3 Intelligent-Tiering** automatically moves objects between access tiers based on usage. It's good when you can't predict access patterns (there's a small per-object monitoring fee).
            - **Standard-IA / One Zone-IA** for data you rarely read but need within milliseconds. Both have a retrieval fee and a minimum storage duration, and One Zone-IA keeps data in a single AZ.
            - **Glacier Instant Retrieval, Glacier Flexible Retrieval, Glacier Deep Archive** for archives. Storage is much cheaper, but retrieval is slower or costlier (Deep Archive retrievals take hours).
            - **S3 Express One Zone**, a single-AZ, very low-latency class for performance-critical workloads (it uses directory buckets).

            **Versioning** keeps every version of an object, so an accidental overwrite or delete can be undone (a delete just adds a delete marker). **Lifecycle rules** automate transitions, for example Standard → Standard-IA after 30 days → Glacier after 90. They also automate expiration: delete old logs, delete noncurrent versions after N days, and clean up incomplete multipart uploads.
        """,
        a_bn=r"""
            S3 bucket-এ object রাখে। প্রতিটা storage class storage-এর দাম, access খরচ আর retrieval speed-এর মধ্যে আলাদা trade-off করে:
            - **S3 Standard**: ঘন ঘন access হয় এমন data-র জন্য।
            - **S3 Intelligent-Tiering**: ব্যবহার দেখে object-কে automatically এক access tier থেকে আরেক tier-এ সরায়। Access pattern আগে থেকে বোঝা না গেলে ভালো (প্রতি object-এ সামান্য monitoring fee আছে)।
            - **Standard-IA / One Zone-IA**: কম পড়া হয়, কিন্তু দরকার হলে millisecond-এ লাগে এমন data। দুটোতেই retrieval fee আর minimum storage duration আছে; One Zone-IA data একটা AZ-তেই রাখে।
            - **Glacier Instant Retrieval, Glacier Flexible Retrieval, Glacier Deep Archive**: archive-এর জন্য। Storage অনেক সস্তা, কিন্তু retrieval ধীর বা বেশি খরচের (Deep Archive থেকে আনতে কয়েক ঘণ্টা লাগে)।
            - **S3 Express One Zone**: single-AZ, খুব কম latency-র class, performance-critical workload-এর জন্য (directory bucket ব্যবহার করে)।

            **Versioning** একটা object-এর প্রতিটা version রেখে দেয়, তাই ভুল করে overwrite বা delete হলেও ফেরানো যায় (delete করলে শুধু একটা delete marker যোগ হয়)। **Lifecycle rule** transition automate করে, যেমন Standard → ৩০ দিন পর Standard-IA → ৯০ দিন পর Glacier। Expiration-ও automate করে: পুরনো log delete, N দিন পর noncurrent version delete, আর অসম্পূর্ণ multipart upload পরিষ্কার।
        """,
        ex_en=r"""
            - **Versioning without lifecycle silently grows the bill**, because every overwrite keeps the old copy. Always pair it with `NoncurrentVersionExpiration`.
            - Minimum storage durations apply: 30 days for the IA classes, 90 for Glacier Instant and Flexible Retrieval, 180 for Deep Archive. Moving tiny or short-lived objects to IA can therefore cost more, not less.
            - In the API, `GLACIER` means Glacier Flexible Retrieval, `GLACIER_IR` is Instant Retrieval and `DEEP_ARCHIVE` is Deep Archive.
            - Once versioning is enabled it can only be *suspended*, not removed. For ransomware protection, look at S3 Object Lock and MFA Delete.
        """,
        ex_bn=r"""
            - **Lifecycle ছাড়া versioning চুপচাপ bill বাড়ায়**, কারণ প্রতিবার overwrite করলে পুরনো copy থেকে যায়। তাই সবসময় সাথে `NoncurrentVersionExpiration` দাও।
            - Minimum storage duration মানতে হয়: IA class-এ ৩০ দিন, Glacier Instant ও Flexible Retrieval-এ ৯০ দিন, Deep Archive-এ ১৮০ দিন। তাই খুব ছোট বা অল্প দিনের object IA-তে নিলে খরচ কমার বদলে বাড়তে পারে।
            - API-তে `GLACIER` মানে Glacier Flexible Retrieval, `GLACIER_IR` মানে Instant Retrieval, আর `DEEP_ARCHIVE` মানে Deep Archive।
            - Versioning একবার enable করলে শুধু *suspend* করা যায়, পুরোপুরি বন্ধ করা যায় না। Ransomware থেকে রক্ষার জন্য S3 Object Lock আর MFA Delete দেখো।
        """,
        tip_en=r"""Give a concrete lifecycle example (logs or user uploads) with day counts. It shows you think about cost, not just features.""",
        tip_bn=r"""দিনের হিসাবসহ একটা concrete lifecycle উদাহরণ দাও (log বা user upload)। এতে বোঝা যায় তুমি শুধু feature না, খরচ নিয়েও ভাবো।""",
        mist_en=r"""Enabling versioning without expiring noncurrent versions, or assuming "Glacier" always means hours-long retrieval (Glacier Instant Retrieval is millisecond access).""",
        mist_bn=r"""Noncurrent version expire না করে versioning চালু করা, অথবা ভাবা যে "Glacier" মানেই কয়েক ঘণ্টার retrieval (Glacier Instant Retrieval-এ millisecond-এ access পাওয়া যায়)।""",
        code=r"""
            {
              "Rules": [
                {
                  "ID": "logs-tiering",
                  "Status": "Enabled",
                  "Filter": { "Prefix": "logs/" },
                  "Transitions": [
                    { "Days": 30, "StorageClass": "STANDARD_IA" },
                    { "Days": 90, "StorageClass": "GLACIER" }
                  ],
                  "Expiration": { "Days": 365 },
                  "NoncurrentVersionExpiration": { "NoncurrentDays": 30 },
                  "AbortIncompleteMultipartUpload": { "DaysAfterInitiation": 7 }
                }
              ]
            }
        """,
        lang="json",
        follow=[
            ("How would you protect a bucket against accidental or malicious deletion?", "Bucket-কে ভুল করে বা ইচ্ছাকৃত delete থেকে কীভাবে রক্ষা করবে?"),
            ("When is Intelligent-Tiering a better choice than writing your own lifecycle rules?", "নিজে lifecycle rule লেখার চেয়ে Intelligent-Tiering কখন ভালো?"),
        ],
        related=["aws-007", "aws-026"],
        refs=[S3_CLASSES, S3_VERSIONING, S3_LIFECYCLE],
    ),
    # ------------------------------------------------------------------ aws-007
    Q(
        id="aws-007", sub="S3 Security Defaults", diff="easy", type="mcq",
        prio="high", market="both", mins=1,
        tags=["s3", "block-public-access", "acl", "encryption", "security"],
        ver="Amazon S3 (defaults for new buckets since 2023)", vs=True, status="stable",
        q_en=r"""You create a new S3 bucket today with default settings and upload `logo.png`. Which statement is true?""",
        q_bn=r"""আজ default setting দিয়ে একটা নতুন S3 bucket বানিয়ে `logo.png` upload করলে। কোন কথাটা সত্য?""",
        options=[
            ("The object is publicly readable by default, so anyone with the object URL can download it",
             "Default-এ object-টা public, তাই object URL জানা যে কেউ download করতে পারবে"),
            ("Block Public Access is on, ACLs are disabled (Object Ownership = Bucket owner enforced), and the object is encrypted at rest with SSE-S3 automatically",
             "Block Public Access চালু, ACL disabled (Object Ownership = Bucket owner enforced), আর object-টা automatically SSE-S3 দিয়ে encrypted at rest"),
            ("The object is stored unencrypted until you enable default encryption with a KMS key",
             "KMS key দিয়ে default encryption enable না করা পর্যন্ত object-টা unencrypted অবস্থায় থাকে"),
            ("You can make the object public by uploading it with the `public-read` ACL",
             "`public-read` ACL দিয়ে upload করলেই object-টা public করা যায়"),
        ],
        correct=1,
        a_en=r"""
            Option 2. Since April 2023, new buckets have **Block Public Access** enabled and **ACLs disabled** by default (Object Ownership = *Bucket owner enforced*). Since January 2023, every new object is encrypted at rest with **SSE-S3** by default. To serve files publicly, the recommended pattern is CloudFront with Origin Access Control in front of a private bucket. For temporary access to private files, use presigned URLs.
        """,
        a_bn=r"""
            Option 2। April 2023 থেকে নতুন bucket-এ default-এ **Block Public Access** চালু থাকে আর **ACL disabled** থাকে (Object Ownership = *Bucket owner enforced*)। January 2023 থেকে প্রতিটা নতুন object default-এ **SSE-S3** দিয়ে encrypted at rest হয়। File public-ভাবে serve করতে চাইলে recommended pattern হলো private bucket-এর সামনে Origin Access Control-সহ CloudFront। Private file-এ সাময়িক access দিতে presigned URL ব্যবহার করো।
        """,
        ex_en=r"""
            - **Option 4 is the tempting trap** for anyone who learned from older tutorials. With ACLs disabled, a request that sets an ACL such as `public-read` is rejected (`AccessControlListNotSupported`). Access is controlled only by policies.
            - Option 1 was never true: S3 objects have always been private by default. The newer defaults just make it much harder to expose them by accident.
            - Option 3 is outdated. You *choose* SSE-KMS when you need key policies, CloudTrail auditing of key usage or separation of duties, but encryption at rest is on even if you don't.
            - Making a bucket public now takes deliberate steps: turn off Block Public Access, then add a bucket policy. Good teams also block that with organisation guardrails.
        """,
        ex_bn=r"""
            - **Option 4 হলো আকর্ষণীয় ফাঁদ**, বিশেষ করে যারা পুরনো tutorial দেখে শিখেছে তাদের জন্য। ACL disabled থাকলে `public-read`-এর মতো ACL set করা request reject হয় (`AccessControlListNotSupported`)। Access শুধু policy দিয়ে নিয়ন্ত্রণ হয়।
            - Option 1 কখনোই সত্য ছিল না: S3 object সবসময় default-এ private। নতুন default-গুলো শুধু ভুল করে public করে ফেলা অনেক কঠিন করেছে।
            - Option 3 পুরনো তথ্য। Key policy, key ব্যবহারের CloudTrail audit বা separation of duties লাগলে তুমি নিজে SSE-KMS *বেছে নাও*; কিন্তু না বাছলেও encryption at rest চালু থাকে।
            - এখন bucket public করতে হলে ইচ্ছাকৃতভাবে কয়েকটা ধাপ পার হতে হয়: Block Public Access বন্ধ করা, তারপর bucket policy যোগ করা। ভালো team-গুলো organisation guardrail দিয়ে এটাও আটকে রাখে।
        """,
        tip_en=r"""Mention the dates (2023) and the recommended alternatives: CloudFront + OAC for public content, presigned URLs for temporary private access. It shows your knowledge is current.""",
        tip_bn=r"""তারিখগুলো (2023) আর recommended বিকল্পগুলো উল্লেখ করো: public content-এর জন্য CloudFront + OAC, সাময়িক private access-এর জন্য presigned URL। এতে বোঝা যায় তোমার জ্ঞান up to date।""",
        related=["aws-013", "aws-014"],
        refs=[S3_BPA, S3_OWNERSHIP, S3_ENC],
    ),
]

if __name__ == "__main__":
    save("aws", "b1", QUESTIONS)
