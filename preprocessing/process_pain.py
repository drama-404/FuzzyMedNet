import numpy as np
import re


def pain_score_conversion(score):
    if score is np.nan:
        return np.nan
    if 'unable' in score:
        return np.nan

    num = re.findall(r'\d+', score)
    if num:
        return int(num[0])

    score = score.lower()
    if 'none' in score and 'mild' not in score:
        return 0
    if 'none' in score and 'mild' in score:
        return 1
    if 'mild' in score and 'mod' not in score:
        return 2
    if 'mild' in score and 'mod' in score:
        return 3
    if 'mod' in score and 'severe' not in score:
        return 5
    if 'mod' in score and 'severe' in score:
        return 6
    if 'severe' in score and 'worst' not in score:
        return 8
    if 'severe' in score and 'worst' in score:
        return 9
    if 'worst' in score:
        return 10
    else:
        return np.nan

# Apply the function to the pain_score column
# df['pain_score'] = df['pain_score'].apply(pain_score_conversion)
