from Algorithm import Algorithm
import time
import matplotlib.pyplot as plt

def main():
    avg_runtime = 0
    avg_fitness = 0
    fitness_stddev = 0

    ind_fitness_list = []

    runs = 30
    run = 0
    algo = Algorithm()

    while run < runs:
        algo = Algorithm()

        start = time.time()
        ((ind, ind_fitness), fitness) = algo.run()

        avg_fitness += ind_fitness
        ind_fitness_list.append(ind_fitness)

        end = time.time()
        avg_runtime += (end-start)/runs
        run += 1

    avg_fitness /= runs
    fitness_stddev = sum([(x-avg_fitness)**2 for x in ind_fitness_list])/(runs-1)

    print("Avg. solution fitness:", avg_fitness)
    print("Std. dev. of the solutions' fitness:", fitness_stddev)

    plt.plot(range(algo.noIterations), fitness, label='Fitness vs iteration')

    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.title("Fitness evolution")
    plt.legend()
    plt.show()

    print("Avg. runtime:", float((end-start)*1000), "ms")

main()