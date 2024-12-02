# query_arxiv/date_filter.py
from datetime import datetime, timedelta

class DateFilter:
    def filterByRecentDays(self, papers, recent_days: int):
        recent_date = datetime.now() - timedelta(days=recent_days)
        return [paper for paper in papers if datetime.fromisoformat(paper.published) > recent_date]