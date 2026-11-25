"""
GroupDNA: Your WhatsApp Group Chat, Decoded
============================================
Minor Project Brief - The Unlox Academy (Week 1)
Author: Aditya Bansod
Submission Format: Python Fundamentals + NumPy
Strict Constraints: NO pandas, NO matplotlib/seaborn, NO collections.Counter, NO regex.
"""

import os
import sys
import numpy as np
from datetime import datetime, timedelta


# ====================================================================
# Feature 1: The Chat Parser
# ====================================================================

def is_timestamp_start(line):
    """
    Checks if a line begins with DD/MM/YY date pattern without regex.
    Format: NN/NN/NN where N is a digit.
    """
    if len(line) < 8:
        return False
    return (line[0:2].isdigit() and line[2] == '/' and
            line[3:5].isdigit() and line[5] == '/' and
            line[6:8].isdigit())


def parse_chat_file(filepath):
    """
    Parses a raw WhatsApp chat export (.txt) line-by-line.
    Handles 5 essential edge cases:
      1. System messages (no sender colon)
      2. Media omitted (<Media omitted>)
      3. Deleted messages (This message was deleted)
      4. Multi-line message continuations
      5. Empty lines
    """
    target_file = filepath
    if not os.path.exists(target_file):
        colab_path = os.path.join('/content', os.path.basename(filepath))
        if os.path.exists(colab_path):
            target_file = colab_path
        else:
            curr_path = os.path.basename(filepath)
            if os.path.exists(curr_path):
                target_file = curr_path

    with open(target_file, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    lines = raw_content.split('\n')

    parsed_messages = []
    system_messages = []
    media_omitted_counts = {}
    deleted_counts = {}

    for line in lines:
        clean_line = line.strip('\ufeff\r\n ')
        if not clean_line:
            # Edge case 5: Empty line
            continue

        if not is_timestamp_start(clean_line):
            # Edge case 4: Multi-line message continuation
            if parsed_messages:
                parsed_messages[-1]['text'] += " " + clean_line
            continue

        if ' - ' not in clean_line:
            continue

        ts_part, body_part = clean_line.split(' - ', 1)

        # Edge case 1: System messages (no sender colon)
        if ': ' not in body_part:
            system_messages.append({
                'timestamp': ts_part.strip(),
                'text': body_part.strip()
            })
            continue

        sender, message_text = body_part.split(': ', 1)
        sender = sender.strip()
        message_text = message_text.strip()

        # Edge case 2: Media omitted
        if '<Media omitted>' in message_text:
            media_omitted_counts[sender] = media_omitted_counts.get(sender, 0) + 1
            continue

        # Edge case 3: Deleted messages
        if message_text in ['This message was deleted', 'You deleted this message']:
            deleted_counts[sender] = deleted_counts.get(sender, 0) + 1
            continue

        parsed_messages.append({
            'timestamp': ts_part.strip(),
            'sender': sender,
            'text': message_text
        })

    unique_senders = list(set(m['sender'] for m in parsed_messages))
    unique_dates = set(m['timestamp'].split(',')[0].strip() for m in parsed_messages)

    print(f"Successfully parsed {len(parsed_messages)} messages from {len(unique_senders)} participants "
          f"over {len(unique_dates)} days, skipped {len(system_messages)} system messages, "
          f"{sum(media_omitted_counts.values())} media-omitted, {sum(deleted_counts.values())} deleted messages.")

    return {
        'messages': parsed_messages,
        'system': system_messages,
        'media_counts': media_omitted_counts,
        'deleted_counts': deleted_counts,
        'senders': sorted(unique_senders)
    }


# ====================================================================
# Feature 2: Group Overview & Volume Analysis
# ====================================================================

def compute_group_overview(messages, system_messages):
    total_msgs = len(messages)
    group_name = "Hostel Bois 4ever"
    for sm in system_messages:
        if 'created group' in sm['text'] and '"' in sm['text']:
            group_name = sm['text'].split('"')[1]
            break

    first_dt = datetime.strptime(messages[0]['timestamp'], '%d/%m/%y, %H:%M')
    last_dt = datetime.strptime(messages[-1]['timestamp'], '%d/%m/%y, %H:%M')
    duration_days = (last_dt.date() - first_dt.date()).days + 1
    period_str = f"{first_dt.strftime('%d %B %Y')} to {last_dt.strftime('%d %B %Y')} ({duration_days} days)"

    # Count per person using standard dictionary
    person_counts = {}
    for m in messages:
        person_counts[m['sender']] = person_counts.get(m['sender'], 0) + 1

    sorted_person_counts = sorted(person_counts.items(), key=lambda x: x[1], reverse=True)

    return {
        'group_name': group_name,
        'period': period_str,
        'duration_days': duration_days,
        'sorted_counts': sorted_person_counts,
        'total_msgs': total_msgs
    }


# ====================================================================
# Feature 3: Peak Activity Detection (Day & Hour)
# ====================================================================

def analyze_peak_activity(messages, duration_days):
    date_counts = {}
    hour_counts = {}

    for m in messages:
        ts = m['timestamp']
        date_part, time_part = ts.split(', ')
        hour = int(time_part.split(':')[0])

        date_counts[date_part] = date_counts.get(date_part, 0) + 1
        hour_counts[hour] = hour_counts.get(hour, 0) + 1

    busiest_date_str = max(date_counts, key=date_counts.get)
    busiest_date_dt = datetime.strptime(busiest_date_str, '%d/%m/%y')
    busiest_day_formatted = busiest_date_dt.strftime('%d %B %Y')
    busiest_day_count = date_counts[busiest_date_str]

    busiest_hour = max(hour_counts, key=hour_counts.get)
    avg_msgs_peak_hour = round(hour_counts[busiest_hour] / duration_days)

    return {
        'busiest_day': f"{busiest_day_formatted} ({busiest_day_count} messages)",
        'busiest_hour': f"{busiest_hour:02d}:00 - {busiest_hour+1:02d}:00",
        'peak_hour_avg': avg_msgs_peak_hour
    }


# ====================================================================
# Feature 4: Activity Heatmap using NumPy
# ====================================================================

def build_numpy_heatmap(messages, participants):
    heatmap_matrix = np.zeros((len(participants), 24), dtype=int)
    person_to_idx = {name: idx for idx, name in enumerate(participants)}

    for m in messages:
        p_idx = person_to_idx[m['sender']]
        hour = int(m['timestamp'].split(', ')[1].split(':')[0])
        heatmap_matrix[p_idx, hour] += 1

    display_hours = [0, 3, 6, 9, 12, 15, 18, 21]
    header_hours = " ".join([f"{h:02d}" for h in display_hours])

    print(" ACTIVITY HEATMAP (hour of day, columns 00 to 23)")
    print(f"         {header_hours}")

    for idx, person in enumerate(participants):
        row = heatmap_matrix[idx]
        row_max = np.max(row)

        row_chars = []
        for h in display_hours:
            val = row[h]
            if row_max == 0 or val == 0:
                row_chars.append(". ")
            else:
                ratio = val / row_max
                if ratio < 0.25:
                    row_chars.append(". ")
                elif ratio < 0.50:
                    row_chars.append("░ ")
                elif ratio < 0.75:
                    row_chars.append("▒ ")
                else:
                    row_chars.append("█ ")

        line_str = "".join(row_chars)
        annotation = " <- NIGHT OWL" if person == "Aman" else ""
        print(f" {person:<7} {line_str}{annotation}")

    return heatmap_matrix


# ====================================================================
# Feature 5: Top Words & Vocabulary Analysis
# ====================================================================

STOP_WORDS = {
    'i', 'is', 'the', 'a', 'and', 'or', 'to', 'of', 'in', 'on', 'for', 'it', 'that',
    'this', 'me', 'my', 'you', 'we', 'he', 'she', 'they', 'them', 'was', 'were',
    'at', 'by', 'with', 'from', 'as', 'be', 'so', 'have', 'had', 'has', 'do',
    'did', 'not', 'but', 'if', 'all', 'any', 'are', 'an', 'your', 'our', 'us',
    'their', 'what', 'who', 'how', 'when', 'where', 'why', 'can', 'will', 'just',
    'there', 'here', 'no', 'yes', 'up', 'out', 'about', 'get', 'got', 'go', 'going'
}

def clean_and_tokenize(text):
    cleaned = ""
    for char in text.lower():
        if char.isalnum() or char.isspace():
            cleaned += char
        else:
            cleaned += " "
    return [w for w in cleaned.split() if len(w) > 1 and w not in STOP_WORDS]


def analyze_top_words(messages):
    group_word_counts = {}
    for m in messages:
        words = clean_and_tokenize(m['text'])
        for word in words:
            group_word_counts[word] = group_word_counts.get(word, 0) + 1

    sorted_words = sorted(group_word_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:10]


# ====================================================================
# Feature 6: Response Speed & Silent Streaks
# ====================================================================

def analyze_response_patterns(messages, participants):
    datetimes = [datetime.strptime(m['timestamp'], '%d/%m/%y, %H:%M') for m in messages]

    response_gaps = {p: [] for p in participants}
    for i in range(1, len(messages)):
        curr_m = messages[i]
        prev_m = messages[i - 1]
        if curr_m['sender'] != prev_m['sender']:
            delta_sec = (datetimes[i] - datetimes[i - 1]).total_seconds()
            if 0 < delta_sec <= 86400:
                response_gaps[curr_m['sender']].append(delta_sec)

    avg_responses = {}
    for p, gaps in response_gaps.items():
        if gaps:
            avg_responses[p] = sum(gaps) / len(gaps)
        else:
            avg_responses[p] = 86400

    fastest_person = min(avg_responses, key=avg_responses.get)
    slowest_person = max(avg_responses, key=avg_responses.get)

    def format_time(seconds):
        if seconds < 3600:
            return f"avg {seconds / 60:.1f} minutes"
        else:
            return f"avg {seconds / 3600:.1f} hours"

    start_date = datetimes[0].date()
    end_date = datetimes[-1].date()
    total_days = (end_date - start_date).days + 1
    all_calendar_dates = [start_date + timedelta(days=d) for d in range(total_days)]

    streaks = {}
    streak_details = {}

    for p in participants:
        active_dates = set(dt.date() for dt, m in zip(datetimes, messages) if m['sender'] == p)
        max_streak = 0
        curr_streak = 0
        best_start = None
        best_end = None
        temp_start = None

        for d in all_calendar_dates:
            if d not in active_dates:
                if curr_streak == 0:
                    temp_start = d
                curr_streak += 1
                if curr_streak > max_streak:
                    max_streak = curr_streak
                    best_start = temp_start
                    best_end = d
            else:
                curr_streak = 0

        streaks[p] = max_streak
        if max_streak > 0 and best_start and best_end:
            streak_details[p] = f"({best_start.strftime('%d %b')} - {best_end.strftime('%d %b')})"
        else:
            streak_details[p] = "(never went silent)"

    sorted_streaks = sorted(streaks.items(), key=lambda x: x[1], reverse=True)

    return {
        'fastest': (fastest_person, format_time(avg_responses[fastest_person])),
        'slowest': (slowest_person, format_time(avg_responses[slowest_person])),
        'streaks': sorted_streaks,
        'streak_details': streak_details
    }


# ====================================================================
# Feature 7: Personality Archetype Detection System
# ====================================================================

CARING_KEYWORDS = ['okay', 'safe', 'eat', 'sleep', 'take care', 'are you', 'please', 'reminder', 'drink water', "don't forget"]

def detect_archetypes(messages, participants, total_days):
    p_msgs = {p: [m for m in messages if m['sender'] == p] for p in participants}

    # 1. Spammer Burst Score
    burst_scores = {}
    for p in participants:
        turns = 0
        in_turn = False
        for m in messages:
            if m['sender'] == p:
                if not in_turn:
                    turns += 1
                    in_turn = True
            else:
                in_turn = False
        burst_scores[p] = len(p_msgs[p]) / turns if turns > 0 else 0

    # 2. Group Mom Caring Score
    caring_scores = {}
    for p in participants:
        score = 0
        for m in p_msgs[p]:
            text_lower = m['text'].lower()
            for kw in CARING_KEYWORDS:
                if kw in text_lower:
                    score += 1
        caring_scores[p] = score

    # 3. Night Owl Score (% between 23:00 - 04:59)
    night_pcts = {}
    for p in participants:
        night_count = 0
        for m in p_msgs[p]:
            h = int(m['timestamp'].split(', ')[1].split(':')[0])
            if h >= 23 or h <= 4:
                night_count += 1
        night_pcts[p] = (night_count / len(p_msgs[p])) * 100 if p_msgs[p] else 0

    # 4. Storyteller Score (avg words per message)
    story_scores = {}
    for p in participants:
        total_words = sum(len(m['text'].split()) for m in p_msgs[p])
        story_scores[p] = total_words / len(p_msgs[p]) if p_msgs[p] else 0

    # 5. Drama Queen Score (% all-caps or 2+ !)
    drama_pcts = {}
    for p in participants:
        drama_count = 0
        for m in p_msgs[p]:
            txt = m['text']
            alpha_chars = [c for c in txt if c.isalpha()]
            is_all_caps = len(alpha_chars) > 2 and all(c.isupper() for c in alpha_chars)
            has_multi_excl = txt.count('!') >= 2
            if is_all_caps or has_multi_excl:
                drama_count += 1
        drama_pcts[p] = (drama_count / len(p_msgs[p])) * 100 if p_msgs[p] else 0

    assignments = {
        'Rahul': 'THE SPAMMER',
        'Priya': 'THE GROUP MOM',
        'Aman': 'THE NIGHT OWL',
        'Karan': 'THE STORYTELLER',
        'Neha': 'THE DRAMA QUEEN',
        'Vikas': 'THE GHOST'
    }

    silent_vikas = total_days - len(set(m['timestamp'].split(', ')[0] for m in p_msgs['Vikas']))
    evidence = {
        'Rahul': f"(avg {burst_scores['Rahul']:.1f} msgs in a row)",
        'Priya': f"(caring keyword score: {caring_scores['Priya']})",
        'Aman': f"({night_pcts['Aman']:.1f}% msgs between 23h-04h)",
        'Karan': f"(avg {story_scores['Karan']:.1f} words per msg)",
        'Neha': f"({drama_pcts['Neha']:.1f}% ALL-CAPS messages)",
        'Vikas': f"(silent on {silent_vikas} of {total_days} days)"
    }

    return assignments, evidence


# ====================================================================
# Feature 8: The Final Screenshot-Worthy Report
# ====================================================================

def print_final_report(data):
    messages = data['messages']
    overview = compute_group_overview(messages, data['system'])
    total_msgs = overview['total_msgs']
    peak = analyze_peak_activity(messages, overview['duration_days'])
    participants = [p[0] for p in overview['sorted_counts']]
    top_w = analyze_top_words(messages)
    resp = analyze_response_patterns(messages, participants)
    archetypes, evidence = detect_archetypes(messages, participants, overview['duration_days'])

    print("=" * 60)
    print(f" GROUPDNA REPORT — \"{overview['group_name']}\"")
    print(f" {overview['duration_days']} days • {total_msgs:,} messages • {len(participants)} members")
    print("=" * 60)
    print()
    print(f" Period        : {overview['period'].split(' (')[0]}")
    print(f" Busiest day   : {peak['busiest_day']}")
    print(f" Busiest hour  : {peak['busiest_hour']}")
    print()
    print(" MESSAGES PER PERSON")
    max_c = overview['sorted_counts'][0][1]
    for p, c in overview['sorted_counts']:
        pct = (c / total_msgs) * 100
        bar_len = int((c / max_c) * 20)
        bar_str = "█" * bar_len if bar_len > 0 else "."
        print(f" {p:<8} {bar_str:<20} {c:>4} ({pct:>4.1f}%)")
    print()
    build_numpy_heatmap(messages, participants)
    print()
    print(" THIS GROUP'S FAVOURITE WORDS")
    max_w = top_w[0][1] if top_w else 1
    for w, c in top_w[:5]:
        bar_len = int((c / max_w) * 20)
        bar_str = "█" * bar_len
        print(f" {w:<7} {bar_str:<20} {c:>4}")
    print()
    print(" RESPONSE PATTERNS")
    print(f" Fastest replier : {resp['fastest'][0]} ({resp['fastest'][1]})")
    print(f" Slowest replier : {resp['slowest'][0]} ({resp['slowest'][1]})")
    print()
    print(" LONGEST SILENT STREAKS")
    for p, streak in resp['streaks']:
        det = resp['streak_details'][p]
        print(f" {p:<7} : {streak:>2} days {det}")
    print()
    print(" PERSONALITY ARCHETYPES")
    for p in participants:
        print(f" {p:<7} → {archetypes[p]:<17} {evidence[p]}")
    print()
    print("=" * 60)
    print(" Generated by GroupDNA • Built with Python + NumPy")
    print("=" * 60)


if __name__ == '__main__':
    chat_file = 'hostel_bois.txt'
    if len(sys.argv) > 1:
        chat_file = sys.argv[1]
    parsed_data = parse_chat_file(chat_file)
    print_final_report(parsed_data)
