import pandas as pd
import re


products_file = "data/Список товаров.xlsx"
supplier_file = "data/Данные поставщика.xlsx"
category_file = "data/Дерево категорий.xlsx"

products_df = pd.read_excel(products_file, usecols=[0, 1])
products_df.columns = ['Наименование', 'Тип товара']
supplier_df = pd.read_excel(supplier_file, usecols=[1])
supplier_df.columns = ['Название']
category_df = pd.read_excel(category_file, usecols=[0, 1, 2])
category_df.columns = ['Главная категория', 'Дочерняя категория', 'Тип товара']

products_df['Наименование'] = products_df['Наименование'].str.strip()
supplier_df['Название'] = supplier_df['Название'].str.strip()
category_df['Тип товара'] = category_df['Тип товара'].str.strip()
products_df['Наименование'] = products_df['Наименование'].apply(lambda x: re.sub(r',.*$', '', x))

results = []
for product in products_df['Наименование']:
    matches = supplier_df[supplier_df['Название'].str.contains(product, na=False, regex=False)]
    if not matches.empty:
        supplier_section = matches['Название'].values[0]
        category_matches = category_df[category_df['Тип товара'] == products_df.loc[products_df['Наименование'] == product, 'Тип товара'].values[0]]
        if not category_matches.empty:
            determined_category = category_matches['Главная категория'].values[0]
            determined_subcategory = category_matches['Дочерняя категория'].values[0]
        else:
            determined_subcategory = "Unknown"
            determined_category = "Unknown"
        results.append((product, supplier_section, determined_category, determined_subcategory))
    else:
        results.append((product, "Unknown", "Unknown", "Unknown"))

results_df = pd.DataFrame(results, columns=['Наименование', 'Название', 'Определенная категория', 'Определенная подкатегория'])
output_file = "Парс.xlsx"
results_df.to_excel(output_file, index=False)
print(f"Результаты сохранены в {output_file}")