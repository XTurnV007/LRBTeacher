import pandas as pd
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Creating a DataFrame for the given data
data = {
    'Group': ['Simulation Method', 'Simulation Method', 'Simulation Method',
              'Interactive Method', 'Interactive Method', 'Interactive Method',
              'Practice Method', 'Practice Method', 'Practice Method',
              'Knowledge Summary Method', 'Knowledge Summary Method', 'Knowledge Summary Method',
              'Evaluation Method', 'Evaluation Method', 'Evaluation Method',
              'GPT Method', 'GPT Method', 'GPT Method'],
    'Before': [64.33, 69.33, 59.00, 
               65.67, 73.00, 66.00, 
               65.00, 61.67, 65.67, 
               64.00, 53.33, 72.33, 
               65.33, 77.33, 64.67, 
               72.00, 50.33, 67.00],
    'After': [72.00, 72.00, 65.33, 
              73.00, 77.67, 76.00, 
              70.67, 64.33, 72.33, 
              65.33, 67.00, 69.33, 
              75.33, 77.33, 78.33, 
              72.67, 63.00, 78.33]
}

df = pd.DataFrame(data)

# Performing ANOVA for 'Before' scores
anova_before = f_oneway(
    df[df['Group'] == 'Simulation Method']['Before'],
    df[df['Group'] == 'Interactive Method']['Before'],
    df[df['Group'] == 'Practice Method']['Before'],
    df[df['Group'] == 'Knowledge Summary Method']['Before'],
    df[df['Group'] == 'Evaluation Method']['Before'],
    df[df['Group'] == 'GPT Method']['Before']
)

# Performing ANOVA for 'After' scores
anova_after = f_oneway(
    df[df['Group'] == 'Simulation Method']['After'],
    df[df['Group'] == 'Interactive Method']['After'],
    df[df['Group'] == 'Practice Method']['After'],
    df[df['Group'] == 'Knowledge Summary Method']['After'],
    df[df['Group'] == 'Evaluation Method']['After'],
    df[df['Group'] == 'GPT Method']['After']
)

# Performing Tukey's HSD test for 'After' scores
tukey_after = pairwise_tukeyhsd(endog=df['After'], groups=df['Group'], alpha=0.05)

anova_results_before = {
    'F-value': anova_before.statistic,
    'p-value': anova_before.pvalue
}

anova_results_after = {
    'F-value': anova_after.statistic,
    'p-value': anova_after.pvalue
}

import ace_tools as tools; tools.display_dataframe_to_user(name="Tukey HSD Test Results", dataframe=pd.DataFrame(data))

anova_results_before, anova_results_after, tukey_after.summary()
