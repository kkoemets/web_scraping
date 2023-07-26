class HtmlCreator:
    @staticmethod
    def create_html_table(rows_elements: list[dict]) -> str:
        table_style: str = """
        <style type="text/css">
        table {
            border-collapse: collapse;
            width: 100%;
            text-align: left;
        }
        th, td {
            padding: 8px;
            border-bottom: 1px solid green;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        </style>
        """

        table_headers: str = "".join(f"<th>{key.capitalize()}</th>" for key in rows_elements[0].keys())

        table_rows: str = "".join(
            f"<tr>{''.join(f'<td>{value}</td>' for value in row.values())}</tr>"
            for row in rows_elements)

        return f"""
        {table_style}
        <table>
          <thead>
            <tr>
              {table_headers}
            </tr>
          </thead>
          <tbody>
            {table_rows}
          </tbody>
        </table>"""
