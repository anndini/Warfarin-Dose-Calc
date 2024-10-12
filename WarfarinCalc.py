import tkinter as tk
from tkinter import messagebox

# Function to calculate Warfarin dose based on user inputs and genotyping
def calculate_dose():
    try:
        age = int(age_entry.get())
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        inr = float(inr_entry.get())
        genotype1 = genotype1_var.get()
        genotype2 = genotype2_var.get()
        vkorc1 = vkorc1_var.get()
        
        # CYP2C9 Allele Activity Scores
        activity_scores = {
            "CYP2C9*1": 1.0,  # Normal function
            "CYP2C9*2": 0.5,  # Decreased function
            "CYP2C9*3": 0.0   # No function
        }
        
        # Calculate CYP2C9 activity score based on genotype
        activity_score = activity_scores[genotype1] + activity_scores[genotype2]
        
        # Determine CYP2C9 metabolizer phenotype based on activity score
        if activity_score == 2.0:
            phenotype_cyp2c9 = "Normal/Extensive Metabolizer"
            dose_adjustment_cyp2c9 = 1.0  # No adjustment
        elif 1.0 <= activity_score < 2.0:
            phenotype_cyp2c9 = "Intermediate Metabolizer"
            dose_adjustment_cyp2c9 = 0.8  # Reduce dose by 20%
        else:
            phenotype_cyp2c9 = "Poor Metabolizer"
            dose_adjustment_cyp2c9 = 0.5  # Reduce dose by 50%
        
        # VKORC1 Genotype Dosing Adjustment
        vkorc1_adjustments = {
            "GG (Normal)": 1.0,     # No adjustment
            "AG (Low Expression)": 0.7,  # Reduce dose by 30%
            "AA (Very Low Expression)": 0.5  # Reduce dose by 50%
        }
        dose_adjustment_vkorc1 = vkorc1_adjustments[vkorc1]
        
        # Example base dose calculation logic for Warfarin (adjust based on guidelines)
        base_dose = (age * 0.2) + (weight * 0.1) + (height * 0.05) + (inr * 0.3)
        
        # Adjust the base dose by both CYP2C9 and VKORC1 factors
        adjusted_dose = base_dose * dose_adjustment_cyp2c9 * dose_adjustment_vkorc1
        
        result_label.config(
            text=f"Calculated Dose: {adjusted_dose:.2f} mg/day\n"
                 f"CYP2C9 Phenotype: {phenotype_cyp2c9}\n"
                 f"VKORC1 Adjustment: {vkorc1} ({dose_adjustment_vkorc1 * 100:.0f}% of base dose)"
        )
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

# Initialize the main application window
app = tk.Tk()
app.title("Warfarin Dosing Calculator (with CYP2C9 and VKORC1 Genotyping)")

# Input fields
tk.Label(app, text="Age (years):").grid(row=0, column=0)
age_entry = tk.Entry(app)
age_entry.grid(row=0, column=1)

tk.Label(app, text="Weight (kg):").grid(row=1, column=0)
weight_entry = tk.Entry(app)
weight_entry.grid(row=1, column=1)

tk.Label(app, text="Height (cm):").grid(row=2, column=0)
height_entry = tk.Entry(app)
height_entry.grid(row=2, column=1)

tk.Label(app, text="INR:").grid(row=3, column=0)
inr_entry = tk.Entry(app)
inr_entry.grid(row=3, column=1)

# Genotype selection for both CYP2C9 alleles
tk.Label(app, text="CYP2C9 Allele 1:").grid(row=4, column=0)
genotype1_var = tk.StringVar()
genotype1_var.set("CYP2C9*1")  # default value
genotype1_menu = tk.OptionMenu(app, genotype1_var, "CYP2C9*1", "CYP2C9*2", "CYP2C9*3")
genotype1_menu.grid(row=4, column=1)

tk.Label(app, text="CYP2C9 Allele 2:").grid(row=5, column=0)
genotype2_var = tk.StringVar()
genotype2_var.set("CYP2C9*1")  # default value
genotype2_menu = tk.OptionMenu(app, genotype2_var, "CYP2C9*1", "CYP2C9*2", "CYP2C9*3")
genotype2_menu.grid(row=5, column=1)

# VKORC1 Genotype selection
tk.Label(app, text="VKORC1 Genotype:").grid(row=6, column=0)
vkorc1_var = tk.StringVar()
vkorc1_var.set("GG (Normal)")  # default value
vkorc1_menu = tk.OptionMenu(app, vkorc1_var, "GG (Normal)", "AG (Low Expression)", "AA (Very Low Expression)")
vkorc1_menu.grid(row=6, column=1)

# Calculate button
calculate_button = tk.Button(app, text="Calculate Dose", command=calculate_dose)
calculate_button.grid(row=7, column=0, columnspan=2)

# Result label
result_label = tk.Label(app, text="Calculated Dose: ")
result_label.grid(row=8, column=0, columnspan=2)

# Run the application
app.mainloop()
