from abc import ABC, abstractmethod

# 1. Спільний інтерфейс Document[cite: 6]
class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

# 2. Конкретні класи документів зі своїми форматами[cite: 6]
class Report(Document):
    def render(self) -> str:
        return "Звіт: [Дані про прибутки та витрати]"

class Invoice(Document):
    def render(self) -> str:
        return "Рахунок: [Сума до оплати: 10 000 грн]"

class Contract(Document):
    def render(self) -> str:
        return "Контракт: [Умови співпраці підтверджено]"

# Патерн Null Object для обробки невідомих типів без винятків[cite: 6]
class NullDocument(Document):
    def render(self) -> str:
        return "Помилка: Невідомий тип документа."

# 3. Фабрика зі статичним методом[cite: 6]
class DocumentFactory:
    # Словник для мапінгу типів на класи (повністю замінює if/elif)
    _doc_map = {
        'report': Report,
        'invoice': Invoice,
        'contract': Contract
    }

    @staticmethod
    def create(doc_type: str) -> Document:
        # Метод get() шукає ключ. Якщо не знаходить — повертає NullDocument
        doc_class = DocumentFactory._doc_map.get(doc_type, NullDocument)
        return doc_class()

# 4. Клієнтський код (жодних if/elif поза фабрикою)[cite: 6]
if __name__ == "__main__":
    # Вхідні дані: просто рядки з типами
    incoming_docs = ['report', 'contract', 'invoice', 'random_text']

    print("--- Обробка документів ---")
    for doc_type in incoming_docs:
        # Тільки рядок doc_type і виклик фабрики[cite: 6]
        document = DocumentFactory.create(doc_type)
        print(f"[{doc_type}] -> {document.render()}")