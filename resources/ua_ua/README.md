# Що знаходиться тут?

У цій теці знаходяться частково або повністю перекладені ресурси українською мовою. Ці файли будуть використані
для заміни англійською локалізації гри Civilization VII.

# Як допомогти?

Всі файли локалізації гри Civilization VII представляють собою xml-файли наступного формату:

```xml
<?xml version="1.0" encoding="utf-8"?>
<Database>
	<EnglishText>
		<!-- Controller mapping screen text -->
		<Row Tag="LOC_UI_CONTROLLER_MAPPING_TITLE">
			<Text>Controls</Text>
		</Row>
    </EnglishText>
</Database>
```

Важливо розуміти, що будь-які конфігураційні частини цих файлів, наприклад `Row`, `Tag="LOC_UI_CONTROLLER_MAPPING_TITLE"`,
`Text` тощо є важливими для коректної роботи гри. Будь ласка, вносьте зміни виключно у рядки тексту які знаходяться
у середині тегу `Text`. Також звертайте увагу на можливі вставки змінних, які виглядають як `{0}`, `{1}`, `{2}` тощо.
Ці змінні використовуються грою для динамічного виведення тексту, тому вони повинні залишатися на своїх місцях.