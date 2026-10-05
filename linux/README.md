# Linux Support Toolkit

Practical Linux commands and troubleshooting procedures for Application Support and Production Support environments.

## Purpose

This section contains commonly used Linux commands for investigating application issues, checking server health, analyzing logs, monitoring processes, and troubleshooting connectivity.

## Disk Usage

Check overall disk usage:

```bash
df -h
```

Check the size of directories:

```bash
du -sh /path/to/directory
```

Find the largest directories:

```bash
du -h --max-depth=1 /var | sort -hr
```

## Memory & CPU

Check memory usage:

```bash
free -h
```

Check CPU and running processes:

```bash
top
```

Alternative:

```bash
htop
```

## Processes

Search for a running process:

```bash
ps aux | grep process-name
```

Check whether a service is running:

```bash
systemctl status service-name
```

Restart a service:

```bash
sudo systemctl restart service-name
```

## Network Troubleshooting

Test connectivity:

```bash
ping hostname
```

Test a specific port:

```bash
nc -zv hostname 443
```

Check HTTP response:

```bash
curl -I https://example.com
```

Check detailed API connectivity:

```bash
curl -v https://example.com
```

## Log Analysis

View the latest log entries:

```bash
tail -n 100 application.log
```

Follow a log in real time:

```bash
tail -f application.log
```

Search for errors:

```bash
grep -i "error" application.log
```

Search for multiple error patterns:

```bash
grep -Ei "error|exception|failed|timeout" application.log
```

## Useful Troubleshooting Sequence

When investigating an application issue on Linux:

1. Check whether the server is reachable.
2. Check CPU and memory usage.
3. Check available disk space.
4. Confirm the application/service is running.
5. Review recent application logs.
6. Check network connectivity and required ports.
7. Identify the error pattern.
8. Compare the issue with recent deployments or configuration changes.
9. Document findings and escalate when required.

## Important Note

These commands are intended for learning, troubleshooting, and controlled support environments.

Always verify the target server, service, and command before executing changes in production.
