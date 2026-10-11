# Security

Remit is a rulebook and a set of checks, not a running service. The bugs that matter most are in the scripts: one that runs something it was not meant to when it reads a record or a file, or an install step that fetches or runs the wrong thing. Please report those. A rule you disagree with is a normal issue.

## How to report

Use GitHub's private report: open the **Security** tab of this repository and choose **Report a vulnerability**. Please do not open a public issue for it until it is fixed.

## What to expect

This is a one-person project, so there is no formal response time. A report that comes with steps to reproduce it gets read promptly.

## Supported versions

Only the latest commit on `main` is supported.
