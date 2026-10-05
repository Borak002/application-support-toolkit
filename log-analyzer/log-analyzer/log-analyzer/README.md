# Python Log Analyzer

A lightweight Python utility for analyzing application logs and identifying common incident indicators.

## Purpose

Application Support Engineers frequently need to review large log files during incident investigation.

This tool provides a simple automated summary of common indicators such as:

* Errors
* Exceptions
* Timeouts
* HTTP 401
* HTTP 404
* HTTP 500
* HTTP 503

The project uses fictional sample data and does not require access to any production environment.

## Requirements

* Python 3.x

No external Python packages are required.

## Usage

Run the analyzer against a log file:

```bash
python3 log_analyzer.py sample.log
```

## Example Output

```text
=============================================
        APPLICATION LOG ANALYZER
=============================================
Log file:       sample.log
Total entries:  20
---------------------------------------------
ERROR           8
EXCEPTION       2
TIMEOUT         3
HTTP 500        2
HTTP 401        1
HTTP 404        1
HTTP 503        1
---------------------------------------------
STATUS: Incident indicators detected.
=============================================
```

## How It Works

The application:

1. Reads the supplied log file.
2. Processes each log entry.
3. Searches for predefined error patterns.
4. Counts each matching category.
5. Produces a summary report.
6. Returns an error if the log file cannot be accessed.

## Application Support Use Cases

This type of utility can assist with:

* Initial incident investigation
* Log triage
* Error pattern identification
* Post-deployment validation
* Production troubleshooting
* Identifying recurring failures
* Preparing evidence for escalation

## Example Investigation

A support engineer receives a report that an API is intermittently failing.

Instead of manually reviewing thousands of log entries, the engineer can run:

```bash
python3 log_analyzer.py application.log
```

The resulting summary can help identify whether the log contains recurring:

* HTTP 500 errors
* Authentication failures
* Timeouts
* Exceptions
* Service-unavailable responses

The engineer can then investigate the relevant timestamps and request identifiers in more detail.

## Future Improvements

Possible enhancements include:

* Timestamp filtering
* Transaction/request ID extraction
* CSV report generation
* JSON output
* Severity-based filtering
* Response-time analysis
* Configurable error patterns
* Automated alerting
* Integration with monitoring systems

## Security

Never analyze or publish confidential production logs containing:

* Customer information
* Passwords
* API keys
* Access tokens
* Bank account information
* Personally identifiable information
* Internal credentials

Use sanitized data when testing or demonstrating the project publicly.

## Disclaimer

This is an independent technical project created for learning and demonstration of Application Support engineering skills. The sample log data is fictional.
