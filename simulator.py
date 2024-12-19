#!/usr/bin/env python
# coding: utf-8

# In[5]:


import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Otsikko
st.title("Päiväkotipaikkojen simulointi")

# Lapsien ja päiväkotien tietojen määrittely
children = pd.DataFrame({
    "child_id": range(1, 11),
    "x": np.random.uniform(0, 10, 10),
    "y": np.random.uniform(0, 10, 10)
})

daycares = pd.DataFrame({
    "daycare_id": range(1, 4),
    "x": [2, 8, 5],
    "y": [3, 7, 1],
    "capacity": [4, 3, 3]
})

# Lasketaan etäisyys lapsen ja päiväkodin välillä
def calculate_distance(child, daycare):
    return np.sqrt((child['x'] - daycare['x'])**2 + (child['y'] - daycare['y'])**2)

# Monte Carlo -simulaatio
def monte_carlo_allocation(children, daycares, iterations=1000):
    best_allocation = None
    best_total_distance = float('inf')

    for _ in range(iterations):
        allocation = {daycare_id: [] for daycare_id in daycares.index}
        remaining_capacity = daycares['capacity'].to_dict()
        total_distance = 0

        shuffled_children = children.sample(frac=1).reset_index(drop=True)

        for _, child in shuffled_children.iterrows():
            distances = daycares.apply(lambda dc: calculate_distance(child, dc), axis=1)
            sorted_daycares = distances.sort_values().index

            for daycare_id in sorted_daycares:
                if remaining_capacity[daycare_id] > 0:
                    allocation[daycare_id].append(child['child_id'])
                    remaining_capacity[daycare_id] -= 1
                    total_distance += distances[daycare_id]
                    break

        if total_distance < best_total_distance:
            best_total_distance = total_distance
            best_allocation = allocation

    return best_allocation, best_total_distance

# Päiväkodit on hyvä asettaa ennen simulaatiota
daycares.set_index('daycare_id', inplace=True)

# Simulaation suoritus
best_allocation, best_total_distance = monte_carlo_allocation(children, daycares)

# Tulostetaan tulokset Streamlitissä
st.subheader("Paras sijoitus:")
for daycare_id, assigned_children in best_allocation.items():
    st.write(f"Päiväkoti {daycare_id}: {assigned_children}")
st.write(f"Yhteensä kuljettu etäisyys: {best_total_distance:.2f}")

# Visualisointi
fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(children['x'], children['y'], color='blue', label='Lapset', s=100)
ax.scatter(daycares['x'], daycares['y'], color='red', marker='s', label='Päiväkodit', s=200)
for _, row in children.iterrows():
    ax.text(row['x'], row['y'], f"C{row['child_id']}", fontsize=12)
for i, row in daycares.iterrows():
    ax.text(row['x'], row['y'], f"D{row.name}", fontsize=14, color='red')
ax.legend()
ax.set_title('Lasten ja päiväkotien sijainnit', fontsize=16)
ax.set_xlabel('x', fontsize=14)
ax.set_ylabel('y', fontsize=14)
ax.grid(True)
st.pyplot(fig)


# In[ ]:




