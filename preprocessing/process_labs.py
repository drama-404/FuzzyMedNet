import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

lab_categories = {
    'Kidney Function': ['bun', 'creatinine'],
    'Liver Function': ['bilirubin', 'albumin'],
    # 'Metabolic Function': ['lactate'],
    'Electrolyte Levels': ['sodium', 'potassium', 'chloride', 'bicarbonate'],  # removed anion gab
    'Blood Clotting': ['pt', 'ptt', 'inr'],
    'Red Blood Cells': ['hematocrit', 'hemoglobin'],
    'White Blood Cells': ['wbc', 'bands'],
    'Platelets': ['platelet'],
    'Blood Sugar': ['glucose']
}


def category_index(category):
    keys_list = list(lab_categories.keys())
    index = keys_list.index(category)

    return index


def define_lab_category(label):
    for category, labs in lab_categories.items():
        if label in labs:
            return category
    return np.nan


def visualize_category(df, category):
    df_filtered = df[df['category'] == category]
    lab_tests = lab_categories[category]

    nrows = int(np.ceil(len(lab_tests) / 2))
    ncols = 2 if len(lab_tests) > 1 else 1

    fig, axes = plt.subplots(nrows, ncols, figsize=(10, 6 * nrows))
    axes = axes.flatten()
    fig.suptitle(f'Lab Results for {category} on First Day of Admission')

    for i, lab_test in enumerate(lab_tests):
        df_lab_test = df_filtered[df_filtered['label'] == lab_test]
        # data = [df_lab_test['min_value'], df_lab_test['max_value']]

        df_melted = df_lab_test.melt(id_vars=['subject_id', 'hadm_id', 'icustay_id', 'label', 'hospital_expire_flag'],
                                     value_vars=['min_value', 'max_value'],
                                     var_name='type', value_name='value')

        # axes[i].boxplot(data, labels=['Min', 'Max'])
        # axes[i].set_title(f'{lab_test} Values')

        sns.boxplot(data=df_melted, x='type', y='value', hue='hospital_expire_flag', ax=axes[i])
        axes[i].set_title(lab_test)

    if len(axes) > len(lab_tests):
        for j in range(len(lab_tests), len(axes)):
            fig.delaxes(axes[j])

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(f'../data_viz_img/lab_results/{category_index(category)}_{category}.png')
    plt.show()
