class HtmlCreator:
    @staticmethod
    def create_html_table(rows_elements: list[dict]) -> str:
        table_rows = "".join(
            f"<tr>{''.join(f'<td>{value}</td>' for value in row.values())}</tr>"
            for row in rows_elements
        )

        return f"<table>{table_rows}</table>"
