# Bug Bounty Field Playbook

## Web Application & API Vulnerability Hunting

---

# PHASE 0: SCOPE & SAFETY

## 0.1 Program Review

- [ ] Read the entire bug bounty policy.
- [ ] Identify explicitly allowed domains.
- [ ] Identify explicitly excluded domains.
- [ ] Identify allowed vulnerability classes.
- [ ] Identify prohibited testing techniques.
- [ ] Check rate limits.
- [ ] Check automated scanning restrictions.
- [ ] Check account requirements.
- [ ] Check test-account requirements.
- [ ] Check rules regarding third-party services.
- [ ] Check rules regarding denial-of-service testing.
- [ ] Check rules regarding data access.
- [ ] Check rules regarding social engineering.
- [ ] Record the reporting requirements.

## 0.2 Create Target Profile

Record:

- [ ] Program name
- [ ] Scope
- [ ] Out-of-scope assets
- [ ] Authentication requirements
- [ ] Test accounts
- [ ] Rate limits
- [ ] Known technologies
- [ ] Known APIs
- [ ] Interesting functionality
- [ ] Previous findings
- [ ] Notes

## 0.3 Establish Testing Boundaries

Never:

- [ ] Destroy production data.
- [ ] Modify another user’s data unnecessarily.
- [ ] Access sensitive information beyond what is required to prove impact.
- [ ] Perform denial-of-service testing unless explicitly authorized.
- [ ] Attack third-party infrastructure outside scope.
- [ ] Send phishing/social-engineering attacks unless explicitly authorized.
- [ ] Use destructive payloads.
- [ ] Continue exploitation after sufficient evidence has been obtained.

---

# PHASE 1: RECONNAISSANCE

## 1.1 Passive Recon

Collect:

- [ ] Root domains
- [ ] Subdomains
- [ ] Historical subdomains
- [ ] DNS records
- [ ] IP addresses
- [ ] ASN information
- [ ] Certificate information
- [ ] Technology fingerprints
- [ ] Historical URLs
- [ ] Public JavaScript
- [ ] Public documentation
- [ ] Public API documentation
- [ ] Public repositories where permitted
- [ ] Search-engine indexed endpoints

## 1.2 Subdomain Enumeration

For each discovered subdomain:

- [ ] Resolve DNS.
- [ ] Identify whether host is alive.
- [ ] Identify HTTP/HTTPS services.
- [ ] Identify redirects.
- [ ] Fingerprint technology.
- [ ] Record response status.
- [ ] Record title.
- [ ] Record server/CDN information.
- [ ] Identify interesting subdomains.
Prioritize names containing:

- [ ] api
- [ ] admin
- [ ] portal
- [ ] dashboard
- [ ] app
- [ ] staging
- [ ] dev
- [ ] test
- [ ] beta
- [ ] internal
- [ ] auth
- [ ] sso
- [ ] vpn

## 1.3 Technology Identification

Identify:

- [ ] Frontend framework
- [ ] Backend framework
- [ ] Web server
- [ ] CDN
- [ ] WAF
- [ ] Authentication provider
- [ ] Cloud provider
- [ ] Database indicators
- [ ] CMS
- [ ] Third-party services
- [ ] API framework

## 1.4 Build an Asset Inventory

Create a table containing:

| Asset | Type | Technology | Auth Required | Interesting Features |
| --- | --- | --- | --- | --- |
| example.com | Web | React | No | Login |
| api.example.com | API | Node | Yes | User API |
| admin.example.com | Admin | Django | Yes | Dashboard |

---

# PHASE 2: ATTACK-SURFACE MAPPING

## 2.1 Crawl the Application

Identify:

- [ ] Pages
- [ ] Forms
- [ ] APIs
- [ ] Parameters
- [ ] Cookies
- [ ] Headers
- [ ] JavaScript files
- [ ] Upload functionality
- [ ] Redirects
- [ ] Authentication flows
- [ ] Password-reset flows
- [ ] Account-management functions

## 2.2 Build an Endpoint Inventory

For every endpoint record:

- [ ] URL
- [ ] HTTP method
- [ ] Authentication requirement
- [ ] Parameters
- [ ] Parameter type
- [ ] Response type
- [ ] User role
- [ ] Interesting behavior
- [ ] Vulnerability classes to test

## 2.3 Parameter Discovery

Look for:

- [ ] Query parameters
- [ ] POST parameters
- [ ] JSON parameters
- [ ] Path parameters
- [ ] Headers
- [ ] Cookies
- [ ] Multipart fields
- [ ] GraphQL variables
- [ ] WebSocket messages
Prioritize parameters involving:

- [ ] IDs
- [ ] Usernames
- [ ] Account numbers
- [ ] File paths
- [ ] URLs
- [ ] Redirects
- [ ] Search
- [ ] Filters
- [ ] Sorting
- [ ] File names
- [ ] HTML/Markdown
- [ ] Templates
- [ ] Commands
- [ ] Database queries

---

# PHASE 3: VULNERABILITY PLAYBOOKS

# PLAYBOOK 01: XSS

## Discovery

- [ ] Identify user-controlled input.
- [ ] Submit a unique marker.
- [ ] Determine whether it is reflected.
- [ ] Determine whether it is stored.
- [ ] Determine whether JavaScript reads it from the DOM.

## Context

Determine whether input reaches:

- [ ] HTML
- [ ] HTML attribute
- [ ] JavaScript
- [ ] CSS
- [ ] URL
- [ ] DOM sink

## Testing

- [ ] Test encoding.
- [ ] Test filtering.
- [ ] Test normalization.
- [ ] Test alternate representations.
- [ ] Identify sanitization.
- [ ] Identify dangerous sinks.
- [ ] Confirm browser execution.

## Impact

- [ ] Self-XSS?
- [ ] Reflected?
- [ ] Stored?
- [ ] DOM?
- [ ] Victim interaction required?
- [ ] Privileged user affected?
- [ ] Sensitive application functionality exposed?

---

# PLAYBOOK 02: SQL INJECTION

## Discovery

- [ ] Identify database-backed parameters.
- [ ] Establish baseline response.
- [ ] Manipulate input.
- [ ] Compare responses.
- [ ] Look for database errors.
- [ ] Look for deterministic behavioral differences.

## Classification

- [ ] Error-based
- [ ] Boolean-based blind
- [ ] Time-based blind
- [ ] UNION-based
- [ ] Stacked queries
- [ ] Second-order

## Confirmation

- [ ] Confirm parameter is responsible.
- [ ] Reproduce from a clean session.
- [ ] Minimize requests.
- [ ] Establish deterministic behavior.
- [ ] Stop once sufficient evidence exists.

## Impact

- [ ] Authentication bypass
- [ ] Unauthorized data access
- [ ] Data modification
- [ ] Cross-tenant access
- [ ] Administrative impact

---

# PLAYBOOK 03: IDOR / BOLA

## Discovery

Identify object references:

- [ ] User IDs
- [ ] Account IDs
- [ ] Order IDs
- [ ] Invoice IDs
- [ ] Document IDs
- [ ] File IDs
- [ ] Message IDs
- [ ] UUIDs

## Test

- [ ] Create two authorized test accounts where permitted.
- [ ] Record Account A’s object identifier.
- [ ] Record Account B’s object identifier.
- [ ] Request Account A’s object while authenticated as B.
- [ ] Compare authorization behavior.
- [ ] Test read access.
- [ ] Test update access.
- [ ] Test delete access where explicitly safe and permitted.

## Confirm

- [ ] Unauthorized object access is reproducible.
- [ ] Server-side authorization is missing.
- [ ] Access is not merely a client-side UI issue.

---

# PLAYBOOK 04: BROKEN ACCESS CONTROL

Test every important function with different roles.

- [ ] Anonymous
- [ ] Normal user
- [ ] Premium user
- [ ] Moderator
- [ ] Administrator
For each endpoint:

- [ ] Can lower-privileged users access it?
- [ ] Can unauthenticated users access it?
- [ ] Can users perform administrative actions?
- [ ] Can users access another tenant?
- [ ] Can users modify protected resources?
- [ ] Are authorization checks performed server-side?

---

# PLAYBOOK 05: SSRF

## Discovery

Search for functionality accepting URLs:

- [ ] URL preview
- [ ] Webhook
- [ ] Image import
- [ ] PDF generation
- [ ] Remote file import
- [ ] Feed/RSS import
- [ ] URL validation
- [ ] Link unfurling
- [ ] Callback functionality

## Testing

- [ ] Determine whether the server makes the request.
- [ ] Use an authorized interaction endpoint for confirmation.
- [ ] Observe DNS/HTTP interaction.
- [ ] Determine whether redirects are followed.
- [ ] Determine whether URL validation exists.
- [ ] Determine whether private/internal destinations are blocked.

## Impact

- [ ] Internal service access
- [ ] Cloud metadata exposure
- [ ] Internal network reachability
- [ ] Credential exposure
- [ ] Administrative interface access

---

# PLAYBOOK 06: CSRF

Identify state-changing operations:

- [ ] Change email
- [ ] Change password
- [ ] Change account settings
- [ ] Add payment information
- [ ] Create API keys
- [ ] Delete resources
- [ ] Change permissions
Check:

- [ ] Is CSRF protection present?
- [ ] Is a token required?
- [ ] Is the token validated server-side?
- [ ] Are cookies SameSite protected?
- [ ] Does the request require a custom header?
- [ ] Can the operation be triggered cross-origin?

---

# PLAYBOOK 07: AUTHENTICATION

## Registration

- [ ] Duplicate account handling
- [ ] Email verification
- [ ] Password policy
- [ ] Account activation
- [ ] Username enumeration

## Login

- [ ] Rate limiting
- [ ] Account enumeration
- [ ] Authentication bypass
- [ ] Session creation
- [ ] MFA enforcement

## Password Reset

- [ ] Token entropy
- [ ] Token expiration
- [ ] Token reuse
- [ ] Token invalidation
- [ ] Host/header manipulation
- [ ] Account binding

## MFA

- [ ] MFA bypass
- [ ] Recovery-flow weaknesses
- [ ] Rate limiting
- [ ] Session handling
- [ ] Alternate authentication paths

---

# PLAYBOOK 08: SESSION MANAGEMENT

Check:

- [ ] Session fixation
- [ ] Session invalidation
- [ ] Logout behavior
- [ ] Session expiration
- [ ] Concurrent sessions
- [ ] Cookie security
- [ ] Secure flag
- [ ] HttpOnly flag
- [ ] SameSite attribute
- [ ] Session/token rotation after authentication
- [ ] Password-change session invalidation

---

# PLAYBOOK 09: FILE UPLOAD

Identify upload functionality.

Check:

- [ ] File type validation
- [ ] MIME validation
- [ ] Extension validation
- [ ] Filename handling
- [ ] Path handling
- [ ] Storage location
- [ ] Access control
- [ ] File retrieval
- [ ] File processing
- [ ] Image processing
- [ ] Archive extraction
- [ ] Server-side execution risk
Prioritize functionality involving:

- [ ] Images
- [ ] Documents
- [ ] Archives
- [ ] Profile pictures
- [ ] Import/export
- [ ] Attachments

---

# PLAYBOOK 10: PATH TRAVERSAL

Identify parameters involving:

- [ ] Files
- [ ] Templates
- [ ] Downloads
- [ ] Images
- [ ] Documents
- [ ] Archives
- [ ] Backups
Test whether user-controlled paths can escape their intended directory.

Check:

- [ ] URL decoding
- [ ] Path normalization
- [ ] Encoding
- [ ] Absolute paths
- [ ] Windows/Linux path differences

---

# PLAYBOOK 11: OPEN REDIRECT

Find parameters such as:

- [ ] `url`
- [ ] `redirect`
- [ ] `next`
- [ ] `return`
- [ ] `returnUrl`
- [ ] `continue`
- [ ] `target`
Test:

- [ ] External destinations
- [ ] Redirect chains
- [ ] URL normalization
- [ ] Encoding
- [ ] Host validation
Determine whether the redirect can be chained into:

- [ ] OAuth
- [ ] Authentication
- [ ] Password reset
- [ ] Phishing-resistant security flows

---

# PLAYBOOK 12: SSTI

Look for:

- [ ] Email templates
- [ ] Report templates
- [ ] Document templates
- [ ] Notification templates
- [ ] User-customizable templates
- [ ] Server-rendered content
Determine:

- [ ] Template engine
- [ ] Input location
- [ ] Whether expressions are evaluated
- [ ] Whether evaluation occurs server-side
- [ ] Whether arbitrary server-side behavior is possible

---

# PLAYBOOK 13: XXE

Look for XML processing:

- [ ] XML APIs
- [ ] SOAP
- [ ] SVG uploads
- [ ] XML imports
- [ ] Document processing
- [ ] SAML-related functionality
Determine:

- [ ] XML parser
- [ ] External entity support
- [ ] Entity resolution
- [ ] Server-side requests
- [ ] File access

---

# PLAYBOOK 14: CORS

For sensitive endpoints:

- [ ] Inspect `Access-Control-Allow-Origin`.
- [ ] Check whether arbitrary origins are accepted.
- [ ] Check credentialed requests.
- [ ] Check origin reflection.
- [ ] Check `null` origin behavior.
- [ ] Determine whether sensitive responses are exposed.
Impact matters more than a pretty CORS header.

---

# PLAYBOOK 15: JWT

Identify JWT usage.

Inspect:

- [ ] Algorithm
- [ ] Header
- [ ] Claims
- [ ] Expiration
- [ ] Issuer
- [ ] Audience
- [ ] Signature validation
- [ ] Key handling
Check:

- [ ] Token expiration
- [ ] Token revocation
- [ ] Algorithm handling
- [ ] Claim manipulation
- [ ] Authorization enforcement
- [ ] Token reuse

---

# PLAYBOOK 16: OAuth

Map:

- [ ] Authorization endpoint
- [ ] Token endpoint
- [ ] Redirect URI
- [ ] Client ID
- [ ] State
- [ ] PKCE
- [ ] Scope
- [ ] Account linking
Test:

- [ ] Redirect URI validation
- [ ] State validation
- [ ] PKCE enforcement
- [ ] Account-linking logic
- [ ] Authorization-code handling
- [ ] Token audience
- [ ] Scope enforcement

---

# PLAYBOOK 17: BUSINESS LOGIC

This requires thinking like a malicious customer rather than a scanner.

For every important workflow:

- [ ] Understand intended sequence.
- [ ] Identify required steps.
- [ ] Identify assumptions.
- [ ] Skip steps.
- [ ] Repeat steps.
- [ ] Change sequence.
- [ ] Modify values.
- [ ] Use unexpected values.
- [ ] Perform actions concurrently where authorized.
- [ ] Test limits.
- [ ] Test negative values where applicable.
- [ ] Test boundary values.
- [ ] Test whether server trusts client-side calculations.
Prioritize:

- [ ] Payments
- [ ] Discounts
- [ ] Credits
- [ ] Refunds
- [ ] Transfers
- [ ] Subscription changes
- [ ] Inventory
- [ ] Permissions
- [ ] Account linking

---

# PLAYBOOK 18: RACE CONDITIONS

Identify operations where timing matters:

- [ ] Coupon redemption
- [ ] Transfers
- [ ] Withdrawals
- [ ] Password resets
- [ ] Account creation
- [ ] Invitation acceptance
- [ ] Resource creation
- [ ] Limited-use functionality
Test:

- [ ] Can the same action be performed concurrently?
- [ ] Is the state checked before modification?
- [ ] Can a one-time operation execute multiple times?
- [ ] Does the server enforce atomicity?

---

# PLAYBOOK 19: GRAPHQL

Map:

- [ ] Queries
- [ ] Mutations
- [ ] Introspection
- [ ] Object types
- [ ] Arguments
- [ ] Authorization
- [ ] Nested relationships
Test:

- [ ] Excessive data exposure
- [ ] BOLA/IDOR
- [ ] Authorization bypass
- [ ] Excessive query depth
- [ ] Excessive resource consumption
- [ ] Sensitive fields
- [ ] Mutation authorization

---

# PLAYBOOK 20: WEBSOCKETS

Identify:

- [ ] WebSocket endpoints
- [ ] Authentication mechanism
- [ ] Message format
- [ ] User identifiers
- [ ] Object identifiers
- [ ] Server-side authorization
Test:

- [ ] Authentication bypass
- [ ] Cross-user data access
- [ ] Message manipulation
- [ ] Authorization failures
- [ ] Origin validation
- [ ] Sensitive event exposure

---

# PHASE 4: VALIDATION

Before reporting any finding:

## Reproduce

- [ ] Start from a clean session.
- [ ] Reproduce the issue.
- [ ] Confirm the exact endpoint.
- [ ] Confirm the exact parameter.
- [ ] Confirm required permissions.
- [ ] Confirm required conditions.

## Minimize

- [ ] Remove unnecessary requests.
- [ ] Remove unnecessary payload components.
- [ ] Reduce exploitation to the smallest reliable PoC.

## Verify Impact

- [ ] Determine affected asset.
- [ ] Determine affected users.
- [ ] Determine required privileges.
- [ ] Determine attacker interaction.
- [ ] Determine confidentiality impact.
- [ ] Determine integrity impact.
- [ ] Determine availability impact.

---

# PHASE 5: REPORTING

## Report Structure

### Title

`[Vulnerability] in [Endpoint/Feature] allows [Impact]`

### Summary

- [ ] What is vulnerable?
- [ ] Why is it vulnerable?
- [ ] What can an attacker accomplish?

### Environment

- [ ] URL
- [ ] HTTP method
- [ ] Account role
- [ ] Required conditions

### Steps to Reproduce

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3
- [ ] Observe result

### Evidence

- [ ] Request
- [ ] Response
- [ ] Screenshot
- [ ] Video if necessary

### Impact

Explain the real security consequence.

Avoid:

> “This could potentially be dangerous.”

Instead explain:

> “An authenticated attacker can access another user’s invoice by modifying the invoice identifier.”

### Remediation

- [ ] Identify the vulnerable trust boundary.
- [ ] Recommend server-side validation.
- [ ] Recommend proper authorization.
- [ ] Recommend contextual output encoding.
- [ ] Recommend parameterized queries.
- [ ] Recommend appropriate security controls.

---

# DAILY HUNTING WORKFLOW

## Step 1: Scope

- [ ] Read program rules.
- [ ] Select target.

## Step 2: Recon

- [ ] Enumerate assets.
- [ ] Identify technologies.
- [ ] Identify interesting hosts.

## Step 3: Crawl

- [ ] Map application.
- [ ] Collect endpoints.
- [ ] Collect parameters.

## Step 4: Build Attack Surface

For each endpoint ask:

- [ ] Does it accept user input?
- [ ] Does it access another user’s data?
- [ ] Does it perform an important action?
- [ ] Does it interact with files?
- [ ] Does it make server-side requests?
- [ ] Does it interact with a database?
- [ ] Does it redirect?
- [ ] Does it process templates?
- [ ] Does it handle authentication?
- [ ] Does it handle payments or sensitive business logic?

## Step 5: Prioritize

### High-value targets

- [ ] Authentication
- [ ] Authorization
- [ ] Admin functions
- [ ] APIs
- [ ] Account management
- [ ] Payment functionality
- [ ] File processing
- [ ] OAuth/SSO
- [ ] Internal integrations
- [ ] Multi-tenant functionality

## Step 6: Test

Run relevant playbooks against the endpoint.

## Step 7: Investigate Anomalies

Whenever something behaves unexpectedly:

- [ ] Reproduce it.
- [ ] Change one variable.
- [ ] Compare responses.
- [ ] Identify the trust boundary.
- [ ] Determine whether the behavior has security impact.

## Step 8: Validate

- [ ] Clean-session reproduction.
- [ ] Minimal PoC.
- [ ] Confirm impact.

## Step 9: Report

- [ ] Clear title.
- [ ] Reproduction steps.
- [ ] Evidence.
- [ ] Impact.
- [ ] Remediation.

---

# THE CORE MENTAL MODEL

For every endpoint, ask these questions:

### INPUT

**What can I control?**

### PROCESSING

**What does the server do with my input?**

### TRUST

**What does the server assume I cannot control?**

### AUTHORIZATION

**What prevents me from accessing something I shouldn’t?**

### STATE

**What happens if I repeat, reorder, or manipulate the operation?**

### OUTPUT

**Where does my input or the resulting data go?**

### IMPACT

**What security boundary can I cross?**

---

# PRIORITY MATRIX

| Vulnerability | Typical Value | Priority |
| --- | --- | --- |
| Account takeover | Critical | 🔴 Highest |
| Authentication bypass | Critical | 🔴 Highest |
| Remote code execution | Critical | 🔴 Highest |
| SQL injection | Critical/High | 🔴 Highest |
| SSRF with cloud/internal impact | Critical/High | 🔴 Highest |
| Privilege escalation | High/Critical | 🔴 High |
| BOLA/IDOR exposing sensitive data | High | 🔴 High |
| Stored XSS affecting privileged users | High | 🔴 High |
| Business logic affecting money | High/Critical | 🔴 High |
| Sensitive data exposure | High | 🟠 High |
| File upload vulnerabilities | High/Critical | 🟠 High |
| CSRF | Medium/High | 🟡 Medium |
| Reflected XSS | Medium | 🟡 Medium |
| Open redirect | Low/Medium | 🟢 Lower |
| Self-XSS | Usually Low | 🟢 Lower |

---

# FINAL RULE

Do not hunt vulnerabilities by payload.

Hunt **trust boundaries**.

For every feature, determine:

`Who controls the input?`

↓

`Who is supposed to be allowed to perform the action?`

↓

`What does the server trust?`

↓

`What happens if those assumptions are false?`

↓

`Can the resulting behavior cross a security boundary?`

That mental model scales much better than memorizing hundreds of payloads.
