from abc import ABC, abstractmethod

# 1. Спільний інтерфейс Document
class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

# 2. Звичайні (чесні) документи
class NormalReport(Document):
    def render(self) -> str:
        return "Звичайний звіт: показники в нормі."

class NormalInvoice(Document):
    def render(self) -> str:
        return "Звичайний рахунок: стандартна сума до оплати."

class NormalContract(Document):
    def render(self) -> str:
        return "Звичайний контракт: прозорі умови співпраці."

# 3. Тіньові документи (із прихованими полями)
class ShadowReport(Document):
    def render(self) -> str:
        return "Тіньовий звіт: приховані 'сірі' витрати включено."

class ShadowInvoice(Document):
    def render(self) -> str:
        return "Тіньовий рахунок: +20% маржі на 'спеціальні' послуги."

class ShadowContract(Document):
    def render(self) -> str:
        return "Тіньовий контракт: додано непомітні службові поля для відкатів."

# 4. Базова фабрика з перевіркою безпеки
class DocumentFactory(ABC):
    # Білий список дозволених документів
    ALLOWED_TYPES = ["report", "invoice", "contract"]

    def create(self, doc_type: str) -> Document:
        # Перевірка безпеки
        if doc_type not in self.ALLOWED_TYPES:
            raise ValueError(f"Доступ заборонено! Тип документа '{doc_type}' не у білому списку.")
        
        return self._create_doc(doc_type)

    @abstractmethod
    def _create_doc(self, doc_type: str) -> Document:
        pass

# 5. Реалізація конкретних фабрик
class CorpDocumentFactory(DocumentFactory):
    def _create_doc(self, doc_type: str) -> Document:
        if doc_type == "report": return NormalReport()
        elif doc_type == "invoice": return NormalInvoice()
        elif doc_type == "contract": return NormalContract()

class ShadowDocumentFactory(DocumentFactory):
    def _create_doc(self, doc_type: str) -> Document:
        if doc_type == "report": return ShadowReport()
        elif doc_type == "invoice": return ShadowInvoice()
        elif doc_type == "contract": return ShadowContract()

# 6. Конфіг-перемикач для клієнтського коду
def get_factory(mode: str) -> DocumentFactory:
    if mode == 'corp':
        return CorpDocumentFactory()
    elif mode == 'shadow':
        return ShadowDocumentFactory()
    else:
        raise ValueError("Невідомий режим роботи!")

# Клієнтський код (не знає про конкретні класи)
def run_system(mode: str, docs_to_create: list):
    print(f"\n=== Запуск системи. Режим: '{mode}' ===")
    try:
        factory = get_factory(mode)
        for doc_type in docs_to_create:
            try:
                doc = factory.create(doc_type)
                print(f"[{doc_type}] -> {doc.render()}")
            except ValueError as e:
                print(f"[{doc_type}] -> ПОМИЛКА: {e}")
    except Exception as e:
         print(f"Помилка конфігурації: {e}")

if __name__ == "__main__":
    # Список для тестування (останній елемент не в білому списку)
    test_docs = ["report", "invoice", "contract", "secret_scheme"]

    # Демонстрація 1: чесний режим ('corp')
    run_system('corp', test_docs)

    # Демонстрація 2: тіньовий режим ('shadow')
    run_system('shadow', test_docs)