class TestShortPhrase:
    def test_short_phrase(self):
        max_len = 15
        phrase = input("Введите фразу короче 15 символов: ")
        len_phr = len(phrase)
        assert len_phr <= max_len, f"Длина введенной фразы '{phrase}' более {max_len} символов"

# python -m pytest -s test_shortphrase.py -k "test_short_phrase"
