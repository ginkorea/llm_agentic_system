import unittest
from workbench.query_arxiv.date_filter import DateFilter
from workbench.query_arxiv.paper import Paper
from datetime import datetime

class TestDateFilter(unittest.TestCase):

    def test_filter_by_recent_days(self):
        papers = [
            Paper("cs.CL", "Old Paper", "Old Author", "Old Abstract", "2022-01-01", "http://arxiv.org/abs/1234"),
            Paper("cs.CL", "Recent Paper", "Recent Author", "Recent Abstract", datetime.now().isoformat(), "http://arxiv.org/abs/5678")
        ]
        filter = DateFilter()
        recent_papers = filter.filterByRecentDays(papers, 30)
        self.assertEqual(len(recent_papers), 1)
        self.assertEqual(recent_papers[0].title, "Recent Paper")

if __name__ == '__main__':
    unittest.main()