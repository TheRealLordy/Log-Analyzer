import re
from collections import Counter, defaultdict

LOGFILE = "OpenSSH_2k.log"

# Pattern for failed login attempts
FAILED_PATTERN = re.compile(
    r'^(\w+\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*'
    r'Failed password for (?:invalid user )?(\S+) from (\S+) port'
)

# Pattern for successful logins
ACCEPTED_PATTERN = re.compile(
    r'^(\w+\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*'
    r'Accepted \S+ for (\S+) from (\S+) port'
)

ip_attempts         = Counter()
ip_first_time       = {}
ip_last_time        = {}
ip_username_counter = defaultdict(Counter)

accepted_logins     = []  

try:
    with open(LOGFILE, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip()
            if not line:
                continue

           
            m = FAILED_PATTERN.search(line)
            if m:
                ts   = m.group(1)
                user = m.group(2)
                ip   = m.group(3)

                ip_attempts[ip] += 1
                ip_username_counter[ip][user] += 1

                if ip not in ip_first_time:
                    ip_first_time[ip] = ts
                ip_last_time[ip] = ts
                continue

            
            m = ACCEPTED_PATTERN.search(line)
            if m:
                accepted_logins.append((m.group(1), m.group(2), m.group(3)))

except FileNotFoundError:
    print(f"Error: file '{LOGFILE}' not found.")
    exit(1)
except Exception as e:
    print("Error:", e)
    exit(1)


# Failed attempts table

print("\nFailed login attempts (sshd password failures)")
print("-" * 80)
print(f"{'Count':>6}   {'First seen':<16}   {'Last seen':<16}   {'IP':<15}   {'Uniq users':>10}   Most tried")
print("-" * 80)

if not ip_attempts:
    print("  No failed password attempts found.")
else:
    for ip, cnt in ip_attempts.most_common(15):
        first     = ip_first_time.get(ip, "—")
        last      = ip_last_time.get(ip, "—")
        uniq      = len(ip_username_counter[ip])
        top_users = ip_username_counter[ip].most_common(3)
        users_str = ", ".join(f"{u} ({c}×)" for u, c in top_users) or "(none)"
        print(f"{cnt:6d}   {first:<16}   {last:<16}   {ip:<15}   {uniq:>10}   {users_str}")


# Accepted logins

print(f"\nSuccessful logins")
print("-" * 55)

if not accepted_logins:
    print("  No successful logins found.")
else:
    print(f"  {'Timestamp':<20}   {'User':<15}   IP")
    print("  " + "-" * 50)
    for ts, user, ip in accepted_logins:
        print(f"  {ts:<20}   {user:<15}   {ip}")


# Summary

print("\n" + "=" * 55)
print("Summary")
print("=" * 55)
print(f"  Total unique attacking IPs  : {len(ip_attempts)}")
print(f"  Total failed attempts       : {sum(ip_attempts.values())}")
print(f"  Total successful logins     : {len(accepted_logins)}")
if ip_attempts:
    top_ip  = ip_attempts.most_common(1)[0]
    top_usr = Counter()
    for counter in ip_username_counter.values():
        top_usr.update(counter)
    print(f"  Most aggressive IP          : {top_ip[0]} ({top_ip[1]} attempts)")
    print(f"  Most targeted username      : {top_usr.most_common(1)[0][0]} ({top_usr.most_common(1)[0][1]} times)")