import pandas as pd

data = [
    {
        'class': 'Year 1',
        'student count': 20,
        'room': 'Yellow',
        'info': {
            'teachers': {'math': 'Rick Scott', 'physics': 'Elon Mask'}
        },
        'students': [
            {'name': 'Tom', 'sex': 'M', 'grades': {'math': 66, 'physics': 77}},
            {'name': 'James', 'sex': 'M', 'grades': {'math': 80, 'physics': 78}},
        ]
    },
    {
        'class': 'Year 2',
        'student count': 25,
        'room': 'Blue',
        'info': {
            'teachers': {'math': 'Alan Turing', 'physics': 'Albert Einstein'}
        },
        'students': [
            {'name': 'Tony', 'sex': 'M'},
            {'name': 'Jacqueline', 'sex': 'F'},
        ]
    },
]

df = pd.json_normalize(
    data,
    record_path=['students'],
    meta=['class', 'room', ['info', 'teachers', 'math']]
)

# print(df)
df.to_excel('../output/test.xlsx')
