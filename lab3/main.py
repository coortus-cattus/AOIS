from logic_operator import LogicOperator
from truth_table import TruthTable
from opz_converter import OPZConverter
from sdnf_builder import SDNFBuilder
from sknf_builder import SKNFBuilder
from index_form import IndexForm
from minimizer import Minimizer
from menu import menu

from logic_processor import LogicProcessor

def main():
    current_processor = None
    while True:
        choice = menu()
        if choice == "1":
            expression = input("Enter function (use a,b,c,d,e and operators &,|,>,!,~): ")
            try:
                current_processor = LogicProcessor(expression)
                print("\nTruth table created!")
            except Exception as e:
                print(f"Error in expression: {e}")
        elif choice in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            if current_processor is None:
                print("Please enter a function first")
                continue
            if choice == "2":
                print(f"SDNF: {current_processor.sdnf_builder.build_sdnf()}")
            elif choice == "3":
                print(f"SKNF: {current_processor.sknf_builder.build_sknf()}")
            elif choice == "4":
                print(f"Index form (Decimal): {current_processor.index_form.compute_index()}")
            elif choice == "5":
                current_processor.minimizer.minimize_sdnf_raschetny(current_processor.sdnf_builder.get_minterms())
            elif choice == "6":
                current_processor.minimizer.minimize_sknf_raschetny(current_processor.sknf_builder.get_maxterms())
            elif choice == "7":
                current_processor.minimizer.minimize_sdnf_raschet_table(current_processor.sdnf_builder.get_minterms())
            elif choice == "8":
                current_processor.minimizer.minimize_sknf_raschet_table(current_processor.sknf_builder.get_maxterms())
            elif choice == "9":
                current_processor.minimizer.karnaugh_map_sdnf(current_processor.sdnf_builder.get_minterms())
            elif choice == "10":
                current_processor.minimizer.karnaugh_map_sknf(current_processor.sknf_builder.get_maxterms())
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Please select 1-11")

if __name__ == "__main__":
    main()