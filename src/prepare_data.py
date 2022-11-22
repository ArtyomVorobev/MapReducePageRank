import config as cfg
import json

from mrjob.protocol import JSONProtocol


class Preprocessor:
    def __init__(self, data_path: str, output_path: str) -> None:
        self.data_path = data_path
        self.output_path = output_path
        self.json = JSONProtocol()

    def prepare_data(self) -> None:
        categories = {}
        with open(self.data_path, encoding='utf-8') as file:
            for line in file:
                links = line.split(' ')
                node_category = links[0].split('/')[-1]
                out_category = links[2].split('/')[-1]
                if node_category not in categories:
                    categories[node_category] = []
                categories[node_category].append(out_category)
        with open(self.output_path, 'w', encoding='utf-8') as out_file:
            for category in categories.keys():
                cur_categories = {}
                cur_page_rank = 1/len(categories[category])
                for out_category in categories[category]:
                    cur_categories[out_category] = (out_category, cur_page_rank)
            out_file.write(self.write_node(category, cur_categories))
                
    def write_node(self, node_category: str, outer_categories: dict, pr_score: float = 1.0) -> str:
        node = {}
        if outer_categories:
            node['outer_links'] = sorted(outer_categories.items())
        node['score'] = pr_score
        return self.json.write(node_category, node) + '\n'
       

if __name__ == '__main__':
    prepare_data(cfg.DATA_PATH, cfg.OUTPUT_PATH)