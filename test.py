#!/usr/bin/env python3

import pytest

if __name__ == "__main__":
    # Запуск всех тестов из модуля substest
    pytest.main(["-v", "substest.py", "strfabrictest.py"])