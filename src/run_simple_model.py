import argparse

from functools import reduce

from simple_model import SimpleModelPool

parser = argparse.ArgumentParser(description='Simple model which takes r_0 and a ttl and iterates for a certain number of cycles.')
parser.add_argument('n', type=int, help='Number of nodes')
parser.add_argument('r_0', type=float, help='Average number of infected next cycle per infected this cycle')
parser.add_argument('n_0', type=int, help='Initial number of infected')
parser.add_argument('ttl', type=int, help='Time to live before the infected becomes uninfected')
parser.add_argument('fatality_rate', type=float, help='Fatality rate per cycle')
parser.add_argument('n_iterations', type=int, help='Number of iterations to run')
parser.add_argument('-a', '--acquired', action='store_true', help='Applies acquired immunity')
parser.add_argument('-v', '--verbose', action='store_true', help='Show population status at every step')
parser.add_argument('-t', '--trials', type=int, default=1, help='Number of trials to run')

def run_simple_model_pool(n, r_0, n_0, ttl, fatality_rate, n_iterations, acquired_immunity, verbose):
    model = SimpleModelPool(n, r_0, n_0, ttl, fatality_rate, acquired_immunity=acquired_immunity)
    model.iterate(n_iterations, verbose=verbose)
    return model

def avg(ns):
    assert type(ns) == list
    return reduce(lambda acc, cum: acc + cum, ns) / len(ns)

args = parser.parse_args()
print('run_simple_model_pool({}, {}, {}, {}, {}, {}, {}, {})'\
    .format(args.n, args.r_0, args.n_0, args.ttl, args.fatality_rate, args.n_iterations, args.acquired, args.verbose))

rs = list()
cumulative_infected = list()
for i in range(0, args.trials):
    print('********************************************************************************')
    print('********************************* Trial {} *********************************'.format(i))
    print('********************************************************************************')
    model = run_simple_model_pool(args.n, args.r_0, args.n_0, args.ttl, args.fatality_rate, args.n_iterations, args.acquired, args.verbose)
    print(model.get_results())

    rs.append(model._cumulative_infected / model._cumulative_denominator)
    cumulative_infected.append(model._cumulative_infected)

print('\n\n********************************************************************************')
print('Average R: {}'.format(avg(rs)))
print('Average cumulative infected: {}'.format(avg(cumulative_infected)))
print('********************************************************************************\n\n')
