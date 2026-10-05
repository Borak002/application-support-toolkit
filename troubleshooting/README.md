
# Application Troubleshooting Playbook

Practical incident-investigation scenarios for Application Support and Production Support environments.

The objective of troubleshooting is not simply to restore service, but to understand:

**What happened → Why it happened → What was done → How recovery was verified**

---

# 1. HTTP 500 — Internal Server Error

## Symptom

Users receive:

```text
HTTP 500 Internal Server Error
```

## Investigation

Start by checking the application logs:

```bash
grep -Ei "error|exception|500" application.log
```

Check recent service logs:

```bash
journalctl -u application-service -n 100
```

Check whether the service is running:

```bash
systemctl status application-service
```

Check server resources:

```bash
free -h
df -h
```

## Possible Causes

* Unhandled application exception
* Database connectivity failure
* Invalid configuration
* Missing environment variable
* Dependency failure
* Resource exhaustion
* Recent deployment issue

## Resolution Approach

1. Identify the exact exception.
2. Determine when the failure started.
3. Check recent deployments or configuration changes.
4. Validate dependent services.
5. Apply the approved remediation.
6. Restart the service only when appropriate.
7. Re-test the affected functionality.

## Verification

Confirm:

* HTTP response is successful.
* Application logs no longer show the error.
* The affected transaction or workflow completes successfully.
* Monitoring returns to normal.

---

# 2. Connection Timeout

## Symptom

An application reports:

```text
Connection timed out
```

## Investigation

Test basic connectivity:

```bash
ping hostname
```

Test the required port:

```bash
nc -zv hostname 443
```

Test the endpoint:

```bash
curl -v https://example.com
```

Check DNS:

```bash
nslookup example.com
```

## Possible Causes

* Remote service unavailable
* Network instability
* Firewall restrictions
* Incorrect endpoint
* DNS failure
* VPN/network routing issue
* Service overloaded

## Resolution Approach

Determine whether the failure is:

**Application → Network → External dependency**

Do not immediately restart the application without understanding where the connection is failing.

---

# 3. Database Connection Failure

## Symptom

The application reports an error such as:

```text
Unable to connect to database
```

or:

```text
Connection refused
```

## Investigation

Check whether the database service is running:

```bash
systemctl status postgresql
```

Check whether the database port is reachable:

```bash
nc -zv database-host 5432
```

Check recent database logs.

For PostgreSQL, review:

```bash
journalctl -u postgresql -n 100
```

Check available disk space:

```bash
df -h
```

## Possible Causes

* Database service stopped
* Network connectivity issue
* Incorrect connection configuration
* Authentication failure
* Database resource exhaustion
* Disk space exhaustion
* Connection pool exhaustion

## Resolution

Validate the database service and connectivity before making application changes.

---

# 4. Disk Space Exhaustion

## Symptom

The application becomes slow or fails unexpectedly.

Possible errors include:

```text
No space left on device
```

## Investigation

Check disk usage:

```bash
df -h
```

Find large directories:

```bash
du -h --max-depth=1 /var | sort -hr
```

Find large files:

```bash
find /var -type f -size +500M -exec ls -lh {} \;
```

## Possible Causes

* Large application logs
* Unmanaged log rotation
* Temporary files
* Database growth
* Backup files
* Core dumps

## Resolution

Do not blindly delete files.

First:

1. Identify what is consuming the space.
2. Confirm whether files are safe to remove.
3. Follow the organization's retention policy.
4. Archive or remove files through an approved process.
5. Confirm disk space has been recovered.
6. Verify application health.

---

# 5. Service Is Down

## Symptom

An application or API is unavailable.

## Investigation

Check service status:

```bash
systemctl status application-service
```

Check recent logs:

```bash
journalctl -u application-service -n 100
```

Check listening ports:

```bash
ss -tulpn
```

Check server resources:

```bash
free -h
df -h
```

## Possible Causes

* Application crash
* Failed deployment
* Configuration error
* Port conflict
* Resource exhaustion
* Dependency failure

## Recovery

If restarting the service is approved:

```bash
sudo systemctl restart application-service
```

Then immediately verify:

```bash
systemctl status application-service
```

And test the application endpoint:

```bash
curl -I https://example.com
```

---

# 6. Unauthorized / Authentication Failure

## Symptom

An API returns:

```text
401 Unauthorized
```

or:

```text
403 Forbidden
```

## Investigation

Check:

* Token validity
* API credentials
* Authentication headers
* Token expiry
* User permissions
* Recent credential/configuration changes

Search application logs:

```bash
grep -Ei "unauthorized|forbidden|authentication|token" application.log
```

## Important Distinction

**401 Unauthorized**

Usually indicates missing or invalid authentication credentials.

**403 Forbidden**

Usually means the request was authenticated but does not have sufficient permission.

---

# 7. SSL/TLS Connection Failure

## Symptom

An application cannot establish a secure connection.

Possible errors:

```text
SSL connection error
```

```text
Connection reset
```

```text
TLS handshake failed
```

## Investigation

Test the endpoint:

```bash
curl -Iv https://example.com
```

Inspect the certificate:

```bash
openssl s_client -connect example.com:443
```

Check:

* Certificate validity
* Certificate expiry
* TLS negotiation
* DNS resolution
* Network connectivity

## Possible Causes

* Expired certificate
* Incorrect certificate chain
* TLS incompatibility
* Network interruption
* Remote service issue
* Incorrect hostname

---

# 8. High CPU or Memory Usage

## Symptom

The application becomes slow or unstable.

## Investigation

Check memory:

```bash
free -h
```

Check processes:

```bash
top
```

Check running processes:

```bash
ps aux --sort=-%cpu | head
```

For memory:

```bash
ps aux --sort=-%mem | head
```

## Possible Causes

* Memory leak
* CPU-intensive process
* Excessive traffic
* Background job
* Large batch operation
* Application defect

## Resolution

Identify the process responsible before terminating anything.

For production systems, follow the approved incident-management procedure.

---

# 9. Failed Deployment

## Symptom

An application becomes unavailable immediately after deployment.

## Investigation

Establish:

* Deployment time
* Version deployed
* Previous working version
* Error messages
* Configuration changes
* Dependency changes

Compare application logs before and after deployment.

Check service status:

```bash
systemctl status application-service
```

Check recent logs:

```bash
journalctl -u application-service --since "30 minutes ago"
```

## Resolution

If the deployment is confirmed as the cause:

1. Follow the organization's rollback procedure.
2. Restore the known-good version.
3. Verify service availability.
4. Confirm the affected workflow.
5. Document the incident.
6. Capture evidence for engineering review.

---

# Incident Investigation Template

Use this structure when documenting an incident.

## Incident

**Title:**
Brief description of the issue.

**Start Time:**
YYYY-MM-DD HH:MM

**Affected Service:**
Application/API/Service

**Severity:**
P1 / P2 / P3 / P4

## Symptoms

What did users or monitoring systems report?

## Investigation

Document:

* Logs reviewed
* Commands executed
* Monitoring observations
* Transaction/request IDs
* Relevant timestamps
* Dependencies checked

## Findings

What evidence was discovered?

## Root Cause

What caused the incident?

## Resolution

What action restored service?

## Verification

How was recovery confirmed?

## Preventive Action

What can reduce the likelihood of recurrence?

---

# Troubleshooting Principles

### 1. Start with evidence

Do not assume the cause before reviewing logs, monitoring, and system state.

### 2. Establish a timeline

Determine when the issue started and what changed around that time.

### 3. Isolate the failure

Determine whether the problem is:

```text
Client
   ↓
Application
   ↓
Database
   ↓
Internal Dependency
   ↓
External Dependency
```

### 4. Change one thing at a time

Avoid introducing additional variables during an investigation.

### 5. Verify after remediation

A successful restart does not automatically mean the incident is resolved.

### 6. Document everything important

Good documentation makes future incidents faster to diagnose.

---

# Support Engineer Mindset

Effective Application Support is more than resolving tickets.

It involves:

**Observe → Investigate → Diagnose → Resolve → Verify → Document → Improve**

The goal is to restore service safely while producing enough evidence to prevent the same problem from becoming a recurring incident.

---

## Security Reminder

Never publish real:

* Customer information
* Bank account details
* API credentials
* Passwords
* Access tokens
* Private IP addresses
* Production logs
* Internal hostnames
* Confidential company information

All examples in this repository are generic and created for demonstration purposes.
