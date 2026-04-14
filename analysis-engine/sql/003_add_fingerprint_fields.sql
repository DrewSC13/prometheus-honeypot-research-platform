ALTER TABLE session_features
ADD COLUMN IF NOT EXISTS fp_vector JSONB,
ADD COLUMN IF NOT EXISTS fingerprint_label TEXT;