from collections import UserList
from pathlib import Path
import pickle

# TODO: add help string

save_file = Path("notes.bin")


class Notes:
    def __init__(self, title, description, tag):
        self.title = title
        self.description = description
        self.tag = tag


class Notebook(UserList):
    def __init__(self):
        self.notes = []


class NoteBook(UserList):
    def __init__(self):
        super().__init__()
        self.load_notes()

    def load_notes(self):
        try:
            with open(save_file, "rb") as file:
                self.data = pickle.load(file)
                print("Заметки успешно загружены.")
        except FileNotFoundError:
            print("Файл заметок не найден. Создан новый блокнот.")
        except Exception as e:
            print(f"Ошибка при загрузке заметок: {e}")

    def save_notes(self):
        with open(save_file, "wb") as file:
            pickle.dump(self.data, file)
            print("Заметки успешно сохранены.")

    def note_main(self):
        while True:
            self.display_menu()
            choice = input("Введите номер действия (help для справки): ")

            if choice == "1":
                self.add_note_from_user()
            elif choice == "2":
                self.display_all_notes()
            elif choice == "3":
                self.sort_notes_by_tags()
                print("Записи отсортированы по тегам.")
            elif choice == "4":
                search_text = input("Введите текст для поиска: ")
                self.find_notes(search_text)
            elif choice == "5":
                note_index = int(input("Введите индекс записи для изменения: "))
                new_text = input("Введите новый текст: ")
                self.change_note(note_index, new_text)
            elif choice == "6":
                note_index = int(input("Введите индекс записи для удаления: "))
                self.delete_note(note_index)
            elif choice == "help":
                self.help()
            elif choice == "0":
                self.save_notes()
                print("Выход из блокнота.")
                break
            else:
                print("Некорректный ввод. Пожалуйста, выберите действие из меню.")

    def display_menu(self):
        print("\n===== Меню блокнота =====")
        print("1. Добавить запись")
        print("2. Вывести все записи")
        print("3. Сортировать записи по тегам")
        print("4. Найти записи по тексту")
        print("5. Изменить запись")
        print("6. Удалить запись")
        print("0. Выйти из блокнота")
        print("=========================\n")

    def add_note_from_user(self):
        input_text = input("Введите текст записи: ")
        self.add_note(input_text)

    def add_note(self, text):
        tags = self.extract_tags(text)
        self.data.append({"text": text, "tags": tags})
        print("Запись добавлена в блокнот.")

    def display_all_notes(self):
        print("\n===== Все записи в блокноте =====")
        for index, note in enumerate(self.data):
            print(f"Индекс: {index}, Текст: {note['text']}, Теги: {note['tags']}")
        print("==============================\n")

    # def run_notebook(self):
    #     while True:
    #         self.display_menu()
    #         choice = input("Введите номер действия (help для справки): ")

    #         if choice == "1":
    #             self.add_note_from_user()
    #         elif choice == "2":
    #             self.display_all_notes()
    #         elif choice == "3":
    #             self.sort_notes_by_tags()
    #             print("Записи отсортированы по тегам.")
    #         elif choice == "4":
    #             search_text = input("Введите текст для поиска: ")
    #             self.find_notes(search_text)
    #         elif choice == "5":
    #             note_index = int(input("Введите индекс записи для изменения: "))
    #             new_text = input("Введите новый текст: ")
    #             self.change_note(note_index, new_text)
    #         elif choice == "6":
    #             note_index = int(input("Введите индекс записи для удаления: "))
    #             self.delete_note(note_index)
    #         elif choice == "help":
    #             self.help()
    #         elif choice == "0":
    #             print("Выход из блокнота.")
    #             break
    #         else:
    #             print("Некорректный ввод. Пожалуйста, выберите действие из меню.")

    def extract_tags(self, text: str):
        tags = [word[1:] for word in text.split() if word.startswith("#")]
        return tags

    def search_notes(self, search_text: str):
        matching_notes = []
        for index, note in enumerate(self.data):
            if search_text.lower() in note["text"].lower():
                matching_notes.append((index, note))

        if matching_notes:
            print("Найденные записи:")
            for index, note in matching_notes:
                print(f"Индекс: {index}, Текст: {note['text']}, Теги: {note['tags']}")
        else:
            print("Нет записей, соответствующих поисковому запросу.")

    def sort_notes_by_tags(self):
        self.data.sort(key=lambda note: len(note["tags"]))

    # @staticmethod
    # def add_note_from_user():
    #     notebook = NoteBook()
    #     input_text = input("Введите текст записи: ")
    #     notebook.add_note(input_text)

    def change_note(self, note_index, new_text):
        if 0 <= note_index < len(self.data):
            tags = self.extract_tags(new_text)
            self.data[note_index] = {"text": new_text, "tags": tags}
            print(f"Запись с индексом {note_index} изменена в блокноте.")
        else:
            print("Указанный индекс записи не существует.")

    def delete_note(self, note_index):
        if 0 <= note_index < len(self.data):
            del self.data[note_index]
            print(f"Запись с индексом {note_index} удалена из блокнота.")
        else:
            print("Указанный индекс записи не существует.")


notebook = NoteBook()


def add(text: list):
    notebook.add_note(" ".join(text))


def show(_: list):
    notebook.display_all_notes()


def sort(_: list):
    notebook.sort_notes_by_tags()
    print("Records sorted")


def find(text: list):
    notebook.search_notes(" ".join(text))


def change(text: list):
    notebook.change_note(int(text[0]), " ".join(text[1:]))


def delete(text: list):
    notebook.delete_note(int(text[0]))


def help(_: list = None):
    print("\n===== Notebook command`s help =====")
    print("add <any string>       - add new record to notebook")
    print("show                   - show all records")
    print("sort                   - sort records by tags")
    print("find <text>            - find records by part")
    print("change <number> <text> - changing a record by its number")
    print("delete <number>        - removing a record by its number")
    print("help                   - notebook commands list")
    print("exit                   - leave notebook")
    print("==============================\n")


# def get_user_input(prompt):
#     return input(prompt)
COMMANDS = {
    "add": add,
    "show": show,
    "sort": sort,
    "find": find,
    "change": change,
    "delete": delete,
    "help": help,
}


def parser(text: str):
    text = text.strip().split()
    if text[0] in COMMANDS:
        COMMANDS[text[0]](text[1:])
    else:
        print("Wrong command. Please try again.")


def note_main():
    help()

    while True:
        # menu = """
        # Menu:
        # 1. Add Note
        # 2. Search note
        # 3. Edit note
        # 4. Delete Note
        # 5. Sort Notes by tag
        # 6. Exit
        # """

        # print(menu)

        choice = input("Enter your command >>> ")
        if choice == "exit":
            notebook.save_notes()
            break
        parser(choice)

        # if choice == "1":
        #     title = input("Please enter title name: ")
        #     description = input("Please enter description: ")
        #     tag = input("Please enter tag: ")
        #     notebook.add_note(title, description, tag)
        #     print("Note has been added successfully!")

        # elif choice == "2":
        #     keyword = input("Enter key word for search: ")
        #     found_notes = notebook.search_notes(keyword)
        #     if found_notes:
        #         print("Search results:")
        #         for note in found_notes:
        #             print(
        #                 f"Title: {note.title}\nDescription: {note.description}\nTag: {note.tag}\n=========="
        #             )
        #     else:
        #         print("Note is not found.")

        # elif choice == "3":
        #     note_index = int(input("Please enter note number you want to edit: "))
        #     new_title = input("Enter a new title: ")
        #     new_description = input("Enter a new description: ")
        #     new_tag = input("Enter a new tag: ")
        #     notebook.edit_note(note_index, new_title, new_description, new_tag)
        #     print("Note has been edited successfully!")

        # elif choice == "4":
        #     note_index = int(input("Please enter note number you want to be removed: "))
        #     notebook.delete_note(note_index)
        #     print("Note has been removed successfully")

        # elif choice == "5":
        #     sorted_notes = notebook.sort_notes_by_tag()
        #     if sorted_notes:
        #         print("Sorted notes:")
        #         for note in sorted_notes:
        #             print(
        #                 f"Title: {note.title}\nDescription: {note.description}\nTag: {note.tag}\n=========="
        #             )
        #     else:
        #         print("No notes found.")

        # elif choice == "6":
        #     break

        # else:
        #     print("Wrong choice. Please try again.")


if __name__ == "__main__":
    note_main()
    # Пример использования

    # notebook = NoteBook()
    # # notebook.note_main()

    # # Пример добавления записей с тегами
    # input_text_1 = "Сегодня я поучаствовал в #программирование. Было интересно!"
    # input_text_2 = "Завтра планирую заняться #программирование и #учеба."

    # notebook.add_note(input_text_1)
    # notebook.add_note(input_text_2)

    # # Вывод записей до сортировки
    # print("Записи до сортировки:")
    # for note in notebook.data:
    #     print(f"Текст: {note['text']}, Теги: {note['tags']}")

    # # Сортировка записей по количеству тегов
    # notebook.sort_notes_by_tags()

    # # Вывод записей после сортировки
    # print("\nЗаписи после сортировки:")
    # for note in notebook.data:
    #     print(f"Текст: {note['text']}, Теги: {note['tags']}")

    # # Использование блокнота с интерфейсом
    # # notebook.run_notebook()

    # # Пример добавления записи через пользовательский ввод
    # notebook.add_note_from_user()
    # # Пример добавления записи с тегами
    # input_text = "Сегодня я поучаствовал в #программирование. Было интересно!"
    # notebook.add_note(input_text)
    # print(notebook)
    # # Пример добавления записи через пользовательский ввод
    # notebook.add_note_from_user()
    # print(notebook)
    # notebook.add_note_from_user()
    # notebook.add_note_from_user()
    # print(notebook)
    # input()
