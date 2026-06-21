import json
from solana.rpc.api import Client

# Using a public mainnet endpoint to fetch actual network block data
SOLANA_CLIENT = Client("https://api.mainnet-beta.solana.com")

def calculate_solana_fees(compute_units_requested=250000):
    """
    Calculates estimated base fee + recent priority fees on Solana.
    Standard transaction base fee is 5000 lamports.
    """
    try:
        # Fetch recent prioritization fees from the network
        response = SOLANA_CLIENT.get_recent_prioritization_fees()
        fees_list = response.value
        
        if fees_list:
            # Get the median fee per compute unit from recent blocks
            prioritization_fees = [f.prioritization_fee for f in fees_list]
            prioritization_fees.sort()
            median_fee_per_cu = prioritization_fees[len(prioritization_fees) // 2]
        else:
            median_fee_per_cu = 0
            
        # Standard Solana Base Fee = 5,000 Lamports
        base_fee_lamports = 5000
        # Priority Fee = Micro-lamports per CU * CU Requested / 1,000,000
        priority_fee_lamports = int((median_fee_per_cu * compute_units_requested) / 1000000)
        total_fee_lamports = base_fee_lamports + priority_fee_lamports
        
        result = {
            "status": "success",
            "base_fee_lamports": base_fee_lamports,
            "estimated_priority_fee_lamports": priority_fee_lamports,
            "total_estimated_fee_lamports": total_fee_lamports,
            "recommended_compute_unit_price": median_fee_per_cu
        }
        return result

    except Exception as e:
        return {"status": "error", "message": str(e)}

# Quick local test to make sure it runs perfectly
if __name__ == "__main__":
    print("Testing local agent script parameters...")
    fee_data = calculate_solana_fees()
    print(json.dumps(fee_data, indent=4))
