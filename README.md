# SSH Log Analyzer

A Python script that parses OpenSSH log files and reports failed and successful login attempts.

## What it does

- Reads through an SSH log file line by line
- Detects **failed** login attempts and tracks which IP sent them, when, and which usernames were tried
- Detects **successful** logins and lists them separately
- Prints a summary table with the top 15 most aggressive IPs

## Output

**Failed attempts table** — one row per IP, sorted by attempt count:

| Column | Description |
|---|---|
| Count | Total failed attempts from that IP |
| First seen | Timestamp of the first attempt |
| Last seen | Timestamp of the most recent attempt |
| IP | Source IP address |
| Uniq users | How many different usernames were tried |
| Most tried | The top 3 usernames attempted |

**Successful logins** — timestamp, username, and IP for every accepted login.

**Summary** — totals and the most aggressive IP and most targeted username.

## How to use it

1. Put `ssh_log_analyzer.py` in the same folder as your log file
2. Edit line 4 to point to your log file: `LOGFILE = "your_log.log"`
3. Run it:

```bash
python ssh_log_analyzer.py
```

## Requirements

- Python 3.x
- No extra libraries needed (uses only the standard library)

## Example output

```
Failed login attempts (sshd password failures)
--------------------------------------------------------------------------------
 Count   First seen         Last seen          IP                Uniq users   Most tried
--------------------------------------------------------------------------------
   286   Dec 10 10:54:29    Dec 10 11:04:43    183.62.140.253            10   root (276�), oracle (2�), zhangyan (1�)
    80   Dec 10 09:12:48    Dec 10 09:20:02    187.141.143.180           28   root (46�), oracle (4�), git (2�)
    46   Dec 10 09:11:21    Dec 10 11:04:45    103.99.0.122              19   admin (10�), root (6�), user (4�)
    26   Dec 10 07:27:52    Dec 10 07:28:51    112.95.230.3               3   root (24�), pgadmin (1�), utsims (1�)
    17   Dec 10 08:24:45    Dec 10 08:26:24    5.188.10.180               6   admin (11�), default (2�), 0 (1�)
    17   Dec 10 09:07:58    Dec 10 09:12:59    185.190.58.151             3   admin (15�), 123 (1�), api (1�)
     7   Dec 10 07:32:27    Dec 10 07:34:23    123.235.32.19              1   root (7�)
     6   Dec 10 10:14:01    Dec 10 10:14:13    119.4.203.64               1   admin (6�)
     5   Dec 10 07:07:45    Dec 10 10:21:09    52.80.34.196               3   matlab (3�), test9 (1�), test (1�)
     5   Dec 10 10:04:54    Dec 10 10:05:22    60.2.12.12                 1   root (5�)
     3   Dec 10 08:33:26    Dec 10 08:33:31    103.207.39.212             3   support (1�), uucp (1�), admin (1�)
     3   Dec 10 09:18:30    Dec 10 09:18:35    103.207.39.16              3   support (1�), uucp (1�), admin (1�)
     2   Dec 10 06:55:48    Dec 10 07:08:30    173.234.31.186             1   webmaster (2�)
     2   Dec 10 07:11:44    Dec 10 10:55:10    202.100.179.208            2   chen (1�), cheng (1�)
     2   Dec 10 07:13:43    Dec 10 07:13:56    5.36.59.76                 1   root (2�)

Successful logins
-------------------------------------------------------
  Timestamp              User              IP
  --------------------------------------------------
  Dec 10 09:32:20        fztu              119.137.62.142

=======================================================
Summary
=======================================================
  Total unique attacking IPs  : 23
  Total failed attempts       : 519
  Total successful logins     : 1
  Most aggressive IP          : 183.62.140.253 (286 attempts)
  Most targeted username      : root (370 times)

```

## What I learned building this

- Using `re` (regular expressions) to extract structured data from unstructured text
- Using `Counter` and `defaultdict` from `collections` for efficient counting
- Reading and handling file errors gracefully with `try/except`
- Formatting terminal output with f-strings and alignment specifiers
