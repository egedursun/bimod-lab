
#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#

import matplotlib.pyplot as plt


unit_cost_per_response_cycle = 0.12  # $(USD)

NQ = 50
number_of_questions= [x for x in range(1, NQ+1)]

cost_per_question = []
total_costs = []
requirement_for_utility = []
for i in number_of_questions:
    tot_cost = 0
    for j in range(0, i):
        tot_cost += unit_cost_per_response_cycle * (j + 1)
    cost_per_question.append(tot_cost / i)
    total_costs.append(tot_cost)
    requirement_for_utility.append(1 / (tot_cost / i) * 15)

print(cost_per_question)
print(total_costs)


# build the plots for the cost per question and total cost
# use separate charts
plt.figure(figsize=(10, 5))
plt.plot(number_of_questions, cost_per_question, label='Cost per Question')
plt.xlabel('Number of Questions')
plt.ylabel('Cost per Question')
plt.title('Cost per Question vs Number of Questions')
plt.legend()
plt.grid()
plt.show()

plt.figure(figsize=(20, 10))
plt.plot(number_of_questions, requirement_for_utility, label='Marginal Value')
plt.plot(number_of_questions, total_costs, label='Total Cost')
plt.axvline(x=20, color='purple', linestyle='--', label='Line of Utility')
plt.axvline(x=15, color='r', linestyle='--', label='Line of Utility')
plt.axvline(x=10, color='orange', linestyle='--')
plt.axvline(x=5, color='g', linestyle='--')
plt.xlabel('Number of Questions')
plt.ylabel('Marginal Value (f(x))')
plt.yticks([x for x in range(0, 161, 5)])
plt.grid()
plt.legend([
    'Marginal Value',
    'Total Cost',
    'Line of Utility for Simple Tasks (~$3 per Chat)',
    'Line of Utility for Moderately Complex Tasks (~$8 per Chat)',
    'Line of Utility for Complex Tasks (~$15 per Chat)',
    'Line of Utility for Very Sensitive & Complex Tasks (~$25 per Chat)'])
plt.xticks([x for x in range(0, NQ+1, 1)])
plt.twinx()
plt.ylabel('Total Cost ($USD)')
plt.yticks([x for x in range(0, 101, 5)])
plt.title('Total Cost vs Number of Questions')
plt.show()
