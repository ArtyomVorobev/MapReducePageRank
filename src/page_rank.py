from mrjob.job import MRJob
from mrjob.protocol import JSONProtocol
from mrjob.step import MRStep


class MRPageRank(MRJob):

    INPUT_PROTOCOL = JSONProtocol

    def configure_args(self):
        super(MRPageRank, self).configure_args()
        self.add_passthru_arg(
            '--damping-factor', dest='damping_factor', default=0.85, type=float,
            help='The value of damping factor. Defaults to 0.85.')

        self.add_passthru_arg(
            '--iters', dest='iters', default=20, type=int,
            help='The number of iterations. Defaults to 20.')

    def map(self, node_category, node_values):
        yield node_category, ('node', node_values)
        if "outer_links" in node_values:
            for outer_link, link_score in node_values["outer_links"]:
                yield outer_link, ('pr_score', node_values['pr_score'] * link_score)

    def reduce(self, node_category, node_values):
        node = {}
        total_pr = 0
        prev_score_set = False

        for value_type, value in node_values:
            if value_type == 'node':
                node = value
                if not prev_score_set:
                    node['previous'] = node['pr_score']
                    prev_score_set = True
            elif value_type == 'pr_score':
                total_pr += value

        node['pr_score'] = 1 - self.options.damping_factor + self.options.damping_factor * total_pr
        yield node_category, node

    def steps(self):
        return [MRStep(mapper=self.map, reducer=self.reduce)]*self.options.iters


if __name__ == '__main__':
    MRPageRank.run()
