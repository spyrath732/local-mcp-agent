import duckdb
from mcp.server.fastmcp import FastMCP

# Αρχικοποίηση
mcp = FastMCP("EnergyAnalyticsServer")
DB_PATH = "energy_analytics.duckdb"

@mcp.tool()
def run_readonly_sql(query: str) -> str:
    """
    Εκτελεί ένα read-only SQL SELECT query στη βάση DuckDB.
    ΣΗΜΑΝΤΙΚΟ - Η βάση περιέχει τον πίνακα 'grid_generation' με τις εξής στήλες:
    - plant_id (VARCHAR): Κωδικός μονάδας
    - plant_name (VARCHAR): Όνομα μονάδας (π.χ. 'Ptolemaida V')
    - fuel_type (VARCHAR): Τύπος καυσίμου (π.χ. 'Lignite', 'Natural Gas', 'Wind', 'Solar')
    - region (VARCHAR): Περιοχή
    - generation_mwh (DOUBLE): Παραγωγή ενέργειας σε MWh
    - co2_tons (DOUBLE): Εκπομπές CO2 σε τόνους
    - recorded_date (DATE): Ημερομηνία καταγραφής
    Χρησιμοποίησε αποκλειστικά αυτόν τον πίνακα και αυτές τις στήλες για τα queries σου.
    """
    cleaned_query = query.strip().upper()
    if not cleaned_query.startswith("SELECT"):
        return "ERROR: Only SELECT statements are allowed."

    try:
        con = duckdb.connect(DB_PATH, read_only=True)
        result = con.execute(query).fetchall()
        columns = [desc[0] for desc in con.description]
        con.close()
        
        if not result:
            return "Query executed successfully, but returned 0 rows."
            
        header = " | ".join(columns)
        separator = "-" * len(header)
        rows = [" | ".join(str(val) for val in row) for row in result]
        return f"{header}\n{separator}\n" + "\n".join(rows)
    except Exception as e:
        return f"SQL Error: {str(e)}"

if __name__ == "__main__":
    mcp.run(transport="stdio")