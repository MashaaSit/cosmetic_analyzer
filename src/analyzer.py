import pandas as pd

ingredients_classification = pd.read_csv('ingredients_classification.csv', sep=',', skipinitialspace=True)


weight_values = {('allergen', 1): 4, ('comedogenic', 1): 4,
                 ('comedogenic', 0): 3, ('keratolytic', 1): 2,
                 ('sebo_regulating', 1): 2,('anti_inflammatory', 1): 2,
                 ('keratolytic', 0): -2,('sebo_regulating', 0): -2,
                 ('anti_inflammatory', 0): -2, ('neutral', 1): 1,
                 ('neutral', 0): 0}

def place_in_composition(ingredient, composition):
    place = composition.index(ingredient)/len(composition)
    if place < 0.2:
        return 0.8
    elif place >= 0.2 and place < 0.8:
        return 0.15
    else:
        return 0.05
    
unknown_count = 0
known_count = 0
def find_ingredient_info(ingredient):
    global unknown_count
    row = ingredients_classification[ingredient == ingredients_classification['ingredient_name']]
    if len(row) == 0:
        unknown_count += 1
        return ('neutral', 0)
    global known_count
    known_count+=1
    return (row['acne_effect'].values[0], int(row['allergen'].values[0]))
    
def calculate_risk(ingredients_list):
    score = 0

    for ingredient in ingredients_list:
        ingredient_info = find_ingredient_info(ingredient)

        score += weight_values[ingredient_info] * place_in_composition(ingredient, ingredients_list)

    score /= len(ingredients_list)

    return round(score, 4)

df1 = pd.read_csv('1-200.csv')
df2 = pd.read_csv('201-400.csv')
df3 = pd.read_csv('401-600.csv')
df = pd.concat([df1, df2, df3], axis=0)
res = []
for index, row in df.iterrows():
    res.append(calculate_risk(list(row['ingredients'].split(', '))))
print(sorted(res)[:10])   # минимальные
print(sorted(res)[-10:])  # максимальные
df['risk_score'] = res
df['risk_level'] = pd.cut(df['risk_score'], 
                           bins=[-float('inf'), 0, 0.5, float('inf')],
                           labels=['low', 'medium', 'high'])
print(df['risk_level'].value_counts())
df.to_csv('cosmetic_products.csv')

print(unknown_count)
print(known_count)
total = sum(len(row['ingredients'].split(', ')) for _, row in df.iterrows())
print(f'Покрытие базы: {(total - unknown_count) / total:.1%}')