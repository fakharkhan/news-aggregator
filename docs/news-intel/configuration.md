### Configuration

Edit `config/topics.yaml`:

```yaml
topics:
  - IMF program
  - energy prices
  - CPEC
  - inflation Pakistan
  - AI regulation
  - semiconductor supply chain

categories:
  Pakistan (Local):
    keywords:
      - Pakistan
      - Lahore
      - Karachi
      - ...

feeds:
  - name: Dawn Pakistan
    url: https://www.dawn.com/feed
    category: Pakistan (Local)
```

- **topics**: words/phrases to prioritize and surface in summaries.
- **categories**: each category includes indicator keywords used for heuristics.
- **feeds**: list of RSS/Atom feeds with optional default category.

Advanced:
- Set `NEWS_INTEL_TOPICS` to point to a custom YAML file.
- Tune classification in `src/news_intel/classify.py`.

