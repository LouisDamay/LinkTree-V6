import pickle

# La structure de données.
# Voici une disposition par défaut que vous êtes libre de modifier à votre guise.
all_labels = [
    [
        # Vous pouvez mettre plusieurs liens.
        {'1': ['https://drive.mathworks.com/files/','https://google.com/']},
        {'2': ['https://google.com/']},
        {'3': ['https://google.com/']},
        {'4': ['https://google.com/']},
        {'5': ['https://google.com/']},
        {'6': ['https://google.com/']},
        {'7': ['https://google.com/']},
        {'8': ['https://google.com/']},
        {'9': ['https://google.com/']},
        {'A': ['https://google.com/']},
        {'B': ['https://google.com/']},
        {'C': ['https://google.com/']},
    ],
]


with open('../assets/all_labels.bin', 'wb') as file:
    pickle.dump(all_labels, file)
