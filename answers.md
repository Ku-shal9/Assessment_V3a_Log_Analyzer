# Q1: How to run on a fresh machine

## Install

- Python 3.8+
- pip
- pandas

```bash
pip install pandas
```

## Run

```bash
cd /path/to/log-analyzer
python3 scripts/generate_logs.py
cd app
python3 main.py
```

Output: `app/log_report.csv`

# Q2: Stack choice: Python

## Why Python?

```bash
Particularly, log anayzer is task centered to DevOps ecosystem, particulalry, which is particulalry surrounded by text processing, data processing, and an analytics pipeline. The task involves heavy string manipulation, parsing, and maybe counting (not necessarily). Since python offers so much of standard libraries, that can handle regex, json files, collection for counting; we don't need anything extra, not any heavy dependecy. Likewise, Python is effective for semi-structured and schema-flexible worlkload, as the analyzer handles standard logs, malformed logs, json lines, and multiple timestamp formats.  Python has robust testing frameworks, such as unittest and pytest, which make it easy to write and run automated tests for the analyzer. The main thing is it is platform independent.

Personally, I'm mostly familiar with it and writing in Python feels natural to me.

Maybe the only drawback is heavy runtime. However, the taks is more of a I/O bound, so the main delay actually arises from disk reading. Since disk operations are again slower than python scripts, the lower raw performance compared to languages, such as C++ is not a major issue.
```

## What could be the worst choice?

```bash
To be honest for this project, using a heavy frontend stack, such as React or Node might be not a very good choice. This is a fully backend proecssing task centered to servers, and since Node is built around async I/O, reading line by line (synchronous tasks) would hurt JS frameworks identity.
Why to read line-by-line? It is because the testing ranges as defined in instruction ranges from few hundreds to few hundred thousands. If everything is loaded at once, the RAM will be fully occupied and the CPU will be steaming out.
```

# Q3: Edge-Case Handled: Two-token timestamp

## What was handled?

```bash
Since our analyzer can be exposed to whatever data, there can be a case of two-token timestamps such as 2024/03/15 14:23:01 or 15-Mar-2024 14:23:01. Since they contain spaces inside themselves, they are parsed as two tokens not a single one. What this does is shift the entire field positions. This was one of the challenging edge-case because it is a structural problem.

File: parser.py
Line:  The multi-token behavior is extract_timestamp_prefix (lines 31–43), called from line 112, with formats at lines 11–12, 14 and parsing at lines 51–55.
```

## What would have happened if not handled?

```bash
As said earlier if this was not handled, then the entire field tokens will be shifted and the logic will fail instantly. If the program doesn't find the specific field on specific token, it would either crash or produce wrong data.
```

# Q4: AI Usage

### Question to ChatGPT

```bash
Uploaded the PDF and asked to generate a detailed explanation in layman terms of what's said in the PDF.
Also I aksed it to generate a step-wise instruction on what to do in each iteration.
```

### What it gave me?

```bash
Detailed instruction on what's mentioned in the PDF in a very layman understanding with key points which I shouldn't miss out during the development.
```

### Question to Claude (1)

```bash
Generate me a simple architecture to make a server log analyzer. Similalry, give me an incremental prototyping instruction...
```

### What it gave me?

```bash
Developed a simple flow of how the functions and modules interact with each other, how the data flows. Similalry, instruction on how to proceed on each increment.
```

### Question to Claude (2)

```bash
How can i handle JSON lines mixed with the standard logs file?
```

### What it gave me?

```bash
Use Python's standard json library with .get() function and parse the JSON line.
```

### Question to Claude (3)

```bash
What would be an ideal solution to the two-token timestamp case?
```

### What it gave me?

```bash
Detect whether the timestamp uses two tokens, then merge those two tokens into one timestamp. Suggested a hardcoded regex pattern matching for two-token timestamps.
```

### Change in output

> For this third question, I changed the cursor's output and adopted a more resilient and simple method using slicing. Claude gave me a hardcoded regex pattern matching for only two-cases. Thus, it would silently fail if any extra token appears. What i did was implemted a multi-token timestamp, since there won't be always the case that only two-token timestamp will appear. there can be cases where multiple might appear. However, I have also hard-coded that, it would only check for maximum of six; but still it can be changed later on.

### Question to ChatGPT

```bash
How can i use collections module?
```

### What it gave me?

```bash
Collections offer two important data structures 'counter' and 'defaultdict' that can be used for my project. Counter can be imported from the collections module for frequency counting of status codes, path appearances, or most frequent IPs. Similalry, defaultdict can be used for grouping logs. Whats special about defaultdict is, it automatically creates a default value when the key doesn't exist.
```

### Question to Cursor

```bash
Eventhough my parser handles many of the cases, it is still not resillient enough when it sees thousands of unseen logs. What can be done in such case?
```

### What it gave me?

```bash
Focus on predictable behavior, skip what you can't parse, count it, parse everything that matches your rules, while nor pretending a skipped line was analyzed.
```

# Q5: Honest Gap

### One thing that is not good enough

```bash
The parser survives the bad data correctly, but it doesn't explain the failures very well; not so graceful.
In order to guarantee the safety of the pipeline, it kind of rejects the bad line. So when it sees the unseen data, it might reject tons of them.  This enforces that parser might not be able to distinguish between "true garbage" and "almost valid lines" that failed on one field.
```

### How i found the gap?

> I consulted with my professor who also handles the college server. I showed him the project and with the help of him, I was able to get actual server logs from college. While it was handling the timestamps in some-cases, the analyzer couldn't extract any meaningful information.

### What would i fix in other day?

```bash
Implement a structured parse result solution instead of returning only a parsed log dictionary or None when parsing fails. Right now, when a line fails, the parser just skips it and increments something like malformed_lines += 1, which tells the parse failed but there is no absolute reason on why it failed.

Thus, as aforesaid, what would be a better option is to return something like when succeeded ParseResult(parsed=data, error=None), when failed parse could return ParseResult(parsed=None, error="JSON_INVALID") or ParseResult(parsed=None, error="TIMESTAMP_AMBIGUOUS").
```
