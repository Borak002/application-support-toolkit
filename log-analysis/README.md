# Log Analysis Toolkit

Practical log-analysis techniques for Application Support and Production Support engineers investigating application errors, failed requests, timeouts, authentication failures, and service issues.

## Purpose

Application logs provide evidence about what happened inside a system.

A good support investigation should move from:

**Symptom → Evidence → Root Cause → Action → Verification**

This toolkit documents common techniques for finding and interpreting useful information from application and system logs.

---

## 1. View Recent Log Entries

Display the last 100 lines:

```bash
tail -n 100 application.log
```

Display the last 500 lines:

```bash
tail -n 500 application.log
```

Follow a log in real time:

```bash
tail -f application.log
```

Exit the live log view with:

```text
Ctrl + C
```

---

## 2. Search for Errors

Search for the word `error`:

```bash
grep -i "error" application.log
```

Search for exceptions:

```bash
grep -i "exception" application.log
```

Search for failures:

```bash
grep -i "failed" application.log
```

Search for timeouts:

```bash
grep -i "timeout" application.log
```

---

## 3. Search for Multiple Error Patterns

A useful approach is to search for several common failure indicators:

```bash
grep -Ei "error|exception|failed|timeout|critical" application.log
```

This can quickly identify potential incidents in a large log file.

---

## 4. Show the Lines Around an Error

Sometimes the most useful information appears immediately before or after an error.

Show five lines before and after matching results:

```bash
grep -i -C 5 "exception" application.log
```

Show ten lines after an error:

```bash
grep -i -A 10 "error" application.log
```

Show ten lines before an error:

```bash
grep -i -B 10 "error" application.log
```

---

## 5. Count Errors

Count occurrences of a specific error:

```bash
grep -ic "error" application.log
```

Count timeout occurrences:

```bash
grep -ic "timeout" application.log
```

This can help determine whether an issue is isolated or recurring.

---

## 6. Find HTTP Errors

Search for common HTTP status codes:

```bash
grep -E "400|401|403|404|500|502|503|504" application.log
```

Common meanings:

| Status | Meaning               |
| ------ | --------------------- |
| 400    | Bad Request           |
| 401    | Unauthorized          |
| 403    | Forbidden             |
| 404    | Not Found             |
| 500    | Internal Server Error |
| 502    | Bad Gateway           |
| 503    | Service Unavailable   |
| 504    | Gateway Timeout       |

Always investigate the surrounding log entries rather than relying only on the status code.

---

## 7. Investigate Authentication Failures

Search for authentication-related errors:

```bash
grep -Ei "unauthorized|authentication|invalid token|forbidden" application.log
```

Potential causes include:

* Expired credentials
* Invalid API keys
* Expired tokens
* Incorrect permissions
* Authentication service failures
* Configuration changes

---

## 8. Investigate Connection Problems

Search for common connectivity errors:

```bash
grep -Ei "connection refused|connection reset|connection timed out|socket|network" application.log
```

For SSL/TLS-related issues:

```bash
grep -Ei "ssl|tls|certificate|handshake" application.log
```

These errors may indicate:

* Remote service downtime
* Network instability
* Firewall restrictions
* Expired certificates
* Incorrect endpoint configuration
* TLS compatibility problems

---

## 9. Search by Transaction or Request ID

When investigating a customer transaction, request ID, or correlation ID:

```bash
grep "REQUEST_ID" application.log
```

For example:

```bash
grep "REQ-20261005-00123" application.log
```

Searching by a unique identifier is often more reliable than searching only by an error message.

---

## 10. Search by Timestamp

If the incident occurred around a known time:

```bash
grep "2026-10-05 14:" application.log
```

This can help narrow a large log file to a specific incident window.

---

## 11. Combine Timestamp and Error Searches

For example:

```bash
grep "2026-10-05" application.log | grep -Ei "error|failed|timeout"
```

This allows you to focus on failures that occurred on a particular date.

---

## 12. Review Systemd Logs

For applications running as Linux services:

```bash
journalctl -u service-name
```

Show recent entries:

```bash
journalctl -u service-name -n 100
```

Follow the service logs:

```bash
journalctl -u service-name -f
```

Show logs from the current boot:

```bash
journalctl -u service-name -b
```

---

## 13. Investigate an Incident

A structured log investigation can follow this process:

### 1. Establish the timeline

Determine:

* When did the issue start?
* When was it first reported?
* When did it stop?
* Were there recent deployments or configuration changes?

### 2. Identify the affected service

Determine which application, API, database, or external service is involved.

### 3. Find a unique identifier

Look for:

* Transaction ID
* Request ID
* Correlation ID
* Customer reference
* Batch ID

### 4. Search the logs

Start with the identifier and then investigate associated errors.

### 5. Identify the failure pattern

Look for:

* Exceptions
* Timeouts
* Authentication failures
* Connection errors
* HTTP errors
* Database errors
* Dependency failures

### 6. Correlate evidence

Compare application logs with:

* Monitoring alerts
* Deployment records
* Server health
* Database activity
* External service status

### 7. Determine the likely cause

Separate the **symptom** from the **root cause**.

Example:

```text
Symptom:
Payment request failed.

Log evidence:
Connection timeout while calling external payment service.

Likely cause:
External dependency was unavailable or unreachable.

Action:
Confirm dependency availability and retry/reprocess according to the approved procedure.

Verification:
Confirm successful transaction processing.
```

---

## 14. Useful Incident Questions

When reviewing logs, ask:

* What failed?
* When did it fail?
* How frequently is it failing?
* Which service generated the error?
* Is the failure internal or external?
* Are multiple users affected?
* Is there a common transaction or request pattern?
* Did the issue begin after a deployment?
* Is the dependency available?
* Has the issue recovered?
* What evidence supports the conclusion?

---

## Application Support Principle

**Do not treat every error message as the root cause.**

An application may report:

```text
HTTP 500 Internal Server Error
```

That is a symptom.

The underlying cause might be:

* Database connectivity failure
* Unhandled application exception
* Invalid configuration
* Dependency failure
* Resource exhaustion
* Authentication failure

The goal of log analysis is to move from the visible symptom to the underlying failure.

---

## Security & Data Protection

Logs can contain sensitive information.

Never publish or commit:

* Passwords
* API keys
* Access tokens
* Customer credentials
* Bank account details
* Personally identifiable information
* Production secrets
* Private connection strings

Use sanitized or fictional examples when documenting incidents publicly.

---

## Troubleshooting Workflow

```text
Incident reported
       ↓
Establish timeline
       ↓
Identify affected service
       ↓
Find transaction/request ID
       ↓
Search logs
       ↓
Identify error pattern
       ↓
Correlate with monitoring/deployments
       ↓
Determine likely root cause
       ↓
Apply approved resolution
       ↓
Verify recovery
       ↓
Document findings
```

## Disclaimer

All examples in this document are generic and intended for learning and demonstration purposes. Production logs and confidential company information should never be published in a public repository.
