import os

import matplotlib.pyplot as plt
import pandas as pd
import shap


os.makedirs("src/explainability/plots", exist_ok=True)


class SHAPAnalyzer:

    def __init__(self, model, X):

        self.model = model
        self.X = X

    # --------------------------------------------------
    # Helper
    # --------------------------------------------------

    def _save_plot(self, filename):

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                "src/explainability/plots",
                filename,
            )
        )

        plt.close()

    # --------------------------------------------------
    # Create Explainers
    # --------------------------------------------------

    def _create_explainers(self):

        if hasattr(self.model, "estimators_"):

            return [

                shap.TreeExplainer(estimator)

                for estimator in self.model.estimators_

            ]

        model_name = type(self.model).__name__.lower()

        if "xgb" in model_name or "forest" in model_name:

            return [shap.TreeExplainer(self.model)]

        if "ridge" in model_name or "linear" in model_name:

            return [shap.LinearExplainer(self.model, self.X)]

        raise ValueError(
            f"SHAP not implemented for {type(self.model)}"
        )

    # --------------------------------------------------
    # Global Feature Importance
    # --------------------------------------------------

    def feature_importance(self):

        explainers = self._create_explainers()

        total_importance = None

        for explainer in explainers:

            shap_values = explainer.shap_values(self.X)

            importance = abs(shap_values).mean(axis=0)

            if total_importance is None:

                total_importance = importance

            else:

                total_importance += importance

        total_importance /= len(explainers)

        importance_df = pd.DataFrame(
            {
                "feature": self.X.columns,
                "importance": total_importance,
            }
        ).sort_values(
            "importance",
            ascending=False,
        )

        plt.figure(figsize=(10, 8))

        plt.barh(
            importance_df["feature"],
            importance_df["importance"],
        )

        plt.gca().invert_yaxis()

        plt.xlabel("Mean |SHAP Value|")

        plt.title("Global SHAP Feature Importance")

        self._save_plot(
            "shap_feature_importance.png"
        )

        print("\nTop Features\n")

        print(importance_df.head(20))

        return importance_df

    # --------------------------------------------------
    # SHAP Summary Plot
    # --------------------------------------------------

    def summary_plot(self):

        explainers = self._create_explainers()

        if len(explainers) == 1:

            shap_values = explainers[0].shap_values(
                self.X
            )

        else:

            all_values = []

            for explainer in explainers:

                all_values.append(
                    explainer.shap_values(self.X)
                )

            shap_values = sum(all_values) / len(all_values)

        plt.figure(figsize=(10, 8))

        shap.summary_plot(
            shap_values,
            self.X,
            show=False,
        )

        self._save_plot(
            "shap_summary.png"
        )