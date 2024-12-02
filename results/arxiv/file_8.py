# main.py
from workbench.query_arxiv.query_arxiv import QueryArXiv
from workbench.query_arxiv.query_params import QueryParams
import argparse

def main():
    parser = argparse.ArgumentParser(description='Query ArXiv database.')
    parser.add_argument('--category', type=str, help='Category of the paper')
    parser.add_argument('--title', type=str, help='Keyword for the title')
    parser.add_argument('--author', type=str, help='Keyword for the author')
    parser.add_argument('--abstract', type=str, help='Keyword in the abstract')
    parser.add_argument('--recent_days', type=int, required=True, help='Filter papers from the most recent k days')
    parser.add_argument('--to_file', type=str, help='Path to save the results in CSV format')
    parser.add_argument('--verbose', action='store_true', help='Flag to print results to the console')

    args = parser.parse_args()
    params = QueryParams(
        category=args.category,
        title=args.title,
        author=args.author,
        abstract=args.abstract,
        recent_days=args.recent_days
    )

    query_arxiv = QueryArXiv()
    papers = query_arxiv.executeQuery(params)

    if args.to_file:
        query_arxiv.saveResultsToCSV(papers, args.to_file)
    if args.verbose or not args.to_file:
        query_arxiv.printResults(papers, args.verbose)

if __name__ == '__main__':
    main()