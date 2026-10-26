# AWS batch 3 — aws-014 … aws-019 (presigned URLs, IAM policy JSON, secrets, VPC, RDS, load balancers)
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "tools"))
from qb import Q, save  # noqa: E402

S3_PRESIGNED = ("Amazon S3 — Download and upload objects with presigned URLs", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html")
S3_PRESIGNED_UPLOAD = ("Amazon S3 — Uploading objects with presigned URLs", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/PresignedUrlUploadObject.html")
SDK_JS_V3 = ("AWS SDK for JavaScript v3 — Developer Guide", "https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/welcome.html")
IAM_POLICIES = ("IAM — Policies and permissions", "https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html")
IAM_BP = ("IAM — Security best practices", "https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html")
S3_POLICY_EXAMPLES = ("Amazon S3 — Bucket policy examples", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html")
SM_INTRO = ("AWS Secrets Manager — What is Secrets Manager?", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html")
SM_ROTATION = ("AWS Secrets Manager — Rotate secrets", "https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html")
PARAM_STORE = ("AWS Systems Manager — Parameter Store", "https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html")
VPC_WHAT = ("Amazon VPC — What is Amazon VPC?", "https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html")
NAT_GW = ("Amazon VPC — NAT gateways", "https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html")
GW_ENDPOINTS = ("AWS PrivateLink — Gateway endpoints", "https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html")
RDS_MULTIAZ = ("Amazon RDS — Multi-AZ DB instance deployments", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html")
RDS_REPLICAS = ("Amazon RDS — Working with read replicas", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html")
RDS_PITR = ("Amazon RDS — Restoring a DB instance to a specified time", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html")
ALB = ("Elastic Load Balancing — What is an Application Load Balancer?", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html")
NLB = ("Elastic Load Balancing — What is a Network Load Balancer?", "https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html")
ELB_HOW = ("Elastic Load Balancing — How it works", "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html")

QUESTIONS = [
    # ------------------------------------------------------------------ aws-014
    Q(
        id="aws-014", sub="S3 Presigned URLs", diff="medium", type="coding",
        prio="high", market="both", mins=8,
        tags=["s3", "presigned-url", "aws-sdk-v3", "express", "file-upload"],
        ver="AWS SDK for JavaScript v3 (@aws-sdk/client-s3, @aws-sdk/s3-request-presigner); Express 5; Node.js 24", vs=True, status="stable",
        q_en=r"""
            Write an Express endpoint using AWS SDK for JavaScript v3 that returns a **presigned PUT URL**, so the browser can upload a profile picture directly to a private S3 bucket. Requirements:
            - only `image/jpeg`, `image/png` and `image/webp` are allowed;
            - the declared size must be at most 5 MB;
            - the object key must be under `uploads/<userId>/` and must not be chosen by the client;
            - the URL is valid for 5 minutes.

            Example: `POST /api/uploads/avatar` with body `{ "contentType": "image/png", "size": 48213 }` → `{ "url": "https://…X-Amz-Signature=…", "key": "uploads/42/7c9e….png" }`. Also show how the frontend uses the URL.
        """,
        q_bn=r"""
            AWS SDK for JavaScript v3 দিয়ে একটা Express endpoint লেখো, যেটা একটা **presigned PUT URL** return করবে, যাতে browser সরাসরি একটা private S3 bucket-এ profile picture upload করতে পারে। Requirement:
            - শুধু `image/jpeg`, `image/png` আর `image/webp` allow;
            - declared size সর্বোচ্চ 5 MB;
            - object key থাকবে `uploads/<userId>/`-এর ভেতরে, আর client নিজে key বেছে নিতে পারবে না;
            - URL ৫ মিনিট valid থাকবে।

            উদাহরণ: `POST /api/uploads/avatar`, body `{ "contentType": "image/png", "size": 48213 }` → `{ "url": "https://…X-Amz-Signature=…", "key": "uploads/42/7c9e….png" }`। Frontend কীভাবে URL-টা ব্যবহার করবে সেটাও দেখাও।
        """,
        a_en=r"""
            The server never touches the file bytes. It authenticates the user, validates the request, generates the key itself and signs a `PutObjectCommand` with `getSignedUrl` from `@aws-sdk/s3-request-presigner`. The browser then `PUT`s the file straight to S3.

            Key points:
            - **Credentials come from the IAM role** (instance profile, ECS task role or Lambda role). That role needs only `s3:PutObject` on `arn:aws:s3:::<bucket>/uploads/*`.
            - **Sign the Content-Type.** In SDK v3 the S3 presigner leaves `content-type` unsigned by default. Passing `signableHeaders: new Set(["content-type"])` makes S3 reject an upload whose `Content-Type` differs (`SignatureDoesNotMatch`).
            - `expiresIn: 300` seconds. A URL can't outlive the credentials that signed it, so with role credentials it may expire earlier. The SDK maximum is 7 days.
            - **The bucket needs a CORS rule** allowing `PUT` from your frontend origin, otherwise the browser blocks the request.
            - A presigned PUT **can't enforce a size range**, so the 5 MB check on the declared size is advisory. Verify after upload (`HeadObject` in a "confirm" endpoint, or an S3 event → Lambda). For hard enforcement, use a **presigned POST** with a `content-length-range` condition (`@aws-sdk/s3-presigned-post`).
        """,
        a_bn=r"""
            Server কখনো file-এর byte ছোঁয় না। সে user authenticate করে, request validate করে, নিজে key তৈরি করে, আর `@aws-sdk/s3-request-presigner`-এর `getSignedUrl` দিয়ে একটা `PutObjectCommand` sign করে। তারপর browser সরাসরি S3-এ file `PUT` করে।

            মূল বিষয়:
            - **Credential আসে IAM role থেকে** (instance profile, ECS task role বা Lambda role)। ওই role-এর শুধু `arn:aws:s3:::<bucket>/uploads/*`-এ `s3:PutObject` লাগে।
            - **Content-Type sign করো।** SDK v3-এর S3 presigner default-এ `content-type` sign করে না। `signableHeaders: new Set(["content-type"])` দিলে ভিন্ন `Content-Type`-এর upload S3 reject করে (`SignatureDoesNotMatch`)।
            - `expiresIn: 300` second। যে credential দিয়ে sign করা হয়েছে, URL তার চেয়ে বেশি দিন টেকে না; তাই role credential হলে আগেও expire হতে পারে। SDK-তে সর্বোচ্চ ৭ দিন।
            - **Bucket-এ CORS rule লাগবে**, যেটা তোমার frontend origin থেকে `PUT` allow করে; নাহলে browser request block করবে।
            - Presigned PUT **size range enforce করতে পারে না**, তাই declared size-এর 5 MB check শুধু পরামর্শমূলক। Upload-এর পরে যাচাই করো ("confirm" endpoint-এ `HeadObject`, বা S3 event → Lambda)। শক্তভাবে enforce করতে **presigned POST** ব্যবহার করো, সাথে `content-length-range` condition (`@aws-sdk/s3-presigned-post`)।
        """,
        quick_en=r"""The server validates the type and size, builds the key under `uploads/<userId>/` itself and signs a `PutObjectCommand` with `getSignedUrl` (`expiresIn: 300`, Content-Type signed); the browser then PUTs straight to S3. A presigned PUT can't enforce size, so verify after upload or use a presigned POST.""",
        quick_bn=r"""Server type আর size validate করে, `uploads/<userId>/`-এর নিচে key নিজেই বানায়, আর `getSignedUrl` দিয়ে একটা `PutObjectCommand` sign করে (`expiresIn: 300`, Content-Type signed); তারপর browser সরাসরি S3-তে PUT করে। Presigned PUT size enforce করতে পারে না, তাই upload-এর পরে verify করো বা presigned POST ব্যবহার করো।""",
        ex_en=r"""
            - **Why presigned uploads:** large files never pass through your Node process, so there's no memory or bandwidth pressure on the API and no 6 MB Lambda payload limit. S3 handles the scaling.
            - **Never let the client choose the key.** Generating it server-side (`uploads/<userId>/<uuid>.<ext>`) stops users from overwriting each other's files or writing outside their prefix.
            - **Edge cases:** the client may send a different `Content-Type` than it declared (blocked by signing it), files bigger than 5 MB (catch with the post-upload check or a presigned POST), and URL reuse within 5 minutes (harmless, because the key is unique). Also handle the user never confirming the upload: a lifecycle rule can expire objects under a `pending/` prefix.
            - Serving the images later: keep the bucket private and use CloudFront + OAC, or presigned GET URLs.
        """,
        ex_bn=r"""
            - **Presigned upload কেন:** বড় file তোমার Node process দিয়ে যায় না, তাই API-র memory বা bandwidth-এর উপর চাপ পড়ে না, Lambda-র 6 MB payload limit-ও থাকে না। Scaling-টা S3 সামলায়।
            - **Client-কে কখনো key বাছতে দিও না।** Server-side-এ key বানালে (`uploads/<userId>/<uuid>.<ext>`) একজন user আরেকজনের file overwrite করতে বা নিজের prefix-এর বাইরে লিখতে পারে না।
            - **Edge case:** client declared type-এর বদলে অন্য `Content-Type` পাঠাতে পারে (sign করলে আটকায়), 5 MB-এর বেশি file (upload-পরবর্তী check বা presigned POST দিয়ে ধরো), আর ৫ মিনিটের মধ্যে URL আবার ব্যবহার (ক্ষতি নেই, কারণ key unique)। User upload confirm না করলে কী হবে সেটাও সামলাও: `pending/` prefix-এর object lifecycle rule দিয়ে expire করা যায়।
            - পরে image serve করতে bucket private রেখে CloudFront + OAC, অথবা presigned GET URL ব্যবহার করো।
        """,
        tip_en=r"""Draw the three-step flow first (ask API → PUT to S3 → confirm). Then mention the two details most candidates miss: the bucket's CORS rule, and the fact that a presigned PUT can't enforce size (presigned POST can).""",
        tip_bn=r"""প্রথমে তিন ধাপের flow-টা বলো (API-কে জিজ্ঞেস করা → S3-এ PUT → confirm)। তারপর যে দুইটা detail বেশিরভাগ candidate মিস করে সেগুলো বলো: bucket-এর CORS rule, আর presigned PUT যে size enforce করতে পারে না (presigned POST পারে)।""",
        mist_en=r"""Uploading the file through Express with multer and then to S3 (double bandwidth), embedding access keys in the frontend, letting the client pick the key, or forgetting CORS and then debugging a "network error".""",
        mist_bn=r"""File আগে multer দিয়ে Express-এ নিয়ে তারপর S3-এ পাঠানো (bandwidth দ্বিগুণ), frontend-এ access key বসিয়ে দেওয়া, client-কে key বাছতে দেওয়া, বা CORS ভুলে গিয়ে পরে "network error" debug করা।""",
        code=r"""
            // server.js — Express 5, Node.js 24, AWS SDK for JavaScript v3
            import express from "express";
            import { randomUUID } from "node:crypto";
            import { S3Client, PutObjectCommand } from "@aws-sdk/client-s3";
            import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
            import { requireAuth } from "./auth.js"; // sets req.user

            const app = express();
            app.use(express.json());

            // No keys in code: credentials come from the IAM role via the default provider chain
            const s3 = new S3Client({ region: process.env.AWS_REGION });
            const BUCKET = process.env.UPLOAD_BUCKET;
            const ALLOWED = new Map([
              ["image/jpeg", "jpg"],
              ["image/png", "png"],
              ["image/webp", "webp"],
            ]);
            const MAX_BYTES = 5 * 1024 * 1024;

            app.post("/api/uploads/avatar", requireAuth, async (req, res) => {
              const { contentType, size } = req.body ?? {};
              const ext = ALLOWED.get(contentType);
              if (!ext) return res.status(400).json({ error: "Unsupported file type" });
              if (!Number.isInteger(size) || size <= 0 || size > MAX_BYTES) {
                return res.status(400).json({ error: "File must be between 1 byte and 5 MB" });
              }

              const key = `uploads/${req.user.id}/${randomUUID()}.${ext}`; // server-chosen key
              const command = new PutObjectCommand({
                Bucket: BUCKET,
                Key: key,
                ContentType: contentType,
              });

              const url = await getSignedUrl(s3, command, {
                expiresIn: 300,                              // seconds
                signableHeaders: new Set(["content-type"]),  // browser must send the same type
              });
              res.json({ url, key });
            });

            app.listen(3000);
        """,
        lang="javascript",
        extra=[
            dict(lang="javascript", label_en="Frontend (browser)", label_bn="Frontend (browser)", src=r"""
                async function uploadAvatar(file) {
                  const r = await fetch("/api/uploads/avatar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ contentType: file.type, size: file.size }),
                  });
                  if (!r.ok) throw new Error((await r.json()).error);
                  const { url, key } = await r.json();

                  // Direct upload to S3 — Content-Type must match the signed value
                  const put = await fetch(url, {
                    method: "PUT",
                    headers: { "Content-Type": file.type },
                    body: file,
                  });
                  if (!put.ok) throw new Error(`S3 upload failed: ${put.status}`);

                  // Tell the API the upload finished so it can verify (HeadObject) and save the key
                  await fetch("/api/users/me/avatar", {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ key }),
                  });
                }
            """),
            dict(lang="json", label_en="Bucket CORS configuration (aws s3api put-bucket-cors format)", label_bn="Bucket CORS configuration (aws s3api put-bucket-cors format)", src=r"""
                {
                  "CORSRules": [
                    {
                      "AllowedOrigins": ["https://app.example.com"],
                      "AllowedMethods": ["PUT"],
                      "AllowedHeaders": ["Content-Type"],
                      "ExposeHeaders": ["ETag"],
                      "MaxAgeSeconds": 3000
                    }
                  ]
                }
            """),
        ],
        time="O(1) per request (signing is local, no call to S3)",
        space="O(1)",
        follow=[
            ("How would you enforce the 5 MB limit at the S3 level?", "S3 level-এ 5 MB limit কীভাবে enforce করবে?"),
            ("How would you upload a 5 GB video from the browser?", "Browser থেকে একটা 5 GB video কীভাবে upload করবে?"),
            ("How do you scan uploaded files for malware before using them?", "Upload হওয়া file ব্যবহারের আগে malware scan কীভাবে করবে?"),
        ],
        related=["aws-015", "aws-007"],
        refs=[S3_PRESIGNED, S3_PRESIGNED_UPLOAD, SDK_JS_V3],
    ),
    # ------------------------------------------------------------------ aws-015
    Q(
        id="aws-015", sub="Least-Privilege IAM Policies", diff="medium", type="coding",
        prio="high", market="both", mins=6,
        tags=["iam", "least-privilege", "s3", "policy-json", "conditions"],
        ver="IAM policy language (Version 2012-10-17)", vs=False, status="stable",
        q_en=r"""
            Write an identity-based IAM policy (JSON) for an application role that may **list, read, write and delete objects only under the `uploads/` prefix** of the bucket `acme-media`, and nothing else in that bucket or account. Explain each statement.

            Expected behaviour: `GetObject` on `uploads/a.png` → allowed; `PutObject` on `private/secret.txt` → denied; `ListBucket` with prefix `uploads/` → allowed; `ListBucket` with no prefix → denied.
        """,
        q_bn=r"""
            একটা application role-এর জন্য identity-based IAM policy (JSON) লেখো, যেটা `acme-media` bucket-এর **শুধু `uploads/` prefix-এর ভেতরে object list, read, write আর delete** করতে পারবে; ওই bucket বা account-এর আর কিছুই না। প্রতিটা statement ব্যাখ্যা করো।

            Expected behaviour: `uploads/a.png`-এ `GetObject` → allowed; `private/secret.txt`-এ `PutObject` → denied; prefix `uploads/` দিয়ে `ListBucket` → allowed; prefix ছাড়া `ListBucket` → denied।
        """,
        a_en=r"""
            Two statements, because S3 actions work at two resource levels:
            1. **`s3:ListBucket` is a bucket-level action**, so its resource is the bucket ARN (`arn:aws:s3:::acme-media`), not an object ARN. I restrict *what* can be listed with the `s3:prefix` condition key (`uploads/` and `uploads/*`). A list request without a matching prefix has no matching `Allow`, so it's denied.
            2. **Object actions** (`s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`) use object ARNs, so the resource is `arn:aws:s3:::acme-media/uploads/*`.

            No `s3:*`, no `Resource: "*"`. Everything not listed is implicitly denied. If the bucket uses SSE-KMS with a customer managed key, the role also needs `kms:GenerateDataKey` (for uploads) and `kms:Decrypt` (for downloads) on that key. Without them you get AccessDenied even though the S3 policy is correct.
        """,
        a_bn=r"""
            দুইটা statement লাগে, কারণ S3 action দুই resource level-এ কাজ করে:
            1. **`s3:ListBucket` bucket-level action**, তাই এর resource হলো bucket ARN (`arn:aws:s3:::acme-media`), object ARN না। *কী* list করা যাবে সেটা `s3:prefix` condition key দিয়ে সীমিত করি (`uploads/` আর `uploads/*`)। মিলে যাওয়া prefix ছাড়া list request-এর কোনো `Allow` match করে না, তাই সেটা deny হয়।
            2. **Object action** (`s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`) object ARN ব্যবহার করে, তাই resource হলো `arn:aws:s3:::acme-media/uploads/*`।

            কোনো `s3:*` বা `Resource: "*"` নেই। যা লেখা নেই, সেটা implicitly deny। Bucket যদি customer managed key দিয়ে SSE-KMS ব্যবহার করে, তাহলে role-এর ওই key-তে `kms:GenerateDataKey` (upload-এর জন্য) আর `kms:Decrypt` (download-এর জন্য) লাগবে। এগুলো না থাকলে S3 policy ঠিক থাকলেও AccessDenied আসে।
        """,
        quick_en=r"""Use two statements: `s3:ListBucket` on the bucket ARN with an `s3:prefix` condition for `uploads/`, and `s3:GetObject`, `s3:PutObject` and `s3:DeleteObject` on `arn:aws:s3:::acme-media/uploads/*`. Everything else is implicitly denied; with SSE-KMS the role also needs `kms:GenerateDataKey` and `kms:Decrypt`.""",
        quick_bn=r"""দুটো statement লাগে: bucket ARN-এ `s3:ListBucket`, সাথে `uploads/`-এর জন্য `s3:prefix` condition; আর `arn:aws:s3:::acme-media/uploads/*`-এ `s3:GetObject`, `s3:PutObject` ও `s3:DeleteObject`। বাকি সব নিজে থেকেই deny; SSE-KMS থাকলে role-এর `kms:GenerateDataKey` আর `kms:Decrypt`-ও লাগবে।""",
        ex_en=r"""
            - **The #1 bug** is putting `ListBucket` on `arn:aws:s3:::acme-media/*` or `GetObject` on `arn:aws:s3:::acme-media`. The ARN level must match the action.
            - Versioned buckets: `s3:GetObjectVersion` and `s3:DeleteObjectVersion` are separate actions. Add them only if the app really needs version-level access.
            - **Per-user prefixes:** policy variables like `${aws:PrincipalTag/team}`, or `${cognito-identity.amazonaws.com:sub}` for Cognito identities, can generate `uploads/<user>/*` dynamically. Policy variables require `"Version": "2012-10-17"`.
            - **Validate before shipping:** IAM Access Analyzer policy validation catches syntax and security issues, and the IAM policy simulator lets you test the expected allow/deny cases listed in the question.
        """,
        ex_bn=r"""
            - **সবচেয়ে common bug:** `ListBucket` দেওয়া `arn:aws:s3:::acme-media/*`-এ, বা `GetObject` দেওয়া `arn:aws:s3:::acme-media`-এ। ARN-এর level action-এর সাথে মিলতে হবে।
            - Versioned bucket: `s3:GetObjectVersion` আর `s3:DeleteObjectVersion` আলাদা action। App-এর সত্যিই version-level access লাগলেই শুধু যোগ করো।
            - **User-ভিত্তিক prefix:** `${aws:PrincipalTag/team}`, বা Cognito identity-র জন্য `${cognito-identity.amazonaws.com:sub}`-এর মতো policy variable দিয়ে `uploads/<user>/*` dynamically তৈরি করা যায়। Policy variable-এর জন্য `"Version": "2012-10-17"` লাগে।
            - **Ship করার আগে যাচাই:** IAM Access Analyzer-এর policy validation syntax আর security সমস্যা ধরে, আর IAM policy simulator দিয়ে প্রশ্নের allow/deny case-গুলো test করা যায়।
        """,
        tip_en=r"""Explain the bucket-ARN vs object-ARN split before you write any JSON. Interviewers use this question mainly to check whether you know that distinction.""",
        tip_bn=r"""JSON লেখার আগেই bucket-ARN বনাম object-ARN-এর ভাগটা ব্যাখ্যা করো। Interviewer মূলত এই পার্থক্যটা তুমি জানো কি না সেটাই এই প্রশ্ন দিয়ে যাচাই করে।""",
        mist_en=r"""Using `"Action": "s3:*"` with `"Resource": "*"`, forgetting the KMS permissions on an SSE-KMS bucket, or thinking a `Deny` is needed to block other prefixes (they're already implicitly denied).""",
        mist_bn=r"""`"Resource": "*"`-সহ `"Action": "s3:*"` দেওয়া, SSE-KMS bucket-এ KMS permission ভুলে যাওয়া, বা ভাবা যে অন্য prefix আটকাতে `Deny` লাগবে (এগুলো তো আগে থেকেই implicitly deny)।""",
        code=r"""
            {
              "Version": "2012-10-17",
              "Statement": [
                {
                  "Sid": "ListOnlyUploadsPrefix",
                  "Effect": "Allow",
                  "Action": "s3:ListBucket",
                  "Resource": "arn:aws:s3:::acme-media",
                  "Condition": {
                    "StringLike": { "s3:prefix": ["uploads/", "uploads/*"] }
                  }
                },
                {
                  "Sid": "ObjectAccessUnderUploads",
                  "Effect": "Allow",
                  "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
                  "Resource": "arn:aws:s3:::acme-media/uploads/*"
                }
              ]
            }
        """,
        lang="json",
        time="N/A (declarative policy document)",
        space="N/A",
        follow=[
            ("How would you give each user access only to `uploads/<their-id>/`?", "প্রত্যেক user-কে শুধু `uploads/<তার-id>/`-এ access কীভাবে দেবে?"),
            ("When would you use a bucket policy instead of (or in addition to) this identity policy?", "কখন এই identity policy-র বদলে (বা সাথে) bucket policy ব্যবহার করবে?"),
        ],
        related=["aws-003", "aws-014", "aws-024"],
        refs=[IAM_POLICIES, IAM_BP, S3_POLICY_EXAMPLES],
    ),
    # ------------------------------------------------------------------ aws-016
    Q(
        id="aws-016", sub="Secrets Manager vs Parameter Store", diff="medium", type="comparison",
        prio="high", market="both", mins=5,
        tags=["secrets-manager", "parameter-store", "secrets", "kms", "configuration"],
        ver="AWS Secrets Manager / AWS Systems Manager Parameter Store (2026)", vs=False, status="stable",
        q_en=r"""How do you store environment secrets (database password, JWT secret, third-party API keys) for an app on AWS? Compare AWS Secrets Manager and SSM Parameter Store.""",
        q_bn=r"""AWS-এ একটা app-এর environment secret (database password, JWT secret, third-party API key) কীভাবে রাখবে? AWS Secrets Manager আর SSM Parameter Store-এর তুলনা করো।""",
        a_en=r"""
            First, secrets don't belong in a committed `.env`, an AMI, a Docker image or EC2 user data. I keep them in a managed store, give the app's IAM role read access to exactly those secrets, and load them at startup (cached in memory).

            - **Secrets Manager** is purpose-built for secrets. It has **built-in rotation**: managed rotation for supported databases like RDS and Aurora, or a rotation Lambda for anything else. It also gives you versioning with staging labels (`AWSCURRENT`/`AWSPREVIOUS`), cross-Region replication and resource policies. You pay per secret per month plus per API call.
            - **Parameter Store** is hierarchical key/value configuration (`/myapp/prod/DB_URL`). `SecureString` parameters are encrypted with KMS. Standard parameters have no extra storage charge (up to 4 KB each), while the Advanced tier (larger values, parameter policies) costs extra. It has **no built-in rotation**.

            My rule: credentials that should rotate (database passwords, keys shared with partners) go in Secrets Manager. Plain configuration and secrets that rarely change go in Parameter Store. ECS task definitions and Lambda can read from both.
        """,
        a_bn=r"""
            প্রথম কথা, secret কখনো commit করা `.env`, AMI, Docker image বা EC2 user data-তে থাকা উচিত না। আমি এগুলো একটা managed store-এ রাখি, app-এর IAM role-কে ঠিক ওই secret-গুলো পড়ার access দিই, আর startup-এ load করে memory-তে cache করি।

            - **Secrets Manager** secret-এর জন্যই বানানো। এতে **built-in rotation** আছে: RDS, Aurora-র মতো supported database-এর জন্য managed rotation, অন্য কিছুর জন্য rotation Lambda। আরও আছে staging label-সহ versioning (`AWSCURRENT`/`AWSPREVIOUS`), cross-Region replication আর resource policy। প্রতি secret-এর মাসিক খরচ আর প্রতি API call-এর খরচ দিতে হয়।
            - **Parameter Store** hierarchical key/value configuration (`/myapp/prod/DB_URL`)। `SecureString` parameter KMS দিয়ে encrypted থাকে। Standard parameter-এ storage-এর বাড়তি খরচ নেই (প্রতিটা 4 KB পর্যন্ত), আর Advanced tier-এ (বড় value, parameter policy) বাড়তি খরচ লাগে। এতে **built-in rotation নেই**।

            আমার নিয়ম: যে credential rotate হওয়া উচিত (database password, partner-দের সাথে শেয়ার করা key), সেটা Secrets Manager-এ। সাধারণ configuration আর কালেভদ্রে বদলায় এমন secret Parameter Store-এ। ECS task definition আর Lambda দুটো থেকেই পড়তে পারে।
        """,
        quick_en=r"""Keep secrets out of `.env` files, images and user data: store them in a managed service, give the app's IAM role read access, and load them at startup. Secrets Manager has built-in rotation and replication but costs per secret; Parameter Store `SecureString` is cheap hierarchical config with no built-in rotation.""",
        quick_bn=r"""Secret কখনো `.env`, image বা user data-তে রেখো না: managed service-এ রাখো, app-এর IAM role-কে read access দাও, আর startup-এ load করো। Secrets Manager-এ built-in rotation আর replication আছে কিন্তু প্রতি secret-এ খরচ; Parameter Store-এর `SecureString` সস্তা hierarchical config, কিন্তু built-in rotation নেই।""",
        ex_en=r"""
            - **ECS `secrets`** in a task definition (`valueFrom` = a secret or parameter ARN) are injected as environment variables when the container *starts*. After a rotation, running tasks still hold the old value until they're redeployed. Apps that must pick up rotations immediately should fetch at runtime with a short cache.
            - **Rotation without downtime:** use the alternating-users strategy, or make the app retry with a fresh fetch on an authentication failure, so the brief window where `AWSPREVIOUS` is still in use doesn't cause errors.
            - For Lambda, the AWS Parameters and Secrets Lambda Extension caches values locally, which cuts latency and API calls.
            - With a customer managed KMS key, the role also needs `kms:Decrypt` on that key to read a `SecureString` or a secret.
        """,
        ex_bn=r"""
            - Task definition-এর **ECS `secrets`** (`valueFrom` = secret বা parameter-এর ARN) container *start* হওয়ার সময় environment variable হিসেবে inject হয়। Rotation-এর পরেও চলমান task-গুলো redeploy না হওয়া পর্যন্ত পুরনো value ধরে রাখে। যে app-কে rotation সাথে সাথে নিতে হবে, তার উচিত runtime-এ ছোট cache-সহ fetch করা।
            - **Downtime ছাড়া rotation:** alternating-users strategy ব্যবহার করো, অথবা authentication fail হলে app যেন নতুন করে fetch করে retry করে। তাহলে যে অল্প সময় `AWSPREVIOUS` ব্যবহার হচ্ছে, তখন error হবে না।
            - Lambda-তে AWS Parameters and Secrets Lambda Extension value-গুলো locally cache করে, ফলে latency আর API call দুটোই কমে।
            - Customer managed KMS key ব্যবহার করলে `SecureString` বা secret পড়তে role-এর ওই key-তে `kms:Decrypt`-ও লাগবে।
        """,
        tip_en=r"""Lead with the decision rule (rotation → Secrets Manager; config → Parameter Store), then justify it with features and cost. Mentioning how ECS injects secrets at container start shows real-world experience.""",
        tip_bn=r"""প্রথমে সিদ্ধান্তের নিয়মটা বলো (rotation → Secrets Manager; config → Parameter Store), তারপর feature আর খরচ দিয়ে যুক্তি দাও। ECS কীভাবে container start-এর সময় secret inject করে সেটা বললে বাস্তব অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Committing `.env` files, logging the loaded config (secrets end up in CloudWatch Logs), or assuming Parameter Store rotates secrets automatically.""",
        mist_bn=r"""`.env` file commit করা, load করা config log করা (secret CloudWatch Logs-এ চলে যায়), বা ভাবা যে Parameter Store নিজে থেকে secret rotate করে।""",
        code=r"""
            // config.js — load secrets once at startup (AWS SDK for JavaScript v3)
            import { SecretsManagerClient, GetSecretValueCommand } from "@aws-sdk/client-secrets-manager";
            import { SSMClient, GetParameterCommand } from "@aws-sdk/client-ssm";

            const sm = new SecretsManagerClient({});
            const ssm = new SSMClient({});

            export async function loadConfig() {
              // RDS-managed secret: JSON with username/password/host/port
              const db = await sm.send(new GetSecretValueCommand({ SecretId: "prod/shop/db" }));
              const { username, password, host, port } = JSON.parse(db.SecretString);

              const jwt = await ssm.send(new GetParameterCommand({
                Name: "/shop/prod/JWT_SECRET",
                WithDecryption: true, // SecureString → decrypted with KMS
              }));

              return {
                db: { user: username, password, host, port },
                jwtSecret: jwt.Parameter.Value,
              };
            }
        """,
        lang="javascript",
        follow=[
            ("How does an ECS task get a secret, and what happens after the secret rotates?", "ECS task কীভাবে secret পায়, আর secret rotate হওয়ার পরে কী হয়?"),
            ("How would you rotate a database password without downtime?", "Downtime ছাড়া database password কীভাবে rotate করবে?"),
        ],
        related=["aws-012", "aws-021"],
        refs=[SM_INTRO, SM_ROTATION, PARAM_STORE],
    ),
    # ------------------------------------------------------------------ aws-017
    Q(
        id="aws-017", sub="VPC Networking", diff="medium", type="conceptual",
        prio="high", market="both", mins=5,
        tags=["vpc", "subnets", "nat-gateway", "internet-gateway", "vpc-endpoints"],
        ver="Version-independent concept (Amazon VPC)", vs=False, status="stable",
        q_en=r"""Explain a typical production VPC layout: public vs private subnets, route tables, the Internet Gateway, NAT Gateways and VPC endpoints. Where would you put an ALB, the app servers and an RDS database?""",
        q_bn=r"""একটা সাধারণ production VPC layout ব্যাখ্যা করো: public বনাম private subnet, route table, Internet Gateway, NAT Gateway আর VPC endpoint। ALB, app server আর RDS database কোথায় রাখবে?""",
        a_en=r"""
            - A **VPC** is your private network in one Region (for example `10.0.0.0/16`). Each **subnet** lives in exactly one AZ.
            - A subnet is **public** only because its route table has `0.0.0.0/0 → Internet Gateway` (and its resources have public IPs). A **private** subnet has no route to the IGW.
            - A **NAT Gateway** gives private subnets outbound-only internet access. Private subnets route `0.0.0.0/0` to it, so instances can make *outbound* calls (OS updates, third-party APIs) but can't be reached from the internet. The classic **zonal** NAT Gateway sits in a public subnet of one AZ, so you run one per AZ for availability. AWS now also offers a **regional** NAT Gateway (availability mode `regional`) that expands across AZs automatically and doesn't need a public subnet. Either way it charges per hour **and per GB processed**, which can become one of the bigger network costs.
            - **VPC endpoints** keep AWS traffic private. *Gateway endpoints* for S3 and DynamoDB are free and work through route tables. *Interface endpoints* (PrivateLink) for services like ECR, Secrets Manager and CloudWatch Logs cost per hour and per GB.

            Placement: the **ALB** goes in public subnets in at least two AZs. **App servers / ECS tasks** go in private app subnets. **RDS** goes in private DB subnets (a DB subnet group spanning AZs), and its security group allows 5432 only from the app's security group.
        """,
        a_bn=r"""
            - **VPC** হলো একটা Region-এর ভেতরে তোমার private network (যেমন `10.0.0.0/16`)। প্রতিটা **subnet** ঠিক একটা AZ-এ থাকে।
            - একটা subnet **public** হয় শুধু এই কারণে যে তার route table-এ `0.0.0.0/0 → Internet Gateway` আছে (আর ভেতরের resource-এর public IP আছে)। **Private** subnet-এর IGW পর্যন্ত কোনো route নেই।
            - **NAT Gateway** private subnet-কে শুধু outbound internet access দেয়। Private subnet `0.0.0.0/0` তার দিকে route করে, ফলে instance *outbound* call করতে পারে (OS update, third-party API), কিন্তু internet থেকে কেউ তাদের কাছে পৌঁছাতে পারে না। প্রচলিত **zonal** NAT Gateway একটা AZ-এর public subnet-এ থাকে, তাই availability-র জন্য প্রতি AZ-এ একটা রাখো। AWS এখন একটা **regional** NAT Gateway-ও দেয় (availability mode `regional`), যেটা নিজে থেকেই AZ জুড়ে ছড়িয়ে যায় আর public subnet লাগে না। যেটাই হোক, খরচ হয় প্রতি ঘণ্টা **আর প্রতি GB process করা data-র জন্য**, যেটা network খরচের বড় অংশ হয়ে যেতে পারে।
            - **VPC endpoint** AWS traffic private রাখে। S3 আর DynamoDB-র *gateway endpoint* free, route table দিয়ে কাজ করে। ECR, Secrets Manager, CloudWatch Logs-এর মতো service-এর *interface endpoint* (PrivateLink)-এ প্রতি ঘণ্টা আর প্রতি GB খরচ লাগে।

            কোথায় কী: **ALB** কমপক্ষে দুইটা AZ-এর public subnet-এ। **App server / ECS task** private app subnet-এ। **RDS** private DB subnet-এ (AZ জুড়ে একটা DB subnet group), আর তার security group 5432 শুধু app-এর security group থেকে allow করে।
        """,
        quick_en=r"""A subnet is public only because its route table sends `0.0.0.0/0` to an Internet Gateway; private subnets reach out through a NAT Gateway and reach AWS services privately through VPC endpoints. Put the ALB in public subnets, and app servers and RDS in private subnets across at least two AZs.""",
        quick_bn=r"""Subnet public হয় শুধু তখনই, যখন তার route table `0.0.0.0/0`-কে Internet Gateway-তে পাঠায়; private subnet বাইরে যায় NAT Gateway দিয়ে, আর AWS service-এ private-ভাবে যায় VPC endpoint দিয়ে। ALB রাখো public subnet-এ, আর app server ও RDS রাখো অন্তত দুটো AZ জুড়ে private subnet-এ।""",
        ex_en=r"""
            - **The default VPC** has only public subnets. It's fine for learning, but don't run production databases there.
            - **Cost trap:** private instances pulling large objects from S3 or images from ECR through the NAT Gateway pay NAT processing on every GB. An S3 gateway endpoint removes that cost for S3 traffic. Also keep each AZ's private route table pointing at the NAT in the *same* AZ to avoid cross-AZ charges.
            - **Plan CIDRs early.** Overlapping ranges block VPC peering and Transit Gateway connectivity later.
            - Don't rely on bastion hosts with port 22 open. SSM Session Manager reaches private instances through the SSM agent, using either a NAT route or SSM interface endpoints.
            - For IPv6, an egress-only Internet Gateway plays the "outbound only" role that NAT plays for IPv4.
        """,
        ex_bn=r"""
            - **Default VPC**-তে শুধু public subnet থাকে। শেখার জন্য ঠিক আছে, কিন্তু সেখানে production database চালিও না।
            - **খরচের ফাঁদ:** private instance যদি NAT Gateway দিয়ে S3 থেকে বড় object বা ECR থেকে image টানে, প্রতি GB-তে NAT processing charge লাগে। S3 gateway endpoint দিলে S3 traffic-এর এই খরচ থাকে না। আর প্রতিটা AZ-এর private route table-কে *একই* AZ-এর NAT-এ point করাও, তাহলে cross-AZ charge এড়ানো যায়।
            - **CIDR আগে থেকে plan করো।** Range overlap করলে পরে VPC peering বা Transit Gateway connect করা যায় না।
            - Port 22 খোলা bastion host-এর উপর নির্ভর কোরো না। SSM Session Manager SSM agent দিয়ে private instance-এ পৌঁছায়, NAT route বা SSM interface endpoint ব্যবহার করে।
            - IPv6-এ egress-only Internet Gateway "শুধু outbound" ভূমিকা পালন করে, যেটা IPv4-এ NAT করে।
        """,
        tip_en=r"""Sketch the subnet tiers per AZ, then state the one-sentence definition: "public means a route to the IGW". Finishing with the NAT cost trap shows production awareness.""",
        tip_bn=r"""প্রতি AZ-এর subnet tier-গুলো এঁকে বা বলে দেখাও, তারপর এক লাইনের definition দাও: "public মানে IGW-তে route আছে"। শেষে NAT-এর খরচের ফাঁদের কথা বললে production-এর অভিজ্ঞতা বোঝা যায়।""",
        mist_en=r"""Saying a subnet is public because "it has public IPs", putting RDS in a public subnet, or using a single zonal NAT Gateway for all AZs and calling it highly available.""",
        mist_bn=r""""Public IP আছে বলে subnet public" বলা, RDS public subnet-এ রাখা, বা সব AZ-এর জন্য একটা zonal NAT Gateway রেখে সেটাকে highly available বলা।""",
        code=r"""
            VPC 10.0.0.0/16 (two AZs shown; three is common in production)

            public-a  10.0.0.0/24    public-b  10.0.1.0/24    -> ALB, zonal NAT Gateway (one per AZ)
            app-a     10.0.10.0/24   app-b     10.0.11.0/24   -> EC2 / ECS tasks
            db-a      10.0.20.0/24   db-b      10.0.21.0/24   -> RDS (DB subnet group)

            Public route table:
              10.0.0.0/16        -> local
              0.0.0.0/0          -> igw-0abc
            Private route table (AZ a):
              10.0.0.0/16        -> local
              0.0.0.0/0          -> nat-0aaa  (NAT Gateway in public-a)
              pl-xxxx (S3)       -> vpce-0s3  (gateway endpoint, no extra charge)
        """,
        lang="text",
        follow=[
            ("How can an instance in a private subnet download OS updates?", "Private subnet-এর instance কীভাবে OS update download করে?"),
            ("Why might your NAT Gateway bill be higher than your EC2 bill?", "তোমার NAT Gateway-এর bill কেন EC2-র bill-এর চেয়েও বেশি হতে পারে?"),
        ],
        related=["aws-008", "aws-023", "aws-026"],
        refs=[VPC_WHAT, NAT_GW, GW_ENDPOINTS],
    ),
    # ------------------------------------------------------------------ aws-018
    Q(
        id="aws-018", sub="RDS High Availability & Backups", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["rds", "multi-az", "read-replicas", "pitr", "high-availability"],
        ver="Amazon RDS for PostgreSQL (2026)", vs=False, status="stable",
        q_en=r"""A production RDS for PostgreSQL database must survive the loss of its Availability Zone with **automatic failover** and **no loss of committed transactions**. Which option meets this requirement?""",
        q_bn=r"""একটা production RDS for PostgreSQL database-কে তার Availability Zone নষ্ট হলেও টিকে থাকতে হবে, **automatic failover**-সহ আর **commit হওয়া transaction না হারিয়ে**। কোন option এই requirement পূরণ করে?""",
        options=[
            ("Create a read replica in another AZ; RDS promotes it automatically when the primary fails",
             "অন্য AZ-এ একটা read replica বানানো; primary fail করলে RDS নিজে থেকেই সেটাকে promote করবে"),
            ("Enable a Multi-AZ deployment, which keeps a synchronously replicated standby in another AZ and fails over automatically behind the same endpoint",
             "Multi-AZ deployment চালু করা, যেটা অন্য AZ-এ synchronously replicated standby রাখে আর একই endpoint-এর পেছনে automatically failover করে"),
            ("Enable automated backups with 35-day retention so you can do a point-in-time restore",
             "35 দিনের retention-সহ automated backup চালু করা, যাতে point-in-time restore করা যায়"),
            ("Put RDS Proxy in front of the database",
             "Database-এর সামনে RDS Proxy বসানো"),
        ],
        correct=1,
        a_en=r"""
            Option 2. **Multi-AZ** replicates *synchronously* to a standby in a different AZ. If the primary or its AZ fails, RDS fails over automatically (usually within a minute or two), and the DNS endpoint stays the same, so apps just reconnect. Committed transactions are already on the standby, so none are lost.
        """,
        a_bn=r"""
            Option 2। **Multi-AZ** অন্য AZ-এর একটা standby-তে *synchronously* replicate করে। Primary বা তার AZ fail করলে RDS নিজে থেকে failover করে (সাধারণত এক-দুই মিনিটের মধ্যে), আর DNS endpoint একই থাকে, তাই app শুধু reconnect করে। Commit হওয়া transaction আগে থেকেই standby-তে আছে, তাই কিছুই হারায় না।
        """,
        quick_en=r"""Enable Multi-AZ: it keeps a synchronously replicated standby in another AZ and fails over automatically behind the same endpoint, so committed transactions aren't lost. An RDS read replica is asynchronous and promoting it is manual, and a point-in-time restore creates a new instance.""",
        quick_bn=r"""Multi-AZ চালু করো: এটা অন্য AZ-এ synchronous-ভাবে replicate হওয়া একটা standby রাখে আর একই endpoint-এর পেছনে নিজে থেকে failover করে, তাই committed transaction হারায় না। RDS read replica asynchronous আর তাকে promote করতে হয় হাতে, আর point-in-time restore নতুন instance বানায়।""",
        ex_en=r"""
            - **Option 1 is the tempting one.** RDS read replicas use *asynchronous* replication, so recent writes can be lost, and promoting an RDS read replica is a manual action. Replicas are for scaling reads and for cross-Region DR. (Aurora is different: Aurora Replicas in other AZs are automatic failover targets.)
            - Option 3: point-in-time restore creates a **new** instance with a new endpoint and takes time. It's for recovering from bad deletes or corruption, not for HA. Automated backups allow restores to within roughly the last five minutes, with up to 35 days of retention.
            - Option 4: RDS Proxy pools connections and can make failovers smoother for the app, but it doesn't create a standby.
            - A Multi-AZ *DB instance* standby can't serve reads. A Multi-AZ *DB cluster* deployment has two readable standbys, if you want HA and read capacity together.
        """,
        ex_bn=r"""
            - **Option 1-টাই আকর্ষণীয়।** RDS read replica *asynchronous* replication ব্যবহার করে, তাই সাম্প্রতিক write হারিয়ে যেতে পারে, আর RDS read replica promote করা একটা manual কাজ। Replica মূলত read scale করা আর cross-Region DR-এর জন্য। (Aurora আলাদা: অন্য AZ-এর Aurora Replica automatic failover target হিসেবে কাজ করে।)
            - Option 3: point-in-time restore নতুন endpoint-সহ একটা **নতুন** instance বানায়, আর সময়ও লাগে। এটা ভুল delete বা corruption থেকে উদ্ধারের জন্য, HA-র জন্য না। Automated backup দিয়ে মোটামুটি শেষ পাঁচ মিনিট পর্যন্ত restore করা যায়, retention সর্বোচ্চ 35 দিন।
            - Option 4: RDS Proxy connection pool করে আর failover-এর সময় app-এর জন্য ব্যাপারটা মসৃণ করতে পারে, কিন্তু কোনো standby তৈরি করে না।
            - Multi-AZ *DB instance*-এর standby read serve করতে পারে না। HA আর read capacity একসাথে চাইলে Multi-AZ *DB cluster* deployment-এ দুইটা readable standby থাকে।
        """,
        tip_en=r"""Use the formula: Multi-AZ = availability (synchronous, automatic). Read replicas = scale (asynchronous, manual promotion). Backups/PITR = recovery from mistakes. Saying all three in one breath sounds senior.""",
        tip_bn=r"""এই সূত্রটা বলো: Multi-AZ = availability (synchronous, automatic)। Read replica = scale (asynchronous, manual promotion)। Backup/PITR = ভুল থেকে উদ্ধার। তিনটা এক নিঃশ্বাসে বলতে পারলে senior শোনায়।""",
        related=["aws-023", "aws-030"],
        refs=[RDS_MULTIAZ, RDS_REPLICAS, RDS_PITR],
    ),
    # ------------------------------------------------------------------ aws-019
    Q(
        id="aws-019", sub="Load Balancers (ALB vs NLB)", diff="medium", type="mcq",
        prio="high", market="both", mins=2,
        tags=["alb", "nlb", "load-balancing", "health-checks", "routing"],
        ver="Elastic Load Balancing (ALB / NLB, 2026)", vs=False, status="stable",
        q_en=r"""One domain must route `/api/*` to an Express service and everything else to a Next.js service, terminate HTTPS with an ACM certificate, and only send traffic to healthy targets. Which setup fits best?""",
        q_bn=r"""একটা domain-এ `/api/*` যাবে একটা Express service-এ, বাকি সব যাবে একটা Next.js service-এ; ACM certificate দিয়ে HTTPS terminate করতে হবে, আর traffic শুধু healthy target-এ যাবে। কোন setup সবচেয়ে উপযুক্ত?""",
        options=[
            ("A Network Load Balancer with two TCP listeners, one per service",
             "একটা Network Load Balancer, যার প্রতিটা service-এর জন্য একটা করে দুইটা TCP listener"),
            ("An Application Load Balancer with an HTTPS listener and path-based rules forwarding to two target groups, each with its own health check",
             "একটা Application Load Balancer, যার HTTPS listener-এ path-based rule দিয়ে দুইটা target group-এ forward হয়, প্রতিটার নিজস্ব health check-সহ"),
            ("A Gateway Load Balancer in front of both services",
             "দুটো service-এর সামনে একটা Gateway Load Balancer"),
            ("Route 53 weighted records that split traffic between the two services",
             "দুইটা service-এর মধ্যে traffic ভাগ করা Route 53 weighted record"),
        ],
        correct=1,
        a_en=r"""
            Option 2. An **ALB** works at layer 7, so it can read the host, path, headers and query string. It routes `/api/*` to the Express target group with a default rule for Next.js, terminates TLS with an ACM certificate, and runs a **health check per target group** (for example `GET /healthz` must return 200), so unhealthy targets stop receiving traffic.
        """,
        a_bn=r"""
            Option 2। **ALB** layer 7-এ কাজ করে, তাই host, path, header আর query string পড়তে পারে। `/api/*`-কে Express target group-এ পাঠায়, default rule দিয়ে বাকিটা Next.js-এ; ACM certificate দিয়ে TLS terminate করে; আর **প্রতিটা target group-এর জন্য health check** চালায় (যেমন `GET /healthz`-কে 200 দিতে হবে), ফলে unhealthy target-এ traffic যাওয়া বন্ধ হয়।
        """,
        quick_en=r"""An Application Load Balancer with an HTTPS listener (ACM certificate) and path-based rules: `/api/*` goes to the Express target group, everything else to Next.js, each with its own health check. An NLB works at layer 4, so it can't route by path.""",
        quick_bn=r"""HTTPS listener (ACM certificate) আর path-based rule-সহ একটা Application Load Balancer: `/api/*` যাবে Express target group-এ, বাকি সব Next.js-এ, আর প্রতিটা group-এর নিজস্ব health check থাকবে। NLB layer 4-এ কাজ করে, তাই path দেখে route করতে পারে না।""",
        ex_en=r"""
            - **Option 1 is the tempting one** because NLBs are "faster". But an NLB works at layer 4 (TCP/UDP/TLS) and never sees URL paths, so it can't do path routing. Use an NLB for extreme throughput or very low latency, static IPs per AZ (Elastic IPs), non-HTTP protocols, preserving client IPs at the TCP level, or exposing a service through PrivateLink.
            - Option 3: a Gateway Load Balancer is for inserting third-party virtual appliances, like firewalls, into the traffic path.
            - Option 4: DNS works on hostnames, not paths, so weighted records can't split by `/api`.
            - ALB extras: host-based routing (`api.example.com` vs `app.example.com`), redirects and fixed responses, OIDC/Cognito authentication, AWS WAF, WebSockets, HTTP/2 and gRPC. An Auto Scaling group can use ELB health checks to *replace* instances that fail them.
        """,
        ex_bn=r"""
            - **Option 1 আকর্ষণীয়**, কারণ NLB "দ্রুত"। কিন্তু NLB layer 4-এ (TCP/UDP/TLS) কাজ করে, URL path কখনো দেখে না, তাই path routing করতে পারে না। NLB ব্যবহার করো খুব বেশি throughput বা খুব কম latency, প্রতি AZ-এ static IP (Elastic IP), non-HTTP protocol, TCP level-এ client IP ধরে রাখা, বা PrivateLink দিয়ে service expose করার জন্য।
            - Option 3: Gateway Load Balancer traffic path-এ firewall-এর মতো third-party virtual appliance বসানোর জন্য।
            - Option 4: DNS কাজ করে hostname নিয়ে, path নিয়ে না, তাই weighted record দিয়ে `/api` আলাদা করা যায় না।
            - ALB-এর বাড়তি সুবিধা: host-based routing (`api.example.com` বনাম `app.example.com`), redirect আর fixed response, OIDC/Cognito authentication, AWS WAF, WebSocket, HTTP/2 আর gRPC। Auto Scaling group ELB health check ব্যবহার করে fail করা instance *replace* করতে পারে।
        """,
        tip_en=r"""Say "ALB = layer 7, routes on request content; NLB = layer 4, routes on connections". Then give one concrete use case for each.""",
        tip_bn=r""""ALB = layer 7, request-এর content দেখে route করে; NLB = layer 4, connection দেখে route করে" বলো। তারপর প্রতিটার একটা করে concrete use case দাও।""",
        related=["aws-023", "aws-022"],
        refs=[ALB, NLB, ELB_HOW],
    ),
]

if __name__ == "__main__":
    save("aws", "b3", QUESTIONS)
