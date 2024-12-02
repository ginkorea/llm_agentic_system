class ContentParser:
    def parse_content(self, content, format):
        if format == "plain":
            return self.parse_plain_text(content)
        elif format == "html":
            return self.parse_html(content)
        elif format == "markdown":
            return self.parse_markdown(content)
        else:
            raise ValueError("Unsupported format")

    def parse_plain_text(self, content):
        return content

    def parse_html(self, content):
        # Implementation of HTML parsing
        pass

    def parse_markdown(self, content):
        # Implementation of markdown parsing
        pass