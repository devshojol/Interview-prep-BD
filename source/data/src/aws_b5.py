# AWS batch 5 — aws-027 … aws-032 (security, deployments, API Gateway, DR, event-driven, multi-account)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

GUARDDUTY = ("Amazon GuardDuty — What is Amazon GuardDuty?", "https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html")
WAF = ("AWS WAF — Developer Guide", "https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html")
KMS = ("AWS KMS — Developer Guide", "https://docs.aws.amazon.com/kms/latest/developerguide/overview.html")
CLOUDTRAIL = ("AWS CloudTrail — User Guide", "https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html")
CODEDEPLOY_CONFIGS = ("AWS CodeDeploy — Deployment configurations", "https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html")
ECS_DEPLOY_TYPES = ("Amazon ECS — Deployment types", "https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html")
DEPLOY_WP = ("AWS Whitepaper — Overview of deployment options: deployment strategies", "https://docs.aws.amazon.com/whitepapers/latest/overview-deployment-options/deployment-strategies.html")
APIGW_CHOOSE = ("API Gateway — Choose between REST APIs and HTTP APIs", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html")
APIGW_THROTTLE = ("API Gateway — Throttle requests to your REST APIs", "https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html")
DR_WP = ("AWS Whitepaper — Disaster recovery options in the cloud", "https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html")
AURORA_GLOBAL_DR = ("Aurora — Using switchover or failover in an Aurora global database", "https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database-disaster-recovery.html")
AWS_BACKUP = ("AWS Backup — What is AWS Backup?", "https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html")
LAMBDA_SQS = ("AWS Lambda — Configuring Amazon SQS event source mappings", "https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html")
SQS_DLQ = ("Amazon SQS — Dead-letter queues", "https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html")
BUILDERS_IDEMPOTENCY = ("Amazon Builders' Library — Making retries safe with idempotent APIs", "https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/")
SCPS = ("AWS Organizations — Service control policies (SCPs)", "https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html")
ORG_WP = ("AWS Whitepaper — Organizing your AWS environment using multiple accounts", "https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html")
CONTROL_TOWER = ("AWS Control Tower — What is AWS Control Tower?", "https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html")

QUESTIONS = [
    # ------------------------------------------------------------------ aws-027
    Q(
        id="aws-027", sub="Security Best Practices", diff="hard", type="security-performance",
        prio="high", market="both", mins=10,
        tags=["security", "guardduty", "waf", "kms", "encryption"],
        ver="AWS security services (2026): GuardDuty, WAF, KMS, CloudTrail, Security Hub", vs=False, status="stable",
        q_en=r"""You inherit a production AWS account running a Node.js app on EC2 with RDS and S3. What security controls would you put in place first, and how do GuardDuty, AWS WAF, KMS, CloudTrail and encryption in transit and at rest fit together? What are the performance or cost side effects?""",
        q_bn=r"""তুমি এমন একটা production AWS account-এর দায়িত্ব পেলে, যেখানে EC2-তে Node.js app চলে, সাথে RDS আর S3। প্রথমে কোন security control-গুলো বসাবে? GuardDuty, AWS WAF, KMS, CloudTrail আর encryption in transit ও at rest কীভাবে একসাথে কাজ করে? Performance বা খরচের উপর এগুলোর কী প্রভাব পড়ে?""",
        a_en=r"""
            In priority order:
            1. **Identity first:** MFA on root and no root access keys. People sign in through IAM Identity Center with MFA. Remove long-lived IAM user keys, use roles for workloads, and let CI deploy through OIDC. Tighten permissions with IAM Access Analyzer's unused-access findings.
            2. **Visibility:** **CloudTrail** records every API call (a multi-Region trail into a locked-down S3 bucket, ideally in a separate log account). **GuardDuty** watches CloudTrail, VPC Flow Logs and DNS logs for threats such as crypto-mining, use of stolen credentials or unusual API calls. Security Hub and AWS Config track posture against best-practice checks.
            3. **Edge and network:** **AWS WAF** on CloudFront or the ALB, with managed rule groups (common OWASP-style attacks, known bad inputs, IP reputation) plus **rate-based rules**. No SSH from `0.0.0.0/0`; use Session Manager instead. The database stays in private subnets, and security groups are chained.
            4. **Data:** *at rest*: S3 default encryption (SSE-S3, or SSE-KMS when you need key control), EBS encryption by default, and RDS encryption with **KMS**. *In transit*: TLS everywhere (ACM certificates on CloudFront/ALB), a bucket-policy deny for `aws:SecureTransport = false`, and `rds.force_ssl` on PostgreSQL. Use KMS customer managed keys when you need key policies, audit trails of key use or separation of duties.
            5. **Instances:** IMDSv2 required, patching through SSM Patch Manager, and Amazon Inspector for vulnerability scanning of EC2, ECR images and Lambda.
            6. **Secrets and recovery:** Secrets Manager for credentials, and AWS Backup with Vault Lock so ransomware can't delete the backups.
        """,
        a_bn=r"""
            অগ্রাধিকার অনুযায়ী:
            1. **আগে identity:** root-এ MFA, root-এর কোনো access key নয়। মানুষ IAM Identity Center দিয়ে MFA-সহ login করবে। Long-lived IAM user key সরিয়ে দাও, workload-এর জন্য role দাও, আর CI-কে OIDC দিয়ে deploy করতে দাও। IAM Access Analyzer-এর unused-access finding দেখে permission আরও টাইট করো।
            2. **Visibility:** **CloudTrail** প্রতিটা API call রেকর্ড করে (multi-Region trail, locked-down S3 bucket-এ, সম্ভব হলে আলাদা log account-এ)। **GuardDuty** CloudTrail, VPC Flow Logs আর DNS log দেখে crypto-mining, চুরি হওয়া credential-এর ব্যবহার বা অস্বাভাবিক API call-এর মতো হুমকি ধরে। Security Hub আর AWS Config best-practice check অনুযায়ী posture track করে।
            3. **Edge আর network:** CloudFront বা ALB-তে **AWS WAF**, সাথে managed rule group (common OWASP ধরনের attack, known bad input, IP reputation) আর **rate-based rule**। `0.0.0.0/0` থেকে কোনো SSH নয়; বদলে Session Manager। Database private subnet-এ, security group চেইন করা।
            4. **Data:** *at rest*: S3 default encryption (SSE-S3, বা key-এর উপর নিয়ন্ত্রণ লাগলে SSE-KMS), default-এ EBS encryption, আর **KMS** দিয়ে RDS encryption। *In transit*: সব জায়গায় TLS (CloudFront/ALB-তে ACM certificate), bucket policy-তে `aws:SecureTransport = false` হলে deny, আর PostgreSQL-এ `rds.force_ssl`। Key policy, key ব্যবহারের audit trail বা separation of duties লাগলে KMS customer managed key ব্যবহার করো।
            5. **Instance:** IMDSv2 required, SSM Patch Manager দিয়ে patching, আর EC2, ECR image ও Lambda-র vulnerability scan-এর জন্য Amazon Inspector।
            6. **Secret আর recovery:** credential-এর জন্য Secrets Manager, আর Vault Lock-সহ AWS Backup, যাতে ransomware backup delete করতে না পারে।
        """,
        ex_en=r"""
            **Performance and cost side effects** (the "-performance" half of this question):
            - **WAF** adds very little latency, especially on CloudFront at the edge. Rule capacity and request volume drive the cost, so start with managed rule groups and add custom rules based on real traffic.
            - **SSE-KMS on busy S3 buckets** makes a KMS call per object operation, which adds cost and can run into KMS request quotas. Enable **S3 Bucket Keys** to cut KMS calls dramatically.
            - **TLS** cost is negligible on modern CPUs. Terminate it at CloudFront or the ALB and reuse connections (keep-alive) to the backend.
            - **GuardDuty and Inspector** are priced by volume analysed. Use their cost estimates per account rather than guessing.

            **Gotchas:** RDS encryption at rest must be enabled at creation. To encrypt an existing database you snapshot it, copy the snapshot with encryption, and restore. Logs stored in the same account an attacker controls can be deleted, which is why a separate log-archive account matters. Deleting a KMS key is irreversible after its waiting period (7–30 days), so prefer disabling it. GuardDuty findings can drive automated responses through EventBridge (isolate the instance's security group, revoke sessions, notify on-call).
        """,
        ex_bn=r"""
            **Performance আর খরচের প্রভাব** (প্রশ্নের "-performance" অংশ):
            - **WAF** খুব সামান্য latency যোগ করে, বিশেষ করে edge-এ CloudFront-এ। খরচ নির্ভর করে rule capacity আর request volume-এর উপর, তাই managed rule group দিয়ে শুরু করো, তারপর আসল traffic দেখে custom rule যোগ করো।
            - **ব্যস্ত S3 bucket-এ SSE-KMS** প্রতিটা object operation-এ KMS call করে, যাতে খরচ বাড়ে আর KMS request quota-তে আটকাতে পারে। **S3 Bucket Keys** চালু করলে KMS call অনেক কমে যায়।
            - আধুনিক CPU-তে **TLS**-এর খরচ নগণ্য। CloudFront বা ALB-তে terminate করো, আর backend-এ connection reuse (keep-alive) করো।
            - **GuardDuty আর Inspector**-এর দাম নির্ভর করে কতটা data বিশ্লেষণ হলো তার উপর। অনুমান না করে প্রতি account-এ তাদের cost estimate দেখো।

            **Gotcha:** RDS encryption at rest তৈরির সময়েই চালু করতে হয়। চলমান database encrypt করতে হলে snapshot নিয়ে encryption-সহ copy করে restore করতে হয়। Attacker যে account নিয়ন্ত্রণ করে, সেখানে রাখা log delete হয়ে যেতে পারে, এজন্যই আলাদা log-archive account জরুরি। KMS key-এর waiting period (৭–৩০ দিন) পার হলে delete আর ফেরানো যায় না, তাই delete না করে disable করাই ভালো। GuardDuty finding দিয়ে EventBridge-এর মাধ্যমে automated response চালানো যায় (instance-এর security group আলাদা করা, session revoke, on-call-কে জানানো)।
        """,
        tip_en=r"""Prioritise out loud ("identity first, then visibility, then network, then data") instead of listing services randomly. Then cover the performance/cost angle, like S3 Bucket Keys for KMS. Few candidates mention it.""",
        tip_bn=r"""এলোমেলোভাবে service-এর নাম না বলে জোরে অগ্রাধিকার বলো ("আগে identity, তারপর visibility, তারপর network, তারপর data")। তারপর performance/খরচের দিকটা বলো, যেমন KMS-এর জন্য S3 Bucket Keys। খুব কম candidate এটা উল্লেখ করে।""",
        mist_en=r"""Thinking GuardDuty *blocks* attacks (it detects; WAF and security groups block), confusing CloudTrail (API audit) with CloudWatch Logs (application logs), or enabling SSE-KMS on a hot bucket without Bucket Keys.""",
        mist_bn=r"""GuardDuty attack *block* করে ভাবা (এটা detect করে; block করে WAF আর security group), CloudTrail (API audit) আর CloudWatch Logs (application log) গুলিয়ে ফেলা, বা Bucket Keys ছাড়া ব্যস্ত bucket-এ SSE-KMS চালু করা।""",
        code=r"""
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "DenyInsecureTransport",
                  "Effect": "Deny",
                  "Principal": "*",
                  "Action": "s3:*",
                  "Resource": ["arn:aws:s3:::acme-media", "arn:aws:s3:::acme-media/*"],
                  "Condition": { "Bool": { "aws:SecureTransport": "false" } }
                }
              ]
            }
        """,
        lang="json",
        extra=[dict(lang="bash", label_en="Quick hardening commands", label_bn="দ্রুত hardening command", src=r"""
            # Require IMDSv2 on an existing instance
            aws ec2 modify-instance-metadata-options --instance-id i-0123456789abcdef0 \
              --http-tokens required --http-endpoint enabled

            # Encrypt all new EBS volumes in this Region by default
            aws ec2 enable-ebs-encryption-by-default --region ap-south-1

            # Turn on GuardDuty threat detection
            aws guardduty create-detector --enable
        """)],
        follow=[
            ("GuardDuty reports an EC2 instance talking to a known crypto-mining pool. What are your first five steps?", "GuardDuty জানাচ্ছে একটা EC2 instance পরিচিত crypto-mining pool-এর সাথে যোগাযোগ করছে। তোমার প্রথম পাঁচটা পদক্ষেপ কী?"),
            ("When would you choose SSE-KMS with a customer managed key over SSE-S3?", "কখন SSE-S3-এর বদলে customer managed key-সহ SSE-KMS বেছে নেবে?"),
        ],
        related=["aws-001", "aws-024", "aws-032"],
        refs=[GUARDDUTY, WAF, KMS],
    ),
    # ------------------------------------------------------------------ aws-028
    Q(
        id="aws-028", sub="Deployment Strategies", diff="hard", type="comparison",
        prio="high", market="both", mins=8,
        tags=["deployment", "blue-green", "canary", "codedeploy", "iac"],
        ver="Amazon ECS (rolling + built-in blue/green), AWS CodeDeploy, CloudFormation/CDK/Terraform (2026)", vs=True, status="stable",
        q_en=r"""Compare rolling, blue/green and canary deployments on AWS. How would you implement each for an ECS service or a Lambda function, and how do immutable infrastructure and Infrastructure as Code (CloudFormation, CDK, Terraform) make releases safer?""",
        q_bn=r"""AWS-এ rolling, blue/green আর canary deployment-এর তুলনা করো। একটা ECS service বা Lambda function-এর জন্য প্রতিটা কীভাবে implement করবে? Immutable infrastructure আর Infrastructure as Code (CloudFormation, CDK, Terraform) কীভাবে release-কে নিরাপদ করে?""",
        a_en=r"""
            - **Rolling:** replace tasks or instances in batches. This is the ECS default, controlled by `minimumHealthyPercent`/`maximumPercent`; Auto Scaling groups use instance refresh. It's cheap because no second full environment is needed. Downsides: old and new versions serve traffic at the same time, and rollback means another rolling deploy. Turn on the **ECS deployment circuit breaker with rollback** and CloudWatch alarm-based rollback.
            - **Blue/green:** run the new version (green) next to the old one (blue), test it with test traffic, switch production traffic, and keep blue alive for instant rollback. On AWS you can do this with ECS's built-in blue/green deployments (bake time, lifecycle hooks), with CodeDeploy, or by swapping ALB target groups. It costs double capacity during the switch, and the database schema must work with both versions.
            - **Canary:** shift a small share first, then the rest, with automatic rollback if alarms fire. Examples: CodeDeploy's `CodeDeployDefault.ECSCanary10Percent5Minutes` for ECS, `CodeDeployDefault.LambdaCanary10Percent5Minutes` for Lambda aliases, ALB weighted target groups, or Route 53 weighted records. *Linear* is the variant that shifts in equal steps.
            - **Immutable infrastructure:** never patch servers in place. Build a new AMI or container image tagged with the commit SHA, roll out new instances or tasks, and throw the old ones away. Rollback means redeploying the previous tag.
            - **IaC:** CloudFormation/CDK (AWS-native stacks, change sets, drift detection) or Terraform (multi-cloud, `plan`/`apply`, state). Every environment becomes reproducible, and changes are reviewed in PRs after `cdk diff` or `terraform plan`.

            My default: rolling with circuit breaker and alarms for most services, and canary or blue/green for critical customer-facing APIs.
        """,
        a_bn=r"""
            - **Rolling:** task বা instance batch ধরে ধরে replace করা। এটাই ECS-এর default, যা `minimumHealthyPercent`/`maximumPercent` দিয়ে নিয়ন্ত্রণ হয়; Auto Scaling group-এ instance refresh ব্যবহার হয়। সস্তা, কারণ দ্বিতীয় পূর্ণ environment লাগে না। অসুবিধা: পুরনো আর নতুন version একসাথে traffic serve করে, আর rollback মানে আবার একটা rolling deploy। **ECS deployment circuit breaker rollback-সহ** আর CloudWatch alarm-ভিত্তিক rollback চালু রাখো।
            - **Blue/green:** পুরনোটার (blue) পাশে নতুন version (green) চালাও, test traffic দিয়ে test করো, production traffic সরাও, আর তাৎক্ষণিক rollback-এর জন্য blue চালু রাখো। AWS-এ এটা করা যায় ECS-এর built-in blue/green deployment দিয়ে (bake time, lifecycle hook), CodeDeploy দিয়ে, বা ALB target group অদলবদল করে। Switch-এর সময় দ্বিগুণ capacity লাগে, আর database schema-কে দুই version-এর সাথেই চলতে হবে।
            - **Canary:** আগে অল্প একটা অংশে traffic সরাও, তারপর বাকিটা; alarm বাজলে automatic rollback। উদাহরণ: ECS-এর জন্য CodeDeploy-এর `CodeDeployDefault.ECSCanary10Percent5Minutes`, Lambda alias-এর জন্য `CodeDeployDefault.LambdaCanary10Percent5Minutes`, ALB weighted target group, বা Route 53 weighted record। *Linear* হলো সমান সমান ধাপে সরানোর variant।
            - **Immutable infrastructure:** কখনো চলমান server-এ patch কোরো না। Commit SHA দিয়ে tag করা নতুন AMI বা container image build করো, নতুন instance বা task চালু করো, পুরনোগুলো ফেলে দাও। Rollback মানে আগের tag আবার deploy করা।
            - **IaC:** CloudFormation/CDK (AWS-native stack, change set, drift detection) বা Terraform (multi-cloud, `plan`/`apply`, state)। প্রতিটা environment হুবহু আবার তৈরি করা যায়, আর `cdk diff` বা `terraform plan` দেখে PR-এ পরিবর্তন review হয়।

            আমার default: বেশিরভাগ service-এ circuit breaker আর alarm-সহ rolling, আর গুরুত্বপূর্ণ customer-facing API-তে canary বা blue/green।
        """,
        ex_en=r"""
            - **The database is the hard part.** Every strategy that runs two versions at once needs backward-compatible schema changes. Use expand/contract: add the new column → deploy code that writes both → backfill → switch reads → remove the old column in a later release.
            - **Rollback triggers must be automatic:** attach CloudWatch alarms (5xx rate, p99 latency, business metrics like failed payments) to the deployment so it rolls back without anyone watching a dashboard.
            - **Canary needs enough traffic to be meaningful.** Ten percent of very little traffic for five minutes proves nothing. Low-traffic services may need synthetic tests or longer bake times.
            - Feature flags complement deployment strategies: deploy dark, then release to a percentage of users, decoupling *deploy* from *release*.
            - IaC caveat: avoid manual console changes ("ClickOps"). They cause drift, and the next `apply` may silently revert them.
        """,
        ex_bn=r"""
            - **কঠিন অংশ হলো database।** যে strategy-তে একসাথে দুইটা version চলে, সেখানে backward-compatible schema change লাগে। Expand/contract পদ্ধতি নাও: নতুন column যোগ → দুটোতেই লেখে এমন code deploy → backfill → read নতুন column-এ সরানো → পরের release-এ পুরনো column বাদ।
            - **Rollback trigger automatic হতে হবে:** deployment-এর সাথে CloudWatch alarm জুড়ে দাও (5xx rate, p99 latency, failed payment-এর মতো business metric), যাতে কেউ dashboard-এ চোখ না রাখলেও rollback হয়।
            - **Canary অর্থবহ হতে যথেষ্ট traffic লাগে।** খুব কম traffic-এর দশ শতাংশ পাঁচ মিনিট চালিয়ে কিছুই প্রমাণ হয় না। কম traffic-এর service-এ synthetic test বা লম্বা bake time লাগতে পারে।
            - Feature flag deployment strategy-র পরিপূরক: আগে লুকিয়ে deploy করো, তারপর কিছু শতাংশ user-এর জন্য release করো। এতে *deploy* আর *release* আলাদা হয়ে যায়।
            - IaC-এর সতর্কতা: console-এ হাতে পরিবর্তন ("ClickOps") এড়িয়ে চলো। এতে drift তৈরি হয়, আর পরের `apply` সেগুলো নিঃশব্দে উল্টে দিতে পারে।
        """,
        tip_en=r"""Compare on four axes (cost, speed of rollback, blast radius, complexity), then bring up the database compatibility problem yourself. Interviewers often hold that question back to see if you think of it.""",
        tip_bn=r"""চারটা মাপকাঠিতে তুলনা করো (খরচ, rollback-এর গতি, blast radius, জটিলতা), তারপর নিজে থেকেই database compatibility-র সমস্যাটা তোলো। Interviewer প্রায়ই প্রশ্নটা চেপে রাখে, দেখতে চায় তুমি নিজে ভাবো কি না।""",
        mist_en=r"""Deploying a breaking schema migration together with a blue/green switch, calling "rolling" zero-risk, or relying on manual rollback with no alarms.""",
        mist_bn=r"""Blue/green switch-এর সাথে একসাথে breaking schema migration deploy করা, "rolling"-কে ঝুঁকিহীন বলা, বা alarm ছাড়া manual rollback-এর উপর নির্ভর করা।""",
        code=r"""
            # CloudFormation (excerpt): ECS service with safe rolling deployments
            OrdersService:
              Type: AWS::ECS::Service
              Properties:
                Cluster: !Ref Cluster
                LaunchType: FARGATE
                DesiredCount: 4
                TaskDefinition: !Ref OrdersTaskDef   # new image tag => new task definition revision
                DeploymentConfiguration:
                  MinimumHealthyPercent: 100         # never drop below current capacity
                  MaximumPercent: 200                # start new tasks before stopping old ones
                  DeploymentCircuitBreaker:
                    Enable: true
                    Rollback: true                   # roll back if new tasks keep failing
                  Alarms:
                    AlarmNames: [orders-5xx-high, orders-p99-latency-high]
                    Enable: true
                    Rollback: true                   # roll back if alarms fire during deploy
        """,
        lang="yaml",
        follow=[
            ("How do you deploy a database schema change safely with blue/green?", "Blue/green-এ database schema change নিরাপদে কীভাবে deploy করবে?"),
            ("What is the difference between canary and linear traffic shifting?", "Canary আর linear traffic shifting-এর পার্থক্য কী?"),
        ],
        related=["aws-021", "aws-023"],
        refs=[DEPLOY_WP, ECS_DEPLOY_TYPES, CODEDEPLOY_CONFIGS],
    ),
    # ------------------------------------------------------------------ aws-029
    Q(
        id="aws-029", sub="API Gateway", diff="hard", type="mcq",
        prio="medium", market="both", mins=2,
        tags=["api-gateway", "rest-api", "http-api", "throttling", "authorizers"],
        ver="Amazon API Gateway (REST API vs HTTP API feature set, 2026)", vs=True, status="stable",
        q_en=r"""You're exposing a Lambda-backed public API to partner companies. Each partner needs its **own API key with a monthly quota and per-client throttling**, requests must be **validated against a schema** before they reach Lambda, and **AWS WAF** must protect the API. Which option fits?""",
        q_bn=r"""তুমি partner company-গুলোর জন্য Lambda-চালিত একটা public API expose করছ। প্রতিটা partner-এর **নিজস্ব API key, মাসিক quota আর per-client throttling** লাগবে, request Lambda-তে পৌঁছানোর আগে **schema অনুযায়ী validate** হতে হবে, আর API-কে **AWS WAF** দিয়ে রক্ষা করতে হবে। কোন option উপযুক্ত?""",
        options=[
            ("An API Gateway HTTP API with a JWT authorizer, because it's cheaper, faster and supports usage plans",
             "JWT authorizer-সহ API Gateway HTTP API, কারণ এটা সস্তা, দ্রুত আর usage plan support করে"),
            ("An API Gateway REST API with API keys, usage plans, request validation and an associated AWS WAF web ACL",
             "API key, usage plan, request validation আর যুক্ত AWS WAF web ACL-সহ API Gateway REST API"),
            ("A Lambda function URL with `AuthType: AWS_IAM`",
             "`AuthType: AWS_IAM`-সহ একটা Lambda function URL"),
            ("An Application Load Balancer with a Lambda target and one listener rule per partner",
             "Lambda target-সহ একটা Application Load Balancer, প্রতিটা partner-এর জন্য একটা করে listener rule"),
        ],
        correct=1,
        a_en=r"""
            Option 2. Only **REST APIs** support API keys, **usage plans** (per-client quotas and throttling), **request validation**, AWS WAF integration, caching, private endpoints and resource policies. HTTP APIs are cheaper and lower latency, with native JWT authorizers, but they don't have those API-management features.
        """,
        a_bn=r"""
            সঠিক উত্তর Option 2। Partner-দের জন্য যা যা দরকার, অর্থাৎ আলাদা API key, **usage plan** দিয়ে প্রতিটা client-এর quota আর throttling, **request validation**, আর AWS WAF-এর সাথে যুক্ত হওয়া, এগুলো শুধু **REST API**-তেই পাওয়া যায়। Caching, private endpoint আর resource policy-ও তাই। HTTP API দামে সস্তা, latency-ও কম, আর এতে নিজস্ব JWT authorizer আছে; কিন্তু এই API management-এর সুবিধাগুলো এতে নেই।
        """,
        ex_en=r"""
            - **Option 1 is the tempting trap.** "HTTP APIs are the newer, cheaper option" is true, but they don't support API keys, usage plans, request validation or WAF. Choose HTTP APIs for simple JWT-protected backends (for example a SPA calling Lambda with Cognito or Auth0 tokens).
            - Options 3 and 4 have no built-in API keys, quotas or schema validation. You'd have to rebuild API management yourself.
            - **API keys identify and meter clients. They don't authenticate them.** Keys are easy to leak, so pair them with a real authorizer: IAM (SigV4), a Cognito user pool authorizer, or a Lambda authorizer.
            - **Throttling layers:** an account-level Region limit, stage and method throttles, and per-key limits from usage plans. Clients over the limit get `429 Too Many Requests` and should back off and retry.
        """,
        ex_bn=r"""
            - **Option 1 হলো আকর্ষণীয় ফাঁদ।** "HTTP API নতুন আর সস্তা" কথাটা সত্য, কিন্তু এতে API key, usage plan, request validation বা WAF নেই। সহজ JWT-সুরক্ষিত backend-এর জন্য HTTP API বেছে নাও (যেমন Cognito বা Auth0 token দিয়ে Lambda call করা SPA)।
            - Option 3 আর 4-এ built-in API key, quota বা schema validation নেই। API management পুরোটা নিজেকে আবার বানাতে হবে।
            - **API key client চেনে আর মাপে, authenticate করে না।** Key সহজে leak হয়, তাই সাথে আসল authorizer দাও: IAM (SigV4), Cognito user pool authorizer, বা Lambda authorizer।
            - **Throttling-এর স্তর:** account-level Region limit, stage আর method throttle, আর usage plan থেকে per-key limit। Limit পার হলে client `429 Too Many Requests` পায়, তখন তাকে backoff করে retry করতে হবে।
        """,
        tip_en=r"""Say the rule of thumb: "HTTP API for simple, cheap proxies with JWT; REST API when I need API management: keys, usage plans, validation, WAF, caching". Then add that API keys aren't authentication.""",
        tip_bn=r"""নিয়মটা বলো: "JWT-সহ সহজ, সস্তা proxy-র জন্য HTTP API; API management (key, usage plan, validation, WAF, caching) লাগলে REST API"। তারপর যোগ করো যে API key authentication না।""",
        related=["aws-010", "aws-031"],
        refs=[APIGW_CHOOSE, APIGW_THROTTLE],
    ),
    # ------------------------------------------------------------------ aws-030
    Q(
        id="aws-030", sub="Disaster Recovery (RPO/RTO)", diff="extreme", type="system-design",
        prio="high", market="international", mins=20,
        tags=["disaster-recovery", "rpo-rto", "multi-region", "aurora-global-database", "fintech"],
        ver="AWS (2026): Aurora Global Database, DynamoDB global tables, S3 CRR, AWS Backup, Route 53 / ARC", vs=True, status="stable",
        q_en=r"""Design a multi-Region disaster recovery strategy for a fintech payment platform: Node.js services on ECS, Aurora PostgreSQL, S3 for receipts, and DynamoDB for idempotency keys. The business requires **RPO ≤ 1 minute and RTO ≤ 15 minutes** for payments, and accepts looser targets for reporting. Which DR strategy do you pick, and how do you handle data, failover, failback and testing?""",
        q_bn=r"""একটা fintech payment platform-এর জন্য multi-Region disaster recovery strategy design করো: ECS-এ Node.js service, Aurora PostgreSQL, receipt-এর জন্য S3, আর idempotency key-র জন্য DynamoDB। Business payment-এর জন্য **RPO ≤ ১ মিনিট আর RTO ≤ ১৫ মিনিট** চায়, আর reporting-এর জন্য ঢিলেঢালা target মেনে নেয়। কোন DR strategy বেছে নেবে, আর data, failover, failback ও testing কীভাবে সামলাবে?""",
        a_en=r"""
            *Advanced material.* **Clarify first:** RPO/RTO per capability (payments vs reporting vs admin), data-residency or regulatory limits on which Regions are allowed, dependencies on payment networks and banks, and budget.

            **Strategy spectrum** (cheapest → fastest): *backup & restore* (RPO/RTO in hours) → *pilot light* (data replicated, compute mostly off; RTO tens of minutes or more) → *warm standby* (a smaller but fully working copy; RTO minutes) → *multi-site active/active* (near-zero RTO, highest cost and complexity).

            **My choice: warm standby for the payment path, and backup & restore for reporting.** Active/active for a payment ledger means multi-writer conflict handling, which I'd avoid unless the business truly needs near-zero RTO.

            **Data:**
            - **Aurora Global Database:** storage-level replication to the DR Region, with lag typically in seconds, which meets RPO ≤ 1 minute. Use *switchover* for planned moves (RPO 0) and *failover* for real outages (RPO = lag at failure). Aurora PostgreSQL can even enforce a maximum lag with `rds.global_db_rpo`, blocking commits rather than exceeding it.
            - **DynamoDB global tables** for idempotency keys. The default mode (MREC) is eventually consistent with last-writer-wins, so a duplicate could slip through inside the replication window. Back that up with the payment provider's own idempotency keys, or pick the multi-Region strong consistency mode (MRSC) when the table is created. MRSC has its own constraints: exactly three Regions (or two replicas plus a witness), and no TTL or transactions, so key expiry needs another approach.
            - **S3 Cross-Region Replication** (with Replication Time Control for a predictable SLA), replica secrets in Secrets Manager, multi-Region KMS keys, and ECR replication.
            - **AWS Backup** with cross-Region *and* cross-account copies plus Vault Lock. Replication also copies corruption and bad deletes, so point-in-time backups are still required.

            **Compute and traffic:** the same IaC pipeline deploys both Regions. The DR Region runs ECS at minimum size, with quotas raised in advance. Traffic moves through Route 53 failover records with health checks, or Application Recovery Controller routing controls for a deliberate, human-approved switch.
        """,
        a_bn=r"""
            *Advanced বিষয়।* **আগে প্রশ্ন করে পরিষ্কার হও:** প্রতিটা capability-র RPO/RTO (payment, reporting, admin আলাদা), কোন Region ব্যবহার করা যাবে তার data-residency বা regulatory সীমা, payment network আর bank-এর উপর dependency, আর budget।

            **Strategy-র spectrum** (সবচেয়ে সস্তা → সবচেয়ে দ্রুত): *backup & restore* (RPO/RTO ঘণ্টায়) → *pilot light* (data replicated, compute প্রায় বন্ধ; RTO কয়েক দশ মিনিট বা বেশি) → *warm standby* (ছোট কিন্তু পুরোপুরি চালু একটা copy; RTO মিনিটে) → *multi-site active/active* (প্রায় শূন্য RTO, খরচ আর জটিলতা সবচেয়ে বেশি)।

            **আমার পছন্দ: payment path-এর জন্য warm standby, reporting-এর জন্য backup & restore।** Payment ledger-এ active/active মানে multi-writer conflict সামলানো, তাই business-এর সত্যিই প্রায় শূন্য RTO না লাগলে আমি এটা এড়িয়ে চলব।

            **Data:**
            - **Aurora Global Database:** DR Region-এ storage-level replication, lag সাধারণত কয়েক second, যা RPO ≤ ১ মিনিট পূরণ করে। পরিকল্পিত সরানোর জন্য *switchover* (RPO 0), আসল outage-এ *failover* (RPO = failure-এর মুহূর্তের lag)। Aurora PostgreSQL `rds.global_db_rpo` দিয়ে সর্বোচ্চ lag বেঁধেও দিতে পারে; সীমা পার হওয়ার বদলে commit আটকে দেয়।
            - Idempotency key-র জন্য **DynamoDB global table**। Default mode (MREC) eventually consistent, last-writer-wins, তাই replication-এর ফাঁকে একটা duplicate ঢুকে যেতে পারে। এর পেছনে payment provider-এর নিজস্ব idempotency key রাখো, অথবা table তৈরির সময়েই multi-Region strong consistency mode (MRSC) বেছে নাও। MRSC-এর নিজস্ব সীমাবদ্ধতা আছে: ঠিক তিনটা Region লাগে (বা দুইটা replica আর একটা witness), আর TTL বা transaction support করে না, তাই key expire করার অন্য উপায় লাগবে।
            - **S3 Cross-Region Replication** (নির্দিষ্ট SLA-র জন্য Replication Time Control-সহ), Secrets Manager-এ replica secret, multi-Region KMS key, আর ECR replication।
            - Cross-Region *আর* cross-account copy আর Vault Lock-সহ **AWS Backup**। Replication corruption আর ভুল delete-ও copy করে, তাই point-in-time backup তবুও লাগবে।

            **Compute আর traffic:** একই IaC pipeline দুই Region-এই deploy করে। DR Region-এ ECS চলে সর্বনিম্ন size-এ, quota আগে থেকেই বাড়ানো। Traffic সরে health check-সহ Route 53 failover record দিয়ে, অথবা ইচ্ছাকৃত, মানুষের অনুমোদিত switch-এর জন্য Application Recovery Controller-এর routing control দিয়ে।
        """,
        ex_en=r"""
            **Failover runbook (target ≤ 15 minutes):**
            1. *Detect:* alarms plus synthetic payment canaries. An incident commander decides. Automatic failover for payments risks flapping and split-brain.
            2. *Fence the old primary:* stop writes there (routing control off, writers scaled to zero) so two Regions never accept payments at the same time.
            3. *Promote:* run the Aurora global database failover. The secondary becomes the writer.
            4. *Scale:* raise ECS desired counts in the DR Region.
            5. *Shift traffic,* then *verify* with synthetic transactions.
            6. *Reconcile* in-flight payments using idempotency keys and settlement reports from the payment provider.

            **Failback:** rebuild replication toward the original Region, then do a planned *switchover* (RPO 0) in a quiet window.

            **Testing:** an untested DR plan is a hope, not a plan. Run regular game days, inject failures with AWS Fault Injection Service, and *measure* the real RTO and RPO against the targets.

            **Trade-offs:** warm standby roughly doubles some fixed costs (replicated storage, minimum compute, cross-Region transfer). Justify it against the cost of downtime per minute and regulatory exposure. Remember dependencies outside AWS: payment gateways, banks, DNS providers and third-party APIs must also work from the DR Region (IP allow-lists are a common surprise).
        """,
        ex_bn=r"""
            **Failover runbook (target ≤ ১৫ মিনিট):**
            1. *Detect:* alarm আর synthetic payment canary। সিদ্ধান্ত নেয় একজন incident commander। Payment-এ automatic failover-এ flapping আর split-brain-এর ঝুঁকি থাকে।
            2. *পুরনো primary-কে fence করো:* সেখানে write বন্ধ করো (routing control off, writer শূন্যে scale), যাতে দুই Region কখনো একসাথে payment না নেয়।
            3. *Promote:* Aurora global database failover চালাও। Secondary writer হয়ে যায়।
            4. *Scale:* DR Region-এ ECS-এর desired count বাড়াও।
            5. *Traffic সরাও,* তারপর synthetic transaction দিয়ে *যাচাই* করো।
            6. চলমান payment-গুলো idempotency key আর payment provider-এর settlement report দিয়ে *reconcile* করো।

            **Failback:** মূল Region-এর দিকে আবার replication তৈরি করো, তারপর চুপচাপ সময়ে একটা পরিকল্পিত *switchover* (RPO 0) করো।

            **Testing:** test না করা DR plan আসলে plan না, আশা মাত্র। নিয়মিত game day চালাও, AWS Fault Injection Service দিয়ে failure inject করো, আর আসল RTO ও RPO target-এর সাথে *মেপে* দেখো।

            **Trade-off:** warm standby কিছু fixed খরচ প্রায় দ্বিগুণ করে (replicated storage, সর্বনিম্ন compute, cross-Region transfer)। প্রতি মিনিট downtime-এর খরচ আর regulatory ঝুঁকির সাথে তুলনা করে এটা justify করো। AWS-এর বাইরের dependency মনে রাখো: payment gateway, bank, DNS provider আর third-party API-কেও DR Region থেকে কাজ করতে হবে (IP allow-list প্রায়ই চমক দেয়)।
        """,
        tip_en=r"""Map the RPO/RTO numbers to a named strategy (warm standby) and justify why not active/active. Then walk through the runbook, including **fencing** and **reconciliation**. Mentioning split-brain and idempotency during failover is what makes a fintech answer convincing.""",
        tip_bn=r"""RPO/RTO-র সংখ্যাগুলোকে একটা নির্দিষ্ট strategy-র (warm standby) সাথে মেলাও, আর কেন active/active না সেটা যুক্তি দিয়ে বলো। তারপর **fencing** আর **reconciliation**-সহ runbook ধরে এগোও। Failover-এর সময় split-brain আর idempotency-র কথা বললেই fintech উত্তর বিশ্বাসযোগ্য হয়।""",
        mist_en=r"""Saying "Multi-AZ is our DR", treating replication as a backup (it replicates deletes and corruption too), choosing automatic DNS failover for a payment ledger without fencing, or never testing the plan.""",
        mist_bn=r""""Multi-AZ-ই আমাদের DR" বলা, replication-কে backup ভাবা (এটা delete আর corruption-ও replicate করে), fencing ছাড়া payment ledger-এ automatic DNS failover বেছে নেওয়া, বা plan কখনো test না করা।""",
        code=r"""
            Normal operation — primary ap-south-1, DR ap-southeast-1 (warm standby)

                              Route 53 / ARC routing control
                                     │ (primary active)
                 ┌───────────────────┴────────────────────┐
                 ▼                                        ▼
            ap-south-1 (active)                     ap-southeast-1 (warm standby)
             ECS services: full size                  ECS services: minimum size (same images, ECR replication)
             Aurora Global DB: writer        ──►      Aurora secondary cluster (read-only, lag ~seconds)
             DynamoDB global table           ◄─►      DynamoDB replica
             S3 receipts                     ──►      S3 CRR (+ Replication Time Control)
             Secrets / KMS                   ──►      replica secrets, multi-Region keys
             AWS Backup vault                ──►      cross-Region + cross-account copies (Vault Lock)

            Failover runbook (target ≤ 15 min)
             1. Detect  : alarms + synthetic payment canaries → incident commander decides
             2. Fence   : stop writes in the primary (routing control off / writers scaled to 0)
             3. Promote : Aurora global database failover → secondary becomes writer
             4. Scale   : raise ECS desired counts in the DR Region (quotas pre-approved)
             5. Shift   : ARC routing control / Route 53 failover → DR Region
             6. Verify  : synthetic transactions; reconcile in-flight payments by idempotency key
             7. Later   : rebuild replication, planned switchover back (failback, RPO 0)
        """,
        lang="text",
        follow=[
            ("How do you prevent both Regions from accepting payments at the same time during a failover?", "Failover-এর সময় দুই Region একসাথে payment নেওয়া কীভাবে ঠেকাবে?"),
            ("Why isn't cross-Region replication a substitute for backups?", "Cross-Region replication কেন backup-এর বিকল্প না?"),
            ("How would the design change if the regulator requires all data to stay in one country?", "Regulator যদি বলে সব data একটা দেশের ভেতরেই রাখতে হবে, তাহলে design কীভাবে বদলাবে?"),
        ],
        related=["aws-018", "aws-023", "aws-031"],
        refs=[DR_WP, AURORA_GLOBAL_DR, AWS_BACKUP],
    ),
    # ------------------------------------------------------------------ aws-031
    Q(
        id="aws-031", sub="Event-Driven Architecture", diff="extreme", type="system-design",
        prio="high", market="international", mins=18,
        tags=["sqs", "sns", "eventbridge", "idempotency", "dlq"],
        ver="Amazon SQS / SNS / EventBridge; AWS Lambda nodejs24.x; AWS SDK for JavaScript v3", vs=True, status="stable",
        q_en=r"""Design an event-driven order flow on AWS: when an order is placed, payment capture, inventory reservation, email notification and analytics must all happen asynchronously. Use SQS, SNS and/or EventBridge with Lambda. How do you guarantee correctness when messages are delivered more than once, fail repeatedly, or arrive out of order?""",
        q_bn=r"""AWS-এ একটা event-driven order flow design করো: order place হলে payment capture, inventory reservation, email notification আর analytics, সবকিছু asynchronously হতে হবে। Lambda-র সাথে SQS, SNS আর/অথবা EventBridge ব্যবহার করো। Message একাধিকবার deliver হলে, বারবার fail করলে, বা ভুল ক্রমে এলে correctness কীভাবে নিশ্চিত করবে?""",
        a_en=r"""
            *Advanced material.*

            **Flow:** the Order API writes the order **and** an `OrderPlaced` event atomically using a **transactional outbox** (an outbox table relayed to the bus, or DynamoDB Streams through EventBridge Pipes). This avoids the "saved the order but failed to publish" dual-write bug. Events go to an **EventBridge** bus (content-based rules, archive and replay) or an **SNS** topic, and fan out to **one SQS queue per consumer** (payments, inventory, email, analytics), each read by a Lambda function. A queue per consumer isolates failures and lets each consumer scale, retry and be redriven on its own.

            **Correctness:**
            - **At-least-once delivery** (SQS standard, SNS, EventBridge) means every consumer must be **idempotent**. Store an idempotency key such as `step#orderId` with a conditional write (DynamoDB `attribute_not_exists`) or a unique constraint, and pass idempotency keys to the payment provider.
            - **Retries and DLQs:** an SQS redrive policy (`maxReceiveCount` ≥ 5) sends poison messages to a **dead-letter queue**. Alarm on DLQ depth, fix, then redrive. Set the queue visibility timeout to **at least 6× the function timeout**. Enable **partial batch responses** (`ReportBatchItemFailures`) so one bad message doesn't make the whole batch retry. EventBridge targets get their own retry policy and DLQ.
            - **Ordering:** standard queues don't guarantee order. Make updates commutative or versioned (ignore an event older than the stored version), or use **SQS FIFO** with `MessageGroupId = orderId` for per-order ordering and 5-minute deduplication, at lower throughput.
            - **Back-pressure:** set **maximum concurrency** on the SQS event source (or reserved concurrency) so a backlog doesn't overwhelm the database or the payment API.
            - **Multi-step consistency:** use a **saga**. If inventory fails after payment succeeded, run a compensating refund, orchestrated with Step Functions or choreographed with events.
            - **Observability:** correlation IDs in event metadata, tracing, and alarms on `ApproximateAgeOfOldestMessage`, DLQ depth and Lambda errors/throttles.
        """,
        a_bn=r"""
            *Advanced বিষয়।*

            **Flow:** Order API **transactional outbox** দিয়ে order **আর** `OrderPlaced` event একসাথে atomically লেখে (bus-এ relay হওয়া একটা outbox table, বা EventBridge Pipes দিয়ে DynamoDB Streams)। এতে "order save হলো কিন্তু publish fail করল" ধরনের dual-write bug এড়ানো যায়। Event যায় একটা **EventBridge** bus-এ (content-based rule, archive আর replay) বা **SNS** topic-এ, তারপর fan-out হয়ে **প্রতিটা consumer-এর জন্য একটা SQS queue**-তে (payments, inventory, email, analytics), প্রতিটা একটা Lambda function পড়ে। Consumer-প্রতি queue failure আলাদা রাখে, আর প্রতিটা consumer আলাদাভাবে scale, retry আর redrive হতে পারে।

            **Correctness:**
            - **At-least-once delivery** (SQS standard, SNS, EventBridge) মানে প্রতিটা consumer-কে **idempotent** হতে হবে। `step#orderId`-এর মতো idempotency key conditional write (DynamoDB `attribute_not_exists`) বা unique constraint দিয়ে রাখো, আর payment provider-কেও idempotency key পাঠাও।
            - **Retry আর DLQ:** SQS redrive policy (`maxReceiveCount` ≥ 5) poison message-কে **dead-letter queue**-তে পাঠায়। DLQ depth-এ alarm দাও, ঠিক করো, তারপর redrive করো। Queue-এর visibility timeout রাখো **function timeout-এর অন্তত ৬ গুণ**। **Partial batch response** (`ReportBatchItemFailures`) চালু করো, যাতে একটা খারাপ message-এর জন্য পুরো batch আবার retry না হয়। EventBridge target-এর নিজস্ব retry policy আর DLQ থাকে।
            - **Ordering:** standard queue order guarantee দেয় না। Update-গুলো commutative বা versioned করো (stored version-এর চেয়ে পুরনো event উপেক্ষা করো), অথবা **SQS FIFO**-তে `MessageGroupId = orderId` দিয়ে প্রতি order-এ ordering আর ৫ মিনিটের deduplication নাও, কম throughput মেনে নিয়ে।
            - **Back-pressure:** SQS event source-এ **maximum concurrency** (বা reserved concurrency) set করো, যাতে জমে থাকা message database বা payment API-কে ডুবিয়ে না দেয়।
            - **Multi-step consistency:** **saga** ব্যবহার করো। Payment সফল হওয়ার পরে inventory fail করলে compensating refund চালাও, Step Functions দিয়ে orchestrate করে বা event দিয়ে choreograph করে।
            - **Observability:** event metadata-তে correlation ID, tracing, আর `ApproximateAgeOfOldestMessage`, DLQ depth ও Lambda error/throttle-এ alarm।
        """,
        ex_en=r"""
            **About the code below:** it's a simplified consumer. It claims an idempotency key, performs the side effect, marks the key completed, and reports only failed messages. It has a known gap: if the function crashes *after* claiming the key but *before* finishing, the key stays `IN_PROGRESS` and retries skip it. Production implementations (for example the Powertools for AWS Lambda idempotency utility) store an in-progress expiry and the saved result, so a stuck claim can be retried and duplicates get the original response. The strongest defence is making the side effect itself idempotent: a unique `(order_id)` constraint on the reservation table, or the payment provider's idempotency key.

            **Why key on `orderId` and not the event ID?** A producer retry can publish the *same business event* twice with *different* event IDs. Deduplicate on business identity.

            **EventBridge vs SNS:** EventBridge offers rich content filtering, schema discovery, archive/replay and many SaaS and AWS sources. SNS offers very high-throughput fan-out and FIFO topics. Both pair well with SQS queues in front of each consumer, which buffer and absorb bursts.
        """,
        ex_bn=r"""
            **নিচের code সম্পর্কে:** এটা একটা সরল consumer। এটা idempotency key claim করে, side effect চালায়, key completed mark করে, আর শুধু fail করা message report করে। এর একটা জানা ফাঁক আছে: key claim করার *পরে* কিন্তু কাজ শেষ করার *আগে* function crash করলে key `IN_PROGRESS` অবস্থায় থেকে যায়, আর retry সেটাকে skip করে। Production implementation (যেমন Powertools for AWS Lambda-র idempotency utility) in-progress expiry আর সংরক্ষিত result রাখে, ফলে আটকে থাকা claim আবার retry করা যায় আর duplicate-রা আগের response-ই পায়। সবচেয়ে শক্ত সুরক্ষা হলো side effect-টাকেই idempotent বানানো: reservation table-এ `(order_id)`-এর উপর unique constraint, বা payment provider-এর idempotency key।

            **Event ID-র বদলে `orderId`-এ key কেন?** Producer retry করলে *একই business event* *ভিন্ন* event ID-সহ দুইবার publish হতে পারে। তাই business identity দিয়ে deduplicate করো।

            **EventBridge বনাম SNS:** EventBridge দেয় সমৃদ্ধ content filtering, schema discovery, archive/replay আর অনেক SaaS ও AWS source। SNS দেয় খুব বেশি throughput-এর fan-out আর FIFO topic। দুটোই প্রতিটা consumer-এর সামনে SQS queue-এর সাথে ভালো মেলে, যা burst সামলে buffer করে।
        """,
        tip_en=r"""State the core assumption first: "delivery is at-least-once, so every consumer is idempotent". Then cover retries/DLQ, ordering, back-pressure and sagas in that order. Pointing out the outbox pattern and the crash-after-claim gap marks a senior answer.""",
        tip_bn=r"""আগে মূল অনুমানটা বলো: "delivery at-least-once, তাই প্রতিটা consumer idempotent"। তারপর এই ক্রমে বলো: retry/DLQ, ordering, back-pressure, saga। Outbox pattern আর claim-এর পরে crash হওয়ার ফাঁকটা ধরিয়ে দিলে উত্তরটা senior মানের হয়।""",
        mist_en=r"""Assuming SQS standard or EventBridge delivers exactly once, using one shared queue for all consumers, setting the visibility timeout shorter than the function timeout, or throwing an error for the whole batch when one message fails.""",
        mist_bn=r"""SQS standard বা EventBridge exactly-once deliver করে ধরে নেওয়া, সব consumer-এর জন্য একটাই shared queue, function timeout-এর চেয়ে কম visibility timeout, বা একটা message fail করলে পুরো batch-এর জন্য error throw করা।""",
        code=r"""
            // inventory-consumer — runtime nodejs24.x
            // SQS event source mapping with ReportBatchItemFailures enabled; queue fed by an EventBridge rule
            import {
              DynamoDBClient, PutItemCommand, UpdateItemCommand, DeleteItemCommand,
            } from "@aws-sdk/client-dynamodb";
            import { reserveInventory } from "./inventory.js"; // should itself be idempotent (unique order_id)

            const ddb = new DynamoDBClient({});
            const TABLE = process.env.IDEMPOTENCY_TABLE;

            const claim = (pk) => ddb.send(new PutItemCommand({
              TableName: TABLE,
              Item: {
                pk: { S: pk },
                status: { S: "IN_PROGRESS" },
                expiresAt: { N: String(Math.floor(Date.now() / 1000) + 7 * 24 * 3600) }, // DynamoDB TTL
              },
              ConditionExpression: "attribute_not_exists(pk)",
            }));
            const complete = (pk) => ddb.send(new UpdateItemCommand({
              TableName: TABLE,
              Key: { pk: { S: pk } },
              UpdateExpression: "SET #s = :done",
              ExpressionAttributeNames: { "#s": "status" }, // "status" is a reserved word
              ExpressionAttributeValues: { ":done": { S: "COMPLETED" } },
            }));
            const release = (pk) => ddb.send(new DeleteItemCommand({ TableName: TABLE, Key: { pk: { S: pk } } }));

            export const handler = async (event) => {
              const batchItemFailures = [];

              for (const record of event.Records) {
                const { detail } = JSON.parse(record.body);       // EventBridge event delivered via SQS
                const pk = `reserve-inventory#${detail.orderId}`;  // business identity, not event id

                try {
                  await claim(pk);
                } catch (err) {
                  if (err.name === "ConditionalCheckFailedException") continue; // duplicate → already handled
                  batchItemFailures.push({ itemIdentifier: record.messageId });
                  continue;
                }

                try {
                  await reserveInventory(detail.orderId, detail.items);
                  await complete(pk);
                } catch (err) {
                  console.error(JSON.stringify({ msg: "reserve failed", orderId: detail.orderId, err: err.message }));
                  await release(pk);                                // allow the retry to run again
                  batchItemFailures.push({ itemIdentifier: record.messageId });
                }
              }

              // Only failed messages return to the queue (→ DLQ after maxReceiveCount)
              return { batchItemFailures };
            };
        """,
        lang="javascript",
        follow=[
            ("How would you replay a day's worth of events after fixing a consumer bug?", "Consumer-এর bug ঠিক করার পরে এক দিনের event আবার কীভাবে replay করবে?"),
            ("When would you choose Step Functions orchestration over event choreography?", "কখন event choreography-র বদলে Step Functions orchestration বেছে নেবে?"),
            ("How do you avoid the dual-write problem between the database and the event bus?", "Database আর event bus-এর মধ্যে dual-write সমস্যা কীভাবে এড়াবে?"),
        ],
        related=["aws-010", "aws-025", "aws-030"],
        refs=[LAMBDA_SQS, SQS_DLQ, BUILDERS_IDEMPOTENCY],
    ),
    # ------------------------------------------------------------------ aws-032
    Q(
        id="aws-032", sub="Multi-Account Security & Organizations", diff="extreme", type="architecture",
        prio="medium", market="international", mins=15,
        tags=["organizations", "scp", "identity-center", "control-tower", "multi-account"],
        ver="AWS Organizations (SCPs, RCPs), IAM Identity Center, AWS Control Tower (2026)", vs=True, status="stable",
        q_en=r"""Your company runs dev, staging and production for several products in **one AWS account with shared IAM users**. Design a secure multi-account setup with AWS Organizations. How would you use SCPs, IAM Identity Center, centralised logging and guardrails, and what pitfalls would you watch for during the migration?""",
        q_bn=r"""তোমার company কয়েকটা product-এর dev, staging আর production সব চালায় **একটা AWS account-এ, shared IAM user দিয়ে**। AWS Organizations দিয়ে একটা secure multi-account setup design করো। SCP, IAM Identity Center, centralised logging আর guardrail কীভাবে ব্যবহার করবে, আর migration-এর সময় কোন ফাঁদগুলোর দিকে নজর রাখবে?""",
        a_en=r"""
            *Advanced material.* **Why multiple accounts:** an account is AWS's strongest isolation boundary. You get a smaller blast radius, separate service quotas, clean billing per product or environment, and simpler IAM inside each account.

            **Structure (OUs):**
            - **Management account:** Organizations and billing only. No workloads, and very few people.
            - **Security OU:** a *Log Archive* account (organisation CloudTrail, Config and VPC Flow Logs into locked S3 buckets with Object Lock), and a *Security Tooling/Audit* account (delegated admin for GuardDuty, Security Hub, IAM Access Analyzer).
            - **Infrastructure OU:** shared networking (Transit Gateway, centralised egress and inspection, IPAM) and shared services (CI/CD, ECR).
            - **Workloads OU:** *Prod* and *Non-Prod* sub-OUs, with one account per product per environment. Plus a **Sandbox** OU with budgets and a **Suspended** OU for closing accounts.
            - **AWS Control Tower** can set up this landing zone, its controls and an account factory. Alternatively, build it with Organizations plus IaC.

            **Identity:** **IAM Identity Center** connected to the corporate IdP (Google Workspace, Entra ID, Okta) with MFA. **Permission sets** (ReadOnly, Developer, Admin) are assigned per account and group, and everyone gets short-lived credentials. No IAM users. A small number of monitored break-glass credentials (hardware MFA) cover emergencies. CI/CD uses an OIDC role in each target account.

            **Guardrails:**
            - **SCPs** set the *maximum* permissions in member accounts. Typical denies: leaving the organisation, disabling CloudTrail, GuardDuty or Config, unapproved Regions, creating IAM users or access keys, and root-user actions.
            - **Resource control policies (RCPs)** and `aws:PrincipalOrgID` conditions build a *data perimeter*, so S3 buckets and KMS keys are only usable by your organisation's principals.
            - Tag policies, backup policies and declarative policies (for example enforcing EC2 settings such as IMDS defaults) add consistency.
        """,
        a_bn=r"""
            *Advanced বিষয়।* **কেন একাধিক account:** AWS-এ account হলো সবচেয়ে শক্ত isolation boundary। এতে blast radius ছোট হয়, service quota আলাদা হয়, product বা environment অনুযায়ী billing পরিষ্কার থাকে, আর প্রতিটা account-এর ভেতরে IAM সহজ হয়।

            **কাঠামো (OU):**
            - **Management account:** শুধু Organizations আর billing। কোনো workload নেই, access খুব অল্প কয়েকজনের।
            - **Security OU:** একটা *Log Archive* account (organisation CloudTrail, Config আর VPC Flow Logs, Object Lock-সহ locked S3 bucket-এ), আর একটা *Security Tooling/Audit* account (GuardDuty, Security Hub, IAM Access Analyzer-এর delegated admin)।
            - **Infrastructure OU:** shared networking (Transit Gateway, centralised egress ও inspection, IPAM) আর shared service (CI/CD, ECR)।
            - **Workloads OU:** *Prod* আর *Non-Prod* sub-OU, প্রতিটা product-এর প্রতিটা environment-এর জন্য একটা account। সাথে budget-সহ একটা **Sandbox** OU, আর account বন্ধ করার জন্য **Suspended** OU।
            - **AWS Control Tower** এই landing zone, এর control আর account factory setup করে দিতে পারে। বিকল্প হিসেবে Organizations আর IaC দিয়ে নিজে বানাও।

            **Identity:** corporate IdP-র (Google Workspace, Entra ID, Okta) সাথে যুক্ত **IAM Identity Center**, MFA-সহ। **Permission set** (ReadOnly, Developer, Admin) account আর group অনুযায়ী assign করা হয়, আর সবাই short-lived credential পায়। কোনো IAM user নয়। জরুরি অবস্থার জন্য অল্প কয়েকটা monitored break-glass credential (hardware MFA)। CI/CD প্রতিটা target account-এ একটা OIDC role ব্যবহার করে।

            **Guardrail:**
            - **SCP** member account-গুলোর *সর্বোচ্চ* permission ঠিক করে দেয়। সাধারণ deny: organisation ছেড়ে যাওয়া, CloudTrail/GuardDuty/Config বন্ধ করা, অনুমোদনহীন Region, IAM user বা access key তৈরি, আর root user-এর action।
            - **Resource control policy (RCP)** আর `aws:PrincipalOrgID` condition দিয়ে *data perimeter* বানাও, যাতে S3 bucket আর KMS key শুধু তোমার organisation-এর principal-রাই ব্যবহার করতে পারে।
            - Tag policy, backup policy আর declarative policy (যেমন IMDS default-এর মতো EC2 setting enforce করা) সামঞ্জস্য আনে।
        """,
        ex_en=r"""
            **How SCPs actually behave** (frequent interview probes):
            - SCPs **never grant** permissions. They only filter. A user still needs an IAM Allow, and an action must be allowed by *every* SCP level from the root through the OUs to the account.
            - SCPs **don't apply to the management account**, which is another reason to keep workloads out of it. They *do* apply to the root user of member accounts. They don't restrict service-linked roles.
            - **Region-deny SCPs must exempt global services** (IAM, Organizations, STS, Route 53, CloudFront, Support, billing and others) with `NotAction`. The policy below shows an abbreviated list. Start from AWS's published example and test it.
            - SCPs have size and attachment-count quotas, so keep them focused and composable.

            **Migration pitfalls:** test SCPs on a test OU before attaching them to Prod. Move one workload at a time, with resources recreated by IaC rather than copied by hand. Re-plan non-overlapping CIDRs for Transit Gateway. Watch cross-account access (bucket policies, KMS key policies) that used to work implicitly inside one account. Rotate and delete the old shared IAM users last, after confirming nothing still uses them (IAM last-accessed data, CloudTrail).
        """,
        ex_bn=r"""
            **SCP আসলে কীভাবে আচরণ করে** (interview-তে প্রায়ই জিজ্ঞেস করা হয়):
            - SCP **কখনো permission দেয় না**, শুধু filter করে। User-এর তবুও IAM Allow লাগে, আর root থেকে OU হয়ে account পর্যন্ত *প্রতিটা* SCP level-কে action-টা allow করতে হবে।
            - SCP **management account-এ প্রযোজ্য না**, workload সেখানে না রাখার আরেকটা কারণ। Member account-এর root user-এর উপর *প্রযোজ্য*। Service-linked role-কে সীমিত করে না।
            - **Region-deny SCP-তে global service-গুলো বাদ দিতে হয়** (IAM, Organizations, STS, Route 53, CloudFront, Support, billing ইত্যাদি) `NotAction` দিয়ে। নিচের policy-তে তালিকাটা সংক্ষিপ্ত। AWS-এর প্রকাশিত উদাহরণ থেকে শুরু করে test করো।
            - SCP-এর size আর কতগুলো attach করা যায় তার quota আছে, তাই এগুলো focused আর composable রাখো।

            **Migration-এর ফাঁদ:** Prod-এ attach করার আগে একটা test OU-তে SCP test করো। একবারে একটা workload সরাও, resource হাতে copy না করে IaC দিয়ে নতুন করে বানাও। Transit Gateway-এর জন্য non-overlapping CIDR নতুন করে plan করো। আগে একটা account-এর ভেতরে implicitly চলত এমন cross-account access-এর (bucket policy, KMS key policy) দিকে নজর রাখো। পুরনো shared IAM user-গুলো সবার শেষে rotate করে delete করো, আগে নিশ্চিত হয়ে নাও কেউ আর ব্যবহার করছে না (IAM last-accessed data, CloudTrail)।
        """,
        tip_en=r"""Start with *why* (blast radius, isolation), then draw the OU tree, then identity, then guardrails. Being precise that "SCPs don't grant permissions and don't apply to the management account" is the detail that separates real experience from buzzwords.""",
        tip_bn=r"""শুরু করো *কেন* দিয়ে (blast radius, isolation), তারপর OU tree আঁকো, তারপর identity, তারপর guardrail। "SCP permission দেয় না আর management account-এ প্রযোজ্য না", এই কথাটা নিখুঁতভাবে বলতে পারলেই বোঝা যায় তোমার সত্যিকারের অভিজ্ঞতা আছে, শুধু buzzword না।""",
        mist_en=r"""Running workloads in the management account, treating SCPs as permission grants, region-deny SCPs that break IAM or CloudFront, or keeping shared IAM users "just for now" after Identity Center is live.""",
        mist_bn=r"""Management account-এ workload চালানো, SCP-কে permission দেওয়ার মাধ্যম ভাবা, এমন region-deny SCP যা IAM বা CloudFront ভেঙে দেয়, বা Identity Center চালু হওয়ার পরেও shared IAM user "আপাতত" রেখে দেওয়া।""",
        code=r"""
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "ProtectOrgAndSecurityServices",
                  "Effect": "Deny",
                  "Action": [
                    "organizations:LeaveOrganization",
                    "cloudtrail:StopLogging",
                    "cloudtrail:DeleteTrail",
                    "guardduty:DeleteDetector",
                    "guardduty:DisassociateFromAdministratorAccount",
                    "config:StopConfigurationRecorder",
                    "config:DeleteConfigurationRecorder"
                  ],
                  "Resource": "*"
                },
                {
                  "Sid": "DenyUnapprovedRegions",
                  "Effect": "Deny",
                  "NotAction": [
                    "iam:*", "organizations:*", "sts:*", "route53:*", "cloudfront:*",
                    "support:*", "budgets:*", "ce:*", "health:*", "waf:*"
                  ],
                  "Resource": "*",
                  "Condition": {
                    "StringNotEquals": { "aws:RequestedRegion": ["ap-south-1", "ap-southeast-1"] },
                    "ArnNotLike": { "aws:PrincipalArn": "arn:aws:iam::*:role/OrgBreakGlassRole" }
                  }
                },
                {
                  "Sid": "NoLongLivedIamUserCredentials",
                  "Effect": "Deny",
                  "Action": ["iam:CreateUser", "iam:CreateAccessKey"],
                  "Resource": "*",
                  "Condition": {
                    "ArnNotLike": { "aws:PrincipalArn": "arn:aws:iam::*:role/OrgBreakGlassRole" }
                  }
                }
              ]
            }
        """,
        lang="json",
        follow=[
            ("Why don't SCPs affect the management account, and what does that imply?", "SCP কেন management account-এ প্রভাব ফেলে না, আর এর মানে কী?"),
            ("How would you build a data perimeter so company data can't be copied to an outside account?", "Company-র data যেন বাইরের কোনো account-এ copy করা না যায়, সেজন্য data perimeter কীভাবে বানাবে?"),
        ],
        related=["aws-003", "aws-024", "aws-027"],
        refs=[SCPS, ORG_WP, CONTROL_TOWER],
    ),
]

if __name__ == "__main__":
    save("aws", "b5", QUESTIONS)
