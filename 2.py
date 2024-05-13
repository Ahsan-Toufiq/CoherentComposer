import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotext as plt

df = pd.read_csv('/home/hassan/CoherentComposer/clean_dataset.csv')


column_counts = df.count()

# Plotting
plt.figure(figsize=(10, 6)) 
plt.bar(column_counts.index, column_counts.values, color='blue') 
plt.xlabel('Columns')
plt.ylabel('Total Records in each Column')
plt.title('Total Records per Column in CSV')
plt.xticks(rotation=45)
plt.tight_layout() 
plt.show()

for column in df.columns:
    df[column + '_wc'] = df[column].apply(lambda x: len(str(x).split()))

# Bar Chart of Total Records in Each Column
plt.figure(figsize=(10, 6))
column_wc = [df[col].count() for col in df.columns]
plt.bar(df.columns, column_wc, color='skyblue')
plt.xlabel('Columns')
plt.ylabel('Number of Records')
plt.title('Total Records in Each Column')
plt.xticks(rotation=45)
plt.show()

# Boxplot for each numeric interpretation (if applicable)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df.select_dtypes(include=['int', 'float']))  # Modify this line if your data contains interpretable numeric columns
plt.title('Distribution of Numeric Data')
plt.ylabel('Value')
plt.xticks(rotation=45)
plt.show()

# Additional Visualizations
# Histogram of word counts if the data is textual
plt.figure(figsize=(10, 6))
sns.histplot(df['atmosphere_wc'], color='purple', kde=True)
plt.title('Word Count Distribution for Atmosphere Descriptions')
plt.xlabel('Word Count')
plt.show()

# Heatmap of correlation matrix (if there are multiple numeric summaries)
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix of Data')
plt.show()