import os
import json
import joblib
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from ml.preprocess import PlacementPreprocessor

def train_and_save_model(csv_path, output_dir='ml/model_versions'):
    print(f"Starting training pipeline with dataset: {csv_path}")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}")
        
    df = pd.read_csv(csv_path)
    
    # Needs 'placed' binary target column
    if 'placed' not in df.columns:
        raise ValueError("Dataset must contain a 'placed' target column (0 or 1).")
        
    X = df.drop('placed', axis=1)
    y = df['placed']
    
    # Create an sklearn Pipeline
    pipeline = Pipeline([
        ('preprocessor', PlacementPreprocessor()),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    print("Fitting model...")
    pipeline.fit(X, y)
    
    # Evaluate
    score = pipeline.score(X, y)
    print(f"Training Accuracy: {score:.4f}")
    
    # Save versioned model
    os.makedirs(output_dir, exist_ok=True)
    version = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"placement_model_{version}.pkl"
    model_path = os.path.join(output_dir, model_filename)
    
    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")
    
    # Save metadata
    metadata = {
        "version": version,
        "training_date": datetime.now().isoformat(),
        "accuracy": score,
        "dataset_size": len(df)
    }
    with open(os.path.join(output_dir, f"metadata_{version}.json"), "w") as f:
        json.dump(metadata, f, indent=2)
        
    # Update symlink / overwrite main pkl
    main_model_path = os.path.join(os.path.dirname(output_dir), 'placement_model.pkl')
    try:
        if os.path.exists(main_model_path) and os.path.islink(main_model_path):
            os.remove(main_model_path)
        # For cross-platform, just copy or save another reference
        joblib.dump(pipeline, main_model_path)
        print(f"Updated main model at {main_model_path}")
    except Exception as e:
        print(f"Could not update main model link: {e}")
        
    return version

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        train_and_save_model(sys.argv[1])
    else:
        print("Usage: python train_model.py <path_to_dataset.csv>")
