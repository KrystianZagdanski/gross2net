import requests
from bs4 import BeautifulSoup
from form_data import form_data, calculator_token_link, calculator_link
from calculator_parser import Parser


class Calculator:
    _calculator_link = calculator_link
    _calculator_token_link = calculator_token_link
    _form_data = form_data
    _cookies = None

    @classmethod
    def _set_token_and_cookies(cls):
        response = requests.get(calculator_token_link)
        if response.status_code != 200:
            return False
        cls._cookies = response.cookies
        # find and set token
        response_parser = BeautifulSoup(response.content, "html.parser")
        token = response_parser.find(id="sedlak_calculator__token").get("value")
        cls._form_data["sedlak_calculator[_token]"] = token

    @classmethod
    def set_gross(cls, gross):
        cls._form_data["sedlak_calculator[earnings]"] = gross[0]
        for i, val in enumerate(gross):
            cls._form_data[f"sedlak_calculator[monthlyEarnings][{i}]"] = val

    @classmethod
    def set_end26year(cls, val=True):
        if val:
            cls._form_data["work_end26Year"] = "on"
            cls._form_data["sedlak_calculator[end26Year]"] = 1
            del cls._form_data["sedlak_calculator[freeCost]"]
        else:
            cls._form_data["sedlak_calculator[freeCost]"] = 1
            del cls._form_data["work_end26Year"]
            del cls._form_data["sedlak_calculator[end26Year]"]

    @classmethod
    def set_the_same_city(cls, val=True):
        if val:
            cls._form_data["sedlak_calculator[theSameCity]"] = 1
        else:
            del cls._form_data["sedlak_calculator[theSameCity]"]

    @classmethod
    def set_ppk(cls, ppk=None):
        if ppk:
            cls._form_data["sedlak_calculator[PPK]"] = 1
            cls._form_data["sedlak_calculator[employeePercent]"] = ppk

    @classmethod
    def set_values(cls, gross, end26year=None, the_same_city=None, ppk=None):
        cls.set_gross(gross)
        if end26year:
            cls.set_end26year(end26year)
        if the_same_city:
            cls.set_the_same_city(the_same_city)
        if ppk:
            cls.set_ppk(ppk)

    @classmethod
    def get_results(cls):
        cls._set_token_and_cookies()
        response = requests.post(calculator_link, data=form_data, cookies=cls._cookies)
        if response.status_code != 200:
            return False
        return Parser.parse_response(response)
