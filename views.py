from abc import ABC, abstractmethod
from terminaltables import AsciiTable


class AbstractView(ABC):
    def __init__(self):
        self.repositories = {}

    @abstractmethod
    def draw(self):
        pass

    def set_repository(self, name, repository):
        self.repositories[name] = repository


class AddCost(AbstractView):
    SHORTCUT = 'dk'
    LABEL = 'Dodaj koszt'

    def draw(self):
        print(AddCost.LABEL)
        name = input('Tytuł: ')
        amount = float(input('Wartość: '))
        found_category = False

        while not found_category:
            try:
                category_name = input('Kategoria: ')
                category_id, _ = self.repositories['category'].get_by_name(category_name)
                found_category = True
            except TypeError:
                found_category = False

        self.repositories['entry'].save(name, category_id, amount * -1)


class ListCosts(AbstractView):
    SHORTCUT = 'wk'
    LABEL = 'Wypisz koszty'

    def draw(self):
        print(ListCosts.LABEL)
        rows = [
            ['data dodania', 'kwota', 'kategoria']
        ]
        for _, created_at, amount, category in self.repositories['entry'].get_costs():
            rows.append([created_at, amount, category])

        table = AsciiTable(rows)
        print(table.table)


class AddIncome(AbstractView):
    SHORTCUT = 'dp'
    LABEL = 'Dodaj przychód'

    def draw(self):
        print(AddIncome.LABEL)


class ListIncomes(AbstractView):
    SHORTCUT = 'wp'
    LABEL = 'Wypisz przychody'

    def draw(self):
        print(ListIncomes.LABEL)


class MainMenu(AbstractView):
    OPTIONS = {
        AddCost.SHORTCUT: AddCost(),
        ListCosts.SHORTCUT: ListCosts(),
        AddIncome.SHORTCUT: AddIncome(),
        ListIncomes.SHORTCUT: ListIncomes()
    }

    def get_screen(self):
        option = None
        while option not in MainMenu.OPTIONS:
            option = input('Wybierz opcję: ')

        return MainMenu.OPTIONS[option]

    def draw(self):
        print('Powiedz co chcesz zrobić: ')
        for shortcut, screen in MainMenu.OPTIONS.items():
            print(f'[{shortcut}] - {screen.LABEL}')
