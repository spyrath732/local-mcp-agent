import duckdb

def init_db():
    con = duckdb.connect("energy_analytics.duckdb")
    
    con.execute("""
        CREATE OR REPLACE TABLE grid_generation (
            plant_id VARCHAR,
            plant_name VARCHAR,
            fuel_type VARCHAR,
            region VARCHAR,
            generation_mwh DOUBLE,
            co2_tons DOUBLE,
            recorded_date DATE
        )
    """)
    
    con.execute("""
        INSERT INTO grid_generation VALUES
        ('PLT-01', 'Ptolemaida V', 'Lignite', 'Western Macedonia', 4200.5, 3850.0, '2026-11-15'),
        ('PLT-02', 'Megalopoli CCGT', 'Natural Gas', 'Peloponnese', 3150.0, 1260.0, '2026-11-15'),
        ('PLT-03', 'Kafireas Wind Park', 'Wind', 'Central Greece', 1890.2, 0.0, '2026-11-15'),
        ('PLT-04', 'Kozani Solar Hub', 'Solar', 'Western Macedonia', 1420.8, 0.0, '2026-11-15'),
        ('PLT-05', 'Agios Nikolaos CCGT', 'Natural Gas', 'Central Greece', 3600.0, 1440.0, '2026-11-16'),
        ('PLT-06', 'Kafireas Wind Park', 'Wind', 'Central Greece', 2150.4, 0.0, '2026-11-16'),
        ('PLT-07', 'Kozani Solar Hub', 'Solar', 'Western Macedonia', 980.0, 0.0, '2026-11-16')
    """)
    
    print("Database 'energy_analytics.duckdb' initialized successfully!")
    con.close()

if __name__ == "__main__":
    init_db()