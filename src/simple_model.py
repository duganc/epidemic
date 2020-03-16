import random


class SimpleModelPool():

    def __init__(
        self,
        n,
        r_0,
        n_0,
        ttl,
        fatality_rate,
        acquired_immunity=False,
        immunity_rate=0.0,
        immunity_scalar=0.0
    ):
        assert type(n) == int
        assert n > 0
        assert type(r_0) == float
        assert r_0 > 0.0
        assert type(n_0) == int
        assert 0 < n_0 <= n
        assert type(ttl) == int
        assert ttl > 0
        assert type(fatality_rate) == float
        assert 0.0 <= fatality_rate <= 1.0
        assert type(acquired_immunity) == bool
        assert type(immunity_rate) == float
        assert 0.0 <= immunity_rate <= 1.0
        assert type(immunity_scalar) == float
        assert 0.0 <= immunity_scalar <= 1.0

        self.n = n
        self.r_0 = r_0
        self.p = r_0 / float(n)
        self.n_0 = n_0
        self.ttl = ttl
        self.fatality_rate = fatality_rate
        self.immunity_rate = immunity_rate
        self.immunity_scalar = immunity_scalar

        self._cumulative_infected = 0
        self._cumulative_denominator = 0
        self._infected_at_t = list()

        immunities = [self._adjust_for_immunity(random.random()) * immunity_scalar for i in range(0, n)]

        self._pool = [SimpleModelNode(True, self.ttl, immunities[i], acquired_immunity) for i in range(0, n_0)] + [SimpleModelNode(False, self.ttl, immunities[i], acquired_immunity) for i in range(n_0, n)]

    def __str__(self):
        return str([i.to_symbol() for i in self._pool])

    def __repr__(self):
        str(self)

    def get_results(self):
        to_return = list()
        to_return.append('Newly infected at:')
        for t in range(0, len(self._infected_at_t)):
            to_return.append('{}: {}'.format(t, self._infected_at_t[t]))

        to_return.append('')
        to_return.append('Cumulative Infected: {}'.format(self._cumulative_infected))
        to_return.append('R_0: {}'.format(self._cumulative_infected / self._cumulative_denominator))
        return '\n'.join(to_return)

    def get_n_infected(self):
        return len(i for i in self._pool if i.is_infected())

    def iterate(self, t, verbose=False):
        assert type(t) == int
        assert t > 0
        assert type(verbose) == bool

        for i in range(0, t):
            print('********************************* Iteration {} *********************************'.format(i))
            infected_pool = [n for n in self._pool if n.is_infected()]
            self._infected_at_t.append(len(infected_pool))

            if verbose:
                print('b: {}'.format(self))

            for node in infected_pool:
                self._cumulative_denominator += 1
                self.try_infect_pool()

            print('r_0 = {} / {} = {}'.format(self._cumulative_infected, self._cumulative_denominator, self._cumulative_infected/self._cumulative_denominator))
            if verbose:
                print('a: {}'.format(self))

            print('n_newly_infected: {}'.format(self._infected_at_t[i]))

            died = list()
            for node in infected_pool:
                if random.random() <= self.fatality_rate:
                    died.append(node)
            print('n_died: {}'.format(len(died)))

            self._pool = [n for n in self._pool if n not in died]

            n_recovered = 0
            for node in infected_pool:
                recovered = node.advance_ttl()
                n_recovered += (1 if recovered else 0)

            print('n_recovered: {}'.format(n_recovered))

            if verbose:
                print('r: {}'.format(self))

    def try_infect_pool(self):
        for node in self._pool:

            newly_infected = node.maybe_infect(self.p)
            if newly_infected:
                self._cumulative_infected += 1

    def _adjust_for_immunity(self, x):
        return (1.0 if x <= (1.0 - self.immunity_rate) else 0.0)


class SimpleModelNode:

    def __init__(self, is_infected, ttl, immunity, acquired_immunity=False):
        assert type(is_infected) == bool
        assert type(ttl) == int
        assert ttl > 0
        assert type(immunity) == float
        assert 0.0 <= immunity <= 1.0
        assert type(acquired_immunity) == bool

        self._is_infected = is_infected

        self.ttl = ttl
        self.timer = ttl

        self.immunity = immunity
        self.acquired_immunity = acquired_immunity

    def __str__(self):
        return 'Node({}, immunity={})'.format(self._is_infected, self.immunity)

    def __repr__(self):
        return str(self)

    def to_symbol(self):
        if self.is_infected():
            return '*'
        if self.immunity > 0.99:
            return '^'
        return '_'

    def is_infected(self):
        return self._is_infected

    def maybe_infect(self, p):
        assert type(p) == float
        assert 0.0 <= p <= 1.0

        if self.is_infected():
            return False

        infect = True if random.random() <= p * (1 - self.immunity) else False
        if infect:
            self._is_infected = True
            self.timer = self.ttl
        return infect

    def advance_ttl(self):
        self.timer -= 1
        if self.timer <= 0:
            self._is_infected = False
            if self.acquired_immunity:
                self.immunity = 1.0
            return True
        else:
            return False
