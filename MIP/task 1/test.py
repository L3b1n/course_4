import pulp
import random

def generate_and_save_knapsack(n, C, seed=42, solver_name="HiGHS", output_file="knapsack_model.lp"):
    random.seed(seed)
    
    weights = [random.randint(1, 20) for _ in range(n)]
    values = [random.randint(10, 100) for _ in range(n)]
    
    model = pulp.LpProblem("Knapsack_Problem", pulp.LpMinimize)
    
    x = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(n)]
    model += pulp.lpSum(-values[i] * x[i] for i in range(n)), "Total_Value"
    model += pulp.lpSum(weights[i] * x[i] for i in range(n)) <= C, "Capacity_Constraint"
    model.writeLP(output_file)
    print(f"Модель сохранена в файл: {output_file}")
    
    solver = pulp.getSolver(solver_name)
    model.solve(solver)
    
    print(f"Status: {pulp.LpStatus[model.status]}")
    print(f"Общая стоимость: {pulp.value(model.objective)}")
    print("Выбранные предметы:")
    for i in range(n):
        if pulp.value(x[i]) == 1:
            print(f" - Предмет {i + 1}: вес = {weights[i]}, стоимость = {values[i]}")
    
    return output_file

if __name__ == "__main__":
    output_path = "knapsack_model_2.lp"
    generate_and_save_knapsack(n=10000, C=50000, output_file=output_path)
