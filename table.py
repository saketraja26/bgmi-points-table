import pandas as pd
import os

# Official BGMI Point System
POINT_SYSTEM = {1: 10, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 1, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}

# Team Data for Each Group
GROUP_A_TEAMS = [
    "AM BOYZZ Esports", "Team LOSS_X", "MITxSQUADUP", "BOB ESPORTS",
    "Team_OG", "Alpha_x", "TSM", "Team Gardians",
    "Team TED", "INSAS ESPORTS", "CFS ESPORTS", "XSPARK",
    "Team Swarajya", "Team Homelanders", "Team NV", "IMMORTAL THUNDERS"
]

GROUP_B_TEAMS = [
    "RushX", "ALPHA GAMING", "Team Arise", "97",
    "Team Trust", "Strawts", "Team Shadow", "Team Ethnic",
    "Curse breakers", "TEAM APEX", "1v4", "AERO SCISSORS ESPORTS",
    "Inferno 5", "6INE", "TEAM RAVEN ESPORTS", "SelfishPlayers"
]

GROUP_C_TEAMS = [
    "Team Wushang", "Team Xtreme", "Team Beast", "FST Fraggers",
    "VP GAMING", "Team_OG", "Chaos Knight", "KALKI ESPORTS",
    "Divas", "TEAM NS", "Team Nirbhay", "Team Sword",
    "Flow Esport", "Team Yaurus", "Team KUKD"
]

GROUPS = {
    'A': GROUP_A_TEAMS,
    'B': GROUP_B_TEAMS,
    'C': GROUP_C_TEAMS
}

def create_data_folders():
    """Create separate folders for each group's match data"""
    for group in ['A', 'B', 'C']:
        folder = f"Group_{group}_Data"
        if not os.path.exists(folder):
            os.makedirs(folder)

def add_match_data(group):
    """
    Prompts user for match data and saves it to a unique CSV for the specified group.
    """
    folder = f"Group_{group}_Data"
    files = [f for f in os.listdir(folder) if f.startswith(f'group_{group}_match_') and f.endswith('.csv')]
    match_no = len(files) + 1
    
    teams_data = []
    print(f"\n{'='*70}")
    print(f"  ENTERING MATCH DATA FOR GROUP {group} - MATCH {match_no}")
    print(f"{'='*70}")
    print(f"\nTeams in Group {group}:")
    for idx, team in enumerate(GROUPS[group], 1):
        print(f"  {idx}. {team}")
    print()
    
    num_teams = len(GROUPS[group])
    
    for i in range(1, num_teams + 1):
        print(f"\n--- Rank {i} ---")
        name = input(f"Team Name: ").strip()
        kills = int(input(f"Kills for {name}: "))
        
        teams_data.append({
            'Group': group,
            'Team': name,
            'Rank': i,
            'Kills': kills,
            'WWCD': 1 if i == 1 else 0,
            'PLCT': POINT_SYSTEM.get(i, 0)
        })
    
    df = pd.DataFrame(teams_data)
    filepath = os.path.join(folder, f"group_{group}_match_{match_no}.csv")
    df.to_csv(filepath, index=False)
    print(f"\n✓ Match {match_no} for Group {group} saved successfully!")
    print(f"  Saved to: {filepath}\n")

def generate_group_leaderboard(group):
    """
    Reads all match CSVs for a specific group and generates the leaderboard.
    """
    folder = f"Group_{group}_Data"
    if not os.path.exists(folder):
        print(f"No data folder found for Group {group}.")
        return None
    
    files = [f for f in os.listdir(folder) if f.startswith(f'group_{group}_match_') and f.endswith('.csv')]
    
    if not files:
        print(f"No match data available for Group {group}.")
        return None

    # Combine all match data
    all_matches = pd.concat([pd.read_csv(os.path.join(folder, f)) for f in files])
    
    # Aggregate data by Team
    leaderboard = all_matches.groupby('Team').agg({
        'WWCD': 'sum',
        'PLCT': 'sum',
        'Kills': 'sum'
    }).reset_index()

    # Calculate Total
    leaderboard['TOTAL'] = leaderboard['PLCT'] + leaderboard['Kills']
    leaderboard['Group'] = group
    
    # Sort by Total, then Kills, then WWCD (Tie-breaker rules)
    leaderboard = leaderboard.sort_values(by=['TOTAL', 'Kills', 'WWCD'], ascending=False)
    
    # Add Rank Column
    leaderboard.insert(0, 'RANK', range(1, len(leaderboard) + 1))
    
    return leaderboard

def display_group_leaderboard(group):
    """Display leaderboard for a specific group"""
    leaderboard = generate_group_leaderboard(group)
    
    if leaderboard is None:
        return
    
    print("\n" + "="*75)
    print(f"  GROUP {group} POINTS TABLE")
    print("="*75)
    print(f"{'RANK':<6} {'TEAM NAME':<30} {'WWCD':<6} {'PLCT.':<6} {'KILLS':<6} {'TOTAL':<6}")
    print("-" * 75)
    
    for _, row in leaderboard.iterrows():
        wwcd_display = int(row['WWCD']) if row['WWCD'] > 0 else ""
        print(f"{int(row['RANK']):<6} {row['Team']:<30} {wwcd_display:<6} {int(row['PLCT']):<6} {int(row['Kills']):<6} {int(row['TOTAL']):<6}")
    print("="*75 + "\n")

def generate_combined_leaderboard():
    """
    Generates a combined leaderboard from all groups.
    """
    all_leaderboards = []
    
    for group in ['A', 'B', 'C']:
        lb = generate_group_leaderboard(group)
        if lb is not None:
            all_leaderboards.append(lb)
    
    if not all_leaderboards:
        print("No match data available for any group.")
        return
    
    # Combine all groups
    combined = pd.concat(all_leaderboards, ignore_index=True)
    
    # Sort by Total, then Kills, then WWCD
    combined = combined.sort_values(by=['TOTAL', 'Kills', 'WWCD'], ascending=False)
    
    # Reset Rank
    combined['RANK'] = range(1, len(combined) + 1)
    
    print("\n" + "="*85)
    print("  COMBINED POINTS TABLE - ALL GROUPS")
    print("="*85)
    print(f"{'RANK':<6} {'TEAM NAME':<30} {'GROUP':<7} {'WWCD':<6} {'PLCT.':<6} {'KILLS':<6} {'TOTAL':<6}")
    print("-" * 85)
    
    for _, row in combined.iterrows():
        wwcd_display = int(row['WWCD']) if row['WWCD'] > 0 else ""
        print(f"{int(row['RANK']):<6} {row['Team']:<30} {row['Group']:<7} {wwcd_display:<6} {int(row['PLCT']):<6} {int(row['Kills']):<6} {int(row['TOTAL']):<6}")
    print("="*85 + "\n")

def view_all_group_leaderboards():
    """Display all three group leaderboards"""
    for group in ['A', 'B', 'C']:
        display_group_leaderboard(group)

def main_menu():
    """Main menu for the points table system"""
    create_data_folders()
    
    while True:
        print("\n" + "="*60)
        print("  BGMI TOURNAMENT POINTS TABLE SYSTEM")
        print("="*60)
        print("1. Add Match Data for Group A")
        print("2. Add Match Data for Group B")
        print("3. Add Match Data for Group C")
        print("4. View Group A Standings")
        print("5. View Group B Standings")
        print("6. View Group C Standings")
        print("7. View All Groups Standings")
        print("8. View Combined Leaderboard (All Groups)")
        print("9. Exit")
        print("="*60)
        
        choice = input("\nSelect Option: ").strip()

        if choice == '1':
            add_match_data('A')
        elif choice == '2':
            add_match_data('B')
        elif choice == '3':
            add_match_data('C')
        elif choice == '4':
            display_group_leaderboard('A')
        elif choice == '5':
            display_group_leaderboard('B')
        elif choice == '6':
            display_group_leaderboard('C')
        elif choice == '7':
            view_all_group_leaderboards()
        elif choice == '8':
            generate_combined_leaderboard()
        elif choice == '9':
            print("\nExiting... Goodbye!")
            break
        else:
            print("\n⚠ Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()