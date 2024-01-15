## Loading libraries

# System
from argparse import ArgumentParser
import os
import sys
from utils import parse_args_feature_generation

# Data
import pandas as pd
import numpy as np

# scikit-learn
from sklearn.neighbors import LocalOutlierFactor
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA


# PCA

def function_pca(df, n_components):
    df_tags
    df_normalized=(df - df.mean()) / df.std()

    pca = PCA(n_components=n_components)
    pca_df = pd.DataFrame(pca.fit_transform(df.iloc[:,2:]))
    pca_df["sample_type"] = new_df["sample_type"]
    

    return PCA_df


# sns.scatterplot(PCA_df, x = 0, y = 1, hue = "sample_type")
# plt.xlabel("PC1")
# plt.ylabel("PC2")
# plt.show


# # Local Outlier Factor Trial

# In[23]:



np.random.seed(42)


# fit the model for outlier detection (default)
clf = LocalOutlierFactor(n_neighbors=5, contamination = 0.2)
# use fit_predict to compute the predicted labels of the training samples
# (when LOF is used for outlier detection, the estimator has no predict,
# decision_function and score_samples methods).
y_pred = clf.fit_predict(new_df.iloc[:,2:])
# n_errors = (y_pred != ground_truth).sum()
# X_scores = clf.negative_outlier_factor_

# plt.title("Local Outlier Factor (LOF)")
# plt.scatter(X[:, 0], X[:, 1], color="k", s=3.0, label="Data points")
# # plot circles with radius proportional to the outlier scores
# radius = (X_scores.max() - X_scores) / (X_scores.max() - X_scores.min())
# plt.scatter(
#     X[:, 0],
#     X[:, 1],
#     s=1000 * radius,
#     edgecolors="r",
#     facecolors="none",
#     label="Outlier scores",
# )
# plt.axis("tight")
# plt.xlim((-5, 5))
# plt.ylim((-5, 5))
# plt.xlabel("prediction errors: %d" % (n_errors))
# legend = plt.legend(loc="upper left")
# legend.legendHandles[0]._sizes = [10]
# legend.legendHandles[1]._sizes = [20]
# plt.show()


# In[24]:


lof_result = pd.concat([new_df, pd.DataFrame(y_pred)], axis = 1)


# In[25]:


lof_PCA = pd.concat([PCA_df, pd.DataFrame(y_pred, columns = ["outlier"])], axis = 1)
sns.scatterplot(PCA_df, x = 0, y = 1, hue = "sample_type")
plt.show()


# In[26]:


sns.scatterplot(lof_PCA, x = 0, y = 1, hue = "outlier")


# In[27]:


lof_PCA


# # Isolation Forest Trial

# In[28]:


clf = IsolationForest(n_estimators=100, warm_start=True)
clf.fit(new_df.iloc[:,2:])  # fit 10 trees  
clf.predict(new_df.iloc[:,2:])


# In[29]:


y_pred #lof

