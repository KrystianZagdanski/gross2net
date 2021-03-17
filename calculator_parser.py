from bs4 import BeautifulSoup


class Parser:
    @staticmethod
    def _td2float(td):
        strings_to_replace = {
            "<td colspan=\"4\">": "",
            "</td>": "",
            " ": "",
            ",": "."
        }
        td = str(td)
        for key, val in strings_to_replace.items():
            td = td.replace(key, val)
        try:
            return float(td)
        except ValueError:
            return False

    @staticmethod
    def parse_response(response):
        response_parser = BeautifulSoup(response.content, "html.parser")
        path = ".worker >.table-responsive >.table >tbody >tr"
        results = []
        try:
            table_elements = response_parser.select(path)
            # remove table names and sum
            table_elements.pop(0)
            table_elements.pop(0)
            table_elements.pop(-1)

            for elem in table_elements:
                fields = elem.find_all("td")
                gross = Parser._td2float(fields[1])
                net = Parser._td2float(fields[-1])
                if gross and net:
                    results.append((gross, net))
        except IndexError:
            return False
        return results
