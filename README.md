## usage
```python3
$ uv run main.py
```


```bash
CLI Timer Started. Commands: start <task>, pause, report, exit
>> start fix: prevent racing of requests
Started task: 'fix: prevent racing of requests' at 2025-05-06T01:29:14.744650+00:00 UTC
>> 
```
```>> pause```

```bash
CLI Timer Started. Commands: start <task>, pause, report, exit
>> start fix: prevent racing of requests
Started task: 'fix: prevent racing of requests' at 2025-05-06T01:29:14.744650+00:00 UTC
>> pause
Paused 'fix: prevent racing of requests' after 0:02:59
>> 
```

```bash
$ cat tasks.json
```

```json
{
  "fix: prevent racing of requests": "0:02:59"
}
```
