import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

class PlacementPreprocessor:
    def __init__(self):
        self.dept_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def fit(self, df):
        # We assume df has 'department' and numeric columns
        if 'department' in df.columns:
            self.dept_encoder.fit(df['department'].astype(str))
            
        numeric_cols = ['cgpa', 'backlog_count', 'communication_score', 
                        'aptitude_score', 'internships', 'projects']
        
        # Fit scaler on available numeric columns
        cols_to_scale = [c for c in numeric_cols if c in df.columns]
        if cols_to_scale:
            self.scaler.fit(df[cols_to_scale])
            
        self.is_fitted = True
        return self
        
    def transform(self, df):
        if not self.is_fitted:
            raise ValueError("Preprocessor is not fitted yet.")
            
        df_out = df.copy()
        
        if 'department' in df_out.columns:
            # Handle unseen labels gracefully by mapping to a default if necessary
            # or just transforming known ones (for simplicity, we assume known during training)
            known_classes = self.dept_encoder.classes_
            df_out['department'] = df_out['department'].apply(
                lambda x: x if x in known_classes else known_classes[0] if len(known_classes) > 0 else 'Unknown'
            )
            df_out['department'] = self.dept_encoder.transform(df_out['department'].astype(str))
            
        numeric_cols = ['cgpa', 'backlog_count', 'communication_score', 
                        'aptitude_score', 'internships', 'projects']
        cols_to_scale = [c for c in numeric_cols if c in df_out.columns]
        
        if cols_to_scale:
            df_out[cols_to_scale] = self.scaler.transform(df_out[cols_to_scale])
            
        return df_out
        
    def fit_transform(self, df):
        return self.fit(df).transform(df)
