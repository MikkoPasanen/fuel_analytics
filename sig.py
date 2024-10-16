"""
Ohjelma laskee
- Pearsonin korrelaatiokertoimen ja sig-arvon
  kahden scale-muuttujan valille ja
- Spearmanin jarjestyskorrelaatiokertoimen ja sig-arvon
  kahden ordinal-muuttujan valille.
"""

import scipy as sc
from scipy import stats as st

# Valitaan kaksi scale-muuttujaa
mins = [1.587, 1.678, 1.714, 1.142, 1.514, 1.529, 1.679, 0.99]
maxs = [2.259, 2.399, 2.029, 1.529, 2.16, 2.029, 2.109, 1.898]
# Pearsonin korrelaatiokerroin scale-muuttujille
pearson_info = st.pearsonr(mins, maxs)
p_corr_coeff = pearson_info[0]
p_sig = pearson_info[1]

print("Pearson correlation coefficient \nbetween scale variables: ", p_corr_coeff)
print("Pearson sig.: ", p_sig)

print("")

# # Spearmanin jarjestyskorrelaatiokerroin ordinal-muuttujille
mins = [1.587, 1.678, 1.714, 1.142, 1.514, 1.529, 1.679, 0.99]
maxs = [2.259, 2.399, 2.029, 1.529, 2.16, 2.029, 2.109, 1.898]

# Spearmanin jarjestyskorrelaatiokerroin ordinal-muuttujille
spearman_info = st.spearmanr(mins, maxs)
s_corr_coeff = spearman_info[0]
s_sig = spearman_info[1]

print("Spearman correlation coefficient \nbetween ordinal variables: ", s_corr_coeff)
print("Spearman sig.: ", s_sig)
