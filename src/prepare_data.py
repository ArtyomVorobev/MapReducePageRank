import config as cfg

from mrjob.protocol import JSONProtocol


class Preprocessor:
    def __init__(self, data_path: str, output_path: str) -> None:
        self.data_path = data_path
        self.output_path = output_path
        self.json = JSONProtocol()

    def prepare_data(self) -> None:
        with open(self.data_path, encoding='utf-8') as file:
            categories = self.extract_categories_from(file)

        with open(self.output_path, 'w', encoding='utf-8') as out_file:
            self.write_categories_to(out_file, categories)

    @staticmethod
    def extract_categories_from(file) -> dict:
        categories = {}
        for line in file:
            links = line.split(' ')
            node_category = links[0].split('/')[-1]
            out_category = links[2].split('/')[-1]
            if node_category not in categories:
                categories[node_category] = []
            categories[node_category].append(out_category)
        return categories

    def write_categories_to(self, out_file, categories):
        nodes_values = {}
        for category in categories.keys():
            out_categories = {}
            cur_page_rank = 1/len(categories[category])
            for out_category in categories[category]:
                out_categories[out_category] = cur_page_rank
            nodes_values[category] = self.get_node_values(out_categories)
            out_file.write(self.json.write(category, nodes_values[category]).decode() + '\n')

    @staticmethod
    def get_node_values(outer_categories: dict, pr_score: float = 1.0) -> dict:
        node_values = {}
        if outer_categories:
            node_values['outer_links'] = sorted(outer_categories.items())
        node_values['pr_score'] = pr_score
        return node_values


if __name__ == '__main__':
    preprocessor = Preprocessor(cfg.DATA_PATH, cfg.OUTPUT_PATH)
    preprocessor.prepare_data()
