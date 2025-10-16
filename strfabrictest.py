import pytest

try:
    from strategy import Worker, AllInput, ScreenInput, OnlyErrInput, FileInput, TestStrat
except ImportError:
    # Заглушки для тестирования
    class Worker:
        def run(self): pass
        def create(self): pass
        def name(self): pass

    class AllInput(Worker):
        def name(self): return "all"
        def run(self): pass
        def create(self): return AllInput()

    class ScreenInput(Worker):
        def name(self): return "screen"
        def run(self): pass
        def create(self): return ScreenInput()

    class OnlyErrInput(Worker):
        def name(self): return "err"
        def run(self): pass
        def create(self): return OnlyErrInput()

    class FileInput(Worker):
        def name(self): return "file"
        def run(self): pass
        def create(self): return FileInput()

    class TestStrat(Worker):
        def name(self): return "TestStrat"
        def run(self): pass
        def create(self): return TestStrat()


from strfabric import StrFabric


def test_strfabric_initialization():
    """Проверка инициализации фабрики с предустановленными функциями"""
    fabric = StrFabric()
    assert fabric.availableFunctionsCount() == 4
    expected_names = {'AllInput', 'ScreenInput', 'OnlyErrInput', 'FileInput'}
    assert set(fabric.availableFunctionsNames()) == expected_names


def test_strfabric_register_function_valid():
    """Проверка регистрации валидной функции"""
    fabric = StrFabric()
    func = TestStrat()  # Используем существующий класс как тестовую стратегию
    fabric.registerFuncton(func)
    assert fabric.getFunction("TestStrat") is not None
    assert fabric.availableFunctionsCount() == 5

    # Восстановим оригинальное поведение, если меняли
    if 'original_name' in locals():
        func.name = original_name


def test_strfabric_get_function():
    """Проверка получения экземпляра через create()"""
    fabric = StrFabric()
    instance = fabric.getFunction("AllInput")
    assert instance is not None
    assert isinstance(instance, AllInput)


def test_strfabric_get_function_not_exists():
    """Проверка возврата None при отсутствующем ключе"""
    fabric = StrFabric()
    assert fabric.getFunction("nonexistent") is None


def test_strfabric_available_functions_names():
    """Проверка получения списка имен функций"""
    fabric = StrFabric()
    names = fabric.availableFunctionsNames()
    assert isinstance(names, type(dict().keys()))
    expected = {'AllInput', 'ScreenInput', 'OnlyErrInput', 'FileInput'}
    assert set(names) == expected


def test_strfabric_register_function_missing_name():
    """Проверка ошибки при отсутствии метода name()"""
    fabric = StrFabric()

    class InvalidFunc:
        def run(self): pass
        def create(self): pass

    with pytest.raises(ValueError, match="This function is not contains method name!"):
        fabric.registerFuncton(InvalidFunc())


def test_strfabric_register_function_name_not_string():
    """Проверка ошибки, если name() возвращает не строку"""
    fabric = StrFabric()

    class InvalidFunc:
        def name(self): return 123
        def run(self): pass
        def create(self): pass

    with pytest.raises(ValueError, match="Method key not returned string!"):
        fabric.registerFuncton(InvalidFunc())


def test_strfabric_register_function_missing_run():
    """Проверка ошибки при отсутствии метода run()"""
    fabric = StrFabric()

    class InvalidFunc:
        def name(self): return "test"
        def create(self): pass

    with pytest.raises(ValueError, match="This function is not contains method run!"):
        fabric.registerFuncton(InvalidFunc())


def test_strfabric_register_function_missing_create():
    """Проверка ошибки при отсутствии метода create()"""
    fabric = StrFabric()

    class InvalidFunc:
        def name(self): return "test"
        def run(self): pass

    with pytest.raises(ValueError, match="This function is not contains method create!"):
        fabric.registerFuncton(InvalidFunc())