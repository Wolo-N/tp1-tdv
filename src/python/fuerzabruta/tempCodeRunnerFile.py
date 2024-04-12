
    #     # Convert breakpoint indices to actual coordinates for the best combination
    #     best_x = [grid_x[x[0]] for x in best_combination]
    #     best_y = [grid_y[y[1]] for y in best_combination]

    #     # Construct the solution dictionary
    #     solution = {
    #         'n': len(best_combination),
    #         'x': best_x,
    #         'y': best_y,
    #         'obj': 2
    #     }
    #     # Display the best solution
    #     print('\nBest Solution:', solution)

    # # Asegúrate de que el directorio exista
    #     solution_directory = 'data/solutions'
    #     if not os.path.exists(solution_directory):
    #         os.makedirs(solution_directory)

    #     solution_filename = os.path.join(solution_directory, f'solution_{instance_name}')
    #     try:
    #         with open(solution_filename, 'w') as f:
    #             json.dump(solution, f)
    #         print(f'Solution exported to {solution_filename}')
    #     except Exception as e:
    #         print(f"Error al guardar la solución: {e}")

    #     plot_graph(instance_name, m, n, N)