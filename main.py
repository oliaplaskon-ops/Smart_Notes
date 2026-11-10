from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
QLabel, QListWidget,
QLineEdit, QTextEdit, QHBoxLayout,
QVBoxLayout, QInputDialog, QMessageBox)
import json
import os

app = QApplication([])

if os.path.exists("notes_data.json"):
    with open("notes_data.json", "r", encoding="utf-8") as file:
        notes = json.load(file)
else:
    notes = {
        "Ласкаво просимо!": {
            "текст": "Це найкращий додаток для заміток у світі!",
            "теги": ["додаток", "інструкція"]
        },
        "Ще одна замітки": {
            "текст": "Ще одна крута замітки",
            "теги": ["додаток", "життя"]
        }
    }

with open("notes_data.json", "w", encoding="utf-8") as file:
    json.dump(notes, file, ensure_ascii=False, indent=2)

notes_win = QWidget()
notes_win.resize(900, 600)
notes_win.setWindowTitle("Розумні замітки")

list_notes = QListWidget()
list_tags = QListWidget()

list_notes_label = QLabel('Список заміток')
list_tags_label = QLabel('Список тегів')

button_note_create = QPushButton("Створити замітки")
button_note_del = QPushButton("Видалити замітки")
button_note_save = QPushButton("Зберегти замітки")

field_tag = QLineEdit()
field_tag.setPlaceholderText("Введіть тег...")

field_text = QTextEdit()

button_tag_add = QPushButton("Додати до замітки")
button_tag_del = QPushButton("Відкріпити від замітки")
button_tag_search = QPushButton("Шукати замітки по тегу")

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_2 = QVBoxLayout()
row_1 = QHBoxLayout()
row_2 = QHBoxLayout()
row_3 = QHBoxLayout()
row_4 = QHBoxLayout()

col_1.addWidget(field_text)

col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)
col_2.addLayout(row_1)

row_2.addWidget(button_note_save)
col_2.addLayout(row_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
row_3.addWidget(button_tag_add)
row_3.addWidget(button_tag_del)
col_2.addLayout(row_3)
row_4.addWidget(button_tag_search)
col_2.addLayout(row_4)

layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)

notes_win.setLayout(layout_notes)

def write_notes():
    with open("notes_data.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, ensure_ascii=False, indent=2)

def show_note():
    key = list_notes.selectedItems()[0].text()
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])

def button_add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Додати нову замітки", "Назва замітки:")
    if ok and note_name != "" and note_name not in notes:
        notes[note_name] = {"текст":"", "теги":[]}
        list_notes.addItem(note_name)
        write_notes()
    else:
        mes = QMessageBox()
        mes.setText("Жодна замітки не обрана")
        mes.exec_()

def button_del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        write_notes()
    else:
        mes = QMessageBox()
        mes.setText("Жодна замітки не обрана")
        mes.exec_()

def button_save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        write_notes()
        mes = QMessageBox()
        mes.setText("Вашу замітки збережено")
        mes.exec_()
    else:
        mes = QMessageBox()
        mes.setText("Жодна замітки не обрана")
        mes.exec_()

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if tag != "" and tag not in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            field_tag.clear()
            write_notes()
        else:
            mes = QMessageBox()
            mes.setText("Цей тег не підходить.\nВын пустий або також вже є.")
            mes.exec_()
    else:
        mes = QMessageBox()
        mes.setText("Жодна замітка не обрана")
        mes.exec_()

def del_tag():
    if list_notes.selectedItems() and list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        write_notes()
    else:
        mes = QMessageBox()
        mes.setText("Жодна замітка або тег не обрані")
        mes.exec_()

def search_tag():
    tag = field_tag.text()
    if button_tag_search.text() == "Шукати замітки за тегом":
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        mes = QMessageBox()
        mes.setText(f"Всього було знайдено {len(notes_filtered)} заміток")
        mes.exec_()
        button_tag_search.setText("Скинути пошук")
        list_notes.clear()
        list_notes.addItems(notes_filtered)
        list_tags.clear()
        field_text.clear()
    else:
        list_notes.clear()
        list_notes.addItems(notes)
        list_tags.clear()
        field_tag.clear()
        field_text.clear()
        button_tag_search.setText("Шукати замітки за тегом")

list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(button_add_note)
button_note_del.clicked.connect(button_del_note)
button_note_save.clicked.connect(button_save_note)

button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

list_notes.addItems(notes)

notes_win.show()
app.exec()
