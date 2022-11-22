import config as cfg
from mrjob.job import MRJob

class MRPageRank(MRJob):
    def configure_args(self):
        super(MRPageRank, self).configure_args()
        self.add_passthru_arg(
            '--damping-factor', dest='damping_factor', default=0.85, type='float',
            help='The value of damping factor. Defaults to 0.85.')

        self.add_passthru_arg(
            '--iters', dest='iters', default=20, type='int',
            help='The number of iterations. Defaults to 20.')
            
    def map(self, node_id, node):
        pass

    def reduce(self, node_id, node_values):
        pass 

    def steps(self):
        return ([self.mr(mapper=self.map, reducer=self.reduce)]*self.options.iters)


if __name__ == '__main__':
    MRPageRank.run()
