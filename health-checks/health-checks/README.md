# Service Health Checks

A lightweight Bash-based health-check utility for Application Support and Production Support environments.

## What It Does

The script checks:

* Service availability
* HTTP response status
* Response time
* Basic connectivity failures
* Unhealthy HTTP responses

It returns an appropriate exit code so it can also be integrated into automation or monitoring workflows.

## Usage

Make the script executable:

```bash
chmod +x health_check.sh
```

Run it against the default test endpoint:

```bash
./health_check.sh
```

Test a specific service:

```bash
./health_check.sh https://example.com
```

## Example

```text
======================================
       SERVICE HEALTH CHECK
======================================
Target: https://example.com
Time:   Mon Oct 05 14:30:00 WAT
--------------------------------------
HTTP Status:    200
Response Time:  0.245s
--------------------------------------
STATUS: HEALTHY
```

## HTTP Status Handling

| Status | Interpretation                        |
| ------ | ------------------------------------- |
| 2xx    | Service is responding successfully    |
| 3xx    | Service is responding with a redirect |
| 000    | Connection could not be established   |
| 4xx    | Client/request-related failure        |
| 5xx    | Server-side failure                   |

## Exit Codes

The script returns:

```text
0 → Service is available
1 → Service is unavailable or returned an unhealthy response
```

This makes it possible to use the script in automation and monitoring pipelines.

## Application Support Use Cases

This type of health check can be useful for:

* API availability checks
* Production monitoring
* Deployment verification
* Post-release validation
* Incident investigation
* Scheduled service checks
* Basic uptime monitoring

## Production Considerations

For production monitoring, a health check should ideally be extended with:

* Authentication handling
* TLS certificate validation
* DNS checks
* TCP port checks
* Response-body validation
* Retry logic
* Alerting
* Centralized logging
* Monitoring dashboards

## Security

Do not hard-code:

* API keys
* Passwords
* Access tokens
* Private endpoints
* Production credentials

Use environment variables or a secure secrets-management system when authentication is required.

## Disclaimer

This is an independent technical project created for learning, demonstration, and Application Support engineering practice.
